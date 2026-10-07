"""Atomic, explicit JSON/CSV experiment persistence and content identities."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
import os
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from dataclasses import fields, is_dataclass
from datetime import date
from pathlib import Path
from typing import Protocol, runtime_checkable

import numpy as np

from analysis.alternative_contracts import CaseInput, FoldSpec, TrainingSet
from analysis.alternative_validation_io import read_json, safe_output, sha256
from analysis.calibration import FloatArray
from analysis.data_io import CsvCell, Json

type Row = dict[str, CsvCell]


@runtime_checkable
class ObjectMapping(Protocol):
    def items(self) -> Iterable[tuple[object, object]]: ...


@runtime_checkable
class ObjectSequence(Protocol):
    def __iter__(self) -> Iterator[object]: ...


def json_value(value: object) -> Json:
    """Convert owned dataclasses; refuse arbitrary objects and nonfinite metadata."""
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, np.ndarray):
        converters: list[Callable[[object], FloatArray]] = [np.asarray]
        array = converters[0](value)
        if array.ndim == 1:
            return [array.item(i) for i in range(len(array))]
        return [json_value(array.take(i, axis=0)) for i in range(len(array))]
    if isinstance(value, ObjectMapping):
        return {str(key): json_value(item) for key, item in value.items()}
    if isinstance(value, ObjectSequence):
        return [json_value(item) for item in value]
    if is_dataclass(value) and not isinstance(value, type):
        accessors: list[Callable[[object, str], object]] = [getattr]
        return {field.name: json_value(accessors[0](value, field.name)) for field in fields(value)}
    raise TypeError(f"Unsupported JSON object: {type(value).__name__}")


def dumps(value: object) -> str:
    return json.dumps(json_value(value), ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def digest(value: object) -> str:
    return hashlib.sha256(dumps(value).encode()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        _ = handle.write(json.dumps(json_value(value), ensure_ascii=False, sort_keys=True,
                                    indent=2, allow_nan=False) + "\n")
    os.replace(temporary, path)


def write_rows(path: Path, records: Sequence[Mapping[str, CsvCell]],
               columns: tuple[str, ...] = ()) -> None:
    """Empty surfaces retain headers; heterogeneous diagnostics retain all fields."""
    names = list(dict.fromkeys((*columns, *(key for row in records for key in row))))
    if not names:
        raise ValueError(f"No schema for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(temporary, "wt", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=names)
        writer.writeheader()
        writer.writerows(records)
    os.replace(temporary, path)


def write_laws(path: Path, records: Iterable[Mapping[str, Json]]) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with gzip.open(temporary, "wt", encoding="utf-8") as handle:
        for row in records:
            _ = handle.write(dumps(row) + "\n")
    os.replace(temporary, path)


def load_fit(output: Path, record: dict[str, Json]) -> dict[str, Json]:
    reference = record.get("model_ref")
    if reference is None:
        return record
    expected = f"cache/fits/{record['fit_ref']}.json"
    if reference != expected:
        raise ValueError("Fitted model reference escaped its content-keyed cache location")
    full = read_json(output / expected)
    if full["fit_ref"] != record["fit_ref"] or full["train_hash"] != record["train_hash"]:
        raise ValueError("Serialized fitted model identity mismatch")
    return full
def write_stream_rows(path: Path, records: Iterable[Mapping[str, CsvCell]],
                      columns: tuple[str, ...]) -> int:
    """Large pooled ancestry is streamed, not materialized millions of times."""
    temporary = path.with_name(path.name + ".tmp")
    opener = gzip.open if path.suffix == ".gz" else open
    count = 0
    with opener(temporary, "wt", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in records:
            writer.writerows((row,))
            count += 1
    os.replace(temporary, path)
    return count


def protected_hashes(root: Path) -> dict[str, Json]:
    receipt = read_json(root / ".omo/evidence/alternative-baseline-hashes.json")
    expected = receipt["files"]
    if not isinstance(expected, dict) or len(expected) != 60:
        raise ValueError("Expected frozen 60-file protection receipt")
    actual: dict[str, Json] = {}
    for relative, metadata in expected.items():
        if not isinstance(metadata, dict):
            raise TypeError("Invalid preservation receipt")
        path = root / relative
        record: dict[str, Json] = {"sha256": sha256(path), "bytes": path.stat().st_size}
        if record != metadata:
            raise ValueError(f"Protected input changed: {relative}")
        actual[relative] = record
    return actual


def source_hashes(root: Path) -> dict[str, Json]:
    """Model code, plan and schema are part of cache identity, not invented versions."""
    paths = sorted((root / "analysis").glob("*.py"))
    paths.extend((root / ".omo/notepads/alternative-statistical-plan.md",
                  root / ".omo/evidence/alternative-output-schema.md"))
    return {path.relative_to(root).as_posix(): sha256(path) for path in paths}


def check_output(root: Path, output: Path, resume: bool) -> None:
    safe_output(root, output)
    if output.exists() and any(output.iterdir()) and not resume:
        raise ValueError("Nonempty output requires --resume; existing artifacts are not overwritten")


def known_input(case: CaseInput) -> dict[str, Json]:
    value = json_value(case)
    if not isinstance(value, dict):
        raise TypeError("Known input must serialize as an object")
    return value


def training_rows(training: TrainingSet) -> Iterator[Row]:
    for index, row in enumerate(training.rows):
        yield {
            "row_id": row.row_id, "train_hash": training.train_hash,
            "source_case_id": row.source_case_id,
            "source_case_init": row.source_case_init.isoformat(),
            "source_year": row.source_year, "source_init": row.source_init.isoformat(),
            "hist_start": row.hist_start.isoformat(), "hist_end": row.hist_end.isoformat(),
            "product": row.product, "variable": row.variable, "lead": row.lead,
            "observation": row.observation, "ensemble": dumps(row.ensemble),
            "member_keys": dumps(row.member_keys), "source_files": dumps(row.source_files),
            "provenance_hash": row.provenance_hash, "archive_era": row.archive_era,
            "cutoff": training.cutoff.isoformat(),
            "catalog_cutoff": training.catalog_cutoff.isoformat(),
            "held_out_years": dumps(training.held_out_years),
            "year_weight": training.year_weights.item(index),
        }


def fold_rows(folds: tuple[FoldSpec, ...], training: TrainingSet) -> list[Row]:
    return [{
        "fold_id": fold.fold_id, "training_row_ids": dumps(fold.training_row_ids),
        "validation_row_ids": dumps(fold.validation_row_ids),
        "pseudo_init": fold.pseudo_init.isoformat(),
        "held_out_years": dumps(fold.held_out_years), "ancestor_hash": fold.ancestor_hash,
        "outer_train_hash": training.train_hash,
        "catalog_cutoff": training.catalog_cutoff.isoformat(),
    } for fold in folds]
