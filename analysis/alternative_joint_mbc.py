"""Frozen out-of-sample empirical MBCp/MBCr/MBCn annual-mean compositions."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

import numpy as np

from analysis.alternative_contracts import AlternativeError
from analysis.alternative_joint_coordinates import (
    fixed_seed,
    matrix_json,
    parse_vector,
    parse_vectors,
    vector_json,
)
from analysis.calibration import FloatArray
from analysis.data_io import Json


@dataclass(frozen=True, slots=True, kw_only=True)
class AffineStep:
    matrix: FloatArray
    offset: FloatArray

    def apply(self, x: FloatArray) -> FloatArray:
        return x @ self.matrix + self.offset

    def to_spec(self) -> dict[str, Json]:
        return {"kind": "affine", "matrix": matrix_json(self.matrix),
                "offset": vector_json(self.offset)}


@dataclass(frozen=True, slots=True, kw_only=True)
class ScalarStep:
    knots: tuple[FloatArray, ...]
    values: tuple[FloatArray, ...]

    def apply(self, x: FloatArray) -> FloatArray:
        rows = np.atleast_2d(x)
        mapped = np.column_stack([
            np.interp(rows[:, j], knots, values)
            for j, (knots, values) in enumerate(zip(self.knots, self.values, strict=True))
        ])
        return mapped[0] if x.ndim == 1 else mapped

    def to_spec(self) -> dict[str, Json]:
        return {"kind": "scalar", "knots": [vector_json(k) for k in self.knots],
                "values": [vector_json(v) for v in self.values]}


type MapStep = AffineStep | ScalarStep


@dataclass(frozen=True, slots=True, kw_only=True)
class FrozenMap:
    method_id: str
    steps: tuple[MapStep, ...]
    dimension: int

    def apply(self, x: FloatArray) -> FloatArray:
        if np.size(x, axis=-1) != self.dimension:
            raise AlternativeError("MBC_DIMENSION_MISMATCH", str(x.shape))
        result = x.copy()
        for step in self.steps:
            result = step.apply(result)
        return result

    def to_spec(self) -> dict[str, Json]:
        return {"type": "frozen_annual_mbc", "method_id": self.method_id,
                "dimension": self.dimension, "steps": [step.to_spec() for step in self.steps],
                "metric": "T_degC,sqrt(P_mm/100)", "endpoints": "constant"}


def empirical_step(x: FloatArray, y: FloatArray | None = None) -> ScalarStep:
    """Fit tied source midranks -> destination interpolated midpoint quantiles."""
    knots: list[FloatArray] = []
    values: list[FloatArray] = []
    for j in range(np.size(x, axis=1)):
        unique, counts = np.unique(x[:, j], return_counts=True)
        positions = (np.cumsum(counts) - 0.5 * counts) / np.size(x, axis=0)
        knots.append(unique)
        if y is None:
            values.append(positions)
        else:
            n = np.size(y, axis=0)
            values.append(np.interp(positions, (np.arange(n) + 0.5) / n, np.sort(y[:, j])))
    return ScalarStep(knots=tuple(knots), values=tuple(values))


def recolor(x: FloatArray, y: FloatArray) -> AffineStep:
    dimension = np.size(x, axis=1)

    def factor(values: FloatArray) -> FloatArray:
        covariance = np.atleast_2d(np.cov(values, rowvar=False, ddof=1))
        covariance = 0.5 * covariance + 0.5 * np.diag(np.diag(covariance))
        return np.linalg.cholesky(covariance + 1e-6 * np.eye(dimension))

    matrix = np.linalg.solve(factor(x).T, factor(y).T)
    return AffineStep(matrix=matrix, offset=np.mean(y, axis=0) - np.mean(x, axis=0) @ matrix)


def fit_map(method_id: str, x: FloatArray, y: FloatArray, seed: int) -> FrozenMap:
    """Fit every operation on training vectors and retain all of them for replay."""
    if x.shape != y.shape or x.ndim != 2 or np.size(x, axis=0) < 2:
        raise AlternativeError("INVALID_MBC_TRAINING", f"{x.shape},{y.shape}")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise AlternativeError("NONFINITE_MBC_TRAINING", method_id)
    dimension = np.size(x, axis=1)
    steps: list[MapStep] = []
    current = x.copy()

    def append(step: MapStep) -> None:
        nonlocal current
        steps.append(step)
        current = step.apply(current)

    match method_id:
        case "mbcp_annual":
            append(empirical_step(current, y))
            for _ in range(20):
                append(recolor(current, y))
                append(empirical_step(current, y))
        case "mbcr_annual":
            append(empirical_step(current))
            target_ranks = empirical_step(y).apply(y)
            for _ in range(20):
                append(recolor(current, target_ranks))
                append(empirical_step(current))
            n = np.size(y, axis=0)
            positions = (np.arange(n) + 0.5) / n
            append(ScalarStep(
                knots=tuple(positions.copy() for _ in range(dimension)),
                values=tuple(np.sort(y[:, j]) for j in range(dimension)),
            ))
        case "mbcn_annual":
            append(empirical_step(current, y))
            rng = np.random.default_rng(fixed_seed(seed, "mbcn-Haar", str(dimension)))
            for _ in range(30):
                rotation, triangular = np.linalg.qr(rng.normal(size=(dimension, dimension)))
                signs = np.where(np.diag(triangular) < 0, -1.0, 1.0)
                rotation = rotation * signs
                append(AffineStep(matrix=rotation, offset=np.zeros(dimension)))
                append(empirical_step(current, y @ rotation))
                append(AffineStep(matrix=rotation.T, offset=np.zeros(dimension)))
            append(empirical_step(current, y))
        case _:
            raise AlternativeError("UNKNOWN_MBC_METHOD", method_id)
    if not np.isfinite(current).all():
        raise AlternativeError("NONFINITE_MBC_MAP", method_id)
    return FrozenMap(method_id=method_id, steps=tuple(steps), dimension=dimension)


def map_from_spec(spec: Mapping[str, Json]) -> FrozenMap:
    """Reconstruct the saved composition without touching its original training."""
    method, dimension, items = spec["method_id"], spec["dimension"], spec["steps"]
    if not isinstance(method, str) or not isinstance(dimension, int) or not isinstance(items, list):
        raise AlternativeError("INVALID_MAP_SPEC", "Method/dimension/steps malformed.")
    steps: list[MapStep] = []
    for item in items:
        match item:
            case {"kind": "affine", "matrix": matrix, "offset": offset}:
                steps.append(AffineStep(matrix=np.asarray(parse_vectors(matrix)), offset=parse_vector(offset)))
            case {"kind": "scalar", "knots": knots, "values": values}:
                steps.append(ScalarStep(knots=parse_vectors(knots), values=parse_vectors(values)))
            case _:
                raise AlternativeError("INVALID_MAP_SPEC", "Unknown saved map operation.")
    return FrozenMap(method_id=method, dimension=dimension, steps=tuple(steps))
