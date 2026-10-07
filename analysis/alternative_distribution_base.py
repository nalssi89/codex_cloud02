"""Immutable empirical and SciPy-backed original-unit predictive laws."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from numpy.typing import ArrayLike
from scipy import stats
from scipy.special import ndtr
from scipy.stats._distn_infrastructure import rv_continuous_frozen

from analysis.alternative_contracts import PredictiveDistribution
from analysis.calibration import FloatArray, gaussian_crps
from analysis.data_io import Json


def array(value: ArrayLike) -> FloatArray:
    return np.asarray(value, dtype=np.float64)


def floats(value: FloatArray) -> tuple[float, ...]:
    return tuple(float(value.take(i)) for i in range(value.size))


def probabilities(value: FloatArray) -> FloatArray:
    result = array(value)
    if np.any(~np.isfinite(result)) or np.any((result < 0) | (result > 1)):
        raise ValueError("probabilities must be finite and in [0, 1]")
    return result


def normalized(weights: FloatArray) -> FloatArray:
    result = array(weights).copy()
    if result.ndim != 1 or result.size == 0 or np.any(~np.isfinite(result)):
        raise ValueError("weights must be a nonempty finite vector")
    if np.any(result < 0) or not float(result.sum()) > 0:
        raise ValueError("weights must be nonnegative with positive total")
    result /= result.sum()
    result.flags.writeable = False
    return result


def numeric_score(law: PredictiveDistribution, observation: float) -> float:
    from analysis.alternative_distribution_integrals import cdf_crps

    answer = cdf_crps(law, observation, max(1.0, abs(law.mean())))
    if not answer.converged:
        raise ArithmeticError(f"CRPS quadrature failed: error={answer.error}")
    return answer.value


@dataclass(frozen=True, slots=True, kw_only=True)
class Empirical:
    values: FloatArray
    weights: FloatArray

    def _cumulative(self) -> FloatArray:
        cumulative = np.concatenate(([0.0], np.cumsum(self.weights)))
        cumulative[-1] = 1.0
        return array(cumulative)

    def cdf(self, value: FloatArray) -> FloatArray:
        index = np.searchsorted(self.values, value, side="right")
        return array(self._cumulative()[index])

    def cdf_left(self, value: FloatArray) -> FloatArray:
        index = np.searchsorted(self.values, value, side="left")
        return array(self._cumulative()[index])

    def sf(self, value: FloatArray) -> FloatArray:
        index = np.searchsorted(self.values, value, side="right")
        tails = np.concatenate((np.cumsum(self.weights[::-1])[::-1], [0.0]))
        tails[0] = 1.0
        return array(tails[index])

    def quantile(self, probability: FloatArray) -> FloatArray:
        p = probabilities(probability)
        index = np.searchsorted(np.cumsum(self.weights), p, side="left")
        return array(self.values[np.minimum(index, self.values.size - 1)])

    def mean(self) -> float:
        return float(np.sum(self.values*self.weights))

    def crps(self, observation: float) -> float:
        if not math.isfinite(observation):
            raise ValueError("observation must be finite")
        w, x = self.weights, self.values
        return float(np.sum(w*np.abs(x-observation))
                     - np.sum(w*x*(2*np.cumsum(w)-w-1)))

    def atom_mass(self, value: float) -> float:
        return float(self.weights[self.values == value].sum())

    def atom_locations(self) -> tuple[float, ...]:
        return floats(self.values)

    def log_density(self, value: float) -> float:
        if math.isnan(value):
            raise ValueError("density argument must not be NaN")
        return -math.inf

    def to_spec(self) -> dict[str, Json]:
        return {"tag": "weighted_empirical",
                "values": list(floats(self.values)),
                "weights": list(floats(self.weights))}


def empirical(values: FloatArray, weights: FloatArray) -> Empirical:
    x, w = array(values), normalized(weights)
    if x.ndim != 1 or x.shape != w.shape or np.any(~np.isfinite(x)):
        raise ValueError("values must be a matching finite vector")
    keep = w > 0
    x, w = x[keep], w[keep]
    unique, inverse = np.unique(x, return_inverse=True)
    masses = np.bincount(inverse, weights=w)
    unique.flags.writeable = False
    return Empirical(values=unique, weights=normalized(array(masses)))


@dataclass(frozen=True, slots=True, kw_only=True)
class ScientificLaw:
    tag: str
    parameters: tuple[float, ...]
    censor_zero: bool = False
    _frozen: rv_continuous_frozen = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_frozen", self._build())

    def _law(self) -> rv_continuous_frozen:
        return self._frozen

    def _build(self) -> rv_continuous_frozen:
        p = self.parameters
        if self.tag == "normal":
            return stats.norm(loc=p[0], scale=p[1])
        if self.tag == "student_t":
            return stats.t(p[0], loc=p[1], scale=p[2])
        if self.tag == "logistic":
            return stats.logistic(loc=p[0], scale=p[1])
        if self.tag == "lognormal":
            return stats.lognorm(p[1], scale=math.exp(p[0]))
        if self.tag == "gamma":
            return stats.gamma(p[0], loc=p[2], scale=p[1])
        if self.tag == "censored_gev":
            return stats.genextreme(-p[2], loc=p[0], scale=p[1])
        raise ValueError(f"unknown scientific law {self.tag}")

    def cdf(self, value: FloatArray) -> FloatArray:
        x = array(value)
        if not self.censor_zero:
            return array(self._law().cdf(x))
        result = array(np.where(x < 0, 0.0, np.nan))
        physical = x >= 0
        result[physical] = array(self._law().cdf(x[physical]))
        return result

    def cdf_left(self, value: FloatArray) -> FloatArray:
        x = array(value)
        return array(np.where(x <= 0, 0, self.cdf(x))) if self.censor_zero else self.cdf(x)

    def sf(self, value: FloatArray) -> FloatArray:
        x = array(value)
        if not self.censor_zero:
            return array(self._law().sf(x))
        result = array(np.where(x < 0, 1.0, np.nan))
        physical = x >= 0
        result[physical] = array(self._law().sf(x[physical]))
        return result

    def quantile(self, probability: FloatArray) -> FloatArray:
        q = array(self._law().ppf(probabilities(probability)))
        return array(np.maximum(0, q)) if self.censor_zero else q

    def mean(self) -> float:
        p = self.parameters
        if not self.censor_zero:
            return float(self._law().mean())
        if self.tag == "normal":
            z = p[0] / p[1]
            return p[0] * float(ndtr(z)) + p[1] * math.exp(-z*z/2) / math.sqrt(2*math.pi)
        if self.tag == "gamma":
            k, theta, shift = p
            if shift >= 0:
                return k * theta + shift
            return (k * theta * float(stats.gamma.sf(-shift, k+1, scale=theta))
                    + shift * float(stats.gamma.sf(-shift, k, scale=theta)))
        from analysis.alternative_distribution_integrals import survival_mean

        return survival_mean(self)

    def crps(self, observation: float) -> float:
        if self.tag == "normal":
            y = max(0.0, observation) if self.censor_zero else observation
            result = float(gaussian_crps(array(self.parameters[0]),
                                        array(self.parameters[1]), array(y),
                                        self.censor_zero))
            return result + max(0.0, -observation) if self.censor_zero else result
        return numeric_score(self, observation)

    def atom_mass(self, value: float) -> float:
        return float(self._law().cdf(0)) if self.censor_zero and value == 0 else 0.0

    def atom_locations(self) -> tuple[float, ...]:
        return (0.0,) if self.censor_zero else ()

    def log_density(self, value: float) -> float:
        if self.censor_zero and value <= 0:
            return -math.inf
        return float(self._law().logpdf(value))

    def to_spec(self) -> dict[str, Json]:
        return {"tag": self.tag, "parameters": list(self.parameters),
                "censor_zero": self.censor_zero}
