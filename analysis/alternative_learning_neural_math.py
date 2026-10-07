"""Typed climate initialization and the exact Torch module/optimizer boundaries."""

from math import exp, expm1, log, log1p, sqrt

import numpy as np
import torch
from scipy.optimize import minimize_scalar
from scipy.special import gammaln
from torch import Tensor, nn
from torch.optim import Optimizer

from analysis.alternative_contracts import AlternativeError
from analysis.calibration import FloatArray


def softplus(value: float) -> float:
    return max(value, 0.0) + log1p(exp(-abs(value)))


def inverse_softplus(value: float) -> float:
    return value + log(-expm1(-value))


def forward(model: nn.Sequential, features: Tensor) -> Tensor:
    first, last = model[0], model[2]
    assert isinstance(first, nn.Linear) and isinstance(last, nn.Linear)
    return last.forward(torch.tanh(first.forward(features)))


def adam_step(optimizer: Optimizer) -> None:
    optimizer.step()


def initial_intercepts(
    method: str, y: FloatArray, weights: FloatArray, rain: bool,
) -> FloatArray:
    total = weights.sum().item()
    p0 = (weights[y == 0].sum().item() + 0.5) / (total + 1)
    logit = log(p0 / (1 - p0))
    selected = y > 0 if rain else np.ones(y.size, dtype=bool)
    # For all-dry data, mean=1 is only a climate starting value; the positive
    # intensity and shape are identified exclusively by regularization.
    values = y[selected] if selected.any() else np.array([1.0])
    weight = weights[selected] if selected.any() else np.array([1.0])
    positive_total = weight.sum().item()
    mean = (weight * values).sum().item() / positive_total
    variance = (weight * (values - mean)**2).sum().item() / positive_total
    if method == "drn_small":
        if rain:
            log_y = (weight * np.log(values)).sum().item() / positive_total
            wet_fraction = weights[selected].sum().item() / total
            def climate_shape(raw_shape: float) -> float:
                shape = softplus(raw_shape) + 0.1
                return wet_fraction * (
                    shape * log(mean / shape) + gammaln(shape).item()
                    - (shape - 1) * log_y + shape
                ) + 0.01 * raw_shape**2
            solution = minimize_scalar(climate_shape)
            if not solution.success:
                raise AlternativeError("FIT_FAILED", "Gamma climate initialization failed")
            result = solution.x
            assert isinstance(result, float)
            return np.array([logit, log(mean), result])
        return np.array([mean, inverse_softplus(max(sqrt(variance), 1e-3))])
    coefficients = np.asarray(np.quantile(values, np.linspace(0, 1, 6)), dtype=np.float64)
    first = inverse_softplus(max(coefficients.item(0) - 1e-6, 1e-4)) if rain else coefficients.item(0)
    increments = np.diff(coefficients)
    return np.array([
        first, *[inverse_softplus(max(increments.item(k) - 1e-6, 1e-4)) for k in range(5)],
        *([logit] if rain else []),
    ], dtype=np.float64)
