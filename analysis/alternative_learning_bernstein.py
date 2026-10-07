"""Exact Bernstein law with a scalar bisection kernel for neural mixtures.

All support, PPF, mean, density, atom and JSON semantics remain those of the
canonical Bernstein constructor. This removes tiny-array/SciPy-comb overhead,
not inverse iterations, probability accuracy or the bounded-tail model.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb
from typing import override

import numpy as np

from analysis.alternative_contracts import PredictiveDistribution
from analysis.alternative_distribution_bernstein import Bernstein
from analysis.alternative_distributions import bernstein
from analysis.calibration import FloatArray


@dataclass(frozen=True, slots=True, kw_only=True)
class LearningBernstein(Bernstein):
    powers: tuple[float, ...]

    @override
    def _positive_cdf(self, value: FloatArray) -> FloatArray:
        first, last = self.coefficients.item(0), self.coefficients.item(-1)
        result: list[float] = []
        for observed in value.flat:
            x = float(observed)
            if x < first:
                result.append(0.)
                continue
            if x >= last:
                result.append(1.)
                continue
            lower, upper = 0., 1.
            for _ in range(64):
                midpoint = (lower + upper) / 2
                q = self.powers[-1]
                for coefficient in reversed(self.powers[:-1]):
                    q = q * midpoint + coefficient
                if q < x - first:
                    lower = midpoint
                else:
                    upper = midpoint
            result.append((lower + upper) / 2)
        return np.asarray(result, dtype=np.float64).reshape(value.shape)


def learning_bernstein(
    coefficients: FloatArray, p_zero: float = 0.,
) -> PredictiveDistribution:
    base = bernstein(coefficients, p_zero)
    if not isinstance(base, Bernstein):
        return base  # Canonical all-atom endpoint, not a model substitution.
    degree = coefficients.size - 1
    powers = tuple(
        sum(
            (coefficients.item(k) - coefficients.item(0))
            * comb(degree, k) * comb(degree - k, j - k)
            * (-1) ** (j - k) for k in range(j + 1)
        )
        for j in range(degree + 1)
    )
    return LearningBernstein(
        coefficients=base.coefficients, p_zero=base.p_zero, powers=powers,
    )
