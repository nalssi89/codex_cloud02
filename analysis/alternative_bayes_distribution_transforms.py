"""Fixed physical transforms shared without a scalar/precision import cycle."""

from __future__ import annotations

import math

import numpy as np

from analysis.calibration import FloatArray

LOG_SINH_ONE = math.log(math.sinh(1))
TRANSFORMS = {"temperature", "sqrt", "yj", "logsinh"}


def _array(value: object) -> FloatArray:
    return np.asarray(value, dtype=np.float64)


def forward(values: FloatArray, transform: str) -> FloatArray:
    """Fixed physical-to-latent coordinates; rain inputs must be nonnegative."""
    x = _array(values)
    if transform not in TRANSFORMS or np.any(np.isnan(x)):
        raise ValueError("unknown transform or NaN coordinate")
    if transform == "temperature":
        return _array((x - 10) / 10)
    if np.any(x < 0):
        raise ValueError("negative physical rain")
    if transform == "sqrt":
        return _array(np.sqrt(x / 100))
    if transform == "yj":
        return _array(2 * np.expm1(.5 * np.log1p(x / 100)))
    u = 1 + x / 100
    result = u + np.log1p(-np.exp(-2 * u)) - math.log(2) - LOG_SINH_ONE
    return _array(np.where(np.equal(x, 0), 0, result))


def inverse(values: FloatArray, transform: str) -> FloatArray:
    """Stable censored physical inverse, including both support endpoints."""
    z = _array(values)
    if transform not in TRANSFORMS or np.any(np.isnan(z)):
        raise ValueError("unknown transform or NaN coordinate")
    if transform == "temperature":
        return _array(10 + 10 * z)
    z = np.maximum(0, z)
    if transform == "sqrt":
        return _array(100 * z**2)
    if transform == "yj":
        return _array(100 * (z + z**2 / 4))
    u = z + LOG_SINH_ONE
    # asinh(exp(u)) without ever exponentiating a large positive coordinate.
    a = np.arcsinh(np.exp(np.minimum(u, 0)))
    b = np.maximum(u, 0) + np.log1p(np.sqrt(1 + np.exp(-2 * np.maximum(u, 0))))
    result = np.maximum(0, 100 * (np.where(u >= 0, b, a) - 1))
    return _array(np.where(z <= 0, 0, result))
