"""Publish the reporting owner's actual tables at the frozen canonical locations."""

import os
import shutil
from pathlib import Path
from time import perf_counter

from analysis.alternative_experiment_types import ExperimentInputs
from analysis.alternative_runner_io import protected_hashes, source_hashes, write_json
from analysis.data_io import Json

REQUIRED_REPORTS = (
    "paired_comparison.csv", "coverage_and_failures.csv", "failure_inclusive_policy.csv",
    "equal_valid_window_metrics.csv", "category_metrics.csv", "joint_metrics.csv",
    "distribution_diagnostics.csv", "common_threshold_checks.csv", "REPORT_KO.md",
)


def publish_reports(output: Path, inputs: ExperimentInputs) -> dict[str, Json]:
    from analysis.alternative_reporting import generate_reports

    reports = generate_reports(output, inputs)
    for name in REQUIRED_REPORTS:
        source = output / "reports" / name
        if not source.is_file():
            raise RuntimeError(f"Real reporting dependency did not produce {name}")
        temporary = output / (name + ".tmp")
        _ = shutil.copyfile(source, temporary)
        os.replace(temporary, output / name)
    return reports


def refresh_completed_reports(root: Path, output: Path, inputs: ExperimentInputs,
                              summary: dict[str, Json], expected_sources: dict[str, Json],
                              started: float) -> None:
    """FULL-only final snapshot: the reporter never promotes a pending experiment.

    The first report already exists and the completed run is source-verified.
    This real second invocation refreshes its completed-state manifest and report;
    it does not fit another model or replace any failed method's law.
    """
    if summary["scope"] != "FULL":
        return
    try:
        summary["reports"] = publish_reports(output, inputs)
    except Exception as error:
        summary.update(status="FAILED_REPORTING", terminal_exit_code=2,
                       terminal_error=f"{type(error).__name__}: {error}",
                       elapsed_seconds=perf_counter() - started)
        write_json(output / "run_summary.json", summary)
        raise RuntimeError(f"Completed report refresh failed: {error}") from error
    actual_sources = source_hashes(root)
    summary["source_hashes_after"] = actual_sources
    summary["protected_hashes_after"] = protected_hashes(root)
    summary["elapsed_seconds"] = perf_counter() - started
    if actual_sources != expected_sources:
        summary.update(status="FAILED_SOURCE_CHANGED", terminal_exit_code=2,
                       terminal_error="Implementation changed during completed report refresh")
        write_json(output / "run_summary.json", summary)
        raise RuntimeError("Implementation changed during completed report refresh")
    write_json(output / "run_summary.json", summary)
