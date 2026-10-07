"""Run deterministic real fits and independent atom-aware BQN CRPS audits."""

from __future__ import annotations

from dataclasses import replace
from itertools import pairwise
from math import comb, exp

import numpy as np
import torch
from scipy.integrate import quad
from scipy.optimize import brentq
from torch import Tensor

from analysis.alternative_contracts import FitConfig, TrainingSet
from analysis.alternative_distributions import bernstein
from analysis.alternative_learning_checks import fixture
from analysis.alternative_learning_neural import bqn_loss, fit_neural
from analysis.alternative_learning_neural_math import softplus
from analysis.calibration import FloatArray


def cdf_oracle(coefficients: FloatArray, p0: float, y: float, rain: bool) -> float:
    """Invert the explicit polynomial independently of distribution CDF code."""
    lower = 0.0 if rain else coefficients.item(0)
    upper = coefficients.item(5)
    def polynomial(v: float) -> float:
        return sum(
            coefficients.item(k) * comb(5, k) * v**k * (1 - v)**(5 - k)
            for k in range(6)
        )
    def cdf(value: float) -> float:
        if value < lower:
            return 0.0
        if value >= upper:
            return 1.0
        if value <= coefficients.item(0):
            return p0
        return p0 + (1 - p0) * float(brentq(
            lambda v: polynomial(v) - value, 0.0, 1.0, xtol=1e-14,
        ))
    cuts = sorted({min(lower, y), max(upper, y), lower, upper, coefficients.item(0), y})
    return sum(float(quad(
        lambda value: cdf(value)**2 if value < y else (1 - cdf(value))**2,
        a, b, epsabs=1e-10, epsrel=1e-10,
    )[0]) for a, b in pairwise(cuts))


def check_quadrature() -> None:
    for rain in (False, True):
        raw = torch.tensor(
            [[0.4, -0.5, 0.0, 0.3, 0.8, 1.0, -1.2][:7 if rain else 6]],
            dtype=torch.float64, requires_grad=True,
        )
        values = np.asarray(raw.detach().numpy(), dtype=np.float64).reshape(-1)
        first = softplus(values.item(0)) + 1e-6 if rain else values.item(0)
        coefficients: FloatArray = np.concatenate((
            np.array([first]), first + np.cumsum(np.logaddexp(0, values[1:6]) + 1e-6),
        ))
        p0 = 1 / (1 + exp(-values.item(6))) if rain else 0.0
        for y in (0.0, 3.0, 15.0):
            observation = torch.tensor([y], dtype=torch.float64)
            oracle = cdf_oracle(coefficients, p0, y, rain)
            errors = [
                abs(float(bqn_loss(raw, observation, rain, nodes).detach()[0]) - oracle)
                for nodes in (64, 128, 256)
            ]
            assert all(np.isfinite(errors)) and max(errors) <= 1e-7, errors
            assert abs(bernstein(coefficients, p0).crps(y) - oracle) <= 1e-7
            print("BQN", rain, y, "CDF oracle", oracle, "errors64/128/256", errors)
        def loss(parameters: Tensor, is_rain: bool = rain) -> Tensor:
            return bqn_loss(parameters, torch.tensor([3.0], dtype=torch.float64), is_rain)
        assert torch.autograd.gradcheck(loss, (raw,))


def _all_dry(training: TrainingSet) -> TrainingSet:
    return replace(
        training, rows=tuple(replace(row, observation=0.0) for row in training.rows),
        local_observations=np.zeros_like(training.local_observations),
        thresholds=np.zeros(2), train_hash="neural-audit-all-dry",
    )


def check_fits() -> None:
    for label, training in (
        ("temperature", fixture()), ("rain", fixture(rain=True)),
        ("constant_rain", fixture(rain=True, constant=True)),
        ("all_dry", _all_dry(fixture(rain=True))),
    ):
        for method in ("drn_small", "bqn_monotone"):
            model, diagnostics = fit_neural(method, training, FitConfig())
            repeated, repeated_diagnostics = fit_neural(method, training, FitConfig())
            assert model.to_spec() == repeated.to_spec()
            assert diagnostics.objective == repeated_diagnostics.objective
            assert diagnostics.objective is not None
            assert diagnostics.convergence and np.isfinite(diagnostics.objective)
            law, repeat_law = model.predict(training.target), repeated.predict(training.target)
            # Full tagged-law identity checks all x, not just a quantile grid.
            assert law.to_spec() == repeat_law.to_spec()
            probabilities: FloatArray = np.linspace(0.001, 0.999, 999)
            quantiles = law.quantile(probabilities)
            np.testing.assert_array_equal(quantiles, repeat_law.quantile(probabilities))
            assert np.all(np.diff(quantiles) >= 0) and np.all(np.isfinite(quantiles))
            grid: FloatArray = np.linspace(quantiles.min().item(), quantiles.max().item(), 257)
            cdf = law.cdf(grid)
            np.testing.assert_array_equal(cdf, repeat_law.cdf(grid))
            np.testing.assert_array_equal(law.cdf_left(grid), repeat_law.cdf_left(grid))
            assert np.all(np.diff(cdf) >= 0) and np.all((cdf >= 0) & (cdf <= 1))
            assert np.all(law.cdf(quantiles) >= probabilities - 1e-12)
            assert np.isfinite(law.mean()) and np.isfinite(law.crps(5.0))
            if training.target.variable == "prcp":
                assert 0 < law.atom_mass(0.0) < 1 and np.all(quantiles >= 0)
            if label == "all_dry":
                assert "all_dry_positive_intensity_regularization_identified_only" in diagnostics.boundary_flags
            print(method, label, "objective", diagnostics.objective,
                  "mean", law.mean(), "zero atom", law.atom_mass(0.0),
                  "flags", diagnostics.boundary_flags)
    print("EXACT TWO-SEED FIT/PREDICTION DETERMINISM AND RAIN EDGE CASES PASS")


if __name__ == "__main__":
    check_quadrature()
    check_fits()
