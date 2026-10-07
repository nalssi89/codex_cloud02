"""Complete mixture laws and atom-aware generalized inversion."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.special import logsumexp, ndtr

from analysis.alternative_contracts import PredictiveDistribution
from analysis.alternative_distribution_base import (
    ScientificLaw,
    array,
    floats,
    numeric_score,
    probabilities,
)
from analysis.alternative_distribution_integrals import (
    atom_locations,
    law_error,
    survival,
)
from analysis.calibration import FloatArray
from analysis.data_io import Json


def invert(law: PredictiveDistribution, probability: FloatArray,
           lower: float, upper: float) -> FloatArray:
    p = probabilities(probability)
    result = np.empty_like(p)
    atomic = tuple(sorted(atom_locations(law)))
    for index in np.ndindex(p.shape):
        target = float(p[index])
        if target == 0 or target == 1:
            result[index] = lower if target == 0 else upper
            continue
        found = False
        for atom in atomic:
            if float(law.cdf_left(array(atom))) < target <= float(law.cdf(array(atom))):
                result[index], found = atom, True
                break
        if found:
            continue
        lo, hi = lower, upper
        if not math.isfinite(lo):
            lo = min(-1.0, hi-1) if math.isfinite(hi) else -1.0
            while float(law.cdf(array(lo))) >= target:
                lo = lo*2 if lo < 0 else -1.0
        if not math.isfinite(hi):
            hi = max(1.0, lo+1)
            while float(law.cdf(array(hi))) < target:
                hi = hi*2 if hi > 0 else 1.0
        for _ in range(120):
            middle = lo + (hi-lo)/2
            if middle == lo or middle == hi:
                break
            if float(law.cdf(array(middle))) >= target:
                hi = middle
            else:
                lo = middle
        result[index] = hi
    return array(result)


def absolute_normal(location: float, scale: float) -> float:
    z = location/scale
    return (2*scale*math.exp(-z*z/2)/math.sqrt(2*math.pi)
            + location*(2*float(ndtr(z))-1))


@dataclass(frozen=True, slots=True, kw_only=True)
class Mixture:
    parts: tuple[PredictiveDistribution, ...]
    weights: FloatArray

    def cdf(self, value: FloatArray) -> FloatArray:
        return array(sum(w*part.cdf(value) for part, w in zip(self.parts, floats(self.weights))))

    def cdf_left(self, value: FloatArray) -> FloatArray:
        return array(sum(w*part.cdf_left(value)
                         for part, w in zip(self.parts, floats(self.weights))))

    def sf(self, value: FloatArray) -> FloatArray:
        return array(sum(w*survival(part, value)
                         for part, w in zip(self.parts, floats(self.weights))))

    def quantile(self, probability: FloatArray) -> FloatArray:
        p = probabilities(probability)
        # The component quantiles at p bracket the mixture quantile.
        result = np.empty_like(p)
        for index in np.ndindex(p.shape):
            q = [float(part.quantile(array(p[index]))) for part in self.parts]
            result[index] = float(invert(self, array(p[index]), min(q), max(q)))
        return array(result)

    def mean(self) -> float:
        return math.fsum(w*part.mean() for part, w in zip(self.parts, floats(self.weights)))

    def crps(self, observation: float) -> float:
        if all(isinstance(part, ScientificLaw) and part.tag == "normal"
               and not part.censor_zero for part in self.parts):
            params = [part.parameters for part in self.parts if isinstance(part, ScientificLaw)]
            weights = floats(self.weights)
            first = math.fsum(w*absolute_normal(p[0]-observation, p[1])
                              for w, p in zip(weights, params))
            cross = math.fsum(wi*wj*absolute_normal(
                pi[0]-pj[0], math.hypot(pi[1], pj[1]))
                for wi, pi in zip(weights, params) for wj, pj in zip(weights, params))
            return first-.5*cross
        return numeric_score(self, observation)

    def atom_mass(self, value: float) -> float:
        return math.fsum(w*part.atom_mass(value)
                         for part, w in zip(self.parts, floats(self.weights)))

    def crps_error_bound(self, observation: float) -> float:
        return math.fsum(w*law_error(part, observation)
                         for part, w in zip(self.parts, floats(self.weights)))

    def atom_locations(self) -> tuple[float, ...]:
        return tuple(sorted({x for part in self.parts for x in atom_locations(part)}))

    def log_density(self, value: float) -> float:
        return float(logsumexp([math.log(w)+part.log_density(value)
                                for part, w in zip(self.parts, floats(self.weights))]))

    def to_spec(self) -> dict[str, Json]:
        return {"tag": "mixture", "parts": [part.to_spec() for part in self.parts],
                "weights": list(floats(self.weights))}
