"""Read-only readiness regression on authentic smoke exports, never a FULL claim."""

from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter
from unittest.mock import patch

from analysis import alternative_validation_coverage as coverage
from analysis import alternative_validation_joint_ancestry as joint
from analysis.alternative_validation_ancestry import ancestry_checks
from analysis.alternative_validation_inventory import inventory_checks
from analysis.alternative_validation_io import csv_records
from analysis.alternative_validation_masks import paired_checks
from analysis.data_io import Json


def main() -> None:
    started = perf_counter()
    root = Path(__file__).resolve().parents[1]
    receipts: list[Json] = []
    for suffix in ("scalar_final", "monthly_final", "joint_final", "joint_repaired"):
        output = root / f"outputs/alternative_runner_smoke_{suffix}"
        receipt: dict[str, Json] = {"fixture": output.name, "ancestry": ancestry_checks(output)}
        if suffix != "joint_repaired":
            receipt["coverage"] = coverage.coverage_checks(root, output)
            receipt["paired_masks"] = paired_checks(output)
        else:
            receipt["reports"] = "UNAVAILABLE: guarded FAILED_SOURCE_CHANGED run has no report exports"
        receipts.append(receipt)
        try:
            _ = inventory_checks(root, output)
        except AssertionError:
            pass
        else:
            raise AssertionError("authentic SMOKE was promoted to FULL")
    output = root / "outputs/alternative_runner_smoke_scalar_final"
    def wrong_count(path: Path) -> list[dict[str, str]]:
        rows = csv_records(path)
        if path.name == "coverage_and_failures.csv":
            rows[0]["scored_count"] = str(int(rows[0]["scored_count"])+1)
        return rows
    rejections = 0
    with patch.object(coverage, "csv_records", wrong_count):
        try:
            _ = coverage.coverage_checks(root, output)
        except AssertionError:
            rejections += 1
        else:
            raise AssertionError("corrupt grouped score count accepted")
    output = root / "outputs/alternative_runner_smoke_joint_final"
    for field in ("joint_train_hash", "component_training_hashes", "observations", "row_ids"):
        def corrupt(path: Path, field: str = field) -> list[dict[str, str]]:
            rows = csv_records(path)
            if path.name == "joint_component_manifest.csv" and field in (
                "joint_train_hash", "component_training_hashes"
            ):
                rows[0][field] = "0"*64 if field == "joint_train_hash" else '["'+"0"*64+'"]'
            if path.name == "joint_training_manifest.csv.gz" and field in ("observations", "row_ids"):
                rows[0][field] = "[1000000000000]" if field == "observations" else '["foreign-row"]'
            return rows
        with patch.object(joint, "csv_records", corrupt):
            try:
                _ = joint.joint_ancestry_checks(output)
            except (AssertionError, KeyError):
                rejections += 1
            else:
                raise AssertionError("corrupt joint hash/source linkage accepted")
    print(json.dumps({"status": "PASS", "scope": "AUTHENTIC_SMOKE_READINESS_NOT_FULL",
                      "receipts": receipts, "corruption_rejections": rejections,
                      "smoke_full_rejections": 4, "elapsed_seconds": perf_counter()-started},
                     indent=2))


if __name__ == "__main__":
    main()
