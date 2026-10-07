#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "matplotlib==3.11.2", "pypdf==6.19.0",
#                 "pymupdf==1.28.2", "pillow==12.3.0"]
# ///
"""Independent source-to-PDF integrity audit; no generator/scorer is imported.

Numerical PASS is not visual-layout approval. Every actual PDF page is rendered
at 150 dpi, with four-page contact sheets for the separate human visual review.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
import re
import sys
from collections import Counter
from collections.abc import Callable, Mapping, Sequence, Sized
from contextlib import ExitStack
from dataclasses import dataclass, field
from datetime import date, timedelta
from importlib.metadata import version
from io import BytesIO
from pathlib import Path
from types import ModuleType
from typing import Protocol

import pymupdf
from PIL import Image as PillowImage
from pypdf import PdfReader

METHODS = ("RAW", "QM", "QDM", "EMOS")
PRODUCTS = ("1mon", "3mon")
VARIABLES = ("t15m", "prcp")
FIELDS = {"lead": "LEAD", "month": "VALID_MONTH", "season": "SEASON", "year": "YEAR"}
FAMILIES = {
    "deterministic": ("BIAS", "MAE", "RMSE", "CORRELATION", "ACC", "N"),
    "probabilistic": ("CRPS", "CRPS_SKILL", "BRIER", "BRIER_SKILL", "RPS", "RPS_SKILL"),
    "tercile": ("BS_BN", "BS_BN_SKILL", "BS_NN", "BS_NN_SKILL", "BS_AN", "BS_AN_SKILL"),
    "interval": ("COVERAGE90", "WIDTH90", "OBS_MEAN", "PRED_MEAN"),
}
REFERENCES = {
    "deterministic": (),
    "probabilistic": ("CLIM_CRPS", "CLIM_BRIER", "CLIM_RPS"),
    "tercile": ("CLIM_BS_BN", "CLIM_BS_NN", "CLIM_BS_AN"),
    "interval": ("OBS_MEAN",),
}
EXPORT_FIELDS = (
    "PAGE", "DIMENSION", "PRODUCT", "VARIABLE", "FAMILY", "METRIC",
    "METHOD", "BIN", "VALUE", "N", "PRESENT", "SOURCE_FILE",
)
PINNED = {
    "numpy": "2.5.3", "matplotlib": "3.11.2", "pypdf": "6.19.0",
    "pymupdf": "1.28.2", "pillow": "12.3.0",
}
SourceKey = tuple[str, str, str, str]
PlotKey = tuple[int, str, str, str]
type JsonValue = None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
load_json: Callable[[str], JsonValue] = json.loads


class ReaderPage(Protocol):
    def extract_text(self) -> str: ...


class Reader(Protocol):
    @property
    def pages(self) -> Sequence[ReaderPage]: ...
    @property
    def outline(self) -> Sized: ...
    def close(self) -> None: ...


class Rect(Protocol):
    @property
    def width(self) -> float: ...
    @property
    def height(self) -> float: ...


class Pixmap(Protocol):
    @property
    def width(self) -> int: ...
    @property
    def height(self) -> int: ...
    @property
    def samples(self) -> bytes: ...
    def save(self, filename: str) -> None: ...


class Page(Protocol):
    @property
    def rect(self) -> Rect: ...
    def get_text(self, option: str = "text") -> JsonValue: ...
    def get_pixmap(self, *, dpi: int, alpha: bool) -> Pixmap: ...
    def get_drawings(self) -> Sized: ...
    def get_images(self) -> Sized: ...
    def get_fonts(self) -> Sequence[tuple[int, str, str, str, str, str]]: ...


class Document(Protocol):
    @property
    def page_count(self) -> int: ...
    def load_page(self, index: int) -> Page: ...
    def extract_font(self, xref: int) -> tuple[str, str, str, bytes]: ...
    def get_toc(self) -> list[list[JsonValue]]: ...
    def close(self) -> None: ...


class DocumentFactory(Protocol):
    def __call__(self, *, stream: bytes, filetype: str) -> Document: ...


def open_document(
    payload: bytes,
    loader: Callable[[ModuleType, str], DocumentFactory] = getattr,
) -> Document:
    """Read an immutable snapshot without holding the producer's disk file."""
    return loader(pymupdf, "open")(stream=payload, filetype="pdf")


@dataclass(frozen=True, slots=True)
class Entry:
    page: int
    kind: str
    dimension: str
    product: str
    variable: str
    family: str
    title: str
    figure: str


@dataclass(slots=True)
class Audit:
    """Mutable run accumulator: checks append evidence and increment counters."""

    errors: list[str] = field(default_factory=list)
    checks: int = 0
    pages: list[JsonValue] = field(default_factory=list)
    compared: int = 0
    gaps: int = 0
    bookmarks: list[JsonValue] = field(default_factory=list)

    def check(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.errors.append(message)


def mapping(value: JsonValue) -> Mapping[str, JsonValue]:
    if not isinstance(value, dict):
        raise TypeError("Expected JSON object")
    return value


def sequence(value: JsonValue) -> Sequence[JsonValue]:
    if not isinstance(value, list):
        raise TypeError("Expected JSON array")
    return value


def integer(value: JsonValue) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"Expected integer, got {value!r}")
    return value


def string(value: JsonValue) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Expected string, got {value!r}")
    return value


def number(value: JsonValue) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"Expected number, got {value!r}")
    return float(value)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return list(reader.fieldnames or ()), list(reader)


def equal_number(actual: str, expected: str) -> bool:
    if actual == "" or expected == "":
        return actual == expected
    try:
        a, b = float(actual), float(expected)
        return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= 1e-12
    except ValueError:
        return False


def compact(text: str) -> str:
    return re.sub(r"[\s|]+", "", text)


def source_observation(
    daily: Mapping[str, Mapping[str, str]], case: Mapping[str, str],
) -> tuple[float | None, int]:
    """Rebuild the source QC-qualified mean/sum and actual contributor minimum."""
    start, end = date.fromisoformat(case["VALID_START"]), date.fromisoformat(case["VALID_END"])
    period = [daily.get((start + timedelta(days=i)).strftime("%Y%m%d"))
              for i in range((end - start).days + 1)]
    if not period or any(row is None for row in period):
        return None, 0
    present = [row for row in period if row is not None]
    variable = "PRCP" if case["VARIABLE"] == "prcp" else "T15M"
    minimum = min(int(row[f"N_STATION_{variable}"]) for row in present)
    values: list[float] = []
    for row in present:
        count = int(row[f"N_STATION_{variable}"])
        value = float(row[variable]) if row[variable] else math.nan
        if row[f"QC_{variable}"] != "OK" \
                or not 0 < int(row["N_STATION_REQUIRED"]) <= count <= int(row["N_STATION_TOTAL"]) \
                or not math.isfinite(value):
            return None, minimum
        values.append(value)
    total = math.fsum(values)
    return (total if case["VARIABLE"] == "prcp" else total / len(values)), minimum


def bins(dimension: str, product: str, years: Sequence[str]) -> tuple[str, ...]:
    if dimension == "lead":
        return tuple(f"W{i:02}" for i in range(1, 9)) if product == "1mon" else tuple(
            f"M{i:02}" for i in range(1, 7))
    if dimension == "month":
        return tuple(str(i) for i in range(1, 13))
    if dimension == "season":
        return ("DJF", "MAM", "JJA", "SON")
    return tuple(years)


def numerical(root: Path, audit: Audit) -> list[Entry]:
    manifest = mapping(load_json((root / "outputs/pdf_manifest.json").read_text(encoding="utf-8-sig")))
    audit.check(integer(manifest["total_pages"]) == 68, "Manifest total_pages must be 68")
    pdf_path = Path(string(manifest["pdf"]))
    audit.check(pdf_path.parent == Path("outputs") and pdf_path.suffix == ".pdf"
                and (root / pdf_path).is_file(), "Manifest PDF must identify an existing outputs PDF")
    hashes = mapping(manifest["source_hashes"])
    sources: dict[str, dict[SourceKey, dict[str, str]]] = {}
    initial: dict[str, str] = {}
    for filename, expected_hash in hashes.items():
        initial[filename] = digest(root / filename)
        audit.check(initial[filename] == string(expected_hash), f"Source hash mismatch: {filename}")
    for dim, column in FIELDS.items():
        filename = f"outputs/metrics_by_{dim}.csv"
        path = root / filename
        initial[filename] = digest(path)
        audit.check(hashes.get(filename) == initial[filename], f"Source hash mismatch: {filename}")
        _, source_rows = rows(path)
        table: dict[SourceKey, dict[str, str]] = {}
        for row in source_rows:
            key = (row["PRODUCT"], row["VARIABLE"], row["METHOD"], row[column])
            audit.check(key not in table, f"Duplicate original source key: {dim}/{key}")
            table[key] = row
        sources[dim] = table
        groups: dict[tuple[str, str, str], list[str]] = {}
        for (product, variable, _method, bin_value), row in table.items():
            groups.setdefault((product, variable, bin_value), []).append(row["N"])
        for key, counts in groups.items():
            audit.check(len(counts) == 4 and len(set(counts)) == 1,
                        f"Unequal/missing method sample counts: {dim}/{key}")
    years = sorted({key[3] for key in sources["year"]}, key=int)
    audit.check(years == [str(i) for i in range(2022, 2027)], "Unexpected year union")
    entries: list[Entry] = []
    for raw in sequence(manifest["pages"]):
        row = mapping(raw)
        entries.append(Entry(integer(row["page"]), *(string(row[k]) for k in (
            "kind", "dimension", "product", "variable", "family", "title", "figure"))))
    audit.check([e.page for e in entries] == list(range(1, 69)), "Manifest page sequence is not 1..68")
    audit.check(len(entries) == 68, "Manifest must contain 68 entries")
    coverage: set[tuple[str, str, str, str]] = set()
    expected: dict[PlotKey, tuple[Entry, dict[str, str] | None, str]] = {}
    for entry in entries:
        if entry.page <= 4:
            audit.check(entry.kind == "frontmatter" and not any((
                entry.dimension, entry.product, entry.variable, entry.family, entry.figure)),
                f"Invalid frontmatter metadata: page {entry.page}")
            continue
        audit.check(entry.kind == "chart", f"Page {entry.page} is not a chart")
        identity = (entry.dimension, entry.product, entry.variable, entry.family)
        valid = (entry.dimension in FIELDS and entry.product in PRODUCTS
                 and entry.variable in VARIABLES and entry.family in FAMILIES)
        audit.check(valid and identity not in coverage, f"Invalid/duplicate chart family: {identity}")
        if not valid:
            continue
        coverage.add(identity)
        audit.check(entry.figure.startswith("outputs/dimension_figures/")
                    and (root / entry.figure).is_file(), f"Missing chart PNG: {entry.figure}")
        for metric in FAMILIES[entry.family]:
            for method in METHODS:
                for bin_value in bins(entry.dimension, entry.product, years):
                    source = sources[entry.dimension].get((entry.product, entry.variable, method, bin_value))
                    expected[(entry.page, metric, method, bin_value)] = (entry, source, metric)
        for metric in REFERENCES[entry.family]:
            for bin_value in bins(entry.dimension, entry.product, years):
                source = sources[entry.dimension].get((entry.product, entry.variable, "RAW", bin_value))
                expected[(entry.page, metric, "REFERENCE", bin_value)] = (entry, source, metric)
    audit.check(len(coverage) == 64, f"Chart coverage: {len(coverage)}/64")
    figure_paths = {e.figure for e in entries if e.kind == "chart"}
    actual_figures = {p.relative_to(root).as_posix() for p in (root / "outputs/dimension_figures").glob("*.png")}
    audit.check(len(figure_paths) == 64 and actual_figures == figure_paths, "PNG coverage is not exactly 64")
    header, exported = rows(root / "outputs/pdf_plot_data.csv")
    audit.check(tuple(header) == EXPORT_FIELDS, f"Incorrect plot CSV schema: {header}")
    seen: set[PlotKey] = set()
    for row in exported:
        key = (int(row["PAGE"]), row["METRIC"], row["METHOD"], row["BIN"])
        audit.check(key not in seen, f"Duplicate exported key: {key}")
        seen.add(key)
        audit.check(key in expected, f"Unexpected exported key: {key}")
        if key not in expected:
            continue
        entry, source, metric = expected[key]
        audit.check(all(row[column] == value for column, value in (
            ("DIMENSION", entry.dimension), ("PRODUCT", entry.product),
            ("VARIABLE", entry.variable), ("FAMILY", entry.family),
            ("SOURCE_FILE", f"outputs/metrics_by_{entry.dimension}.csv"))),
            f"Export metadata mismatch: {key}")
        present = source is not None
        audit.check(row["PRESENT"] == ("1" if present else "0"), f"Incorrect PRESENT: {key}")
        expected_value = source[metric] if source is not None else ""
        expected_n = source["N"] if source is not None else ""
        audit.check(equal_number(row["VALUE"], expected_value), f"Value mismatch: {key}")
        audit.check(equal_number(row["N"], expected_n), f"N mismatch: {key}")
        audit.compared += 1
        audit.gaps += int(not present)
    audit.check(seen == set(expected), f"Incomplete canonical export grid: missing {len(set(expected) - seen)}")
    for filename, before in initial.items():
        audit.check(digest(root / filename) == before, f"Source changed during audit: {filename}")
    return entries


def contact_sheets(paths: Sequence[Path], destination: Path) -> list[str]:
    new: Callable[[str, tuple[int, int], str], PillowImage.Image] = PillowImage.new
    open_image: Callable[[str], PillowImage.Image] = PillowImage.open
    destination.mkdir(parents=True, exist_ok=True)
    result: list[str] = []
    for start in range(0, len(paths), 4):
        canvas = new("RGB", (3200, 2260), "white")
        for offset, path in enumerate(paths[start:start + 4]):
            image = open_image(str(path))
            image.thumbnail((1600, 1130))
            canvas.paste(image, ((offset % 2) * 1600, (offset // 2) * 1130))
            image.close()
        path = destination / f"contact_{start // 4 + 1:03}.png"
        canvas.save(str(path))
        canvas.close()
        result.append(str(path))
    return result


def frontmatter_audit(root: Path, texts: Sequence[str], audit: Audit) -> None:
    """Compare rendered summary values and factual counts with original outputs."""
    _, overall = rows(root / "outputs/metrics_overall.csv")
    table = {(r["PRODUCT"], r["VARIABLE"], r["METHOD"]): r for r in overall}
    for page_number, columns in (
        (3, ("BIAS", "MAE", "RMSE", "CORRELATION", "ACC")),
        (4, ("CRPS", "CRPS_SKILL", "BRIER_SKILL", "RPS_SKILL", "COVERAGE90", "WIDTH90")),
    ):
        text = compact(texts[page_number - 1])
        for product in PRODUCTS:
            for variable in VARIABLES:
                for method in METHODS:
                    row = table[(product, variable, method)]
                    expected = row["N"] + method + "".join(
                        f"{float(row[column]):.3f}" if row[column] else "결측" for column in columns
                    )
                    audit.check(expected in text,
                                f"Rounded summary row mismatch: page {page_number}/{product}/{variable}/{method}")
    source = mapping(load_json((root / "outputs/run_summary.json").read_text(encoding="utf-8-sig")))
    data = mapping(load_json((root / "outputs/data_audit.json").read_text(encoding="utf-8-sig")))
    cover = compact(texts[0]).replace(",", "")
    for key in ("cases_accounted", "cases_verified"):
        audit.check(str(integer(source[key])) in cover, f"Cover source count missing: {key}")
    _, cases = rows(root / "outputs/case_audit.csv")
    statuses = Counter(row["STATUS"] for row in cases)
    audit.check({key: integer(value) for key, value in mapping(source["case_status_counts"]).items()}
                == dict(statuses), "Run summary statuses differ from accounted cases")
    for key, count in statuses.items():
        if key != "VERIFIED":
            audit.check(str(count) in cover, f"Cover exclusion count missing: {key}/{count}")
    audit.check(integer(source["cases_accounted"]) == len(cases)
                and integer(source["cases_verified"]) == statuses["VERIFIED"],
                "Run summary case counts differ from accounted cases")
    provenance = mapping(data.get("observation_source", {}))
    audit.check(provenance == mapping(source.get("observation_source", {})),
                "Observation provenance differs between run summary and data audit")
    daily_relative = string(provenance.get(
        "daily_relative_path",
        "GLOSEA6_KMA_20220301-20260831_v1/data/asos/asos_kma_daily.csv.gz",
    ))
    daily_path = (root / daily_relative).resolve()
    if not daily_path.is_relative_to(root.resolve()) or Path(daily_relative).is_absolute():
        raise ValueError("Observation daily path must stay inside the project")
    if "source_daily_sha256" in provenance:
        audit.check(digest(daily_path) == string(provenance["source_daily_sha256"]),
                    "Selected daily observations differ from completed-run provenance")
    manifest = mapping(load_json((root / "outputs/pdf_manifest.json").read_text(encoding="utf-8-sig")))
    audit.check(mapping(manifest.get("observation_source", {})) == provenance,
                "PDF manifest observation provenance differs from completed run")
    audit.check(daily_relative in mapping(manifest["source_hashes"]),
                "PDF manifest does not hash the selected daily source")
    if provenance.get("selected"):
        audit.check(string(provenance["source_end"]) in texts[0],
                    "Latest complete observation endpoint missing from cover")
        audit.check(compact(string(provenance["retrieved_at_utc"])) in compact(texts[0]),
                    "Selected source collection UTC missing from cover")
        guidance_text = compact(texts[1])
        audit.check("원래기기QC아님" in guidance_text,
                    "Derived validity/count QC must not claim original instrument QC")
        for key in ("station_date_rows", "expected_station_date_rows"):
            audit.check(str(integer(provenance[key])) in guidance_text,
                        f"Selected station audit count missing: {key}")
    _, daily_rows = rows(daily_path)
    daily = {row["DATE"]: row for row in daily_rows}
    audit.check(len(daily) == len(daily_rows) and all(row["AREA"] == "kma" for row in daily_rows),
                "Duplicate/wrong-area source daily observations")
    for case in cases:
        value, stations = source_observation(daily, case)
        audit.check(int(case["N_STATION_MIN"]) == stations,
                    f"Source contributor minimum mismatch: {case['CASE_ID']}")
        if case["STATUS"] == "VERIFIED":
            audit.check(value is not None and equal_number(case["OBS"], repr(value)),
                        f"Source QC/observation mismatch: {case['CASE_ID']}")
        else:
            audit.check(value is None or int(case["FCST_VALID"]) < 2,
                        f"Available source observation excluded: {case['CASE_ID']}")
    for key in ("forecast_init_start", "forecast_init_end", "observation_start", "observation_end"):
        audit.check(string(data[key]) in cover, f"Cover source date missing: {key}")
    for product in PRODUCTS:
        for variable in VARIABLES:
            audit.check(table[(product, variable, "RAW")]["N"] in cover,
                        f"Cover group sample count missing: {product}/{variable}")
    monthly_temperature = [
        r for r in cases if r["PRODUCT"] == "3mon" and r["VARIABLE"] == "t15m" and r["STATUS"] == "VERIFIED"
    ]
    windows = {(r["VALID_START"], r["VALID_END"]) for r in monthly_temperature}
    audit.check(len(monthly_temperature) == int(table[("3mon", "t15m", "RAW")]["N"]),
                "Monthly temperature metric count differs from verified cases")
    audit.check(str(len(monthly_temperature)) in cover and f"{len(windows)}개" in cover,
                "Monthly temperature case/window counts missing from cover")
    guidance = compact(texts[1]).replace("\\", "/")
    for command in (
        ".venv/Scripts/python.exeanalysis/make_dimension_pdf.py",
        ".venv/Scripts/python.exeanalysis/validate_dimension_pdf.py",
    ):
        audit.check(command in guidance, f"PDF reproduction command missing: {command}")
    audit.check("3개월누적이아닙니다" in guidance, "Missing non-aggregate 3mon interpretation warning")
    audit.check("VALID_START" in guidance, "Missing VALID_START grouping criterion")
    _, predictions = rows(root / "outputs/matched_predictions.csv.gz")
    monthly_predictions = [row for row in predictions
                           if row["PRODUCT"] == "3mon" and row["VARIABLE"] == "t15m"
                           and row["METHOD"] == "RAW"]
    audit.check(len(monthly_predictions) == len(monthly_temperature),
                "Monthly temperature prediction coverage differs from verified cases")
    no_middle_events = bool(monthly_predictions) and all(
        float(row["EVENT_NN"]) == 0 for row in monthly_predictions
    )
    audit.check(("NN=0" in cover) == no_middle_events,
                "Monthly temperature NN=0 warning differs from source events")


def pdf_audit(pdf: Path, entries: Sequence[Entry], output: Path, dpi: int, audit: Audit) -> list[str]:
    read_pdf: Callable[[BytesIO], Reader] = PdfReader
    payload = pdf.read_bytes()
    with ExitStack() as resources:
        stream = resources.enter_context(BytesIO(payload))
        reader = read_pdf(stream)
        _ = resources.callback(reader.close)
        document = open_document(payload)
        _ = resources.callback(document.close)
        sheets = inspect_document(reader, document, entries, output, dpi, audit)
        audit.check(digest(pdf) == hashlib.sha256(payload).hexdigest(),
                    "PDF changed while its immutable snapshot was rendered")
        return sheets


def inspect_document(
    reader: Reader, document: Document, entries: Sequence[Entry],
    output: Path, dpi: int, audit: Audit,
) -> list[str]:
    """Inspect borrowed PDF resources; their caller closes them even on failure."""
    audit.check(len(reader.pages) == 68, f"pypdf page count: {len(reader.pages)}/68")
    audit.check(bool(reader.outline), "Missing PDF navigation bookmarks")
    audit.check(document.page_count == len(reader.pages), "PDF parser page counts disagree")
    expected_navigation = [(1, 1), (1, 3)]
    for first in (5, 21, 37, 53):
        expected_navigation.append((1, first))
        expected_navigation.extend((2, first + group * 4) for group in range(4))
    navigation = document.get_toc()
    audit.check([(integer(item[0]), integer(item[2])) for item in navigation] == expected_navigation,
                "Bookmark hierarchy or destination pages differ from the dimension/group coverage")
    audit.bookmarks = [
        {"level": integer(item[0]), "title": string(item[1]), "page": integer(item[2])}
        for item in navigation
    ]
    output.mkdir(parents=True, exist_ok=True)
    rendered: list[Path] = []
    all_text: list[str] = []
    embedded: dict[int, bool] = {}
    for index in range(document.page_count):
        page = document.load_page(index)
        text = reader.pages[index].extract_text()
        all_text.append(text)
        entry = entries[index] if index < len(entries) else None
        if entry is not None and entry.kind == "frontmatter":
            title_components = {
                1: ("GloSea6", "예측 성능", "검증 보고서"),
                2: ("읽는 법",),
                3: ("결정론", "성능", "요약"),
                4: ("확률", "성능", "요약"),
            }[entry.page]
            title_ok = all(compact(component) in compact(text) for component in title_components)
        else:
            title_ok = entry is not None and compact(entry.title) in compact(text)
        audit.check(title_ok, f"Extracted title/page identity mismatch: page {index + 1}")
        audit.check(f"{index + 1}/68" in compact(text), f"Printed page index mismatch: page {index + 1}")
        audit.check(bool(re.search(r"[가-힣]", text)), f"No selectable Korean text: page {index + 1}")
        audit.check("\ufffd" not in text and "\x00" not in text, f"Replacement/tofu text: page {index + 1}")
        width, height = page.rect.width, page.rect.height
        # PyMuPDF uses tuples for bboxes; normalize that external payload into
        # genuine JSON arrays before applying the recursive JSON schema.
        text_dict = mapping(load_json(json.dumps(page.get_text("dict"))))
        clipped: list[JsonValue] = []
        bounds: list[JsonValue] = []
        for raw_block in sequence(text_dict["blocks"]):
            block = mapping(raw_block)
            if block.get("type") != 0:
                continue
            for raw_line in sequence(block["lines"]):
                for raw_span in sequence(mapping(raw_line)["spans"]):
                    span = mapping(raw_span)
                    bbox: list[JsonValue] = [number(v) for v in sequence(span["bbox"])]
                    bounds.append({"text": span["text"], "bbox": list(bbox)})
                    if (number(bbox[0]) < -0.5 or number(bbox[1]) < -0.5
                            or number(bbox[2]) > width + 0.5 or number(bbox[3]) > height + 0.5):
                        clipped.append(bounds[-1])
        audit.check(not clipped, f"Text outside physical page: page {index + 1}")
        fonts = page.get_fonts()
        for font in fonts:
            xref = font[0]
            if xref not in embedded:
                embedded[xref] = bool(document.extract_font(xref)[3])
        audit.check(bool(fonts) and all(embedded[f[0]] for f in fonts),
                    f"Unembedded font resources: page {index + 1}")
        drawings = len(page.get_drawings())
        images = len(page.get_images())
        if entry is not None and entry.kind == "chart":
            audit.check(drawings >= 10 and images == 0,
                        f"Chart is not authentic vector output: page {index + 1}, drawings={drawings}, images={images}")
        pix = page.get_pixmap(dpi=dpi, alpha=False)
        capture = output / f"page_{index + 1:03}.png"
        pix.save(str(capture))
        rendered.append(capture)
        samples = pix.samples
        ink = sum(value < 245 for value in samples) / len(samples)
        audit.check(ink > 0.001, f"Nearly blank rendered page: {index + 1}")
        audit.pages.append({
            "page": index + 1, "capture": str(capture), "sha256": digest(capture),
            "width_points": width, "height_points": height,
            "width_pixels": pix.width, "height_pixels": pix.height,
            "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "title_matches": title_ok, "text": text, "text_bounds": bounds,
            "clipped_text": clipped, "nonwhite_channel_fraction": ink,
            "vector_objects": drawings, "raster_images": images,
            "embedded_fonts": [f[3] for f in fonts if embedded[f[0]]],
        })
    frontmatter_audit(output.parents[2], all_text, audit)
    audit.check(len(rendered) == 68, f"Rendered page coverage: {len(rendered)}/68")
    return contact_sheets(rendered, output.parent / "contact_sheets")


def main() -> int:
    arguments = sys.argv[1:]
    if arguments == ["--help"]:
        print("Usage: validate_dimension_pdf.py [--help | --dpi 150]\n" + (__doc__ or ""))
        return 0
    if arguments not in ([], ["--dpi", "150"]):
        print("Invalid arguments. Usage: validate_dimension_pdf.py [--help | --dpi 150]", file=sys.stderr)
        return 2
    root = Path(__file__).resolve().parents[1]
    manifest = mapping(load_json((root / "outputs/pdf_manifest.json").read_text(encoding="utf-8-sig")))
    pdf = root / string(manifest["pdf"])
    dpi = 150
    audit = Audit()
    sheets: list[str] = []
    versions = {package: version(package) for package in PINNED}
    for package, pinned in PINNED.items():
        audit.check(versions[package] == pinned, f"Version mismatch: {package}={versions[package]}, expected {pinned}")
    try:
        entries = numerical(root, audit)
        sheets = pdf_audit(pdf, entries, root / "outputs/pdf_qa/pages", dpi, audit)
    except (OSError, ValueError, KeyError, TypeError) as error:
        audit.errors.append(f"{type(error).__name__}: {error}")
    report: dict[str, JsonValue] = {
        "status": "PASS" if not audit.errors else "FAIL",
        "scope": "Independent numerical and static PDF functional integrity; human visual approval required separately",
        "checks": audit.checks, "compared_records": audit.compared,
        "missing_bin_records": audit.gaps, "rendered_pages": len(audit.pages),
        "dpi": dpi, "pdf": str(pdf), "versions": {k: v for k, v in versions.items()},
        "pdf_sha256": digest(pdf) if pdf.is_file() else None,
        "errors": list(audit.errors), "pages": audit.pages, "contact_sheets": list(sheets),
        "bookmarks": audit.bookmarks,
        "static_pdf_ui": {"motion": "N/A", "keyboard_interaction": "N/A",
                          "navigation": "bookmarks checked", "text_selection": "extraction checked"},
        "visual_layout_status": "NOT_CLAIMED",
    }
    manifest = mapping(load_json((root / "outputs/pdf_manifest.json").read_text(encoding="utf-8-sig")))
    source_hashes: dict[str, JsonValue] = {}
    for filename, expected_hash in mapping(manifest["source_hashes"]).items():
        actual_hash = digest(root / filename)
        audit.check(actual_hash == string(expected_hash), f"Source changed after rendering: {filename}")
        source_hashes[filename] = actual_hash
    report["source_hashes"] = source_hashes
    report["status"] = "PASS" if not audit.errors else "FAIL"
    report["checks"] = audit.checks
    report["capture_list"] = [
        mapping(page)["capture"] for page in audit.pages
    ]
    destination = root / "outputs/pdf_validation.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    _ = destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in (
        "status", "checks", "compared_records", "missing_bin_records", "rendered_pages", "errors")},
        ensure_ascii=False))
    print(f"Evidence: {destination}")
    return 0 if not audit.errors else 1


if __name__ == "__main__":
    sys.exit(main())
