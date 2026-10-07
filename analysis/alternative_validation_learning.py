"""Learning-law tests with exact Fisher and constrained isotonic references."""

from __future__ import annotations

from dataclasses import replace
from datetime import date

import numpy as np
from scipy.optimize import LinearConstraint, minimize
from scipy.special import expit

from analysis.alternative_contracts import (
    CaseInput,
    FeatureSpec,
    FitConfig,
    TrainingRow,
    TrainingSet,
)
from analysis.alternative_validation_forest import forest_weights
from analysis.alternative_validation_io import mapping, number, sequence, text
from analysis.alternative_validation_oracles import close, empirical_crps, floats
from analysis.alternative_validation_reference import vector
from analysis.data_io import Json


def fixture() -> TrainingSet:
    target = CaseInput(case_id="validation", init=date(2026, 2, 1),
                       valid_start=date(2026, 2, 1), valid_end=date(2026, 2, 7),
                       product="1mon", lead="W1", variable="t15m",
                       members=np.array([4.]), member_keys=("one",), provenance_hash="synthetic")
    rows = tuple(TrainingRow(
        row_id=f"validation:{year}:{j}", source_case_id=target.case_id,
        source_case_init=date(2022, 2, 1), source_year=year, source_init=date(year, 2, 1),
        hist_start=date(year, 2, 1), hist_end=date(year, 2, 7),
        product="1mon", lead="W1", variable="t15m",
        ensemble=np.array([float((year-1990)//2)]),
        observation=float((year-1990)//3+j), member_keys=("one",),
        provenance_hash="synthetic", archive_era="three_24")
        for year in range(1990, 2010) for j in (0,))
    observations = np.array([r.observation for r in rows])
    return TrainingSet(target=target, rows=rows,
                       year_weights=np.ones(len(rows), dtype=np.float64),
                       cutoff=target.init, catalog_cutoff=target.init, held_out_years=(2026,),
                       train_hash="synthetic", local_observations=observations,
                       thresholds=np.quantile(observations, [1/3, 2/3]))


def learning_checks() -> dict[str, Json]:
    from analysis import alternative_learning_order as order
    from analysis.alternative_learning_category import (
        fit_category,
        ordinal_probabilities,
    )
    from analysis.alternative_learning_regression_math import (
        initial_fit,
        natural_gradient,
        score_gradient,
    )

    eta = np.array([[1., np.log(2.)], [-1., np.log(.5)]])
    _, gradient = score_gradient(np.array([3., 2.]), eta, False, 1)
    actual, clips = natural_gradient(eta, gradient, False, 1)
    expected = gradient * np.array([[4., .5], [.25, .5]])
    np.testing.assert_allclose(actual, expected, atol=1e-12)
    if clips or np.allclose(actual, gradient):
        raise AssertionError("natural gradient did not apply Fisher inverse")
    rain_eta = np.array([[0., 1.], [-2., 2.]])
    _, rain_gradient = score_gradient(np.array([0., 2.]), rain_eta, True, 3)
    actual_rain, _ = natural_gradient(rain_eta, rain_gradient, True, 3)
    p0 = expit(rain_eta[:, 0])
    np.testing.assert_allclose(actual_rain, rain_gradient / np.column_stack(
        (p0*(1-p0), 3*(1-p0))), atol=1e-12)
    all_wet, _ = initial_fit(np.linspace(1., 5., 20), np.ones(20), True)
    occurrence = float(expit(all_wet.take(0)))
    if not 0 < occurrence < 1:
        raise AssertionError("all-wet penalized occurrence separates to probability boundary")
    response, weights = np.array([0., 1., 0., 1.]), np.array([1., 3., 2., 1.])
    differences = np.eye(4)[:-1]-np.eye(4)[1:]
    reference = minimize(lambda z: float(np.sum(weights*(z-response)**2)),
                         np.full(4, .5), jac=lambda z: 2*weights*(z-response),
                         constraints=LinearConstraint(differences, 0, np.inf),
                         method="SLSQP", options={"ftol": 1e-12})
    if not reference.success:
        raise AssertionError("independent constrained isotonic oracle failed")
    np.testing.assert_allclose(order.antitonic(response, weights), reference.x, atol=1e-7)
    years = np.repeat(np.arange(10, dtype=np.int64), [1, 2]*5)
    sampled = np.array([0, 0, 0, 2, 2, 4, 5, 6, 7, 9])
    leaf_weights = np.bincount(sampled, minlength=10)[years]/np.bincount(years)[years]
    leaf = order.fit_tree(np.zeros((len(years), 8)), np.ones(len(years)), years, leaf_weights,
                          np.flatnonzero(leaf_weights > 0), np.random.default_rng(3))
    np.testing.assert_allclose(leaf.masses, leaf_weights[leaf_weights > 0]/10, atol=1e-12)
    probabilities = ordinal_probabilities(np.array([0., -2., .8]),
                                         np.array([[-100.], [0.], [100.]]))
    if np.any(probabilities < 0):
        raise AssertionError("ordinal probabilities cross")
    np.testing.assert_allclose(probabilities.sum(axis=1), 1, atol=1e-12)
    result: dict[str, Json] = {"status": "PASS", "fisher": "EXACT",
                               "bootstrap_leaf_mass": "PASS", "isotonic": "PASS"}
    training = fixture()
    constant_rows = tuple(replace(r, observation=2.) for r in training.rows)
    collapsed = replace(training, rows=constant_rows,
                        local_observations=np.full(len(constant_rows), 2.),
                        thresholds=np.array([2., 2.]))
    for method in ("ordinal_logit", "elr_threshold_logit"):
        category_model, _ = fit_category(method, collapsed)
        prediction = category_model.predict(collapsed.target, collapsed.thresholds)
        close(float(np.sum(prediction.probabilities)), 1, method+" mass")
        close(float(prediction.probabilities.take(1)), 0, method+" empty middle")
        if np.any(prediction.probabilities < 0):
            raise AssertionError("empty-category model produces negative probability")
        result[method] = {"status": "PASS", "equal_threshold_middle": 0.}
    for method in ("qrf_year_forest", "idr_mean_order"):
        model, diagnostics = order.fit_order(method, training, FitConfig(seed=42))
        law = model.predict(training.target)
        close(float(law.cdf(np.array([np.inf])).take(0)), 1, method+" mass")
        if diagnostics.n_years != 20 or not np.isfinite(law.crps(3)):
            raise AssertionError(method+" missing annual law")
        if method == "qrf_year_forest":
            from analysis.alternative_data import features_for_case
            saved = model.to_spec()
            f = mapping(saved["features"])
            feature_spec = FeatureSpec(names=tuple(text(v) for v in sequence(f["names"])),
                                       center=vector(f["center"]), scale=vector(f["scale"]),
                                       predictor_power=number(f["predictor_power"]))
            expected_weights = forest_weights(saved, features_for_case(training.target, feature_spec))
            support = vector(saved["observations"])
            grid = np.unique(support)
            expected_cdf = np.array([float(np.sum(expected_weights[support <= value]))
                                     for value in floats(grid)])
            np.testing.assert_allclose(law.cdf(grid), expected_cdf, atol=1e-12, rtol=1e-12)
            close(law.crps(3), empirical_crps(support, expected_weights, 3),
                  "QRF predictive leaf-mixture CRPS")
        if method == "idr_mean_order":
            cdfs = np.stack([model.predict(replace(
                training.target, members=np.array([x]))).cdf(np.array([1., 3., 6.]))
                for x in (0., 2., 4., 8., 10.)])
            if np.any(np.diff(cdfs, axis=0) > 1e-10):
                raise AssertionError("IDR stochastic order fails")
        result[method] = {"status": "PASS", "mean": law.mean(), "crps": law.crps(3)}
    return result
