"""Independent scalar content-hash wire replay shared by vector source audits."""

import hashlib
import json
from datetime import date

from analysis.alternative_validation_io import decode, sequence, text
from analysis.alternative_validation_reference import vector
from analysis.data_io import Json


def row_ids(value: str) -> list[str]:
    return [text(v) for v in sequence(decode(value))]


def years(value: str) -> set[int]:
    entries = sequence(decode(value))
    if not all(isinstance(v, int) and not isinstance(v, bool) for v in entries):
        raise ValueError("held-out years must be integers")
    return {int(str(v)) for v in entries}


def year_block(start: date, end: date, heldout: set[int]) -> bool:
    return any(start.year <= year <= end.year for year in heldout)


def training_digest(rows: list[dict[str, str]], cutoff: str, catalog: str,
                    heldout: str) -> str:
    digest = hashlib.sha256()
    digest.update(json.dumps([cutoff, catalog, sorted(years(heldout))],
                             separators=(",", ":")).encode())
    for row in sorted(rows, key=lambda r: r["row_id"]):
        payload: list[Json] = [
            row["row_id"], row["source_case_id"], row["source_case_init"],
            int(row["source_year"]), row["source_init"], row["hist_start"], row["hist_end"],
            row["product"], row["variable"], row["lead"],
            float(row["observation"]).hex(), sequence(decode(row["member_keys"])),
            sequence(decode(row["source_files"])), row["provenance_hash"], row["archive_era"],
        ]
        digest.update(json.dumps(payload, separators=(",", ":")).encode())
        digest.update(vector(decode(row["ensemble"])).tobytes())
    return digest.hexdigest()
