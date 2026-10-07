"""Joint past-only folds retaining the ACTUAL issuance's frozen reforecast catalog."""

from __future__ import annotations

import hashlib
from collections.abc import Iterator
from dataclasses import replace
from types import MappingProxyType

import numpy as np

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FoldSpec,
    JointTrainingSet,
    ResidualSet,
    TrainingRow,
    TrainingSet,
)


def historical_case(row: TrainingRow) -> CaseInput:
    """Historical forecast covariates only; its observed value is not copied."""
    return CaseInput(
        case_id=row.row_id, init=row.source_init, valid_start=row.hist_start,
        valid_end=row.hist_end, product=row.product, lead=row.lead,
        variable=row.variable, members=row.ensemble, member_keys=row.member_keys,
        provenance_hash=row.provenance_hash, archive_era=row.archive_era,
    )


def prequential_folds(
    training: JointTrainingSet, minimum_years: int = 10,
) -> Iterator[tuple[int, JointTrainingSet, FoldSpec]]:
    """Discard entire annual vectors if ANY component breaches a pseudo-issue gate."""
    for year in sorted(training.source_years):
        validation = training.rows_by_year[year]
        pseudo_init = min(row.source_init for row in validation)
        held_out = tuple(sorted({
            year, *training.held_out_years,
            *(y for row in validation for y in range(row.hist_start.year, row.hist_end.year + 1)),
        }))
        years = tuple(y for y in sorted(training.source_years) if y not in held_out and all(
            row.hist_end < pseudo_init
            and row.source_case_init <= training.catalog_cutoff
            and not any(row.hist_start.year <= held <= row.hist_end.year for held in held_out)
            for row in training.rows_by_year[y]
        ))
        if len(years) < minimum_years:
            continue
        indices = [training.source_years.index(y) for y in years]
        ancestors = tuple(row.row_id for y in years for row in training.rows_by_year[y])
        digest = hashlib.sha256(
            "|".join((training.train_hash, pseudo_init.isoformat(), *ancestors)).encode()
        ).hexdigest()
        fold = FoldSpec(
            fold_id=f"joint:{year}:{digest[:16]}",
            validation_row_ids=tuple(row.row_id for row in validation),
            training_row_ids=ancestors, pseudo_init=pseudo_init,
            held_out_years=held_out, ancestor_hash=digest,
        )
        subset = replace(
            training, targets=tuple(historical_case(row) for row in validation),
            rows_by_year=MappingProxyType({y: training.rows_by_year[y] for y in years}),
            source_years=years,
            historical_initializations=tuple(training.historical_initializations[i] for i in indices),
            historical_windows=tuple(training.historical_windows[i] for i in indices),
            forecast_means=training.forecast_means[indices],
            observations=training.observations[indices],
            cutoff=pseudo_init, held_out_years=held_out, train_hash=digest,
        )
        yield year, subset, fold


def component_training(training: JointTrainingSet, component: int) -> TrainingSet:
    rows = tuple(training.rows_by_year[year][component] for year in training.source_years)
    values = training.observations[:, component]
    return TrainingSet(
        target=training.targets[component], rows=rows,
        year_weights=np.ones(len(rows), dtype=np.float64),
        cutoff=training.cutoff, catalog_cutoff=training.catalog_cutoff,
        held_out_years=training.held_out_years, train_hash=f"{training.train_hash}:{component}",
        local_observations=values, thresholds=np.quantile(values, [1.0 / 3.0, 2.0 / 3.0]),
    )


def validate_residuals(training: JointTrainingSet, residuals: ResidualSet) -> None:
    """Reject undocumented, in-sample, partial-year or mismatched residual ancestry."""
    if residuals.component_keys != training.component_keys:
        raise AlternativeError("RESIDUAL_COMPONENT_MISMATCH", "Aligned component order differs.")
    if len(residuals.years) < 8:
        raise AlternativeError("INSUFFICIENT_RESIDUAL_YEARS", str(len(residuals.years)))
    if len(set(residuals.years)) != len(residuals.years):
        raise AlternativeError("DUPLICATE_RESIDUAL_YEAR", "One vector per annual validation.")
    shape = (len(residuals.years), len(training.component_keys))
    if residuals.residual_matrix.shape != shape or not np.isfinite(residuals.residual_matrix).all():
        raise AlternativeError("INVALID_RESIDUAL_MATRIX", str(residuals.residual_matrix.shape))
    if residuals.weights.shape != (shape[0],) or not np.allclose(
        residuals.weights, np.full(shape[0], 1.0 / shape[0]), rtol=0, atol=1e-12,
    ):
        raise AlternativeError("INVALID_RESIDUAL_WEIGHTS", "Whole years need equal masses.")
    expected = {year: fold for year, _, fold in prequential_folds(training)}
    if len(residuals.fold_refs) != len(residuals.years):
        raise AlternativeError("MISSING_RESIDUAL_ANCESTRY", "One FoldSpec per vector is required.")
    for year, fold in zip(residuals.years, residuals.fold_refs, strict=True):
        if year not in expected or fold != expected[year]:
            raise AlternativeError("NONPREQUENTIAL_RESIDUAL", f"Year {year} has invalid ancestors.")
