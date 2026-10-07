"""Focused N-label/terminal-state regression using saved real reporting tables."""

from __future__ import annotations

from pathlib import Path

from analysis.alternative_reporting import run_completed
from analysis.alternative_reporting_common import rows, save_json, text
from analysis.alternative_reporting_plots import plots, score_label


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    source = root / "outputs/alternative_reporting_smoke_verified_20261007/reports"
    output = root / "outputs/alternative_reporting_refinement_20261007"
    output.mkdir(parents=True, exist_ok=True)
    metrics = rows(source / "continuous_metrics.csv")
    counts = rows(source / "coverage_and_failures.csv")
    assert metrics and counts
    actual = metrics[0]
    assert score_label(actual).split("\n")[1].removeprefix("N=") == text(actual, "scored_N")
    for status in ("RUNNING", "FAILED_SOURCE_CHANGED", "FAILED", "INTERRUPTED", "UNRECORDED"):
        assert not run_completed({"scope": "FULL", "status": status})
    assert not run_completed({"scope": "FULL"})
    assert run_completed({"scope": "FULL", "status": "COMPLETED"})
    generated = plots(output, counts, metrics, "REPORTING_SMOKE")
    assert len(generated) == 16
    save_json(output / "refinement_receipt.json", {
        "status": "PASS", "scope": "REPORTING_REFINEMENT_NOT_FULL",
        "source": str(source.relative_to(root)),
        "model_or_data_smoke_rerun": False,
        "terminal_state_rejections": 6,
        "actual_saved_N_label_checked": True,
        "actual_saved_table_figures": len(generated),
    })
    print(f"PASS REPORTING_REFINEMENT_NOT_FULL figures={len(generated)}")


if __name__ == "__main__":
    main()
