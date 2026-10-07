"""Read-only actual-export law identity and corruption regression; not FULL."""

from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter
from unittest.mock import patch

from analysis import alternative_validation_analytic_marginals as analytic
from analysis.alternative_validation_category import category_score
from analysis.alternative_validation_io import csv_records, json_lines
from analysis.alternative_validation_joint_scores import joint_score_checks
from analysis.alternative_validation_scores import score_checks
from analysis.data_io import Json


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    started = perf_counter()
    receipts: list[Json] = []
    for suffix in ("scalar_final", "monthly_final", "joint_final"):
        output = root / f"outputs/alternative_runner_smoke_{suffix}"
        before = {str(p): (p.stat().st_size, p.stat().st_mtime_ns)
                  for p in output.rglob("*") if p.is_file()}
        result = score_checks(output)
        marginal = result["analytic_joint_laws"]
        if not isinstance(marginal, dict):
            raise TypeError("missing analytic law receipt")
        receipts.append({"fixture": output.name, "status": result["status"],
                         "saved_laws": result["saved_laws"],
                         "scalar_saved_laws": result["scalar_saved_laws"],
                         "analytic_marginals": marginal["analytic_joint_marginals"],
                         "category_scores": result["category_scores"],
                         "joint_scores": joint_score_checks(output)
                         if suffix != "scalar_final" else "NO_JOINT_ROWS"})
        after = {str(p): (p.stat().st_size, p.stat().st_mtime_ns)
                 for p in output.rglob("*") if p.is_file()}
        if before != after:
            raise AssertionError("score validation mutated authentic exports")
    output = root / "outputs/alternative_runner_smoke_monthly_final"
    records = [r for r in json_lines(output / "distribution_specs.jsonl.gz") if "joint_id" in r]
    rejected = 0
    for variant in ("duplicate", "missing", "fit_ref"):
        altered = [dict(r) for r in records]
        if variant == "duplicate":
            altered.append(dict(altered[0]))
        elif variant == "missing":
            _ = altered.pop()
        else:
            altered[0]["fit_ref"] = "foreign-fit"
        try:
            _ = analytic.analytic_checks(output, altered)
        except (AssertionError, KeyError):
            rejected += 1
        else:
            raise AssertionError("corrupt analytic law identity accepted")
    for field in ("CRPS", "PRED_MEAN", "P05", "P_BN", "case_id", "fit_ref", "duplicate"):
        def corrupt(path: Path, field: str = field) -> list[dict[str, str]]:
            rows = csv_records(path)
            if path.name == "joint_analytic_marginals.csv.gz":
                if field == "duplicate":
                    rows.append(dict(rows[0]))
                elif field in ("case_id", "fit_ref"):
                    rows[0][field] = "foreign-source"
                else:
                    rows[0][field] = str(float(rows[0][field])+1000)
            return rows
        with patch.object(analytic, "csv_records", corrupt):
            try:
                _ = analytic.analytic_checks(output, records)
            except (AssertionError, KeyError):
                rejected += 1
            else:
                raise AssertionError("corrupt analytic marginal source/score accepted")
    tied = dict(csv_records(output / "joint_analytic_marginals.csv.gz")[0])
    tied.update(OBS="0", Q33="0", Q67="0", P_BN="1", P_NN="0", P_AN="0", BRIER="0", RPS="0")
    category_score(tied)
    tied.update(P_BN=".5", P_NN=".5")
    try:
        category_score(tied)
    except AssertionError:
        rejected += 1
    else:
        raise AssertionError("tied threshold positive middle mass accepted")
    print(json.dumps({"status": "PASS", "scope": "ACTUAL_SAVED_SCORE_SMOKE_NOT_FULL",
                      "receipts": receipts, "corruption_rejections": rejected,
                      "read_only": True, "tied_threshold_contract": "PASS",
                      "elapsed_seconds": perf_counter()-started}, indent=2))


if __name__ == "__main__":
    main()
