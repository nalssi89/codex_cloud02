"""Fixed physical coordinates shared by the annual joint adaptations."""

from __future__ import annotations

import hashlib
from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from analysis.alternative_contracts import AlternativeError, CaseInput
from analysis.calibration import FloatArray
from analysis.data_io import Json


def rain_columns(targets: tuple[CaseInput, ...]) -> tuple[int, ...]:
    return tuple(j for j, target in enumerate(targets) if target.variable == "prcp")


def forward(values: FloatArray, rain: tuple[int, ...]) -> FloatArray:
    """Transform annual means FIRST, with no training/target dependent metric."""
    result = np.array(values, dtype=np.float64, copy=True)
    if not np.isfinite(result).all():
        raise AlternativeError("NONFINITE_JOINT_INPUT", "Joint coordinates must be finite.")
    for j in rain:
        if np.any(result[..., j] < 0):
            raise AlternativeError("NEGATIVE_RAIN", "Negative rain is not a latent input.")
        result[..., j] = np.sqrt(result[..., j] / 100.0)
    return result


def inverse(values: FloatArray, rain: tuple[int, ...]) -> FloatArray:
    """Call only AFTER adding the entire latent residual vector."""
    result = np.array(values, dtype=np.float64, copy=True)
    for j in rain:
        result[..., j] = 100.0 * np.maximum(0.0, result[..., j]) ** 2
    return result


def fixed_seed(seed: int, *parts: str) -> int:
    digest = hashlib.sha256("|".join((str(seed), *parts)).encode()).digest()
    return int.from_bytes(digest[:8], "big")


def matrix_json(values: FloatArray) -> list[Json]:
    matrix = np.atleast_2d(values)
    return [
        [matrix.item(i, j) for j in range(np.size(matrix, axis=1))]
        for i in range(np.size(matrix, axis=0))
    ]


def vector_json(values: FloatArray) -> list[Json]:
    return [values.item(i) for i in range(values.size)]


def correlation(values: FloatArray) -> FloatArray:
    """Half-shrink empirical Pearson correlation; constant coordinates are independent."""
    centered = values - np.mean(values, axis=0)
    norm = np.sqrt(np.sum(centered * centered, axis=0))
    scaled = np.divide(centered, norm, out=np.zeros_like(centered), where=norm > 0)
    sample = scaled.T @ scaled
    np.fill_diagonal(sample, 1.0)
    result = 0.5 * sample + 0.5 * np.eye(np.size(values, axis=1))
    diagonal = np.sqrt(np.diag(result))
    result = result / diagonal[:, None] / diagonal[None, :]
    _ = np.linalg.cholesky(result)
    return result


def stable_order(values: FloatArray, keys: Sequence[str], seed: int) -> NDArray[np.int64]:
    """Values sort first; only exact ties consult a stable key-derived permutation."""
    hashes = [fixed_seed(seed, "rank-tie", key) for key in keys]
    def order_key(i: int) -> tuple[float, int, str]:
        return values.item(i), hashes[i], keys[i]

    return np.asarray(sorted(range(len(keys)), key=order_key), dtype=np.int64)


def parse_vector(value: Json) -> FloatArray:
    """Parse JSON numeric arrays once at the saved-model boundary."""
    match value:
        case list() as items:
            numbers: list[float] = []
            for item in items:
                match item:
                    case int() | float():
                        numbers.append(float(item))
                    case _:
                        raise AlternativeError("INVALID_JOINT_SPEC", "Expected a numeric vector.")
            return np.asarray(numbers, dtype=np.float64)
        case _:
            raise AlternativeError("INVALID_JOINT_SPEC", "Expected a vector list.")


def parse_vectors(value: Json) -> tuple[FloatArray, ...]:
    match value:
        case list() as rows:
            return tuple(parse_vector(row) for row in rows)
        case _:
            raise AlternativeError("INVALID_JOINT_SPEC", "Expected a matrix list.")
