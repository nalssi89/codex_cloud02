"""Affine, censor-before-power and hurdle transformations of complete laws."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from analysis.alternative_contracts import PredictiveDistribution
from analysis.alternative_distribution_base import array, numeric_score, probabilities
from analysis.alternative_distribution_integrals import (
    atom_locations,
    law_error,
    survival,
    survival_mean,
)
from analysis.calibration import FloatArray
from analysis.data_io import Json


@dataclass(frozen=True, slots=True, kw_only=True)
class Affine:
    base: PredictiveDistribution
    offset: float
    scale: float

    def cdf(self, value: FloatArray) -> FloatArray:
        z = array((value - self.offset) / self.scale)
        return self.base.cdf(z) if self.scale > 0 else array(1 - self.base.cdf_left(z))

    def cdf_left(self, value: FloatArray) -> FloatArray:
        z = array((value - self.offset) / self.scale)
        return self.base.cdf_left(z) if self.scale > 0 else array(1 - self.base.cdf(z))

    def sf(self, value: FloatArray) -> FloatArray:
        z = array((value - self.offset) / self.scale)
        return survival(self.base, z) if self.scale > 0 else self.base.cdf_left(z)

    def quantile(self, probability: FloatArray) -> FloatArray:
        p = probabilities(probability)
        if self.scale > 0:
            return array(self.offset + self.scale * self.base.quantile(p))
        # Reflection uses the strict upper inverse at atoms (not Q(1-p)).
        from analysis.alternative_distribution_mixture import invert

        endpoints = self.offset + self.scale * self.base.quantile(array([1, 0]))
        return invert(self, p, float(endpoints.take(0)), float(endpoints.take(1)))

    def mean(self) -> float:
        return self.offset + self.scale * self.base.mean()

    def crps(self, observation: float) -> float:
        return abs(self.scale) * self.base.crps((observation-self.offset)/self.scale)

    def crps_error_bound(self, observation: float) -> float:
        return abs(self.scale)*law_error(self.base, (observation-self.offset)/self.scale)

    def atom_mass(self, value: float) -> float:
        return self.base.atom_mass((value-self.offset)/self.scale)

    def atom_locations(self) -> tuple[float, ...]:
        return tuple(self.offset+self.scale*x for x in atom_locations(self.base))

    def log_density(self, value: float) -> float:
        return self.base.log_density((value-self.offset)/self.scale)-math.log(abs(self.scale))

    def to_spec(self) -> dict[str, Json]:
        return {"tag": "affine", "base": self.base.to_spec(),
                "offset": self.offset, "scale": self.scale}


@dataclass(frozen=True, slots=True, kw_only=True)
class PowerCensored:
    base: PredictiveDistribution
    power: float
    unit_scale: float

    def _inverse(self, value: FloatArray) -> FloatArray:
        return array(np.maximum(value/self.unit_scale, 0)**self.power)

    def cdf(self, value: FloatArray) -> FloatArray:
        x = array(value)
        return array(np.where(x < 0, 0, self.base.cdf(self._inverse(x))))

    def cdf_left(self, value: FloatArray) -> FloatArray:
        x = array(value)
        return array(np.where(x <= 0, 0, self.base.cdf_left(self._inverse(x))))

    def sf(self, value: FloatArray) -> FloatArray:
        x = array(value)
        return array(np.where(x < 0, 1, survival(self.base, self._inverse(x))))

    def quantile(self, probability: FloatArray) -> FloatArray:
        return array(self.unit_scale * np.maximum(0, self.base.quantile(
            probabilities(probability)))**(1/self.power))

    def mean(self) -> float:
        return survival_mean(self)

    def crps(self, observation: float) -> float:
        return numeric_score(self, observation)

    def atom_mass(self, value: float) -> float:
        if value < 0:
            return 0.0
        if value == 0:
            return float(self.base.cdf(array(0)))
        return self.base.atom_mass(math.pow(value/self.unit_scale, self.power))

    def atom_locations(self) -> tuple[float, ...]:
        return tuple(sorted({0.0, *(self.unit_scale*max(0, x)**(1/self.power)
                                     for x in atom_locations(self.base))}))

    def log_density(self, value: float) -> float:
        if value <= 0:
            return -math.inf
        z = math.pow(value/self.unit_scale, self.power)
        return (self.base.log_density(z) + math.log(self.power/self.unit_scale)
                + (self.power-1)*math.log(value/self.unit_scale))

    def to_spec(self) -> dict[str, Json]:
        return {"tag": "power_censored", "base": self.base.to_spec(),
                "power": self.power, "unit_scale": self.unit_scale}


@dataclass(frozen=True, slots=True, kw_only=True)
class Hurdle:
    p_zero: float
    positive: PredictiveDistribution

    def cdf(self, value: FloatArray) -> FloatArray:
        x = array(value)
        return array(np.where(x < 0, 0, self.p_zero+(1-self.p_zero)*self.positive.cdf(x)))

    def cdf_left(self, value: FloatArray) -> FloatArray:
        x = array(value)
        return array(np.where(x <= 0, 0,
                             self.p_zero+(1-self.p_zero)*self.positive.cdf_left(x)))

    def sf(self, value: FloatArray) -> FloatArray:
        x = array(value)
        return array(np.where(x < 0, 1, (1-self.p_zero)*survival(self.positive, x)))

    def quantile(self, probability: FloatArray) -> FloatArray:
        p = probabilities(probability)
        if self.p_zero == 1:
            return array(np.zeros_like(p))
        q = self.positive.quantile(array(np.maximum(0, (p-self.p_zero)/(1-self.p_zero))))
        return array(np.where(p <= self.p_zero, 0, q)) if self.p_zero else q

    def mean(self) -> float:
        return (1-self.p_zero)*self.positive.mean()

    def crps(self, observation: float) -> float:
        return numeric_score(self, observation)

    def crps_error_bound(self, observation: float) -> float:
        return (1-self.p_zero)*law_error(self.positive, observation)

    def atom_mass(self, value: float) -> float:
        return self.p_zero if value == 0 else (1-self.p_zero)*self.positive.atom_mass(value)

    def atom_locations(self) -> tuple[float, ...]:
        return (0.0, *atom_locations(self.positive))

    def log_density(self, value: float) -> float:
        if value <= 0 or self.p_zero == 1:
            return -math.inf
        return math.log1p(-self.p_zero)+self.positive.log_density(value)

    def to_spec(self) -> dict[str, Json]:
        return {"tag": "hurdle", "p_zero": self.p_zero,
                "positive": self.positive.to_spec()}
