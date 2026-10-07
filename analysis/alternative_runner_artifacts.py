"""Runnable exhaustive statistical comparison, preserving the published baseline."""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np

from analysis.alternative_runner_io import (
    Row,
    digest,
    write_rows,
)
from analysis.alternative_runner_tables import json_object
from analysis.calibration import FloatArray
from analysis.data_io import Json


def write_numeric_laws(output: Path, laws: list[dict[str, Json]]) -> None:
    numeric_arrays: dict[str, FloatArray] = {}
    numeric_manifest: list[Row] = []
    for record in laws:
        law_spec = json_object(record["distribution"])
        for name, value in law_spec.items():
            if not isinstance(value, list) or not value:
                continue
            # Preserve the exact inline law required by every public decoder, while
            # exposing its numeric arrays in a versioned, pickle-free companion shard.
            try:
                array = np.asarray(value, dtype=np.float64)
            except (ValueError, TypeError):
                continue
            if not np.isfinite(array).all():
                raise ValueError("Nonfinite distribution array")
            array_key = "v1_" + digest([record["case_id"], record["method_id"],
                                      record.get("joint_id", ""), record["fit_ref"], name])
            numeric_arrays[array_key] = array
            numeric_manifest.append({
                "case_id": str(record["case_id"]), "method_id": str(record["method_id"]),
                "fit_ref": str(record["fit_ref"]), "field": name, "array_key": array_key,
                "shard": "distribution_arrays_v1.npz", "version": 1,
            })
    temporary_numeric = output / "distribution_arrays_v1.tmp.npz"
    np.savez_compressed(temporary_numeric, allow_pickle=False, **numeric_arrays)
    os.replace(temporary_numeric, output / "distribution_arrays_v1.npz")
    write_rows(output / "distribution_array_manifest.csv", numeric_manifest,
               ("case_id", "method_id", "fit_ref", "field", "array_key", "shard", "version"))
