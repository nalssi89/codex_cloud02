"""Actual eligibility, restricted masks and separately issued fallback policies."""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from collections.abc import Sequence
from itertools import combinations

import numpy as np

from analysis.alternative_experiment_types import ExperimentInputs
from analysis.alternative_registry import method_registry
from analysis.alternative_reporting_common import (
    Row,
    decode,
    identity,
    mask_hash,
    mean,
    method,
    number,
    scope,
    string_list,
    text,
)
from analysis.scoring import empirical_crps, probability_scores, tercile_probabilities

GATES = frozenset({"GATED_DATA", "NOT_APPLICABLE_DOMAIN", "INSUFFICIENT_TRAINING",
                   "INSUFFICIENT_INNER_FOLDS"})
FAILURES = frozenset({"FIT_FAILED", "POSTERIOR_DIAGNOSTICS_FAILED",
                      "NUMERICAL_DISTRIBUTION_FAILED", "SCORE_FAILED"})


def indexed(records: Sequence[Row]) -> dict[tuple[str, str], Row]:
    result: dict[tuple[str, str], Row] = {}
    for row in records:
        key = identity(row), method(row)
        if key in result:
            raise ValueError(f"Duplicate reporting identity: {key}")
        result[key] = row
    return result


def coverage(inputs: ExperimentInputs, statuses: Sequence[Row],
             predictions: Sequence[Row], selected: set[str]) -> list[Row]:
    ledger, scored = indexed(statuses), indexed(predictions)
    result: list[Row] = []
    for spec in method_registry():
        if spec.id not in selected or spec.surface == "joint":
            continue
        groups: dict[tuple[str, str], list[str]] = defaultdict(list)
        for case in inputs.cases:
            groups[(case.product, case.variable)].append(case.case_id)
        for (product, variable), ids in sorted(groups.items()):
            domain = spec.domain == "both" or (
                spec.domain == "temperature" and variable == "t15m") or (
                spec.domain == "precipitation" and variable == "prcp")
            counts: Counter[str] = Counter()
            eligible: list[str] = []
            successes: list[str] = []
            for case_id in ids:
                state = text(ledger.get((case_id, spec.id), {}), "status") or "UNRECORDED"
                counts[state] += 1
                if not domain or state in GATES or case_id not in inputs.truths:
                    continue
                eligible.append(case_id)
                if state == "OK" and (case_id, spec.id) in scored:
                    successes.append(case_id)
            result.append({
                "PRODUCT": product, "VARIABLE": variable, "method_id": spec.id,
                "surface": spec.surface, "family_no": spec.family_no,
                "supplied_count": len(ids), "domain_eligible_count": len(ids) if domain else 0,
                "scientific_gates": sum(counts[g] for g in GATES),
                "missing_targets": sum(case_id not in inputs.truths for case_id in ids) if domain else 0,
                "eligible_count": len(eligible), "scored_count": len(successes),
                "fit_failures": counts["FIT_FAILED"]+counts["POSTERIOR_DIAGNOSTICS_FAILED"],
                "numerical_or_score_failures": counts["NUMERICAL_DISTRIBUTION_FAILED"]+counts["SCORE_FAILED"],
                "scientific_support_gates": counts["INSUFFICIENT_TRAINING"]+counts["INSUFFICIENT_INNER_FOLDS"],
                "input_conflicts": counts["INPUT_CONFLICT"],
                "score_missing_after_OK": sum(text(ledger.get((i, spec.id), {}), "status") == "OK"
                                              and (i, spec.id) not in scored for i in eligible),
                "unrecorded_count": counts["UNRECORDED"],
                "success_fraction": len(successes) / len(eligible) if eligible else None,
                "eligible_ids": json.dumps(sorted(eligible), separators=(",", ":")),
                "success_mask_hash": mask_hash(successes),
                "status_counts": json.dumps(dict(sorted(counts.items())), sort_keys=True),
            })
    # Joint eligibility is its vector status universe, never a guessed scalar denominator.
    joint_groups: dict[tuple[str, str, str], list[Row]] = defaultdict(list)
    for row in statuses:
        if text(row, "surface") == "joint":
            product, variable = scope(row)
            joint_groups[(product, variable, method(row))].append(row)
    for (product, variable, method_id), records in sorted(joint_groups.items()):
        counts = Counter(text(r, "status") for r in records)
        eligible_ids = [identity(r) for r in records if text(r, "status") not in
                        GATES | {"TARGET_UNAVAILABLE"}]
        success_ids = [i for i in eligible_ids if (i, method_id) in scored and
                       text(ledger[(i, method_id)], "status") == "OK"]
        result.append({"PRODUCT": product, "VARIABLE": variable, "method_id": method_id,
                       "surface": "joint", "supplied_count": len(records),
                       "domain_eligible_count": len(records)-counts["NOT_APPLICABLE_DOMAIN"],
                       "scientific_gates": sum(counts[g] for g in GATES),
                       "missing_targets": counts["TARGET_UNAVAILABLE"],
                       "eligible_count": len(eligible_ids), "scored_count": len(success_ids),
                       "fit_failures": counts["FIT_FAILED"]+counts["POSTERIOR_DIAGNOSTICS_FAILED"],
                       "numerical_or_score_failures": counts["NUMERICAL_DISTRIBUTION_FAILED"]+counts["SCORE_FAILED"],
                       "scientific_support_gates": counts["INSUFFICIENT_TRAINING"]+counts["INSUFFICIENT_INNER_FOLDS"],
                       "input_conflicts": counts["INPUT_CONFLICT"],
                       "family_no": next(spec.family_no for spec in method_registry()
                                         if spec.id == method_id.split("__")[0]),
                       "unrecorded_count": 0, "eligible_ids": json.dumps(sorted(eligible_ids)),
                       "success_fraction": len(success_ids)/len(eligible_ids) if eligible_ids else None,
                       "success_mask_hash": mask_hash(success_ids),
                       "status_counts": json.dumps(dict(sorted(counts.items())))})
    return result


def common_masks(predictions: Sequence[Row], counts: Sequence[Row],
                 scores: tuple[str, ...], surface: str) -> tuple[list[Row], list[Row]]:
    by_scope: dict[tuple[str, str], dict[str, dict[str, Row]]] = defaultdict(dict)
    for row in predictions:
        by_scope[scope(row)].setdefault(method(row), {})[identity(row)] = row
    for row in counts:
        if text(row, "surface") == surface and (number(row, "domain_eligible_count") or 0) > 0:
            _ = by_scope[scope(row)].setdefault(method(row), {})
    family_by_id = {spec.id: spec.family_no for spec in method_registry()}
    comparisons: list[Row] = []
    masks: list[Row] = []
    for (product, variable), methods in sorted(by_scope.items()):
        sets: list[tuple[str, tuple[str, ...]]] = [
            ("pairwise", pair) for pair in combinations(sorted(methods), 2)]
        families: dict[int, list[str]] = defaultdict(list)
        for method_id in sorted(methods):
            families[family_by_id[method_id.split("__")[0]]].append(method_id)
        sets.extend((f"family_{family}", tuple(ids)) for family, ids in sorted(families.items()))
        for label, ids in sets:
            common = set(methods[ids[0]])
            for method_id in ids[1:]:
                common.intersection_update(methods[method_id])
            mask = mask_hash(common)
            masks.append({"PRODUCT": product, "VARIABLE": variable, "surface": surface,
                          "mask_kind": label, "methods": json.dumps(ids), "N": len(common),
                          "mask_hash": mask, "case_ids": json.dumps(sorted(common))})
            for score in scores:
                # A score-specific missing value cannot silently shrink a mask.
                values = [[number(methods[i][case], score) for case in sorted(common)] for i in ids]
                if any(v is None for column in values for v in column):
                    continue
                means = [mean([v for v in column if v is not None]) for column in values]
                for method_id, average in zip(ids, means, strict=True):
                    comparisons.append({"PRODUCT": product, "VARIABLE": variable,
                                        "surface": surface, "mask_kind": label,
                                        "methods": json.dumps(ids), "method_id": method_id,
                                        "score": score, "N": len(common), "mask_hash": mask,
                                        "mean_loss": average,
                                        "delta_first_minus_second":
                                            means[0]-means[1] if len(ids) == 2 and
                                            means[0] is not None and means[1] is not None else None})
    return comparisons, masks


def climate_loss(inputs: ExperimentInputs, case_id: str, score: str) -> float:
    truth = inputs.truths[case_id]
    if score == "CRPS":
        return empirical_crps(truth.historical_observations, truth.observation)
    probabilities = tercile_probabilities(truth.historical_observations, truth.thresholds)
    category = int(truth.observation > float(truth.thresholds.item(0))) + int(
        truth.observation > float(truth.thresholds.item(1)))
    event = np.asarray([float(i == category) for i in range(3)], dtype=np.float64)
    brier, rps = probability_scores(probabilities, event)
    return brier if score == "BRIER" else rps


def policies(inputs: ExperimentInputs, predictions: Sequence[Row], statuses: Sequence[Row],
             counts: Sequence[Row]) -> tuple[list[Row], list[Row]]:
    scored, ledger = indexed(predictions), indexed(statuses)
    output: list[Row] = []
    details: list[Row] = []
    for count in counts:
        surface = text(count, "surface")
        method_id = method(count)
        ids = string_list(decode(text(count, "eligible_ids")))
        for score in (("CRPS", "BRIER", "RPS") if surface == "continuous" else ("BRIER", "RPS")):
            values: list[float] = []
            success_losses: list[float] = []
            missing = 0
            fallback = 0
            for case_id in ids:
                state = text(ledger.get((case_id, method_id), {}), "status")
                value = number(scored.get((case_id, method_id), {}), score) if state == "OK" else None
                source = "method"
                if value is None:
                    if state not in FAILURES and state != "OK":
                        missing += 1
                        continue
                    value = climate_loss(inputs, case_id, score)
                    source = "climatology_on_failure"
                    fallback += 1
                else:
                    success_losses.append(value)
                if value < -1e-10:
                    raise ValueError(f"Negative nonnegative loss: {case_id}/{method_id}/{score}")
                values.append(value)
                details.append({"case_id": case_id, "method_id": method_id,
                                "policy": f"{method_id}+climatology_on_failure",
                                "score": score, "loss": value, "source": source,
                                "original_status": state})
            output.append({"PRODUCT": count["PRODUCT"], "VARIABLE": count["VARIABLE"],
                           "surface": surface, "method_id": method_id, "score": score,
                           "policy": f"{method_id}+climatology_on_failure",
                           "eligible_count": len(ids), "scored_count": len(values),
                           "fallback_count": fallback,
                           "policy_status": "COMPLETE" if not missing else "INCOMPLETE",
                           "mean_loss": mean(values) if not missing else None,
                           "lower_bound": math.fsum(success_losses)/len(ids) if ids else None,
                           "upper_bound": "+inf", "bound_label": "nonnegative missing-loss bound",
                           "eligible_mask_hash": mask_hash(ids)})
    return output, details
