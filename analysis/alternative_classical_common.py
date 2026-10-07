"""Numerical conventions shared by owned classical models."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from math import exp, log1p
from time import perf_counter

import numpy as np
from scipy.optimize import minimize

from analysis.alternative_contracts import (
    AlternativeError,
    FitDiagnostics,
    FitResult,
    FitStatus,
    FittedModel,
    TrainingSet,
)
from analysis.calibration import FloatArray


@dataclass(frozen=True, slots=True)
class Coordinates:
    offset: float
    scale: float
    mean_center: float
    mean_scale: float
    log_center: float
    log_scale: float


def coordinates(training: TrainingSet) -> Coordinates:
    y = np.array([r.observation for r in training.rows])
    rain = training.target.variable == "prcp"
    offset = 0.0 if rain else float(y.mean())
    positive = y[y > 0]
    scale = (max(float(positive.mean()), 1.0) if positive.size else 1.0
             ) if rain else max(float(y.std()), 1.0)
    m = np.array([(float(r.ensemble.mean()) - offset) / scale for r in training.rows])
    lm = np.log1p(np.maximum(m, 0.0))
    return Coordinates(offset, scale, float(m.mean()), max(float(m.std()), 1e-6),
                       float(lm.mean()), max(float(lm.std()), 1e-6))


def moments(ensemble: FloatArray, coord: Coordinates) -> tuple[float, float]:
    m = (float(ensemble.mean()) - coord.offset) / coord.scale
    v = float(ensemble.var(ddof=1)) / coord.scale**2 if ensemble.size > 1 else 0.0
    return m, v


def solve(objective: Callable[[FloatArray], float], starts: tuple[FloatArray, ...],
          bounds: tuple[tuple[float | None, float | None], ...],
          ) -> tuple[FloatArray, float, str, tuple[str, ...]]:
    """Select only converged finite optimizer results; never retain a start."""
    successes: list[tuple[FloatArray, float, str]] = []
    messages: list[str] = []
    for start in starts:
        result = minimize(objective, start, method="L-BFGS-B", bounds=bounds,
                          options={"maxiter": 500, "ftol": 1e-10, "gtol": 1e-6,
                                   "maxls": 50})
        messages.append(f"success={result.success}; nit={result.nit}; {result.message}")
        if result.success and np.isfinite(result.fun) and np.all(np.isfinite(result.x)):
            successes.append((np.asarray(result.x, dtype=np.float64),
                              float(result.fun), str(result.message)))
    if not successes:
        raise AlternativeError("SOLVER_NOT_CONVERGED", "; ".join(messages))
    p, value, _ = min(successes, key=lambda item: item[1])
    flags = tuple(f"parameter_{i}_bound" for i, (lo, hi) in enumerate(bounds)
                  if (lo is not None and abs(p.item(i) - lo) < 1e-7)
                  or (hi is not None and abs(p.item(i) - hi) < 1e-7))
    return p, value, "; ".join(messages), flags


def result(method_id: str, training: TrainingSet, started: float,
           model: FittedModel | None, objective: float | None = None,
           count: int = 0, message: str = "", flags: tuple[str, ...] = (),
           status: FitStatus = FitStatus.OK, reason: str = "") -> FitResult:
    return FitResult(method_id=method_id, status=status, fitted_model=model,
                     diagnostics=FitDiagnostics(
                         objective=objective, convergence=status == FitStatus.OK,
                         n_rows=len(training.rows),
                         n_years=len({r.source_year for r in training.rows}),
                         train_hash=training.train_hash, parameter_count=count,
                         boundary_flags=flags, elapsed_seconds=perf_counter() - started,
                         message=message), reason_code=reason)


def softplus(value: float) -> float:
    return max(value, 0.0) + log1p(exp(-abs(value)))
