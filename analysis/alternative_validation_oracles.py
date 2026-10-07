"""Independent expectation and quadrature oracles, never production scores."""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from itertools import pairwise

import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr
from scipy.stats import gamma as gamma_law
from scipy.stats import poisson

from analysis.calibration import FloatArray
from analysis.data_io import Json


def floats(value: FloatArray) -> tuple[float, ...]:
    return tuple(float(value.take(i)) for i in range(value.size))


@dataclass(frozen=True, kw_only=True)
class OracleIntegral:
    value: float
    error: float


def close(actual: float, expected: float, label: str, atol: float = 2e-7,
          rtol: float = 2e-7) -> None:
    """Fail on NaN, infinity, or a discrepancy beyond fixed numerical accuracy."""
    if not math.isfinite(actual) or not math.isfinite(expected):
        raise AssertionError(f"{label}: nonfinite {actual}, {expected}")
    if abs(actual - expected) > atol + rtol * abs(expected):
        raise AssertionError(f"{label}: actual={actual}, independent={expected}")


def integrate(function: Callable[[float], float], lower: float,
              upper: float, scale: float = 1.0) -> OracleIntegral:
    """Tight independent adaptive integration with an explicit error budget."""
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError("integration scale must be finite and positive")
    result = quad(lambda z: function(z*scale), lower/scale, upper/scale,
                  epsabs=1e-8, epsrel=1e-7, limit=200, full_output=1)
    value, error = float(result[0])*scale, float(result[1])*scale
    budget = 1e-8 * scale + 1e-7 * abs(value)
    if error > budget or len(result) != 3:
        result = quad(lambda z: function(z*scale), lower/scale, upper/scale,
                      epsabs=1e-9, epsrel=1e-8, limit=400, full_output=1)
        value, error = float(result[0])*scale, float(result[1])*scale
    if not math.isfinite(value) or error > budget or len(result) != 3:
        raise AssertionError(f"quadrature uncertified: value={value}, error={error}")
    return OracleIntegral(value=float(value), error=float(error))


def crps_integral(cdf: Callable[[float], float], y: float,
                  splits: tuple[float, ...] = (), scale: float = 1.0) -> OracleIntegral:
    points = sorted({-math.inf, math.inf, y, *splits})
    values: list[OracleIntegral] = []
    for a, b in pairwise(points):
        if b <= y:
            values.append(integrate(lambda z: cdf(z) ** 2, a, b, scale))
        else:
            values.append(integrate(lambda z: (1 - cdf(z)) ** 2, a, b, scale))
    return OracleIntegral(value=math.fsum(v.value for v in values),
                          error=math.fsum(v.error for v in values))


def mean_integral(cdf: Callable[[float], float], scale: float = 1.0,
                  splits: tuple[float, ...] = ()) -> float:
    points = sorted({-math.inf, 0., math.inf, *splits})
    return math.fsum(
        integrate(lambda z: 1-cdf(z), a, b, scale).value if a >= 0 else
        -integrate(cdf, a, b, scale).value for a, b in pairwise(points))


def empirical_crps(values: FloatArray, weights: FloatArray, y: float) -> float:
    """O(n^2) expectation identity, intentionally unlike sorted production sums."""
    first = math.fsum(float(w) * abs(float(x) - y)
                      for x, w in zip(floats(values), floats(weights), strict=True))
    second = math.fsum(float(wi) * float(wj) * abs(float(xi) - float(xj))
                       for xi, wi in zip(floats(values), floats(weights), strict=True)
                       for xj, wj in zip(floats(values), floats(weights), strict=True))
    return first - second / 2


def normal_absolute(mu: float, sigma: float) -> float:
    if sigma == 0:
        return abs(mu)
    z = mu / sigma
    return 2 * sigma * math.exp(-z * z / 2) / math.sqrt(2 * math.pi) + mu * (
        2 * float(ndtr(z)) - 1)


def normal_mixture_crps(mus: FloatArray, sigmas: FloatArray,
                        weights: FloatArray, y: float) -> float:
    first = math.fsum(float(w) * normal_absolute(float(mu) - y, float(sd))
                      for mu, sd, w in zip(floats(mus), floats(sigmas), floats(weights), strict=True))
    cross = math.fsum(
        float(wi) * float(wj) * normal_absolute(
            float(mi - mj), math.hypot(float(si), float(sj)))
        for mi, si, wi in zip(floats(mus), floats(sigmas), floats(weights), strict=True)
        for mj, sj, wj in zip(floats(mus), floats(sigmas), floats(weights), strict=True))
    return first - cross / 2


def tweedie_reference(mu: float, phi: float, power: float,
                     y: float) -> tuple[float, float, float, float]:
    """Direct Poisson-Gamma convolution, independently chosen fixed tail bound."""
    rate = math.pow(mu, 2 - power) / (phi * (2 - power))
    shape = (2 - power) / (power - 1)
    scale = phi * (power - 1) * math.pow(mu, power - 1)
    upper = int(poisson.ppf(1 - 1e-14, rate)) + 4
    indices = np.arange(1, upper + 1, dtype=np.float64)
    masses = np.asarray(poisson.pmf(indices, rate), dtype=np.float64)
    atom = math.exp(-rate)
    cdf = atom + float(np.sum(masses * gamma_law.cdf(y, indices * shape, scale=scale)))
    second = float(np.sum(masses * indices * shape * (1 + indices * shape) * scale**2))
    mean = float(np.sum(masses * indices * shape * scale))
    close(atom + float(np.sum(masses)), 1, "independent convolution mass", atol=1e-12)
    close(mean, mu, "independent convolution mean", atol=1e-10)
    return cdf if y >= 0 else 0, atom, mean, second - mean**2


def niw_conditional_reference(z: FloatArray, x: float) -> tuple[float, float, float]:
    """Small d=2 NIW calculation by augmented crossproducts, not fit helper reuse."""
    n = len(z)
    augmented = np.vstack((np.zeros((1, 2)), z))
    posterior_mean = np.sum(augmented, axis=0) / (n + 1)
    psi = 7 * np.eye(2) + augmented.T @ augmented - (
        n + 1) * np.outer(posterior_mean, posterior_mean)
    df = n + 9
    scale = (n + 2) / ((n + 1) * df) * psi
    mx, my = floats(posterior_mean)
    xx, xy, _, yy = floats(scale)
    difference = x - mx
    location = my + xy / xx * difference
    residual = yy - xy**2 / xx
    conditional_scale = (df + difference**2 / xx) / (df + 1) * residual
    return float(df + 1), location, math.sqrt(conditional_scale)


def self_checks() -> dict[str, Json]:
    """Execute oracles even while independently owned production modules arrive."""
    normal: Callable[[float], float] = lambda x: 0.5 * math.erfc(-x / math.sqrt(2))
    score = crps_integral(normal, 0).value
    close(score, (math.sqrt(2) - 1) / math.sqrt(math.pi), "known Normal CRPS")
    censored: Callable[[float], float] = lambda x: 0.0 if x < 0 else normal(x)
    close(mean_integral(censored), 1 / math.sqrt(2 * math.pi), "censored mean")
    close(crps_integral(censored, 0, (0,)).value, score / 2, "censored CRPS")
    values = np.array([0., 0., 2., 5.])
    weights = np.array([.1, .2, .3, .4])
    close(empirical_crps(values, weights, 1), 1.06, "weighted tied empirical")
    close(empirical_crps(np.array([3.]), np.array([1.]), 1), 2, "singleton")
    mus, sigmas, mixing = np.array([-2., 2.]), np.ones(2), np.array([.5, .5])
    mixture_cdf: Callable[[float], float] = lambda x: float(.5 * ndtr(x + 2) + .5 * ndtr(x - 2))
    mixture_score = normal_mixture_crps(mus, sigmas, mixing, 0)
    close(mixture_score, crps_integral(mixture_cdf, 0).value, "mixture cross expectation")
    component_average = normal_absolute(2, 1) - 1 / math.sqrt(math.pi)
    if abs(component_average - mixture_score) < .5:
        raise AssertionError("mixture oracle failed to distinguish component-score average")
    squared_mean = integrate(lambda z: 2 * z * (1 - censored(z)), 0, math.inf).value
    close(squared_mean, .5, "Jensen censored square")
    if squared_mean <= mean_integral(censored) ** 2:
        raise AssertionError("Jensen moment oracle did not detect inverse(mean) defect")
    _, atom, mean, variance = tweedie_reference(3, 2, 1.5, 2)
    close(variance, 2 * 3**1.5, "Tweedie exact variance")
    return {"status": "PASS", "known_normal_crps": score,
            "mixture_crps": mixture_score, "incorrect_component_average": component_average,
            "tweedie_atom": atom, "tweedie_mean": mean, "checks": 12}
