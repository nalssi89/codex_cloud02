"""Joint scope from actual component manifests and aligned annual climatology."""

from __future__ import annotations

import json
import math
from collections.abc import Callable, Sequence
from itertools import combinations
from pathlib import Path

import numpy as np

from analysis.alternative_experiment_types import ExperimentInputs
from analysis.alternative_reporting_common import (
    Row,
    decode,
    identity,
    mask_hash,
    mean,
    method,
    number,
    string_list,
    text,
)
from analysis.alternative_reporting_fairness import FAILURES, indexed


def metadata(records: Sequence[Row], schedule: Sequence[Row],
             inputs: ExperimentInputs) -> list[Row]:
    catalog = {case.case_id: case for case in inputs.cases}
    planned = indexed([r for r in schedule if text(r, "surface") == "joint"])
    result: list[Row] = []
    for original in records:
        row = dict(original)
        plan = planned.get((identity(row), method(row)), {})
        wire = text(row, "component_case_ids") or text(plan, "component_case_ids")
        if not wire:
            raise ValueError(f"No actual joint component manifest: {identity(row)}/{method(row)}")
        ids = string_list(decode(wire))
        cases = [catalog[i] for i in ids]
        if len(cases) < 2 or len({c.product for c in cases}) != 1:
            raise ValueError("Invalid or product-mixed joint component scope")
        first = min(c.valid_start for c in cases)
        row.update({
            "component_case_ids": json.dumps(ids, separators=(",", ":")),
            "PRODUCT": cases[0].product,
            "VARIABLE": json.dumps([f"{c.variable}:{c.lead}" for c in cases], separators=(",", ":")),
            "component_windows": json.dumps([[c.valid_start.isoformat(), c.valid_end.isoformat()]
                                            for c in cases], separators=(",", ":")),
            "YEAR": first.year, "VALID_MONTH": first.month,
            "SEASON": ("DJF", "MAM", "JJA", "SON")[(first.month % 12)//3],
            "LEAD": json.dumps([c.lead for c in cases], separators=(",", ":")),
            "VALID_START": first.isoformat(),
            "VALID_END": max(c.valid_end for c in cases).isoformat(),
        })
        result.append(row)
    return result


def climate(inputs: ExperimentInputs, status: Row) -> Row:
    """Empirical whole annual vectors, not independent scalar resampling."""
    ids = string_list(decode(text(status, "component_case_ids")))
    histories = [{row.source_year: row.observation for row in inputs.historical[i]} for i in ids]
    years = set(histories[0])
    for history in histories[1:]:
        years.intersection_update(history)
    if len(years) < 2:
        raise ValueError("Joint climatology has fewer than two aligned annual vectors")
    samples = np.asarray([[h[year] for h in histories] for year in sorted(years)], dtype=np.float64)
    observations = np.asarray([inputs.truths[i].observation for i in ids], dtype=np.float64)
    centers = np.asarray(np.mean(samples, axis=0), dtype=np.float64)
    scales = np.maximum(1., np.std(samples, axis=0, ddof=1))
    standardized = (samples-centers)/scales
    actual = (observations-centers)/scales
    energy = float(np.mean(np.linalg.norm(standardized-actual, axis=1)) -
                   .5*np.mean(np.linalg.norm(standardized[:, None]-standardized[None, :], axis=2)))
    pairs = list(combinations(range(len(ids)), 2))
    variogram = math.fsum(
        (math.sqrt(abs(float(actual.item(i))-float(actual.item(j)))) -
         float(np.mean(np.sqrt(np.abs(standardized[:, i]-standardized[:, j])))))**2
        for i, j in pairs)/len(pairs)
    result: Row = {"ENERGY": energy, "VARIOGRAM": variogram}
    catalog = {c.case_id: c for c in inputs.cases}
    variables = [catalog[i].variable for i in ids]
    if len(ids) == 2 and set(variables) == {"t15m", "prcp"}:
        t, p = variables.index("t15m"), variables.index("prcp")
        high = float(inputs.truths[ids[t]].thresholds.item(1))
        low = float(inputs.truths[ids[p]].thresholds.item(0))
        probability = float(np.mean((samples[:, t] > high) & (samples[:, p] <= low)))
        event = float(observations.item(t) > high and observations.item(p) <= low)
        result["HOT_DRY_BRIER"] = (probability-event)**2
    return result


def policies(inputs: ExperimentInputs, predictions: Sequence[Row], statuses: Sequence[Row],
             counts: Sequence[Row], scores: tuple[str, ...]) -> tuple[list[Row], list[Row]]:
    saved, ledger = indexed(predictions), indexed(statuses)
    result: list[Row] = []
    details: list[Row] = []
    for count in counts:
        if text(count, "surface") != "joint":
            continue
        method_id = method(count)
        ids = string_list(decode(text(count, "eligible_ids")))
        for score in scores:
            if score == "HOT_DRY_BRIER":
                labels = string_list(decode(text(count, "VARIABLE")))
                if len(labels) != 2 or {label.split(":")[0] for label in labels} != {"t15m", "prcp"}:
                    continue
            values: list[float] = []
            successes: list[float] = []
            fallback = 0
            missing = 0
            for joint_id in ids:
                status = ledger[(joint_id, method_id)]
                state = text(status, "status")
                value = number(saved.get((joint_id, method_id), {}), score) if state == "OK" else None
                source = "method"
                if value is None and state in FAILURES | {"OK"}:
                    value = number(climate(inputs, status), score)
                    source = "climatology_on_failure"
                    fallback += int(value is not None)
                elif value is not None:
                    successes.append(value)
                if value is None:
                    missing += 1
                    continue
                values.append(value)
                details.append({"joint_id": joint_id, "method_id": method_id,
                                "score": score, "loss": value, "source": source,
                                "original_status": state,
                                "component_case_ids": status["component_case_ids"]})
            result.append({"PRODUCT": count["PRODUCT"], "VARIABLE": count["VARIABLE"],
                           "surface": "joint", "method_id": method_id, "score": score,
                           "policy": f"{method_id}+climatology_on_failure",
                           "eligible_count": len(ids), "scored_count": len(values),
                           "fallback_count": fallback, "mean_loss": mean(values) if not missing else None,
                           "policy_status": "COMPLETE" if not missing else "INCOMPLETE",
                           "lower_bound": math.fsum(successes)/len(ids) if ids else None,
                           "upper_bound": "+inf", "bound_label": "nonnegative missing-loss bound",
                           "eligible_mask_hash": mask_hash(ids),
                           "climatology": "same aligned outer annual vectors; whole-vector empirical law"})
    return result, details


def scalar_case_coverage(inputs: ExperimentInputs, statuses: Sequence[Row]) -> list[Row]:
    """Retain unavailable/incomplete component IDs without calling them vector predictions."""
    counts: dict[tuple[str, str, str, str], int] = {}
    catalog = {case.case_id: case for case in inputs.cases}
    for row in statuses:
        if text(row, "surface") != "joint":
            continue
        case = catalog[identity(row)]
        key = case.product, case.variable, method(row), text(row, "status")
        counts[key] = counts.get(key, 0)+1
    return [{"PRODUCT": p, "VARIABLE": v, "method_id": m, "status": s, "count": n,
             "surface": "joint_component_coverage_not_vector_score"}
            for (p, v, m, s), n in sorted(counts.items())]


def inspect_scenarios(output: Path, predictions: Sequence[Row]) -> list[Row]:
    """Inspect actual saved finite arrays without replacing analytic marginals."""
    path = output / "joint_scenarios.npz"
    if not path.exists():
        return [{"status": "MISSING", "artifact": path.name}] if predictions else []
    loaders: list[Callable[..., object]] = [np.load]
    archive = loaders[0](path, allow_pickle=False)
    if not isinstance(archive, np.lib.npyio.NpzFile):
        raise TypeError("Joint arrays must be saved NPZ")
    records: list[Row] = []
    with archive as shard:
        for row in predictions:
            samples = np.asarray(shard[text(row, "scenario_key")], dtype=np.float64)
            weights = np.asarray(shard[text(row, "weights_key")], dtype=np.float64)
            components = string_list(decode(text(row, "component_case_ids")))
            valid = (samples.ndim == 2 and samples.shape[1] == len(components)
                     and weights.shape == (len(samples),) and bool(np.all(np.isfinite(samples)))
                     and bool(np.all(np.isfinite(weights))) and bool(np.all(weights >= 0))
                     and abs(float(np.sum(weights))-1) <= 1e-9)
            records.append({"joint_id": identity(row), "method_id": method(row),
                            "status": "OK" if valid else "ERROR_INVALID_SCENARIOS",
                            "scenario_count": len(samples), "dimension": len(components),
                            "total_mass": float(np.sum(weights)),
                            "approximation_metadata": text(row, "approximation_metadata"),
                            "component_case_ids": text(row, "component_case_ids"),
                            "representation": "actual finite scenario law; analytic references separate"})
    return records
