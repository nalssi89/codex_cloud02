"""Runnable exhaustive statistical comparison, preserving the published baseline."""

from __future__ import annotations

import os
from collections import Counter
from collections.abc import Sequence
from pathlib import Path

import numpy as np

from analysis.alternative_contracts import (
    CaseInput,
    JointTrainingSet,
    MethodSpec,
    TrainingSet,
)
from analysis.alternative_registry import method_registry
from analysis.alternative_runner_ancestry import actual_fold_rows
from analysis.alternative_runner_artifacts import write_numeric_laws
from analysis.alternative_runner_engine import (
    Engine,
    joint_scalar_ancestry,
    retained_joint_rows,
)
from analysis.alternative_runner_io import (
    Row,
    dumps,
    load_fit,
    training_rows,
    write_laws,
    write_rows,
    write_stream_rows,
)
from analysis.alternative_runner_tables import (
    collect,
    joint_case_statuses,
    json_object,
    json_objects,
    registry_rows,
    table_row,
)
from analysis.alternative_runner_types import Work
from analysis.data_io import Json
from analysis.scoring import generate_summaries


def build_outputs(engine: Engine, cases: tuple[CaseInput, ...],
                  selected: tuple[MethodSpec, ...], work: Sequence[Work],
                  results: Sequence[dict[str, Json]], joint_sets: Sequence[JointTrainingSet],
                  output: Path) -> dict[str, Json]:
    """Write actual saved tables and invoke the reporting owner's real implementation."""
    registry = method_registry()
    scalar_statuses = [table_row(result["status"]) for item, result in zip(work, results, strict=True)
                       if item.target is not None]
    joint_statuses = [table_row(result["status"]) for item, result in zip(work, results, strict=True)
                      if item.joint_training is not None]
    case_statuses = scalar_statuses + joint_case_statuses(cases, selected, work, results, engine.inputs)
    continuous, category, joint = (collect(results, key)
                                    for key in ("continuous", "category", "joint"))
    fit_records = collect(results, "fit")
    fits = {str(row["fit_ref"]): row for row in fit_records}
    training_sets = {training.train_hash: training for training in engine.scalar_training_sets()}
    joint_manifest: list[Row] = []
    joint_components: list[Row] = []
    for item in joint_sets:
        for component in joint_scalar_ancestry(item):
            _ = training_sets.setdefault(component.train_hash, component)
        joint_manifest.extend(retained_joint_rows(item))
        joint_components.append({
            "joint_train_hash": item.train_hash, "component_case_ids": dumps(item.component_keys),
            "source_years": dumps(item.source_years), "dimension": len(item.targets),
            "component_training_hashes": dumps(tuple(engine.cache.get(t, "local").train_hash
                                                     for t in item.targets)),
            "product": item.targets[0].product, "init": item.cutoff.isoformat(),
            "available_leads": dumps(tuple(dict.fromkeys(t.lead for t in item.targets))),
            "partial_horizon": int(len({t.lead for t in item.targets}) <
                                   (8 if item.targets[0].product == "1mon" else 6)),
        })
    # Local and vector component fits refer to independent original-unit ledgers;
    # joint vector hashes are not forged into scalar row content hashes.
    training_count = write_stream_rows(output / "training_ledger.csv.gz",
        (row for training in training_sets.values() for row in training_rows(training)), (
            "row_id", "train_hash", "source_case_id", "source_case_init", "source_year",
            "source_init", "hist_start", "hist_end", "product", "variable", "lead",
            "observation", "ensemble", "member_keys", "source_files", "provenance_hash",
            "archive_era", "cutoff", "catalog_cutoff", "held_out_years", "year_weight",
        ))
    fold_fits: dict[tuple[str, str], tuple[dict[str, Json], TrainingSet]] = {}
    for item, result in zip(work, results, strict=True):
        if item.target is None or "fit" not in result:
            continue
        fit = json_object(result["fit"])
        training = engine.cache.get(item.target, item.spec.fit_scope)
        ancestry_fit = load_fit(output, fit) if item.spec.surface == "category" else fit
        fold_fits[(str(fit["fit_ref"]), training.train_hash)] = (ancestry_fit, training)
    fold_count = write_stream_rows(output / "fold_ancestry.csv.gz",
        (row for fit, training in fold_fits.values() for row in actual_fold_rows(fit, training)), (
            "fold_id", "training_row_ids", "validation_row_ids", "pseudo_init",
            "held_out_years", "ancestor_hash", "outer_train_hash", "catalog_cutoff",
            "role",
        ))
    fit_table: list[Row] = []
    joint_fold_records: list[Row] = []
    actual_fit_records = {str(json_object(result["fit"])["fit_ref"]): json_object(result["fit"])
                          for result in results if "fit" in result}
    for row in fits.values():
        flattened = {key: value for key, value in row.items() if key != "model"}
        diagnostic_value = row.get("diagnostics")
        if isinstance(diagnostic_value, str):
            flattened["diagnostics"] = diagnostic_value
        diagnostic = actual_fit_records[str(row["fit_ref"])]["diagnostics"]
        if isinstance(diagnostic, dict):
            for name in ("convergence", "numerical_error", "posterior_diagnostics", "n_rows",
                         "n_years", "parameter_count", "objective", "elapsed_seconds", "message"):
                value = diagnostic.get(name)
                flattened[name] = dumps(value) if isinstance(value, (dict, list)) else value
        fit_table.append(flattened)
    for metadata in actual_fit_records.values():
        if metadata.get("method_id") in {
            "mbcp_annual", "mbcr_annual", "mbcn_annual",
            "residual_gaussian_copula__emos", "residual_gaussian_copula__bjp",
            "decc_path_shrunk_error__emos", "decc_path_shrunk_error__bjp",
        }:
            fit = load_fit(output, metadata)
            model = fit.get("model")
            if isinstance(model, dict):
                residual = model.get("residuals")
                if isinstance(residual, dict):
                    residual_folds = residual.get("folds")
                    if isinstance(residual_folds, list):
                        for fold in residual_folds:
                            joint_fold_records.append({
                                **table_row(fold), "fit_ref": str(fit["fit_ref"]),
                                "outer_joint_train_hash": str(fit["train_hash"]),
                            })
    laws = [json_object(result["law"]) for result in results if "law" in result]
    scenario_marginals: list[Row] = []
    analytic_marginals: list[Row] = []
    arrays: dict[str, np.ndarray[tuple[int, ...], np.dtype[np.float64]]] = {}
    for result in results:
        if "joint" in result:
            row = table_row(result["joint"])
            arrays[str(row["scenario_key"])] = np.asarray(result["samples"], dtype=np.float64)
            arrays[str(row["weights_key"])] = np.asarray(result["weights"], dtype=np.float64)
            scenario_marginals.extend(table_row(r) for r in json_objects(result["scenario_marginals"]))
            analytic_marginals.extend(table_row(r) for r in json_objects(result["analytic_marginals"]))
            laws.extend(json_objects(result["marginal_laws"]))
    write_rows(output / "method_inventory.csv", registry_rows(registry, case_statuses))
    write_rows(output / "case_method_status.csv.gz", case_statuses,
               ("case_id", "method_id", "status", "reason_code", "surface", "fit_ref"))
    write_rows(output / "joint_key_status.csv.gz", joint_statuses,
               ("case_id", "method_id", "status", "reason_code", "surface", "fit_ref"))
    write_rows(output / "fit_ledger.csv.gz", fit_table,
               ("fit_ref", "method_id", "status", "train_hash", "diagnostics"))
    write_rows(output / "joint_training_manifest.csv.gz", joint_manifest,
               ("joint_train_hash", "source_year", "component_case_ids", "row_ids"))
    write_rows(output / "joint_component_manifest.csv", joint_components,
               ("joint_train_hash", "component_case_ids", "source_years", "dimension"))
    write_rows(output / "joint_fold_ancestry.csv.gz", joint_fold_records,
               ("fold_id", "fit_ref", "outer_joint_train_hash", "ancestor_hash"))
    write_laws(output / "fitted_model_specs.jsonl.gz",
               (load_fit(output, fit) for fit in actual_fit_records.values()))
    write_laws(output / "distribution_specs.jsonl.gz", laws)
    write_numeric_laws(output, laws)
    common_columns = ("case_id", "method_id", "variable", "fit_ref", "CASE_ID", "METHOD",
                      "VARIABLE", "PRODUCT", "INIT_DATE", "VALID_START", "VALID_END",
                      "LEAD", "N_TRAIN", "OBS", "Q33", "Q67", "P_BN", "P_NN", "P_AN",
                      "BRIER", "RPS")
    write_rows(output / "continuous_predictions.csv.gz", continuous,
               (*common_columns, "PRED_MEAN", "CRPS", "P05", "P95"))
    write_rows(output / "category_predictions.csv.gz", category, common_columns)
    write_rows(output / "joint_predictions.csv.gz", joint,
               ("joint_id", "method_id", "scenario_key", "weights_key", "units",
                "approximation_metadata", "ENERGY", "VARIOGRAM", "HOT_DRY_P", "HOT_DRY_BRIER"))
    write_rows(output / "joint_scenario_marginals.csv.gz", scenario_marginals,
               (*common_columns, "joint_id", "PRED_MEAN", "CRPS"))
    write_rows(output / "joint_analytic_marginals.csv.gz", analytic_marginals,
               (*common_columns, "joint_id", "PRED_MEAN", "CRPS"))
    temporary = output / "joint_scenarios.tmp.npz"
    np.savez_compressed(temporary, allow_pickle=False, **arrays)
    os.replace(temporary, output / "joint_scenarios.npz")
    if continuous:
        generate_summaries(continuous, output)
    else:
        for name in ("overall", "by_lead", "by_season", "by_year", "by_month"):
            write_rows(output / f"metrics_{name}.csv", [],
                       ("PRODUCT", "VARIABLE", "METHOD", "N", "CRPS", "BRIER", "RPS"))
    return {
        "status_counts": dict(Counter(str(r["status"]) for r in case_statuses)),
        "continuous_rows": len(continuous), "category_rows": len(category),
        "joint_rows": len(joint), "fit_records": len(fit_table),
        "training_records": training_count, "fold_records": fold_count,
        "method_rows": dict(Counter(str(row["METHOD"]) for row in continuous)),
        "joint_key_status_counts": dict(Counter(str(r["status"]) for r in joint_statuses)),
    }
