"""Replay actual grouped, score-specific reporting masks and original-unit deltas."""

from __future__ import annotations

import json
import math
from pathlib import Path

from analysis.alternative_validation_ancestry import row_ids
from analysis.alternative_validation_io import (
    csv_records,
    ordered_hash,
    require_columns,
)
from analysis.alternative_validation_oracles import close
from analysis.data_io import DATASET, Json


def paired_checks(output: Path) -> dict[str, Json]:
    root = Path(__file__).resolve().parents[1]
    catalog = {r["CASE_ID"]: r for r in csv_records(root / DATASET / "cases/verification_cases.csv")}
    lookup: dict[tuple[str, str, str, str], dict[str, dict[str, str]]] = {}
    for surface in ("continuous", "category", "joint"):
        for row in csv_records(output / f"{surface}_predictions.csv.gz"):
            if surface == "joint":
                cases = [catalog[k] for k in row_ids(row["component_case_ids"])]
                row["VARIABLE"] = json.dumps([f'{c["VARIABLE"]}:{c["LEAD"]}' for c in cases],
                                             separators=(",", ":"))
            key = (surface, row["PRODUCT"], row["VARIABLE"], row["method_id"])
            identity = row.get("case_id") or row["joint_id"]
            if identity in lookup.setdefault(key, {}):
                raise AssertionError("duplicate prediction in paired mask")
            lookup[key][identity] = row
    path = output / "paired_comparison.csv"
    if not path.exists():
        path = output / "reports/paired_comparison.csv"
    paired = csv_records(path)
    if paired:
        require_columns(paired, ("PRODUCT", "VARIABLE", "surface", "mask_kind", "methods",
                                 "method_id", "score", "N", "mask_hash",
                                 "mean_loss", "delta_first_minus_second"), "grouped comparisons")
    checked = 0
    for row in paired:
        methods = row_ids(row["methods"])
        if not methods or len(methods) != len(set(methods)) or row["method_id"] not in methods:
            raise AssertionError("invalid comparison participants")
        groups = [lookup.get((row["surface"], row["PRODUCT"], row["VARIABLE"], m), {})
                  for m in methods]
        common = set(groups[0])
        for group in groups[1:]:
            common.intersection_update(group)
        if int(row["N"]) != len(common) or row["mask_hash"] != ordered_hash(sorted(common)):
            raise AssertionError("grouped exact common-success mask differs")
        if not common:
            if row["mean_loss"] or row["delta_first_minus_second"]:
                raise AssertionError("empty common mask has fabricated loss/delta")
            continue
        averages = [math.fsum(float(g[key][row["score"]]) for key in sorted(common))/len(common)
                    for g in groups]
        close(float(row["mean_loss"]), averages[methods.index(row["method_id"])],
              "grouped original-unit mean loss")
        if len(methods) == 2:
            close(float(row["delta_first_minus_second"]), averages[0]-averages[1],
                  "grouped original-unit paired delta")
        elif row["delta_first_minus_second"]:
            raise AssertionError("non-pair family mask reports paired delta")
        checked += 1
    return {"status": "PASS", "comparison_rows": len(paired), "nonempty_masks": checked}
