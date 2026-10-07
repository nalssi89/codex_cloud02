"""Actual-case BMA ancestry, mixed-law means and JSON-restored CRPS receipts."""

from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter

import numpy as np

from analysis.alternative_classical import fit_classical
from analysis.alternative_classical_audit import method
from analysis.alternative_classical_mixture import MixtureModel
from analysis.alternative_classical_mixture_audit import round_trip
from analysis.alternative_contracts import FitConfig, FitStatus
from analysis.alternative_data import (
    fold_training,
    inner_folds,
    load_experiment,
    training_for,
)


def main() -> None:
    started = perf_counter()
    inputs = load_experiment(Path.cwd())
    seen: set[tuple[str, str]] = set()
    receipts: list[dict[str, object]] = []
    for target in inputs.cases:
        key = target.product, target.variable
        if key in seen or target.case_id not in inputs.truths:
            continue
        training = training_for(target, inputs, "local")
        if target.variable == "prcp" and np.any(training.local_observations <= 0):
            continue
        fitted = fit_classical(method("bma_component_pool"), training, FitConfig(workers=1))
        assert fitted.status == FitStatus.OK, fitted.diagnostics.message
        model = fitted.fitted_model
        assert isinstance(model, MixtureModel) and len(model.components) == 3
        metadata = fitted.diagnostics.posterior_diagnostics
        years, ancestors = metadata["common_prequential_years"], metadata["fold_receipts"]
        assert isinstance(years, list) and len(years) >= 8
        assert isinstance(ancestors, list)
        folds = {fold.fold_id: fold for fold in inner_folds(
            training, target, min_years=10, last_n=None)}
        for record in ancestors:
            assert isinstance(record, dict)
            fold_id = record["fold_id"]
            assert isinstance(fold_id, str)
            fold = folds[fold_id]
            ancestor = fold_training(training, fold)
            assert record["train_hash"] == ancestor.train_hash == fold.ancestor_hash
            assert ancestor.catalog_cutoff == training.catalog_cutoff
            assert ancestor.target.case_id == target.case_id
            assert len({row.source_year for row in ancestor.rows}) >= 10
            assert all(row.hist_end < fold.pseudo_init for row in ancestor.rows)
            assert all(row.source_year not in fold.held_out_years for row in ancestor.rows)
            assert not any(row.hist_start.year <= year <= row.hist_end.year
                           for row in ancestor.rows for year in fold.held_out_years)
        law = model.predict(target)
        restored = round_trip(law)
        expected_mean = sum(weight * component.predict(target).mean()
                            for weight, component in zip(model.weights, model.components, strict=True))
        np.testing.assert_allclose(law.mean(), expected_mean, rtol=1e-12, atol=1e-10)
        np.testing.assert_allclose(restored.mean(), expected_mean, rtol=1e-10, atol=1e-8)
        observation = inputs.truths[target.case_id].observation
        crps = law.crps(observation)
        np.testing.assert_allclose(restored.crps(observation), crps, rtol=1e-9, atol=1e-8)
        assert np.isfinite(crps) and crps >= 0
        assert all(weight > 0 for weight in model.weights)
        assert abs(sum(model.weights)-1) < 1e-12
        receipts.append({"case_id": target.case_id, "train_hash": training.train_hash,
                         "common_prequential_years": years, "ancestor_count": len(ancestors),
                         "fold_failures": metadata["fold_failures"], "weights": model.weights,
                         "mean": law.mean(), "serialized_mean": restored.mean(),
                         "crps": crps, "serialized_crps": restored.crps(observation),
                         "atom": law.atom_mass(0), "status": str(fitted.status),
                         "fit_seconds": fitted.diagnostics.elapsed_seconds})
        seen.add(key)
        if len(seen) == 4:
            break
    assert len(receipts) == 4
    print(json.dumps({"scope": "ACTUAL_BMA_SMOKE", "receipts": receipts,
                      "seconds": perf_counter()-started}, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
