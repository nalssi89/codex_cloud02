"""Real dispatch, conservative fit sharing, and complete prediction checkpoints."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import replace

import numpy as np

from analysis.alternative_bayes import fit_mbjp
from analysis.alternative_contracts import (
    AlternativeError,
    ContinuousPrediction,
    FitStatus,
    JointFitResult,
    JointPrediction,
    JointTrainingSet,
    MethodSpec,
    PredictiveDistribution,
    TrainingSet,
)
from analysis.alternative_data import gate_report
from analysis.alternative_distributions import (
    distribution_from_spec,
    weighted_empirical,
)
from analysis.alternative_experiment_types import JointTruth
from analysis.alternative_joint import fit_joint
from analysis.alternative_joint_folds import component_training
from analysis.alternative_joint_marginals import fit_bjp_marginal, fit_emos_marginal
from analysis.alternative_runner_engine_base import COUPLING_IDS
from analysis.alternative_runner_io import (
    Row,
    digest,
    dumps,
    json_value,
    write_json,
)
from analysis.alternative_runner_scalar import EngineScalar
from analysis.alternative_runner_scoring import (
    identity,
    score_continuous,
    score_joint,
)
from analysis.alternative_validation_io import read_json
from analysis.data_io import Json


class Engine(EngineScalar):
    resume_hits: int
    def joint(self, training: JointTrainingSet, spec: MethodSpec,
              marginal: str) -> dict[str, Json]:
        targets = training.targets
        joint_id = digest([target.case_id for target in targets])[:24]
        method_id = f"{spec.id}__{marginal}" if spec.id in COUPLING_IDS else spec.id
        modified = replace(spec, fixed_parameters={**spec.fixed_parameters,
                                                  "marginal_method": marginal}) if (
            spec.id in COUPLING_IDS) else spec
        key = self.fit_key(modified, training, targets, marginal)
        status: Row = {"case_id": joint_id, "method_id": method_id, "surface": "joint",
                       "fit_ref": key, "status": "OK", "reason_code": ""}
        result: dict[str, Json] = {"status": json_value(status), "joint_train_hash": training.train_hash}
        path = self.output / "cache" / f"{key}.json"
        stage = "fit"
        try:
            gate = gate_report(spec, training, self.inputs)
            result["gate"] = json_value(gate)
            if spec.domain == "temperature" and any(t.variable != "t15m" for t in targets):
                status.update(status="NOT_APPLICABLE_DOMAIN", reason_code="TEMPERATURE_ONLY")
            elif any(target.case_id not in self.inputs.truths for target in targets):
                status.update(status="TARGET_UNAVAILABLE", reason_code="COMPONENT_TARGET_UNAVAILABLE")
            elif not gate.allowed:
                status.update(status="GATED_DATA", reason_code=gate.reason_code)
            else:
                config = self.fit_config(modified, training.train_hash)
                saved = read_json(path) if self.resume and path.exists() else None
                if saved is None:
                    fit: JointFitResult = (
                        fit_mbjp(modified, training, config) if spec.owner == "bayes"
                        else fit_joint(modified, training, None, config)
                    )
                    status.update(status=str(fit.status), reason_code=fit.reason_code)
                    result["fit"] = self.record_fit(
                        method_id, key, str(fit.status), training.train_hash, fit.diagnostics,
                        fit.fitted_model.to_spec if fit.fitted_model is not None else None, spec=modified,
                    )
                    saved = dict[str, Json]()
                    if fit.status == FitStatus.OK:
                        if fit.fitted_model is None:
                            raise ValueError("OK joint fit lacks model")
                        stage = "prediction"
                        marginals: tuple[PredictiveDistribution, ...] = ()
                        if spec.id in COUPLING_IDS:
                            fitter = fit_bjp_marginal if marginal == "bjp" else fit_emos_marginal
                            marginals = tuple(
                                fitter(component_training(training, j), config).predict(target)
                                for j, target in enumerate(targets)
                            )
                            saved["analytic_marginals"] = [law.to_spec() for law in marginals]
                        prediction = fit.fitted_model.predict(targets, marginals, config)
                        saved.update({
                            "samples": json_value(prediction.samples),
                            "weights": json_value(prediction.weights),
                            "marginal_refs": list(prediction.marginal_refs),
                            "approximation_metadata": dict(prediction.approximation_metadata),
                        })
                        # MBJP exact marginal laws are emitted by its own model, not EMOS.
                        exact = prediction.approximation_metadata.get("exact_marginal_specs")
                        if isinstance(exact, list):
                            saved["analytic_marginals"] = exact
                else:
                    if saved.get("fit_ref") != key:
                        raise AlternativeError("CACHE_IDENTITY_CONFLICT", path.name)
                    cached_status = saved["status"]
                    if not isinstance(cached_status, dict):
                        raise TypeError("Invalid checkpoint status")
                    status.update(status=str(cached_status["status"]),
                                  reason_code=str(cached_status["reason_code"]))
                    result["fit"] = saved["fit"]
                    with self.lock:
                        self.resume_hits += 1
                if status["status"] == "OK":
                    stage = "score"
                    metadata = saved["approximation_metadata"]
                    refs = saved["marginal_refs"]
                    if not isinstance(metadata, dict) or not isinstance(refs, list):
                        raise TypeError("Invalid checkpoint joint metadata")
                    prediction = JointPrediction(
                        joint_id=joint_id, method_id=method_id, component_case_ids=tuple(
                            target.case_id for target in targets),
                        samples=np.asarray(saved["samples"], dtype=np.float64),
                        weights=np.asarray(saved["weights"], dtype=np.float64),
                        marginal_refs=tuple(str(ref) for ref in refs),
                        approximation_metadata=metadata, fit_ref=key,
                    )
                    truth = JointTruth(
                        observations=np.asarray([self.inputs.truths[t.case_id].observation for t in targets]),
                        centers=np.mean(training.observations, axis=0),
                        scales=np.maximum(1.0, np.std(training.observations, axis=0, ddof=1)),
                        thresholds=tuple(self.inputs.truths[t.case_id].thresholds for t in targets),
                    )
                    row = score_joint(prediction, truth)
                    variables = [target.variable for target in targets]
                    if len(targets) == 2 and set(variables) == {"t15m", "prcp"}:
                        temperature, rain = variables.index("t15m"), variables.index("prcp")
                        event = (
                            (prediction.samples[:, temperature] > truth.thresholds[temperature].item(1))
                            & (prediction.samples[:, rain] <= truth.thresholds[rain].item(0))
                        )
                        probability = float(prediction.weights @ event)
                        occurred = float(
                            truth.observations.item(temperature) > truth.thresholds[temperature].item(1)
                            and truth.observations.item(rain) <= truth.thresholds[rain].item(0)
                        )
                        row.update(HOT_DRY_P=probability, HOT_DRY_BRIER=(probability - occurred)**2)
                    row.update({
                        "joint_id": joint_id, "method_id": method_id, "fit_ref": key,
                        "scenario_key": f"s_{key}", "weights_key": f"w_{key}",
                        "component_case_ids": dumps(prediction.component_case_ids),
                        "variables": dumps(variables),
                        "units": dumps(["degC" if variable == "t15m" else "mm" for variable in variables]),
                        "approximation_metadata": dumps(metadata),
                        "marginal_refs": dumps(prediction.marginal_refs),
                        "PRODUCT": targets[0].product, "INIT_DATE": targets[0].init.isoformat(),
                        "dimension": len(targets), "N_TRAIN": len(training.source_years),
                    })
                    result["joint"] = json_value(row)
                    result["samples"] = saved["samples"]
                    result["weights"] = saved["weights"]
                    scenario_rows: list[Json] = []
                    analytic_rows: list[Json] = []
                    laws: list[Json] = []
                    exact_specs = saved.get("analytic_marginals", [])
                    for j, target in enumerate(targets):
                        law = weighted_empirical(prediction.samples[:, j], prediction.weights)
                        projected_id = f"{method_id}__scenario_marginal"
                        common = identity(target, projected_id, key, len(training.source_years))
                        scalar_prediction = ContinuousPrediction(
                            case_id=target.case_id, method_id=projected_id, fit_ref=key, distribution=law,
                        )
                        scenario_rows.append(json_value({
                            **common, "joint_id": joint_id, "surface": "scenario_projected",
                            **score_continuous(scalar_prediction, self.inputs.truths[target.case_id]),
                        }))
                        if isinstance(exact_specs, list) and j < len(exact_specs):
                            law_spec = exact_specs[j]
                            if not isinstance(law_spec, dict):
                                raise TypeError("Invalid analytic marginal law")
                            analytic_id = f"{method_id}__analytic_marginal"
                            exact_law = distribution_from_spec(law_spec)
                            exact_prediction = ContinuousPrediction(
                                case_id=target.case_id, method_id=analytic_id,
                                fit_ref=key, distribution=exact_law,
                            )
                            analytic_rows.append(json_value({
                                **identity(target, analytic_id, key, len(training.source_years)),
                                "joint_id": joint_id, "surface": "analytic",
                                **score_continuous(exact_prediction, self.inputs.truths[target.case_id]),
                            }))
                            laws.append({"case_id": target.case_id, "method_id": analytic_id,
                                         "joint_id": joint_id, "fit_ref": key, "distribution": law_spec})
                    result["scenario_marginals"] = scenario_rows
                    result["analytic_marginals"] = analytic_rows
                    result["marginal_laws"] = laws
                if not (self.resume and path.exists()):
                    write_json(path, {**saved, "status": status, "fit": result.get("fit"), "fit_ref": key})
        except (AlternativeError, ValueError, TypeError, FloatingPointError,
                OverflowError, np.linalg.LinAlgError) as error:
            code = error.code if isinstance(error, AlternativeError) else type(error).__name__
            status.update(status="NUMERICAL_DISTRIBUTION_FAILED" if stage != "fit" else "FIT_FAILED",
                          reason_code=code, message=str(error))
            for name in ("joint", "samples", "weights", "scenario_marginals", "analytic_marginals",
                         "marginal_laws"):
                _ = result.pop(name, None)
            if "fit" not in result:
                result["fit"] = {"method_id": method_id, "fit_ref": key,
                                 "status": status["status"], "train_hash": training.train_hash,
                                 "diagnostics": {"message": str(error)}}
        result["status"] = json_value(status)
        return result

    def scalar_training_sets(self) -> Iterator[TrainingSet]:
        seen: set[str] = set()
        for training in (*self.cache.local.values(), *self.cache.pooled.values()):
            if training.train_hash in seen:
                continue
            seen.add(training.train_hash)
            yield training
