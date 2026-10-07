"""Real dispatch, conservative fit sharing, and complete prediction checkpoints."""

from __future__ import annotations

from time import perf_counter

import numpy as np

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    CategoryFitResult,
    CategoryPrediction,
    ContinuousPrediction,
    FitDiagnostics,
    FitStatus,
    MethodSpec,
    TrainingSet,
)
from analysis.alternative_data import gate_report
from analysis.alternative_distributions import (
    distribution_from_spec,
)
from analysis.alternative_runner_engine_base import EngineBase
from analysis.alternative_runner_io import (
    Row,
    digest,
    json_value,
    known_input,
    write_json,
)
from analysis.alternative_runner_scoring import (
    identity,
    score_categories,
    score_continuous,
)
from analysis.alternative_validation_io import read_json
from analysis.data_io import Json


class EngineScalar(EngineBase):
    resume_hits: int
    def scalar(self, target: CaseInput, spec: MethodSpec) -> dict[str, Json]:
        started = perf_counter()
        status: Row = {"case_id": target.case_id, "method_id": spec.id,
                       "surface": spec.surface, "fit_ref": "", "status": "OK", "reason_code": ""}
        result: dict[str, Json] = {"status": json_value(status), "elapsed_seconds": 0.0}
        if target.case_id not in self.inputs.truths:
            status.update(status="TARGET_UNAVAILABLE",
                          reason_code=self.inputs.excluded_cases.get(target.case_id, "TARGET_UNAVAILABLE"))
            result["status"] = json_value(status)
            return result
        if ((spec.domain == "temperature" and target.variable != "t15m")
                or (spec.domain == "precipitation" and target.variable != "prcp")):
            status.update(status="NOT_APPLICABLE_DOMAIN", reason_code="VARIABLE_DOMAIN")
            result["status"] = json_value(status)
            return result
        training: TrainingSet | None = None
        stage = "fit"
        try:
            training = self.cache.get(target, spec.fit_scope)
            key = self.fit_key(spec, training, (target,))
            prediction_key = digest([key, known_input(target), "prediction-v1"])
            status["fit_ref"] = key
            path = self.output / "cache" / f"{prediction_key}.json"
            gate = gate_report(spec, training, self.inputs)
            result["gate"] = json_value(gate)
            result["training_hash"] = training.train_hash
            if not gate.allowed:
                status.update(status="INSUFFICIENT_TRAINING" if gate.reason_code == "INSUFFICIENT_TRAINING"
                              else "GATED_DATA", reason_code=gate.reason_code)
            else:
                saved = read_json(path) if self.resume and path.exists() else None
                if saved is not None:
                    if saved.get("prediction_key") != prediction_key or saved.get("fit_ref") != key:
                        raise AlternativeError("CACHE_IDENTITY_CONFLICT", path.name)
                    with self.lock:
                        self.resume_hits += 1
                    result["fit"] = saved["fit"]
                    cached_status = saved["status"]
                    if not isinstance(cached_status, dict):
                        raise TypeError("Invalid checkpoint status")
                    status.update(status=str(cached_status["status"]),
                                  reason_code=str(cached_status["reason_code"]))
                elif spec.owner == "baseline":
                    law = self.baseline_law(target, spec, training)
                    saved = {"distribution": law.to_spec()}
                    result["fit"] = self.record_fit(
                        spec.id, key, "OK", training.train_hash, FitDiagnostics(
                            convergence=True, n_rows=len(training.rows),
                            n_years=len({row.source_year for row in training.rows}),
                            train_hash=training.train_hash,
                            message="Eligible annual climatology" if spec.id == "climatology_empirical"
                            else "Published protected original baseline; unchanged scores and law",
                        ), law.to_spec, spec=spec,
                    )
                else:
                    fit = self.fit_scalar(spec, training, key)
                    status.update(status=str(fit.status), reason_code=fit.reason_code)
                    result["fit"] = self.record_fit(
                        spec.id, key, str(fit.status), training.train_hash, fit.diagnostics,
                        fit.fitted_model.to_spec if fit.fitted_model is not None else None, spec=spec,
                    )
                    saved = {}
                    if fit.status == FitStatus.OK:
                        stage = "prediction"
                        if isinstance(fit, CategoryFitResult):
                            if fit.fitted_model is None:
                                raise ValueError("OK category fit lacks model")
                            prediction = fit.fitted_model.predict(target, training.thresholds)
                            saved["probabilities"] = json_value(prediction.probabilities)
                        else:
                            if fit.fitted_model is None:
                                raise ValueError("OK continuous fit lacks model")
                            law = fit.fitted_model.predict(target)
                            saved["distribution"] = law.to_spec()
                if status["status"] == "OK":
                    stage = "score"
                    truth = self.inputs.truths[target.case_id]
                    common = identity(target, spec.id, key, len(training.rows))
                    if spec.surface == "category":
                        probabilities = np.asarray(saved["probabilities"], dtype=np.float64)
                        category_prediction = CategoryPrediction(
                            case_id=target.case_id, method_id=spec.id, fit_ref=key,
                            thresholds=training.thresholds, probabilities=probabilities,
                        )
                        result["category"] = json_value({
                            **common, **score_categories(category_prediction, truth),
                        })
                    else:
                        distribution = saved["distribution"]
                        if not isinstance(distribution, dict):
                            raise TypeError("Invalid saved law")
                        law = distribution_from_spec(distribution)
                        continuous_prediction = ContinuousPrediction(
                            case_id=target.case_id, method_id=spec.id, fit_ref=key, distribution=law,
                        )
                        scores = score_continuous(continuous_prediction, truth)
                        if spec.id in {"RAW", "QM", "QDM", "EMOS"}:
                            published = self.baseline[(target.case_id, spec.id)]
                            for column in ("OBS", "Q33", "Q67", "PRED_MEAN", "CRPS",
                                           "P_BN", "P_NN", "P_AN", "BRIER", "RPS"):
                                if not np.isclose(float(str(published[column])), float(str(scores[column])),
                                                  rtol=1e-12, atol=1e-12):
                                    raise AlternativeError("BASELINE_SCORE_CHANGED", column)
                            scores = {**published,
                                      "CONTRACT_P05": law.quantile(np.array([0.05])).item(),
                                      "CONTRACT_P95": law.quantile(np.array([0.95])).item()}
                        result["continuous"] = json_value({**scores, **common})
                        result["law"] = {"case_id": target.case_id, "method_id": spec.id,
                                         "fit_ref": key, "distribution": distribution}
                # A checkpoint is complete only after prediction/scoring validation.
                # It stores NO observed target and NO scores; resume re-scores the law.
                if not (self.resume and path.exists()):
                    write_json(path, {**saved, "fit": result.get("fit"),
                                      "status": status, "fit_ref": key,
                                      "prediction_key": prediction_key})
        except (AlternativeError, ValueError, TypeError, FloatingPointError,
                OverflowError, np.linalg.LinAlgError) as error:
            code = error.code if isinstance(error, AlternativeError) else type(error).__name__
            failure = ("INSUFFICIENT_TRAINING" if code.startswith("INSUFFICIENT") else
                       "INPUT_CONFLICT" if code in {"INPUT_CONFLICT", "CACHE_IDENTITY_CONFLICT"}
                       or code.startswith("BASELINE_") else
                       "NUMERICAL_DISTRIBUTION_FAILED" if stage != "fit" else "FIT_FAILED")
            status.update(status=failure, reason_code=code, message=str(error))
            _ = result.pop("continuous", None)
            _ = result.pop("category", None)
            _ = result.pop("law", None)
            if "fit" not in result and training is not None:
                result["fit"] = {"method_id": spec.id, "fit_ref": status["fit_ref"],
                                 "train_hash": training.train_hash, "status": failure,
                                 "diagnostics": {"message": str(error)}}
        result["status"] = json_value(status)
        result["elapsed_seconds"] = perf_counter() - started
        return result
