"""Independent product/variable/surface coverage reconciliation."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from analysis.alternative_validation_ancestry import row_ids
from analysis.alternative_validation_io import (
    csv_records,
    decode,
    ordered_hash,
    require_columns,
)
from analysis.data_io import DATASET, Json

GATES = frozenset({"GATED_DATA", "NOT_APPLICABLE_DOMAIN", "INSUFFICIENT_TRAINING",
                   "INSUFFICIENT_INNER_FOLDS"})


def coverage_checks(root: Path, output: Path) -> dict[str, Json]:
    catalog = {r["CASE_ID"]: r for r in csv_records(
        root / DATASET / "cases/verification_cases.csv")}
    statuses = [r for r in csv_records(output / "case_method_status.csv.gz")
                if r["surface"] != "joint"]
    schedule = {(r["case_id"], r["method_id"]): r
                for r in csv_records(output / "fit_schedule.csv") if r["surface"] == "joint"}
    for original in csv_records(output / "joint_key_status.csv.gz"):
        row = dict(original)
        plan = schedule[(row["case_id"], row["method_id"])]
        components = row_ids(row.get("component_case_ids") or plan["component_case_ids"])
        cases = [catalog[key] for key in components]
        if len(cases) < 2 or len({c["PRODUCT"] for c in cases}) != 1:
            raise AssertionError("invalid joint coverage component scope")
        row.update(PRODUCT=cases[0]["PRODUCT"], VARIABLE=json.dumps(
            [f'{c["VARIABLE"]}:{c["LEAD"]}' for c in cases], separators=(",", ":")))
        statuses.append(row)
    groups: dict[tuple[str, ...], list[dict[str, str]]] = {}
    for row in statuses:
        case = catalog[row["case_id"]] if row["surface"] != "joint" else row
        key = (case["PRODUCT"], case["VARIABLE"], row["method_id"], row["surface"])
        groups.setdefault(key, []).append(row)
    scored = {(r.get("case_id") or r["joint_id"], r["method_id"])
              for name in ("continuous", "category", "joint")
              for r in csv_records(output / f"{name}_predictions.csv.gz")}
    path = output / "coverage_and_failures.csv"
    if not path.exists():
        path = output / "reports/coverage_and_failures.csv"
    coverage = csv_records(path)
    require_columns(coverage, ("PRODUCT", "VARIABLE", "method_id", "surface",
                              "eligible_count", "scored_count", "status_counts",
                              "success_mask_hash"), "grouped failure coverage")
    observed = {r["CASE_ID"] for r in csv_records(root / "outputs/matched_predictions.csv.gz")}
    inventory = {r["method_id"]: r for r in csv_records(output / "method_inventory.csv")}
    indexed = {(r["case_id"], r["method_id"]): r for r in statuses}
    seen: set[tuple[str, ...]] = set()
    for row in coverage:
        key = tuple(row[k] for k in ("PRODUCT", "VARIABLE", "method_id", "surface"))
        if key in seen:
            raise AssertionError(f"duplicate/unknown coverage group {key}")
        seen.add(key)
        domain = True
        if row["surface"] != "joint":
            spec = inventory[row["method_id"]]
            domain = (spec["domain"] == "both" or
                      (spec["domain"] == "temperature" and row["VARIABLE"] == "t15m") or
                      (spec["domain"] == "precipitation" and row["VARIABLE"] == "prcp"))
            relevant = [indexed.get((case_id, row["method_id"]), {
                "case_id": case_id, "method_id": row["method_id"], "surface": row["surface"],
                "status": "UNRECORDED"}) for case_id, case in catalog.items()
                if (case["PRODUCT"], case["VARIABLE"]) == key[:2]]
        else:
            relevant = groups[key]
        counts = Counter(r["status"] for r in relevant)
        eligible = [r["case_id"] for r in relevant if r["status"] not in
                    GATES | {"TARGET_UNAVAILABLE"} and
                    domain and (r["surface"] == "joint" or r["case_id"] in observed)]
        successes = [r["case_id"] for r in relevant if r["case_id"] in eligible and
                     r["status"] == "OK" and (r["case_id"], r["method_id"]) in scored]
        expected = {
            "supplied_count": len(relevant), "eligible_count": len(eligible),
            "scored_count": len(successes), "scientific_gates": sum(counts[g] for g in GATES),
            "fit_failures": counts["FIT_FAILED"] + counts["POSTERIOR_DIAGNOSTICS_FAILED"],
            "numerical_or_score_failures": counts["NUMERICAL_DISTRIBUTION_FAILED"] + counts["SCORE_FAILED"],
            "scientific_support_gates": counts["INSUFFICIENT_TRAINING"] + counts["INSUFFICIENT_INNER_FOLDS"],
            "input_conflicts": counts["INPUT_CONFLICT"], "unrecorded_count": counts["UNRECORDED"],
            "domain_eligible_count": (len(relevant)-counts["NOT_APPLICABLE_DOMAIN"]
                                      if row["surface"] == "joint"
                                      else len(relevant) if domain else 0),
            "missing_targets": (sum(r["case_id"] not in observed for r in relevant)
                                if row["surface"] != "joint" and domain
                                else counts["TARGET_UNAVAILABLE"]),
            "score_missing_after_OK": sum(r["status"] == "OK" and r["case_id"] in eligible and
                                          (r["case_id"], r["method_id"]) not in scored
                                          for r in relevant),
        }
        if row["surface"] == "joint":
            del expected["score_missing_after_OK"]
        for column, value in expected.items():
            if int(row[column]) != value:
                raise AssertionError(f"{key}: {column}={row[column]}, expected {value}")
        if decode(row["status_counts"]) != dict(counts):
            raise AssertionError(f"{key}: terminal status counts differ")
        if row_ids(row["eligible_ids"]) != sorted(eligible):
            raise AssertionError(f"{key}: eligible case IDs differ")
        if row["success_mask_hash"] != ordered_hash(sorted(successes)):
            raise AssertionError(f"{key}: scored success-mask hash differs")
    if not groups.keys() <= seen:
        raise AssertionError(f"coverage omitted groups {sorted(groups.keys() - seen)}")
    return {"status": "PASS", "coverage_groups": len(seen),
            "terminal_records": len(statuses), "group_keys": "PRODUCT,VARIABLE,method_id,surface"}
