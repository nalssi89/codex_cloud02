"""Fixed, year-balanced CPU DRN/BQN fits; prediction never consumes truth."""

from __future__ import annotations

from dataclasses import dataclass
from math import comb, exp, log, pi
from time import perf_counter

import numpy as np
import torch
from torch import Tensor, nn
from torch.nn import functional as F

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FeatureSpec,
    FitConfig,
    FitDiagnostics,
    FittedModel,
    PredictiveDistribution,
    TrainingSet,
)
from analysis.alternative_data import features_for_case, features_for_training
from analysis.alternative_distributions import (
    gamma,
    hurdle,
    mixture,
    normal,
)
from analysis.alternative_learning_bernstein import learning_bernstein
from analysis.alternative_learning_neural_math import (
    adam_step,
    forward,
    initial_intercepts,
    softplus,
)
from analysis.calibration import FloatArray
from analysis.data_io import Json


def _network(n_outputs: int, seed: int, intercepts: FloatArray) -> nn.Sequential:
    _ = torch.default_generator.manual_seed(seed)
    model = nn.Sequential(nn.Linear(8, 4), nn.Tanh(), nn.Linear(4, n_outputs))
    model = model.to(dtype=torch.float64, device="cpu")
    with torch.no_grad():
        for layer in model:
            if isinstance(layer, nn.Linear):
                _ = nn.init.xavier_uniform_(layer.weight)
                _ = layer.bias.zero_()
        layer = model[2]
        assert isinstance(layer, nn.Linear)
        _ = layer.bias.copy_(torch.as_tensor(intercepts, dtype=torch.float64))
    return model


def _coefficients(raw: Tensor, rain: bool) -> Tensor:
    first = F.softplus(raw[:, :1]) + 1e-6 if rain else raw[:, :1]
    return torch.cat((first, first + torch.cumsum(
        F.softplus(raw[:, 1:6]) + 1e-6, dim=1,
    )), dim=1)


def bqn_loss(raw: Tensor, y: Tensor, rain: bool, nodes: int = 64) -> Tensor:
    """Split atom and Q(v)=y kink; moving-boundary terms vanish at the kink."""
    abscissa, weights = np.polynomial.legendre.leggauss(nodes)
    v = torch.as_tensor((abscissa + 1) / 2, dtype=torch.float64)
    w = torch.as_tensor(weights / 2, dtype=torch.float64)
    transform = np.array([
        [comb(5, k) * comb(5 - k, j - k) * (-1)**(j - k) if j >= k else 0
         for k in range(6)] for j in range(6)
    ], dtype=np.float64)
    polynomial = _coefficients(raw, rain) @ torch.as_tensor(transform.T, dtype=torch.float64)
    # Detached inverse is valid: both pinball branches equal zero at Q=y.
    a = np.asarray(polynomial.detach().numpy(), dtype=np.float64)
    observed = np.asarray(y.detach().numpy(), dtype=np.float64)
    lower, upper = np.zeros_like(observed), np.ones_like(observed)
    for _ in range(52):
        midpoint = (lower + upper) / 2
        value = a[:, 5]
        for k in range(4, -1, -1):
            value = value * midpoint + a[:, k]
        below = value < observed
        lower, upper = np.where(below, midpoint, lower), np.where(below, upper, midpoint)
    crossing = torch.as_tensor((lower + upper)[:, None] / 2, dtype=torch.float64)
    p0 = torch.sigmoid(raw[:, 6:7]) if rain else torch.zeros_like(y[:, None])
    wet = torch.ones_like(p0) - p0
    result = y * p0[:, 0] ** 2
    for start, width in (
        (torch.zeros_like(crossing), crossing), (crossing, torch.ones_like(crossing) - crossing),
    ):
        location = start + width * v
        q = polynomial[:, 5:6]
        for k in range(4, -1, -1):
            q = q * location + polynomial[:, k:k + 1]
        u = p0 + wet * location
        error = y[:, None] - q
        pinball = torch.maximum(u * error, (u - 1) * error)
        result = result + wet[:, 0] * width[:, 0] * (pinball @ w) * 2
    return result


def _drn_loss(raw: Tensor, y: Tensor, rain: bool) -> Tensor:
    if not rain:
        sigma = F.softplus(raw[:, 1]) + 1e-4
        return torch.log(sigma) + 0.5 * ((y - raw[:, 0]) / sigma) ** 2 + (
            0.5 * log(2 * pi)
        )
    shape = F.softplus(raw[:, 2]) + 0.1
    log_mean = raw[:, 1]
    positive = torch.clamp(y, min=torch.finfo(torch.float64).tiny)
    log_density = (
        shape * (torch.log(shape) - log_mean) - torch.lgamma(shape)
        + (shape - 1) * torch.log(positive) - positive * shape * torch.exp(-log_mean)
    )
    return torch.where(
        y == 0, F.softplus(-raw[:, 0]), F.softplus(raw[:, 0]) - log_density,
    )


@dataclass(frozen=True)
class NeuralModel:
    """Two complete fitted laws, mixed equally rather than averaged parameters."""

    method_id: str
    rain: bool
    feature_spec: FeatureSpec
    parameters: tuple[tuple[FloatArray, ...], ...]
    seeds: tuple[int, int]
    torch_version: str

    def predict(self, target: CaseInput) -> PredictiveDistribution:
        if (target.variable == "prcp") != self.rain:
            raise AlternativeError("INPUT_CONFLICT", "neural model variable mismatch")
        x = features_for_case(target, self.feature_spec)
        parts: list[PredictiveDistribution] = []
        for w1, b1, w2, b2 in self.parameters:
            raw = np.asarray(w2 @ np.tanh(w1 @ x + b1) + b2, dtype=np.float64)
            if self.method_id == "bqn_monotone":
                first = softplus(raw.item(0)) + 1e-6 if self.rain else raw.item(0)
                coefficients = np.concatenate((np.array([first]), first + np.cumsum(
                    np.logaddexp(0, raw[1:6]) + 1e-6,
                )))
                p0 = exp(-softplus(-raw.item(6))) if self.rain else 0.0
                parts.append(learning_bernstein(coefficients, p0))
            elif self.rain:
                p0 = exp(-softplus(-raw.item(0)))
                shape = softplus(raw.item(2)) + 0.1
                parts.append(hurdle(p0, gamma(shape, exp(raw.item(1)) / shape)))
            else:
                parts.append(normal(raw.item(0), softplus(raw.item(1)) + 1e-4))
        return mixture(tuple(parts), np.array([0.5, 0.5]))

    def to_spec(self) -> dict[str, Json]:
        return {
            "kind": "neural", "method_id": self.method_id, "rain": self.rain,
            "parameters": [[p.tolist() for p in seed] for seed in self.parameters],
            "seeds": list(self.seeds), "torch_version": self.torch_version,
            "feature_spec": {
                "names": list(self.feature_spec.names),
                "center": self.feature_spec.center.tolist(),
                "scale": self.feature_spec.scale.tolist(),
                "predictor_power": self.feature_spec.predictor_power,
            },
        }


def fit_neural(
    method_id: str, training: TrainingSet, config: FitConfig,
) -> tuple[FittedModel, FitDiagnostics]:
    """400 full-batch Adam steps per fixed seed; retain best finite training loss."""
    started = perf_counter()
    if method_id not in ("drn_small", "bqn_monotone"):
        raise AlternativeError("INPUT_CONFLICT", f"unknown neural method {method_id}")
    if torch.__version__.split("+")[0] != "2.8.0":
        raise AlternativeError("FIT_FAILED", "neural algorithm requires Torch 2.8.0 CPU")
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    x_array, feature_spec = features_for_training(training)
    y_array = np.array([row.observation for row in training.rows], dtype=np.float64)
    rain = training.target.variable == "prcp"
    weights_array = training.year_weights
    x, y = torch.as_tensor(x_array, dtype=torch.float64), torch.as_tensor(y_array, dtype=torch.float64)
    weights = torch.as_tensor(weights_array / weights_array.sum(), dtype=torch.float64)
    intercepts = initial_intercepts(method_id, y_array, weights_array, rain)
    seeds = (config.seed, config.seed + 1)
    parameters: list[tuple[FloatArray, ...]] = []
    objectives: list[float] = []
    for seed in seeds:
        model = _network(intercepts.size, seed, intercepts)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
        best = float("inf")
        best_parameters: tuple[FloatArray, ...] = ()
        for step in range(401):
            optimizer.zero_grad()
            raw = forward(model, x)
            losses = bqn_loss(raw, y, rain) if method_id == "bqn_monotone" else _drn_loss(raw, y, rain)
            penalty = torch.zeros((), dtype=torch.float64)
            for name, parameter in model.named_parameters():
                if name == "2.bias" and rain:
                    index = 6 if method_id == "bqn_monotone" else 0
                    penalty = penalty + 0.01 * (
                        parameter[:index].square().sum() + parameter[index + 1:].square().sum()
                    ) + 0.125 * parameter[index].square()
                else:
                    penalty = penalty + 0.01 * parameter.square().sum()
            objective = torch.dot(weights, losses) + penalty
            value = float(objective.detach())
            if not np.isfinite(value):
                raise AlternativeError("FIT_FAILED", f"nonfinite neural objective at seed {seed}, step {step}")
            if value < best:
                best = value
                best_parameters = tuple(
                    np.asarray(p.detach().numpy(), dtype=np.float64).copy() for p in model.parameters()
                )
            if step < 400:
                torch.autograd.backward(objective)
                norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 5)
                if not bool(torch.isfinite(norm)):
                    raise AlternativeError("FIT_FAILED", "nonfinite neural gradient")
                adam_step(optimizer)
        parameters.append(best_parameters)
        objectives.append(best)
    fitted = NeuralModel(method_id, rain, feature_spec, tuple(parameters), seeds, str(torch.__version__))
    flags = ("bounded_quantile_tails",) if method_id == "bqn_monotone" else ()
    lowest, highest = y_array.min().item(), y_array.max().item()
    if rain and highest == 0:
        flags += ("all_dry_positive_intensity_regularization_identified_only",)
    if rain and highest == lowest and lowest > 0:
        flags += ("constant_positive_rain_history",)
    return fitted, FitDiagnostics(
        objective=float(np.mean(objectives)), convergence=True,
        n_rows=len(training.rows), n_years=len({r.source_year for r in training.rows}),
        train_hash=training.train_hash, parameter_count=2 * sum(p.size for p in parameters[0]),
        boundary_flags=flags,
        elapsed_seconds=perf_counter() - started,
        message="Two fixed seeds; 400 Adam steps each; finite budget completion, not stationarity.",
    )
