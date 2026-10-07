"""Independent block-density, moment and zero-rectangle posterior checks."""

from __future__ import annotations

import json
import math
from time import perf_counter

import numpy as np
from scipy.integrate import quad
from scipy.stats import multivariate_t, t

from analysis.alternative_bayes_algebra import condition, draw_parameters, update
from analysis.alternative_bayes_likelihood import censored_loglikelihood
from analysis.calibration import FloatArray


def main() -> None:
    started = perf_counter()
    rng = np.random.default_rng(2197)
    data = rng.normal(size=(24, 4)) + np.asarray([0.2, -0.4, 0.8, 1.2])
    posterior = update(data, np.ones((24, 1)), np.ones(1))
    center = data.mean(axis=0)
    scatter = (data - center).T @ (data - center)
    np.testing.assert_allclose(posterior.coefficients[0:1].ravel(), 24 / 25 * center, atol=1e-13)
    np.testing.assert_allclose(posterior.iw_scale, 7 * np.eye(4) + scatter
                               + 24 / 25 * np.outer(center, center), atol=1e-13)
    df, location, scale = posterior.predictive(np.ones(1))
    issued = np.asarray([1.1, -0.6])
    conditional_df, conditional_location, conditional_scale = condition(
        location, scale, issued, df
    )
    assert conditional_df is not None
    ratios: list[float] = []
    for y in (np.asarray([0.1, 0.4]), np.asarray([2.0, -1.0]), np.asarray([-3.0, 4.0])):
        density_ratio = float(multivariate_t.pdf(
            np.concatenate((issued, y)), loc=location, shape=scale, df=int(df)
        ))
        density_ratio /= float(multivariate_t.pdf(
            issued, loc=location[:2], shape=scale[:2, :2], df=int(df)
        ))
        density_conditional = float(multivariate_t.pdf(
            y, loc=conditional_location, shape=conditional_scale, df=int(conditional_df)
        ))
        ratios.append(abs(density_ratio / density_conditional - 1))
    assert max(ratios) < 1e-12
    # Density integration tests scale versus covariance, not the update formula.
    scalar_scale = math.sqrt(conditional_scale.item(0, 0))
    scalar_mean = conditional_location.item(0)

    def density(z: float) -> float:
        return float(t.pdf(z, conditional_df, loc=scalar_mean, scale=scalar_scale))
    integrated_mean = quad(lambda z: z * density(z), -np.inf, np.inf, epsabs=1e-10)[0]
    integrated_variance = quad(
        lambda z: (z - scalar_mean) ** 2 * density(z), -np.inf, np.inf, epsabs=1e-10
    )[0]
    np.testing.assert_allclose(integrated_mean, scalar_mean, atol=1e-10)
    np.testing.assert_allclose(
        integrated_variance, conditional_scale.item(0, 0) * conditional_df / (conditional_df - 2),
        rtol=1e-10,
    )
    draws = np.asarray([draw_parameters(posterior, rng)[1] for _ in range(20000)])
    expected = posterior.iw_scale / (posterior.iw_df - 5)
    moment_difference: FloatArray = np.abs(np.mean(draws, axis=0) - expected)
    moment_error = float(np.max(moment_difference))
    assert moment_error < 0.015
    # Analytic orthant law is independent of conditional quadrature implementation.
    orthant_errors: list[float] = []
    for rho in (-0.8, 0.0, 0.7):
        probability = math.exp(censored_loglikelihood(
            np.zeros(2), np.zeros(2), np.asarray([[1.0, rho], [rho, 1.0]]), np.ones(2)
        ))
        oracle = 0.25 + math.asin(rho) / (2 * math.pi)
        orthant_errors.append(abs(probability - oracle))
    assert max(orthant_errors) < 1e-11
    # Conditional one-zero density must change with the revealed coordinate.
    cov = np.asarray([[1.0, 0.8], [0.8, 1.0]])
    low = censored_loglikelihood(np.asarray([-1.0, 0]), np.zeros(2), cov, np.asarray([0., 1.]))
    high = censored_loglikelihood(np.asarray([1.0, 0]), np.zeros(2), cov, np.asarray([0., 1.]))
    assert low > high + 2
    # Matrix regression equals a separate precision solve; NIG hyperparameters exact.
    h = np.column_stack((np.ones(24), np.linspace(-1, 1, 24)))
    regression = update(data[:, :1], h, np.asarray([4., 1.]), nig=True)
    np.testing.assert_allclose(
        regression.coefficients, np.linalg.solve(h.T @ h + np.diag([0.25, 1]), h.T @ data[:, :1])
    )
    assert regression.iw_df == 32
    print(json.dumps({
        "status": "PASS", "conditional_density_max_relative_error": max(ratios),
        "inverse_wishart_moment_max_error": moment_error,
        "zero_rectangle_max_error": max(orthant_errors),
        "elapsed_seconds": perf_counter() - started,
    }, indent=2))


if __name__ == "__main__":
    main()
