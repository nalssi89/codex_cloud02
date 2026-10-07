"""Exact compound-Poisson Gamma Tweedie law with certified series tails."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import exp, expm1, isfinite, log, pow

import numpy as np
from scipy.optimize import brentq
from scipy.special import gammainc, gammaincc, gammaln, logsumexp
from scipy.stats import poisson

from analysis.calibration import FloatArray
from analysis.data_io import Json


@dataclass(frozen=True, slots=True, kw_only=True)
class Tweedie:
    """Original-unit Tweedie, with a zero atom and no Gamma substitution.

    The CDF truncation bounds are also valid for survival probabilities and
    integrated tails. Density evaluation retains their range plus its own
    mode-centred range; monotone adjacent ratios bound both omitted tails.
    """

    mu: float
    phi: float
    power: float
    _lam: float = field(init=False, repr=False)
    _alpha: float = field(init=False, repr=False)
    _theta: float = field(init=False, repr=False)
    _low: int = field(init=False, repr=False)
    _high: int = field(init=False, repr=False)
    _indices: FloatArray = field(init=False, repr=False, compare=False)
    _weights: FloatArray = field(init=False, repr=False, compare=False)
    cdf_mass_bound: float = field(init=False)
    cdf_first_moment_bound: float = field(init=False)

    def __post_init__(self) -> None:
        if not all(isfinite(v) for v in (self.mu, self.phi, self.power)):
            raise ValueError("Tweedie parameters must be finite")
        if self.mu < 0 or self.phi <= 0 or not 1 < self.power < 2:
            raise ValueError("Tweedie requires mu>=0, phi>0, 1<power<2")
        alpha = (2 - self.power) / (self.power - 1)
        lam = pow(self.mu, 2 - self.power) / (self.phi * (2 - self.power))
        theta = self.phi * (self.power - 1) * pow(self.mu, self.power - 1)
        if self.mu > 0 and (not isfinite(lam) or lam <= 0
                            or not isfinite(theta) or theta <= 0):
            raise ValueError("Compound parameters outside finite floating-point range")
        low, high = 1, 0
        mass, moment = 0.0, 0.0
        if lam:
            low = max(1, int(poisson.ppf(1e-14, lam)))
            high = max(low, int(poisson.isf(1e-14, lam)))
            while True:
                mass = float(poisson.cdf(low - 1, lam) - exp(-lam)
                             + poisson.sf(high, lam))
                moment = self.mu * float(poisson.cdf(low - 2, lam)
                                         + poisson.sf(high - 1, lam))
                if mass <= 1e-12 and moment <= 1e-12:
                    break
                low, high = max(1, low - 32), high + 32
        indices = np.arange(low, high + 1, dtype=np.float64)
        weights = np.exp(-lam + indices * log(lam) - gammaln(indices + 1)) if lam else indices.copy()
        indices.flags.writeable = weights.flags.writeable = False
        for key, value in (
            ("_lam", lam), ("_alpha", alpha), ("_theta", theta),
            ("_low", low), ("_high", high), ("_indices", indices),
            ("_weights", weights), ("cdf_mass_bound", max(0.0, mass)),
            ("cdf_first_moment_bound", moment),
        ):
            object.__setattr__(self, key, value)

    def atom_mass(self, value: float) -> float:
        return exp(-self._lam) if value == 0 else 0.0

    def mean(self) -> float:
        return self.mu

    def _probability(self, value: FloatArray, *, survival: bool) -> FloatArray:
        values = np.asarray(value, dtype=np.float64)
        result = np.empty_like(values)
        for index in range(values.size):
            x = float(values.take(index))
            if np.isnan(x):
                probability = float("nan")
            elif x < 0:
                probability = 1.0 if survival else 0.0
            elif x == float("inf") or not self._lam:
                probability = 0.0 if survival else 1.0
            elif x == 0:
                probability = -expm1(-self._lam) if survival else exp(-self._lam)
            else:
                shapes = self._indices * self._alpha
                terms = gammaincc(shapes, x / self._theta) if survival else gammainc(shapes, x / self._theta)
                probability = float(np.sum(self._weights*terms))
                if not survival:
                    probability += exp(-self._lam)
            result.flat[index] = np.clip(probability, 0.0, 1.0)
        return result

    def cdf(self, value: FloatArray) -> FloatArray:
        return self._probability(value, survival=False)

    def sf(self, value: FloatArray) -> FloatArray:
        return self._probability(value, survival=True)

    def cdf_left(self, value: FloatArray) -> FloatArray:
        values = np.asarray(value, dtype=np.float64)
        return np.where(np.equal(values, 0), 0.0, self.cdf(values))

    def quantile(self, probability: FloatArray) -> FloatArray:
        def residual(x: float, tail: float) -> float:
            return float(self.sf(np.asarray(x))) - tail

        probabilities = np.asarray(probability, dtype=np.float64)
        if np.any(~np.isfinite(probabilities) | (probabilities < 0) | (probabilities > 1)):
            raise ValueError("Quantile probabilities must be finite and in [0,1]")
        result = np.zeros_like(probabilities)
        for index in range(probabilities.size):
            p = float(probabilities.take(index))
            if not self.mu or p <= exp(-self._lam):
                continue
            if p == 1:
                result.flat[index] = float("inf")
                continue
            # Survival inversion avoids subtracting almost-one CDFs.
            upper = max(self.mu, self._theta)
            while float(self.sf(np.asarray(upper))) > 1 - p:
                upper *= 2
                if not isfinite(upper):
                    raise ArithmeticError("Tweedie quantile bracket overflow")
            result.flat[index] = brentq(
                residual, 0, upper, args=(1 - p,), xtol=5e-324, rtol=1e-12,
            )
        return result

    def _log_ratio(self, n: int, x: float) -> float:
        a = n * self._alpha
        return (log(self._lam) - log(n + 1)
                + self._alpha * (log(x) - log(self._theta))
                + float(gammaln(a) - gammaln(a + self._alpha)))

    def _log_terms(self, indices: FloatArray, x: float) -> FloatArray:
        shapes = indices * self._alpha
        return np.asarray(
            -self._lam + indices * log(self._lam) - gammaln(indices + 1)
            + (shapes - 1) * log(x) - x / self._theta
            - gammaln(shapes) - shapes * log(self._theta),
            dtype=np.float64,
        )

    def density_bounds(self, value: float) -> tuple[float, float, float]:
        """Return log density, log absolute remainder, relative remainder."""
        if np.isnan(value):
            return float("nan"), float("nan"), float("nan")
        if value <= 0 or not isfinite(value) or not self._lam:
            return -float("inf"), -float("inf"), 0.0
        # Find the first decreasing step: ratios decrease for all alpha>0.
        right = 1
        while self._log_ratio(right, value) > 0:
            right *= 2
        left = 1
        while left < right:
            mid = (left + right) // 2
            if self._log_ratio(mid, value) > 0:
                left = mid + 1
            else:
                right = mid
        low, high = min(self._low, left), max(self._high, left)
        total = float(logsumexp(self._log_terms(np.arange(low, high + 1, dtype=np.float64), value)))
        while True:
            right_ratio = self._log_ratio(high, value)
            right_bound = float(self._log_terms(np.asarray([high], dtype=np.float64), value).take(0))
            right_bound += right_ratio - log(-expm1(right_ratio)) if right_ratio < 0 else float("inf")
            left_bound = -float("inf")
            if low > 1:
                left_ratio = -self._log_ratio(low - 1, value)
                left_bound = float(self._log_terms(np.asarray([low], dtype=np.float64), value).take(0))
                left_bound += left_ratio - log(-expm1(left_ratio)) if left_ratio < 0 else float("inf")
            bound = float(logsumexp(np.asarray([left_bound, right_bound])))
            if bound <= log(1e-12) and bound - total <= log(1e-9):
                return total, bound, exp(bound - total)
            new_low, new_high = max(1, low - 32), high + 32
            extra = np.concatenate((
                np.arange(new_low, low, dtype=np.float64),
                np.arange(high + 1, new_high + 1, dtype=np.float64),
            ))
            total = float(logsumexp(np.asarray([total, float(logsumexp(self._log_terms(extra, value)))])))
            low, high = new_low, new_high

    def log_density(self, value: float) -> float:
        return self.density_bounds(value)[0]

    def crps(self, observation: float) -> float:
        from analysis.alternative_distribution_integrals import cdf_crps

        answer = cdf_crps(self, observation, max(1.0, self.mu))
        if not answer.converged:
            raise ArithmeticError(f"Tweedie CRPS error bound exceeded: {answer.error}")
        return answer.value

    def atom_locations(self) -> tuple[float, ...]:
        return (0.0,)

    def crps_error_bound(self, observation: float) -> float:
        return 2*(self.cdf_first_moment_bound+max(0.0, observation)*self.cdf_mass_bound)

    def to_spec(self) -> dict[str, Json]:
        return {"tag": "tweedie", "mu": self.mu, "phi": self.phi, "power": self.power}
