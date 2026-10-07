"""Real dispatch, conservative fit sharing, and complete prediction checkpoints."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import replace

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    TrainingRow,
    TrainingSet,
)
from analysis.alternative_data import training_for
from analysis.alternative_experiment_types import ExperimentInputs
from analysis.alternative_training import make_training


class TrainingCache:
    """Run-local cache over the loader's immutable catalog, never month/lead keys."""

    def __init__(self, inputs: ExperimentInputs) -> None:
        self.inputs: ExperimentInputs = inputs
        self.local: dict[str, TrainingSet] = {}
        self.pooled: dict[tuple[str, str, str, tuple[int, ...]], TrainingSet] = {}
        self.pools: dict[tuple[str, str], tuple[TrainingRow, ...]] = {}
        grouped: dict[tuple[str, str], list[TrainingRow]] = defaultdict(list)
        for history in inputs.historical.values():
            for row in history:
                if row.ensemble.flags.writeable:
                    raise AlternativeError("MUTABLE_INPUT", row.row_id)
                grouped[(row.product, row.variable)].append(row)
        self.pools = {key: tuple(rows) for key, rows in grouped.items()}

    def get(self, target: CaseInput, scope: str) -> TrainingSet:
        if target.case_id not in self.local:
            self.local[target.case_id] = training_for(target, self.inputs, "local")
        local = self.local[target.case_id]
        if scope == "local":
            return local
        if scope != "pooled":
            raise ValueError(f"Unexpected scalar scope {scope}")
        key = (target.product, target.variable, target.init.isoformat(), local.held_out_years)
        if key not in self.pooled:
            rows = self.pools[(target.product, target.variable)]
            self.pooled[key] = make_training(target, rows, target.init)
        base = self.pooled[key]
        return replace(base, target=target, local_observations=local.local_observations,
                       thresholds=local.thresholds)
