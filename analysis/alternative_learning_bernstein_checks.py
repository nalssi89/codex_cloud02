"""Independent numerical equivalence and near-degenerate Bernstein checks."""

from __future__ import annotations

import json
from decimal import Decimal, localcontext
from math import comb
from time import perf_counter

import numpy as np

from analysis.alternative_distributions import bernstein, mixture
from analysis.alternative_learning_bernstein import learning_bernstein
from analysis.calibration import FloatArray


def decimal_cdf(coefficients: FloatArray, value: float) -> float:
    """80-digit Bernstein inversion, independent of the scalar Horner kernel."""
    with localcontext() as context:
        context.prec = 80
        c = tuple(Decimal.from_float(float(item)) for item in coefficients.flat)
        y = Decimal.from_float(value)
        if y < c[0]:
            return 0.
        if y >= c[-1]:
            return 1.
        lower, upper = Decimal(0), Decimal(1)
        for _ in range(100):
            u = (lower + upper) / 2
            q = sum(
                c[k] * comb(5, k) * u**k * (1 - u) ** (5 - k)
                for k in range(6)
            )
            if q < y:
                lower = u
            else:
                upper = u
        return float((lower + upper) / 2)


def main() -> None:
    largest = 0.
    for coefficients, p0 in (
        (np.array([-2., -1., .25, 3., 5., 8.]), 0.),
        (np.array([.01, .2, 1., 8., 20., 50.]), .3),
        (np.full(6, 5.), .4),
    ):
        canonical = bernstein(coefficients, p0)
        accelerated = learning_bernstein(coefficients, p0)
        grid = np.linspace(-3, 55, 129)
        assert accelerated.cdf(grid).dtype == np.dtype(np.float64)
        assert accelerated.cdf_left(grid).dtype == np.dtype(np.float64)
        assert accelerated.quantile(np.linspace(0, 1, 129)).dtype == np.dtype(np.float64)
        assert accelerated.cdf(grid).shape == grid.shape
        difference = canonical.cdf(grid) - accelerated.cdf(grid)
        error = max(abs(difference.item(i)) for i in range(difference.size))
        largest = max(largest, error)
        assert error <= 1e-10
        np.testing.assert_allclose(canonical.cdf_left(grid), accelerated.cdf_left(grid), atol=1e-10)
        np.testing.assert_array_equal(
            canonical.quantile(np.linspace(0, 1, 129)),
            accelerated.quantile(np.linspace(0, 1, 129)),
        )
        assert canonical.mean() == accelerated.mean()
        assert canonical.to_spec() == accelerated.to_spec()
        assert canonical.atom_mass(0.) == accelerated.atom_mass(0.)
        assert abs(canonical.crps(3.) - accelerated.crps(3.)) <= 1e-7
        assert np.isclose(canonical.log_density(3.), accelerated.log_density(3.), atol=1e-10)
    coefficients = 10000 + np.arange(6, dtype=np.float64) * 1e-6
    accelerated = learning_bernstein(coefficients)
    grid = np.linspace(coefficients.item(0), coefficients.item(5), 33)
    oracle = np.array(
        [decimal_cdf(coefficients, float(value)) for value in grid.flat], dtype=np.float64,
    )
    difference = accelerated.cdf(grid) - oracle
    decimal_error = max(abs(difference.item(i)) for i in range(difference.size))
    assert decimal_error <= 1e-10
    assert np.all(np.diff(accelerated.cdf(grid)) >= 0)
    parts = (np.arange(6, dtype=np.float64), np.arange(6, dtype=np.float64) + .5)
    original = mixture(tuple(bernstein(c) for c in parts), np.array([.5, .5]))
    faster = mixture(tuple(learning_bernstein(c) for c in parts), np.array([.5, .5]))
    start = perf_counter()
    original_q = original.quantile(np.array([.5]))
    original_seconds = perf_counter() - start
    start = perf_counter()
    faster_q = faster.quantile(np.array([.5]))
    faster_seconds = perf_counter() - start
    np.testing.assert_allclose(original_q, faster_q, atol=1e-10)
    print(json.dumps({
        "canonical_cdf_error": largest, "decimal_near_degenerate_error": decimal_error,
        "original_single_quantile_seconds": original_seconds,
        "accelerated_single_quantile_seconds": faster_seconds,
    }, indent=2))


if __name__ == "__main__":
    main()
