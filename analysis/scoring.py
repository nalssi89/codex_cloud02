"""Proper scores and unit-preserving verification summaries."""

from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from statistics import NormalDist

import numpy as np
from numpy.typing import NDArray

from analysis.data_io import CsvCell, write_csv

FloatArray = NDArray[np.float64]
ScoreRow = Mapping[str, CsvCell]


def empirical_crps(values: FloatArray, observation: float) -> float:
    """CRPS of the issued empirical predictive distribution, not fair-CRPS."""
    ordered = np.sort(values)
    count = len(ordered)
    pair_term = np.sum((2 * np.arange(1, count + 1) - count - 1) * ordered) / count**2
    return array_mean(np.abs(values - observation)) - float(pair_term)


def tercile_probabilities(values: FloatArray, thresholds: FloatArray) -> FloatArray:
    """BN <= q33, NN q33 < Y <= q67, AN > q67."""
    low = np.count_nonzero(values <= thresholds.flat[0]) / len(values)
    cumulative = np.count_nonzero(values <= thresholds.flat[1]) / len(values)
    return np.array([low, cumulative - low, 1 - cumulative], dtype=np.float64)


def probability_scores(probabilities: FloatArray, event: FloatArray) -> tuple[float, float]:
    """Multicategory Brier sum and unnormalized two-boundary ranked probability score."""
    brier = float(np.sum((probabilities - event) ** 2))
    rps = float(np.sum((np.cumsum(probabilities)[:2] - np.cumsum(event)[:2]) ** 2))
    return brier, rps


def score_prediction(
    mean: float, crps: float, probabilities: FloatArray, quantiles: FloatArray,
    observed: float, historical_observed: FloatArray, thresholds: FloatArray,
) -> Mapping[str, CsvCell]:
    """Use exactly the same observation and training climatology for every method."""
    category = int(observed > thresholds.flat[0]) + int(observed > thresholds.flat[1])
    event = np.array([float(index == category) for index in range(3)], dtype=np.float64)
    climate_probability = tercile_probabilities(historical_observed, thresholds)
    brier, rps = probability_scores(probabilities, event)
    climate_brier, climate_rps = probability_scores(climate_probability, event)
    error = mean - observed
    result: dict[str, CsvCell] = {
        "OBS": observed, "PRED_MEAN": mean, "ERROR": error,
        "CLIM_MEAN": array_mean(historical_observed),
        "Q33": float(thresholds.flat[0]), "Q67": float(thresholds.flat[1]),
        "CRPS": crps, "CLIM_CRPS": empirical_crps(historical_observed, observed),
        "BRIER": brier, "CLIM_BRIER": climate_brier,
        "RPS": rps, "CLIM_RPS": climate_rps,
        "P05": float(quantiles.flat[0]), "P95": float(quantiles.flat[1]),
        "COVERAGE90": int(quantiles.flat[0] <= observed <= quantiles.flat[1]),
        "WIDTH90": float(quantiles.flat[1] - quantiles.flat[0]),
    }
    for index, label in enumerate(("BN", "NN", "AN")):
        result[f"P_{label}"] = float(probabilities.flat[index])
        result[f"EVENT_{label}"] = int(event.flat[index])
        result[f"BS_{label}"] = float((probabilities.flat[index] - event.flat[index]) ** 2)
        result[f"CLIM_P_{label}"] = float(climate_probability.flat[index])
        result[f"CLIM_BS_{label}"] = float((climate_probability.flat[index] - event.flat[index]) ** 2)
    return result


def distribution_summary(
    mu: float, sigma: float, thresholds: FloatArray, precipitation: bool,
) -> tuple[float, FloatArray, FloatArray]:
    """The rainfall mean includes the censoring atom; latent mu is not its mean."""
    distribution = np.array(
        [NormalDist(mu, sigma).cdf(float(t)) for t in thresholds.flat], dtype=np.float64,
    )
    probabilities = np.array(
        [distribution.flat[0], distribution.flat[1] - distribution.flat[0], 1 - distribution.flat[1]],
        dtype=np.float64,
    )
    quantiles = np.array(
        [NormalDist(mu, sigma).inv_cdf(p) for p in (0.05, 0.95)], dtype=np.float64,
    )
    mean = mu
    if precipitation:
        z = mu / sigma
        mean = mu * NormalDist().cdf(z) + sigma * math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
        quantiles = np.maximum(quantiles, 0)
    return mean, probabilities, quantiles


def numeric_column(rows: Sequence[ScoreRow], name: str) -> FloatArray:
    """Analysis tables define numeric fields at their production boundary."""
    values: list[float] = []
    for row in rows:
        value = row[name]
        if value is None:
            raise RuntimeError(f"Missing numeric analysis field: {name}")
        values.append(float(value))
    return np.asarray(values, dtype=np.float64)


def correlation(left: FloatArray, right: FloatArray) -> float | None:
    """Undefined correlations are blanks, not invented zero skill."""
    if len(left) < 3 or np.ptp(left) == 0 or np.ptp(right) == 0:
        return None
    x, y = left - array_mean(left), right - array_mean(right)
    covariance = math.fsum(float(a * b) for a, b in zip(x.flat, y.flat, strict=True))
    return covariance / math.sqrt(
        math.fsum(float(a * a) for a in x.flat) * math.fsum(float(b * b) for b in y.flat),
    )


def array_mean(values: FloatArray) -> float:
    """Preserve scalar typing for NumPy versions with untyped mean overloads."""
    return math.fsum(float(v) for v in values.flat) / len(values)


def metric_summary(rows: Sequence[ScoreRow]) -> Mapping[str, CsvCell]:
    """Never pool temperature/rainfall or weekly/monthly incompatible scales."""
    observed, predicted = numeric_column(rows, "OBS"), numeric_column(rows, "PRED_MEAN")
    error = predicted - observed
    climate = numeric_column(rows, "CLIM_MEAN")
    result: dict[str, CsvCell] = {
        "N": len(rows), "BIAS": array_mean(error),
        "MAE": array_mean(np.abs(error)), "RMSE": math.sqrt(array_mean(error**2)),
        "CORRELATION": correlation(predicted, observed),
        "ACC": correlation(predicted - climate, observed - climate),
        "OBS_MEAN": array_mean(observed), "PRED_MEAN": array_mean(predicted),
        "COVERAGE90": array_mean(numeric_column(rows, "COVERAGE90")),
        "WIDTH90": array_mean(numeric_column(rows, "WIDTH90")),
    }
    for score in ("CRPS", "BRIER", "RPS", "BS_BN", "BS_NN", "BS_AN"):
        value = array_mean(numeric_column(rows, score))
        reference = array_mean(numeric_column(rows, f"CLIM_{score}"))
        result[score] = value
        result[f"CLIM_{score}"] = reference
        result[f"{score}_SKILL"] = 1 - value / reference if reference > 0 else None
    return result


def generate_summaries(predictions: Sequence[ScoreRow], output: Path) -> None:
    """Save overall, lead, season, year and valid-month comparison tables."""
    for name, dimensions in (
        ("overall", ("PRODUCT", "VARIABLE", "METHOD")),
        ("by_lead", ("PRODUCT", "VARIABLE", "LEAD", "METHOD")),
        ("by_season", ("PRODUCT", "VARIABLE", "SEASON", "METHOD")),
        ("by_year", ("PRODUCT", "VARIABLE", "YEAR", "METHOD")),
        ("by_month", ("PRODUCT", "VARIABLE", "VALID_MONTH", "METHOD")),
    ):
        groups: dict[tuple[CsvCell, ...], list[ScoreRow]] = defaultdict(list)
        for row in predictions:
            groups[tuple(row[d] for d in dimensions)].append(row)
        records: list[Mapping[str, CsvCell]] = []
        for key, cases in sorted(groups.items(), key=lambda pair: str(pair[0])):
            record = dict(zip(dimensions, key, strict=True))
            record.update(metric_summary(cases))
            records.append(record)
        write_csv(output / f"metrics_{name}.csv", records)
