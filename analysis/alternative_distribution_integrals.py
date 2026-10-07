"""Support-aware adaptive quadrature with explicit survival-tail error."""

from __future__ import annotations

import math
from itertools import pairwise
from typing import Protocol, runtime_checkable

import numpy as np
from numpy.typing import ArrayLike
from scipy.integrate import quad

from analysis.alternative_contracts import NumericIntegral, PredictiveDistribution
from analysis.calibration import FloatArray


def array(value: ArrayLike) -> FloatArray:
    return np.asarray(value, dtype=np.float64)


@runtime_checkable
class SurvivalLaw(Protocol):
    def sf(self, value: FloatArray) -> FloatArray: ...


@runtime_checkable
class AtomicLaw(Protocol):
    def atom_locations(self) -> tuple[float, ...]: ...


@runtime_checkable
class CertifiedLaw(Protocol):
    def crps_error_bound(self, observation: float) -> float: ...


def law_error(law: PredictiveDistribution, observation: float) -> float:
    return law.crps_error_bound(observation) if isinstance(law, CertifiedLaw) else 0.0


def atom_locations(law: PredictiveDistribution) -> tuple[float, ...]:
    return law.atom_locations() if isinstance(law, AtomicLaw) else ()


def survival(law: PredictiveDistribution, value: FloatArray) -> FloatArray:
    if isinstance(law, SurvivalLaw):
        return law.sf(value)
    return array(1.0 - law.cdf(value))


def knots(law: PredictiveDistribution, extra: tuple[float, ...]) -> list[float]:
    points = law.quantile(array([0, .001, .01, .1, .5, .9, .99, .999, 1]))
    atoms = atom_locations(law)
    return sorted({float(points.take(i)) for i in range(points.size)
                   if not math.isnan(float(points.take(i)))}
                  | set(extra) | set(atoms))


def cdf_crps(distribution: PredictiveDistribution, observation: float,
             scale: float, tolerance: float = 1e-7) -> NumericIntegral:
    """Integrate the mixed CDF *after* mixing, never component CRPS averages."""
    if not math.isfinite(observation) or not math.isfinite(scale) or scale <= 0:
        raise ValueError("finite observation and positive finite scale required")
    if not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("positive finite tolerance required")
    points = knots(distribution, (observation, 0.0))
    # Finite support is sufficient; adding the observation includes exterior loss.
    def integrand(z: float) -> float:
        if z < observation:
            return float(distribution.cdf(array(z))) ** 2
        return float(survival(distribution, array(z))) ** 2

    answer, error = 0.0, math.inf
    for refinement in (1.0, .1):
        pieces = [quad(integrand, a, b, epsabs=1e-8*scale*refinement/len(points),
                       epsrel=tolerance*refinement, limit=200, full_output=1)
                  for a, b in pairwise(points)]
        answer = math.fsum(float(piece[0]) for piece in pieces)
        error = math.fsum(float(piece[1]) for piece in pieces) + law_error(distribution, observation)
        success = all(len(piece) == 3 for piece in pieces)
        if success and error <= max(1e-8*scale, tolerance*abs(answer)):
            return NumericIntegral(value=answer, error=error, converged=True)
    return NumericIntegral(value=answer, error=error, converged=False)


def survival_mean(law: PredictiveDistribution) -> float:
    """Positive part minus negative part, split near the law's actual location."""
    points = knots(law, (0.0,))
    def function(z: float) -> float:
        return float(survival(law, array(z))) if z >= 0 else -float(law.cdf(array(z)))
    pieces = [quad(function, a, b, epsabs=1e-9, epsrel=1e-9,
                   limit=200, full_output=1) for a, b in pairwise(points)]
    result = math.fsum(float(piece[0]) for piece in pieces)
    error = math.fsum(float(piece[1]) for piece in pieces)
    if not math.isfinite(result) or any(len(piece) != 3 for piece in pieces):
        raise ArithmeticError(f"mean integration failed: value={result}, error={error}")
    if error > max(1e-8, 1e-7*abs(result)):
        raise ArithmeticError(f"mean error bound exceeded: {error}")
    return result
