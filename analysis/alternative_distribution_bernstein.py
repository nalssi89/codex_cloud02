"""Bounded monotone Bernstein-quantile law, with an optional rain atom."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.special import comb

from analysis.alternative_distribution_base import (
    array,
    floats,
    numeric_score,
    probabilities,
)
from analysis.calibration import FloatArray
from analysis.data_io import Json


def polynomial(coefficients: FloatArray, probability: FloatArray) -> FloatArray:
    n = coefficients.size-1
    u = array(probability)
    if np.all(np.equal(coefficients, coefficients.take(0))):
        return array(np.full_like(u, float(coefficients.take(0))))
    return array(sum(float(c)*float(comb(n, k))*u**k*(1-u)**(n-k)
                     for k, c in enumerate(floats(coefficients))))


@dataclass(frozen=True, slots=True, kw_only=True)
class Bernstein:
    coefficients: FloatArray
    p_zero: float = 0.0

    def _positive_cdf(self, value: FloatArray) -> FloatArray:
        x = array(value)
        lo, hi = np.zeros_like(x), np.ones_like(x)
        for _ in range(64):
            mid = (lo+hi)/2
            below = polynomial(self.coefficients, array(mid)) < x
            lo = np.where(below, mid, lo)
            hi = np.where(below, hi, mid)
        first, last = float(self.coefficients.take(0)), float(self.coefficients.take(-1))
        return array(np.where(x < first, 0, np.where(x >= last, 1, (lo+hi)/2)))

    def cdf(self, value: FloatArray) -> FloatArray:
        x = array(value)
        positive = self._positive_cdf(x)
        if self.p_zero == 0:
            return positive
        return array(np.where(x < 0, 0, self.p_zero+(1-self.p_zero)*positive))

    def cdf_left(self, value: FloatArray) -> FloatArray:
        x = array(value)
        result = self.cdf(x)
        first, last = float(self.coefficients.take(0)), float(self.coefficients.take(-1))
        if first == last:
            result = array(np.where(np.equal(x, first), self.p_zero, result))
        return array(np.where(np.equal(x, 0), 0, result)) if self.p_zero else result

    def sf(self, value: FloatArray) -> FloatArray:
        # Reflection of the polynomial avoids upper-tail CDF subtraction.
        x = array(value)
        upper = Bernstein(coefficients=array(-self.coefficients[::-1]))._positive_cdf(-x)
        first, last = float(self.coefficients.take(0)), float(self.coefficients.take(-1))
        if first == last:
            upper = array(x < first)
        if self.p_zero == 0:
            return upper
        return array(np.where(x < 0, 1, (1-self.p_zero)*upper))

    def quantile(self, probability: FloatArray) -> FloatArray:
        p = probabilities(probability)
        if self.p_zero == 1:
            return array(np.zeros_like(p))
        u = array(np.maximum(0, (p-self.p_zero)/(1-self.p_zero)))
        q = polynomial(self.coefficients, u)
        return array(np.where(p <= self.p_zero, 0, q)) if self.p_zero else q

    def mean(self) -> float:
        return (1-self.p_zero)*float(self.coefficients.mean())

    def crps(self, observation: float) -> float:
        return numeric_score(self, observation)

    def atom_mass(self, value: float) -> float:
        mass = self.p_zero if value == 0 else 0.0
        if float(self.coefficients.take(0)) == float(self.coefficients.take(-1)) == value:
            mass += 1-self.p_zero
        return mass

    def atom_locations(self) -> tuple[float, ...]:
        locations = [0.0] if self.p_zero else []
        if float(self.coefficients.take(0)) == float(self.coefficients.take(-1)):
            locations.append(float(self.coefficients.take(0)))
        return tuple(locations)

    def log_density(self, value: float) -> float:
        c = self.coefficients
        first, last = float(c.take(0)), float(c.take(-1))
        if value < first or value > last or first == last or self.p_zero == 1:
            return -math.inf
        u = self._positive_cdf(array(value))
        derivative = float(polynomial(array((c.size-1)*np.diff(c)), u))
        return math.log1p(-self.p_zero)-math.log(derivative) if derivative > 0 else math.inf

    def to_spec(self) -> dict[str, Json]:
        return {"tag": "bernstein", "coefficients": list(floats(self.coefficients)),
                "p_zero": self.p_zero}
