"""Executable density/pair-expectation oracle independent of CDF-square CRPS."""

from __future__ import annotations

import json
import math
from time import perf_counter
from unittest.mock import patch

import numpy as np
from scipy.integrate import quad
from scipy.stats import norm, t

from analysis.alternative_bayes_distribution import (
    BayesianScalar,
    distribution_from_spec,
    forward,
    inverse,
)
from analysis.alternative_contracts import AlternativeError
from analysis.calibration import FloatArray


def array(value: object) -> FloatArray:
    return np.asarray(value, dtype=np.float64)


def physical(z: float, transform: str) -> float:
    """Independent direct formulas; logsinh switches only beyond machine precision."""
    if transform == "temperature":
        return 10 + 10 * z
    if z <= 0:
        return 0
    if transform == "sqrt":
        return 100 * z * z
    if transform == "yj":
        return 100 * ((1 + z / 2)**2 - 1)
    u = z + math.log(math.sinh(1))
    return 100 * ((math.asinh(math.exp(u)) if u < 40 else u + math.log(2)) - 1)


def oracle(law: BayesianScalar, observation: float) -> tuple[float, float]:
    """CRPS=E|Y-y|-E[Y(2F(Y)-1)]; the zero atom contributes only to E|Y-y|."""
    lower = -math.inf if law.transform == "temperature" else 0.0
    def density(z: float) -> float:
        x = (z - law.locations) / law.scales
        f = norm.pdf(x) if law.df is None else t.pdf(x, law.df)
        return float(np.sum(f * law.weights / law.scales))
    def cdf(z: float) -> float:
        x = (z - law.locations) / law.scales
        f = norm.cdf(x) if law.df is None else t.cdf(x, law.df)
        return float(np.sum(f * law.weights))
    def expected(z: float) -> float:
        return physical(z, law.transform) * density(z)
    def pair(z: float) -> float:
        return physical(z, law.transform) * (2 * cdf(z) - 1) * density(z)
    boundary = float(forward(array(max(observation, 0) if lower == 0 else observation),
                             law.transform))
    atom = cdf(0) if lower == 0 else 0
    mean = float(quad(expected, lower, math.inf, epsabs=1e-8, epsrel=1e-9)[0])
    absolute = float(quad(lambda z: abs(physical(z, law.transform) - observation) * density(z),
                          lower, boundary, epsabs=1e-8, epsrel=1e-9)[0])
    absolute += float(quad(lambda z: abs(physical(z, law.transform) - observation) * density(z),
                           boundary, math.inf, epsabs=1e-8, epsrel=1e-9)[0])
    pair_expectation = float(quad(pair, lower, math.inf, epsabs=1e-8, epsrel=1e-9)[0])
    return mean, absolute + atom * abs(observation) - pair_expectation


def precision_gate_audit() -> None:
    """Exercise the real score-time precision gate and its serialized metadata."""
    passing = BayesianScalar(locations=np.full(128, .6), scales=np.full(128, .9),
                             weights=np.ones(128), df=None, transform="temperature",
                             chain_shape=(4, 32), training_sd=1.0)
    restored = distribution_from_spec(passing.to_spec())
    assert restored.chain_shape == (4, 32) and restored.training_sd == 1
    np.testing.assert_allclose(restored.crps(13), oracle(restored, 13)[1], rtol=1e-8)
    actual_observations: list[float] = []
    def gate(distribution: BayesianScalar, observation: float) -> tuple[float, float, bool]:
        assert distribution is restored
        actual_observations.append(observation)
        return .1, .01, False
    with patch("analysis.alternative_bayes_precision.score_crps_precision", side_effect=gate):
        try:
            _ = restored.crps(13)
        except AlternativeError as error:
            assert error.code == "POSTERIOR_DIAGNOSTICS_FAILED"
        else:
            raise AssertionError("failed actual-observation gate was accepted")
    assert actual_observations == [13]
    failing = BayesianScalar(locations=np.linspace(-.5, 1.5, 128), scales=np.full(128, .9),
                             weights=np.ones(128), df=None, transform="temperature",
                             chain_shape=(4, 32), training_sd=1e-12)
    try:
        _ = failing.crps(13)
    except AlternativeError as error:
        assert error.code == "POSTERIOR_DIAGNOSTICS_FAILED"
    else:
        raise AssertionError("real precision failure was accepted")


def main() -> None:
    start = perf_counter()
    checks = 0
    maximum_error = 0.0
    for transform in ("temperature", "sqrt", "yj", "logsinh"):
        values = array([-100, 0, 10, 100]) if transform == "temperature" else array([0, 1e-8, 1, 100, 1e8])
        np.testing.assert_allclose(inverse(forward(values, transform), transform), values,
                                   rtol=1e-7, atol=1e-12)
        if transform != "temperature":
            assert float(forward(array(0), transform)) == 0
            assert float(inverse(array(0), transform)) == 0
        for df in (None, 7.0):
            law = BayesianScalar(locations=array([-.4, 1.2] if df is None else [.6]),
                                 scales=array([.8, .5] if df is None else [.9]),
                                 weights=array([.3, .7] if df is None else [1]),
                                 df=df, transform=transform)
            endpoints = law.cdf(array([-math.inf, math.inf]))
            np.testing.assert_array_equal(endpoints, [0, 1])
            p = array([0, .001, .1, .5, .9, .999, 1])
            q = law.quantile(p)
            interior = q[1:-1]
            expected_cdf = np.maximum(p[1:-1], law.atom_mass(0))
            np.testing.assert_allclose(law.cdf(interior), expected_cdf, atol=3e-13, rtol=3e-13)
            if transform != "temperature":
                assert float(q.take(0)) == 0 and math.isinf(float(q.take(-1)))
                assert float(law.cdf_left(array(0))) == 0
            for observation in (-5.0, 0.0, 100.0):
                expected_mean, expected_crps = oracle(law, observation)
                np.testing.assert_allclose(law.mean(), expected_mean, rtol=2e-8, atol=2e-8)
                actual = law.crps(observation)
                maximum_error = max(maximum_error, abs(actual - expected_crps))
                np.testing.assert_allclose(actual, expected_crps, rtol=2e-8, atol=2e-8)
                checks += 1
            restored = distribution_from_spec(law.to_spec())
            np.testing.assert_array_equal(restored.cdf(array([0, 10, 100])),
                                          law.cdf(array([0, 10, 100])))
            x, delta = 15.0, 1e-4
            numerical_density = float(law.cdf(array(x + delta)) - law.cdf(array(x - delta))) / (2 * delta)
            np.testing.assert_allclose(math.exp(law.log_density(x)), numerical_density, rtol=1e-7)
    huge = inverse(array([1000, 1e6, math.inf]), "logsinh")
    assert np.all(np.isfinite(huge[:2])) and math.isinf(float(huge.take(-1)))
    for transform, df in (("sqrt", 2), ("logsinh", 1)):
        try:
            _ = BayesianScalar(locations=array([0]), scales=array([1]), weights=array([1]),
                               df=df, transform=transform)
        except AlternativeError:
            pass
        else:
            raise AssertionError("infinite mean Student was accepted")
    large = BayesianScalar(locations=np.linspace(-1, 2, 8192), scales=np.ones(8192),
                           weights=np.ones(8192), df=None, transform="sqrt")
    vector_start = perf_counter()
    assert np.all(np.diff(large.cdf(array([0, 10, 100, 1000]))) > 0)
    probabilities = array([.3, .7, .99])
    np.testing.assert_allclose(large.cdf(large.quantile(probabilities)),
                               np.maximum(probabilities, large.atom_mass(0)), atol=1e-12)
    with patch("analysis.alternative_bayes_distribution.quad",
               return_value=(0.0, 1.0, {}, "forced quadrature failure")):
        try:
            _ = large.crps(0)
        except AlternativeError as error:
            assert error.code == "NUMERICAL_DISTRIBUTION_FAILED"
        else:
            raise AssertionError("quadrature failure was not reported")
    precision_gate_audit()
    print(json.dumps({"oracle_crps_checks": checks, "maximum_absolute_crps_error": maximum_error,
                      "actual_observation_precision_gate": "PASS",
                      "8192_draw_cdf_ppf_seconds": perf_counter() - vector_start,
                      "elapsed_seconds": perf_counter() - start, "status": "PASS"}))


if __name__ == "__main__":
    main()
