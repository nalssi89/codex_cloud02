"""Original saved weighted scenario expectations in outer-training coordinates."""

from __future__ import annotations

import math
from collections.abc import Callable
from itertools import combinations
from pathlib import Path

import numpy as np

from analysis.alternative_validation_io import (
    csv_records,
    decode,
    require_columns,
    sequence,
    text,
)
from analysis.alternative_validation_oracles import close, floats
from analysis.alternative_validation_reference import vector
from analysis.calibration import FloatArray
from analysis.data_io import Json


def energy_variogram(samples: FloatArray, weights: FloatArray, observation: FloatArray,
                     centers: FloatArray, scales: FloatArray) -> tuple[float, float]:
    if np.any(scales < 1) or not np.all(np.isfinite(scales)):
        raise AssertionError("joint scaling lacks original-unit SD floor 1")
    normalized = (samples-centers)/scales
    actual = (observation-centers)/scales
    distances = np.linalg.norm(normalized-actual, axis=1)
    pair_distances = np.linalg.norm(normalized[:, None]-normalized[None, :], axis=2)
    energy = float(np.sum(weights*distances)-
                   np.sum(weights[:, None]*weights[None, :]*pair_distances)/2)
    pairs = tuple(combinations(range(np.size(samples, axis=1)), 2))
    if not pairs:
        raise AssertionError("joint law requires at least two components")
    variogram = math.fsum(
        (math.sqrt(abs(float(actual.take(i)-actual.take(j))))-
         float(np.sum(weights*np.sqrt(np.abs(normalized[:, i]-normalized[:, j])))))**2
        for i, j in pairs)/len(pairs)
    return energy, variogram


def joint_score_checks(output: Path) -> dict[str, Json]:
    rows = csv_records(output / "joint_predictions.csv.gz")
    if not rows:
        raise AssertionError("no saved joint predictions")
    require_columns(rows, ("joint_id", "method_id", "scenario_key", "weights_key",
                           "observations", "centers", "scales", "variables", "thresholds",
                           "ENERGY", "VARIOGRAM", "HOT_DRY_P", "HOT_DRY_BRIER"),
                    "joint original-unit score metadata")
    loaders: list[Callable[..., object]] = [np.load]
    archive = loaders[0](output / "joint_scenarios.npz", allow_pickle=False)
    if not isinstance(archive, np.lib.npyio.NpzFile):
        raise TypeError("joint scenarios must be NPZ")
    scored_events = 0
    with archive as shard:
        for row in rows:
            samples: FloatArray = np.asarray(shard[row["scenario_key"]], dtype=np.float64)
            weights: FloatArray = np.asarray(shard[row["weights_key"]], dtype=np.float64)
            observation = vector(decode(row["observations"]))
            centers, scales = vector(decode(row["centers"])), vector(decode(row["scales"]))
            if weights.shape != (len(samples),) or samples.shape[1:] != observation.shape:
                raise AssertionError("joint scenario/weight/truth dimensions disagree")
            if np.any(weights < 0) or not np.all(np.isfinite(samples)):
                raise AssertionError("invalid joint predictive mass/support")
            close(float(np.sum(weights)), 1, "joint scenario total mass", atol=1e-10)
            energy, variogram = energy_variogram(samples, weights, observation, centers, scales)
            close(float(row["ENERGY"]), energy, "saved standardized energy", atol=1e-7)
            close(float(row["VARIOGRAM"]), variogram, "saved variogram p=.5", atol=1e-7)
            variables = [text(v) for v in sequence(decode(row["variables"]))]
            thresholds = [floats(vector(v)) for v in sequence(decode(row["thresholds"]))]
            if len(variables) != samples.shape[1] or len(thresholds) != len(variables):
                raise AssertionError("joint event component labels mismatch")
            if len(variables) == 2 and set(variables) == {"t15m", "prcp"}:
                temperature, rain = variables.index("t15m"), variables.index("prcp")
                event = ((samples[:, temperature] > thresholds[temperature][1]) &
                         (samples[:, rain] <= thresholds[rain][0]))
                probability = float(np.sum(weights*event))
                occurred = (float(observation.take(temperature)) > thresholds[temperature][1]
                            and float(observation.take(rain)) <= thresholds[rain][0])
                close(float(row["HOT_DRY_P"]), probability, "hot/dry event probability")
                close(float(row["HOT_DRY_BRIER"]), (probability-float(occurred))**2,
                      "hot/dry event Brier")
                scored_events += 1
            elif row["HOT_DRY_P"] or row["HOT_DRY_BRIER"]:
                raise AssertionError("hot/dry event reported on unsupported joint component key")
    return {"status": "PASS", "energy_variogram_records": len(rows),
            "hot_dry_records": scored_events}
