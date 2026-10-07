#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "scipy==1.18.1"]
# ///
# How to run: uv run analysis/audit_scoring_sensitivity.py
"""Labelled finite-ensemble sensitivity; never replace issued-distribution scores.

Run after rebuilding core outputs from the selected source (daily count >=50,
actual-n means including 61/60; no 62/n scaling or raw-station imputation).
Counts follow matched predictions, not the historical strict62 case total.
Independent observation-policy/calendar validation is a separate training audit.
"""

from __future__ import annotations

import csv
import gzip
import json
import math
import sys
from collections import defaultdict
from collections.abc import Iterator, Mapping
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analysis.data_io import DATASET, observation_daily_path, observation_provenance
from analysis.validate_results import day, observation_summary, parse_daily


def rows(path: Path) -> Iterator[Mapping[str, str]]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as handle:
        yield from csv.DictReader(handle)


def run() -> None:
    source = ROOT / DATASET
    provenance = observation_provenance(source)
    daily = {day(row["DATE"]): parse_daily(row)
             for row in rows(observation_daily_path(source))}
    members: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows(ROOT / "outputs/calibrated_members.csv.gz"):
        members[row["CASE_ID"], row["METHOD"]].append(float(row["VALUE"]))
    groups: dict[tuple[str, str, str], list[tuple[float, float, int]]] = defaultdict(list)
    case_ids: set[str] = set()
    maximum_difference = 0.0
    for row in rows(ROOT / "outputs/matched_predictions.csv.gz"):
        observed, stations = observation_summary(
            daily, day(row["VALID_START"]), day(row["VALID_END"]), row["VARIABLE"] == "prcp",
        )
        if observed is None or abs(observed - float(row["OBS"])) > 1e-10 \
                or stations != int(row["N_STATION"]):
            raise RuntimeError(f"Selected-source target observation mismatch: {row['CASE_ID']}")
        case_ids.add(row["CASE_ID"])
        issued = float(row["CRPS"])
        count = int(row["N_MEMBERS"])
        if row["METHOD"] == "EMOS":
            sensitivity = issued
        else:
            ensemble = sorted(members[row["CASE_ID"], row["METHOD"]])
            assert len(ensemble) == count > 1
            observation = float(row["OBS"])
            pair_term = math.fsum(
                (2 * index - count - 1) * value for index, value in enumerate(ensemble, 1)
            ) / count**2
            recomputed = math.fsum(abs(value - observation) for value in ensemble) / count - pair_term
            maximum_difference = max(maximum_difference, abs(recomputed - issued))
            assert abs(recomputed - issued) <= 1e-10
            sensitivity = recomputed - pair_term / (count - 1)
        groups[row["PRODUCT"], row["VARIABLE"], row["METHOD"]].append((issued, sensitivity, count))
    comparisons: list[Mapping[str, str | int | float]] = []
    for key, cases in sorted(groups.items()):
        product, variable, method = key
        comparisons.append({
            "product": product, "variable": variable, "method": method, "cases": len(cases),
            "issued_empirical_or_analytic_crps": math.fsum(v[0] for v in cases) / len(cases),
            "iid_fair_ensemble_sensitivity": math.fsum(v[1] for v in cases) / len(cases),
            "member_count_min": min(v[2] for v in cases),
            "member_count_max": max(v[2] for v in cases),
        })
    report = {
        "observation_source": provenance,
        "status": "PASS", "comparisons": comparisons,
        "cases_audited": len(case_ids),
        "observation_policy_scope": (
            "Selected-source outputs: daily station count >=50; "
            "use actual-n daily means, including 61/60; "
            "no 62/n scaling or raw-station imputation. "
            "Policy/calendar validation is a separate training audit."
        ),
        "maximum_issued_crps_recompute_difference": maximum_difference,
        "interpretation": (
            "Issued empirical CRPS is correct for discrete RAW/QM/QDM forecasts. "
            "EMOS is an analytic continuous/censored distribution. The alternate denominator "
            "M*(M-1), not M*M, removes a finite-sampling contribution only under suitable "
            "independent/exchangeable sampling assumptions, which this archive does not establish. "
            "This is sensitivity, NOT a corrected official score or proof of unfair comparison."
        ),
        "files_modified": ["outputs/method_review/scoring_sensitivity.json"],
    }
    destination = ROOT / "outputs/method_review"
    destination.mkdir(exist_ok=True)
    with (destination / "scoring_sensitivity.json").open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    print(json.dumps(report, indent=2), flush=True)


def main() -> None:
    if sys.argv[1:] == ["--help"]:
        print("Usage: python analysis/audit_scoring_sensitivity.py\nLabelled iid finite-ensemble CRPS sensitivity.")
        return
    if sys.argv[1:]:
        raise SystemExit("Unexpected arguments; use --help")
    run()


if __name__ == "__main__":
    main()
