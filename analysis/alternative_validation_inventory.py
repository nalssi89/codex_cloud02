"""Frozen subtype inventory and failure-inclusive status accounting."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from analysis.alternative_validation_coverage import coverage_checks
from analysis.alternative_validation_io import csv_records, read_json, require_columns
from analysis.data_io import DATASET, Json

FAMILIES: dict[int, tuple[str, ...]] = {
    1: ("joint_gaussian_plugin", "bjp_niw", "bjp_sqrt_censored", "bayesian_anomaly_ridge",
        "bjp_yj_fixed", "bjp_logsinh_fixed"),
    2: ("cdf_mix_fixed50", "cdf_mix_cv", "anomaly_signal_shrink"),
    3: ("anomaly_mos", "emos_constant_variance", "mos_unit_slope"),
    4: ("gamma_positive", "csg_fixed_shift", "csg_estimated_shift"),
    5: ("power_gaussian_sqrt", "power_gaussian_cuberoot", "power_logistic_sqrt",
        "power_logistic_cuberoot"),
    6: ("hurdle_gamma", "hurdle_lognormal"),
    7: ("gev_censored_gumbel", "gev_censored_shrunk_shape", "tweedie_p15",
        "tweedie_selected_p"),
    8: ("kernel_normal_equal", "kernel_rain_hurdle_equal", "bma_group_normal",
        "bma_group_rain", "bma_component_pool"),
    9: ("pooled_mos_ridge", "pooled_emos_ridge", "pooled_emos_cyclic"),
    10: ("bjp_t", "bjp_ti", "detrend_qm", "detrend_qdm", "detrend_emos"),
    11: ("ordinal_logit", "elr_threshold_logit"),
    12: ("gamlss_ridge", "componentwise_boost", "ngboost_small"),
    13: ("qrf_year_forest", "idr_mean_order"),
    14: ("drn_small", "bqn_monotone"),
    15: ("schaake_window", "schaake_block", "ecc_q", "decc_path_shrunk_error",
         "residual_gaussian_copula"),
    16: ("mbjp_niw", "mbjp_sqrt_censored", "mbcp_annual", "mbcr_annual",
         "mbcn_annual", "otc_annual", "dotc_annual"),
    17: ("finite_member_iid_signal_noise", "finite_member_known_covariance"),
}
REQUIRED_IDS = frozenset(identifier for ids in FAMILIES.values() for identifier in ids)
STATUSES = frozenset((
    "OK", "NOT_APPLICABLE_DOMAIN", "GATED_DATA", "INSUFFICIENT_TRAINING",
    "INSUFFICIENT_INNER_FOLDS", "INPUT_CONFLICT", "FIT_FAILED",
    "POSTERIOR_DIAGNOSTICS_FAILED", "NUMERICAL_DISTRIBUTION_FAILED", "TARGET_UNAVAILABLE",
))
FAILURES = frozenset(("FIT_FAILED", "POSTERIOR_DIAGNOSTICS_FAILED",
                      "NUMERICAL_DISTRIBUTION_FAILED"))
RAIN_ONLY = frozenset((
    "bjp_sqrt_censored", "bjp_yj_fixed", "bjp_logsinh_fixed", *FAMILIES[4],
    *FAMILIES[5], *FAMILIES[6], *FAMILIES[7], "kernel_rain_hurdle_equal", "bma_group_rain",
))
TEMP_ONLY = frozenset((
    "joint_gaussian_plugin", "bjp_niw", "kernel_normal_equal", "bma_group_normal", *FAMILIES[17],
))
CLOSED_GATES = frozenset(("bma_group_normal", "bma_group_rain", *FAMILIES[17]))
REQUIRED_FILES = (
    "run_summary.json", "method_inventory.csv", "case_method_status.csv.gz",
    "training_ledger.csv.gz", "fit_ledger.csv.gz", "fit_schedule.csv", "fold_ancestry.csv.gz",
    "distribution_specs.jsonl.gz", "continuous_predictions.csv.gz",
    "category_predictions.csv.gz", "joint_predictions.csv.gz", "joint_scenarios.npz",
    "paired_comparison.csv", "coverage_and_failures.csv", "failure_inclusive_policy.csv",
    "equal_valid_window_metrics.csv", "category_metrics.csv", "joint_metrics.csv",
    "metrics_overall.csv", "metrics_by_lead.csv", "metrics_by_season.csv",
    "metrics_by_year.csv", "metrics_by_month.csv",
    "joint_training_manifest.csv.gz", "joint_component_manifest.csv",
    "joint_fold_ancestry.csv.gz",
)


def inventory_checks(root: Path, output: Path) -> dict[str, Json]:
    inventory = csv_records(output / "method_inventory.csv")
    require_columns(inventory, ("method_id", "family_no", "surface"), "inventory")
    ids = [row["method_id"] for row in inventory]
    if len(ids) != len(set(ids)):
        raise AssertionError("duplicate method IDs/aliases in inventory")
    missing = REQUIRED_IDS - set(ids)
    if missing:
        raise AssertionError(f"missing frozen subtypes: {sorted(missing)}")
    by_id = {row["method_id"]: row for row in inventory}
    for family, methods in FAMILIES.items():
        for method in methods:
            if int(by_id[method]["family_no"]) != family:
                raise AssertionError(f"{method}: wrong family")
    for method in FAMILIES[11]:
        if by_id[method]["surface"] != "category":
            raise AssertionError("category-only model masquerades as continuous")
    ledger = csv_records(output / "case_method_status.csv.gz")
    require_columns(ledger, ("case_id", "method_id", "status", "reason_code", "surface"),
                    "status ledger")
    keys = [(r["case_id"], r["method_id"]) for r in ledger]
    if len(keys) != len(set(keys)):
        raise AssertionError("duplicate terminal case/method records")
    for row in ledger:
        if row["status"] not in STATUSES:
            raise AssertionError(f"invalid status {row['status']}")
        if row["status"] != "OK" and not row["reason_code"]:
            raise AssertionError("non-OK terminal status lacks reason")
        if row["method_id"] not in by_id:
            raise AssertionError("status ledger references unregistered method")
    cases = {r["case_id"] for r in ledger if r.get("surface") != "joint"}
    supplied = {r["CASE_ID"] for r in csv_records(
        root / DATASET / "cases/verification_cases.csv")}
    if cases != supplied:
        raise AssertionError("terminal ledger silently omits/adds supplied cases")
    catalog = {r["CASE_ID"]: r["VARIABLE"] for r in csv_records(
        root / DATASET / "cases/verification_cases.csv")}
    observed = {r["CASE_ID"] for r in csv_records(root / "outputs/matched_predictions.csv.gz")}
    zero_history = {r["CASE_ID"] for r in csv_records(root / "outputs/training_ledger.csv.gz")
                    if float(r["OBS"]) == 0}
    for row in ledger:
        if row["surface"] == "joint" or row["method_id"] not in REQUIRED_IDS:
            continue
        method, case, status = row["method_id"], row["case_id"], row["status"]
        wrong_domain = ((method in RAIN_ONLY and catalog[case] != "prcp")
                        or (method in TEMP_ONLY and catalog[case] != "t15m"))
        if status == "NOT_APPLICABLE_DOMAIN" and not wrong_domain:
            raise AssertionError(f"{method}: applicable domain falsely excluded")
        if status == "TARGET_UNAVAILABLE" and case in observed:
            raise AssertionError("known observed target falsely excluded")
        if wrong_domain and status not in {"NOT_APPLICABLE_DOMAIN", "TARGET_UNAVAILABLE"}:
            raise AssertionError("wrong-domain method fitted/ranked")
        if status == "GATED_DATA" and not (
            method in CLOSED_GATES or (method == "gamma_positive" and case in zero_history)
        ):
            raise AssertionError(f"{method}: unexplained scientific/cost gate")
    expected = {(case, method) for case in cases for method in ids
                if by_id[method]["surface"] != "joint"}
    if not expected <= set(keys):
        raise AssertionError("missing case/method terminal combinations")
    summary = read_json(output / "run_summary.json")
    if summary.get("scope") != "FULL":
        raise AssertionError("full validation requires scope=FULL, not SMOKE")
    counters = Counter(r["status"] for r in ledger)
    _ = coverage_checks(root, output)
    fits = csv_records(output / "fit_ledger.csv.gz")
    require_columns(fits, ("method_id", "status", "train_hash"), "fit ledger")
    attempted = {r["method_id"] for r in fits}
    for method in REQUIRED_IDS:
        applicable = any(r["method_id"] == method and r["status"] not in {
            "NOT_APPLICABLE_DOMAIN", "GATED_DATA", "TARGET_UNAVAILABLE"} for r in ledger)
        if applicable and method not in attempted:
            raise AssertionError(f"{method}: applicable but no actual fit record")
    policy = csv_records(output / "failure_inclusive_policy.csv")
    require_columns(policy, ("method_id", "policy", "eligible_count", "scored_count"), "policy")
    for row in policy:
        if (row["policy"].endswith("+climatology_on_failure")
                and int(row["eligible_count"]) != int(row["scored_count"])):
            raise AssertionError("failure-inclusive policy hides missing forecasts")
    return {"status": "PASS", "required_subtypes": len(REQUIRED_IDS),
            "families": 17, "terminal_records": len(ledger),
            "status_counts": dict(counters)}
