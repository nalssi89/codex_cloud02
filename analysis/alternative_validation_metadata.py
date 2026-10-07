"""Saved computation identity, posterior quality and comparison-mask audit."""

from __future__ import annotations

import math
from pathlib import Path

from analysis.alternative_validation_io import (
    csv_records,
    decode,
    mapping,
    number,
    read_json,
    require_columns,
    require_metadata,
)
from analysis.alternative_validation_masks import paired_checks
from analysis.alternative_validation_oracles import close
from analysis.data_io import Json


def metadata_checks(output: Path) -> dict[str, Json]:
    summary = read_json(output / "run_summary.json")
    require_metadata(summary, (
        "scope", "active_provenance", "config", "dependency_versions", "seed",
        "protected_hashes_before", "protected_hashes_after", "expected_registry_entries",
        "attempted_registry_entries", "completed_registry_entries", "case_statuses",
        "timings", "cache_counts", "gate_receipts",
    ), "run summary")
    if summary["protected_hashes_before"] != summary["protected_hashes_after"]:
        raise AssertionError("runner preservation receipts changed")
    if number(summary["seed"]) != 20261007:
        config = mapping(summary["config"])
        if config.get("seed_override_explicit") is not True:
            raise AssertionError("changed seed not explicitly recorded")
    provenance = mapping(summary["active_provenance"])
    require_metadata(provenance, ("daily_sha256",), "active observations")
    if not provenance["daily_sha256"]:
        raise AssertionError("active observation hash missing")
    versions = mapping(summary["dependency_versions"])
    require_metadata(versions, ("python", "numpy", "scipy"), "dependencies")
    fits = csv_records(output / "fit_ledger.csv.gz")
    require_columns(fits, ("method_id", "status", "train_hash", "fit_hash", "algorithm_version",
                          "fixed_parameters", "seed", "posterior_diagnostics",
                          "convergence", "numerical_error"), "fit identity")
    seen: dict[str, tuple[str, ...]] = {}
    mcmc = 0
    for fit in fits:
        identity = (fit["method_id"], fit["train_hash"], fit["algorithm_version"],
                    fit["fixed_parameters"], fit["seed"])
        if fit["fit_hash"] in seen and seen[fit["fit_hash"]] != identity:
            raise AssertionError("cache fit hash collides across scientific identity")
        seen[fit["fit_hash"]] = identity
        if not fit["algorithm_version"] or not fit["fixed_parameters"] or not fit["fit_hash"]:
            raise AssertionError("incomplete version/fixed-parameter cache identity")
        _ = mapping(decode(fit["fixed_parameters"]))
        if fit["status"] != "OK":
            continue
        if fit["convergence"].lower() not in ("true", "1"):
            raise AssertionError("unconverged fit was labeled OK")
        if fit.get("model_spec"):
            _ = mapping(decode(fit["model_spec"]))
        else:
            expected_ref = f"cache/fits/{fit['fit_ref']}.json"
            if fit.get("model_ref") != expected_ref:
                raise AssertionError("model reference is not its content-keyed cache path")
            full = read_json(output / expected_ref)
            if full["fit_ref"] != fit["fit_ref"] or full["train_hash"] != fit["train_hash"]:
                raise AssertionError("persisted fitted model scientific identity differs")
            _ = mapping(full["model"])
        posterior = mapping(decode(fit["posterior_diagnostics"]))
        if "rhat_max" in posterior:
            mcmc += 1
            if (number(posterior["rhat_max"]) > 1.01
                    or number(posterior["ess_bulk_min"]) < 400
                    or number(posterior["ess_tail_min"]) < 400):
                raise AssertionError("OK posterior fails Rhat/ESS")
            if posterior.get("passed") is not True:
                raise AssertionError("OK posterior diagnostic result did not pass")
            if (posterior.get("predictive_mcse_passed") is not True
                    or posterior.get("importance_passed") is not True
                    or number(posterior["importance_effective_count"]) < 400
                    or number(posterior["maximum_weight"]) > .05):
                raise AssertionError("OK posterior predictive MCSE/importance gate failed")
            if number(posterior["chains"]) != 4 or number(posterior["warmup_per_chain"]) != 1024:
                raise AssertionError("posterior chain/warmup schedule changed")
        if fit["numerical_error"] and (
            not math.isfinite(float(fit["numerical_error"])) or float(fit["numerical_error"]) < 0
        ):
            raise AssertionError("invalid reported numerical error")
    paired = paired_checks(output)
    return {"status": "PASS", "fit_cache_identities": len(seen),
            "MCMC_posteriors_checked": mcmc, "pairwise_masks": paired}


def summary_checks(output: Path) -> dict[str, Json]:
    """Recompute unchanged summary-group counts/losses, never mix physical units."""
    predictions = csv_records(output / "continuous_predictions.csv.gz")
    dimensions = ("PRODUCT", "VARIABLE", "METHOD", "LEAD", "SEASON", "YEAR", "VALID_MONTH")
    require_columns(predictions, dimensions, "unchanged summary metadata")
    checked_groups = 0
    for name, keys in (
        ("overall", ("PRODUCT", "VARIABLE", "METHOD")),
        ("by_lead", ("PRODUCT", "VARIABLE", "LEAD", "METHOD")),
        ("by_season", ("PRODUCT", "VARIABLE", "SEASON", "METHOD")),
        ("by_year", ("PRODUCT", "VARIABLE", "YEAR", "METHOD")),
        ("by_month", ("PRODUCT", "VARIABLE", "VALID_MONTH", "METHOD")),
    ):
        groups: dict[tuple[str, ...], list[dict[str, str]]] = {}
        for prediction in predictions:
            groups.setdefault(tuple(prediction[key] for key in keys), []).append(prediction)
        table = csv_records(output / f"metrics_{name}.csv")
        require_columns(table, (*keys, "N", "CRPS", "BRIER", "RPS"), f"summary {name}")
        recorded: set[tuple[str, ...]] = set()
        for row in table:
            group = tuple(row[key] for key in keys)
            if group in recorded:
                raise AssertionError("duplicate summary group")
            recorded.add(group)
            actual = groups[group]
            if int(row["N"]) != len(actual):
                raise AssertionError("summary hides success-mask record count")
            for score in ("CRPS", "BRIER", "RPS"):
                expected = math.fsum(float(r[score]) for r in actual)/len(actual)
                close(float(row[score]), expected, "unchanged original-unit summary:"+score)
            checked_groups += 1
        if recorded != groups.keys():
            raise AssertionError("summary omits/adds unit-preserving group")
    return {"status": "PASS", "tables": 5, "groups": checked_groups}
