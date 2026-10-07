"""Runnable exhaustive statistical comparison, preserving the published baseline."""

from __future__ import annotations

import argparse
import importlib.metadata
import os
import platform
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import perf_counter

# Set before importing NumPy/SciPy/Torch, including when this file is a CLI script.
for _thread_variable in (
    "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS",
):
    os.environ[_thread_variable] = "1"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


from analysis.alternative_contracts import (
    FitConfig,
)
from analysis.alternative_data import load_experiment
from analysis.alternative_registry import method_registry
from analysis.alternative_runner_engine import (
    Engine,
    check_catalog_immutability,
)
from analysis.alternative_runner_io import (
    check_output,
    digest,
    dumps,
    json_value,
    known_input,
    protected_hashes,
    source_hashes,
    write_json,
    write_rows,
)
from analysis.alternative_runner_metadata import case_statuses, complete_metadata
from analysis.alternative_runner_outputs import build_outputs
from analysis.alternative_runner_reporting import (
    publish_reports,
    refresh_completed_reports,
)
from analysis.alternative_runner_schedule import build_schedule
from analysis.alternative_runner_tables import json_object
from analysis.alternative_runner_types import RunOptions, Work
from analysis.alternative_validation_io import read_json
from analysis.data_io import Json

type RunSummary = dict[str, Json]

def _execute(engine: Engine, work: Work) -> dict[str, Json]:
    if work.target is not None:
        return engine.scalar(work.target, work.spec)
    if work.joint_training is not None:
        return engine.joint(work.joint_training, work.spec, work.marginal)
    raise ValueError("Work must identify one real scalar or joint input")



def run(root: Path, output: Path, options: RunOptions) -> RunSummary:
    """Execute every requested algorithm; subsets explicitly remain SMOKE."""
    started = perf_counter()
    root, output = root.resolve(), output.resolve()
    if not 1 <= options.workers <= 6:
        raise ValueError("--workers must be in 1..6")
    registry = method_registry()
    registered = {spec.id for spec in registry}
    unknown = set(options.methods) - registered
    if unknown:
        raise ValueError(f"Unknown methods: {','.join(sorted(unknown))}")
    check_output(root, output, options.resume)
    before = protected_hashes(root)
    sources = source_hashes(root)
    inputs = load_experiment(root)
    supplied = {target.case_id for target in inputs.cases}
    if set(options.case_ids) - supplied:
        raise ValueError(f"Unknown case IDs: {','.join(sorted(set(options.case_ids) - supplied))}")
    immutable_before = check_catalog_immutability(inputs)
    absent = read_json(root / ".omo/evidence/alternative-latest-absent-history.json")
    absent_ids = absent["case_ids"]
    if not isinstance(absent_ids, list) or len(absent_ids) != 16:
        raise ValueError("Expected 16 frozen latest absent-history component keys")
    if not all(isinstance(case_id, str) and case_id in supplied
               and case_id not in inputs.historical for case_id in absent_ids):
        raise ValueError("Latest absent-history receipt disagrees with actual catalog")
    selected = tuple(spec for spec in registry if not options.methods or spec.id in options.methods)
    cases = tuple(case for case in inputs.cases if not options.case_ids or case.case_id in options.case_ids)
    config = FitConfig(seed=options.seed, workers=options.workers)
    engine = Engine(inputs, output, config, sources, before, options.resume)
    if any(spec.owner == "baseline" and spec.id != "climatology_empirical" for spec in selected):
        engine.prepare_baseline({target.case_id for target in cases})
    output.mkdir(parents=True, exist_ok=True)
    write_rows(output / "case_inventory.csv", [{
        **{name: value for name, value in known_input(target).items()
           if not isinstance(value, (dict, list))},
        "target_status": "AVAILABLE" if target.case_id in inputs.truths else "TARGET_UNAVAILABLE",
        "history_rows": len(inputs.historical.get(target.case_id, ())),
        "known_input_hash": digest(known_input(target)),
        "latest_absent_history_receipt": int(target.case_id in absent_ids),
        "selected": int(not options.case_ids or target.case_id in options.case_ids),
    } for target in inputs.cases])
    dependency_versions = {package: importlib.metadata.version(package)
                           for package in ("numpy", "scipy", "torch")}
    dependency_versions["python"] = platform.python_version()
    provenance = dict(inputs.provenance)
    provenance["daily_sha256"] = provenance["source_daily_sha256"]
    config_value = json_value(config)
    if not isinstance(config_value, dict):
        raise TypeError("Fit configuration must serialize as an object")
    config_value["seed_override_explicit"] = options.seed != 20261007
    summary: RunSummary = {
        "scope": "SMOKE" if options.methods or options.case_ids else "FULL",
        "status": "RUNNING", "provenance": dict(inputs.provenance),
        "active_provenance": provenance, "options": json_value(options),
        "config": config_value, "config_hash": digest(config_value),
        "dependency_versions": json_value(dependency_versions),
        "dependency_hash": digest(dependency_versions),
        "seed": options.seed, "seed_hash": digest(options.seed), "source_hashes": sources,
        "case_statuses": case_statuses(inputs, options),
        "timings": {"elapsed_seconds": perf_counter() - started},
        "cache_counts": {}, "gate_receipts": [],
        "protected_hashes_before": before,
        "cases_supplied": len(inputs.cases), "truths_available": len(inputs.truths),
        "targets_unavailable": len(inputs.excluded_cases), "cases_selected": len(cases),
        "registry_entries": len(registry), "selected_registry_entries": len(selected),
        "expected_registry_entries": [spec.id for spec in registry],
        "selected_methods": [spec.id for spec in selected],
        "catalog_hash": immutable_before, "worker_blas_threads": 1, "worker_torch_threads": 1,
        "retained_latest_absent_history_case_ids": absent_ids,
    }
    write_json(output / "run_summary.json", summary)
    work, schedule, joint_sets = build_schedule(engine, cases, selected, inputs.cases, output)
    summary["planned_tasks"] = len(work)
    summary["distinct_outer_train_hashes"] = len({
        str(row["train_hash"]) for row in schedule if row.get("train_hash")})
    summary["distinct_fit_keys"] = len({str(row["fit_ref"]) for row in schedule if row.get("fit_ref")})
    summary["joint_keys"] = len(joint_sets)
    write_json(output / "run_summary.json", summary)
    print(f"ALTERNATIVE_START scope={summary['scope']} tasks={len(work)} " +
          f"cases={len(cases)} workers={options.workers}", flush=True)
    results: list[dict[str, Json]] = []
    # Threads share one immutable parse and proven pooled fits. Torch global RNG
    # fits are serialized by Engine.neural_lock; NumPy/model streams are explicit.
    with ThreadPoolExecutor(max_workers=options.workers) as executor:
        futures = [executor.submit(_execute, engine, item) for item in work]
        for index, future in enumerate(futures, 1):
            results.append(future.result())
            if index % 100 == 0 or index == len(futures):
                print(f"ALTERNATIVE_PROGRESS {index}/{len(futures)}", flush=True)
    summary["attempted_registry_entries"] = json_value(sorted({
        item.spec.id for item, result in zip(work, results, strict=True) if "fit" in result}))
    summary["completed_registry_entries"] = [spec.id for spec in selected]
    summary["fit_reuse_hits"] = engine.fit_reuses
    summary["resume_prediction_hits"] = engine.resume_hits
    write_json(output / "run_summary.json", summary)
    output_summary = build_outputs(engine, cases, selected, work, results, joint_sets, output)
    summary.update(output_summary)
    summary.update(complete_metadata(engine, results, started))
    immutable_after = check_catalog_immutability(inputs)
    if immutable_after != immutable_before:
        summary.update(status="FAILED_INPUT_CHANGED", terminal_exit_code=2,
                       terminal_error="Accepted input catalog changed during execution",
                       catalog_hash_after=immutable_after, elapsed_seconds=perf_counter() - started)
        write_json(output / "run_summary.json", summary)
        raise RuntimeError("Accepted input catalog changed during execution")
    after = protected_hashes(root)
    sources_after = source_hashes(root)
    summary["source_hashes_after"] = sources_after
    summary["protected_hashes_after"] = after
    if sources_after != sources:
        summary.update(
            status="FAILED_SOURCE_CHANGED", terminal_exit_code=2,
            terminal_error="Implementation changed during execution; rerun/resume with new source hashes",
            changed_source_paths=json_value(sorted(
                name for name in set(sources) | set(sources_after)
                if sources.get(name) != sources_after.get(name))),
            elapsed_seconds=perf_counter() - started,
        )
        write_json(output / "run_summary.json", summary)
        raise RuntimeError("Implementation changed during execution; rerun/resume with new source hashes")
    summary["status"] = "PREDICTIONS_COMPLETED"
    write_json(output / "run_summary.json", summary)
    try:
        summary["reports"] = publish_reports(output, inputs)
    except Exception as error:
        summary.update(status="FAILED_REPORTING", terminal_exit_code=2,
                       terminal_error=f"{type(error).__name__}: {error}",
                       elapsed_seconds=perf_counter() - started)
        write_json(output / "run_summary.json", summary)
        raise RuntimeError(f"Reporting failed: {error}") from error
    final_sources = source_hashes(root)
    summary["source_hashes_after"] = final_sources
    summary["protected_hashes_after"] = protected_hashes(root)
    if final_sources != sources:
        summary.update(status="FAILED_SOURCE_CHANGED", terminal_exit_code=2,
                       terminal_error="Implementation changed during reporting",
                       changed_source_paths=json_value(sorted(
                           name for name in set(sources) | set(final_sources)
                           if sources.get(name) != final_sources.get(name))),
                       elapsed_seconds=perf_counter() - started)
        write_json(output / "run_summary.json", summary)
        raise RuntimeError("Implementation changed during reporting")
    summary.update({
        "status": "COMPLETED", "protected_hashes_after": after,
        "elapsed_seconds": perf_counter() - started,
        "fit_failure_policy": "No substituted method law; reporter separates deployable climatology fallback",
        "unresolved_gate_receipts": [json_object(result["gate"]) for result in results
                                     if "gate" in result and json_object(result["gate"]).get("allowed") is False],
    })
    write_json(output / "run_summary.json", summary)
    refresh_completed_reports(root, output, inputs, summary, sources, started)
    print("ALTERNATIVE_SUMMARY " + dumps({
        key: summary.get(key) for key in ("scope", "status", "cases_selected", "continuous_rows",
                                         "category_rows", "joint_rows", "elapsed_seconds",
                                         "fit_reuse_hits", "resume_prediction_hits")
    }), flush=True)
    return summary


class Arguments(argparse.Namespace):
    """Argparse's boundary uses declared destinations, not unchecked Any."""

    output: Path = Path("outputs/alternative_comparison")
    methods: str | None = None
    case_id: list[str]
    workers: int = 4
    seed: int = 20261007
    resume: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.case_id = []


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fit all 61 researched subtypes and five controls on actual GloSea6 inputs.")
    _ = parser.add_argument("--output", type=Path, default=Path("outputs/alternative_comparison"))
    _ = parser.add_argument("--methods", help="Comma-separated exact registry IDs; marks scope=SMOKE")
    _ = parser.add_argument("--case-id", action="append", default=[], help="Exact case ID (repeatable); SMOKE")
    _ = parser.add_argument("--workers", type=int, choices=range(1, 7), default=4)
    _ = parser.add_argument("--seed", type=int, default=20261007)
    _ = parser.add_argument("--resume", action="store_true",
                            help="Reuse only complete content/source/parameter/known-input matched checkpoints")
    namespace = Arguments()
    _ = parser.parse_args(namespace=namespace)
    methods = tuple(namespace.methods.split(",")) if namespace.methods is not None else ()
    if any(not method for method in methods) or len(methods) != len(set(methods)):
        parser.error("methods must be nonempty unique exact registry IDs")
    try:
        _ = run(Path(__file__).resolve().parents[1], namespace.output, RunOptions(
            methods=methods, case_ids=tuple(namespace.case_id),
            workers=namespace.workers, seed=namespace.seed, resume=namespace.resume,
        ))
    except (ValueError, RuntimeError) as error:
        parser.exit(2, f"comparison error: {error}\n")


if __name__ == "__main__":
    main()
