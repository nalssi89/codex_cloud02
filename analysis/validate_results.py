#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "scipy==1.18.1"]
# ///
"""Independent, streaming real-data QA. Run: python analysis/validate_results.py.

No production reader, quantile mapper, or scoring function is used to recompute
results. The production calibrator is exercised only by the leakage experiment.
Numerical tolerances are absolute 2e-8 plus relative 2e-9; quadrature allows 2e-7.
"""

from __future__ import annotations

import calendar
import csv
import gzip
import json
import math
import sys
from collections import Counter, defaultdict
from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from statistics import NormalDist
from typing import NamedTuple, TextIO, TypedDict

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analysis.data_io import Json, observation_daily_path, observation_provenance

Row = dict[str, str]
Array = NDArray[np.float64]
METHODS = ("RAW", "QM", "QDM", "EMOS")
LABELS = ("BN", "NN", "AN")
SOURCE = "GLOSEA6_KMA_20220301-20260831_v1"


@dataclass(frozen=True, slots=True)
class Checks:
    """Keep named counts and maximum absolute deviations, not assertion traces."""

    counts: Counter[str] = field(default_factory=Counter)
    deviations: dict[str, float] = field(default_factory=dict)

    def require(self, condition: bool, name: str, context: str) -> None:
        assert condition, f"{name}: {context}"
        self.counts[name] += 1

    def close(
        self, actual: float, expected: float, name: str, context: str,
        absolute: float = 2e-8,
    ) -> None:
        delta = abs(actual - expected)
        self.deviations[name] = max(self.deviations.get(name, 0.0), delta)
        self.require(
            math.isfinite(actual) and math.isfinite(expected)
            and delta <= absolute + 2e-9 * abs(expected),
            name, f"{context}: actual={actual!r}, expected={expected!r}, delta={delta!r}",
        )


def rows(path: Path) -> Iterator[Row]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as stream:
        yield from csv.DictReader(stream)


def day(value: str) -> date:
    return date.fromisoformat(value) if "-" in value else date(
        int(value[:4]), int(value[4:6]), int(value[6:8]),
    )


def window(init: date, product: str, lead: str) -> tuple[date, date]:
    offset = int(lead[1:])
    if product == "1mon":
        start = init + timedelta(days=7 * (offset - 1))
        return start, start + timedelta(days=6)
    assert product == "3mon", f"Unknown product {product}"
    year, month = divmod(init.year * 12 + init.month - 1 + offset, 12)
    return date(year, month + 1, 1), date(
        year, month + 1, calendar.monthrange(year, month + 1)[1],
    )


class DailyRecord(NamedTuple):
    """Independent source means with the declared station rule and QC flags."""

    temperature: float
    precipitation: float
    temperature_stations: int
    precipitation_stations: int
    required_stations: int
    total_stations: int
    temperature_qc: str
    precipitation_qc: str


Daily = Mapping[date, DailyRecord]


def parse_daily(row: Mapping[str, str]) -> DailyRecord:
    """Read source fields directly, including unavailable (blank) values."""
    return DailyRecord(
        float(row["T15M"]) if row["T15M"] else math.nan,
        float(row["PRCP"]) if row["PRCP"] else math.nan,
        int(row["N_STATION_T15M"]), int(row["N_STATION_PRCP"]),
        int(row["N_STATION_REQUIRED"]), int(row["N_STATION_TOTAL"]),
        row["QC_T15M"], row["QC_PRCP"],
    )


def observation_summary(
    daily: Daily, start: date, end: date, rain: bool,
) -> tuple[float | None, int]:
    """All days must pass source QC/count rules; never rescale their means."""
    period = [daily.get(start + timedelta(days=offset))
              for offset in range((end - start).days + 1)]
    assert period, f"Empty observation window {start}/{end}"
    if any(record is None for record in period):
        return None, 0
    records = [record for record in period if record is not None]
    minimum = min(record.precipitation_stations if rain else record.temperature_stations
                  for record in records)
    values: list[float] = []
    for record in records:
        stations = record.precipitation_stations if rain else record.temperature_stations
        value = record.precipitation if rain else record.temperature
        if not 0 < record.required_stations <= stations <= record.total_stations \
                or (record.precipitation_qc if rain else record.temperature_qc) != "OK" \
                or not math.isfinite(value):
            return None, minimum
        values.append(value)
    total = math.fsum(values)
    return (total if rain else total / len(values)), minimum


def observation(daily: Daily, start: date, end: date, rain: bool) -> float | None:
    return observation_summary(daily, start, end, rain)[0]


def observation_regressions(qa: Checks) -> None:
    """Deterministic source-boundary checks for contributing-station averages."""
    start, end = date(2000, 1, 1), date(2000, 1, 2)
    source = {
        "T15M": "10", "PRCP": "3", "N_STATION_T15M": "61",
        "N_STATION_PRCP": "60", "N_STATION_REQUIRED": "50",
        "N_STATION_TOTAL": "62", "QC_T15M": "OK", "QC_PRCP": "OK",
    }
    first = parse_daily(source)
    second = parse_daily({**source, "T15M": "20", "PRCP": "5",
                          "N_STATION_T15M": "60", "N_STATION_PRCP": "61"})
    daily = {start: first, end: second}
    for rain, expected in ((False, 15.0), (True, 8.0)):
        value, stations = observation_summary(daily, start, end, rain)
        qa.require(value is not None and stations == 60, "partial_station_acceptance", str(rain))
        assert value is not None
        qa.close(value, expected, "unscaled_participating_means", str(rain))
        for count in (50, 62):
            boundary = parse_daily({**source, "N_STATION_T15M": str(count),
                                    "N_STATION_PRCP": str(count)})
            qa.require(observation({start: boundary}, start, start, rain)
                       == (3.0 if rain else 10.0),
                       "station_rule_boundaries", f"{rain}/{count}")
        other_qc = first._replace(temperature_qc="FAIL") if rain \
            else first._replace(precipitation_qc="FAIL")
        qa.require(observation({start: other_qc}, start, start, rain) is not None,
                   "variable_specific_qc", str(rain))
        value = observation({start: first._replace(required_stations=61)}, start, start, rain)
        qa.require((value is None) == rain, "variable_specific_station_rule", str(rain))
        for field_name, replacement in (
            ("QC_PRCP" if rain else "QC_T15M", "FAIL"),
            ("N_STATION_PRCP" if rain else "N_STATION_T15M", "49"),
            ("N_STATION_PRCP" if rain else "N_STATION_T15M", "63"),
            ("N_STATION_REQUIRED", "63"), ("N_STATION_REQUIRED", "0"),
            ("PRCP" if rain else "T15M", ""),
            ("PRCP" if rain else "T15M", "nan"),
            ("PRCP" if rain else "T15M", "inf"),
        ):
            invalid = parse_daily({**source, field_name: replacement})
            qa.require(observation({start: first, end: invalid}, start, end, rain) is None,
                       "invalid_daily_rejected", f"{rain}/{field_name}/{replacement}")
        qa.require(observation({start: first}, start, end, rain) is None,
                   "missing_day_rejected", str(rain))


def mean(values: Sequence[float]) -> float:
    return math.fsum(values) / len(values)


def quantile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    return ordered[lower] + (position - lower) * (ordered[upper] - ordered[lower])


def discrete_crps(values: Sequence[float], observed: float) -> float:
    """Direct pairwise matrix, deliberately unlike production sorted CRPS."""
    sample = np.asarray(values, dtype=np.float64)
    distances: Array = np.asarray(
        np.abs(sample.reshape(-1, 1) - sample.reshape(1, -1)), dtype=np.float64,
    )
    return mean([abs(value - observed) for value in values]) - math.fsum(
        float(value) for value in distances.flat
    ) / (2 * len(values) ** 2)


def pdf(value: float) -> float:
    return math.exp(-value * value / 2) / math.sqrt(2 * math.pi)


def cdf(value: float) -> float:
    """erfc avoids subtractive cancellation in negative Gaussian tails."""
    return 0.5 * math.erfc(-value / math.sqrt(2))


def normal_crps(mu: float, sigma: float, observed: float, rain: bool) -> float:
    z = (observed - mu) / sigma
    result = sigma * (z * (2 * cdf(z) - 1) + 2 * pdf(z) - 1 / math.sqrt(math.pi))
    if rain:
        zero = -mu / sigma
        result -= sigma * (
            zero * cdf(zero) ** 2 + 2 * cdf(zero) * pdf(zero)
            - cdf(math.sqrt(2) * zero) / math.sqrt(math.pi)
        )
    return result


def integrated_crps(mu: float, sigma: float, observed: float, rain: bool) -> float:
    """Integrate squared CDF errors, split at the observed step and censor."""
    normal = NormalDist(mu, sigma)
    lower = 0.0 if rain else min(observed, mu - 14 * sigma)
    upper = max(observed, mu + 14 * sigma, lower)
    left, _ = quad(
        lambda value: normal.cdf(float(value)) ** 2, lower, observed,
        epsabs=1e-9, epsrel=1e-11,
    )
    right, _ = quad(
        lambda value: (1 - normal.cdf(float(value))) ** 2, observed, upper,
        epsabs=1e-9, epsrel=1e-11,
    )
    return float(left) + float(right)


def correlation(left: Sequence[float], right: Sequence[float]) -> float | None:
    if len(left) < 3 or max(left) == min(left) or max(right) == min(right):
        return None
    lm, rm = mean(left), mean(right)
    covariance = math.fsum((a - lm) * (b - rm) for a, b in zip(left, right, strict=True))
    return covariance / math.sqrt(
        math.fsum((v - lm) ** 2 for v in left)
        * math.fsum((v - rm) ** 2 for v in right),
    )


def distribution(values: Sequence[tuple[float, float]]) -> tuple[list[float], list[float]]:
    """Accumulate tied mass explicitly, each historical year weighing equally."""
    masses: dict[float, float] = defaultdict(float)
    for value, weight in values:
        masses[value] += weight
    ordered = sorted(masses)
    total, cumulative = math.fsum(masses.values()), 0.0
    positions: list[float] = []
    for value in ordered:
        weight = masses[value] / total
        positions.append(cumulative + weight / 2)
        cumulative += weight
    return ordered, positions


def interpolate(value: float, x: Sequence[float], y: Sequence[float]) -> float:
    if value <= x[0]:
        return y[0]
    for index in range(1, len(x)):
        if value <= x[index]:
            fraction = (value - x[index - 1]) / (x[index] - x[index - 1])
            return y[index - 1] + fraction * (y[index] - y[index - 1])
    return y[-1]


def mapping_check(
    qa: Checks, key: str, target: Sequence[float], ensembles: Sequence[Sequence[float]],
    actual: Sequence[float], corrected: Mapping[str, Sequence[float]], rain: bool,
) -> int:
    historical, hp = distribution([
        (value, 1 / (len(ensembles) * len(ensemble)))
        for ensemble in ensembles for value in ensemble
    ])
    observed, op = distribution([(v, 1 / len(actual)) for v in actual])
    dry = 0
    for index, value in enumerate(target):
        probability = interpolate(value, historical, hp)
        qm = interpolate(probability, op, observed)
        rank = (sum(v < value for v in target) + sum(v == value for v in target) / 2) / len(target)
        obs_q = interpolate(rank, op, observed)
        hist_q = interpolate(rank, hp, historical)
        if rain:
            dry += int(hist_q < 0.1)
            qdm = obs_q if hist_q < 0.1 else value * obs_q / hist_q
        else:
            qdm = value + obs_q - hist_q
        qa.close(corrected["QM"][index], qm, "QM_algebra", f"{key}/{index}")
        qa.close(corrected["QDM"][index], qdm, "QDM_algebra", f"{key}/{index}")
    qa.counts["mapping_examples"] += 1
    qa.counts["mapping_dry_exceptions"] += dry
    return dry


def leakage_check(
    qa: Checks, key: str, daily: Daily, start: date, end: date, rain: bool,
    historical_windows: Sequence[tuple[date, date]], target: Sequence[float],
    ensembles: Sequence[Sequence[float]], actual: Sequence[float], fit: Row,
) -> None:
    """Really perturb held-out daily observations, then rebuild and refit."""
    from analysis.calibration import calibrate

    changed = dict(daily)
    for offset in range((end - start).days + 1):
        when = start + timedelta(days=offset)
        record = changed[when]
        changed[when] = record._replace(
            temperature=record.temperature + 1000, precipitation=record.precipitation + 10000,
        )
    qa.require(
        observation(changed, start, end, rain) != observation(daily, start, end, rain),
        "heldout_target_changed", key,
    )
    rebuilt: list[float] = []
    for bounds, original in zip(historical_windows, actual, strict=True):
        value = observation(changed, *bounds, rain)
        qa.require(value is not None, "heldout_training_available", key)
        assert value is not None
        qa.close(value, original, "heldout_training_unchanged", key)
        rebuilt.append(value)
    forecast = np.asarray(target, dtype=np.float64)
    history = tuple(np.asarray(v, dtype=np.float64) for v in ensembles)
    before = calibrate(forecast, history, np.asarray(actual, dtype=np.float64), rain)
    after = calibrate(forecast, history, np.asarray(rebuilt, dtype=np.float64), rain)
    qa.require(before.parameters == after.parameters, "heldout_fit_unchanged", key)
    qa.require(
        np.array_equal(before.qm, after.qm) and np.array_equal(before.qdm, after.qdm)
        and before.mu == after.mu and before.sigma == after.sigma
        and before.fit_crps == after.fit_crps and before.converged == after.converged,
        "heldout_predictions_unchanged", key,
    )
    for name, value in zip(("A", "B", "C", "D"), before.parameters, strict=True):
        qa.close(float(fit[name]), value, "heldout_refit_matches_export", f"{key}/{name}")


@dataclass(frozen=True, slots=True)
class Training:
    year: int
    start: date
    end: date
    members: int
    observed: float
    stations: int
    reference_difference: float
    reference_check: str


class ReferenceDifference(TypedDict):
    case_id: str
    source_year: int
    daily_stations: int
    reference_stations: int
    daily_value: float
    reference_value: float
    absolute_difference: float
    reference_check: str


def check_reference(
    qa: Checks, key: str, item: Training, reference_value: float, reference_stations: int,
    fresh: bool = False,
) -> ReferenceDifference | None:
    """Historical equality is diagnostic, not a contract for a fresh source."""
    context = f"{key}/{item.year}"
    qa.require(math.isfinite(reference_value), "source_reference_finite", context)
    delta = abs(reference_value - item.observed)
    qa.close(item.reference_difference, delta, "saved_reference_difference", context)
    if fresh:
        qa.counts["new_observation_source_reference_checked"] += 1
        qa.deviations["new_observation_source_reference_difference"] = max(
            qa.deviations.get("new_observation_source_reference_difference", 0.0), delta,
        )
        if delta <= 0.0001:
            return None
        qa.counts["NEW_OBSERVATION_SOURCE_DIFFERENCE"] += 1
    elif item.stations == 62:
        qa.require(reference_stations == item.stations, "source_reference_station_minimum", context)
        qa.close(reference_value, item.observed, "source_reference_value", context, absolute=0.0001)
        return None
    else:
        qa.counts["partial_station_reference_checked"] += 1
        qa.deviations["partial_station_reference_difference"] = max(
            qa.deviations.get("partial_station_reference_difference", 0.0), delta,
        )
        if delta <= 0.0001 and reference_stations == item.stations:
            return None
    return {
        "case_id": key, "source_year": item.year,
        "daily_stations": item.stations, "reference_stations": reference_stations,
        "daily_value": item.observed, "reference_value": reference_value,
        "absolute_difference": delta, "reference_check": item.reference_check,
    }


def reference_regressions(qa: Checks) -> None:
    """A real partial-population discrepancy must not weaken all-62 equality."""
    start, end = date(2012, 3, 14), date(2012, 3, 20)
    daily_value, reference_value = 5.817851571428571, 5.857845
    item = Training(2012, start, end, 3, daily_value, 61,
                    abs(reference_value - daily_value), "DAILY_MEAN_POLICY_DIFFERENCE")
    difference = check_reference(Checks(), "partial", item, reference_value, 61)
    qa.require(difference is not None and difference["absolute_difference"] > 0.0001,
               "partial_reference_difference_reported", "61 contributors")
    same = Training(2012, start, end, 3, daily_value, 62, 0.0, "MATCHED")
    qa.require(check_reference(Checks(), "matched", same, daily_value, 62) is None,
               "full_reference_match", "62 contributors")
    strict = Training(2012, start, end, 3, daily_value, 62,
                      item.reference_difference, item.reference_check)
    try:
        _ = check_reference(Checks(), "strict", strict, reference_value, 62)
    except AssertionError:
        qa.counts["full_reference_difference_rejected"] += 1
    else:
        qa.require(False, "full_reference_difference_rejected", "62 contributors")
    fresh = Training(2012, start, end, 3, daily_value, 62,
                     item.reference_difference, "NEW_OBSERVATION_SOURCE_DIFFERENCE")
    difference = check_reference(Checks(), "fresh", fresh, reference_value, 62, fresh=True)
    qa.require(difference is not None, "fresh_full_reference_difference_reported", "62 contributors")


class AuditCounts(TypedDict):
    total_cases: int
    eligible_target_cases: int


class ValidationDigest(TypedDict):
    observation_source: dict[str, Json]
    cases_supplied: int
    cases_verified: int
    prediction_rows: int
    accepted_training_rows: int
    selected_actual_cases: list[str]
    observation_windows_cached: int
    partial_station_reference_differences: list[ReferenceDifference]
    new_observation_source_differences: list[ReferenceDifference]


class ValidationReport(TypedDict, total=False):
    observation_source: dict[str, Json]
    status: str
    invocation: str
    production_scoring_functions_used: bool
    cases_supplied: int
    cases_verified: int
    prediction_rows: int
    accepted_training_rows: int
    selected_actual_cases: list[str]
    observation_windows_cached: int
    partial_station_reference_differences: list[ReferenceDifference]
    new_observation_source_differences: list[ReferenceDifference]
    failure: str
    check_counts: dict[str, int]
    checks_total: int
    maximum_absolute_deviations: dict[str, float]


def read_audit(
    path: Path, loader: Callable[[TextIO], AuditCounts] = json.load,
) -> AuditCounts:
    """Read the fixed generated audit schema; counts are checked immediately."""
    with path.open(encoding="utf-8") as stream:
        return loader(stream)


def validate(root: Path, qa: Checks) -> ValidationDigest:
    observation_regressions(qa)
    reference_regressions(qa)
    source, output = root / SOURCE, root / "outputs"
    provenance = observation_provenance(source)
    fresh = bool(provenance["selected"])
    required = (
        "case_audit.csv", "data_audit.json", "matched_predictions.csv.gz",
        "calibrated_members.csv.gz", "calibration_fits.csv",
        "training_ledger.csv.gz", "metrics_overall.csv", "run_summary.json",
    )
    for name in required:
        qa.require((output / name).is_file(), "input_available", name)
    cases: dict[str, Row] = {}
    for row in rows(source / "cases/verification_cases.csv"):
        qa.require(row["CASE_ID"] not in cases, "supplied_case_unique", row["CASE_ID"])
        cases[row["CASE_ID"]] = row
    audits: dict[str, Row] = {}
    for row in rows(output / "case_audit.csv"):
        key = row["CASE_ID"]
        qa.require(key not in audits, "audit_unique", key)
        audits[key] = row
    qa.require(set(cases) == set(audits), "supplied_case_coverage", "case IDs")
    qa.require(len(cases) == 6580, "supplied_case_count", str(len(cases)))
    accepted = {key for key, row in audits.items() if row["STATUS"] == "VERIFIED"}
    audit_json = read_audit(output / "data_audit.json")
    qa.require(audit_json["total_cases"] == 6580, "data_audit_total", "6580")
    daily: dict[date, DailyRecord] = {}
    for row in rows(observation_daily_path(source)):
        when = day(row["DATE"])
        qa.require(when not in daily and row["AREA"] == "kma", "daily_unique", str(when))
        daily[when] = parse_daily(row)
    cache: dict[tuple[date, date, bool], tuple[float | None, int]] = {}

    def rebuilt(start: date, end: date, rain: bool) -> tuple[float | None, int]:
        token = (start, end, rain)
        if token not in cache:
            cache[token] = observation_summary(daily, start, end, rain)
        return cache[token]

    eligible = 0
    for key, case in cases.items():
        row = audits[key]
        bounds = window(day(case["INIT_DATE"]), case["PRODUCT"], case["LEAD"])
        qa.require(
            bounds == (day(row["VALID_START"]), day(row["VALID_END"])),
            "target_calendar", key,
        )
        qa.require(int(row["DAYS"]) == (bounds[1] - bounds[0]).days + 1, "target_days", key)
        value, stations = rebuilt(*bounds, case["VARIABLE"] == "prcp")
        eligible += int(value is not None and int(row["FCST_VALID"]) >= 2)
        qa.require(int(row["N_STATION_MIN"]) == stations, "target_station_minimum", key)
        if key in accepted:
            qa.require(value is not None, "target_source_qc", key)
            assert value is not None
            qa.close(float(row["OBS"]), value, "target_daily_aggregation", key)
        else:
            qa.require(value is None or int(row["FCST_VALID"]) < 2,
                       "excluded_target_unavailable", f"{key}/{row['STATUS']}")
    qa.require(audit_json["eligible_target_cases"] == eligible,
               "data_audit_eligible", str(eligible))
    qa.require(len(accepted) == eligible, "accepted_case_count", str(len(accepted)))
    predictions: dict[tuple[str, str], Row] = {}
    groups: dict[tuple[str, str, str], list[Row]] = defaultdict(list)
    for row in rows(output / "matched_predictions.csv.gz"):
        key, method = row["CASE_ID"], row["METHOD"]
        qa.require(key in accepted and method in METHODS and (key, method) not in predictions,
                   "prediction_unique_accepted", f"{key}/{method}")
        predictions[key, method] = row
        for name, value in row.items():
            if name not in {
                "CASE_ID", "METHOD", "INIT_DATE", "PRODUCT", "VARIABLE", "LEAD",
                "VALID_START", "VALID_END", "SEASON",
            }:
                qa.require(
                    (not value and name in {"EMOS_MU", "EMOS_SIGMA"} and method != "EMOS")
                    or bool(value) and math.isfinite(float(value)),
                    "prediction_finite", f"{key}/{method}/{name}",
                )
        for name in ("INIT_DATE", "PRODUCT", "VARIABLE", "LEAD", "VALID_START", "VALID_END"):
            qa.require(row[name] == audits[key][name], "prediction_metadata", f"{key}/{method}/{name}")
        qa.require(int(row["N_STATION"]) == int(audits[key]["N_STATION_MIN"]),
                   "prediction_station_minimum", key)
        qa.close(float(row["OBS"]), float(audits[key]["OBS"]), "prediction_observation", key)
        qa.close(float(row["ERROR"]), float(row["PRED_MEAN"]) - float(row["OBS"]),
                 "prediction_error", f"{key}/{method}")
    for method in METHODS:
        qa.require({key for key, m in predictions if m == method} == accepted,
                   "identical_method_mask", method)
    members: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows(output / "calibrated_members.csv.gz"):
        key, method = row["CASE_ID"], row["METHOD"]
        qa.require((key, method) in predictions and method != "EMOS",
                   "member_accepted", f"{key}/{method}")
        values = members[key, method]
        qa.require(int(row["MEMBER_INDEX"]) == len(values) + 1, "member_unique_order", key)
        value = float(row["VALUE"])
        qa.require(math.isfinite(value) and (cases[key]["VARIABLE"] != "prcp" or value >= 0),
                   "member_finite_physical", f"{key}/{method}")
        values.append(value)
    fits: dict[str, Row] = {}
    for row in rows(output / "calibration_fits.csv"):
        key = row["CASE_ID"]
        qa.require(key in accepted and key not in fits, "fit_unique_accepted", key)
        fits[key] = row
        for name in ("A", "B", "C", "D", "MU", "SIGMA", "FIT_CRPS", "INITIAL_CRPS"):
            qa.require(math.isfinite(float(row[name])), "fit_finite", f"{key}/{name}")
        qa.require(
            float(row["B"]) >= 0 and float(row["C"]) > 0 and float(row["D"]) >= 0
            and float(row["SIGMA"]) > 0 and row["CONVERGED"] == "1",
            "fit_physical_converged", key,
        )
        qa.require(float(row["FIT_CRPS"]) <= float(row["INITIAL_CRPS"]) + 1e-8,
                   "fit_improved_initial", key)
    qa.require(set(fits) == accepted, "fit_coverage", "all accepted cases")
    training: dict[str, list[Training]] = defaultdict(list)
    ledger_keys: set[tuple[str, int]] = set()
    for row in rows(output / "training_ledger.csv.gz"):
        key, year = row["CASE_ID"], int(row["SOURCE_YEAR"])
        qa.require((key, year) not in ledger_keys and key in accepted, "ledger_unique", f"{key}/{year}")
        ledger_keys.add((key, year))
        if row["STATUS"] != "OK":
            continue
        start, end, init = day(row["HIST_START"]), day(row["HIST_END"]), day(row["INIT_DATE"])
        case = cases[key]
        qa.require(
            init == day(case["INIT_DATE"]) and year != int(row["TARGET_YEAR"])
            and int(row["TARGET_YEAR"]) == day(audits[key]["VALID_START"]).year
            and end < init,
            "training_no_leakage", f"{key}/{year}",
        )
        qa.require(
            (start, end) == window(date(year, init.month, init.day), case["PRODUCT"], case["LEAD"]),
            "training_calendar", f"{key}/{year}",
        )
        value, stations = rebuilt(start, end, case["VARIABLE"] == "prcp")
        qa.require(value is not None and int(row["N_STATION_MIN"]) == stations,
                   "training_source_qc_station_minimum", f"{key}/{year}")
        assert value is not None
        qa.close(float(row["OBS"]), value, "training_daily_aggregation", f"{key}/{year}")
        delta = float(row["REFERENCE_DIFF"])
        qa.require(math.isfinite(delta) and delta >= 0 and (fresh or stations < 62 or delta <= 0.0001),
                   "training_reference_diff", key)
        qa.require(row["REFERENCE_CHECK"] == (
            "MATCHED" if delta <= 0.0001 else
            "NEW_OBSERVATION_SOURCE_DIFFERENCE" if fresh else "DAILY_MEAN_POLICY_DIFFERENCE"
        ), "training_reference_policy", f"{key}/{year}")
        training[key].append(Training(
            year, start, end, int(row["MEMBERS"]), value, stations, delta, row["REFERENCE_CHECK"],
        ))
    reference_count = 0
    reference_seen: set[tuple[str, int]] = set()
    reference_differences: list[ReferenceDifference] = []
    training_index = {(key, item.year): item for key, items in training.items() for item in items}
    for row in rows(source / "data/asos/asos_kma_period_reference.csv.gz"):
        token = (row["CASE_ID"], int(row["REFERENCE_YEAR"]))
        item = training_index.get(token)
        if item is not None:
            qa.require(
                (day(row["HIST_START"]), day(row["HIST_END"])) == (item.start, item.end)
                and token not in reference_seen
                and row["VARIABLE"] == cases[token[0]]["VARIABLE"]
                and row["PRODUCT"] == cases[token[0]]["PRODUCT"]
                and row["LEAD"] == cases[token[0]]["LEAD"]
                and 0 < int(row["N_STATION_REQUIRED"]) <= int(row["N_STATION"])
                <= int(row["N_STATION_TOTAL"]) and row["AREA_VALID"] == "1"
                and row["AREA"] == "kma",
                "source_reference_join", str(token),
            )
            reference_seen.add(token)
            reference_value, reference_stations = float(row["VALUE"]), int(row["N_STATION"])
            difference = check_reference(qa, token[0], item, reference_value, reference_stations, fresh)
            if difference is not None:
                reference_differences.append(difference)
            reference_count += 1
    qa.require(reference_count == len(training_index), "source_reference_coverage", str(reference_count))
    examples: list[str] = []
    for product in ("1mon", "3mon"):
        for variable in ("t15m", "prcp"):
            keys = sorted(key for key in accepted if (cases[key]["PRODUCT"], cases[key]["VARIABLE"])
                          == (product, variable))
            # Earliest and latest real cases exercise dates, trends, and differing training windows.
            examples.extend((keys[0], keys[-1]))
            raw_seen: Counter[str] = Counter()
            raw_missing: Counter[str] = Counter()
            raw_identifiers: set[tuple[str, str]] = set()
            for row in rows(source / f"data/model/fcst_raw/{product}_{variable}.csv.gz"):
                key = row["CASE_ID"]
                token = (key, row["MEMBER"])
                qa.require(token not in raw_identifiers and key in cases,
                           "source_forecast_unique", str(token))
                raw_identifiers.add(token)
                if not row["VALUE"] or not math.isfinite(float(row["VALUE"])):
                    raw_missing[key] += 1
                    qa.counts["forecast_blank_members"] += 1
                    continue
                if key in accepted:
                    index = raw_seen[key]
                    qa.require(
                        (day(row["VALID_START"]), day(row["VALID_END"]))
                        == window(day(cases[key]["INIT_DATE"]), product, cases[key]["LEAD"]),
                        "source_forecast_calendar", key,
                    )
                    qa.close(members[key, "RAW"][index], float(row["VALUE"]), "source_raw_member", key)
                raw_seen[key] += 1
            for key in cases:
                if (cases[key]["PRODUCT"], cases[key]["VARIABLE"]) != (product, variable):
                    continue
                qa.require(
                    raw_seen[key] == int(audits[key]["FCST_VALID"])
                    and raw_missing[key] == int(audits[key]["FCST_MISSING"])
                    and raw_seen[key] + raw_missing[key] == int(audits[key]["FCST_EXPECTED"]),
                    "known_forecast_blanks", key,
                )
            historical: dict[tuple[str, int], list[float]] = defaultdict(list)
            for row in rows(source / f"data/model/hcst_mapping/{product}_{variable}.csv.gz"):
                token = (row["CASE_ID"], int(row["SOURCE_YEAR"]))
                if token in training_index:
                    historical[token].append(float(row["VALUE"]))
            for key in keys:
                items = sorted(training[key], key=lambda item: item.year)
                fit = fits[key]
                qa.require(
                    [item.year for item in items] == [int(v) for v in fit["SOURCE_YEARS"].split(";")]
                    and len(items) == int(fit["N_TRAIN"]), "fit_source_years_count", key,
                )
                actual = [item.observed for item in items]
                ensembles = [historical[key, item.year] for item in items]
                for item, ensemble in zip(items, ensembles, strict=True):
                    qa.require(len(ensemble) == item.members and len(ensemble) >= 2,
                               "source_hindcast_member_count", f"{key}/{item.year}")
                a, b, c, d = (float(fit[name]) for name in ("A", "B", "C", "D"))
                losses: list[float] = []
                for ensemble, observed in zip(ensembles, actual, strict=True):
                    center = mean(ensemble)
                    variance = math.fsum((v - center) ** 2 for v in ensemble) / (len(ensemble) - 1)
                    losses.append(normal_crps(a + b * center, math.sqrt(c + d * variance),
                                              observed, variable == "prcp"))
                qa.close(float(fit["FIT_CRPS"]), mean(losses), "fit_objective", key)
                for method in METHODS:
                    independent = check_prediction(
                        qa, predictions[key, method], actual, members.get((key, method)), fit,
                    )
                    groups[product, variable, method].append(independent)
                target = members[key, "RAW"]
                center = mean(target)
                variance = math.fsum((v - center) ** 2 for v in target) / (len(target) - 1)
                qa.close(float(fit["MU"]), a + b * center, "fit_target_mu", key)
                qa.close(float(fit["SIGMA"]), math.sqrt(c + d * variance), "fit_target_sigma", key)
                if key in examples:
                    dry = mapping_check(
                        qa, key, target, ensembles, actual,
                        {method: members[key, method] for method in ("QM", "QDM")}, variable == "prcp",
                    )
                    qa.require(dry == int(fit["QDM_DRY_EXCEPTIONS"]),
                               "QDM_dry_exception_count", key)
                    pred = predictions[key, "EMOS"]
                    qa.close(
                        float(pred["CRPS"]),
                        integrated_crps(float(fit["MU"]), float(fit["SIGMA"]),
                                        float(pred["OBS"]), variable == "prcp"),
                        "EMOS_actual_CDF_integration", key, absolute=2e-7,
                    )
                    leakage_check(
                        qa, key, daily, day(pred["VALID_START"]), day(pred["VALID_END"]),
                        variable == "prcp", [(item.start, item.end) for item in items],
                        target, ensembles, actual, fit,
                    )
            del historical
    overall_keys: set[tuple[str, str, str]] = set()
    for row in rows(output / "metrics_overall.csv"):
        token = (row["PRODUCT"], row["VARIABLE"], row["METHOD"])
        qa.require(token in groups and token not in overall_keys, "overall_unique_group", str(token))
        overall_keys.add(token)
        check_overall(qa, row, groups[token])
    qa.require(overall_keys == set(groups), "overall_group_coverage", str(overall_keys))
    for mu, sigma, observed, rain in (
        (-8.0, 2.0, 0.0, True), (-1.0, 3.0, 0.0, True),
        (0.0, 1.0, 0.0, True), (8.0, 2.0, 0.0, True),
        (-30.0, 1.0, 0.0, True), (-8.0, 2.0, -9.0, False),
        (1.0, 0.01, 1.02, False), (100.0, 20.0, 180.0, True),
    ):
        qa.close(normal_crps(mu, sigma, observed, rain),
                 integrated_crps(mu, sigma, observed, rain), "Gaussian_edge_integration",
                 f"mu={mu},sigma={sigma},y={observed},rain={rain}", absolute=2e-7)
    return {
        "observation_source": provenance,
        "cases_supplied": len(cases), "cases_verified": len(accepted),
        "prediction_rows": len(predictions), "accepted_training_rows": len(training_index),
        "selected_actual_cases": examples, "observation_windows_cached": len(cache),
        "partial_station_reference_differences": [] if fresh else reference_differences,
        "new_observation_source_differences": reference_differences if fresh else [],
    }


def check_prediction(
    qa: Checks, row: Row, actual: Sequence[float], values: Sequence[float] | None, fit: Row,
) -> Row:
    key, method = row["CASE_ID"], row["METHOD"]
    context = f"{key}/{method}"
    observed, rain = float(row["OBS"]), row["VARIABLE"] == "prcp"
    low, high = quantile(actual, 1 / 3), quantile(actual, 2 / 3)
    qa.close(float(row["Q33"]), low, "training_tercile", context)
    qa.close(float(row["Q67"]), high, "training_tercile", context)
    qa.close(float(row["CLIM_MEAN"]), mean(actual), "climatological_mean", context)
    qa.close(float(row["CLIM_CRPS"]), discrete_crps(actual, observed), "climatological_CRPS", context)
    qa.require(int(row["N_TRAIN"]) == len(actual), "prediction_training_count", context)
    climate = [sum(v <= low for v in actual) / len(actual),
               sum(low < v <= high for v in actual) / len(actual),
               sum(v > high for v in actual) / len(actual)]
    independent = dict(row)
    independent["CLIM_MEAN"] = repr(mean(actual))
    independent["CLIM_CRPS"] = repr(discrete_crps(actual, observed))
    if values is not None:
        qa.require(len(values) == int(row["N_MEMBERS"]), "prediction_member_count", context)
        predicted = mean(values)
        score = discrete_crps(values, observed)
        probabilities = [sum(v <= low for v in values) / len(values),
                         sum(low < v <= high for v in values) / len(values),
                         sum(v > high for v in values) / len(values)]
        p05, p95 = quantile(values, 0.05), quantile(values, 0.95)
    else:
        mu, sigma = float(row["EMOS_MU"]), float(row["EMOS_SIGMA"])
        qa.require(sigma > 0, "EMOS_positive_sigma", context)
        qa.close(mu, float(fit["MU"]), "EMOS_fit_mu", context)
        qa.close(sigma, float(fit["SIGMA"]), "EMOS_fit_sigma", context)
        normal = NormalDist(mu, sigma)
        p_low, p_high = normal.cdf(low), normal.cdf(high)
        probabilities = [p_low, p_high - p_low, 1 - p_high]
        predicted = mu * NormalDist().cdf(mu / sigma) + sigma * pdf(mu / sigma) if rain else mu
        p05, p95 = normal.inv_cdf(0.05), normal.inv_cdf(0.95)
        if rain:
            p05, p95 = max(0.0, p05), max(0.0, p95)
        score = normal_crps(mu, sigma, observed, rain)
    qa.close(float(row["PRED_MEAN"]), predicted, "independent_mean", context)
    qa.close(float(row["CRPS"]), score, "independent_CRPS", context)
    independent["PRED_MEAN"] = repr(predicted)
    independent["CRPS"] = repr(score)
    for name, value in (("P05", p05), ("P95", p95), ("WIDTH90", p95 - p05),
                        ("COVERAGE90", float(p05 <= observed <= p95))):
        qa.close(float(row[name]), value, "predictive_interval", f"{context}/{name}")
        independent[name] = repr(value)
    qa.require(not rain or predicted >= 0 and p05 >= 0, "nonnegative_rain", context)
    qa.close(math.fsum(float(row[f"P_{label}"]) for label in LABELS), 1,
             "tercile_probability_sum", context)
    category = int(observed > low) + int(observed > high)
    events = [float(index == category) for index in range(3)]
    for index, label in enumerate(LABELS):
        p, cp, event = probabilities[index], climate[index], events[index]
        qa.require(0 <= float(row[f"P_{label}"]) <= 1, "probability_bounds", context)
        for name, value in (
            (f"P_{label}", p), (f"EVENT_{label}", event), (f"BS_{label}", (p - event) ** 2),
            (f"CLIM_P_{label}", cp), (f"CLIM_BS_{label}", (cp - event) ** 2),
        ):
            qa.close(float(row[name]), value, "scalar_category_scores", f"{context}/{name}")
            independent[name] = repr(value)
    for prefix, probs in (("", probabilities), ("CLIM_", climate)):
        brier = math.fsum((p - event) ** 2 for p, event in zip(probs, events, strict=True))
        rps = (probs[0] - events[0]) ** 2 + (
            probs[0] + probs[1] - events[0] - events[1]
        ) ** 2
        qa.close(float(row[f"{prefix}BRIER"]), brier, "scalar_Brier", context)
        qa.close(float(row[f"{prefix}RPS"]), rps, "scalar_RPS", context)
        independent[f"{prefix}BRIER"] = repr(brier)
        independent[f"{prefix}RPS"] = repr(rps)
    return independent


def check_overall(qa: Checks, row: Row, group: Sequence[Row]) -> None:
    context = "/".join(row[name] for name in ("PRODUCT", "VARIABLE", "METHOD"))
    observed = [float(item["OBS"]) for item in group]
    predicted = [float(item["PRED_MEAN"]) for item in group]
    climate = [float(item["CLIM_MEAN"]) for item in group]
    errors = [p - o for p, o in zip(predicted, observed, strict=True)]
    qa.require(int(row["N"]) == len(group), "overall_count", context)
    for name, value in (
        ("BIAS", mean(errors)), ("MAE", mean([abs(v) for v in errors])),
        ("RMSE", math.sqrt(mean([v * v for v in errors]))),
        ("OBS_MEAN", mean(observed)), ("PRED_MEAN", mean(predicted)),
    ):
        qa.close(float(row[name]), value, "overall_scalar_metrics", f"{context}/{name}")
    for name, value in (
        ("CORRELATION", correlation(predicted, observed)),
        ("ACC", correlation(
            [p - c for p, c in zip(predicted, climate, strict=True)],
            [o - c for o, c in zip(observed, climate, strict=True)],
        )),
    ):
        if value is None:
            qa.require(not row[name], "overall_undefined_correlation", context)
        else:
            qa.close(float(row[name]), value, "overall_correlation", f"{context}/{name}")
    for score in ("CRPS", "BRIER", "RPS", "BS_BN", "BS_NN", "BS_AN"):
        value = mean([float(item[score]) for item in group])
        reference = mean([float(item[f"CLIM_{score}"]) for item in group])
        qa.close(float(row[score]), value, "overall_scores", f"{context}/{score}")
        qa.close(float(row[f"CLIM_{score}"]), reference, "overall_scores", f"{context}/CLIM_{score}")
        if reference > 0:
            qa.close(float(row[f"{score}_SKILL"]), 1 - value / reference,
                     "overall_skill", f"{context}/{score}")
        else:
            qa.require(not row[f"{score}_SKILL"], "overall_undefined_skill", context)
    for name in ("COVERAGE90", "WIDTH90"):
        qa.close(float(row[name]), mean([float(item[name]) for item in group]),
                 "overall_intervals", f"{context}/{name}")


def main() -> None:
    if sys.argv[1:] == ["--help"]:
        print("Usage: python analysis/validate_results.py\n"
              + "Independently validate source data and outputs; write outputs/validation.json.")
        return
    if sys.argv[1:]:
        raise SystemExit("Unexpected arguments; use --help")
    qa = Checks()
    report: ValidationReport = {
        "status": "FAIL", "invocation": "python analysis/validate_results.py",
        "production_scoring_functions_used": False,
    }
    try:
        digest = validate(ROOT, qa)
        report["cases_supplied"] = digest["cases_supplied"]
        report["cases_verified"] = digest["cases_verified"]
        report["prediction_rows"] = digest["prediction_rows"]
        report["accepted_training_rows"] = digest["accepted_training_rows"]
        report["selected_actual_cases"] = digest["selected_actual_cases"]
        report["observation_windows_cached"] = digest["observation_windows_cached"]
        report["partial_station_reference_differences"] = digest["partial_station_reference_differences"]
        report["status"] = "PASS"
    except (AssertionError, OSError, ValueError, KeyError, IndexError) as error:
        report["failure"] = str(error)
        raise
    finally:
        report["check_counts"] = dict(sorted(qa.counts.items()))
        report["checks_total"] = sum(qa.counts.values())
        report["maximum_absolute_deviations"] = dict(sorted(qa.deviations.items()))
        destination = ROOT / "outputs" / "validation.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", encoding="utf-8") as stream:
            json.dump(report, stream, indent=2, allow_nan=False)
        print("VALIDATION_SUMMARY " + json.dumps(report, allow_nan=False))


if __name__ == "__main__":
    main()
