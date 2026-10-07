"""Run every frozen learning ID through its actual known-input surface."""

from __future__ import annotations

import json
from math import exp
from pathlib import Path
from time import perf_counter

import numpy as np

from analysis.alternative_contracts import (
    CategoryFitResult,
    FitConfig,
    FitResult,
    FitStatus,
)
from analysis.alternative_learning import LEARNING_IDS, fit_learning, predict_categories
from analysis.alternative_learning_category import historical_labels


def real_bqn_errors(
    model: object, training: object,
) -> list[float]:
    import torch

    from analysis.alternative_contracts import TrainingSet
    from analysis.alternative_data import features_for_case
    from analysis.alternative_learning_neural import NeuralModel, bqn_loss
    from analysis.alternative_learning_neural_checks import cdf_oracle
    from analysis.alternative_learning_neural_math import softplus

    assert isinstance(model, NeuralModel) and isinstance(training, TrainingSet)
    x = features_for_case(training.target, model.feature_spec)
    observed = np.array([row.observation for row in training.rows], dtype=np.float64)
    reference = np.quantile(observed, [.1, .5, .9])
    worst = [0., 0., 0.]
    for w1, b1, w2, b2 in model.parameters:
        raw = np.asarray(w2 @ np.tanh(w1 @ x + b1) + b2, dtype=np.float64)
        first = softplus(raw.item(0)) + 1e-6 if model.rain else raw.item(0)
        coefficients = np.concatenate((
            np.array([first]), first + np.cumsum(np.logaddexp(0, raw[1:6]) + 1e-6),
        ))
        p0 = exp(-softplus(-raw.item(6))) if model.rain else 0.
        tensor = torch.as_tensor(raw.reshape(1, -1), dtype=torch.float64)
        for value in reference.flat:
            y = float(value)
            expected = cdf_oracle(coefficients, float(p0), y, model.rain)
            for index, nodes in enumerate((64, 128, 256)):
                actual = bqn_loss(tensor, torch.tensor([y], dtype=torch.float64), model.rain, nodes).item()
                worst[index] = max(worst[index], abs(actual - expected))
    assert max(worst) <= 1e-7, worst
    return worst


def main(method_ids: tuple[str, ...] = LEARNING_IDS) -> None:
    from analysis.alternative_data import (
        gate_report,
        load_experiment,
        row_thresholds,
        training_for,
    )
    from analysis.alternative_registry import method_registry

    started = perf_counter()
    inputs = load_experiment(Path.cwd())
    specs = {spec.id: spec for spec in method_registry() if spec.owner == "learning"}
    assert set(specs) == set(LEARNING_IDS)
    # Fixed examples, never selected by skill or verified target response.
    ids = ("20220307_1MON_W01_t15m", "20220307_1MON_W01_prcp", *(
        min(
            (case for case in inputs.cases if case.product == "3mon" and case.variable == variable),
            key=lambda case: (case.init, case.case_id),
        ).case_id for variable in ("t15m", "prcp")
    ))
    report: list[dict[str, object]] = []
    for identifier in ids:
        target = next(case for case in inputs.cases if case.case_id == identifier)
        training = training_for(target, inputs, "pooled")
        assert not hasattr(target, "observation")
        selected, _, own_cuts, ancestors = historical_labels(training)
        for position, index in enumerate(selected):
            expected = row_thresholds(training, training.rows[index])
            assert expected is not None
            np.testing.assert_array_equal(expected, own_cuts[position:position + 1].reshape(-1))
            assert training.rows[index].row_id not in ancestors[position]
        for year in {row.source_year for row in training.rows}:
            total = sum(
                training.year_weights.item(i) for i, row in enumerate(training.rows)
                if row.source_year == year
            )
            assert abs(total - 1) < 1e-12
        for row in training.rows:
            assert row.source_case_init <= training.catalog_cutoff
            assert row.hist_end < training.cutoff
            assert row.source_year not in training.held_out_years
            assert not any(row.hist_start.year <= y <= row.hist_end.year for y in training.held_out_years)
        for method_id in method_ids:
            assert gate_report(specs[method_id], training, inputs).allowed
            result = fit_learning(specs[method_id], training, FitConfig(workers=1))
            assert result.status == FitStatus.OK, (identifier, method_id, result.reason_code)
            record: dict[str, object] = {
                "case_id": identifier, "method_id": method_id,
                "n_rows": result.diagnostics.n_rows,
                "n_years": result.diagnostics.n_years,
                "train_hash": training.train_hash,
                "seconds": result.diagnostics.elapsed_seconds,
                "objective": result.diagnostics.objective,
                "flags": result.diagnostics.boundary_flags,
            }
            if isinstance(result, CategoryFitResult):
                assert result.fitted_model is not None
                prediction = predict_categories(result.fitted_model, target, training.thresholds)
                probabilities = prediction.probabilities
                assert np.all(probabilities >= 0)
                np.testing.assert_allclose(probabilities.sum(), 1, atol=1e-12)
                record["probabilities"] = probabilities.tolist()
                _ = json.dumps(result.fitted_model.to_spec(), allow_nan=False)
            else:
                assert isinstance(result, FitResult)
                assert result.fitted_model is not None
                law = result.fitted_model.predict(target)
                probabilities = np.linspace(.01, .99, 37)
                quantiles = law.quantile(probabilities)
                assert np.all(np.isfinite(quantiles))
                assert np.all(np.diff(quantiles) >= -1e-12)
                grid = np.concatenate((np.array([-np.inf]), quantiles, np.array([np.inf])))
                cdf, left = law.cdf(grid), law.cdf_left(grid)
                assert cdf.item(0) == 0 and cdf.item(-1) == 1
                assert np.all(np.diff(cdf) >= -1e-12)
                assert np.all(left <= cdf + 1e-12)
                mean = law.mean()
                crps = law.crps(mean)
                assert np.isfinite(mean) and np.isfinite(crps) and crps >= 0
                atom = law.atom_mass(0.)
                assert 0 <= atom <= 1
                if target.variable == "prcp":
                    assert mean >= 0
                    assert law.cdf(np.array([-1.])).item(0) == 0
                record.update({"mean": mean, "crps_at_own_mean": crps, "zero_atom": atom})
                if method_id == "bqn_monotone":
                    record["actual_component_crps_errors_64_128_256"] = real_bqn_errors(
                        result.fitted_model, training,
                    )
                _ = json.dumps(result.fitted_model.to_spec(), allow_nan=False)
                _ = json.dumps(law.to_spec(), allow_nan=False)
            report.append(record)
            print(json.dumps(record, allow_nan=False, indent=2), flush=True)
    print(json.dumps({
        "scope": "ALL_LEARNING_EXAMPLE_IDS" if method_ids == LEARNING_IDS else "SMOKE",
        "checks": len(report), "seconds": perf_counter() - started,
    }), flush=True)


if __name__ == "__main__":
    main()
