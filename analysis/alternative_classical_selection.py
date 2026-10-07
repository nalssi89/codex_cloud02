"""Strict historical-only selection of Tweedie's prescribed power grid."""

from __future__ import annotations

from dataclasses import replace
from time import perf_counter
from types import MappingProxyType

import numpy as np

from analysis.alternative_classical_common import result
from analysis.alternative_classical_laws import LocalModel
from analysis.alternative_classical_local import fit_local
from analysis.alternative_classical_mixture import validation_case
from analysis.alternative_contracts import (
    FitConfig,
    FitResult,
    FitStatus,
    MethodSpec,
    TrainingSet,
)
from analysis.data_io import Json


def fit_selected_tweedie(spec: MethodSpec, training: TrainingSet,
                        config: FitConfig) -> FitResult:
    from analysis.alternative_data import fold_training, inner_folds
    started = perf_counter()
    folds = inner_folds(training, training.target, min_years=15, last_n=5)
    rows = {row.row_id: row for row in training.rows}
    scores: dict[float, list[float]] = {p: [] for p in (1.2, 1.5, 1.8)}
    receipts: list[Json] = []
    errors: list[str] = []
    for fold in folds:
        ancestor = fold_training(training, fold)
        if ancestor.catalog_cutoff != training.catalog_cutoff:
            raise ValueError("Inner fit changed outer-frozen original-case catalog")
        fold_scores: dict[float, float] = {}
        for power in scores:
            fitted = fit_local(replace(spec, id="tweedie_p15"), ancestor, config, power)
            if fitted.status != FitStatus.OK or fitted.fitted_model is None:
                errors.append(f"{fold.fold_id}:p={power}:{fitted.diagnostics.message}")
                break
            values = [fitted.fitted_model.predict(validation_case(rows[rid])).crps(
                rows[rid].observation) for rid in fold.validation_row_ids]
            fold_scores[power] = float(np.mean(values))
        if len(fold_scores) == 3:
            for power, score in fold_scores.items():
                scores[power].append(score)
            receipts.append({"fold_id": fold.fold_id, "ancestor_hash": ancestor.train_hash,
                             "training_row_ids": list(fold.training_row_ids),
                             "validation_row_ids": list(fold.validation_row_ids),
                             "pseudo_init": fold.pseudo_init.isoformat()})
    if len(receipts) < 3:
        return result(spec.id, training, started, None,
                      status=FitStatus.INSUFFICIENT_INNER_FOLDS,
                      reason="FEWER_THAN_THREE_COMMON_POWER_FOLDS", message="; ".join(errors))
    averages = {power: float(np.mean(values)) for power, values in scores.items()}
    best = min(averages.values())
    selected = next(power for power in scores if averages[power] <= best + 1e-10)
    fitted = fit_local(replace(spec, id="tweedie_p15"), training, config, selected)
    model = fitted.fitted_model
    if isinstance(model, LocalModel):
        model = replace(model, method_id=spec.id)
    metadata: dict[str, Json] = {"selected_power": selected,
                                "power_cv_scores": {str(p): s for p, s in averages.items()},
                                "fold_receipts": receipts, "fold_failures": [e for e in errors]}
    return replace(fitted, method_id=spec.id, fitted_model=model, diagnostics=replace(
        fitted.diagnostics, elapsed_seconds=perf_counter() - started,
        posterior_diagnostics=MappingProxyType(metadata)))
