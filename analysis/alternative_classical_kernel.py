"""ID-free equal-member kernels fitted to one mixture likelihood per year."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, expm1, log, sqrt
from time import perf_counter

import numpy as np
from scipy.special import gammaln, logsumexp

from analysis.alternative_classical_common import coordinates, result, softplus, solve
from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FitConfig,
    FitResult,
    FitStatus,
    MethodSpec,
    PredictiveDistribution,
    TrainingSet,
)
from analysis.alternative_distributions import gamma, hurdle, mixture, normal
from analysis.calibration import FloatArray
from analysis.data_io import Json

KERNEL_IDS = ("kernel_normal_equal", "kernel_rain_hurdle_equal")


def kernel_log_likelihood(parameters: FloatArray, members: FloatArray,
                          observation: float, rain: bool, scale: float) -> float:
    """Original-unit annual log probability (mass, not density, at rain zero)."""
    a, b, c = (float(parameters.item(i)) for i in range(3))
    if not rain:
        z = (observation - a - b * members) / exp(c)
        component = -0.5 * z**2 - c - 0.5 * log(2 * np.pi) - log(scale)
    else:
        a0, b0 = float(parameters.item(3)), float(parameters.item(4))
        logits = a0 + b0 * np.log1p(members)
        if observation == 0:
            component = -np.logaddexp(0, -logits)
        else:
            mu = np.logaddexp(0, a + b * members) + 1e-6
            shape = exp(c)
            theta = mu / shape
            component = (-np.logaddexp(0, logits) + (shape - 1) * log(observation)
                         - observation / theta - gammaln(shape)
                         - shape * np.log(theta) - log(scale))
    return float(logsumexp(component) - log(members.size))


def kernel_penalty(parameters: FloatArray, rain: bool) -> float:
    """Shared intensity slope ridge and F6 occurrence ridge, including intercept."""
    penalty = 0.5 * float(parameters.item(1))**2
    if rain:
        penalty += (float(parameters.item(3))**2 + float(parameters.item(4))**2) / 8
    return penalty


@dataclass(frozen=True, slots=True)
class KernelModel:
    method_id: str
    parameters: tuple[float, ...]
    offset: float
    scale: float
    training_nll: float
    penalty: float

    def predict(self, target: CaseInput) -> PredictiveDistribution:
        rain = self.method_id == "kernel_rain_hurdle_equal"
        if ((target.variable == "prcp") != rain or target.members.size == 0
            or not np.all(np.isfinite(target.members))
            or (rain and np.any(target.members < 0))):
            raise ValueError("kernel target has wrong domain or invalid members")
        a, b, c = self.parameters[:3]
        members = (target.members - self.offset) / self.scale
        parts: list[PredictiveDistribution] = []
        for i in range(members.size):
            f = float(members.item(i))
            if rain:
                a0, b0 = self.parameters[3:]
                mu = softplus(a + b * f) + 1e-6
                shape = exp(c)
                parts.append(hurdle(exp(-softplus(-a0 - b0 * log(1+f))),
                                    gamma(shape, self.scale * mu / shape)))
            else:
                parts.append(normal(self.offset + self.scale * (a + b * f),
                                    self.scale * exp(c)))
        return mixture(tuple(parts), np.full(len(parts), 1 / len(parts), dtype=np.float64))

    def to_spec(self) -> dict[str, Json]:
        return {"tag": "equal_member_kernel", "method_id": self.method_id,
                "parameters": list(self.parameters), "offset": self.offset,
                "scale": self.scale, "training_nll": self.training_nll,
                "penalty": self.penalty}


def fit_kernel(spec: MethodSpec, training: TrainingSet, config: FitConfig) -> FitResult:
    """Fit frozen F8 with two 500-iteration starts; unsuccessful solves stay failed."""
    del config  # Solver budget/tolerances are frozen, not target-selected.
    started = perf_counter()
    name = spec.id
    rain = name == "kernel_rain_hurdle_equal"
    if name not in KERNEL_IDS or (training.target.variable == "prcp") != rain:
        return result(name, training, started, None, status=FitStatus.NOT_APPLICABLE_DOMAIN,
                      reason="METHOD_VARIABLE_DOMAIN")
    if len({row.source_year for row in training.rows}) < 10:
        return result(name, training, started, None, status=FitStatus.INSUFFICIENT_TRAINING,
                      reason="FEWER_THAN_TEN_YEARS")
    if (any(row.product != training.target.product or row.variable != training.target.variable
            or row.ensemble.size == 0 or not np.all(np.isfinite(row.ensemble))
            or not np.isfinite(row.observation)
            or (rain and (row.observation < 0 or np.any(row.ensemble < 0)))
            for row in training.rows)
        or training.year_weights.shape != (len(training.rows),)
        or not np.all(np.isfinite(training.year_weights))
        or np.any(training.year_weights <= 0)):
        return result(name, training, started, None, status=FitStatus.INPUT_CONFLICT,
                      reason="INVALID_KERNEL_TRAINING")
    if rain and len({r.source_year for r in training.rows if r.observation > 0}) < 3:
        return result(name, training, started, None, status=FitStatus.INSUFFICIENT_TRAINING,
                      reason="FEWER_THAN_THREE_POSITIVE_YEARS")
    coord = coordinates(training)
    members = tuple((row.ensemble - coord.offset) / coord.scale for row in training.rows)
    y: FloatArray = np.array([(r.observation - coord.offset) / coord.scale
                             for r in training.rows], dtype=np.float64)
    means: FloatArray = np.array([float(f.mean()) for f in members], dtype=np.float64)
    weights = training.year_weights
    climate = float(np.average(y, weights=weights))

    def loss(p: FloatArray) -> float:
        return -sum(float(weights.item(i)) * kernel_log_likelihood(
            p, f, float(y.item(i)), rain, coord.scale) for i, f in enumerate(members))

    def objective(p: FloatArray) -> float:
        return loss(p) + kernel_penalty(p, rain)

    bounds: tuple[tuple[float | None, float | None], ...] = (
        (None, None), (0, None), (-12, 12))
    starts: list[FloatArray] = []
    for slope in (0.0, 1.0):
        if rain:
            wet = y > 0
            mu = float(np.average(y[wet], weights=weights[wet]))
            # Stable inverse softplus of the climate mean.
            intercept = mu + log(-expm1(-mu)) - slope * float(means[wet].mean())
            residual = y[wet] - np.logaddexp(0, intercept + slope * means[wet])
            variance = max(float(np.average(residual**2, weights=weights[wet])), 1e-6)
            shape = min(max(mu**2 / variance, exp(-12)), exp(12))
            p0 = float((np.sum(weights[y == 0]) + 0.5) / (weights.sum() + 1))
            starts.append(np.array([intercept, slope, log(shape), log(p0 / (1-p0)), 0.0]))
        else:
            intercept = climate - slope * float(np.average(means, weights=weights))
            residual = y - intercept - slope * means
            sd = max(sqrt(float(np.average(residual**2, weights=weights))), exp(-12))
            starts.append(np.array([intercept, slope, min(log(sd), 12)]))
    if rain:
        bounds = (*bounds, (None, None), (None, None))
    try:
        p, value, message, flags = solve(objective, tuple(starts), bounds)
        nll, penalty = loss(p), kernel_penalty(p, rain)
        model = KernelModel(name, tuple(float(p.item(i)) for i in range(p.size)),
                            coord.offset, coord.scale,
                            nll, penalty)
        prediction = model.predict(training.target)
        if not np.isfinite(prediction.mean()):
            raise AlternativeError("NONFINITE_KERNEL_MEAN", str(model.to_spec()))
        return result(name, training, started, model, value, len(p),
                      f"{message}; training_nll={nll}; penalty={penalty}", flags)
    except (AlternativeError, ValueError, FloatingPointError, OverflowError) as exc:
        return result(name, training, started, None, status=FitStatus.FIT_FAILED,
                      reason=exc.code if isinstance(exc, AlternativeError) else type(exc).__name__,
                      message=str(exc))
