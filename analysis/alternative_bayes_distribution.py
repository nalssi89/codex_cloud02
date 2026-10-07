"""Exact scalar Student or finite Normal-mixture Bayesian predictive laws."""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from itertools import pairwise

import numpy as np
from scipy.integrate import quad
from scipy.special import expit, logsumexp, ndtr, ndtri
from scipy.stats import t

from analysis.alternative_bayes_distribution_transforms import (
    LOG_SINH_ONE,
    TRANSFORMS,
    forward,
    inverse,
)
from analysis.alternative_contracts import AlternativeError
from analysis.calibration import FloatArray
from analysis.data_io import Json

__all__ = ["BayesianScalar", "distribution_from_spec", "forward", "inverse"]


def _array(value: object) -> FloatArray:
    return np.asarray(value, dtype=np.float64)


def _integral(function: Callable[[float], float], points: list[float], scale: float) -> float:
    """Refine once and fail explicitly on QUADPACK warnings or error bounds."""
    for refinement in (1.0, .1):
        pieces = [quad(function, a, b, epsabs=1e-8 * scale * refinement / len(points),
                       epsrel=1e-7 * refinement, limit=200, full_output=1)
                  for a, b in pairwise(points) if a < b]
        answer = math.fsum(float(piece[0]) for piece in pieces)
        error = math.fsum(float(piece[1]) for piece in pieces)
        if (all(len(piece) == 3 for piece in pieces) and math.isfinite(answer)
                and error <= max(1e-8 * scale, 1e-7 * abs(answer))):
            return answer
    raise AlternativeError("NUMERICAL_DISTRIBUTION_FAILED",
                           f"Bayesian quadrature: value={answer}, error={error}")


@dataclass(frozen=True, slots=True, kw_only=True)
class BayesianScalar:
    """Student ``scales`` are sqrt(scale matrix), not marginal standard deviations."""

    locations: FloatArray
    scales: FloatArray
    weights: FloatArray
    df: float | None
    transform: str
    chain_shape: tuple[int, int] | None = None
    training_sd: float | None = None

    def __post_init__(self) -> None:
        arrays = [np.array(a, dtype=np.float64, copy=True)
                  for a in (self.locations, self.scales, self.weights)]
        loc, scales, weights = arrays
        if (any(a.ndim != 1 or a.size == 0 or not np.all(np.isfinite(a)) for a in arrays)
                or not loc.shape == scales.shape == weights.shape
                or np.any(scales <= 0) or np.any(weights < 0) or weights.sum() <= 0
                or not np.isfinite(weights.sum())
                or self.transform not in TRANSFORMS):
            raise ValueError("invalid scalar Bayesian distribution parameters")
        if self.df is not None:
            minimum = 2 if self.transform in {"sqrt", "yj"} else 1
            if loc.size != 1 or not math.isfinite(self.df) or self.df <= minimum:
                raise AlternativeError("NUMERICAL_DISTRIBUTION_FAILED",
                                       f"single Student needs df>{minimum} for finite mean")
        if self.training_sd is not None and (not math.isfinite(self.training_sd) or self.training_sd < 0):
            raise ValueError("training SD must be finite and nonnegative")
        if self.chain_shape is not None and (
                self.df is not None or len(self.chain_shape) != 2
                or any(isinstance(n, bool) or n <= 0 for n in self.chain_shape)
                or math.prod(self.chain_shape) != loc.size or self.training_sd is None):
            raise ValueError("posterior chain shape and training SD must match the Normal draws")
        weights /= weights.sum()
        for name, a in zip(("locations", "scales", "weights"), arrays, strict=True):
            a.setflags(write=False)
            object.__setattr__(self, name, a)

    def _latent(self, value: FloatArray, survival: bool = False) -> FloatArray:
        z = (value[..., None] - self.locations) / self.scales
        if self.df is None:
            probability = ndtr(-z if survival else z)
        else:
            probability = t.sf(z, self.df) if survival else t.cdf(z, self.df)
        return _array(np.sum(probability * self.weights, axis=-1))

    def cdf(self, value: FloatArray) -> FloatArray:
        x = _array(value)
        z = forward(x if self.transform == "temperature" else np.maximum(x, 0),
                    self.transform)
        result = self._latent(_array(z))
        return _array(result if self.transform == "temperature" else np.where(x < 0, 0, result))

    def cdf_left(self, value: FloatArray) -> FloatArray:
        x = _array(value)
        return _array(np.where(x <= 0, 0, self.cdf(x)) if self.transform != "temperature"
                      else self.cdf(x))

    def sf(self, value: FloatArray) -> FloatArray:
        x = _array(value)
        z = forward(x if self.transform == "temperature" else np.maximum(x, 0),
                    self.transform)
        result = self._latent(_array(z), True)
        return _array(result if self.transform == "temperature" else np.where(x < 0, 1, result))

    def quantile(self, probability: FloatArray) -> FloatArray:
        p = _array(probability)
        if np.any(~np.isfinite(p)) or np.any((p < 0) | (p > 1)):
            raise ValueError("quantile probabilities must lie in [0,1]")
        interior = np.where(np.equal(p, 0) | np.equal(p, 1), .5, p)
        q = _array(ndtri(interior) if self.df is None else t.ppf(interior, self.df))
        candidates = _array(self.locations + q[..., None] * self.scales)
        lo, hi = _array(np.min(candidates, axis=-1)), _array(np.max(candidates, axis=-1))
        for _ in range(64):
            mid = lo / 2 + hi / 2
            below = np.where(p <= .5, self._latent(_array(mid)) < p,
                             self._latent(_array(mid), True) > 1 - p)
            lo, hi = np.where(below, mid, lo), np.where(below, hi, mid)
        latent = np.where(np.equal(p, 0), -math.inf,
                          np.where(np.equal(p, 1), math.inf, lo / 2 + hi / 2))
        if self.transform != "temperature":
            latent = np.where((p < 1) & (p <= self.atom_mass(0)), -math.inf, latent)
        return inverse(_array(latent), self.transform)

    def mean(self) -> float:
        if self.transform == "temperature":
            return float(10 + 10 * np.sum(self.weights * self.locations))
        if self.df is None and self.transform in {"sqrt", "yj"}:
            a = self.locations / self.scales
            phi = np.exp(-a**2 / 2) / math.sqrt(2 * math.pi)
            first = self.locations * ndtr(a) + self.scales * phi
            second = (self.locations**2 + self.scales**2) * ndtr(a)
            second += self.locations * self.scales * phi
            moments = second if self.transform == "sqrt" else first + second / 4
            return float(100 * np.sum(self.weights * moments))
        def integrand(z: float) -> float:
            derivative = (2 * z if self.transform == "sqrt" else 1 + z / 2
                          if self.transform == "yj" else math.sqrt(float(expit(2 * (z + LOG_SINH_ONE)))))
            return 100 * derivative * float(self._latent(_array(z), True))
        points = [0.0, math.inf]
        if self.df is None:
            centers = _array(np.quantile(self.locations, [.1, .5, .9]))
            points += [float(centers.take(i)) for i in range(centers.size) if centers.take(i) > 0]
        else:
            points += [float(self.locations.take(0))] if self.locations.take(0) > 0 else []
        return _integral(integrand, sorted(set(points)), 100)

    def crps(self, observation: float) -> float:
        if not math.isfinite(observation):
            raise ValueError("CRPS observation must be finite")
        def integrand(x: float) -> float:
            probability = self.cdf(_array(x)) if x < observation else self.sf(_array(x))
            return float(probability)**2
        quantiles = self.quantile(_array([0, .001, .01, .1, .5, .9, .99, .999, 1]))
        points = sorted({float(quantiles.take(i)) for i in range(quantiles.size)} | {observation, 0.0})
        score = _integral(integrand, points, 10 if self.transform == "temperature" else 100)
        if self.chain_shape is not None:
            from analysis.alternative_bayes_precision import score_crps_precision

            mcse, error, passed = score_crps_precision(self, observation)
            if not passed:
                raise AlternativeError("POSTERIOR_DIAGNOSTICS_FAILED",
                                       f"actual-observation CRPS MCSE={mcse}, quadrature error={error}")
        return score

    def atom_mass(self, value: float) -> float:
        return float(self._latent(_array(0))) if self.transform != "temperature" and value == 0 else 0.0

    def log_density(self, value: float) -> float:
        if not math.isfinite(value) or (self.transform != "temperature" and value <= 0):
            return -math.inf
        latent = float(forward(_array(value), self.transform))
        z = (latent - self.locations) / self.scales
        logs = (-z**2 / 2 - math.log(2 * math.pi) / 2 if self.df is None
                else t.logpdf(z, self.df)) - np.log(self.scales)
        jacobian = (0.1 if self.transform == "temperature" else 1 / (200 * latent)
                    if self.transform == "sqrt" else 1 / (100 * math.sqrt(1 + value / 100))
                    if self.transform == "yj" else 1 / (100 * math.tanh(1 + value / 100)))
        positive = self.weights > 0
        return float(logsumexp(logs[positive] + np.log(self.weights[positive]))) + math.log(jacobian)

    def to_spec(self) -> dict[str, Json]:
        return {"kind": "bayesian_scalar",
                "locations": [float(self.locations.take(i)) for i in range(self.locations.size)],
                "scales": [float(self.scales.take(i)) for i in range(self.scales.size)],
                "weights": [float(self.weights.take(i)) for i in range(self.weights.size)],
                "df": self.df, "transform": self.transform,
                "chain_shape": list(self.chain_shape) if self.chain_shape is not None else None,
                "training_sd": self.training_sd}


def distribution_from_spec(spec: Mapping[str, Json]) -> BayesianScalar:
    """Restore the posterior law, retaining its physical transform and all draws."""
    df, transform = spec.get("df"), spec.get("transform")
    if (spec.get("kind") != "bayesian_scalar" or not isinstance(transform, str)
            or (df is not None and (isinstance(df, bool) or not isinstance(df, (float, int))))):
        raise ValueError("invalid Bayesian scalar specification")
    shape, training_sd = spec.get("chain_shape"), spec.get("training_sd")
    chain_shape: tuple[int, int] | None = None
    if shape is not None:
        if (not isinstance(shape, list) or len(shape) != 2
                or any(isinstance(n, bool) or not isinstance(n, int) for n in shape)):
            raise ValueError("invalid posterior chain shape")
        first, second = shape
        if not isinstance(first, int) or not isinstance(second, int):
            raise ValueError("posterior chain dimensions must be integers")
        chain_shape = (first, second)
    if training_sd is not None and (isinstance(training_sd, bool) or not isinstance(training_sd, (int, float))):
        raise ValueError("invalid training SD")
    return BayesianScalar(locations=_array(spec["locations"]), scales=_array(spec["scales"]),
                          weights=_array(spec["weights"]), df=None if df is None else float(df),
                          transform=transform, chain_shape=chain_shape,
                          training_sd=None if training_sd is None else float(training_sd))
