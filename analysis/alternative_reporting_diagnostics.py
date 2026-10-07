"""Atom-aware PIT, common thresholds, intervals and fixed outer-P90 rain events."""

from __future__ import annotations

import gzip
import hashlib
from collections import defaultdict
from pathlib import Path

import numpy as np

from analysis.alternative_distributions import distribution_from_spec
from analysis.alternative_experiment_types import ExperimentInputs
from analysis.alternative_reporting_common import (
    Row,
    decode,
    identity,
    method,
    number,
    scope,
)
from analysis.alternative_reporting_statistics import SEED
from analysis.data_io import Json


def diagnostics(output: Path, inputs: ExperimentInputs,
                predictions: list[Row]) -> tuple[list[Row], list[Row]]:
    laws: dict[tuple[str, str], dict[str, Json]] = {}
    path = output / "distribution_specs.jsonl.gz"
    if path.exists():
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            for line in handle:
                item = decode(line)
                if not isinstance(item, dict):
                    raise TypeError("Law record is not an object")
                # Keep JSON objects, not a numerical surrogate of an analytic law.
                laws[(str(item["case_id"]), str(item["method_id"]))] = dict(item)
    result: list[Row] = []
    checks: list[Row] = []
    for row in predictions:
        case_id, method_id = identity(row), method(row)
        truth = inputs.truths.get(case_id)
        if truth is None:
            raise ValueError(f"Scored row without eligible truth: {case_id}")
        product, variable = scope(row)
        threshold_ok = (number(row, "Q33") == float(truth.thresholds.item(0)) and
                        number(row, "Q67") == float(truth.thresholds.item(1)))
        checks.append({"case_id": case_id, "method_id": method_id,
                       "threshold_status": "MATCH" if threshold_ok else "MISMATCH"})
        record: Row = {"case_id": case_id, "method_id": method_id,
                       "PRODUCT": product, "VARIABLE": variable, "seed": SEED,
                       "law_status": "MISSING", "PIT": None,
                       "PIT_left": None, "PIT_right": None,
                       "UPPER_RAIN_THRESHOLD": None, "UPPER_RAIN_P": None,
                       "UPPER_RAIN_BRIER": None, "CONTRACT_COVERAGE90": None,
                       "CONTRACT_WIDTH90": None, "representation": ""}
        saved = laws.get((case_id, method_id))
        if saved is not None:
            wire = saved.get("distribution")
            if not isinstance(wire, dict):
                raise ValueError(f"Missing distribution object: {case_id}/{method_id}")
            try:
                law = distribution_from_spec(wire)
                point = np.asarray([truth.observation], dtype=np.float64)
                left, right = float(law.cdf_left(point).item(0)), float(law.cdf(point).item(0))
                digest = hashlib.sha256(f"{SEED}/report_pit/{case_id}/{method_id}".encode())
                u = int.from_bytes(digest.digest()[:8], "big") / 18446744073709551616
                quantiles = law.quantile(np.asarray([.05, .95], dtype=np.float64))
                record.update({"law_status": "OK", "PIT": left+u*(right-left),
                               "PIT_left": left, "PIT_right": right,
                               "CONTRACT_COVERAGE90": int(float(quantiles.item(0)) <= truth.observation
                                                          <= float(quantiles.item(1))),
                               "CONTRACT_WIDTH90": float(quantiles.item(1))-float(quantiles.item(0)),
                               "representation": str(wire.get("tag", wire.get("kind", "")))})
                if variable == "prcp":
                    threshold = float(np.quantile(truth.historical_observations, .9))
                    probability = 1-float(law.cdf(np.asarray([threshold], dtype=np.float64)).item(0))
                    record.update({"UPPER_RAIN_THRESHOLD": threshold, "UPPER_RAIN_P": probability,
                                   "UPPER_RAIN_BRIER": (probability-float(truth.observation > threshold))**2})
            except (ValueError, RuntimeError, ArithmeticError) as error:
                record["law_status"] = f"ERROR:{type(error).__name__}:{error}"
        result.append(record)
    return result, checks


def reliability(predictions: list[Row], surface: str) -> list[Row]:
    groups: dict[tuple[str, str, str, str, int], list[tuple[float, float]]] = defaultdict(list)
    for row in predictions:
        product, variable = scope(row)
        observation, low, high = number(row, "OBS"), number(row, "Q33"), number(row, "Q67")
        if observation is None or low is None or high is None:
            raise ValueError("Missing observed category or common thresholds")
        actual = int(observation > low)+int(observation > high)
        for category, label in enumerate(("BN", "NN", "AN")):
            probability = number(row, f"P_{label}")
            if probability is None:
                raise ValueError("Missing category probability")
            if not 0 <= probability <= 1:
                raise ValueError("Invalid category probability")
            index = min(9, int(probability*10))
            groups[(product, variable, method(row), label, index)].append((probability, float(category == actual)))
    result: list[Row] = []
    for (product, variable, method_id, label, index), values in sorted(groups.items()):
        result.append({"PRODUCT": product, "VARIABLE": variable, "method_id": method_id,
                       "surface": surface, "category": label, "bin_low": index/10,
                       "bin_high": (index+1)/10, "N": len(values),
                       "mean_probability": sum(p for p, _ in values)/len(values),
                       "observed_frequency": sum(event for _, event in values)/len(values),
                       "bin_rule": "fixed tenths, last includes 1; no target tuning"})
    return result
