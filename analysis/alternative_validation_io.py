"""Strict read-only artifact decoding and immutable preservation receipts."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
import sys
from collections.abc import Callable, Iterator, Mapping
from pathlib import Path

from analysis.data_io import Json


def decode(value: str) -> Json:
    """Standard JSON decoder's documented result, checked by consumers' schema."""
    decoders: list[Callable[[str], Json]] = [json.loads]
    return decoders[0](value)


def mapping(value: Json) -> dict[str, Json]:
    if not isinstance(value, dict):
        raise TypeError("expected JSON object")
    return value


def sequence(value: Json) -> list[Json]:
    if not isinstance(value, list):
        raise TypeError("expected JSON list")
    return value


def text(value: Json) -> str:
    if not isinstance(value, str):
        raise TypeError("expected JSON string")
    return value


def number(value: Json) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("expected JSON number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("JSON numeric metadata must be finite")
    return result


def read_json(path: Path) -> dict[str, Json]:
    with path.open(encoding="utf-8") as handle:
        value = decode(handle.read())
    return mapping(value)


def json_lines(path: Path) -> Iterator[dict[str, Json]]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            yield mapping(decode(line))


def csv_records(path: Path) -> list[dict[str, str]]:
    _ = csv.field_size_limit(sys.maxsize)
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def require_columns(rows: list[dict[str, str]], columns: tuple[str, ...],
                    label: str) -> None:
    if not rows:
        raise AssertionError(f"{label}: no rows")
    missing = set(columns) - rows[0].keys()
    if missing:
        raise AssertionError(f"{label}: missing columns {sorted(missing)}")


def sha256(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def preserved(root: Path) -> dict[str, Json]:
    receipt = read_json(root / ".omo/evidence/alternative-baseline-hashes.json")
    files = mapping(receipt["files"])
    if len(files) != 60:
        raise AssertionError(f"preservation receipt has {len(files)}, not 60 files")
    failures: list[Json] = []
    for relative, value in files.items():
        entry = mapping(value)
        path = root / relative
        if not path.is_file():
            failures.append({"path": relative, "reason": "MISSING"})
        elif path.stat().st_size != number(entry["bytes"]) or sha256(path) != entry["sha256"]:
            failures.append({"path": relative, "reason": "HASH_OR_SIZE_CHANGED"})
    return {"status": "FAIL" if failures else "PASS", "files_checked": 60,
            "failures": failures}


def ordered_hash(ids: list[str]) -> str:
    return hashlib.sha256(json.dumps(ids, separators=(",", ":")).encode()).hexdigest()


def safe_output(root: Path, output: Path) -> None:
    """Only a new output child is writable; never baseline/source directories."""
    output = output.resolve()
    allowed = (root / "outputs").resolve()
    if not output.is_relative_to(allowed) or output == allowed:
        raise ValueError("output must be a new child directory of outputs")
    protected = mapping(read_json(root / ".omo/evidence/alternative-baseline-hashes.json")["files"])
    for relative in protected:
        path = (root / relative).resolve()
        if path.is_relative_to(output) or output.is_relative_to(path):
            raise ValueError(f"output overlaps protected path: {relative}")


def require_metadata(record: Mapping[str, Json], keys: tuple[str, ...], label: str) -> None:
    missing = set(keys) - record.keys()
    if missing:
        raise AssertionError(f"{label}: missing metadata {sorted(missing)}")
