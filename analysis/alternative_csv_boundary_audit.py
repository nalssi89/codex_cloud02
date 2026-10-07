"""Real large joint CSV fields must survive both reporting and validation."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from time import perf_counter

from analysis.alternative_reporting_common import rows
from analysis.alternative_validation_io import csv_records, sha256


def main() -> None:
    started = perf_counter()
    root = Path(__file__).resolve().parents[1]
    path = root / "outputs/alternative_comparison_root_all_methods_smoke/joint_predictions.csv.gz"
    before = (sha256(path), path.stat().st_size, path.stat().st_mtime_ns)
    previous_limit = csv.field_size_limit()
    try:
        # Each boundary must work in a fresh process with the default parser cap.
        _ = csv.field_size_limit(131072)
        reporting = rows(path)
        _ = csv.field_size_limit(131072)
        independent = csv_records(path)
        assert reporting == independent, "CSV readers changed original field values"
        largest = max(len(value) for row in independent for value in row.values())
        assert largest > 131072, "actual fixture did not exercise the field boundary"
        assert independent, "actual joint prediction fixture is empty"
        assert before == (sha256(path), path.stat().st_size, path.stat().st_mtime_ns)
    finally:
        _ = csv.field_size_limit(previous_limit)
    print(json.dumps({
        "status": "PASS", "scope": "ACTUAL_JOINT_CSV_BOUNDARY_NOT_FULL",
        "records": len(independent), "maximum_field_characters": largest,
        "read_only": True, "elapsed_seconds": perf_counter() - started,
    }))


if __name__ == "__main__":
    main()
