"""Real protected-baseline reporting smoke and independent arithmetic checks.

No new-method skill is fabricated. Artificial losses only test machine arithmetic,
separately from the copied read-only baseline reporting fixture.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path

import numpy as np

from analysis.alternative_catalog import load_experiment
from analysis.alternative_experiment_types import ExperimentInputs, ScoreTruth
from analysis.alternative_reporting import generate_reports
from analysis.alternative_reporting_common import (
    Row,
    identity,
    mask_hash,
    method,
    number,
    save_json,
    save_rows,
    text,
)
from analysis.alternative_reporting_fairness import (
    climate_loss,
    common_masks,
    coverage,
    policies,
)
from analysis.alternative_reporting_joint import climate as joint_climate
from analysis.alternative_reporting_joint import metadata as joint_metadata
from analysis.alternative_reporting_joint import policies as joint_policies
from analysis.alternative_reporting_statistics import summaries
from analysis.alternative_validation_io import preserved
from analysis.alternative_validation_joint_scores import energy_variogram
from analysis.data_io import csv_rows


def arithmetic(inputs: ExperimentInputs, records: list[Row], statuses: list[Row]) -> dict[str, int | str]:
    """Independent sums, O(n²) empirical CRPS, tied probability and mask receipt."""
    first = records[0]
    case_id = identity(first)
    truth = inputs.truths[case_id]
    history = truth.historical_observations
    oracle = (math.fsum(abs(float(history.item(i))-truth.observation) for i in range(len(history)))/len(history)
              - math.fsum(abs(float(history.item(i))-float(history.item(j)))
                          for i in range(len(history)) for j in range(len(history)))/(2*len(history)**2))
    assert abs(climate_loss(inputs, case_id, "CRPS")-oracle) < 1e-12
    failed = [{**r, "status": "FIT_FAILED"} if identity(r) == case_id and method(r) == method(first)
              else dict(r) for r in statuses]
    predictions = [r for r in records if not (identity(r) == case_id and method(r) == method(first))]
    counts = coverage(inputs, failed, predictions, {"RAW", "QM", "QDM", "EMOS"})
    policy, detail = policies(inputs, predictions, failed, counts)
    target = next(r for r in policy if method(r) == method(first) and text(r, "score") == "CRPS"
                  and text(r, "PRODUCT") == text(first, "PRODUCT")
                  and text(r, "VARIABLE") == text(first, "VARIABLE"))
    eligible = [c.case_id for c in inputs.cases if c.product == text(first, "PRODUCT")
                and c.variable == text(first, "VARIABLE") and c.case_id in inputs.truths]
    successful = [float(str(r["CRPS"])) for r in predictions if method(r) == method(first)
                  and text(r, "PRODUCT") == text(first, "PRODUCT")
                  and text(r, "VARIABLE") == text(first, "VARIABLE")]
    assert number(target, "mean_loss") is not None
    assert abs(float(str(target["mean_loss"]))-(math.fsum(successful)+oracle)/len(eligible)) < 1e-12
    assert abs(float(str(target["lower_bound"]))-math.fsum(successful)/len(eligible)) < 1e-12
    assert target["upper_bound"] == "+inf"
    assert any(r["source"] == "climatology_on_failure" and r["original_status"] == "FIT_FAILED"
               for r in detail)
    _, masks = common_masks(predictions, counts, ("CRPS",), "continuous")
    pair = next(r for r in masks if text(r, "mask_kind") == "pairwise" and
                text(r, "methods") == '["QM", "RAW"]' and text(r, "PRODUCT") == text(first, "PRODUCT")
                and text(r, "VARIABLE") == text(first, "VARIABLE"))
    expected = sorted(set(eligible)-{case_id}) if method(first) in {"RAW", "QM"} else sorted(eligible)
    digest = hashlib.sha256(json.dumps(expected, separators=(",", ":")).encode()).hexdigest()
    assert pair["mask_hash"] == digest
    assert mask_hash(reversed(expected)) == digest
    toy: list[Row] = [
        {"CASE_ID": "a", "METHOD": "RAW", "PRODUCT": "1mon", "VARIABLE": "t15m",
         "VALID_START": "2022-01-01", "VALID_END": "2022-01-07", "CRPS": 2},
        {"CASE_ID": "b", "METHOD": "RAW", "PRODUCT": "1mon", "VARIABLE": "t15m",
         "VALID_START": "2022-01-01", "VALID_END": "2022-01-07", "CRPS": 4},
        {"CASE_ID": "c", "METHOD": "RAW", "PRODUCT": "1mon", "VARIABLE": "t15m",
         "VALID_START": "2022-01-08", "VALID_END": "2022-01-14", "CRPS": 9},
    ]
    _, weighted = summaries(toy, ("CRPS",), "continuous")
    assert number(weighted[0], "mean_loss") == 6
    tied_truth = ScoreTruth(case_id=case_id, observation=0.,
                           historical_observations=np.asarray([0., 0., 0., 1.], dtype=np.float64),
                           thresholds=np.asarray([0., 0.], dtype=np.float64))
    tied = replace(inputs, truths={case_id: tied_truth})
    assert climate_loss(tied, case_id, "BRIER") == .125
    assert climate_loss(tied, case_id, "RPS") == .125
    pairs = [(a, b) for a in inputs.cases for b in inputs.cases if a.variable == "t15m"
             and b.variable == "prcp" and a.product == b.product
             and (a.valid_start, a.valid_end) == (b.valid_start, b.valid_end)
             and a.case_id in inputs.truths and b.case_id in inputs.truths]
    a, b = pairs[0]
    joint_ids = [a.case_id, b.case_id]
    # An actual annual climate fallback, never an invented new-method skill value.
    joint_state: Row = {"case_id": "REPORTING_ARITHMETIC_REAL_PAIR", "method_id": "schaake_window__emos",
                        "surface": "joint", "status": "FIT_FAILED",
                        "component_case_ids": json.dumps(joint_ids)}
    state = joint_metadata([joint_state], [], inputs)[0]
    law_losses = joint_climate(inputs, state)
    histories = [{r.source_year: r.observation for r in inputs.historical[i]} for i in joint_ids]
    years = sorted(set(histories[0]) & set(histories[1]))
    samples = np.asarray([[h[y] for h in histories] for y in years], dtype=np.float64)
    observed = np.asarray([inputs.truths[i].observation for i in joint_ids], dtype=np.float64)
    centers = np.asarray(np.mean(samples, axis=0), dtype=np.float64)
    scales = np.asarray(np.maximum(1., np.std(samples, axis=0, ddof=1)), dtype=np.float64)
    weights = np.full(len(years), 1/len(years), dtype=np.float64)
    oracle_energy, oracle_variogram = energy_variogram(samples, weights, observed, centers, scales)
    assert abs(float(str(law_losses["ENERGY"]))-oracle_energy) < 1e-12
    assert abs(float(str(law_losses["VARIOGRAM"]))-oracle_variogram) < 1e-12
    joint_count: Row = {"PRODUCT": state["PRODUCT"], "VARIABLE": state["VARIABLE"], "surface": "joint",
                       "method_id": method(state), "eligible_ids": json.dumps([identity(state)])}
    result, _ = joint_policies(inputs, [], [state], [joint_count], ("ENERGY", "VARIOGRAM", "HOT_DRY_BRIER"))
    assert all(r["fallback_count"] == 1 and r["scored_count"] == r["eligible_count"] == 1
               and r["policy_status"] == "COMPLETE" for r in result)
    return {"status": "PASS", "independent_arithmetic_assertions": 13}


def run(root: Path, output: Path) -> Mapping[str, object]:
    before = preserved(root)
    assert before["status"] == "PASS"
    actual = load_experiment(root)
    grouped: dict[tuple[str, str, int], list[str]] = defaultdict(list)
    for case in actual.cases:
        if case.case_id in actual.truths:
            grouped[(case.product, case.variable, case.valid_start.year)].append(case.case_id)
    retained = {i for ids in grouped.values() for i in ids[:12]}
    # Keep actual unavailable observations visible, one per product/variable where present.
    unavailable: dict[tuple[str, str], str] = {}
    for case in actual.cases:
        if case.case_id not in actual.truths:
            _ = unavailable.setdefault((case.product, case.variable), case.case_id)
    retained.update(unavailable.values())
    fixture = ExperimentInputs(
        root=actual.root, source=actual.source,
        cases=tuple(c for c in actual.cases if c.case_id in retained),
        historical={i: actual.historical[i] for i in retained if i in actual.historical},
        truths={i: actual.truths[i] for i in retained if i in actual.truths},
        excluded_cases={i: actual.excluded_cases[i] for i in retained if i in actual.excluded_cases},
        provenance=actual.provenance,
    )
    records: list[Row] = [dict(r) for r in csv_rows(root / "outputs/matched_predictions.csv.gz")
                         if r["CASE_ID"] in retained]
    statuses: list[Row] = [
        {"case_id": c.case_id, "method_id": m, "surface": "continuous", "fit_ref": "READ_ONLY_BASELINE",
         "status": "OK" if c.case_id in fixture.truths else "TARGET_UNAVAILABLE", "reason_code": ""}
        for c in fixture.cases for m in ("RAW", "QM", "QDM", "EMOS")
    ]
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError("Smoke fixture output must be new and empty")
    save_json(output / "run_summary.json", {"scope": "REPORTING_SMOKE", "seed": 20261007,
                                          "source": "protected real baseline, no new model fits"})
    save_rows(output / "method_inventory.csv",
              [{"method_id": m, "family_no": 0, "surface": "continuous"}
               for m in ("RAW", "QM", "QDM", "EMOS")])
    # Generated fixture tables are legitimate runtime artifacts, never source edits.
    for name, content in (("continuous_predictions.csv.gz", records),
                          ("case_method_status.csv.gz", statuses)):
        temporary = output / "fixture-table.csv"
        save_rows(temporary, content)
        with gzip.open(output / name, "wb") as handle:
            _ = handle.write(temporary.read_bytes())
        temporary.unlink()
    summary = generate_reports(output, fixture)
    assert summary["scope"] == "REPORTING_SMOKE" and summary["status"] == "INCOMPLETE"
    assert summary["missing_or_error_laws"] == len(records)
    first_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in (output / "reports").iterdir()}
    repeated = generate_reports(output, fixture)
    assert repeated == summary
    second_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in (output / "reports").iterdir()}
    assert first_hashes == second_hashes
    checks = arithmetic(fixture, records, statuses)
    after = preserved(root)
    assert after == before
    receipt = {"status": "PASS", "scope": "REPORTING_SMOKE_NOT_FULL",
               "real_baseline_rows": len(records), "actual_cases": len(fixture.cases),
               "actual_years": sorted({c.valid_start.year for c in fixture.cases}),
               "report_status": summary["status"], "arithmetic": checks,
               "byte_deterministic_report_files": len(first_hashes),
               "protected_files_unchanged": 60}
    # Receipt JSON is already composed exclusively of scalar/list/dict machine values.
    encoded = json.dumps(receipt, indent=2, sort_keys=True)
    _ = (output / "reporting_smoke_receipt.json").write_text(encoded+"\n", encoding="utf-8")
    return receipt


def main() -> None:
    class Arguments(argparse.Namespace):
        output: Path = Path()
        root: Path = Path()

    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--output", required=True, type=Path)
    _ = parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(namespace=Arguments())
    print(json.dumps(run(args.root, args.output), sort_keys=True))


if __name__ == "__main__":
    main()
