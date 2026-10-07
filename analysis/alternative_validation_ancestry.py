"""Read-only row-level date, pool and fold ancestry validation."""

from __future__ import annotations

from calendar import monthrange
from datetime import date, timedelta
from pathlib import Path

import numpy as np

from analysis.alternative_validation_io import (
    csv_records,
    decode,
    number,
    require_columns,
)
from analysis.alternative_validation_reference import vector
from analysis.alternative_validation_training_wire import (
    row_ids,
    training_digest,
    year_block,
    years,
)
from analysis.data_io import Json

__all__ = ["ancestry_checks", "calendar_checks", "calendar_window", "row_ids",
           "training_digest", "year_block", "years"]


def calendar_window(issue: date, product: str, lead: str) -> tuple[date, date]:
    index = int(lead[1:])
    if product == "1mon":
        start = issue+timedelta(weeks=index-1)
        return start, start+timedelta(days=6)
    if product != "3mon":
        raise ValueError("unsupported calendar product")
    month = issue.month+index
    year = issue.year+(month-1)//12
    month = (month-1) % 12+1
    return date(year, month, 1), date(year, month, monthrange(year, month)[1])


def calendar_checks() -> dict[str, Json]:
    if calendar_window(date(2024, 2, 26), "1mon", "W1") != (
        date(2024, 2, 26), date(2024, 3, 3)
    ):
        raise AssertionError("seven-day leap-day window lost a contributing day")
    if calendar_window(date(2024, 1, 15), "3mon", "M1") != (
        date(2024, 2, 1), date(2024, 2, 29)
    ):
        raise AssertionError("individual February leap-month window incorrect")
    if calendar_window(date(2023, 12, 18), "3mon", "M2") != (
        date(2024, 2, 1), date(2024, 2, 29)
    ):
        raise AssertionError("monthly year-crossing window incorrect")
    return {"status": "PASS", "weekly": "SEVEN_DAYS",
            "monthly": "INDIVIDUAL_CALENDAR_MONTH", "leap_day": "RETAINED"}


def ancestry_checks(output: Path) -> dict[str, Json]:
    ledger = csv_records(output / "training_ledger.csv.gz")
    require_columns(ledger, (
        "row_id", "train_hash", "source_case_init", "source_year", "hist_start",
        "hist_end", "cutoff", "catalog_cutoff", "held_out_years", "product", "variable",
        "year_weight",
        "source_case_id", "source_init", "lead", "observation", "member_keys",
        "source_files", "provenance_hash", "archive_era", "ensemble",
    ), "training ledger")
    by_hash: dict[str, dict[str, dict[str, str]]] = {}
    weights: dict[tuple[str, int], float] = {}
    for row in ledger:
        cutoff = date.fromisoformat(row["cutoff"])
        catalog = date.fromisoformat(row["catalog_cutoff"])
        start, end = date.fromisoformat(row["hist_start"]), date.fromisoformat(row["hist_end"])
        heldout = years(row["held_out_years"])
        source_year = int(row["source_year"])
        issue = date.fromisoformat(row["source_init"])
        if issue.year != source_year or calendar_window(
            issue, row["product"], row["lead"]
        ) != (start, end):
            raise AssertionError(f"historical source-year/calendar window mismatch: {row['row_id']}")
        if end >= cutoff or date.fromisoformat(row["source_case_init"]) > catalog:
            raise AssertionError(f"future data in {row['row_id']}")
        if source_year in heldout or year_block(start, end, heldout):
            raise AssertionError(f"held-out source/valid-year in {row['row_id']}")
        if cutoff > catalog:
            raise AssertionError("response cutoff exceeds outer-frozen catalog")
        group = by_hash.setdefault(row["train_hash"], {})
        if row["row_id"] in group and row != group[row["row_id"]]:
            raise AssertionError("contradictory duplicate ancestry record")
        if row["row_id"] not in group:
            key = row["train_hash"], source_year
            weights[key] = weights.get(key, 0) + float(row["year_weight"])
        group[row["row_id"]] = row
    for train_hash, rows in by_hash.items():
        if len({(r["product"], r["variable"]) for r in rows.values()}) != 1:
            raise AssertionError(f"mixed raw units in pool {train_hash}")
        first = next(iter(rows.values()))
        if training_digest(list(rows.values()), first["cutoff"], first["catalog_cutoff"],
                           first["held_out_years"]) != train_hash:
            raise AssertionError(f"training content hash mismatch: {train_hash}")
        for row in rows.values():
            ensemble = vector(decode(row["ensemble"]))
            observation = number(decode(row["observation"]))
            if not np.all(np.isfinite(ensemble)) or not np.isfinite(observation):
                raise AssertionError("nonfinite accepted training input")
            if row["variable"] == "prcp" and (np.any(ensemble < 0) or observation < 0):
                raise AssertionError("negative accepted rain")
    for key, weight in weights.items():
        if abs(weight - 1) > 1e-9:
            raise AssertionError(f"year-balanced mass {key} = {weight}, not 1")
    folds = csv_records(output / "fold_ancestry.csv.gz")
    if folds:
        require_columns(folds, ("fold_id", "training_row_ids", "validation_row_ids",
                                "pseudo_init", "held_out_years", "ancestor_hash",
                                "outer_train_hash", "catalog_cutoff"), "fold ancestry")
    for fold in folds:
        training_ids = set(row_ids(fold["training_row_ids"]))
        validation_ids = set(row_ids(fold["validation_row_ids"]))
        if training_ids & validation_ids:
            raise AssertionError("fold training/validation overlap")
        outer = by_hash[fold["outer_train_hash"]]
        if not training_ids | validation_ids <= outer.keys():
            raise AssertionError("fold references rows outside its frozen outer pool")
        cutoff = date.fromisoformat(fold["pseudo_init"])
        heldout = years(fold["held_out_years"])
        validation_sources = {int(outer[key]["source_year"]) for key in validation_ids}
        if not validation_sources <= heldout:
            raise AssertionError("fold omitted validation SOURCE_YEAR from whole-year holdout")
        outer_catalogs = {r["catalog_cutoff"] for r in outer.values()}
        if outer_catalogs != {fold["catalog_cutoff"]}:
            raise AssertionError("inner fold changed outer catalog vintage")
        for row_id in training_ids:
            row = outer[row_id]
            if date.fromisoformat(row["hist_end"]) >= cutoff:
                raise AssertionError("inner pseudo-issue has future response")
            if int(row["source_year"]) in heldout or year_block(
                date.fromisoformat(row["hist_start"]), date.fromisoformat(row["hist_end"]), heldout
            ):
                raise AssertionError("inner held-out annual block leaked")
        if not fold["ancestor_hash"]:
            raise AssertionError("fold lacks ancestor hash")
        actual = training_digest([outer[row_id] for row_id in training_ids],
                                 fold["pseudo_init"], fold["catalog_cutoff"],
                                 fold["held_out_years"])
        if actual != fold["ancestor_hash"]:
            raise AssertionError("fold ancestor content hash mismatch")
    fits = csv_records(output / "fit_ledger.csv.gz")
    from analysis.alternative_validation_joint_ancestry import joint_ancestry_checks
    joint_receipt = joint_ancestry_checks(output)
    joint_hashes = {r["joint_train_hash"] for r in csv_records(output / "joint_component_manifest.csv")}
    for fit in fits:
        if fit["status"] == "OK" and fit["train_hash"] not in by_hash.keys() | joint_hashes:
            raise AssertionError("successful fit lacks row-level training ancestry")
    return {"status": "PASS", "training_records": len(ledger),
            "distinct_training_hashes": len(by_hash), "fold_records": len(folds),
            "catalog_policy": "OUTER_FROZEN_NOT_REAL_TIME_RELEASE_PROOF",
            "joint_ancestry": joint_receipt}
