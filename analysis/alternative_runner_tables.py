"""Runnable exhaustive statistical comparison, preserving the published baseline."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence

from analysis.alternative_contracts import (
    CaseInput,
    MethodSpec,
)
from analysis.alternative_experiment_types import ExperimentInputs
from analysis.alternative_runner_engine import (
    COUPLING_IDS,
)
from analysis.alternative_runner_io import (
    Row,
    dumps,
)
from analysis.alternative_runner_types import Work
from analysis.data_io import Json

FAILURES = frozenset(("FIT_FAILED", "POSTERIOR_DIAGNOSTICS_FAILED", "NUMERICAL_DISTRIBUTION_FAILED"))

def table_row(value: Json) -> Row:
    if not isinstance(value, dict):
        raise TypeError("Saved table record must be an json_object")
    result: Row = {}
    for key, item in value.items():
        result[key] = dumps(item) if isinstance(item, (list, dict)) else item
    return result


def json_object(value: Json) -> dict[str, Json]:
    if not isinstance(value, dict):
        raise TypeError("Saved JSON record must be an json_object")
    return value


def json_objects(value: Json) -> list[dict[str, Json]]:
    if not isinstance(value, list):
        raise TypeError("Saved JSON records must be an array")
    return [json_object(item) for item in value]


def registry_rows(registry: tuple[MethodSpec, ...], statuses: Sequence[Row]) -> list[Row]:
    rows: list[Row] = []
    for spec in registry:
        selected = [row for row in statuses if row["method_id"] == spec.id]
        rows.append({
            "method_id": spec.id, "family_no": spec.family_no, "subtype": spec.subtype,
            "domain": spec.domain, "surface": spec.surface, "fit_scope": spec.fit_scope,
            "owner": spec.owner, "algorithm_version": spec.algorithm_version,
            "fixed_parameters": dumps(spec.fixed_parameters), "gate_ids": dumps(spec.gate_ids),
            "attempted_count": sum(row["status"] not in {
                "NOT_APPLICABLE_DOMAIN", "TARGET_UNAVAILABLE", "GATED_DATA"} for row in selected),
            "ok_count": sum(row["status"] == "OK" for row in selected),
            "failure_count": sum(row["status"] in FAILURES for row in selected),
            "gate_count": sum(row["status"] == "GATED_DATA" for row in selected),
            "evidence_refs": ".omo/evidence/alternative-input-applicability.md",
        })
    for spec in registry:
        if spec.id in COUPLING_IDS:
            for marginal in ("emos", "bjp"):
                identifier = f"{spec.id}__{marginal}"
                rows.append({
                    "method_id": identifier, "family_no": spec.family_no,
                    "subtype": spec.subtype, "domain": spec.domain, "surface": "joint",
                    "fit_scope": "joint", "owner": spec.owner,
                    "algorithm_version": spec.algorithm_version,
                    "fixed_parameters": dumps({**spec.fixed_parameters, "marginal_method": marginal}),
                    "gate_ids": dumps(spec.gate_ids), "parent_method_id": spec.id,
                    "variant": "fixed marginal sensitivity, not extra researched subtype",
                })
    return rows


def joint_case_statuses(cases: tuple[CaseInput, ...], specs: tuple[MethodSpec, ...],
                         work: Sequence[Work], results: Sequence[dict[str, Json]],
                         inputs: ExperimentInputs) -> list[Row]:
    groups: dict[tuple[str, str], list[Row]] = defaultdict(list)
    for item, result in zip(work, results, strict=True):
        if item.joint_training is None:
            continue
        status = table_row(result["status"])
        for target in item.joint_training.targets:
            groups[(target.case_id, item.spec.id)].append(status)
    statuses: list[Row] = []
    priority = ("OK", "NUMERICAL_DISTRIBUTION_FAILED", "POSTERIOR_DIAGNOSTICS_FAILED",
                "FIT_FAILED", "INPUT_CONFLICT", "INSUFFICIENT_INNER_FOLDS",
                "INSUFFICIENT_TRAINING", "GATED_DATA", "NOT_APPLICABLE_DOMAIN")
    for target in cases:
        for spec in specs:
            if spec.surface != "joint":
                continue
            row: Row = {"case_id": target.case_id, "method_id": spec.id, "surface": "joint",
                        "fit_ref": "", "status": "", "reason_code": "",
                        "aggregation": "OK if any dimension-matched key succeeds; see joint_key_status"}
            if target.case_id not in inputs.truths:
                row.update(status="TARGET_UNAVAILABLE",
                           reason_code=inputs.excluded_cases.get(target.case_id, "TARGET_UNAVAILABLE"))
            elif spec.domain == "temperature" and target.variable != "t15m":
                row.update(status="NOT_APPLICABLE_DOMAIN", reason_code="TEMPERATURE_ONLY")
            else:
                matching = groups.get((target.case_id, spec.id), [])
                if matching:
                    chosen = min(matching, key=lambda record: priority.index(str(record["status"]))
                                 if str(record["status"]) in priority else len(priority))
                    row.update(status=chosen["status"], reason_code=chosen["reason_code"],
                               fit_ref=chosen["fit_ref"], joint_key_count=len(matching))
                else:
                    row.update(status="INSUFFICIENT_TRAINING",
                               reason_code="NO_AVAILABLE_ALIGNED_COMPANION_HISTORY")
            statuses.append(row)
    return statuses


def collect(results: Sequence[dict[str, Json]], key: str) -> list[Row]:
    return [table_row(result[key]) for result in results if key in result]
