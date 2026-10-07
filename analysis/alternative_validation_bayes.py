"""Independent conjugate posterior and parameter-uncertainty audit."""

from __future__ import annotations

import math

import numpy as np
from scipy.special import ndtr
from scipy.stats import invwishart, t

from analysis.alternative_validation_oracles import (
    close,
    floats,
    niw_conditional_reference,
)
from analysis.calibration import FloatArray
from analysis.data_io import Json


def bayes_checks() -> dict[str, Json]:
    from analysis.alternative_bayes_algebra import condition, update

    z = np.array([[-1., -.5], [0., .3], [.7, 1.2], [1.5, 1.8]], dtype=np.float64)
    design = np.ones((len(z), 1))
    posterior = update(z, design, np.ones(1))
    df, location, scale = posterior.predictive(np.ones(1))
    conditioned_df, conditioned_location, conditioned_scale = condition(
        location, scale, np.array([.8]), df)
    expected_df, expected_loc, expected_sd = niw_conditional_reference(z, .8)
    assert conditioned_df is not None
    close(conditioned_df, expected_df, "NIW conditional df", atol=1e-12)
    close(float(conditioned_location.take(0)), expected_loc, "NIW conditional location", atol=1e-12)
    close(math.sqrt(float(conditioned_scale.take(0))), expected_sd,
          "Student scale is not covariance", atol=1e-12)
    # Independent SciPy inverse-Wishart, not the production Bartlett implementation.
    rng = np.random.default_rng(20261007)
    n_draws = 65536
    covariances: FloatArray = np.asarray(invwishart.rvs(
        df=10 + len(z), scale=posterior.iw_scale, size=n_draws, random_state=rng),
        dtype=np.float64)
    mean_noise = rng.normal(size=(n_draws, 2))
    roots = np.linalg.cholesky(covariances)
    means = location + np.sum(roots * mean_noise[:, None, :], axis=2) / math.sqrt(len(z) + 1)
    variance_x = covariances[:, 0, 0]
    dx = .8 - means[:, 0]
    log_weights = -.5 * (np.log(2 * np.pi * variance_x) + dx**2 / variance_x)
    weights: FloatArray = np.exp(log_weights - np.max(log_weights))
    weights = weights / float(np.sum(weights))
    conditional_means = means[:, 1] + covariances[:, 1, 0] / variance_x * dx
    conditional_sd = np.sqrt(covariances[:, 1, 1] -
                             covariances[:, 1, 0] ** 2 / variance_x)
    threshold = expected_loc + expected_sd
    indicators: FloatArray = np.asarray(
        ndtr((threshold - conditional_means) / conditional_sd), dtype=np.float64)
    estimated = float(np.sum(weights * indicators))
    exact = float(t.cdf(1, expected_df))
    # Conservative fixed bound > six independent MC standard errors.
    mcse = math.sqrt(math.fsum(w*w*(p-estimated)**2 for w, p in zip(
        floats(weights), floats(indicators), strict=True)))
    close(estimated, exact, "independent posterior draws", atol=6 * mcse + 2e-4, rtol=0)
    effective = 1 / float(np.sum(weights * weights))
    if effective < 20000:
        raise AssertionError("posterior-draw oracle importance sample inadequate")
    # Exact NIG scalar update and MNIW regression are separate numerical examples.
    y = np.array([[-1.], [0.], [2.], [3.]])
    h = np.column_stack((np.ones(4), np.array([-1., 0., 1., 2.])))
    v0 = np.diag([4., 1.])
    precision = np.linalg.inv(v0) + h.T @ h
    expected_v = np.linalg.inv(precision)
    expected_beta = expected_v @ h.T @ y
    expected_scale = 6 + float((y.T @ y - expected_beta.T @ precision @ expected_beta).take(0))
    nig = update(y, h, np.array([4., 1.]), nig=True)
    close(float(nig.iw_scale.take(0)), expected_scale, "NIG residual scale", atol=1e-12)
    np.testing.assert_allclose(nig.coefficients, expected_beta, atol=1e-12, rtol=1e-12)
    trend = update(z, h, np.array([1., 4.]))
    expected_v2 = np.linalg.inv(np.diag([1., .25]) + h.T @ h)
    expected_b2 = expected_v2 @ h.T @ z
    expected_s2 = 7*np.eye(2) + z.T @ z - expected_b2.T @ (
        np.diag([1., .25]) + h.T @ h) @ expected_b2
    np.testing.assert_allclose(trend.iw_scale, expected_s2, atol=1e-12, rtol=1e-12)
    # An exp(Student) positive moment is divergent: right-tail integrand grows.
    logs = [x + float(t.logpdf(x, 4)) for x in (100., 200., 400.)]
    if not logs[0] < logs[1] < logs[2]:
        raise AssertionError("exp(Student) moment-existence counterexample failed")
    plugin_sd = math.sqrt(float(np.cov(z.T).take(3)))
    if abs(expected_sd - plugin_sd) < .05:
        raise AssertionError("small-n uncertainty oracle failed to distinguish plug-in")
    return {"status": "PASS", "conditional_df": expected_df,
            "conditional_scale_sd": expected_sd, "independent_draws": n_draws,
            "mcse": mcse, "importance_ess": effective, "posterior_cdf": estimated,
            "exact_cdf": exact, "exp_student_positive_mean": "DIVERGENT"}
