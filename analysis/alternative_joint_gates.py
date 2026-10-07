"""Factual coupling gates and aligned annual input validation."""

from __future__ import annotations

import numpy as np

from analysis.alternative_contracts import AlternativeError, JointTrainingSet


def receipt_open(training: JointTrainingSet, gate: str) -> bool:
    return any(
        receipt.allowed and bool(receipt.evidence_refs)
        and (receipt.counts.get("gate_id") == gate or receipt.reason_code.startswith(gate))
        for receipt in training.gate_receipts
    )


def check_training(training: JointTrainingSet) -> None:
    """No target truth is accessible, and complete vectors retain every original row."""
    n, d = len(training.source_years), len(training.component_keys)
    if n < 10:
        raise AlternativeError("INSUFFICIENT_JOINT_YEARS", str(n))
    if d < 2 or len(training.targets) != d:
        raise AlternativeError("INVALID_JOINT_DIMENSION", str(d))
    if len(set(training.source_years)) != n:
        raise AlternativeError("DUPLICATE_JOINT_YEAR", str(training.source_years))
    if training.forecast_means.shape != (n, d) or training.observations.shape != (n, d):
        raise AlternativeError("INVALID_JOINT_SHAPE", f"Expected {(n, d)}")
    if not np.isfinite(training.forecast_means).all() or not np.isfinite(training.observations).all():
        raise AlternativeError("NONFINITE_JOINT_INPUT", training.train_hash)
    for i, year in enumerate(training.source_years):
        rows = training.rows_by_year[year]
        if len(rows) != d or len({row.source_init for row in rows}) != 1:
            raise AlternativeError("INCOMPLETE_ANNUAL_VECTOR", str(year))
        for j, row in enumerate(rows):
            target = training.targets[j]
            if row.source_year != year or row.variable != target.variable or row.lead != target.lead:
                raise AlternativeError("MISALIGNED_ANNUAL_VECTOR", row.row_id)
            if row.product != target.product or row.hist_end >= training.cutoff:
                raise AlternativeError("JOINT_TIME_LEAKAGE", row.row_id)
            if row.source_case_init > training.catalog_cutoff or row.source_year in training.held_out_years:
                raise AlternativeError("JOINT_CATALOG_LEAKAGE", row.row_id)
            if any(row.hist_start.year <= y <= row.hist_end.year for y in training.held_out_years):
                raise AlternativeError("JOINT_VALID_YEAR_LEAKAGE", row.row_id)
            if not np.isclose(np.mean(row.ensemble), training.forecast_means.item(i, j), rtol=0, atol=1e-10):
                raise AlternativeError("JOINT_MEAN_MISMATCH", row.row_id)
            if row.observation != training.observations[i, j]:
                raise AlternativeError("JOINT_RESPONSE_MISMATCH", row.row_id)
            if target.variable == "prcp" and (row.observation < 0 or np.any(row.ensemble < 0)):
                raise AlternativeError("NEGATIVE_RAIN", row.row_id)


def check_physical(training: JointTrainingSet, path: bool = False) -> None:
    if not receipt_open(training, "G3"):
        raise AlternativeError("G3_PHYSICAL_IDENTITY_UNPROVED", "Structural MEMBER labels are insufficient.")
    if path and len({target.lead for target in training.targets}) < 2:
        raise AlternativeError("DECC_REQUIRES_PATH", "At least two different lead windows are required.")


def check_dynamic(training: JointTrainingSet) -> None:
    if len(training.source_years) < 20:
        raise AlternativeError("G6_INSUFFICIENT_BLOCK_YEARS", "Two blocks each require ten years.")
    rows = [row for year in training.source_years for row in training.rows_by_year[year]]
    same_catalog = len({row.source_case_init for row in rows}) == 1
    eras = {row.archive_era for row in rows}
    if not receipt_open(training, "G6") and not (same_catalog and len(eras) == 1 and "" not in eras):
        raise AlternativeError("G6_VINTAGE_COMPARABILITY_UNPROVED", "Require one documented archive cohort.")
