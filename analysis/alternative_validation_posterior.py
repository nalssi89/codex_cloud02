"""Censor rectangle likelihood and genuine convergence-diagnostic adversaries."""

from __future__ import annotations

import math

import numpy as np
from scipy.special import ndtr

from analysis.alternative_validation_io import number
from analysis.alternative_validation_oracles import close
from analysis.alternative_validation_reference import reference_crps, reference_mean
from analysis.data_io import Json


def posterior_checks() -> dict[str, Json]:
    from analysis.alternative_bayes_diagnostics import diagnose, mcse
    from analysis.alternative_bayes_distribution import BayesianScalar
    from analysis.alternative_bayes_likelihood import censored_loglikelihood

    rho = .8
    covariance = np.array([[1., rho], [rho, 1.]])
    actual = censored_loglikelihood(np.zeros(2), np.zeros(2), covariance, np.ones(2))
    expected = .25+math.asin(rho)/(2*math.pi)
    close(math.exp(actual), expected, "correlated zero rectangle", atol=1e-11)
    if abs(math.exp(actual)-.25) < .1:
        raise AssertionError("joint censor likelihood replaced with marginal product")
    conditional = censored_loglikelihood(np.array([1., 0.]), np.zeros(2),
                                         covariance, np.array([0., 1.]))
    density = math.exp(-.5)/math.sqrt(2*math.pi)
    expected_conditional = density*float(ndtr(-rho/math.sqrt(1-rho*rho)))
    close(math.exp(conditional), expected_conditional,
          "conditional censor rectangle given revealed coordinate", atol=1e-11)
    rng = np.random.default_rng(20261007)
    independent = rng.normal(size=(4, 4096, 3))
    good = diagnose(independent)
    if good["passed"] is not True:
        raise AssertionError("independent diagnostic reference unexpectedly fails")
    separated = independent + np.arange(4)[:, None, None]*3
    bad_location = diagnose(separated)
    if bad_location["passed"] is not False or number(bad_location["rhat_max"]) <= 1.01:
        raise AssertionError("Rhat fails to detect separated chains")
    sticky = np.repeat(rng.normal(size=(4, 64, 1)), 64, axis=1)
    bad_ess = diagnose(sticky)
    if bad_ess["passed"] is not False or number(bad_ess["ess_bulk_min"]) >= 400:
        raise AssertionError("ESS fails to detect strongly autocorrelated draws")
    error = mcse(independent)
    if np.any(error <= 0) or np.any(error > .04):
        raise AssertionError("independent chain MCSE invalid")
    inverse_checks: dict[str, Json] = {}
    for transform in ("temperature", "sqrt", "yj", "logsinh"):
        law = BayesianScalar(locations=np.array([.2]), scales=np.array([.7]),
                             weights=np.ones(1), df=9., transform=transform)
        expected_mean = reference_mean(law.to_spec())
        expected_crps = reference_crps(law.to_spec(), 30.)
        close(law.mean(), expected_mean, "Bayesian inverse mean:"+transform,
              atol=2e-6, rtol=2e-6)
        close(law.crps(30.), expected_crps, "Bayesian inverse CRPS:"+transform,
              atol=2e-6, rtol=2e-6)
        inverse_checks[transform] = {"expected_mean": expected_mean,
                                    "expected_crps": expected_crps}
    return {"status": "PASS", "joint_zero_probability": expected,
            "incorrect_independent_probability": .25, "iid_diagnostics": good,
            "separated_rhat": bad_location["rhat_max"],
            "sticky_bulk_ess": bad_ess["ess_bulk_min"],
            "mcse_max": float(np.max(error)), "SC2_Bayesian_inverse": inverse_checks}
