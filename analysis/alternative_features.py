"""Known mean/spread/calendar/era features with training-only scaling."""

import math
from datetime import timedelta
from typing import assert_never

import numpy as np

from analysis.alternative_contracts import (
    CaseInput,
    FeatureSpec,
    TrainingRow,
    TrainingSet,
)
from analysis.calibration import FloatArray


def _raw(record: CaseInput | TrainingRow, power: float) -> FloatArray:
    """The fixed feature set contains no observed-response-derived predictor."""
    match record:
        case CaseInput():
            ensemble, start, end = record.members, record.valid_start, record.valid_end
        case TrainingRow():
            ensemble, start, end = record.ensemble, record.hist_start, record.hist_end
        case _:
            assert_never(record)
    mean = math.fsum(float(value) for value in ensemble.flat) / ensemble.size
    if power != 1.0:
        mean = math.pow(max(mean, 0.0), power)
    spread = float(np.std(ensemble, ddof=1)) if ensemble.size > 1 else 0.0
    midpoint = start + timedelta(days=(end - start).days // 2)
    phase = 2 * math.pi * (midpoint.timetuple().tm_yday - 1) / 365.2425
    denominator = 7 if record.product == "1mon" else 5
    return np.asarray([
        mean, math.log1p(spread), math.sin(phase), math.cos(phase),
        (int(record.lead[1:]) - 1) / denominator, (end - start).days + 1,
        float(record.archive_era in ("seven_24", "seven_30")),
        float(record.archive_era == "seven_30"),
    ], dtype=np.float64)


def features_for_training(training: TrainingSet) -> tuple[FloatArray, FeatureSpec]:
    """Scale mean, log spread and duration only on eligible year-balanced rows."""
    power = training.feature_spec.predictor_power if training.feature_spec else 1.0
    vectors = [_raw(row, power) for row in training.rows]
    raw: FloatArray = np.asarray(vectors, dtype=np.float64)
    weights: FloatArray = np.asarray(
        training.year_weights / math.fsum(float(w) for w in training.year_weights.flat),
        dtype=np.float64,
    )
    center = np.zeros(8, dtype=np.float64)
    scale = np.ones(8, dtype=np.float64)
    for column in (0, 1, 5):
        center[column] = math.fsum(
            float(weights.flat[index]) * float(vectors[index].flat[column])
            for index in range(len(vectors))
        )
        variance = math.fsum(
            float(weights.flat[index]) * (float(vectors[index].flat[column]) - center[column]) ** 2
            for index in range(len(vectors))
        )
        scale[column] = max(math.sqrt(variance), 1e-6)
    for values in (center, scale):
        values.setflags(write=False)
    spec = FeatureSpec(
        names=("mean", "log_sd", "phase_sin", "phase_cos", "lead",
               "days", "seven_member_era", "extended_history_era"),
        center=center, scale=scale, predictor_power=power,
    )
    return np.asarray((raw - center) / scale, dtype=np.float64), spec


def features_for_case(target: CaseInput, spec: FeatureSpec) -> FloatArray:
    """Apply exactly the fit's saved training scaler to known issue inputs."""
    raw = _raw(target, spec.predictor_power)
    return np.asarray((raw - spec.center) / spec.scale, dtype=np.float64)
