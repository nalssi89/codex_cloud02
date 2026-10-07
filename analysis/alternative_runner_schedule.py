"""Runnable exhaustive statistical comparison, preserving the published baseline."""

from __future__ import annotations

from pathlib import Path

from analysis.alternative_contracts import (
    CaseInput,
    JointTrainingSet,
    MethodSpec,
)
from analysis.alternative_data import aligned_joint
from analysis.alternative_runner_engine import (
    COUPLING_IDS,
    Engine,
    joint_keys,
)
from analysis.alternative_runner_io import (
    Row,
    digest,
    dumps,
    known_input,
    write_rows,
)
from analysis.alternative_runner_types import Work


def build_schedule(engine: Engine, cases: tuple[CaseInput, ...],
              specs: tuple[MethodSpec, ...], all_cases: tuple[CaseInput, ...],
              output: Path) -> tuple[list[Work], list[Row], list[JointTrainingSet]]:
    """Construct complete workload and actual outer/inner content hashes BEFORE fits."""
    work: list[Work] = []
    rows: list[Row] = []
    joint_sets: list[JointTrainingSet] = []
    for target in cases:
        for spec in specs:
            if spec.surface == "joint":
                continue
            item = Work(spec=spec, target=target)
            work.append(item)
            row: Row = {"case_id": target.case_id, "method_id": spec.id, "surface": spec.surface,
                        "fit_scope": spec.fit_scope, "train_hash": "", "fit_ref": "",
                        "inner_fold_hashes": "[]", "known_input_hash": digest(known_input(target)),
                        "posterior_censor_rows": 0, "planned_status": "ATTEMPT"}
            wrong_domain = (
                (spec.domain == "temperature" and target.variable != "t15m")
                or (spec.domain == "precipitation" and target.variable != "prcp")
            )
            if target.case_id not in engine.inputs.truths:
                row["planned_status"] = "TARGET_UNAVAILABLE"
            elif wrong_domain:
                row["planned_status"] = "NOT_APPLICABLE_DOMAIN"
            else:
                training = engine.cache.get(target, spec.fit_scope)
                n_rows, n_years, censor_rows = engine.training_counts(training)
                row.update({
                    "train_hash": training.train_hash,
                    "fit_ref": engine.fit_key(spec, training, (target,)),
                    "n_rows": n_rows,
                    "n_years": n_years,
                    "inner_fold_hashes": dumps(tuple(f.ancestor_hash for f in engine.schedule_folds(
                        spec, training))),
                    "inner_fold_role": "actual algorithm candidates" if
                    spec.id in {"bma_component_pool", "cdf_mix_cv", "tweedie_selected_p"} else "no inner fits",
                    "posterior_censor_rows": censor_rows,
                })
            rows.append(row)
    joint_specs = tuple(spec for spec in specs if spec.surface == "joint")
    selected_ids = {target.case_id for target in cases}
    if joint_specs:
        keys = {tuple(t.case_id for t in targets): targets for targets in joint_keys(all_cases)}
        # Partial future horizons are additional targets, not replacement full paths.
        available = tuple(target for target in all_cases if target.case_id in engine.inputs.historical)
        keys.update({tuple(t.case_id for t in targets): targets for targets in joint_keys(available)})
        for targets in (keys[key] for key in sorted(keys)):
            if not any(target.case_id in selected_ids for target in targets):
                continue
            missing = any(target.case_id not in engine.inputs.historical for target in targets)
            if missing:
                # Source future/absent-history components remain in a separate manifest.
                rows.append({
                    "case_id": digest([t.case_id for t in targets])[:24],
                    "method_id": "*joint_key*", "surface": "joint",
                    "component_case_ids": dumps(tuple(t.case_id for t in targets)),
                    "planned_status": "TARGET_UNAVAILABLE", "fit_ref": "", "train_hash": "",
                    "reason_code": "COMPONENT_HISTORY_OR_TARGET_UNAVAILABLE",
                })
                continue
            training = aligned_joint(targets, engine.inputs)
            joint_sets.append(training)
            for spec in joint_specs:
                marginals = ("emos", "bjp") if spec.id in COUPLING_IDS else ("",)
                for marginal in marginals:
                    modified = MethodSpec(
                        id=spec.id, family_no=spec.family_no, subtype=spec.subtype,
                        domain=spec.domain, surface=spec.surface, fit_scope=spec.fit_scope,
                        algorithm_version=spec.algorithm_version, owner=spec.owner,
                        fixed_parameters={**spec.fixed_parameters, "marginal_method": marginal}
                        if spec.id in COUPLING_IDS else spec.fixed_parameters,
                        gate_ids=spec.gate_ids,
                    )
                    work.append(Work(spec=spec, joint_training=training, marginal=marginal))
                    rows.append({
                        "case_id": digest(list(training.component_keys))[:24],
                        "method_id": f"{spec.id}__{marginal}" if marginal else spec.id,
                        "surface": "joint", "fit_scope": "joint",
                        "component_case_ids": dumps(training.component_keys),
                        "train_hash": training.train_hash,
                        "fit_ref": engine.fit_key(modified, training, targets, marginal),
                        "n_rows": len(training.source_years), "n_years": len(training.source_years),
                        "dimension": len(targets), "planned_status": "ATTEMPT",
                        "posterior_censor_rows": sum(
                            training.observations.item(i) == 0
                            for i in range(training.observations.size)),
                        "known_input_hash": digest([known_input(t) for t in targets]),
                    })
    write_rows(output / "fit_schedule.csv", rows,
               ("case_id", "method_id", "surface", "train_hash", "fit_ref", "planned_status"))
    return work, rows, joint_sets
