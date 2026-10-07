"""Independently verify fresh station rows, raw response hashes and daily means."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path
from typing import TypedDict, cast

ROOT = Path(__file__).resolve().parents[1]
FRESH = ROOT / "observations/kmahub_refresh"
SOURCE = ROOT / "GLOSEA6_KMA_20220301-20260831_v1"


class Retrieval(TypedDict):
    start: str
    end: str
    relative_path: str
    stored_sha256: str
    sha256: str
    bytes: int
    rows: int


class Provenance(TypedDict):
    stations: list[int]
    source_daily_sha256: str
    station_daily_sha256: str
    requests: list[Retrieval]
    source_start: str
    source_end: str
    station_date_rows: int
    daily_rows: int
    counts: dict[str, dict[str, int]]


def digest(payload: bytes) -> str:
    """Hash exact shipped or downloaded bytes, not normalized text."""
    return hashlib.sha256(payload).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    """Read the compact CSV tables without invoking the production loader."""
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    """Require all independent identities before emitting a passing audit."""
    if sys.argv[1:] == ["--help"]:
        print("Usage: python analysis/audit_fresh_observations.py\n" +
              "Audit observations/kmahub_refresh without modifying supplied inputs.")
        return
    if sys.argv[1:]:
        raise SystemExit("Unexpected arguments; use --help")
    metadata = rows(SOURCE / "metadata/asos_kma_station_list.csv")
    stations = {int(row["STN"]) for row in metadata}
    if len(metadata) != 62 or len(stations) != 62:
        raise ValueError("The original station list is not 62 unique IDs")
    for record in rows(SOURCE / "MANIFEST.csv"):
        original = SOURCE / record["RELATIVE_PATH"]
        if original.stat().st_size != int(record["BYTES"]) or \
                digest(original.read_bytes()) != record["SHA256"]:
            raise ValueError(f"Original manifest changed: {record['RELATIVE_PATH']}")
    # This schema is the persisted contract of collect_observations.mjs.
    # The following audit independently verifies its data identities.
    provenance = cast(Provenance, json.loads((FRESH / "provenance.json").read_text(encoding="utf-8")))
    if set(provenance["stations"]) != stations:
        raise ValueError("Fresh and original station sets differ")
    if digest((FRESH / "asos_kma_daily.csv.gz").read_bytes()) != provenance["source_daily_sha256"]:
        raise ValueError("Fresh daily digest differs")
    if digest((FRESH / "station_daily.csv.gz").read_bytes()) != provenance["station_daily_sha256"]:
        raise ValueError("Fresh station digest differs")
    raw: dict[tuple[str, int], tuple[float, float]] = {}
    for request in provenance["requests"]:
        packed = (FRESH / request["relative_path"]).read_bytes()
        if digest(packed) != request["stored_sha256"]:
            raise ValueError("Stored response digest differs")
        payload = gzip.decompress(packed)
        if len(payload) != request["bytes"] or digest(payload) != request["sha256"]:
            raise ValueError("Uncompressed response digest differs")
        text = payload.decode("euc-kr")
        if "#START7777" not in text or "#7777END" not in text:
            raise ValueError("Incomplete response")
        headers = sorted(
            (int(match[1]), match[2])
            for match in re.finditer(r"^#\s*(\d+)\.\s+([A-Z0-9_]+)\s*:", text, re.MULTILINE)
        )
        names = [name for _, name in headers]
        indexes = {name: names.index(name) for name in ("TM", "STN", "TA_AVG", "RN_DAY")}
        count = 0
        for line in text.splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            cells = line.strip().removesuffix(",").split(",") if "," in line else line.split()
            if len(cells) != len(names):
                raise ValueError("Malformed raw response row")
            day, station = cells[indexes["TM"]], int(cells[indexes["STN"]])
            if station not in stations or not request["start"] <= day <= request["end"] \
                    or not provenance["source_start"] <= day <= provenance["source_end"]:
                raise ValueError("Raw row outside station/date request")
            key = (day, station)
            if key in raw:
                raise ValueError(f"Duplicate raw station/date: {key}")
            raw[key] = (float(cells[indexes["TA_AVG"]]), float(cells[indexes["RN_DAY"]]))
            count += 1
        if count != request["rows"]:
            raise ValueError("Raw request row count differs")
    station_seen: set[tuple[str, int]] = set()
    temperatures: dict[str, list[float]] = defaultdict(list)
    rain: dict[str, list[float]] = defaultdict(list)
    station_counts: Counter[str] = Counter()
    expected_gaps: Counter[tuple[str, int, str, str]] = Counter()
    with gzip.open(FRESH / "station_daily.csv.gz", "rt", encoding="utf-8", newline="") as handle:
        for record in csv.DictReader(handle):
            day, station = record["DATE"], int(record["STN"])
            key = (day, station)
            if key in station_seen or key not in raw:
                raise ValueError("Station export duplicated or absent from raw response")
            station_seen.add(key)
            t, p = float(record["TA_AVG_RAW"]), float(record["RN_DAY_RAW"])
            if (t, p) != raw[key]:
                raise ValueError("Station export differs from raw measurement")
            tv = math.isfinite(t) and t > -90
            pv = math.isfinite(p) and (p >= 0 or p == -9)
            if int(record["T15M_VALID"]) != int(tv) or int(record["PRCP_VALID"]) != int(pv):
                raise ValueError("Station validity differs")
            if tv:
                temperatures[day].append(t)
            else:
                expected_gaps[(day, station, "TEMPERATURE_VALUE_MISSING", str(t))] += 1
            if pv:
                value = 0.0 if p == -9 else p
                if float(record["PRCP"]) != value:
                    raise ValueError("Station precipitation normalization differs")
                rain[day].append(value)
            else:
                if record["PRCP"]:
                    raise ValueError("Invalid precipitation was filled")
                expected_gaps[(day, station, "PRECIPITATION_VALUE_MISSING", str(p))] += 1
            station_counts[day] += 1
    if station_seen != raw.keys():
        raise ValueError("Station export omitted a raw measurement")
    daily = rows(FRESH / "asos_kma_daily.csv.gz")
    original_daily = {record["DATE"]: record for record in rows(SOURCE / "data/asos/asos_kma_daily.csv.gz")}
    start = date.fromisoformat(f"{provenance['source_start'][:4]}-" +
                              f"{provenance['source_start'][4:6]}-{provenance['source_start'][6:]}")
    end = date.fromisoformat(f"{provenance['source_end'][:4]}-" +
                            f"{provenance['source_end'][4:6]}-{provenance['source_end'][6:]}")
    dates = {(start + timedelta(days=i)).strftime("%Y%m%d") for i in range((end - start).days + 1)}
    if len(daily) != len(dates) or {record["DATE"] for record in daily} != dates:
        raise ValueError("Fresh daily calendar is incomplete or duplicated")
    independent_counts: dict[str, Counter[int]] = {
        "temperature": Counter(), "precipitation": Counter(), "station_rows": Counter(),
    }
    max_difference = {"temperature": 0.0, "precipitation": 0.0}
    old_difference = {"temperature": 0.0, "precipitation": 0.0}
    changed_counts = {"temperature": 0, "precipitation": 0}
    for record in daily:
        day = record["DATE"]
        if record["AREA"] != "kma" or int(record["N_STATION_TOTAL"]) != 62 or \
                int(record["N_STATION_REQUIRED"]) != 50:
            raise ValueError("Daily station/QC policy changed")
        independent_counts["station_rows"][station_counts[day]] += 1
        for station in stations:
            if (day, station) not in station_seen:
                expected_gaps[(day, station, "STATION_DATE_ROW_MISSING", "")] += 1
        for variable, field, values in (
            ("temperature", "T15M", temperatures[day]),
            ("precipitation", "PRCP", rain[day]),
        ):
            count = len(values)
            independent_counts[variable][count] += 1
            if int(record[f"N_STATION_{field}"]) != count:
                raise ValueError("Daily contributor count differs from independent raw observations")
            expected_qc = "OK" if count >= 50 else "INSUFFICIENT_VALID_STATIONS"
            if record[f"QC_{field}"] != expected_qc:
                raise ValueError("Derived daily QC differs")
            value = float(record[field])
            if count:
                difference = abs(value - math.fsum(values) / count)
                max_difference[variable] = max(max_difference[variable], difference)
                if difference > 1e-12:
                    raise ValueError("Daily mean differs from independently summed station values")
            elif not math.isnan(value):
                raise ValueError("No-observation day was filled")
            if day in original_daily:
                old = original_daily[day]
                old_difference[variable] = max(old_difference[variable], abs(value - float(old[field])))
                changed_counts[variable] += int(int(old[f"N_STATION_{field}"]) != count)
    actual_gaps: Counter[tuple[str, int, str, str]] = Counter()
    for gap in rows(FRESH / "coverage_gaps.csv"):
        value = str(float(gap["RAW_VALUE"])) if gap["RAW_VALUE"] else ""
        actual_gaps[(gap["DATE"], int(gap["STN"]), gap["ISSUE"], value)] += 1
    if expected_gaps != actual_gaps:
        raise ValueError("Coverage gap ledger differs from raw data")
    if provenance["station_date_rows"] != len(raw) or provenance["daily_rows"] != len(daily):
        raise ValueError("Provenance row counts differ")
    for variable, counted in independent_counts.items():
        if {str(key): value for key, value in counted.items()} != provenance["counts"][variable]:
            raise ValueError("Provenance count distributions differ")
    result = {
        "status": "PASS", "manifest_verified_files": 24, "stations": 62,
        "daily_rows": len(daily), "station_date_rows": len(raw),
        "source_start": provenance["source_start"], "source_end": provenance["source_end"],
        "requests_verified": len(provenance["requests"]),
        "counts": {key: dict(value) for key, value in independent_counts.items()},
        "gap_records": sum(expected_gaps.values()), "maximum_independent_mean_difference": max_difference,
        "maximum_original_daily_difference": old_difference, "original_contributor_count_changes": changed_counts,
        "source_daily_sha256": provenance["source_daily_sha256"],
    }
    _ = (FRESH / "independent_audit.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
