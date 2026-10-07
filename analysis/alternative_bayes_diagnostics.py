"""Rank/folded split diagnostics and conservative batch Monte Carlo errors.

Inputs are retained, unthinned values in (chain, draw, variable) order.
ESS uses the multi-chain variance estimate and Geyer's initial-positive,
initial-monotone paired autocorrelation sequence (Vehtari et al., 2021).
"""

from __future__ import annotations

from math import log10, sqrt

import numpy as np
from scipy.special import ndtri
from scipy.stats import rankdata

from analysis.calibration import FloatArray
from analysis.data_io import Json


def _validate(draws: FloatArray) -> None:
    if draws.ndim != 3 or draws.shape[0] < 2 or draws.shape[1] < 4:
        raise ValueError("Expected (>=2 chains, >=4 draws, >=1 parameters)")
    if draws.shape[2] == 0 or not np.all(np.isfinite(draws)):
        raise ValueError("Parameters must be nonempty and all draws finite")


def _split(draws: FloatArray) -> FloatArray:
    half = np.size(draws, axis=1) // 2
    return np.concatenate((draws[:, :half], draws[:, -half:]), axis=0)


def _rank(values: FloatArray) -> FloatArray:
    ranks = np.asarray(rankdata(values, method="average"), dtype=np.float64)
    return np.asarray(
        ndtri((ranks - 0.375) / (values.size + 0.25)), dtype=np.float64
    ).reshape(values.shape)


def _variance(values: FloatArray) -> tuple[float, float]:
    n = np.size(values, axis=1)
    within = float(np.mean(np.var(values, axis=1, ddof=1)))
    if np.all(np.equal(values, values[:, :1])):
        within = 0.0
    between_mean = float(np.var(np.mean(values, axis=1), ddof=1))
    return within, within * (n - 1) / n + between_mean


def _rhat(values: FloatArray) -> float:
    within, variance = _variance(values)
    if within == 0:
        return 1.0 if variance == 0 else float("inf")
    return sqrt(variance / within)


def _ess(values: FloatArray) -> float:
    """FFT biased autocovariances, then positive monotone even/odd pairs."""
    chains, n = np.size(values, axis=0), np.size(values, axis=1)
    total = chains * n
    within, variance = _variance(values)
    if variance == 0:
        return float(total)
    if within == 0:
        return 1.0
    centered = values - np.mean(values, axis=1, keepdims=True)
    fft_size = 1 << (2 * n - 1).bit_length()
    spectrum = np.fft.rfft(centered, n=fft_size, axis=1)
    acov = np.fft.irfft(
        spectrum * np.conjugate(spectrum), n=fft_size, axis=1
    )[:, :n] / n
    rho = 1 - (within - np.mean(acov, axis=0)) / variance
    rho[0] = 1.0
    pair_sum = 0.0
    previous = float("inf")
    for lag in range(0, n - 1, 2):
        pair = rho.item(lag) + rho.item(lag + 1)
        if pair <= 0:
            break
        previous = min(previous, pair)
        pair_sum += previous
    # Permit antithetic ESS > draw count, bounded as in the rank-ESS method.
    tau = max(-1 + 2 * pair_sum, 1 / log10(total))
    return float(total / tau)


def diagnose(draws: FloatArray) -> dict[str, Json]:
    """Return aggregate and ordered per-variable diagnostics.

    Odd lengths drop the central draw when splitting. Tail ESS is the minimum
    ESS of indicators below pooled 5% and 95% quantiles. Unidentified constant
    chains get null R-hat (JSON-safe infinity), ESS=1 and fail; a globally
    constant variable has R-hat=1 and ESS equal to the split draw count.
    """
    _validate(draws)
    split = _split(draws)
    rhats: list[Json] = []
    bulk: list[Json] = []
    tail: list[Json] = []
    numerical_rhats: list[float] = []
    numerical_bulk: list[float] = []
    numerical_tail: list[float] = []
    for parameter in range(np.size(draws, axis=2)):
        raw = split[:, :, parameter]
        ranked = _rank(raw)
        folded = _rank(np.abs(raw - np.median(raw)))
        rhat = max(_rhat(ranked), _rhat(folded))
        bulk_ess = _ess(ranked)
        limits = np.quantile(draws[:, :, parameter], [0.05, 0.95])
        tail_ess = min(
            _ess(np.asarray(np.less_equal(raw, limits.item(0)), dtype=np.float64)),
            _ess(np.asarray(np.less_equal(raw, limits.item(1)), dtype=np.float64)),
        )
        numerical_rhats.append(rhat)
        numerical_bulk.append(bulk_ess)
        numerical_tail.append(tail_ess)
        rhats.append(rhat if np.isfinite(rhat) else None)
        bulk.append(bulk_ess)
        tail.append(tail_ess)
    maximum = max(numerical_rhats)
    minimum_bulk = min(numerical_bulk)
    minimum_tail = min(numerical_tail)
    return {
        "rhat_max": maximum if np.isfinite(maximum) else None,
        "ess_bulk_min": minimum_bulk,
        "ess_tail_min": minimum_tail,
        "passed": bool(maximum <= 1.01 and minimum_bulk >= 400 and minimum_tail >= 400),
        "rhat": rhats,
        "ess_bulk": bulk,
        "ess_tail": tail,
    }


def mcse(draws: FloatArray) -> FloatArray:
    """Estimate error of the grand mean of arbitrary influence values.

    Nonoverlapping sqrt(n)-length batches estimate each chain's mean variance.
    The larger of their pooled independent-chain estimate and the observed
    between-chain mean variance is used. Incomplete final batches are omitted
    only from the within-chain estimate, not from between-chain means.
    Apply directly to means, probability indicators, or CRPS influence values;
    this is not an error estimate for a nonlinear statistic without influence
    values. As with any batch estimator, sufficiently long chains are required.
    """
    _validate(draws)
    chains = np.size(draws, axis=0)
    n, parameters = np.size(draws, axis=1), np.size(draws, axis=2)
    length = int(sqrt(n))
    count = n // length
    batches = draws[:, : count * length].reshape(
        chains, count, length, parameters
    ).mean(axis=2)
    within = np.sum(np.var(batches, axis=1, ddof=1), axis=0) / (
        count * chains**2
    )
    between = np.var(np.mean(draws, axis=1), axis=0, ddof=1) / chains
    return np.asarray(np.sqrt(np.maximum(within, between)), dtype=np.float64)
