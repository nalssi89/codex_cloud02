"""Deterministic reporting wire helpers; no forecast fitting or source writes."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections.abc import Callable, Iterable, Mapping, Sequence
from pathlib import Path

from analysis.data_io import CsvCell, Json, csv_rows

type Row = dict[str, CsvCell]


def decode(text: str) -> Json:
    readers: list[Callable[[str], Json]] = [json.loads]
    return readers[0](text)


def object_json(path: Path) -> dict[str, Json]:
    value = decode(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"Expected JSON object: {path}")
    return value


def rows(path: Path) -> list[Row]:
    _ = csv.field_size_limit(sys.maxsize)
    return [dict(row) for row in csv_rows(path)] if path.exists() else []


def save_rows(path: Path, records: Sequence[Mapping[str, CsvCell]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(key for record in records for key in record))
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields or ["STATUS"])
        writer.writeheader()
        writer.writerows(records)


def save_json(path: Path, value: Mapping[str, Json]) -> None:
    _ = path.write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                   sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def text(row: Mapping[str, CsvCell], key: str, alternate: str = "") -> str:
    return str(row.get(key) or row.get(alternate) or "")


def number(row: Mapping[str, CsvCell], key: str) -> float | None:
    value = row.get(key)
    if value is None or value == "":
        return None
    result = float(value)
    return result if math.isfinite(result) else None


def mask_hash(ids: Iterable[str]) -> str:
    """Exact sorted UTF-8 JSON identities; retain IDs alongside every hash."""
    return hashlib.sha256(json.dumps(sorted(ids), separators=(",", ":"),
                                    ensure_ascii=False).encode()).hexdigest()


def identity(row: Mapping[str, CsvCell]) -> str:
    return text(row, "case_id", "CASE_ID") or text(row, "joint_id")


def method(row: Mapping[str, CsvCell]) -> str:
    return text(row, "method_id", "METHOD")


def scope(row: Mapping[str, CsvCell]) -> tuple[str, str]:
    product = text(row, "PRODUCT", "product")
    variable = text(row, "VARIABLE", "variable")
    if not variable:
        variable = text(row, "component_keys", "variables")
    if not product or not variable:
        raise ValueError(f"Missing unit/product scope: {identity(row)}")
    return product, variable


def window(row: Mapping[str, CsvCell]) -> str:
    components = text(row, "component_windows")
    if components:
        return components
    start, end = text(row, "VALID_START"), text(row, "VALID_END")
    if not start or not end:
        raise ValueError(f"Missing exact valid window: {identity(row)}")
    return f"{start}/{end}"


def mean(values: Sequence[float]) -> float | None:
    return math.fsum(values) / len(values) if values else None


def json_strings(values: Iterable[str]) -> list[Json]:
    return [value for value in values]


def string_list(value: Json) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(v, str) for v in value):
        raise TypeError("Expected JSON string array")
    return [v for v in value if isinstance(v, str)]
