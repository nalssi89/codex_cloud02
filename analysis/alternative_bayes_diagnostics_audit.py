"""Executable mathematical audit: python -m analysis.alternative_bayes_diagnostics_audit."""

from __future__ import annotations

import json
from math import log10, sqrt
from statistics import NormalDist

import numpy as np

from analysis.alternative_bayes_diagnostics import diagnose, mcse
from analysis.calibration import FloatArray


def _rank_oracle(values: FloatArray) -> FloatArray:
    """Independent sorted tie groups and standard-library inverse Normal."""
    flat = values.ravel()
    order = np.argsort(flat)
    result = np.empty(flat.size, dtype=np.float64)
    start = 0
    normal = NormalDist()
    while start < flat.size:
        end = start + 1
        while end < flat.size and flat[order[end]] == flat[order[start]]:
            end += 1
        rank = (start + 1 + end) / 2
        score = normal.inv_cdf((rank - 0.375) / (flat.size + 0.25))
        result[order[start:end]] = score
        start = end
    return result.reshape(values.shape)


def _rhat_oracle(values: FloatArray) -> float:
    m, n = np.size(values, axis=0), np.size(values, axis=1)
    means = [float(np.sum(np.take(values, [c], axis=0))) / n for c in range(m)]
    grand = sum(means) / m
    within = sum(
        float(np.sum((np.take(values, [c], axis=0) - means[c]) ** 2)) / (n - 1)
        for c in range(m)
    ) / m
    between = n * sum((mean - grand) ** 2 for mean in means) / (m - 1)
    return sqrt(((n - 1) * within + between) / (n * within))


def _ess_oracle(values: FloatArray) -> float:
    """Direct O(n^2) lag dot products, not the implementation's FFT."""
    m, n = np.size(values, axis=0), np.size(values, axis=1)
    centered = values - np.mean(values, axis=1, keepdims=True)
    w = float(np.sum(centered**2)) / (m * (n - 1))
    v = (n - 1) * w / n + float(np.var(np.mean(values, axis=1), ddof=1))
    correlations = [1.0]
    for lag in range(1, n):
        covariance = sum(
            float(np.sum(centered[c, :-lag] * centered[c, lag:])) for c in range(m)
        ) / (m * n)
        correlations.append(1 - (w - covariance) / v)
    pairs = [
        correlations[i] + correlations[i + 1] for i in range(0, n - 1, 2)
    ]
    positive: list[float] = []
    for pair in pairs:
        if pair <= 0:
            break
        positive.append(pair)
    monotone_sum = 0.0
    for i in range(len(positive)):
        monotone_sum += min(positive[:i + 1])
    return m * n / max(2 * monotone_sum - 1, 1 / log10(m * n))


def _formula_audit(rng: np.random.Generator) -> None:
    # Odd lengths, tied indicator-like values and nontrivial lag correlations.
    raw = np.round(rng.normal(size=(4, 129, 2)), 1)
    raw[:, 1:, 0] += 0.7 * raw[:, :-1, 0]
    report = diagnose(raw)
    rhats: list[float] = []
    bulks: list[float] = []
    tails: list[float] = []
    for p in range(2):
        split = np.vstack((raw[:, :64, p], raw[:, -64:, p]))
        rank = _rank_oracle(split)
        fold = _rank_oracle(np.abs(split - np.median(split)))
        rhats.append(max(_rhat_oracle(rank), _rhat_oracle(fold)))
        bulks.append(_ess_oracle(rank))
        q = np.quantile(raw[:, :, p], [0.05, 0.95])
        tails.append(min(
            _ess_oracle(np.asarray(np.less_equal(split, q.item(j)), dtype=np.float64))
            for j in range(2)
        ))
    for key, expected in (("rhat", rhats), ("ess_bulk", bulks), ("ess_tail", tails)):
        actual = report[key]
        assert isinstance(actual, list)
        numeric: list[float] = []
        for value in actual:
            assert isinstance(value, float)
            numeric.append(value)
        np.testing.assert_allclose(numeric, expected, rtol=1e-12)


def _behavior_audit(rng: np.random.Generator) -> None:
    iid = rng.normal(size=(4, 8192, 3))
    healthy = diagnose(iid)
    assert healthy["passed"] is True, healthy
    shifted = iid.copy()
    shifted[0, :, 0] += 2
    assert diagnose(shifted)["passed"] is False
    unequal_scale = iid.copy()
    unequal_scale[0] *= 5
    assert diagnose(unequal_scale)["passed"] is False
    walk = np.empty((4, 8192, 1), dtype=np.float64)
    walk[:, 0, 0] = rng.normal(size=4)
    innovations = rng.normal(size=walk.shape) * sqrt(1 - 0.8**2)
    for t in range(1, walk.shape[1]):
        walk[:, t] = 0.8 * walk[:, t - 1] + innovations[:, t]
    ar_report = diagnose(walk)
    ess = ar_report["ess_bulk_min"]
    assert isinstance(ess, float)
    # Analytic AR(1) asymptotic ESS = mn*(1-rho)/(1+rho).
    expected = 4 * 8192 / 9
    assert 0.7 * expected < ess < 1.3 * expected, ar_report
    constant = np.ones((4, 1024, 2), dtype=np.float64)
    assert diagnose(constant)["passed"] is True
    constant[0, :, 0] = 2
    failed = diagnose(constant)
    assert failed["passed"] is False and failed["rhat_max"] is None
    _ = json.dumps(failed, allow_nan=False)
    np.testing.assert_allclose(
        mcse(iid) * sqrt(4 * 8192), np.ones(3), rtol=0.3
    )
    indicators = np.asarray(iid > 0, dtype=np.float64)
    np.testing.assert_allclose(
        mcse(indicators) * sqrt(4 * 8192), np.full(3, 0.5), rtol=0.3
    )


def _batch_audit() -> None:
    values = np.arange(4 * 37 * 2, dtype=np.float64).reshape(4, 37, 2) / 100
    oracle: list[float] = []
    for p in range(2):
        batch_means = np.array([
            [float(np.mean(values[c, j * 6:(j + 1) * 6, p])) for j in range(6)]
            for c in range(4)
        ])
        within = sum(
            float(np.var(np.take(batch_means, [c], axis=0), ddof=1)) for c in range(4)
        ) / 96
        means = np.array([float(np.mean(values[c, :, p])) for c in range(4)])
        between = float(np.var(means, ddof=1)) / 4
        oracle.append(sqrt(max(within, between)))
    np.testing.assert_allclose(mcse(values), oracle, rtol=1e-14)
    np.testing.assert_allclose(mcse(-3 * values + 7), 3 * mcse(values))
    np.testing.assert_array_equal(mcse(np.ones_like(values)), [0, 0])
    # Chain-constant disagreement must not misleadingly yield zero error.
    assert np.all(mcse(np.broadcast_to(values[:, :1], values.shape)) > 0)


def main() -> None:
    rng = np.random.default_rng(20261007)
    _formula_audit(rng)
    _behavior_audit(rng)
    _batch_audit()
    for invalid in (
        np.zeros((1, 20, 1)), np.zeros((2, 3, 1)),
        np.zeros((2, 20, 0)), np.full((2, 20, 1), np.nan),
    ):
        for function in (diagnose, mcse):
            try:
                _ = function(invalid)
            except ValueError:
                continue
            raise AssertionError("Invalid draws were accepted")
    print("PASS: independent rank/R-hat/ESS formulas, AR(1), tails, batches, input gates")


if __name__ == "__main__":
    main()
