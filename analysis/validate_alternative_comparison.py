"""Independent, read-only alternative experiment validation with honest coverage.

Only ``main`` writes, and only ``validation.json`` under the new output tree.
Missing implementations/artifacts never become PASS. Baseline outputs are read.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
import traceback
import warnings
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.alternative_validation_adversarial import (
    adversarial_checks,
    crossing_fold_checks,
)
from analysis.alternative_validation_ancestry import ancestry_checks, calendar_checks
from analysis.alternative_validation_baseline import baseline_checks
from analysis.alternative_validation_bayes import bayes_checks
from analysis.alternative_validation_distributions import production_checks
from analysis.alternative_validation_fit_edges import fit_edge_checks
from analysis.alternative_validation_inventory import REQUIRED_FILES, inventory_checks
from analysis.alternative_validation_io import preserved, safe_output
from analysis.alternative_validation_joint import coupling_checks
from analysis.alternative_validation_joint_scores import joint_score_checks
from analysis.alternative_validation_learning import learning_checks
from analysis.alternative_validation_metadata import metadata_checks, summary_checks
from analysis.alternative_validation_oracles import self_checks
from analysis.alternative_validation_posterior import posterior_checks
from analysis.alternative_validation_reference import reference_examples
from analysis.alternative_validation_schema import schema_checks
from analysis.alternative_validation_scores import joint_self_checks, score_checks
from analysis.alternative_validation_transport import mbc_checks, ot_checks
from analysis.data_io import Json

type ValidationSummary = dict[str, Json]


@dataclass
class Arguments:
    output: Path = Path("outputs/alternative_comparison")


def checked(name: str, action: Callable[[], dict[str, Json]],
            dependencies: tuple[str, ...] = ()) -> dict[str, Json]:
    started = time.perf_counter()
    missing: list[Json] = [module for module in dependencies
                           if importlib.util.find_spec(module) is None]
    if missing:
        return {"check": name, "status": "UNAVAILABLE", "missing_modules": missing,
                "elapsed_seconds": time.perf_counter()-started}
    numerical_warnings: list[warnings.WarningMessage] = []
    try:
        with warnings.catch_warnings(record=True) as numerical_warnings:
            warnings.simplefilter("always")
            details = action()
        status = details.get("status", "PASS")
        warning_messages: list[Json] = [
            {"category": warning.category.__name__, "message": str(warning.message),
             "source": warning.filename, "line": warning.lineno}
            for warning in numerical_warnings]
        if warning_messages:
            status = "FAIL"
        return {"check": name, "status": status, "details": details,
                "numerical_warnings": warning_messages,
                "elapsed_seconds": time.perf_counter()-started}
    except (AssertionError, ArithmeticError, ValueError, TypeError, OSError,
            ImportError, LookupError, AttributeError, RuntimeError) as error:
        return {"check": name, "status": "FAIL", "error": f"{type(error).__name__}: {error}",
                "traceback": traceback.format_exc(),
                "numerical_warnings": [
                    {"category": warning.category.__name__, "message": str(warning.message),
                     "source": warning.filename, "line": warning.lineno}
                    for warning in numerical_warnings],
                "elapsed_seconds": time.perf_counter()-started}


def validate(root: Path, output: Path) -> ValidationSummary:
    """Execute independent oracles and full saved-artifact checks; never write."""
    started = time.perf_counter()
    root, output = root.resolve(), output.resolve()
    safe_output(root, output)
    checks: list[Json] = []
    checks.append(checked("protected_60_before", lambda: preserved(root)))
    checks.append(checked("independent_known_laws", self_checks))
    checks.append(checked("independent_calendar_leap_year_guards", calendar_checks))
    checks.append(checked("SC2_independent_expected_reference_json", reference_examples))
    checks.append(checked("prototype_schema_roundtrip_adversarial", schema_checks,
                          ("analysis.alternative_data",)))
    checks.append(checked("independent_joint_energy_events", joint_self_checks))
    checks.append(checked("production_distribution_oracles", production_checks,
                          ("analysis.alternative_distributions",)))
    checks.append(checked("NIW_NIG_MNIW_independent", bayes_checks,
                          ("analysis.alternative_bayes_algebra",)))
    checks.append(checked("censored_likelihood_Rhat_ESS_MCSE", posterior_checks,
                          ("analysis.alternative_bayes_likelihood",
                           "analysis.alternative_bayes_diagnostics",
                           "analysis.alternative_bayes_distribution")))
    checks.append(checked("learning_Fisher_forest_IDR_ordinal", learning_checks,
                          ("analysis.alternative_learning_order", "analysis.alternative_data")))
    checks.append(checked("real_fit_sparse_wet_negative_rain_constant_M1", fit_edge_checks,
                          ("analysis.alternative_classical",)))
    checks.append(checked("truth_date_catalog_hash_adversarial", adversarial_checks,
                          ("analysis.alternative_data", "analysis.alternative_learning_order")))
    checks.append(checked("crossing_pooled_validation_SOURCE_year_block", crossing_fold_checks,
                          ("analysis.alternative_data",)))
    checks.append(checked("finite_coupling_physical_ids_residual_copula", coupling_checks,
                          ("analysis.alternative_joint_coupling",
                           "analysis.alternative_distributions")))
    checks.append(checked("MBC_saved_out_of_sample_replay", mbc_checks,
                          ("analysis.alternative_joint_mbc",)))
    checks.append(checked("OT_balanced_objective_historical_dynamic_blocks", ot_checks,
                          ("analysis.alternative_joint_ot",
                           "analysis.alternative_joint_ot_solver")))
    missing: list[Json] = [name for name in REQUIRED_FILES if not (output / name).is_file()]
    if missing:
        checks.append({"check": "full_saved_artifacts", "status": "UNAVAILABLE",
                       "missing_files": missing})
    else:
        checks.append(checked("full_subtype_failure_inventory",
                              lambda: inventory_checks(root, output)))
        checks.append(checked("training_pool_fold_ancestry", lambda: ancestry_checks(output)))
        checks.append(checked("computation_metadata_comparison_masks",
                              lambda: metadata_checks(output)))
        checks.append(checked("unchanged_unit_preserving_metric_summaries",
                              lambda: summary_checks(output)))
        checks.append(checked("SC2_every_saved_original_unit_score", lambda: score_checks(output)))
        checks.append(checked("SC2_every_saved_joint_energy_event",
                              lambda: joint_score_checks(output)))
        checks.append(checked("baseline_unchanged_issued_objects",
                              lambda: baseline_checks(root, output)))
    checks.append(checked("protected_60_after", lambda: preserved(root)))
    statuses = [check["status"] for check in checks if isinstance(check, dict)]
    complete = bool(statuses) and all(status == "PASS" for status in statuses)
    return {
        "validator_version": "independent-alternative-v1",
        "status": "PASS" if complete else "FAIL" if "FAIL" in statuses else "INCOMPLETE",
        "full_experiment_validated": complete,
        "root": str(root), "output": str(output), "checks": checks,
        "elapsed_seconds": time.perf_counter()-started,
        "warnings": [
            "Retain original tight QDM sensitivity warning; no thresholds relaxed.",
            "Frozen outer catalog is not a proof of real-time reforecast release.",
            "Baseline analytic laws are not discretized; finite coupling is separately labeled.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--output", type=Path, default=Path("outputs/alternative_comparison"),
                            help="new experiment directory below outputs; never baseline outputs")
    options = Arguments()
    _ = parser.parse_args(argv, namespace=options)
    root = Path(__file__).resolve().parents[1]
    try:
        safe_output(root, options.output)
    except ValueError as error:
        parser.error(str(error))
    result = validate(root, options.output)
    options.output.mkdir(parents=True, exist_ok=True)
    target = options.output / "validation.json"
    # JSON is the only output; no repaired/recomputed production artifacts.
    with target.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=True, allow_nan=False)
        _ = handle.write("\n")
    print(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False))
    return 0 if result["full_experiment_validated"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
