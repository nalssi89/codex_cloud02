#!/usr/bin/env python
"""Independent, read-only-input QM/QDM audit; writes one method-review JSON.

Run: .venv/Scripts/python.exe -B analysis/audit_qm_qdm.py
Run only after core outputs have been rebuilt from the selected observation source:
daily station count >=50, means over actual contributors (including
61/60), no 62/n scaling or raw-station imputation. Case scope comes from outputs;
independent observation-policy/calendar validation belongs to audit_training.py.
No production empirical-distribution, interpolation or ranking routines are used
by the oracle. Only adversarial probes call production calibrate for comparison.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
import sys
from bisect import bisect_right
from collections import Counter, defaultdict
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass, field
from decimal import Decimal, localcontext
from importlib.metadata import version
from itertools import pairwise
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analysis.data_io import observation_daily_path, observation_provenance
from analysis.validate_results import day, observation_summary, parse_daily

type Json = str | int | float | bool | None | list[Json] | dict[str, Json]
type Curve = tuple[list[float], list[float]]
TOL = 1e-10
PROBES = (0.0, 0.05, 0.25, 0.5, 0.75, 0.95, 1.0)
METHODS = ("RAW", "QM", "QDM")


def rows(path: Path) -> Iterator[dict[str, str]]:
    """Stream dictionaries, retaining only compact keyed numerical inputs."""
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as handle:
        yield from csv.DictReader(handle)


def curve(years: Sequence[Sequence[float]]) -> Curve:
    """Merge exact ties, allocating exactly one equal share to each year."""
    masses: dict[float, list[float]] = defaultdict(list)
    for year in years:
        counts = Counter(year)
        for value, count in counts.items():
            masses[value].append(count / len(year) / len(years))
    values = sorted(masses)
    mass = [math.fsum(masses[value]) for value in values]
    total = math.fsum(mass)
    positions = [(math.fsum(mass[:i]) + m / 2) / total for i, m in enumerate(mass)]
    return values, positions


def sequential_curve(years: Sequence[Sequence[float]]) -> Curve:
    """Independent scalar replay of the production cumulative-mass operation order."""
    pairs = sorted(
        (value, 1.0 / (len(years) * len(year))) for year in years for value in year
    )
    cumulative = 0.0
    end_mass: dict[float, float] = {}
    for value, weight in pairs:
        cumulative += weight
        end_mass[value] = cumulative
    values = sorted(end_mass)
    mass: list[float] = []
    previous = 0.0
    for value in values:
        mass.append(end_mass[value] - previous)
        previous = end_mass[value]
    total = float(np.sum(np.asarray(mass, dtype=np.float64)))
    cumulative = 0.0
    positions: list[float] = []
    for weight in mass:
        normalized = weight / total
        cumulative += normalized
        positions.append(cumulative - normalized / 2)
    return values, positions


def linear(x: float, nodes: Sequence[float], values: Sequence[float]) -> float:
    """Scalar binary-search interpolation, with explicit clipped endpoints."""
    if x <= nodes[0]:
        return values[0]
    if x >= nodes[-1]:
        return values[-1]
    right = bisect_right(nodes, x)
    left = right - 1
    weight = (x - nodes[left]) / (nodes[right] - nodes[left])
    return values[left] + weight * (values[right] - values[left])


def midranks(values: Sequence[float]) -> list[float]:
    counts = Counter(values)
    previous = 0
    ranks: dict[float, float] = {}
    for value in sorted(counts):
        ranks[value] = (previous + counts[value] / 2) / len(values)
        previous += counts[value]
    return [ranks[value] for value in values]


def quantiles(values: Sequence[float], probabilities: Sequence[float]) -> list[float]:
    """Issued marginal quantiles: member-midpoint linear, retaining tied atoms."""
    ordered = sorted(values)
    positions = [(i + 0.5) / len(values) for i in range(len(values))]
    return [linear(p, positions, ordered) for p in probabilities]


@dataclass(frozen=True)
class Oracle:
    qm: list[float]
    qdm: list[float]
    p: list[float]
    qo: list[float]
    qh: list[float]
    historical: Curve


def oracle(
    raw: Sequence[float], years: Sequence[Sequence[float]],
    observed: Sequence[float], rain: bool,
    distribution: Callable[[Sequence[Sequence[float]]], Curve] = curve,
) -> Oracle:
    hx, hp = distribution(years)
    ox, op = distribution([[value] for value in observed])
    p = midranks(raw)
    qo = [linear(probability, op, ox) for probability in p]
    qh = [linear(probability, hp, hx) for probability in p]
    qm = [linear(linear(value, hx, hp), op, ox) for value in raw]
    qdm = [
        max(0.0, o if h < 0.1 else value * o / h) if rain else value + o - h
        for value, o, h in zip(raw, qo, qh, strict=True)
    ]
    return Oracle(qm, qdm, p, qo, qh, (hx, hp))


def maximum_error(left: Sequence[float], right: Sequence[float]) -> float:
    return max(abs(a - b) for a, b in zip(left, right, strict=True))


def numbers(values: Sequence[float]) -> list[Json]:
    return [value for value in values]


def hashes(root: Path, paths: Sequence[Path]) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in paths:
        with path.open("rb") as handle:
            result[path.relative_to(root).as_posix()] = hashlib.file_digest(handle, "sha256").hexdigest()
    return result


def decimal_qdm(
    value: float, p: float, years: list[list[float]], observations: list[float], rain: bool,
) -> float:
    """50-digit independent check of a flagged member; floats interpreted exactly."""
    with localcontext() as context:
        context.prec = 50

        def inverse(samples: list[list[float]]) -> Decimal:
            masses: dict[float, Decimal] = defaultdict(Decimal)
            for year in samples:
                for number in year:
                    masses[number] += Decimal(1) / (len(samples) * len(year))
            values = sorted(masses)
            positions: list[Decimal] = []
            cumulative = Decimal(0)
            for number in values:
                positions.append(cumulative + masses[number] / 2)
                cumulative += masses[number]
            probability = Decimal.from_float(p)
            if probability <= positions[0]:
                return Decimal.from_float(values[0])
            if probability >= positions[-1]:
                return Decimal.from_float(values[-1])
            right = bisect_right(positions, probability)
            fraction = (probability - positions[right - 1]) / (positions[right] - positions[right - 1])
            left_value = Decimal.from_float(values[right - 1])
            return left_value + fraction * (Decimal.from_float(values[right]) - left_value)

        h, o = inverse(years), inverse([[v] for v in observations])
        x = Decimal.from_float(value)
        return float((o if h < Decimal("0.1") else x * o / h) if rain else x + o - h)


@dataclass
class Summary:
    cases: int = 0
    members: int = 0
    counts: Counter[str] = field(default_factory=Counter)
    maxima: dict[str, float] = field(default_factory=dict)
    minima: dict[str, float] = field(default_factory=dict)
    totals: dict[str, float] = field(default_factory=dict)
    examples: dict[str, Json] = field(default_factory=dict)

    def extreme(self, name: str, value: float, example: Json = None) -> None:
        if name not in self.maxima or value > self.maxima[name]:
            self.maxima[name] = value
            if example is not None:
                self.examples[name] = example
        self.minima[name] = min(self.minima.get(name, value), value)

    def json(self) -> dict[str, Json]:
        return {
            "cases": self.cases, "members": self.members,
            "counts": dict(self.counts), "maxima": dict(self.maxima),
            "minima": dict(self.minima), "totals": dict(self.totals),
            "extreme_examples": self.examples,
            "mean_case_quantile_grid": {
                method: [self.totals[f"{method}_quantile_{p}_sum"] / self.cases for p in PROBES]
                for method in METHODS
            },
        }


def endpoints(
    key: str, years: list[list[float]], observed: list[float],
    saved: dict[str, list[float]], expected: Oracle, rain: bool, summary: Summary,
) -> dict[str, Json]:
    """Audit endpoint *midposition*, not CDF-zero/one, and deterministic atoms."""
    hx, hp = expected.historical
    ox, op = curve([[v] for v in observed])
    detail: dict[str, Json] = {}
    for side, index in (("lower", 0), ("upper", -1)):
        mapped = linear(hp[index], op, ox)
        gap = abs(mapped - ox[index])
        at = [i for i, x in enumerate(saved["RAW"]) if x == hx[index]]
        outside = [i for i, x in enumerate(saved["RAW"])
                   if (x < hx[index] if index == 0 else x > hx[index])]
        mass = math.fsum(year.count(hx[index]) / len(year) for year in years) / len(years)
        example: dict[str, Json] = {
            "case_id": key, "side": side, "historical_endpoint": hx[index],
            "historical_endpoint_tie_mass": mass, "clipped_probability": hp[index],
            "observed_endpoint": ox[index], "mapped_endpoint": mapped, "absolute_gap": gap,
            "raw_outside_members": len(outside), "raw_at_endpoint_members": len(at),
        }
        if outside:
            i = outside[0]
            example["outside_member_example"] = {
                "member_index": i + 1, "raw": saved["RAW"][i], "saved_qm": saved["QM"][i],
            }
        if at:
            i = at[0]
            example["endpoint_member_example"] = {
                "member_index": i + 1, "raw": saved["RAW"][i], "saved_qm": saved["QM"][i],
            }
        summary.counts[f"{side}_clipped_endpoint_differs_observed_endpoint_cases"] += int(gap > TOL)
        summary.counts[f"{side}_outside_range_non_observed_endpoint_cases"] += int(
            bool(outside) and gap > TOL
        )
        summary.counts[f"{side}_outside_range_non_observed_endpoint_members"] += (
            len(outside) if gap > TOL else 0
        )
        summary.counts[f"{side}_at_range_endpoint_non_observed_endpoint_cases"] += int(
            bool(at) and gap > TOL
        )
        summary.counts[f"{side}_at_range_endpoint_non_observed_endpoint_members"] += (
            len(at) if gap > TOL else 0
        )
        summary.extreme(f"{side}_endpoint_mapping_gap", gap, example)
        if outside:
            summary.extreme(f"{side}_actual_outside_mapping_gap", gap, example)
        if at:
            summary.extreme(f"{side}_actual_at_endpoint_mapping_gap", gap, example)
        detail[side] = example
    if rain:
        zero_rates = {
            "historical_equal_year": math.fsum(year.count(0.0) / len(year) for year in years) / len(years),
            "observed_equal_year": observed.count(0.0) / len(observed),
            **{method: values.count(0.0) / len(values) for method, values in saved.items()},
        }
        zero_example: dict[str, Json] = {"case_id": key, **zero_rates}
        for name, rate in zero_rates.items():
            summary.extreme(f"zero_mass_{name}", rate, zero_example)
            summary.counts[f"zero_mass_{name}_positive_cases"] += int(rate > 0)
            summary.totals[f"zero_mass_{name}_sum"] = (
                summary.totals.get(f"zero_mass_{name}_sum", 0.0) + rate
            )
        for method in METHODS:
            difference = abs(zero_rates[method] - zero_rates["observed_equal_year"])
            summary.counts[f"{method}_zero_mass_differs_observed_cases"] += int(difference > TOL)
            summary.extreme(f"{method}_zero_mass_observed_gap", difference, zero_example)
        detail["zero_masses"] = dict(zero_rates)
    return detail


def diagnose(
    key: str, raw: list[float], saved: dict[str, list[float]], expected: Oracle,
    observed: list[float], rain: bool, summary: Summary,
) -> dict[str, Json]:
    """Count crossings in RAW order and distribution-level change discrepancies."""
    summary.cases += 1
    summary.members += len(raw)
    order = sorted(range(len(raw)), key=raw.__getitem__)
    record: dict[str, Json] = {"case_id": key}
    summary.counts["raw_tied_members_beyond_first"] += len(raw) - len(set(raw))
    summary.counts["raw_tied_cases"] += int(len(raw) != len(set(raw)))
    for method in METHODS:
        values = saved[method]
        y = np.asarray([values[i] for i in order], dtype=np.float64)
        differences = np.diff(y)
        adjacent = int(np.count_nonzero(differences < -TOL))
        exact_adjacent = int(np.count_nonzero(differences < 0))
        # At most 84 forecast members; all pair inversions are inexpensive.
        pair_diff = np.triu(y[:, None] - y[None, :], k=1)
        inversions = int(np.count_nonzero(pair_diff > TOL))
        summary.counts[f"{method}_crossing_cases"] += int(adjacent > 0)
        summary.counts[f"{method}_crossing_cases_all_raw_positive"] += int(
            adjacent > 0 and all(x > 0 for x in raw)
        )
        summary.counts[f"{method}_crossing_cases_all_corrected_positive"] += int(
            adjacent > 0 and all(x > 0 for x in values)
        )
        summary.counts[f"{method}_adjacent_crossings"] += adjacent
        summary.counts[f"{method}_exact_negative_adjacent"] += exact_adjacent
        summary.counts[f"{method}_pair_inversions"] += inversions
        summary.counts[f"{method}_adjacent_ties"] += sum(float(v) == 0 for v in differences.flat)
        summary.counts[f"{method}_tied_cases"] += int(len(values) != len(set(values)))
        summary.counts[f"{method}_negative_members"] += sum(value < 0 for value in values)
        summary.counts[f"{method}_positive_cases"] += int(all(value > 0 for value in values))
        summary.counts[f"{method}_below_training_observation_range"] += sum(
            value < min(observed) - TOL for value in values
        )
        summary.counts[f"{method}_above_training_observation_range"] += sum(
            value > max(observed) + TOL for value in values
        )
        summary.extreme(f"{method}_member_min", min(values), key)
        summary.extreme(f"{method}_member_max", max(values), key)
        fall = max(0.0, -float(np.min(differences)))
        summary.extreme(f"{method}_adjacent_fall", fall, key)
        summary.extreme(f"{method}_pair_fall", float(np.max(pair_diff)), key)
        grid = quantiles(values, PROBES)
        for p, value in zip(PROBES, grid, strict=True):
            name = f"{method}_quantile_{p}_sum"
            summary.totals[name] = summary.totals.get(name, 0.0) + value
        detail: dict[str, Json] = {
            "adjacent_crossings": adjacent, "pair_inversions": inversions,
            "largest_adjacent_fall": fall, "range": [min(values), max(values)],
            "quantile_grid": numbers(grid),
        }
        if method != "RAW":
            wanted = expected.qm if method == "QM" else expected.qdm
            error = maximum_error(values, wanted)
            summary.extreme(f"{method}_oracle_error", error, key)
            summary.counts[f"{method}_oracle_failures"] += int(error > TOL)
            detail["oracle_max_abs_error"] = error
        if rain:
            wet_from_zero = sum(x == 0 and y > 0 for x, y in zip(raw, values, strict=True))
            summary.counts[f"{method}_raw_zero_to_positive_members"] += wet_from_zero
            summary.counts[f"{method}_raw_zero_to_positive_cases"] += int(wet_from_zero > 0)
        record[method] = detail

    issued = quantiles(saved["QDM"], expected.p)
    residuals = [abs(y - z) for y, z in zip(issued, expected.qdm, strict=True)]
    worst = max(range(len(raw)), key=residuals.__getitem__)
    example: dict[str, Json] = {
        "case_id": key, "member_index": worst + 1, "p": expected.p[worst],
        "raw": raw[worst], "qh": expected.qh[worst], "qo": expected.qo[worst],
        "original_rank_formula": expected.qdm[worst], "issued_quantile": issued[worst],
        "absolute_discrepancy": residuals[worst],
        "raw_sorted": numbers([raw[i] for i in order]),
        "qdm_in_raw_order": numbers([saved["QDM"][i] for i in order]),
        "qdm_sorted": numbers(sorted(saved["QDM"])),
    }
    summary.extreme("QDM_issued_quantile_discrepancy", residuals[worst], example)
    summary.counts["QDM_issued_quantile_discrepancy_cases"] += int(max(residuals) > TOL)
    summary.counts["QDM_issued_quantile_discrepancy_members"] += sum(v > TOL for v in residuals)
    summary.totals["QDM_issued_quantile_abs_discrepancy_sum"] = (
        summary.totals.get("QDM_issued_quantile_abs_discrepancy_sum", 0.0) + math.fsum(residuals)
    )
    record["issued_quantile_max_abs_discrepancy"] = max(residuals)
    record["observed_training_range"] = [min(observed), max(observed)]
    record["historical_quantile_grid"] = numbers(
        [linear(p, expected.historical[1], expected.historical[0]) for p in PROBES]
    )
    ox, op = curve([[v] for v in observed])
    record["observed_training_quantile_grid"] = numbers([linear(p, op, ox) for p in PROBES])
    hx = expected.historical[0]
    summary.counts["QM_below_historical_endpoint_members"] += sum(x < hx[0] for x in raw)
    summary.counts["QM_above_historical_endpoint_members"] += sum(x > hx[-1] for x in raw)
    summary.counts["QM_at_observed_min_members"] += sum(
        abs(x - min(observed)) <= TOL for x in saved["QM"]
    )
    summary.counts["QM_at_observed_max_members"] += sum(
        abs(x - max(observed)) <= TOL for x in saved["QM"]
    )
    if rain:
        dry = sum(h < 0.1 for h in expected.qh)
        summary.counts["dry_exception_members"] += dry
        summary.counts["dry_exception_cases"] += int(dry > 0)
        record["dry_exception_members"] = dry
        ratio_errors: list[float] = []
        original_errors: list[float] = []
        for x, h, o, before, after in zip(
            raw, expected.qh, expected.qo, saved["QDM"], issued, strict=True,
        ):
            if h >= 0.1:
                summary.extreme("wet_qh", h, key)
                summary.extreme("wet_qo_over_qh_multiplier", o / h, key)
                summary.extreme("wet_raw_over_qh_change_ratio", x / h, key)
                if o > 0:
                    ratio_errors.append(abs(after / o - x / h))
                    original_errors.append(abs(before / o - x / h))
        summary.extreme("sorted_ratio_preservation_error", max(ratio_errors, default=0.0), key)
        summary.extreme("original_ratio_preservation_error", max(original_errors, default=0.0), key)
        summary.counts["sorted_ratio_preservation_failure_cases"] += int(
            max(ratio_errors, default=0.0) > TOL
        )
        record["sorted_ratio_max_error_non_dry_positive_qo"] = max(ratio_errors, default=0.0)
    else:
        original = maximum_error(
            [y - o for y, o in zip(saved["QDM"], expected.qo, strict=True)],
            [x - h for x, h in zip(raw, expected.qh, strict=True)],
        )
        summary.extreme("original_additive_preservation_error", original, key)
    return record


def adversarial() -> dict[str, Json]:
    """Execute production only as the subject, never as the oracle."""
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from analysis.calibration import calibrate

    examples: list[tuple[str, list[float], list[list[float]], list[float], bool]] = [
        ("additive_reversal", [10, 11, 12], [[0, 0], [100, 100], [200, 200]], [0, 1, 2], False),
        ("ratio_reversal", [10, 11, 12], [[1, 1], [100, 100], [200, 200]], [1, 2, 3], True),
        ("unequal_years", [-100, 0, 2, 5, 8, 10, 100], [[0, 0], [10] * 7], [0, 20], False),
        ("merged_ties", [0, 0, 1, 10, 20, 20], [[0, 0, 10], [0, 20], [20, 20]], [1, 1, 8], False),
        ("dry_boundary", [0, 0.01, 1], [[0.0999] * 2, [0.1] * 2, [0.1001] * 2], [1, 2, 3], True),
        ("all_dry", [0, 0, 0], [[0, 0], [0, 0], [0, 0]], [0, 1, 2], True),
        ("constant_forecast", [3, 3, 3], [[0, 1], [2, 3], [4, 5]], [0, 1, 2], False),
        ("tied_endpoint_midposition", [-10, 0, 110], [[0, 0], [0, 0], [100, 100]], [0, 1, 2], False),
    ]
    result: dict[str, Json] = {}
    for name, raw, years, obs, rain in examples:
        expected = oracle(raw, years, obs, rain)
        target = np.asarray(raw, dtype=np.float64)
        historical = tuple(np.asarray(year, dtype=np.float64) for year in years)
        actual = np.asarray(obs, dtype=np.float64)
        production = calibrate(target, historical, actual, rain)
        qm = [float(v) for v in production.qm.flat]
        qdm = [float(v) for v in production.qdm.flat]
        error = max(maximum_error(qm, expected.qm), maximum_error(qdm, expected.qdm))
        duplicate = calibrate(
            target, (np.tile(historical[0], 3), *historical[1:]), actual, rain,
        )
        duplicate_error = max(
            maximum_error(qm, [float(v) for v in duplicate.qm.flat]),
            maximum_error(qdm, [float(v) for v in duplicate.qdm.flat]),
        )
        doubled = calibrate(np.repeat(target, 2), historical, actual, rain)
        target_error = max(
            maximum_error([x for value in qm for x in (value, value)],
                          [float(v) for v in doubled.qm.flat]),
            maximum_error([x for value in qdm for x in (value, value)],
                          [float(v) for v in doubled.qdm.flat]),
        )
        dry = sum(h < 0.1 for h in expected.qh) if rain else 0
        if max(error, duplicate_error, target_error) > TOL or production.dry_exceptions != dry:
            raise RuntimeError(f"Adversarial oracle/invariance failure: {name}")
        sorted_order = sorted(range(len(raw)), key=raw.__getitem__)
        falls = sum(qdm[b] < qdm[a] - TOL for a, b in pairwise(sorted_order))
        if name in ("additive_reversal", "ratio_reversal") and falls != 2:
            raise RuntimeError(f"Expected the full constructed reversal: {name}")
        if name == "dry_boundary" and (dry != 1 or qdm[0] <= 0):
            raise RuntimeError("Dry threshold/zero-to-wet example did not reproduce")
        if name == "tied_endpoint_midposition" and maximum_error(qm, [0.5, 0.5, 2]) > TOL:
            raise RuntimeError("Tied minimum must clamp to its probability midposition, not CDF zero")
        if any(qm[b] < qm[a] - TOL for a, b in pairwise(sorted_order)):
            raise RuntimeError(f"QM monotonicity failed: {name}")
        result[name] = {
            "raw": numbers(raw), "historical": [numbers(y) for y in years],
            "observations": numbers(obs), "p": numbers(expected.p),
            "historical_values": numbers(expected.historical[0]),
            "historical_mass_midpoints": numbers(expected.historical[1]),
            "qh": numbers(expected.qh), "qo": numbers(expected.qo),
            "qm": numbers(qm), "qdm": numbers(qdm),
            "issued_quantiles_at_original_p": numbers(quantiles(qdm, expected.p)),
            "adjacent_crossings": falls, "oracle_max_error": error,
            "historical_one_year_replication_error": duplicate_error,
            "forecast_member_replication_error": target_error, "dry_exceptions": dry,
        }
    hx, hp = curve([[0, 0], [10] * 7])
    if hx != [0, 10] or hp != [0.25, 0.75]:
        raise RuntimeError("Unequal-sized annual ensembles were not equally weighted")
    weighted = oracle([-100, 100], [[0, 0], [10] * 7], [0, 20], False)
    if weighted.qm != [0, 20]:
        raise RuntimeError("QM clipped-tail example failed")
    if midranks([0, 0, 10]) != [1 / 3, 1 / 3, 5 / 6]:
        raise RuntimeError("Tie midranks failed")
    return result


def interpretation() -> dict[str, Json]:
    return {
        "classification": "A passing oracle establishes numerical implementation of the declared " +
                          "finite-sample formula, not monotonicity, distribution-level change " +
                          "preservation, physical realism or superior forecast skill.",
        "roundoff_check": "The primary oracle uses accurately summed equal-year weights, not the " +
                          "production cumulative-sum rounding pattern. Every case is also compared " +
                          "against an independently coded scalar replay of that floating operation " +
                          "order, still using manual interpolation/midranks. Primary absolute " +
                          "1e-10 exceedances are retained, checked with 50-digit Decimal, and never " +
                          "silently reclassified as strict numerical passes. This distinguishes " +
                          "tiny accumulation sensitivity from an algebra or data-pairing defect.",
        "formula_refs": ["analysis/calibration.py:92-102", "analysis/calibration.py:155-178"],
        "pairing_refs": ["analysis/data_io.py:224-248", "analysis/run_verification.py:79-111"],
        "saved_member_order_ref": "analysis/run_verification.py:140-153",
        "annual_weighting": "Each accepted source year has mass 1/N and each member in year y has " +
                            "mass 1/(N*M_y). Duplicating one complete year's ensemble cannot change " +
                            "QM/QDM. Actual equal M_y within a case makes pooled member weighting " +
                            "coincidentally equivalent; unequal synthetic years test the distinction.",
        "cdf_convention": "Merged-tie probability midpoints with linear interpolation are a plotting-" +
                          "position distribution approximation, not the right-continuous step ECDF. " +
                          "Endpoint clipping and midpoint conventions are deliberate method choices.",
        "crossing_math": "At original forecast midrank p, additive QDM is x+Qo(p)-Qh(p); " +
                         "the difference between adjacent corrected ranks can be negative when " +
                         "the historical quantile increment exceeds the forecast plus observed " +
                         "increments. Rainfall ratios likewise need not be monotone. This alone " +
                         "is not a coding bug. The issued sorted ensemble has a valid monotone " +
                         "quantile function, but generally not the original-rank prescribed values.",
        "change_preservation": "For temperature the original-label identity y-Qo=x-Qh holds up to " +
                               "roundoff. For rain y/Qo=x/Qh holds only when Qh>=0.1 and Qo>0. " +
                               "After sorting, the JSON reports the actual issued Q(p) minus the " +
                               "original-p formula and non-dry positive-Qo ratio residuals. " +
                               "No universal distribution-level rank-change preservation is asserted.",
        "dry_rule_ref": "analysis/calibration.py:169-176",
        "dry_rule": "Qh<0.1 mm substitutes Qo instead of an unbounded ratio; this can turn raw zero " +
                    "into positive rain and explicitly sacrifices multiplicative change preservation. " +
                    "Qh=0.1 is the wet branch. With Qh>=0.1 the multiplier Qo/Qh is bounded by " +
                    "max(training observations)/0.1 for each case, but can still amplify extremes.",
        "qm_tails": "QM is nondecreasing and lies within the historical observational range. " +
                    "It can flatten out-of-support extremes and create ties; equality to observation " +
                    "endpoints may begin before the historical model support ends. It does not " +
                    "preserve extrapolated changes. QDM is not constrained to that empirical range.",
        "tied_endpoint_qualification": "np.interp(target,H_unique,H_midpositions) clamps below the " +
                                       "minimum to half its tied probability mass, NOT to CDF 0; " +
                                       "above maximum it clamps to 1 minus half the maximum mass, " +
                                       "NOT CDF 1. Consequently the clipped mapped values need not " +
                                       "equal observational extrema. Endpoints and zero masses are " +
                                       "quantified on all actual cases, separating out-of-support " +
                                       "members from members exactly at a tied endpoint. This is a " +
                                       "midrank plotting-position variant, not the step empirical CDF.",
        "zero_occurrence_policy": "A deterministic value-only map sends all members in the same zero " +
                                  "atom to the same value; it cannot in general split that atom to " +
                                  "match an arbitrary observational zero frequency. Observed zero " +
                                  "frequency and forecast zero frequency also concern different " +
                                  "climate/conditional populations. A randomized or explicitly " +
                                  "rank-based wet-day/zero-occurrence policy would be a substantive " +
                                  "method change, not a silent arithmetic fix. Claims of full CDF " +
                                  "matching or occurrence-frequency matching need qualification.",
        "temperature_realism": "Negative Celsius temperatures are not invalid. No arbitrary physical " +
                               "temperature cutoff is imposed. Actual min/max and counts outside " +
                               "each training observational range are reported as diagnostics, " +
                               "not proof of unrealistic temperatures; there is no supplied physical " +
                               "validity criterion. Rainfall nonnegativity and all-member finiteness " +
                               "are directly checked.",
        "forecast_vs_climate": "analysis/calibration.py:165 estimates F_f using the weather ensemble " +
                              "for one issue/lead, not a future-climate time-window distribution. " +
                              "These estimate different conditional populations. Ensemble exchangeability, " +
                              "representativeness, stable model-observation quantile bias and adequate " +
                              "sample sizes would be needed to motivate this as forecast calibration. " +
                              "The method may be tested as an ensemble-relative QDM adaptation, " +
                              "but no universal climate-trend-preservation claim follows.",
        "skill": "Overall and year-specific metrics are copied from saved tables, with CRPS difference " +
                 "versus RAW on the same product/variable/year. They are descriptive of the existing " +
                 "matched verification, not a new model-quality ranking or causal attribution of skill " +
                 "to crossings. Sorting/relabeling alone cannot change univariate CRPS, means, " +
                 "tercile probabilities or quantile intervals.",
        "minimal_options": [
            "Keep formula and clearly label original-rank algebra; disclose observed crossings, " +
            "dry substitutions and endpoint limitations. This changes no saved forecasts.",
            "Monotone rearrangement: assign sorted corrected values to RAW-sorted member labels. " +
            "Removes label-order inversions without changing the issued marginal distribution " +
            "or existing univariate scores. It breaks original-label delta identities and may " +
            "alter cross-variable/spatial/temporal member dependence; it does not restore the " +
            "desired distribution-level delta equality.",
            "Change mapping choice to monotone QM, or explicitly fit a constrained monotone " +
            "quantile-change curve. QM clips tails and is not delta preserving; constrained " +
            "projection changes corrected values and requires new held-out scoring. Neither " +
            "is silently applied in this audit.",
            "If climate-change preservation is the aim, define and justify a pooled future/forecast " +
            "distribution and stationary quantile-bias assumptions before applying QDM; larger " +
            "pooling changes the estimand and alone does not guarantee no crossings.",
        ],
        "leakage_scope": "The audit pairs only accepted STATUS=OK source-year rows; it neither uses " +
                         "target observations in the oracle nor infers training leakage from current " +
                         "forecast ranks. Full calendar/observation-availability auditing is separate.",
        "primary_source": {
            "citation": "Cannon, Sobie and Murdock (2015), Bias Correction of GCM Precipitation " +
                        "by Quantile Mapping: How Well Do Methods Preserve Changes in Quantiles " +
                        "and Extremes? Journal of Climate 28, 6938-6959.",
            "doi": "10.1175/JCLI-D-14-00754.1",
            "retrieved_url": "https://journals.ametsoc.org/abstract/journals/clim/28/17/jcli-d-14-00754.1.xml",
            "retrieved_on": "2026-10-06",
            "scope_read": "Relevant retrieved sections 1-5a; response later truncated, not a " +
                          "claim to have audited the entire paper.",
            "section_3": "Projected-series time-dependent CDF is estimated over a time window " +
                         "around t; historical and projected quantiles supply the relative change. " +
                         "This is not automatically equivalent to one conditional issuance ensemble.",
            "section_5a": "Daily precipitation examples use 30-year sliding windows for projected " +
                          "means/empirical quantiles and pooled sliding seasonal windows. Zeros " +
                          "are replaced by uniform random sub-trace values below 0.05 mm/day " +
                          "before correction and thresholded afterward to handle wet-day frequency.",
            "boundary": "The audited deterministic tied-midpoint mapping and Qh<0.1 mm replacement " +
                        "on weekly/monthly accumulated rainfall is a different occurrence policy; " +
                        "the daily-paper threshold must not be transplanted without justification. " +
                        "Crossing/rearrangement conclusions here follow executed counterexamples " +
                        "and permutation invariance, not a claim that the paper studied these cases.",
        },
    }


def run(root: Path) -> None:
    source = root / "GLOSEA6_KMA_20220301-20260831_v1"
    provenance = observation_provenance(source)
    daily = {day(row["DATE"]): parse_daily(row)
             for row in rows(observation_daily_path(source))}
    output = root / "outputs"
    originals = [root / "analysis" / name for name in (
        "calibration.py", "data_io.py", "run_verification.py", "scoring.py",
    )]
    originals += [output / name for name in (
        "calibrated_members.csv.gz", "training_ledger.csv.gz", "calibration_fits.csv",
        "case_audit.csv", "metrics_overall.csv", "metrics_by_year.csv",
    )]
    originals += sorted((source / "data/model/hcst_mapping").glob("*.csv.gz"))
    original_hashes = hashes(root, originals)
    cases = {row["CASE_ID"]: row for row in rows(output / "case_audit.csv")
             if row["STATUS"] == "VERIFIED"}
    for key, row in cases.items():
        observed, stations = observation_summary(
            daily, day(row["VALID_START"]), day(row["VALID_END"]), row["VARIABLE"] == "prcp",
        )
        if observed is None or abs(observed - float(row["OBS"])) > TOL \
                or stations != int(row["N_STATION_MIN"]):
            raise RuntimeError(f"Selected-source target observation mismatch: {key}")
    fits = {row["CASE_ID"]: row for row in rows(output / "calibration_fits.csv")}
    if not cases or set(fits) != set(cases):
        raise RuntimeError("Expected nonempty matching verified and fitted case keys")
    saved: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for row in rows(output / "calibrated_members.csv.gz"):
        values = saved[row["CASE_ID"]][row["METHOD"]]
        if int(row["MEMBER_INDEX"]) != len(values) + 1:
            raise RuntimeError("Non-contiguous or duplicate saved member index")
        values.append(float(row["VALUE"]))
    if set(saved) != set(cases):
        raise RuntimeError("Saved ensemble case keys differ from verified cases")
    accepted: dict[str, dict[int, float]] = defaultdict(dict)
    ledger_counts: dict[tuple[str, int], int] = {}
    for row in rows(output / "training_ledger.csv.gz"):
        if row["STATUS"] != "OK":
            continue
        key, year = row["CASE_ID"], int(row["SOURCE_YEAR"])
        observed, stations = observation_summary(
            daily, day(row["HIST_START"]), day(row["HIST_END"]), cases[key]["VARIABLE"] == "prcp",
        )
        if observed is None or abs(observed - float(row["OBS"])) > TOL \
                or stations != int(row["N_STATION_MIN"]):
            raise RuntimeError(f"Selected-source training observation mismatch: {key}/{year}")
        if year in accepted[key]:
            raise RuntimeError(f"Duplicate accepted source year: {key}/{year}")
        accepted[key][year] = float(row["OBS"])
        ledger_counts[(key, year)] = int(row["MEMBERS"])
    if set(accepted) != set(cases):
        raise RuntimeError("Accepted ledger case keys differ from verified cases")
    groups: dict[str, Summary] = {}
    case_results: list[Json] = []
    visited: set[str] = set()
    roundoff_alerts: list[Json] = []
    uniform: Counter[str] = Counter()
    for product in ("1mon", "3mon"):
        for variable in ("t15m", "prcp"):
            label = f"{product}/{variable}"
            group = Summary()
            groups[label] = group
            history: dict[str, dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
            for row in rows(source / f"data/model/hcst_mapping/{product}_{variable}.csv.gz"):
                key, year = row["CASE_ID"], int(row["SOURCE_YEAR"])
                if key in accepted and year in accepted[key]:
                    history[key][year].append(float(row["VALUE"]))
            for key, years in sorted(history.items()):
                observations = accepted[key]
                source_years = sorted(observations)
                if source_years != sorted(years):
                    raise RuntimeError(f"Unpaired source years: {key}")
                if ";".join(map(str, source_years)) != fits[key]["SOURCE_YEARS"]:
                    raise RuntimeError(f"Fit/ledger source-year mismatch: {key}")
                ensembles = [years[year] for year in source_years]
                if any(len(years[y]) != ledger_counts[(key, y)] for y in source_years):
                    raise RuntimeError(f"Historical member count mismatch: {key}")
                member_counts = sorted({len(year) for year in ensembles})
                uniform[str(member_counts)] += 1
                values = saved[key]
                if set(values) != set(METHODS) or any(
                    len(values[m]) != int(cases[key]["FCST_VALID"]) for m in METHODS
                ):
                    raise RuntimeError(f"Saved method/member mismatch: {key}")
                if not all(math.isfinite(x) for v in values.values() for x in v):
                    raise RuntimeError(f"Nonfinite saved member: {key}")
                raw = values["RAW"]
                obs = [observations[year] for year in source_years]
                expected = oracle(raw, ensembles, obs, variable == "prcp")
                record = diagnose(key, raw, values, expected, obs, variable == "prcp", group)
                record["endpoint_and_zero_mass"] = endpoints(
                    key, ensembles, obs, values, expected, variable == "prcp", group,
                )
                sequential = oracle(raw, ensembles, obs, variable == "prcp", sequential_curve)
                for method, accurate, replay in (
                    ("QM", expected.qm, sequential.qm), ("QDM", expected.qdm, sequential.qdm),
                ):
                    replay_error = maximum_error(values[method], replay)
                    group.extreme(f"{method}_operation_order_oracle_error", replay_error, key)
                    group.counts[f"{method}_operation_order_oracle_failures"] += int(replay_error > TOL)
                    if maximum_error(values[method], accurate) > TOL:
                        errors = [abs(a - b) for a, b in zip(values[method], accurate, strict=True)]
                        i = max(range(len(raw)), key=errors.__getitem__)
                        high_precision = decimal_qdm(
                            raw[i], expected.p[i], ensembles, obs, variable == "prcp",
                        ) if method == "QDM" else None
                        roundoff_alerts.append({
                            "case_id": key, "method": method, "member_index": i + 1,
                            "saved": values[method][i], "accurate_sum_oracle": accurate[i],
                            "sequential_sum_oracle": replay[i],
                            "primary_absolute_error": abs(values[method][i] - accurate[i]),
                            "primary_relative_error": abs(values[method][i] - accurate[i]) /
                                                      max(abs(accurate[i]), 1e-300),
                            "operation_order_absolute_error": replay_error,
                            "decimal_50_digits": high_precision,
                            "decimal_vs_primary": None if high_precision is None else
                                                 abs(high_precision - accurate[i]),
                            "decimal_vs_saved": None if high_precision is None else
                                               abs(high_precision - values[method][i]),
                        })
                # Change only one year's multiplicity; annual mass must not change.
                repeated = [ensembles[0] * 3, *ensembles[1:]]
                invariant = oracle(raw, repeated, obs, variable == "prcp")
                invariance_error = max(
                    maximum_error(expected.qm, invariant.qm),
                    maximum_error(expected.qdm, invariant.qdm),
                )
                group.extreme("one_year_member_replication_error", invariance_error, key)
                group.counts["member_replication_failure_cases"] += int(invariance_error > TOL)
                dry = sum(h < 0.1 for h in expected.qh) if variable == "prcp" else 0
                group.counts["dry_flag_mismatch_cases"] += int(
                    dry != int(fits[key]["QDM_DRY_EXCEPTIONS"])
                )
                record.update({
                    "product": product, "variable": variable,
                    "valid_start": cases[key]["VALID_START"], "valid_end": cases[key]["VALID_END"],
                    "n_train": len(source_years), "historical_member_counts": numbers(member_counts),
                    "member_replication_error": invariance_error,
                })
                case_results.append(record)
                visited.add(key)
            print(f"AUDIT {label}: {group.cases} cases", flush=True)
    if len(case_results) != len(cases) or visited != set(cases):
        raise RuntimeError("Audit did not visit every eligible case")
    failures = sum(
        group.counts[name] for group in groups.values()
        for name in ("QM_oracle_failures", "QDM_oracle_failures",
                     "member_replication_failure_cases", "dry_flag_mismatch_cases")
    )
    operation_failures = sum(
        group.counts[name] for group in groups.values()
        for name in ("QM_operation_order_oracle_failures", "QDM_operation_order_oracle_failures")
    )
    metrics: list[Json] = []
    for name in ("overall", "by_year"):
        metric_rows = [row for row in rows(output / f"metrics_{name}.csv") if row["METHOD"] in METHODS]
        dimensions = ("PRODUCT", "VARIABLE") if name == "overall" else ("PRODUCT", "VARIABLE", "YEAR")
        raw_metrics = {
            tuple(row[d] for d in dimensions): row for row in metric_rows if row["METHOD"] == "RAW"
        }
        for row in metric_rows:
            baseline = raw_metrics[tuple(row[d] for d in dimensions)]
            metric: dict[str, Json] = {"table": name}
            metric.update({d: row[d] for d in (*dimensions, "METHOD")})
            for field_name in ("N", "BIAS", "MAE", "RMSE", "CRPS", "CRPS_SKILL",
                               "BRIER_SKILL", "RPS_SKILL", "COVERAGE90", "WIDTH90"):
                metric[field_name] = float(row[field_name]) if row[field_name] else None
            metric["CRPS_delta_vs_RAW"] = float(row["CRPS"]) - float(baseline["CRPS"])
            metrics.append(metric)
    probes = adversarial()
    final_hashes = hashes(root, originals)
    if original_hashes != final_hashes:
        raise RuntimeError("Original input/source hashes changed during audit")
    report: dict[str, Json] = {
        "observation_source": provenance,
        "status": "FORMULA_MATCH" if failures == 0 else
                  "STRICT_TOLERANCE_ALERT" if operation_failures == 0 else "FORMULA_DISCREPANCY",
        "cases_audited": len(case_results), "verified_cases": len(cases),
        "absolute_tolerance": TOL,
        "observation_policy_scope": "Selected-source outputs: daily station count >=50; " +
                                    "use actual-n daily means, including 61/60; " +
                                    "no 62/n scaling or raw-station imputation. " +
                                    "Policy/calendar validation is a separate training audit.",
        "numpy": np.__version__, "scipy": version("scipy"), "python": sys.version,
        "oracle": "Independent Counter/fsum equal-year masses, binary-search scalar interpolation, " +
                  "manual tie midranks; no production distribution, np.interp or scipy rankdata.",
        "quantile_grid_probabilities": numbers(PROBES),
        "issued_quantile_convention": "Linear interpolation on sorted individual member positions " +
                                     "(i+0.5)/M, clipped endpoints. Repeated atoms retained. " +
                                     "Training curves instead merge ties into mass midpoints, " +
                                     "exactly as the declared production convention.",
        "crossing_convention": "Stable RAW order; meaningful decreases and pair inversions exceed " +
                               "1e-10; exact negative adjacent counts also retained. " +
                               "Negative-adjacent cases are counted separately from positive-valued cases.",
        "historical_member_count_patterns": dict(uniform),
        "groups": {key: value.json() for key, value in groups.items()},
        "strict_tolerance_alerts": roundoff_alerts,
        "operation_order_oracle_failures": operation_failures,
        "adversarial": probes, "case_diagnostics": case_results,
        "saved_skill_comparisons": metrics,
        "source_hashes_start": dict(original_hashes), "source_hashes_end": dict(final_hashes),
        "originals_unchanged": True, "interpretation": interpretation(),
    }
    destination = output / "method_review/qm_qdm_audit.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
        _ = handle.write("\n")
    print(json.dumps({
        "status": report["status"], "cases": len(case_results), "oracle_failures": failures,
        "operation_order_oracle_failures": operation_failures,
        "qdm_crossing_cases": sum(s.counts["QDM_crossing_cases"] for s in groups.values()),
        "qm_crossing_cases": sum(s.counts["QM_crossing_cases"] for s in groups.values()),
        "originals_unchanged": True, "output": destination.relative_to(root).as_posix(),
    }))
    if failures:
        raise SystemExit(1)


def main() -> None:
    if sys.argv[1:] == ["--help"]:
        print("Usage: python -B analysis/audit_qm_qdm.py [--help]\n" +
              "Independently audit all saved verified QM/QDM cases and adversarial inputs.\n" +
              "Writes only outputs/method_review/qm_qdm_audit.json; no production edits.\n" +
              "Exit 1 retains any strict 1e-10 numerical findings in the completed JSON.")
        return
    if sys.argv[1:]:
        raise SystemExit("Unexpected arguments; use --help")
    run(Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    main()
