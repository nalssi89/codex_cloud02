"""Real dispatch, conservative fit sharing, and complete prediction checkpoints."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator

from analysis.alternative_contracts import (
    CaseInput,
    JointTrainingSet,
    TrainingSet,
)
from analysis.alternative_experiment_types import ExperimentInputs
from analysis.alternative_runner_engine_base import COUPLING_IDS
from analysis.alternative_runner_io import (
    Row,
    digest,
    dumps,
    json_value,
    known_input,
)
from analysis.alternative_runner_joint import Engine
from analysis.alternative_training import make_training

__all__ = [
    "COUPLING_IDS",
    "Engine",
    "check_catalog_immutability",
    "joint_keys",
    "joint_scalar_ancestry",
    "retained_joint_rows",
]

def joint_keys(cases: tuple[CaseInput, ...]) -> tuple[tuple[CaseInput, ...], ...]:
    """Every same-window pair and both full/partial T-only and T/P trajectories."""
    by_issue: dict[tuple[str, str], list[CaseInput]] = defaultdict(list)
    for target in cases:
        by_issue[(target.product, target.init.isoformat())].append(target)
    groups: dict[tuple[str, ...], tuple[CaseInput, ...]] = {}
    for targets in by_issue.values():
        ordered = tuple(sorted(targets, key=lambda t: (int(t.lead[1:]), t.variable)))
        by_window: dict[tuple[str, str], list[CaseInput]] = defaultdict(list)
        for target in ordered:
            by_window[(target.valid_start.isoformat(), target.valid_end.isoformat())].append(target)
        candidates = [tuple(pair) for pair in by_window.values() if len(pair) >= 2]
        candidates.extend((tuple(t for t in ordered if t.variable == "t15m"), ordered))
        # Single-variable rain trajectories are also real annual-vector targets.
        candidates.append(tuple(t for t in ordered if t.variable == "prcp"))
        for candidate in candidates:
            if len(candidate) >= 2:
                groups[tuple(t.case_id for t in candidate)] = candidate
    return tuple(groups[key] for key in sorted(groups))


def check_catalog_immutability(inputs: ExperimentInputs) -> str:
    """Fresh content proof at each run boundary; no identity-only array cache."""
    return digest({
        "cases": [known_input(case) for case in inputs.cases],
        "histories": {case_id: json_value(rows) for case_id, rows in inputs.historical.items()},
        "provenance": inputs.provenance,
    })


def joint_scalar_ancestry(training: JointTrainingSet) -> Iterator[TrainingSet]:
    """Joint fit hashes refer to component manifests, not mixed-unit scalar pools."""
    for column, target in enumerate(training.targets):
        component_rows = tuple(
            sorted((annual[column]
                    for annual in training.rows_by_year.values()), key=lambda row: row.row_id)
        )
        component = make_training(target, component_rows, training.catalog_cutoff)
        yield component


def retained_joint_rows(training: JointTrainingSet) -> list[Row]:
    """Explicit vector manifest: original scalar hash components plus annual alignment."""
    return [{
        "joint_train_hash": training.train_hash, "source_year": year,
        "component_case_ids": dumps(training.component_keys),
        "row_ids": dumps(tuple(row.row_id for row in training.rows_by_year[year])),
        "historical_initialization": training.rows_by_year[year][0].source_init.isoformat(),
        "forecast_means": dumps(training.forecast_means.take(index, axis=0)),
        "observations": dumps(training.observations.take(index, axis=0)),
        "held_out_years": dumps(training.held_out_years),
        "cutoff": training.cutoff.isoformat(),
        "catalog_cutoff": training.catalog_cutoff.isoformat(),
    } for index, year in enumerate(training.source_years)]
