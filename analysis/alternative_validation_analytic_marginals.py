"""Every separately issued analytic joint marginal, never a discarded scalar alias."""

from __future__ import annotations

from pathlib import Path

from analysis.alternative_validation_ancestry import row_ids
from analysis.alternative_validation_io import (
    csv_records,
    mapping,
    require_columns,
    text,
)
from analysis.alternative_validation_saved_law import saved_law_checks
from analysis.data_io import Json

type MarginalKey = tuple[str, str, str, str]


def marginal_key(record: dict[str, Json]) -> MarginalKey:
    return (text(record["joint_id"]), text(record["case_id"]),
            text(record["method_id"]), text(record["fit_ref"]))


def analytic_checks(output: Path, records: list[dict[str, Json]]) -> dict[str, Json]:
    specs: dict[MarginalKey, dict[str, Json]] = {}
    for record in records:
        key = marginal_key(record)
        if not all(key) or key in specs:
            raise AssertionError("duplicate/empty analytic joint marginal identity")
        specs[key] = mapping(record["distribution"])
    rows = csv_records(output / "joint_analytic_marginals.csv.gz")
    if rows:
        require_columns(rows, ("joint_id", "case_id", "method_id", "fit_ref", "surface",
                               "variable", "OBS", "Q33", "Q67", "PRED_MEAN", "CRPS",
                               "P_BN", "P_NN", "P_AN", "P05", "P95", "BRIER", "RPS"),
                        "analytic joint marginals")
    joint = {(r["joint_id"], r["method_id"]): r
             for r in csv_records(output / "joint_predictions.csv.gz")}
    fits = {r["fit_ref"]: r for r in csv_records(output / "fit_ledger.csv.gz")}
    seen: set[MarginalKey] = set()
    references: list[Json] = []
    for row in rows:
        key = (row["joint_id"], row["case_id"], row["method_id"], row["fit_ref"])
        if key in seen:
            raise AssertionError("duplicate analytic joint marginal score object")
        seen.add(key)
        if row["surface"] != "analytic" or not row["method_id"].endswith("__analytic_marginal"):
            raise AssertionError("joint analytic law mislabeled as scalar/scenario projection")
        parent_method = row["method_id"].removesuffix("__analytic_marginal")
        parent = joint[(row["joint_id"], parent_method)]
        if row["case_id"] not in row_ids(parent["component_case_ids"]):
            raise AssertionError("analytic marginal has foreign joint component")
        fit = fits[row["fit_ref"]]
        if (row["fit_ref"] != parent["fit_ref"] or fit["status"] != "OK"
                or fit["method_id"] != parent_method):
            raise AssertionError("analytic marginal lacks genuine successful parent fit identity")
        expected = saved_law_checks(row, specs[key])
        if len(references) < 32:
            references.append({"joint_id": key[0], "case_id": key[1], "method_id": key[2],
                               "fit_ref": key[3], **expected})
    if seen != specs.keys():
        raise AssertionError("analytic joint marginal laws and scores do not exactly match")
    return {"status": "PASS", "analytic_joint_marginals": len(seen),
            "independent_expected_reference_examples": references}
