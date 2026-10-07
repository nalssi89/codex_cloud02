#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3"]
# ///
# How to run: uv run analysis/audit_training.py
"""Independent calendar, observation availability and paired-year audit."""

from __future__ import annotations

import calendar
import csv
import gzip
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from collections.abc import Iterator, Mapping
from datetime import date, timedelta
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "GLOSEA6_KMA_20220301-20260831_v1"
sys.path.insert(0, str(ROOT))

from analysis.data_io import observation_daily_path, observation_provenance


class DailyRecord(NamedTuple):
    """Supplied participating-station means and their independent QC metadata."""

    temperature: float
    precipitation: float
    temperature_stations: int
    precipitation_stations: int
    required_stations: int
    total_stations: int
    temperature_qc: str
    precipitation_qc: str


def observed(daily: Mapping[date, DailyRecord], start: date, end: date, variable: str) -> tuple[float | None, int]:
    """Require every day; use supplied means without imputing or rescaling."""
    count = (end - start).days + 1
    assert count > 0, f"Empty observation window {start}/{end}"
    period = [daily.get(start + timedelta(days=i)) for i in range(count)]
    if any(item is None for item in period):
        return None, 0
    present = [item for item in period if item is not None]
    rain = variable == "prcp"
    stations = [item.precipitation_stations if rain else item.temperature_stations for item in present]
    minimum = min(stations)
    for item, n in zip(present, stations, strict=True):
        if not 0 < item.required_stations <= n <= item.total_stations \
                or (item.precipitation_qc if rain else item.temperature_qc) != "OK" \
                or not math.isfinite(item.precipitation if rain else item.temperature):
            return None, minimum
    total = math.fsum(item.precipitation if rain else item.temperature for item in present)
    return (total if rain else total / count), minimum


def rows(path: Path) -> Iterator[Mapping[str, str]]:
    """Standalone parser; no production observation/window helper is imported."""
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as handle:
        yield from csv.DictReader(handle)


def ymd(value: str) -> date:
    return date(int(value[:4]), int(value[4:6]), int(value[6:8]))


def relative_window(initial: date, product: str, lead: str) -> tuple[date, date]:
    """Independent source-relative date arithmetic, not target-year substitution."""
    number = int(lead[1:])
    if product == "1mon":
        start = initial + timedelta(days=(number - 1) * 7)
        return start, start + timedelta(days=6)
    if product != "3mon":
        raise ValueError(f"Unknown product: {product}")
    absolute = initial.year * 12 + initial.month - 1 + number
    year, month_zero = divmod(absolute, 12)
    month = month_zero + 1
    return date(year, month, 1), date(year, month, calendar.monthrange(year, month)[1])


def sha(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def run() -> None:
    provenance = observation_provenance(DATA)
    fresh = bool(provenance["selected"])
    protected = [
        *sorted((ROOT / "outputs").glob("metrics_*.csv")),
        ROOT / "outputs/training_ledger.csv.gz", ROOT / "outputs/calibrated_members.csv.gz",
        ROOT / "outputs/matched_predictions.csv.gz", ROOT / "outputs/calibration_fits.csv",
        ROOT / "outputs/REPORT_KO.md", ROOT / "outputs/GLOSEA6_verification_by_dimension_KO_final.pdf",
        ROOT / "analysis/calibration.py", ROOT / "analysis/run_verification.py",
        ROOT / "analysis/data_io.py", ROOT / "analysis/scoring.py",
    ]
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in protected}
    original_cases = {r["CASE_ID"]: r for r in rows(DATA / "cases/verification_cases.csv")}
    cases = {r["CASE_ID"]: r for r in rows(ROOT / "outputs/case_audit.csv")}
    daily = {
        ymd(r["DATE"]): DailyRecord(
            float(r["T15M"]) if r["T15M"] else math.nan,
            float(r["PRCP"]) if r["PRCP"] else math.nan,
            int(r["N_STATION_T15M"]), int(r["N_STATION_PRCP"]),
            int(r["N_STATION_REQUIRED"]), int(r["N_STATION_TOTAL"]),
            r["QC_T15M"], r["QC_PRCP"],
        )
        for r in rows(observation_daily_path(DATA))
    }

    @lru_cache(maxsize=30000)
    def rebuilt(start: date, end: date, variable: str) -> tuple[float | None, int]:
        return observed(daily, start, end, variable)

    errors: list[str] = []
    accepted: dict[str, dict[int, Mapping[str, str]]] = defaultdict(dict)
    ledger_rows = 0
    historical_year_crossings = 0
    max_delta = 0.0
    for row in rows(ROOT / "outputs/training_ledger.csv.gz"):
        ledger_rows += 1
        if row["STATUS"] != "OK":
            continue
        key, year = row["CASE_ID"], int(row["SOURCE_YEAR"])
        case, original = cases[key], original_cases[key]
        initial = date.fromisoformat(row["INIT_DATE"])
        start, end = date.fromisoformat(row["HIST_START"]), date.fromisoformat(row["HIST_END"])
        source_initial = date(year, initial.month, initial.day)
        expected = relative_window(source_initial, case["PRODUCT"], case["LEAD"])
        value, stations = rebuilt(start, end, case["VARIABLE"])
        delta = abs(float(row["OBS"]) - value) if value is not None else math.inf
        max_delta = max(max_delta, delta)
        historical_year_crossings += int(start.year != year or end.year != year)
        target_year = date.fromisoformat(case["VALID_START"]).year
        checks = (
            (start, end) == expected, end < initial, year != target_year,
            target_year == int(row["TARGET_YEAR"]), initial == ymd(original["INIT_DATE"]),
            stations == int(row["N_STATION_MIN"]), value is not None, delta <= 1e-10,
            year not in accepted[key],
        )
        if not all(checks):
            errors.append(f"Historical join/availability/mean failed: {key}/{year}")
        accepted[key][year] = row
    counts: Counter[str] = Counter()
    paired_member_sizes: Counter[str] = Counter()
    ensemble_mismatch: Counter[str] = Counter()
    annual_members: dict[tuple[str, int], int] = defaultdict(int)
    historical_source_rows = 0
    for product in ("1mon", "3mon"):
        for variable in ("t15m", "prcp"):
            for row in rows(DATA / f"data/model/hcst_mapping/{product}_{variable}.csv.gz"):
                key, year = row["CASE_ID"], int(row["SOURCE_YEAR"])
                if year not in accepted.get(key, {}):
                    continue
                historical_source_rows += 1
                initial = date.fromisoformat(cases[key]["INIT_DATE"])
                if ymd(row["SOURCE_DATE"]) != date(year, initial.month, initial.day):
                    errors.append(f"Wrong hindcast source date: {key}/{year}")
                annual_members[key, year] += 1
    for key, years in accepted.items():
        case = cases[key]
        group = f"{case['PRODUCT']}_{case['VARIABLE']}"
        counts[group] += 1
        counts[f"{group}_training_years_{len(years)}"] += 1
        for year, record in years.items():
            n = annual_members[key, year]
            if n != int(record["MEMBERS"]):
                errors.append(f"Historical member count failed: {key}/{year}")
            paired_member_sizes[str(n)] += 1
            if n != int(case["FCST_VALID"]):
                ensemble_mismatch[group] += 1
    reference_seen: set[tuple[str, int]] = set()
    partial_reference_checks = 0
    partial_reference_differences: list[dict[str, str | int | float]] = []
    for reference in rows(DATA / "data/asos/asos_kma_period_reference.csv.gz"):
        key, year = reference["CASE_ID"], int(reference["REFERENCE_YEAR"])
        record = accepted.get(key, {}).get(year)
        if record is None:
            continue
        start, end = date.fromisoformat(record["HIST_START"]), date.fromisoformat(record["HIST_END"])
        value, stations = rebuilt(start, end, cases[key]["VARIABLE"])
        assert value is not None
        reference_value = float(reference["VALUE"])
        reference_stations = int(reference["N_STATION"])
        delta = abs(reference_value - value)
        reference_check = (
            "MATCHED" if delta <= 0.0001 else
            "NEW_OBSERVATION_SOURCE_DIFFERENCE" if fresh else "DAILY_MEAN_POLICY_DIFFERENCE"
        )
        if (key, year) in reference_seen \
                or (ymd(reference["HIST_START"]), ymd(reference["HIST_END"])) != (start, end) \
                or reference["VARIABLE"] != cases[key]["VARIABLE"] \
                or reference["PRODUCT"] != cases[key]["PRODUCT"] \
                or reference["LEAD"] != cases[key]["LEAD"] \
                or reference["AREA"] != "kma" or reference["AREA_VALID"] != "1" \
                or not 0 < int(reference["N_STATION_REQUIRED"]) <= reference_stations \
                <= int(reference["N_STATION_TOTAL"]) \
                or not math.isfinite(reference_value) \
                or not math.isfinite(float(record["REFERENCE_DIFF"])) \
                or abs(float(record["REFERENCE_DIFF"]) - delta) > 1e-10 \
                or record["REFERENCE_CHECK"] != reference_check \
                or (not fresh and stations == 62
                    and (reference_stations != stations or delta > 0.0001)):
            errors.append(f"Source period reference metadata/difference failed: {key}/{year}")
        reference_seen.add((key, year))
        if fresh or stations < 62:
            partial_reference_checks += 1
            if delta > 0.0001 or reference_stations != stations:
                partial_reference_differences.append({
                    "case_id": key, "source_year": year, "daily_stations": stations,
                    "reference_stations": reference_stations, "daily_value": value,
                    "reference_value": reference_value, "absolute_difference": delta,
                    "reference_check": reference_check,
                })
    if len(reference_seen) != sum(map(len, accepted.values())):
        errors.append("Source period reference coverage failed")
    target_periods: dict[str, set[tuple[str, str]]] = defaultdict(set)
    target_cases = 0
    for key, case in cases.items():
        if case["STATUS"] != "VERIFIED":
            continue
        target_cases += 1
        initial = date.fromisoformat(case["INIT_DATE"])
        start, end = date.fromisoformat(case["VALID_START"]), date.fromisoformat(case["VALID_END"])
        value, stations = rebuilt(start, end, case["VARIABLE"])
        if (start, end) != relative_window(initial, case["PRODUCT"], case["LEAD"]) \
                or value is None or stations != int(case["N_STATION_MIN"]) \
                or not math.isfinite(float(case["OBS"])) \
                or abs(value - float(case["OBS"])) > 1e-10 \
                or key not in accepted:
            errors.append(f"Target observation/membership failed: {key}")
        target_periods[f"{case['PRODUCT']}_{case['VARIABLE']}"].add((case["VALID_START"], case["VALID_END"]))
    for fit in rows(ROOT / "outputs/calibration_fits.csv"):
        key = fit["CASE_ID"]
        if len(accepted[key]) != int(fit["N_TRAIN"]) \
                or sorted(accepted[key]) != sorted(map(int, fit["SOURCE_YEARS"].split(";"))):
            errors.append(f"Saved fit training set failed: {key}")
    changed = [name for name, digest in hashes.items() if sha(ROOT / name) != digest]
    if changed:
        errors.append(f"Protected original artifacts changed: {changed}")
    report = {
        "observation_source": provenance,
        "status": "PASS" if not errors else "FAIL", "errors": errors,
        "supplied_cases": len(cases), "verified_cases": target_cases,
        "ledger_rows": ledger_rows, "accepted_annual_pairs": sum(map(len, accepted.values())),
        "historical_members_checked": historical_source_rows,
        "historical_windows_crossing_source_year": historical_year_crossings,
        "maximum_observation_difference": max_delta, "training_counts": dict(counts),
        "partial_station_references_checked": 0 if fresh else partial_reference_checks,
        "partial_station_reference_differences": [] if fresh else partial_reference_differences,
        "new_observation_source_references_checked": partial_reference_checks if fresh else 0,
        "new_observation_source_differences": partial_reference_differences if fresh else [],
        "historical_member_size_counts": dict(paired_member_sizes),
        "forecast_hindcast_member_count_mismatch_pairs": dict(ensemble_mismatch),
        "distinct_verified_target_periods": {k: len(v) for k, v in target_periods.items()},
        "source_hashes": hashes, "source_files_unchanged": not changed,
        "limits": [
            "Retrospective model version/data availability at historical initialization is not established.",
            "Selected participating-station means are not rescaled or imputed; station provenance is recorded separately.",
            "Member-count mismatch and overlapping windows are statistical issues, not observational look-ahead.",
        ],
    }
    destination = ROOT / "outputs/method_review"
    destination.mkdir(exist_ok=True)
    with (destination / "training_audit.json").open("w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2, allow_nan=False)
    print(json.dumps({k: report[k] for k in ("status", "verified_cases", "accepted_annual_pairs",
                                            "maximum_observation_difference", "errors")}), flush=True)
    if errors:
        raise SystemExit("Training audit failed; see outputs/method_review/training_audit.json")


def main() -> None:
    if sys.argv[1:] == ["--help"]:
        print("Usage: python analysis/audit_training.py\nIndependent calendar/QC/training availability audit.")
        return
    if sys.argv[1:]:
        raise SystemExit("Unexpected arguments; use --help")
    run()


if __name__ == "__main__":
    main()
