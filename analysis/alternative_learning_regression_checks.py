"""Executable regression derivative, Fisher, and real-interface audits."""

from __future__ import annotations

import argparse
import json
from dataclasses import replace
from datetime import date

import numpy as np

from analysis.alternative_contracts import (
    CaseInput,
    FitConfig,
    FittedModel,
    TrainingRow,
    TrainingSet,
)
from analysis.alternative_learning_regression_math import (
    initial_fit,
    natural_gradient,
    penalized_boost_score,
    score_gradient,
    stump_fit,
    stump_predict,
)


def gradient_audit() -> dict[str, float]:
    errors: dict[str, float] = {}
    for rain in (False, True):
        y = np.array([0., 1.3, 4.2, 2.1]) if rain else np.array([-2., 1.3, 4.2, 2.1])
        eta = np.column_stack((np.array([-.9, .2, .8, -.3]), np.array([.2, .5, .7, -.1])))
        _, gradient = score_gradient(y, eta, rain, 2.7)
        numeric = np.zeros_like(gradient)
        for component in range(2):
            perturbation = np.zeros_like(eta)
            perturbation[:, component] = 1e-6
            numeric[:, component] = (
                score_gradient(y, eta+perturbation, rain, 2.7)[0]
                - score_gradient(y, eta-perturbation, rain, 2.7)[0]
            ) / 2e-6
        error = max(abs((numeric-gradient).item(index)) for index in range(8))
        assert error < 2e-7, (rain, error)
        natural, clipped = natural_gradient(eta, gradient, rain, 2.7)
        assert clipped == 0
        if rain:
            p = 1 / (1 + np.exp(-eta[:, 0]))
            fisher = np.column_stack((p*(1-p), (1-p)*2.7))
        else:
            fisher = np.column_stack((np.exp(-2*eta[:, 1]), np.full(4, 2.)))
        np.testing.assert_allclose(natural*fisher, gradient, atol=1e-12)
        assert np.max(np.abs(natural-gradient)) > .1
        errors["rain" if rain else "temperature"] = error
        weights = np.array([.5, 1., .25, 1.5], dtype=np.float64)
        _, penalized_gradient = penalized_boost_score(y, eta, weights, rain, 2.7)
        for row in range(4):
            perturbation = np.zeros_like(eta)
            perturbation[row, 0] = 1e-6
            derivative = (penalized_boost_score(y, eta+perturbation, weights, rain, 2.7)[0]
                          - penalized_boost_score(y, eta-perturbation, weights, rain, 2.7)[0]) / 2e-6
            assert abs(derivative - weights.item(row)*penalized_gradient.item(row*2)) < 2e-7
    _, clipped = natural_gradient(np.array([[12., 12.]]), np.ones((1, 2)), False, 1.)
    assert clipped == 1
    intercept, shape = initial_fit(np.array([1., 2., 3.]), np.ones(3), True)
    assert np.all(np.isfinite(intercept)) and np.isfinite(shape)
    dry_intercept, dry_shape = initial_fit(np.zeros(4), np.ones(4), True)
    assert np.all(np.isfinite(dry_intercept)) and dry_intercept.item(1) == 0 and dry_shape == 1
    x = np.array([[0.], [1.], [2.], [3.]])
    response, weights = np.array([0., 0., 4., 4.]), np.array([1., 3., 2., 1.])
    fitted = stump_fit(x, response, weights)
    assert fitted[0] == 0 and fitted[1] == 1.5
    np.testing.assert_array_equal(stump_predict(x, fitted), response)
    return errors


def fixture(rain: bool) -> TrainingSet:
    variable = "prcp" if rain else "t15m"
    target = CaseInput(
        case_id="audit", init=date(2024, 1, 1), valid_start=date(2024, 1, 1),
        valid_end=date(2024, 1, 7), product="1mon", lead="W1", variable=variable,
        members=np.array([2., 3., 4.]), member_keys=("a", "b", "c"), provenance_hash="audit",
        archive_era="seven_30",
    )
    rows: list[TrainingRow] = []
    for index in range(32):
        year = 1990+index
        month = index % 12+1
        mean = 1.5 + .1*index
        response = (0. if index % 4 == 0 else mean+.4*np.sin(index)) if rain else (
            -.5+1.4*mean+.7*np.sin(index))
        rows.append(TrainingRow(
            row_id=str(index), source_case_id=str(index), source_case_init=date(2023, 1, 1),
            source_year=year, source_init=date(year, month, 1), hist_start=date(year, month, 1),
            hist_end=date(year, month, 7), product="1mon", lead="W1", variable=variable,
            ensemble=np.array([mean-.3, mean, mean+.3]), observation=response,
            member_keys=("a", "b", "c"), provenance_hash=str(index), archive_era=target.archive_era,
        ))
    return TrainingSet(
        target=target, rows=tuple(rows), year_weights=np.ones(32), cutoff=target.init,
        catalog_cutoff=target.init, held_out_years=(), train_hash="regression-audit",
        local_observations=np.array([row.observation for row in rows]),
        thresholds=np.array([2., 3.]),
    )


def interface_audit() -> dict[str, float]:
    from analysis.alternative_data import features_for_training
    from analysis.alternative_learning_regression import fit_regression
    results: dict[str, float] = {}
    for rain in (False, True):
        training = fixture(rain)
        initial, shape = initial_fit(training.local_observations, training.year_weights, rain)
        climate_loss = float(score_gradient(
            training.local_observations, np.tile(initial, (32, 1)), rain, shape,
        )[0].sum())
        models: dict[str, FittedModel] = {}
        for method in ("gamlss_ridge", "componentwise_boost", "ngboost_small"):
            model, diagnostic = fit_regression(method, training, FitConfig())
            distribution = model.predict(training.target)
            assert diagnostic.objective is not None
            assert diagnostic.convergence and np.isfinite(diagnostic.objective)
            assert np.isfinite(distribution.mean())
            quantiles = distribution.quantile(np.array([.1, .5, .9]))
            assert np.all(np.isfinite(quantiles)) and np.all(np.diff(quantiles) >= 0)
            if rain:
                assert distribution.cdf(np.array([-1.]))[0] == 0
                assert 0 < distribution.atom_mass(0.) < 1
            spec = model.to_spec()
            _ = json.dumps(spec, allow_nan=False)
            if method != "gamlss_ridge":
                assert diagnostic.objective <= climate_loss + 1e-7
            if method == "ngboost_small":
                stumps = spec["stumps"]
                assert isinstance(stumps, list) and len(stumps) == 200
                base, _ = features_for_training(training)
                _, gradient = penalized_boost_score(
                    training.local_observations, np.tile(initial, (32, 1)),
                    training.year_weights, rain, shape)
                natural, _ = natural_gradient(np.tile(initial, (32, 1)), gradient, rain, shape)
                first = stumps[0]
                assert isinstance(first, dict)
                expected = stump_fit(base, -natural[:, 0], training.year_weights)
                assert (first["feature"], first["threshold"], first["left"], first["right"]) == expected
                ordinary = stump_fit(base, -gradient[:, 0], training.year_weights)
                assert expected != ordinary
            models[method] = model
            results[f"{method}:{'rain' if rain else 'temperature'}"] = float(diagnostic.objective)
        assert models["componentwise_boost"].to_spec() != models["ngboost_small"].to_spec()
        changed = replace(training.target, members=training.target.members + 1)
        assert models["ngboost_small"].predict(changed).mean() != models["ngboost_small"].predict(training.target).mean()
    try:
        _ = fit_regression("invalid", fixture(False), FitConfig())
    except ValueError:
        raise AssertionError("Expected typed AlternativeError, not ValueError")
    except RuntimeError as error:
        assert "INPUT_CONFLICT" in str(error)
    else:
        raise AssertionError("Unknown regression method accepted")
    rain_training = fixture(True)
    for value in (0., 2.):
        degenerate = replace(rain_training, rows=tuple(
            replace(row, observation=value) for row in rain_training.rows))
        for method in ("gamlss_ridge", "componentwise_boost", "ngboost_small"):
            model, diagnostic = fit_regression(method, degenerate, FitConfig())
            assert diagnostic.convergence
            distribution = model.predict(degenerate.target)
            assert np.isfinite(distribution.mean()) and 0 < distribution.atom_mass(0.) < 1
            if value == 0:
                assert "all_dry_intensity_unidentified" in diagnostic.boundary_flags
                spec = model.to_spec()
                assert spec["shape"] == 1.
            else:
                assert "gamma_shape_bound" in diagnostic.boundary_flags
    return results


class AuditOptions(argparse.Namespace):
    math_only: bool = False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--math-only", action="store_true", help="Audit gradients/Fisher without shared integration.")
    options = AuditOptions()
    _ = parser.parse_args(namespace=options)
    report = {"gradient_errors": gradient_audit()}
    if not options.math_only:
        report["fit_objectives"] = interface_audit()
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
