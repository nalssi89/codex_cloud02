"""Canonical weighted reduction of exact pooled-row replicas."""

from __future__ import annotations

from math import fsum

import numpy as np

from analysis.alternative_contracts import AlternativeError, TrainingRow, TrainingSet
from analysis.calibration import FloatArray


def canonical_rows(training: TrainingSet) -> tuple[tuple[TrainingRow, ...], FloatArray]:
    """Merge only the same provenance row ID, preserving its complete loss weight.

    Exact replication with split weights must generate the identical optimizer
    problem, not an almost-identical floating-point reduction. Distinct archive
    vintages and distinct conditions retain their own row IDs and are not merged.
    """
    unique: dict[str, TrainingRow] = {}
    masses: dict[str, list[float]] = {}
    for i, row in enumerate(training.rows):
        prior = unique.get(row.row_id)
        if prior is not None:
            metadata = (
                row.source_case_id, row.source_case_init, row.source_year,
                row.source_init, row.hist_start, row.hist_end, row.product,
                row.lead, row.variable, row.observation, row.member_keys,
                row.provenance_hash, row.archive_era, row.source_files,
            )
            previous = (
                prior.source_case_id, prior.source_case_init, prior.source_year,
                prior.source_init, prior.hist_start, prior.hist_end, prior.product,
                prior.lead, prior.variable, prior.observation, prior.member_keys,
                prior.provenance_hash, prior.archive_era, prior.source_files,
            )
            if metadata != previous or not np.array_equal(row.ensemble, prior.ensemble):
                raise AlternativeError("INPUT_CONFLICT", f"Conflicting pooled row: {row.row_id}")
        else:
            unique[row.row_id] = row
            masses[row.row_id] = []
        masses[row.row_id].append(training.year_weights.item(i))
    keys = sorted(unique)
    weights = np.array([fsum(masses[key]) for key in keys], dtype=np.float64)
    return tuple(unique[key] for key in keys), weights
