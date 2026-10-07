"""Every saved scalar and analytic joint law, with exact surface coverage."""

from __future__ import annotations

import math
from collections.abc import Callable
from pathlib import Path

import numpy as np

from analysis.alternative_validation_analytic_marginals import analytic_checks
from analysis.alternative_validation_category import category_score
from analysis.alternative_validation_io import (
    csv_records,
    json_lines,
    mapping,
    require_columns,
    require_metadata,
    sha256,
    text,
)
from analysis.alternative_validation_oracles import close
from analysis.alternative_validation_saved_law import saved_law_checks
from analysis.calibration import FloatArray
from analysis.data_io import Json

__all__ = ["category_score", "joint_self_checks", "score_checks"]


def score_checks(output: Path) -> dict[str, Json]:
    records = list(json_lines(output / "distribution_specs.jsonl.gz"))
    specs: dict[tuple[str, str], dict[str, Json]] = {}
    analytic: list[dict[str, Json]] = []
    for record in records:
        require_metadata(record, ("case_id", "method_id", "distribution", "fit_ref"),
                         "saved distribution")
        if "joint_id" in record:
            analytic.append(record)
            continue
        key = text(record["case_id"]), text(record["method_id"])
        if key in specs:
            raise AssertionError("duplicate saved scalar law")
        specs[key] = record
    continuous = csv_records(output / "continuous_predictions.csv.gz")
    if continuous:
        require_columns(continuous, ("case_id", "method_id", "variable", "OBS", "Q33", "Q67",
                                    "PRED_MEAN", "CRPS", "P_BN", "P_NN", "P_AN", "P05", "P95",
                                    "BRIER", "RPS", "fit_ref"), "continuous predictions")
    keys: set[tuple[str, str]] = set()
    references: list[Json] = []
    for row in continuous:
        key = row["case_id"], row["method_id"]
        if key in keys:
            raise AssertionError("duplicate continuous prediction")
        keys.add(key)
        record = specs[key]
        if record["fit_ref"] != row["fit_ref"]:
            raise AssertionError("scalar saved-law/score fit identity mismatch")
        expected = saved_law_checks(row, mapping(record["distribution"]))
        if len(references) < 32:
            references.append({"case_id": key[0], "method_id": key[1], **expected})
    if keys != specs.keys():
        raise AssertionError("saved scalar laws and scored predictions do not match")
    analytic_receipt = analytic_checks(output, analytic)
    categories = csv_records(output / "category_predictions.csv.gz")
    if categories:
        require_columns(categories, ("case_id", "method_id", "OBS", "Q33", "Q67",
                                     "P_BN", "P_NN", "P_AN", "BRIER", "RPS"), "categories")
    for row in categories:
        if any(row.get(field) for field in ("PRED_MEAN", "CRPS", "P05", "P95")):
            raise AssertionError("category-only row fabricates continuous fields")
        if (row["case_id"], row["method_id"]) in specs:
            raise AssertionError("category-only law masquerades as continuous CDF")
        category_score(row)
    joint = csv_records(output / "joint_predictions.csv.gz")
    if joint:
        require_columns(joint, ("joint_id", "method_id", "scenario_key", "units",
                               "approximation_metadata"), "joint rows")
    loaders: list[Callable[..., object]] = [np.load]
    archive = loaders[0](output / "joint_scenarios.npz", allow_pickle=False)
    if not isinstance(archive, np.lib.npyio.NpzFile):
        raise TypeError("joint scenario shard must be NPZ")
    with archive as shard:
        for row in joint:
            scenarios: FloatArray = np.asarray(shard[row["scenario_key"]], dtype=np.float64)
            if scenarios.ndim != 2 or not np.all(np.isfinite(scenarios)):
                raise AssertionError("joint scenarios invalid")
            if not row["units"] or not row["approximation_metadata"]:
                raise AssertionError("joint original-unit/approximation labels missing")
    statuses = csv_records(output / "case_method_status.csv.gz")
    expected_keys = {(r["case_id"], r["method_id"]) for r in statuses
                     if r["status"] == "OK" and r.get("surface") == "continuous"}
    if expected_keys != keys:
        raise AssertionError("OK continuous ledger does not exactly cover saved predictions")
    return {"status": "PASS", "saved_laws": len(records), "scalar_saved_laws": len(specs),
            "continuous_scores": len(continuous), "analytic_joint_laws": analytic_receipt,
            "category_scores": len(categories), "joint_predictions": len(joint),
            "oracle": "SC2_INDEPENDENT_SCIPY_CDF_AND_EXPECTATION",
            "reference_source_sha256": sha256(Path(__file__).with_name(
                "alternative_validation_reference.py")),
            "independent_expected_reference_examples": references}


def joint_self_checks() -> dict[str, Json]:
    independent = np.array([[-1., -1.], [-1., 1.], [1., -1.], [1., 1.]])
    correlated = np.array([[-1., -1.], [1., 1.]])
    def energy(samples: np.ndarray) -> float:
        observation = np.array([1., 1.])
        first = float(np.mean(np.linalg.norm(samples-observation, axis=1)))
        pair = float(np.mean(np.linalg.norm(samples[:, None]-samples[None, :], axis=2)))
        return first-pair/2
    independent_score, correlated_score = energy(independent), energy(correlated)
    if math.isclose(independent_score, correlated_score, abs_tol=.01):
        raise AssertionError("energy oracle cannot distinguish dependence")
    independent_event = float(np.mean(np.all(independent > 0, axis=1)))
    correlated_event = float(np.mean(np.all(correlated > 0, axis=1)))
    close(independent_event, .25, "independent joint event")
    close(correlated_event, .5, "correlated joint event")
    return {"status": "PASS", "independent_energy": independent_score,
            "correlated_energy": correlated_score}
