#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3"]
# ///
# How to run: uv run analysis/observations.py
"""Account for every issued case using source-QC participating-station means."""

from __future__ import annotations

import json
import sys
from collections import Counter
from collections.abc import Mapping
from pathlib import Path
from typing import TypedDict

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.data_io import (
    CsvCell,
    InputError,
    aggregate_observation,
    check_manifest,
    expected_window,
    load_cases,
    load_daily,
    load_forecasts,
    observation_provenance,
    prepare_inputs,
    write_csv,
)


class AuditGroup(TypedDict):
    product: str
    variable: str
    total: int
    status_counts: dict[str, int]
    missing_forecast_members: int


def audit_targets(root: Path) -> list[Mapping[str, CsvCell]]:
    """Use selected daily means; never infer unobserved or missing station values."""
    source = prepare_inputs(root)
    hashes = check_manifest(source)
    cases = load_cases(source)
    daily = load_daily(source)
    provenance = observation_provenance(source)
    output = root / "outputs"
    output.mkdir(exist_ok=True)
    audit: list[Mapping[str, CsvCell]] = []
    for product in ("1mon", "3mon"):
        for variable in ("t15m", "prcp"):
            forecasts = load_forecasts(source, product, variable)
            for case in cases:
                if (case.product, case.variable) != (product, variable):
                    continue
                issued = forecasts[case.case_id]
                if (issued.start, issued.end) != expected_window(case.init, product, case.lead):
                    raise InputError(f"Invalid forecast lead dates: {case.case_id}")
                if len(issued.members) + issued.missing_members != case.expected_members:
                    raise InputError(f"Manifest member count mismatch: {case.case_id}")
                observation = aggregate_observation(
                    daily, issued.start, issued.end, variable == "prcp",
                )
                status = observation.status
                if len(issued.members) < 2:
                    status = "INSUFFICIENT_FORECAST_MEMBERS"
                audit.append({
                    "CASE_ID": case.case_id, "INIT_DATE": case.init.isoformat(),
                    "PRODUCT": product, "LEAD": case.lead, "VARIABLE": variable,
                    "VALID_START": issued.start.isoformat(), "VALID_END": issued.end.isoformat(),
                    "DAYS": observation.days, "N_STATION_MIN": observation.min_stations,
                    "OBS": observation.value, "FCST_EXPECTED": case.expected_members,
                    "FCST_VALID": len(issued.members), "FCST_MISSING": issued.missing_members,
                    "STATUS": status,
                })
            del forecasts
    audit.sort(key=lambda row: str(row["CASE_ID"]))
    write_csv(output / "case_audit.csv", audit)
    write_csv(output / "observed_targets.csv", [r for r in audit if r["STATUS"] == "OK"])
    groups: list[AuditGroup] = []
    for product in ("1mon", "3mon"):
        for variable in ("t15m", "prcp"):
            subset = [r for r in audit if (r["PRODUCT"], r["VARIABLE"]) == (product, variable)]
            groups.append({
                "product": product, "variable": variable, "total": len(subset),
                "status_counts": dict(Counter(str(r["STATUS"]) for r in subset)),
                "missing_forecast_members": sum(int(str(r["FCST_MISSING"])) for r in subset),
            })
    information = {
        "dataset": source.name, "manifest_verified_files": len(hashes),
        "observation_source": provenance,
        "declared_stations": 62, "total_cases": len(audit),
        "eligible_target_cases": sum(r["STATUS"] == "OK" for r in audit),
        "daily_rows": len(daily),
        "observation_start": min(daily).isoformat(), "observation_end": max(daily).isoformat(),
        "forecast_init_start": min(c.init for c in cases).isoformat(),
        "forecast_init_end": max(c.init for c in cases).isoformat(),
        "daily_temperature_station_counts": dict(Counter(str(v[2]) for v in daily.values())),
        "daily_precipitation_station_counts": dict(Counter(str(v[3]) for v in daily.values())),
        "daily_required_station_counts": dict(Counter(str(v.required_stations) for v in daily.values())),
        "observation_policy": (
            "derived variable validity and >=50 contributors; not instrument/API QC; no imputation or rescaling"
            if provenance["selected"] else
            "original QC OK and actual contributors >= supplied daily minimum"
        ),
        "groups": groups,
        "station_mean_provenance": (
            ("Fresh KMA station means; see observation_source provenance. "
             if provenance["selected"] else
             "Supplied KMA station means; individual observations and weights absent. ") +
            "Use each day's actual participating-station mean (including 61/60 contributors) " +
            "when source eligibility is OK and the supplied minimum is met; no 62/n scaling or imputation."
        ),
    }
    with (output / "data_audit.json").open("w", encoding="utf-8") as handle:
        json.dump(information, handle, ensure_ascii=False, indent=2)
    print(json.dumps(information, ensure_ascii=False, indent=2), flush=True)
    return audit


def main() -> None:
    """A real data-audit entry point, not a dry-run."""
    if sys.argv[1:] == ["--help"]:
        print("Usage: python analysis/observations.py\nWrite source-QC case coverage and target observations.")
        return
    if sys.argv[1:]:
        raise SystemExit("Unexpected arguments; use --help")
    _ = audit_targets(Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    main()
