"""Streaming input readers and source-QC national-mean targets."""

from __future__ import annotations

import calendar
import csv
import gzip
import hashlib
import json
import math
import tarfile
from collections import defaultdict
from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Final, NamedTuple, TextIO

import numpy as np
from numpy.typing import NDArray

DATASET: Final = "GLOSEA6_KMA_20220301-20260831_v1"
FloatArray = NDArray[np.float64]
CsvCell = str | int | float | bool | None
type Json = str | int | float | bool | None | list[Json] | dict[str, Json]


class InputError(RuntimeError):
    """An input contract failed; preserve the offending file/key."""


@dataclass(frozen=True, slots=True)
class Case:
    case_id: str
    init: date
    product: str
    lead: str
    variable: str
    expected_members: int


@dataclass(frozen=True, slots=True)
class Forecast:
    start: date
    end: date
    members: FloatArray
    missing_members: int


@dataclass(frozen=True, slots=True)
class Reference:
    start: date
    end: date
    value: float
    stations: int


@dataclass(frozen=True, slots=True)
class Observation:
    value: float | None
    min_stations: int
    status: str
    days: int


class DailyObservation(NamedTuple):
    """Supplied participating-station means and their original quality metadata."""

    temperature: float
    precipitation: float
    temperature_stations: int
    precipitation_stations: int
    required_stations: int
    total_stations: int
    temperature_qc: str
    precipitation_qc: str


def parse_date(value: str) -> date:
    """Parse the package's YYYYMMDD dates without locale dependence."""
    return date(int(value[:4]), int(value[4:6]), int(value[6:8]))


def csv_rows(path: Path) -> Iterator[Mapping[str, str]]:
    """Stream CSV rows; compressed input is never inflated into a row table."""
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as handle:
        yield from csv.DictReader(handle)


def write_csv(path: Path, records: Sequence[Mapping[str, CsvCell]]) -> None:
    """Persist generated analysis tables (not source/config edits)."""
    if not records:
        raise InputError(f"No rows to write: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "wt", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def prepare_inputs(root: Path) -> Path:
    """Extract the untouched supplied archive if needed; refuse unsafe entries."""
    destination = root / DATASET
    if not destination.exists():
        with tarfile.open(root / f"{DATASET}.tar.gz") as archive:
            for item in archive.getmembers():
                target = (root / item.name).resolve()
                if not target.is_relative_to(root.resolve()) or item.issym() or item.islnk():
                    raise InputError(f"Unsafe archive path: {item.name}")
            archive.extractall(root, filter="data")
    return destination


def check_manifest(source: Path) -> list[str]:
    """Verify every shipped manifest hash and byte count before analysis."""
    checked: list[str] = []
    for row in csv_rows(source / "MANIFEST.csv"):
        path = source / row["RELATIVE_PATH"]
        with path.open("rb") as handle:
            digest = hashlib.file_digest(handle, "sha256").hexdigest()
        if digest != row["SHA256"] or path.stat().st_size != int(row["BYTES"]):
            raise InputError(f"Manifest mismatch: {row['RELATIVE_PATH']}")
        checked.append(row["RELATIVE_PATH"])
    return checked


def load_cases(source: Path) -> tuple[Case, ...]:
    """Require one area and unique case keys and exactly 62 declared stations."""
    stations = list(csv_rows(source / "metadata/asos_kma_station_list.csv"))
    if len(stations) != 62 or len({r["STN"] for r in stations}) != 62:
        raise InputError("Metadata does not identify exactly 62 unique stations")
    result = tuple(
        Case(r["CASE_ID"], parse_date(r["INIT_DATE"]), r["PRODUCT"], r["LEAD"],
             r["VARIABLE"], int(r["FCST_MEMBER_COUNT"]))
        for r in csv_rows(source / "cases/verification_cases.csv")
        if r["AREA"] == "kma"
    )
    if len({r.case_id for r in result}) != len(result):
        raise InputError("Duplicate verification case")
    return result


def observation_provenance(
    source: Path, read_json: Callable[[TextIO], Json] = json.load,
) -> dict[str, Json]:
    """Resolve the persisted selection, validating its confined path and content hash."""
    root = source.parent.resolve()
    selection = root / "observations/active_source.json"
    if not selection.exists():
        daily = source / "data/asos/asos_kma_daily.csv.gz"
        with daily.open("rb") as handle:
            digest = hashlib.file_digest(handle, "sha256").hexdigest()
        return {
            "selected": False, "relative_directory": source.name + "/data/asos",
            "daily_relative_path": daily.resolve().relative_to(root).as_posix(),
            "source_policy": "supplied daily QC OK; actual contributors >= supplied minimum; no imputation or rescaling",
            "source_daily_sha256": digest,
        }
    with selection.open(encoding="utf-8") as handle:
        settings = read_json(handle)
    if not isinstance(settings, dict) or set(settings) != {"relative_directory"}:
        raise InputError(f"Invalid observation source selection: {selection}")
    relative = settings["relative_directory"]
    if not isinstance(relative, str) or not relative or "\\" in relative \
            or ":" in relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise InputError(f"Invalid observation relative directory: {relative!r}")
    directory = (root / relative).resolve()
    observations = (root / "observations").resolve()
    if not observations.is_relative_to(root) or directory == observations \
            or not directory.is_relative_to(observations):
        raise InputError(f"Observation source must be a separate observations subdirectory: {relative}")
    daily = directory / "asos_kma_daily.csv.gz"
    provenance = directory / "provenance.json"
    if not daily.is_file() or not provenance.is_file() \
            or not daily.resolve().is_relative_to(directory) \
            or not provenance.resolve().is_relative_to(directory):
        raise InputError(f"Selected observation daily/provenance missing or unsafe: {relative}")
    with provenance.open(encoding="utf-8") as handle:
        metadata = read_json(handle)
    required = {
        "source_policy", "source_start", "source_end", "source_daily_sha256",
        "stations", "retrieved_at_utc", "endpoint", "repository_revision",
    }
    if not isinstance(metadata, dict) or not required.issubset(metadata) \
            or any(not metadata[key] for key in required):
        raise InputError(f"Incomplete observation provenance: {provenance}")
    if not isinstance(metadata["stations"], list) or len(metadata["stations"]) != 62 \
            or len({str(station) for station in metadata["stations"]}) != 62:
        raise InputError(f"Observation provenance must identify 62 unique stations: {provenance}")
    try:
        start, end = (parse_date(str(metadata[key])) for key in ("source_start", "source_end"))
    except (ValueError, TypeError) as error:
        raise InputError(f"Invalid observation provenance dates: {provenance}") from error
    if start > end:
        raise InputError(f"Reversed observation provenance dates: {provenance}")
    with daily.open("rb") as handle:
        digest = hashlib.file_digest(handle, "sha256").hexdigest()
    if metadata["source_daily_sha256"] != digest:
        raise InputError(f"Selected observation hash mismatch: {daily}")
    return {
        **metadata, "selected": True, "relative_directory": relative,
        "daily_relative_path": daily.relative_to(root).as_posix(),
    }


def observation_daily_path(source: Path) -> Path:
    """Source-selection seam for independently implemented observation audits."""
    metadata = observation_provenance(source)
    return source.parent.resolve() / str(metadata["daily_relative_path"])


def load_daily(source: Path) -> Mapping[date, DailyObservation]:
    """Read selected means, actual contributors and the unchanged supplied QC rule."""
    result: dict[date, DailyObservation] = {}
    daily_path = observation_daily_path(source)
    selected = daily_path != (source / "data/asos/asos_kma_daily.csv.gz").resolve()
    for row in csv_rows(daily_path):
        day = parse_date(row["DATE"])
        if day in result or row["AREA"] != "kma":
            raise InputError(f"Daily duplicate or wrong area: {day}")
        observation = DailyObservation(
            float(row["T15M"]) if row["T15M"] else math.nan,
            float(row["PRCP"]) if row["PRCP"] else math.nan,
            int(row["N_STATION_T15M"]), int(row["N_STATION_PRCP"]),
            int(row["N_STATION_REQUIRED"]), int(row["N_STATION_TOTAL"]),
            row["QC_T15M"], row["QC_PRCP"],
        )
        if not 1 <= observation.required_stations <= observation.total_stations \
                or (selected and observation.required_stations != 50) \
                or observation.total_stations != 62 \
                or any(n < 0 or n > observation.total_stations
                       for n in (observation.temperature_stations, observation.precipitation_stations)):
            raise InputError(f"Invalid observation station metadata: {day}")
        result[day] = observation
    return result


def aggregate_observation(
    daily: Mapping[date, DailyObservation],
    start: date, end: date, precipitation: bool,
) -> Observation:
    """Use all source-QC-valid daily means without fill or 62/n rescaling."""
    days = (end - start).days + 1
    values = [daily.get(start + timedelta(days=i)) for i in range(days)]
    if days <= 0 or any(row is None for row in values):
        return Observation(None, 0, "TARGET_OBSERVATION_UNAVAILABLE", days)
    present = [row for row in values if row is not None]
    counts = [row[3] if precipitation else row[2] for row in present]
    minimum = min(counts)
    if any(count < row.required_stations for count, row in zip(counts, present, strict=True)):
        return Observation(None, minimum, "INSUFFICIENT_OBSERVATION_STATIONS", days)
    if any((row.precipitation_qc if precipitation else row.temperature_qc) != "OK"
           for row in present):
        return Observation(None, minimum, "OBSERVATION_QC_FAILED", days)
    numbers = [row[1] if precipitation else row[0] for row in present]
    if not all(math.isfinite(v) for v in numbers):
        return Observation(None, minimum, "NONFINITE_OBSERVATION", days)
    value = math.fsum(numbers)
    if not precipitation:
        value /= days
    return Observation(value, minimum, "OK", days)


def load_references(source: Path) -> Mapping[str, Mapping[int, Reference]]:
    """SOURCE_YEAR is an initialization year; trust explicit historical dates."""
    result: dict[str, dict[int, Reference]] = defaultdict(dict)
    for row in csv_rows(source / "data/asos/asos_kma_period_reference.csv.gz"):
        key, year = row["CASE_ID"], int(row["REFERENCE_YEAR"])
        if year in result[key]:
            raise InputError(f"Duplicate observation reference: {key}/{year}")
        result[key][year] = Reference(
            parse_date(row["HIST_START"]), parse_date(row["HIST_END"]),
            float(row["VALUE"]), int(row["N_STATION"]),
        )
    return result


def expected_window(init: date, product: str, lead: str) -> tuple[date, date]:
    """Use source-date lead arithmetic, including leap days and year crossings."""
    offset = int(lead[1:])
    if product == "1mon":
        start = init + timedelta(days=7 * (offset - 1))
        return start, start + timedelta(days=6)
    if product != "3mon":
        raise InputError(f"Unsupported product: {product}")
    absolute_month = init.year * 12 + init.month - 1 + offset
    year, month0 = divmod(absolute_month, 12)
    start = date(year, month0 + 1, 1)
    return start, date(year, month0 + 1, calendar.monthrange(year, month0 + 1)[1])


def load_forecasts(source: Path, product: str, variable: str) -> Mapping[str, Forecast]:
    """Keep valid issued members; record blanks and reject duplicate member keys."""
    values: dict[str, list[float]] = defaultdict(list)
    missing: dict[str, int] = defaultdict(int)
    bounds: dict[str, tuple[date, date]] = {}
    seen: set[tuple[str, str]] = set()
    for row in csv_rows(source / f"data/model/fcst_raw/{product}_{variable}.csv.gz"):
        key, member = row["CASE_ID"], row["MEMBER"]
        if (key, member) in seen:
            raise InputError(f"Duplicate forecast member: {key}/{member}")
        seen.add((key, member))
        window = (parse_date(row["VALID_START"]), parse_date(row["VALID_END"]))
        if key in bounds and bounds[key] != window:
            raise InputError(f"Forecast member date disagreement: {key}")
        bounds[key] = window
        if not row["VALUE"] or not math.isfinite(float(row["VALUE"])):
            missing[key] += 1
            continue
        value = float(row["VALUE"])
        if variable == "prcp" and value < 0:
            raise InputError(f"Negative raw rainfall: {key}/{member}")
        values[key].append(value)
    return {
        key: Forecast(*window, np.asarray(values[key], dtype=np.float64), missing[key])
        for key, window in bounds.items()
    }


def load_hindcasts(
    source: Path, product: str, variable: str,
) -> Mapping[str, Mapping[int, FloatArray]]:
    """Group actual historical members by source initialization year, not VALUE year."""
    values: dict[str, dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
    seen: set[tuple[str, int, str]] = set()
    for row in csv_rows(source / f"data/model/hcst_mapping/{product}_{variable}.csv.gz"):
        key, year, member = row["CASE_ID"], int(row["SOURCE_YEAR"]), row["MEMBER"]
        if (key, year, member) in seen or not row["VALUE"]:
            raise InputError(f"Duplicate or empty historical member: {key}/{year}/{member}")
        seen.add((key, year, member))
        number = float(row["VALUE"])
        if not math.isfinite(number) or (variable == "prcp" and number < 0):
            raise InputError(f"Invalid historical value: {key}/{year}/{member}")
        values[key][year].append(number)
    return {
        key: {year: np.asarray(v, dtype=np.float64) for year, v in years.items()}
        for key, years in values.items()
    }
