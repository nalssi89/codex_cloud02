#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "scipy==1.18.1"]
# ///
# How to run: uv run analysis/run_verification.py
"""Verify all supplied forecasts using historical-only calibration."""

from __future__ import annotations

import csv
import gzip
import json
import sys
import time
from collections import Counter
from collections.abc import Mapping
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.calibration import FloatArray, calibrate, gaussian_crps
from analysis.data_io import (
    CsvCell,
    InputError,
    aggregate_observation,
    expected_window,
    load_cases,
    load_daily,
    load_forecasts,
    load_hindcasts,
    load_references,
    observation_provenance,
    prepare_inputs,
    write_csv,
)
from analysis.observations import audit_targets
from analysis.scoring import (
    array_mean,
    distribution_summary,
    empirical_crps,
    generate_summaries,
    score_prediction,
    tercile_probabilities,
)


def run(root: Path) -> None:
    """A complete reproducible run; no provided corrected outputs are consumed."""
    started = time.perf_counter()
    audit = audit_targets(root)
    audit_by_key = {str(row["CASE_ID"]): dict(row) for row in audit}
    source, output = prepare_inputs(root), root / "outputs"
    daily, references, cases = load_daily(source), load_references(source), load_cases(source)
    provenance = observation_provenance(source)
    predictions: list[Mapping[str, CsvCell]] = []
    training_ledger: list[Mapping[str, CsvCell]] = []
    fits: list[Mapping[str, CsvCell]] = []
    with gzip.open(output / "calibrated_members.csv.gz", "wt", encoding="utf-8-sig", newline="") as handle:
        members_writer = csv.writer(handle)
        members_writer.writerow(["CASE_ID", "METHOD", "MEMBER_INDEX", "VALUE"])
        for product in ("1mon", "3mon"):
            for variable in ("t15m", "prcp"):
                forecasts = load_forecasts(source, product, variable)
                hindcasts = load_hindcasts(source, product, variable)
                precipitation = variable == "prcp"
                selected = [c for c in cases if (c.product, c.variable) == (product, variable)]
                print(f"PROCESS {product} {variable}: {len(selected)} supplied cases", flush=True)
                completed = 0
                for case in selected:
                    target = audit_by_key[case.case_id]
                    if target["STATUS"] != "OK":
                        continue
                    forecast = forecasts[case.case_id]
                    historic_ensembles: list[FloatArray] = []
                    historic_values: list[float] = []
                    accepted_years: list[int] = []
                    for year, ensemble in sorted(hindcasts[case.case_id].items()):
                        reference = references[case.case_id][year]
                        source_init = date(year, case.init.month, case.init.day)
                        if (reference.start, reference.end) != expected_window(source_init, product, case.lead):
                            raise InputError(f"Historical lead calendar mismatch: {case.case_id}/{year}")
                        historical_observation = aggregate_observation(
                            daily, reference.start, reference.end, precipitation,
                        )
                        reason = historical_observation.status
                        if reference.end >= case.init:
                            reason = "HISTORICAL_OBSERVATION_NOT_KNOWN_AT_INIT"
                        if year == forecast.start.year:
                            reason = "HELD_OUT_TARGET_YEAR"
                        value = historical_observation.value
                        delta = abs(value - reference.value) if value is not None else None
                        if reason == "OK" and (
                            value is None or delta is None or not np.isfinite(delta)
                            or (not provenance["selected"]
                                and historical_observation.min_stations == 62 and delta > 0.0001)
                        ):
                            raise InputError(f"Daily/reference observation mismatch: {case.case_id}/{year}")
                        reference_check = (
                            "OBSERVATION_UNAVAILABLE" if delta is None else
                            "MATCHED" if delta <= 0.0001 else
                            "NEW_OBSERVATION_SOURCE_DIFFERENCE" if provenance["selected"] else
                            "DAILY_MEAN_POLICY_DIFFERENCE"
                        )
                        training_ledger.append({
                            "CASE_ID": case.case_id, "SOURCE_YEAR": year,
                            "HIST_START": reference.start.isoformat(), "HIST_END": reference.end.isoformat(),
                            "INIT_DATE": case.init.isoformat(), "TARGET_YEAR": forecast.start.year,
                            "MEMBERS": len(ensemble), "N_STATION_MIN": historical_observation.min_stations,
                            "OBS": value, "REFERENCE_DIFF": delta,
                            "REFERENCE_CHECK": reference_check, "STATUS": reason,
                        })
                        if reason == "OK" and value is not None:
                            historic_ensembles.append(ensemble)
                            historic_values.append(value)
                            accepted_years.append(year)
                    if len(accepted_years) < 10:
                        target["STATUS"] = "INSUFFICIENT_TRAINING_YEARS"
                        continue
                    historical = np.asarray(historic_values, dtype=np.float64)
                    result = calibrate(forecast.members, tuple(historic_ensembles), historical, precipitation)
                    a, b, c, d = result.parameters
                    fits.append({
                        "CASE_ID": case.case_id, "PRODUCT": product, "VARIABLE": variable,
                        "N_TRAIN": len(accepted_years), "SOURCE_YEARS": ";".join(map(str, accepted_years)),
                        "A": a, "B": b, "C": c, "D": d, "MU": result.mu, "SIGMA": result.sigma,
                        "CONVERGED": int(result.converged), "FIT_CRPS": result.fit_crps,
                        "INITIAL_CRPS": result.initial_crps, "QDM_DRY_EXCEPTIONS": result.dry_exceptions,
                        "OPTIMIZER_MESSAGE": result.optimizer_message,
                    })
                    if not result.converged:
                        target["STATUS"] = "EMOS_FIT_FAILED"
                        continue
                    target["STATUS"] = "VERIFIED"
                    observed_cell = target["OBS"]
                    if observed_cell is None:
                        raise InputError(f"Eligible observation absent: {case.case_id}")
                    observed = float(observed_cell)
                    thresholds = np.quantile(historical, [1 / 3, 2 / 3])
                    common: dict[str, CsvCell] = {
                        "CASE_ID": case.case_id, "INIT_DATE": case.init.isoformat(),
                        "PRODUCT": product, "VARIABLE": variable, "LEAD": case.lead,
                        "VALID_START": forecast.start.isoformat(), "VALID_END": forecast.end.isoformat(),
                        "YEAR": forecast.start.year, "VALID_MONTH": forecast.start.month,
                        "SEASON": ("DJF", "MAM", "JJA", "SON")[(forecast.start.month % 12) // 3],
                        "N_MEMBERS": len(forecast.members), "N_TRAIN": len(accepted_years),
                        "N_STATION": target["N_STATION_MIN"],
                    }
                    for method, ensemble in (
                        ("RAW", forecast.members), ("QM", result.qm), ("QDM", result.qdm),
                    ):
                        scored = score_prediction(
                            array_mean(ensemble), empirical_crps(ensemble, observed),
                            tercile_probabilities(ensemble, thresholds),
                            np.quantile(ensemble, [0.05, 0.95]), observed, historical, thresholds,
                        )
                        predictions.append({
                            **common, "METHOD": method, **scored, "EMOS_MU": None, "EMOS_SIGMA": None,
                        })
                        for index, member in enumerate(ensemble.flat, 1):
                            members_writer.writerow([case.case_id, method, index, float(member)])
                    mean, probabilities, quantiles = distribution_summary(
                        result.mu, result.sigma, thresholds, precipitation,
                    )
                    score = gaussian_crps(
                        np.array([result.mu]), np.array([result.sigma]),
                        np.array([observed]), precipitation,
                    )
                    scored = score_prediction(
                        mean, float(score.flat[0]), probabilities, quantiles, observed, historical, thresholds,
                    )
                    predictions.append({
                        **common, "METHOD": "EMOS", **scored,
                        "EMOS_MU": result.mu, "EMOS_SIGMA": result.sigma,
                    })
                    completed += 1
                    if completed % 100 == 0:
                        print(f"PROGRESS {product} {variable}: {completed} verified", flush=True)
                print(f"FINISHED {product} {variable}: {completed} verified", flush=True)
                del forecasts, hindcasts
    write_csv(output / "case_audit.csv", list(audit_by_key.values()))
    write_csv(output / "matched_predictions.csv.gz", predictions)
    write_csv(output / "training_ledger.csv.gz", training_ledger)
    write_csv(output / "calibration_fits.csv", fits)
    generate_summaries(predictions, output)
    summary = {
        "status": "PASS" if all(r["CONVERGED"] for r in fits) else "FIT_FAILURES",
        "observation_source": provenance,
        "reference_check_counts": dict(Counter(str(r["REFERENCE_CHECK"]) for r in training_ledger)),
        "cases_accounted": len(audit_by_key), "cases_verified": len(predictions) // 4,
        "method_rows": dict(Counter(str(r["METHOD"]) for r in predictions)),
        "case_status_counts": dict(Counter(str(r["STATUS"]) for r in audit_by_key.values())),
        "training_rows": len(training_ledger),
        "fitted_cases": len(fits), "fit_failures": sum(not r["CONVERGED"] for r in fits),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "calibration_protocol": "same-case source-year pairs; HIST_END < INIT_DATE; SOURCE_YEAR != target year",
        "observation_policy": (
            "derived variable validity and >=50 contributors; not instrument/API QC; no imputation or rescaling"
            if provenance["selected"] else
            "original QC OK; supplied minimum met; actual daily means without 62/n scaling"
        ),
        "probability_reference": "training observational terciles, linear quantile 1/3 and 2/3",
        "random_seed": None,
    }
    with (output / "run_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
    print("VERIFICATION_SUMMARY " + json.dumps(summary, ensure_ascii=False), flush=True)
    if summary["fit_failures"]:
        raise SystemExit("Some EMOS fits failed: see calibration_fits.csv")


def main() -> None:
    """Run the real pipeline, or show usage; reject unknown input flags."""
    if sys.argv[1:] == ["--help"]:
        print("Usage: python analysis/run_verification.py\n" +
              "Verify RAW, QM, QDM and EMOS on all source-QC-valid cases; write outputs/.")
        return
    if sys.argv[1:]:
        raise SystemExit("Unexpected arguments; use --help")
    run(Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    main()
