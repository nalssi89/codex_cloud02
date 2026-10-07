"""Rank coupling, physically keyed ECC, and residual Gaussian-copula scenarios."""

from __future__ import annotations

import numpy as np
from scipy.special import ndtr, ndtri
from scipy.stats import qmc

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    PredictiveDistribution,
)
from analysis.alternative_joint_coordinates import fixed_seed, stable_order
from analysis.calibration import FloatArray
from analysis.data_io import Json


def rank_couple(
    template: FloatArray, marginals: tuple[PredictiveDistribution, ...],
    keys: tuple[str, ...], seed: int,
) -> FloatArray:
    """Reorder fixed marginal quantile MULTISETS without jittering template atoms."""
    n, d = np.size(template, axis=0), np.size(template, axis=1)
    probabilities = (np.arange(n, dtype=np.float64) + 0.5) / n
    result = np.empty((n, d), dtype=np.float64)
    for j, marginal in enumerate(marginals):
        order = stable_order(template[:, j], keys, seed)
        result[order, j] = marginal.quantile(probabilities)
    return result


def physical_template(
    targets: tuple[CaseInput, ...],
) -> tuple[FloatArray, tuple[str, ...], dict[str, Json]]:
    """After G3 approval, intersect original physical keys, never array positions."""
    for target in targets:
        if len(target.member_keys) != target.members.size:
            raise AlternativeError("G3_INVALID_KEYS", target.case_id)
        if len(set(target.member_keys)) != len(target.member_keys):
            raise AlternativeError("G3_DUPLICATE_KEYS", target.case_id)
    common = set(targets[0].member_keys)
    for target in targets:
        common.intersection_update(
            key for i, key in enumerate(target.member_keys)
            if np.isfinite(target.members.item(i))
        )
    keys = tuple(sorted(common))
    if len(keys) < 2:
        raise AlternativeError("G3_TOO_FEW_COMMON_MEMBERS", str(len(keys)))
    columns: list[list[float]] = []
    discarded: dict[str, Json] = {}
    fractions: dict[str, Json] = {}
    for target in targets:
        lookup = {key: target.members.item(i) for i, key in enumerate(target.member_keys)}
        columns.append([lookup[key] for key in keys])
        discarded[target.case_id] = [key for key in target.member_keys if key not in common]
        fractions[target.case_id] = len(keys) / len(target.member_keys)
    return np.asarray(columns, dtype=np.float64).T, keys, {
        "retained_fractions": fractions, "discarded_member_ids": discarded,
        "physical_member_ids": list(keys),
    }


def dual_ecc(
    raw: FloatArray, marginals: tuple[PredictiveDistribution, ...],
    keys: tuple[str, ...], error_correlation: FloatArray, scale: FloatArray, seed: int,
) -> FloatArray:
    """Re-rank after error-correlated increments; retain ORIGINAL finite quantiles."""
    calibrated = rank_couple(raw, marginals, keys, seed)
    increment = (calibrated - raw) / scale
    transformed = raw / scale + increment @ np.linalg.cholesky(error_correlation).T
    return rank_couple(transformed, marginals, keys, seed)


def gaussian_copula(
    matrix: FloatArray, marginals: tuple[PredictiveDistribution, ...], seed: int,
    scenario_count: int = 256,
) -> FloatArray:
    """Nested scrambled Sobol construction; 256 and 512 share their first points."""
    if scenario_count not in (256, 512):
        raise AlternativeError("INVALID_SCENARIO_COUNT", "Expected 256 or 512.")
    sampler = qmc.Sobol(d=len(marginals), scramble=True,
                       seed=fixed_seed(seed, "residual-copula") % (2**32))
    uniform = sampler.random_base2(8 if scenario_count == 256 else 9)
    independent = ndtri(np.clip(uniform, 1e-12, 1.0 - 1e-12))
    dependent = independent @ np.linalg.cholesky(matrix).T
    probabilities = ndtr(dependent)
    return np.column_stack([
        marginal.quantile(probabilities[:, j]) for j, marginal in enumerate(marginals)
    ])
