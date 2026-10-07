"""Independent collapsed-Student oracle for jointly censored latent Gibbs draws."""

from __future__ import annotations

import json
import math
from time import perf_counter

import numpy as np
from scipy.integrate import quad
from scipy.stats import t

from analysis.alternative_bayes_algebra import update
from analysis.alternative_bayes_diagnostics import diagnose, mcse
from analysis.alternative_bayes_sampler import run_chains
from analysis.calibration import FloatArray


def main() -> None:
    started = perf_counter()
    revealed = np.column_stack((
        np.linspace(0.1, 1.1, 11), np.linspace(0.1, 1.1, 11) + 0.1 * np.sin(np.arange(11)),
    ))
    posterior = update(revealed, np.ones((11, 1)), np.ones(1))
    degrees, center, scale = posterior.predictive(np.ones(1))
    # Integrate a collapsed bivariate predictive over BOTH latent zero coordinates.
    # This independently integrates theta, unlike the production Gibbs transitions.
    sx = math.sqrt(scale.item(0, 0))
    sy_given_x = scale.item(1, 1) - scale.item(0, 1) ** 2 / scale.item(0, 0)

    def rectangle_integrand(x: float) -> float:
        delta = (x - center.item(0)) ** 2 / scale.item(0, 0)
        mu = center.item(1) + scale.item(1, 0) / scale.item(0, 0) * (x - center.item(0))
        conditional_scale = math.sqrt(sy_given_x * (degrees + delta) / (degrees + 1))
        return float(t.pdf(x, degrees, loc=center.item(0), scale=sx)) * float(
            t.cdf(-mu / conditional_scale, degrees + 1)
        )

    probability = quad(rectangle_integrand, -math.inf, 0, epsabs=1e-11)[0]
    oracle = quad(lambda x: x * rectangle_integrand(x), -math.inf, 0, epsabs=1e-11)[0] / probability
    values = np.vstack((revealed, np.zeros(2)))
    censored = np.zeros(values.shape)
    censored[-1] = 1
    checkpoints = run_chains(
        values, np.ones((12, 1)), np.ones(1), np.ones(1), np.empty(0), censored,
        np.empty(0), "independent_rectangle_2197", nig=False, augmented=False,
    )
    draws = next(checkpoints)
    checkpoints.close()
    latent: FloatArray = draws.monitors[..., -2:]
    assert np.all(latent <= 0)
    diagnostics = diagnose(latent)
    assert diagnostics["passed"], diagnostics
    measured = float(np.mean(latent[..., 0]))
    error = mcse(latent).item(0)
    assert abs(measured - oracle) < 6 * error
    assert probability > 0 and probability < 1
    print(json.dumps({
        "status": "PASS", "joint_zero_probability": probability,
        "collapsed_student_latent_mean": oracle, "gibbs_latent_mean": measured,
        "mean_mcse": error, "standard_errors_from_oracle": abs(measured - oracle) / error,
        "diagnostics": diagnostics, "elapsed_seconds": perf_counter() - started,
    }, indent=2))


if __name__ == "__main__":
    main()
