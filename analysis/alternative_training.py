"""Past-response eligibility and deterministic annual training identities."""

import hashlib
import json
from collections import Counter
from collections.abc import Iterable
from dataclasses import replace
from datetime import date
from typing import assert_never

import numpy as np

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FitScope,
    FoldSpec,
    TrainingRow,
    TrainingSet,
)
from analysis.alternative_experiment_types import ExperimentInputs
from analysis.calibration import FloatArray


def eligible(row: TrainingRow, cutoff: date, catalog_cutoff: date,
             held_out: tuple[int, ...]) -> bool:
    """Catalog vintage and historical response availability are distinct."""
    return (
        row.source_case_init <= catalog_cutoff and row.hist_end < cutoff
        and row.source_year not in held_out
        and not any(row.hist_start.year <= year <= row.hist_end.year for year in held_out)
    )


def training_hash(rows: tuple[TrainingRow, ...], cutoff: date,
                  catalog_cutoff: date, held_out: tuple[int, ...]) -> str:
    """Seal dates, actual values/identities and observation provenance."""
    digest = hashlib.sha256()
    digest.update(json.dumps(
        [cutoff.isoformat(), catalog_cutoff.isoformat(), held_out], separators=(",", ":"),
    ).encode())
    for row in rows:
        digest.update(json.dumps([
            row.row_id, row.source_case_id, row.source_case_init.isoformat(),
            row.source_year, row.source_init.isoformat(), row.hist_start.isoformat(),
            row.hist_end.isoformat(), row.product, row.variable, row.lead,
            float(row.observation).hex(), row.member_keys, row.source_files,
            row.provenance_hash, row.archive_era,
        ], separators=(",", ":")).encode())
        digest.update(row.ensemble.tobytes())
    return digest.hexdigest()


def make_training(target: CaseInput, candidates: Iterable[TrainingRow],
                  catalog_cutoff: date, *,
                  held_out_years: tuple[int, ...] | None = None) -> TrainingSet:
    """Construct year-balanced rows without touching a target truth."""
    held_out = (tuple(range(target.valid_start.year, target.valid_end.year + 1))
                if held_out_years is None else held_out_years)
    seen: dict[str, TrainingRow] = {}
    for row in candidates:
        if (row.product, row.variable) != (target.product, target.variable):
            continue
        if not eligible(row, target.init, catalog_cutoff, held_out):
            continue
        prior = seen.get(row.row_id)
        if prior is not None:
            if (prior.observation != row.observation
                or not np.array_equal(prior.ensemble, row.ensemble)
                or prior.member_keys != row.member_keys
                or prior.hist_start != row.hist_start or prior.hist_end != row.hist_end):
                raise AlternativeError("INPUT_CONFLICT", row.row_id)
            continue
        seen[row.row_id] = row
    rows = tuple(sorted(seen.values(), key=lambda row: row.row_id))
    counts = Counter(row.source_year for row in rows)
    weights = np.asarray([1 / counts[row.source_year] for row in rows], dtype=np.float64)
    local = np.asarray(
        [row.observation for row in rows if row.source_case_id == target.case_id],
        dtype=np.float64,
    )
    if not len(local):
        raise AlternativeError("INSUFFICIENT_TRAINING", f"No local history: {target.case_id}")
    thresholds = np.asarray(np.quantile(local, [1 / 3, 2 / 3]), dtype=np.float64)
    for values in (weights, local, thresholds):
        values.setflags(write=False)
    return TrainingSet(
        target=target, rows=rows, year_weights=weights, cutoff=target.init,
        catalog_cutoff=catalog_cutoff, held_out_years=held_out,
        train_hash=training_hash(rows, target.init, catalog_cutoff, held_out),
        local_observations=local, thresholds=thresholds,
    )


def training_for(target: CaseInput, inputs: ExperimentInputs,
                 scope: FitScope) -> TrainingSet:
    """Select one product/variable and never a later outer catalog vintage."""
    match scope:
        case "local":
            candidates = inputs.historical.get(target.case_id, ())
        case "pooled":
            candidates = tuple(
                row for history in inputs.historical.values() for row in history
                if (row.product, row.variable) == (target.product, target.variable)
            )
        case "joint":
            raise AlternativeError("JOINT_TRAINING_REQUIRED", target.case_id)
        case _:
            assert_never(scope)
    return make_training(target, candidates, target.init)


def inner_folds(training: TrainingSet, target: CaseInput,
                min_years: int, last_n: int | None) -> tuple[FoldSpec, ...]:
    """Use historical pseudo-issuance, not random row or future-aware LOYO."""
    validation = sorted(
        (row for row in training.rows if row.source_case_id == target.case_id),
        key=lambda row: (row.source_year, row.row_id),
    )
    folds: list[FoldSpec] = []
    for row in validation:
        pseudo = replace(
            target, init=row.source_init, valid_start=row.hist_start,
            valid_end=row.hist_end, members=row.ensemble, member_keys=row.member_keys,
            archive_era=row.archive_era,
        )
        held_out = tuple(sorted({row.source_year,
                                 *range(row.hist_start.year, row.hist_end.year + 1)}))
        past = tuple(r for r in training.rows if eligible(
            r, pseudo.init, training.catalog_cutoff, held_out,
        ))
        local_past = [r for r in past if r.source_case_id == target.case_id]
        if len({r.source_year for r in local_past}) < min_years:
            continue
        folds.append(FoldSpec(
            fold_id=f"{target.case_id}/prequential/{row.source_year}",
            validation_row_ids=(row.row_id,),
            training_row_ids=tuple(r.row_id for r in past),
            pseudo_init=pseudo.init, held_out_years=held_out,
            ancestor_hash=training_hash(past, pseudo.init, training.catalog_cutoff, held_out),
        ))
    return tuple(folds if last_n is None else folds[-last_n:])


def fold_training(training: TrainingSet, fold: FoldSpec) -> TrainingSet:
    """Replay a fold with its actual historical ensemble and response cutoff."""
    by_id = {row.row_id: row for row in training.rows}
    validation = by_id[fold.validation_row_ids[0]]
    pseudo = replace(
        training.target, init=fold.pseudo_init, valid_start=validation.hist_start,
        valid_end=validation.hist_end, members=validation.ensemble,
        member_keys=validation.member_keys, archive_era=validation.archive_era,
    )
    ancestor = make_training(
        pseudo, (by_id[key] for key in fold.training_row_ids), training.catalog_cutoff,
        held_out_years=fold.held_out_years,
    )
    if ancestor.train_hash != fold.ancestor_hash:
        raise AlternativeError("ANCESTOR_HASH_MISMATCH", fold.fold_id)
    return ancestor


def row_thresholds(training: TrainingSet, row: TrainingRow) -> FloatArray | None:
    """Return past-only local thresholds; early unsupported labels are absent."""
    past = [
        r.observation for r in training.rows
        if r.source_case_id == row.source_case_id
        and eligible(r, row.source_init, training.catalog_cutoff,
                     tuple(sorted({row.source_year,
                                   *range(row.hist_start.year, row.hist_end.year + 1)})))
    ]
    if len(past) < 10:
        return None
    return np.asarray(np.quantile(past, [1 / 3, 2 / 3]), dtype=np.float64)
