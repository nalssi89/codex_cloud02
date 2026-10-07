"""Byte-preserved baseline score objects and actual issued finite marginal laws."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from analysis.alternative_validation_io import csv_records, json_lines, mapping, text
from analysis.alternative_validation_oracles import close, floats
from analysis.alternative_validation_reference import vector
from analysis.data_io import Json


def baseline_checks(root: Path, output: Path) -> dict[str, Json]:
    old = csv_records(root / "outputs/matched_predictions.csv.gz")
    original = {(row["CASE_ID"], row["METHOD"].lower()): row for row in old}
    current = csv_records(output / "continuous_predictions.csv.gz")
    copied = {(row["case_id"], row["method_id"].lower()): row for row in current
              if row["method_id"].lower() in {"raw", "qm", "qdm", "emos"}}
    if copied.keys() != original.keys():
        raise AssertionError("unchanged baseline control records are incomplete")
    fields = ("OBS", "PRED_MEAN", "CRPS", "Q33", "Q67", "P_BN", "P_NN", "P_AN",
              "P05", "P95", "BRIER", "RPS")
    for key, row in original.items():
        for field in fields:
            # Saved decimal strings may be parsed/reformatted, but values cannot change.
            close(float(copied[key][field]), float(row[field]),
                  f"unchanged baseline {key}/{field}", atol=1e-12, rtol=1e-12)
    original_members: dict[tuple[str, str], Counter[float]] = {}
    for row in csv_records(root / "outputs/calibrated_members.csv.gz"):
        original_members.setdefault((row["CASE_ID"], row["METHOD"].lower()), Counter())[
            float(row["VALUE"])] += 1
    checked_laws = 0
    for record in json_lines(output / "distribution_specs.jsonl.gz"):
        method = text(record["method_id"]).lower()
        if method not in {"raw", "qm", "qdm", "emos"}:
            continue
        key = text(record["case_id"]), method
        spec = mapping(record["distribution"])
        if method == "emos":
            if spec.get("tag") != "normal":
                raise AssertionError("baseline analytic EMOS replaced with finite quantiles")
            parameters = floats(vector(spec["parameters"]))
            close(parameters[0], float(original[key]["EMOS_MU"]), "baseline latent mu",
                  atol=1e-12, rtol=1e-12)
            close(parameters[1], float(original[key]["EMOS_SIGMA"]), "baseline latent sigma",
                  atol=1e-12, rtol=1e-12)
        else:
            if spec.get("tag") != "weighted_empirical":
                raise AssertionError("baseline actual issued member law was replaced")
            values, weights = floats(vector(spec["values"])), floats(vector(spec["weights"]))
            members = original_members[key]
            if set(values) != members.keys():
                raise AssertionError("baseline issued members changed")
            count = sum(members.values())
            for value, weight in zip(values, weights, strict=True):
                close(weight, members[value]/count, "baseline issued member mass", atol=1e-12)
        checked_laws += 1
    if checked_laws != len(original):
        raise AssertionError("baseline control distribution coverage incomplete")
    return {"status": "PASS", "baseline_score_records": len(original),
            "baseline_issued_laws": checked_laws,
            "tight_QDM_warning": "RETAINED_NO_TOLERANCE_RELAXATION"}
