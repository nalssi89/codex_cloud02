#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "matplotlib==3.11.2"]
# ///
# How to run: uv run analysis/make_report.py
"""Reproduce the Korean verification report from completed pipeline outputs."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
import sys
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Literal, NotRequired, Protocol, TextIO, TypedDict

import matplotlib
import numpy as np
from numpy.typing import NDArray

matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.container import BarContainer
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.text import Annotation, Text

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analysis.data_io import Json, csv_rows

METHODS: Final = ("RAW", "QM", "QDM", "EMOS")
GROUPS: Final = (("1mon", "t15m"), ("1mon", "prcp"), ("3mon", "t15m"), ("3mon", "prcp"))
LABELS: Final = {"1mon": "주간", "3mon": "월간", "t15m": "기온", "prcp": "강수"}
SEED: Final = 20261006
REPLICATES: Final = 500
type Row = Mapping[str, str]
type FloatArray = NDArray[np.float64]


class PlotAxes(Protocol):
    """Narrow typed surface for Matplotlib's extensible keyword APIs."""

    def bar(self, x: Sequence[str], height: Sequence[float], *, color: str) -> BarContainer: ...
    def barh(self, y: Sequence[str], width: Sequence[int], *, left: FloatArray,
             label: str, color: str) -> BarContainer: ...
    def bar_label(self, container: BarContainer, *, fmt: str = "%.2f", padding: int = 0,
                  fontsize: int = 9, labels: Sequence[str] = (), label_type: Literal["edge", "center"] = "edge") -> Sequence[Annotation]: ...
    def set_ylim(self, bottom: float, top: float) -> tuple[float, float]: ...
    def set_title(self, label: str) -> Text: ...
    def set_xlabel(self, xlabel: str) -> Text: ...
    def set_ylabel(self, ylabel: str) -> Text: ...
    def grid(self, *, axis: Literal["both", "x", "y"] = "both", alpha: float) -> None: ...
    def plot(self, x: Sequence[str], y: Sequence[float], *, marker: str,
             label: str) -> list[Line2D]: ...
    def axhline(self, y: float, *, color: str, linewidth: int, linestyle: str) -> Line2D: ...
    def legend(self, *, ncols: int, fontsize: int, loc: Literal["best", "upper center"] = "best",
               bbox_to_anchor: tuple[float, float] = (1, 1)) -> Legend: ...


class PlotFigure(Protocol):
    """Only the figure operations needed by this reproducible report."""

    def add_subplot(self, nrows: int, ncols: int, index: int) -> PlotAxes: ...
    def savefig(self, fname: Path, *, dpi: int, bbox_inches: str) -> None: ...


def plot_surface(figure: PlotFigure) -> PlotFigure:
    """Keep only the declared plotting API, not third-party unknown kwargs."""
    return figure


class AuditGroup(TypedDict):
    """Known data-audit group schema."""

    product: str
    variable: str
    total: int
    status_counts: dict[str, int]


class Audit(TypedDict):
    """Fields consumed from the pipeline audit."""

    total_cases: int
    eligible_target_cases: int
    declared_stations: int
    daily_temperature_station_counts: dict[str, int]
    daily_precipitation_station_counts: dict[str, int]
    observation_start: str
    observation_end: str
    forecast_init_start: str
    forecast_init_end: str
    groups: list[AuditGroup]
    observation_source: NotRequired[dict[str, Json]]


class RunSummary(TypedDict):
    """Completed verification status."""

    status: str
    cases_verified: int
    method_rows: dict[str, int]
    fit_failures: int
    elapsed_seconds: float
    observation_source: NotRequired[dict[str, Json]]


class ValidationSummary(TypedDict):
    status: str
    checks_total: int
    cases_verified: int


@dataclass(frozen=True, slots=True)
class Paired:
    """Exact-case improvement with exploratory initialization-year intervals."""

    product: str
    variable: str
    method: str
    n: int
    clusters: int
    crps_delta: float
    rmse_pct: float
    crps_ci: tuple[float, float] | None
    rmse_ci: tuple[float, float] | None

    def cells(self) -> list[str | int | float]:
        """CSV columns; unavailable intervals are blank, never zero-width."""
        return [
            self.product, self.variable, self.method, self.n, self.clusters,
            self.crps_delta, self.rmse_pct,
            *(self.crps_ci if self.crps_ci is not None else ("", "")),
            *(self.rmse_ci if self.rmse_ci is not None else ("", "")),
            REPLICATES, SEED,
            "unavailable: one cluster" if self.clusters < 2 else
            "exploratory: very few clusters" if self.clusters == 2 else "exploratory",
        ]


def read_rows(path: Path) -> list[Row]:
    """Read a UTF-8 pipeline table, including gzip predictions."""
    opener = gzip.open if path.suffix == ".gz" else Path.open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json[T](path: Path, loader: Callable[[TextIO], T]) -> T:
    """Apply the fixed pipeline JSON contract at its file boundary."""
    with path.open(encoding="utf-8") as handle:
        return loader(handle)


def read_audit(path: Path, loader: Callable[[TextIO], Audit] = json.load) -> Audit:
    """Read the fixed data-audit schema."""
    return read_json(path, loader)


def read_summary(path: Path, loader: Callable[[TextIO], RunSummary] = json.load) -> RunSummary:
    """Read the completed pipeline summary schema."""
    return read_json(path, loader)


def read_validation(
    path: Path, loader: Callable[[TextIO], ValidationSummary] = json.load,
) -> ValidationSummary:
    """Require the independently recalculated results before reporting completion."""
    return read_json(path, loader)


def number(row: Row, column: str) -> float:
    """Blank undefined scores remain NaN rather than invented zero values."""
    return float(row[column]) if row[column] else math.nan


def fmt(value: float) -> str:
    """Render missing numerical metrics explicitly."""
    return f"{value:.3f}" if math.isfinite(value) else "산출 불가"


def table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    """Render a compact Markdown table."""
    return "\n".join([
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
        *("| " + " | ".join(row) + " |" for row in rows),
    ])


def title(group: tuple[str, str]) -> str:
    """Label the product without implying a three-month total."""
    return f"{LABELS[group[0]]} {LABELS[group[1]]}"


def station_coverage(audit: Audit) -> str:
    """Describe actual contributors, not the size of the declared station list."""
    parts: list[str] = []
    for label, counts in (
        ("기온", audit["daily_temperature_station_counts"]),
        ("강수", audit["daily_precipitation_station_counts"]),
    ):
        parts.append(label + " " + " / ".join(
            f"{n}지점 {counts[n]:,}일" for n in sorted(counts, key=int)
        ))
    return f"지점 목록 {audit['declared_stations']}개; 실제 일별 기여: " + "; ".join(parts)


def observation_source_lines(audit: Audit) -> list[str]:
    """Report persisted run provenance, never the currently active selection."""
    source = audit.get("observation_source", {})
    if not source.get("selected"):
        return [
            "관측 출처: 원본 제공 권역 일평균. 수집 시각: 제공 자료에 기록 없음.",
            "제공 QC=OK 및 실제 변수별 기여 지점 최소 기준 충족; 개별 지점 행·기기 QC 검증 불가.",
        ]
    counts = source.get("counts")
    row_counts: Json = counts.get("station_rows", {}) if isinstance(counts, dict) else {}
    distribution = " / ".join(f"{n}지점 {days:,}일" for n, days in sorted(
        row_counts.items(), key=lambda item: int(item[0])
    ) if isinstance(days, int)) if isinstance(row_counts, dict) else "기록 없음"
    actual, expected = source["station_date_rows"], source["expected_station_date_rows"]
    if not isinstance(actual, int) or not isinstance(expected, int):
        raise SystemExit("Invalid station row counts in observation provenance")
    measurement_gaps: list[str] = []
    missing = source["missing_codes"]
    if not isinstance(missing, dict):
        raise SystemExit("Invalid missing measurement codes in observation provenance")
    for variable, label in (("temperature", "기온"), ("precipitation", "강수")):
        codes = missing[variable]
        if not isinstance(codes, dict) or any(not isinstance(n, int) for n in codes.values()):
            raise SystemExit("Invalid missing measurement counts in observation provenance")
        measurement_gaps.append(f"{label} 측정 무효 {sum(n for n in codes.values() if isinstance(n, int)):,}행")
    return [
        f"관측 출처: nalssi89/kmahub 정책의 KMA API Hub; 수집 완료 UTC: {source['retrieved_at_utc']}",
        f"수집 범위: {source['source_start']}–{source['source_end']}; "
        + f"지점·날짜 행 {source['station_date_rows']} / 기대 {source['expected_station_date_rows']}",
        f"최신 완결 관측일: {source['source_end']}; 이후 모델 검증 구간은 관측 미확보로 제외한다.",
        f"원 지점·날짜 행 누락 {expected - actual:,}행; "
        + " / ".join(measurement_gaps) + " (수집 행 내 변수별 측정 무효; 행 누락과 별개).",
        "지점 행 존재 분포: " + distribution,
        "QC는 측정값 유효성·변수별 기여 수에서 파생한 검사이며 KMA 원래 기기 QC가 아니다.",
    ]


def observation_policy(audit: Audit) -> str:
    """Distinguish supplied aggregates from newly collected station records."""
    if audit.get("observation_source", {}).get("selected"):
        return (
            "수집 지점·날짜 원자료의 변수별 유효 기여 지점을 동일 가중 평균한다. "
            "기온 > -90만 유효(-99·-99.9 제외); RN_DAY=-9는 kmahub 정책에 따라 0, "
            "다른 음수 강수는 제외한다. 각 변수 최소 50지점이며 행 존재와 측정값 유효성은 다르다. "
            "QC=OK는 파생 유효성·기여 수 검사이지 원래 KMA 기기 QC가 아니다."
        )
    return (
        "원본 일별 자료는 이미 평균된 제공 권역 평균이며 개별 지점 관측 행이 아니다. "
        "제공 N_STATION_REQUIRED 및 QC=OK를 적용한다. 개별 자료·공간 가중치가 없어 "
        "전국 평균 재구성이나 지점별 측정 유효성 검증은 불가하다."
    )


def station_audit(root: Path, audit: Audit) -> list[str]:
    """Stream retained station rows; never infer measurement validity from row presence."""
    source = audit.get("observation_source", {})
    if not source.get("selected"):
        return ["지점별 원자료 감사: 원본 제공 자료에는 지점별 관측 행이 없어 산출 불가."]
    path = root / str(source["relative_directory"]) / "station_daily.csv.gz"
    with path.open("rb") as handle:
        digest = hashlib.file_digest(handle, "sha256").hexdigest()
    if digest != source["station_daily_sha256"]:
        raise SystemExit("Station observation hash differs from recorded run provenance")
    present: Counter[str] = Counter()
    temperature: Counter[str] = Counter()
    precipitation: Counter[str] = Counter()
    for row in csv_rows(path):
        station = row["STN"]
        present[station] += 1
        temperature[station] += int(row["T15M_VALID"])
        precipitation[station] += int(row["PRCP_VALID"])
    stations = source["stations"]
    days = source["daily_rows"]
    if not isinstance(stations, list) or not isinstance(days, int):
        raise SystemExit("Invalid station coverage provenance")
    return [
        "### 지점별 수집 행·측정값 감사",
        "기록된 station_daily_sha256와 일치하는 원자료의 유효성 플래그를 직접 센다. "
        + "아래 행 누락 수는 지점×요청 일수 기준이며 기기 QC 판정이 아니다.",
        table(["STN", "수집 행", "행 누락", "유효 기온", "기온 무효", "유효 강수", "강수 무효"], [
            [str(station), str(present[str(station)]), str(days - present[str(station)]),
             str(temperature[str(station)]), str(present[str(station)] - temperature[str(station)]),
             str(precipitation[str(station)]), str(present[str(station)] - precipitation[str(station)])]
            for station in stations
        ]),
        "수집 JSON 감사(실측 기록; 행 완전성과 변수별 유효성은 별개):\n```json\n"
        + json.dumps({key: source[key] for key in (
            "counts", "missing_codes", "daily_rows", "station_date_rows",
            "expected_station_date_rows", "gap_records", "qc_flag_origin",
        )}, ensure_ascii=False, indent=2) + "\n```",
    ]


def qdm_audit_note(
    root: Path, audit: Audit,
    loader: Callable[[TextIO], dict[str, Json]] = json.load,
) -> str:
    """Keep strict floating-tolerance findings visible, separate from core validation."""
    path = root / "outputs/method_review/qm_qdm_audit.json"
    if not path.is_file():
        return "별도 QM/QDM 감사: 결과 없음; core validation PASS와 별개이다."
    result = read_json(path, loader)
    alerts = result.get("strict_tolerance_alerts", [])
    count = len(alerts) if isinstance(alerts, list) else "기록 없음"
    scope = (
        "관측 출처 일치" if result.get("observation_source") == audit.get("observation_source")
        else "현재 관측 출처와 불일치/미확인; 현 실행 검산으로 주장하지 않음"
    )
    return f"별도 QM/QDM 감사: {result['status']}; strict tolerance 경고 {count}건; {scope}."


def observation_counts(predictions: Sequence[Row], group: tuple[str, str]) -> tuple[int, int, Counter[str]]:
    """Count shared cases, distinct windows and case-specific observed terciles."""
    raw = [r for r in predictions if r["METHOD"] == "RAW"
           and (r["PRODUCT"], r["VARIABLE"]) == group]
    events = Counter("BN" if number(r, "OBS") <= number(r, "Q33") else
                     "NN" if number(r, "OBS") <= number(r, "Q67") else "AN" for r in raw)
    return len(raw), len({(r["VALID_START"], r["VALID_END"]) for r in raw}), events


def monthly_temperature_note(predictions: Sequence[Row]) -> str:
    """Keep sample caveats synchronized with the regenerated prediction artifact."""
    count, windows, events = observation_counts(predictions, ("3mon", "t15m"))
    return (f"월간 기온 {count:,}사례 / {windows:,}개 관측 구간; "
            f"BN={events['BN']:,}, NN={events['NN']:,}, AN={events['AN']:,}.")


def reference_policy_rows(ledger: Sequence[Row], predictions: Sequence[Row]) -> list[list[str]]:
    """Summarize accepted references used by verified cases, with separate units."""
    rows: list[list[str]] = []
    for group in GROUPS:
        ids = {r["CASE_ID"] for r in predictions if r["METHOD"] == "RAW"
               and (r["PRODUCT"], r["VARIABLE"]) == group}
        accepted = [r for r in ledger if r["STATUS"] == "OK" and r["CASE_ID"] in ids]
        differences = [r for r in accepted if r["REFERENCE_CHECK"] in (
            "DAILY_MEAN_POLICY_DIFFERENCE", "NEW_OBSERVATION_SOURCE_DIFFERENCE",
        )]
        rows.append([
            title(group), "°C" if group[1] == "t15m" else "mm",
            str(len(accepted)),
            str(sum(r["REFERENCE_CHECK"] == "MATCHED" for r in accepted)),
            str(len(differences)),
            f"{max(abs(number(r, 'REFERENCE_DIFF')) for r in differences):.10g}"
            if differences else "해당 없음",
        ])
    return rows


def paired_comparisons(predictions: Sequence[Row]) -> list[Paired]:
    """Resample whole INIT years, preserving all cases and their overlaps."""
    results: list[Paired] = []
    rng = np.random.default_rng(SEED)
    for product, variable in GROUPS:
        rows = [r for r in predictions if (r["PRODUCT"], r["VARIABLE"]) == (product, variable)]
        raw = {r["CASE_ID"]: r for r in rows if r["METHOD"] == "RAW"}
        for method in METHODS[1:]:
            corrected = {r["CASE_ID"]: r for r in rows if r["METHOD"] == method}
            ids = sorted(raw.keys() & corrected.keys())
            if len(ids) != len(raw) or len(ids) != len(corrected):
                raise SystemExit(f"Unpaired cases: {product}/{variable}/{method}")
            years = sorted({raw[key]["INIT_DATE"][:4] for key in ids})
            blocks: FloatArray = np.zeros((len(years), 5), dtype=np.float64)
            for index, year in enumerate(years):
                keys = [key for key in ids if raw[key]["INIT_DATE"][:4] == year]
                blocks[index] = [
                    len(keys),
                    math.fsum(number(raw[k], "CRPS") for k in keys),
                    math.fsum(number(corrected[k], "CRPS") for k in keys),
                    math.fsum((number(raw[k], "PRED_MEAN") - number(raw[k], "OBS")) ** 2 for k in keys),
                    math.fsum((number(corrected[k], "PRED_MEAN") - number(corrected[k], "OBS")) ** 2 for k in keys),
                ]
            totals: FloatArray = np.sum(blocks, axis=0)
            delta = float((totals.flat[1] - totals.flat[2]) / totals.flat[0])
            pct = 100 * (1 - math.sqrt(float(totals.flat[4] / totals.flat[3])))
            crps_ci = rmse_ci = None
            if len(years) >= 2:
                draws = rng.integers(0, len(years), size=(REPLICATES, len(years)))
                sampled: FloatArray = np.sum(blocks[draws], axis=1)
                differences: FloatArray = (sampled[:, 1] - sampled[:, 2]) / sampled[:, 0]
                percentages: FloatArray = 100 * (1 - np.sqrt(sampled[:, 4] / sampled[:, 3]))
                c = np.quantile(differences, [0.025, 0.975])
                p = np.quantile(percentages, [0.025, 0.975])
                crps_ci = (float(c.flat[0]), float(c.flat[1]))
                rmse_ci = (float(p.flat[0]), float(p.flat[1]))
            results.append(Paired(product, variable, method, len(ids), len(years), delta, pct, crps_ci, rmse_ci))
    return results


def make_figures(output: Path, metrics: Sequence[Row], leads: Sequence[Row], audit: Audit) -> list[Path]:
    """Save three readable unit-preserving small-multiple comparisons."""
    matplotlib.rcParams["font.family"] = ["Malgun Gothic", "DejaVu Sans"]
    matplotlib.rcParams["axes.unicode_minus"] = False
    paths = [output / name for name in (
        "method_comparison.png", "crps_skill_by_lead.png", "station_coverage_attrition.png",
    )]
    fig = plot_surface(Figure(figsize=(12, 14), layout="constrained"))
    for index, group in enumerate(GROUPS):
        rows = [r for r in metrics if (r["PRODUCT"], r["VARIABLE"]) == group]
        unit = "°C" if group[1] == "t15m" else "mm / target window"
        for column, score in enumerate(("RMSE", "CRPS")):
            ax = fig.add_subplot(4, 2, index * 2 + column + 1)
            ordered = sorted(rows, key=lambda r: number(r, score))
            bars = ax.bar([r["METHOD"] for r in ordered], [number(r, score) for r in ordered], color="#4477AA")
            _ = ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=9)
            _ = ax.set_ylim(0, max(number(r, score) for r in rows) * 1.18)
            _ = ax.set_title(f"{title(group)} — {score} (N={rows[0]['N']}, 낮을수록 우수)")
            _ = ax.set_ylabel(f"{score} ({unit})")
            ax.grid(axis="y", alpha=0.2)
    fig.savefig(paths[0], dpi=150, bbox_inches="tight")
    plt.close("all")
    fig = plot_surface(Figure(figsize=(12, 8), layout="constrained"))
    for index, group in enumerate(GROUPS, 1):
        ax = fig.add_subplot(2, 2, index)
        rows = [r for r in leads if (r["PRODUCT"], r["VARIABLE"]) == group]
        for method in METHODS:
            selected = sorted((r for r in rows if r["METHOD"] == method), key=lambda r: r["LEAD"])
            _ = ax.plot([r["LEAD"] for r in selected], [number(r, "CRPS_SKILL") for r in selected],
                    marker="o", label=method)
        _ = ax.axhline(0, color="black", linewidth=1, linestyle="--")
        _ = ax.set_title(title(group))
        _ = ax.set_xlabel("Lead (W: 주, M: 개별 달)")
        _ = ax.set_ylabel("CRPSS (무차원; 높을수록 우수)")
        ax.grid(alpha=0.2)
        _ = ax.legend(ncols=2, fontsize=9)
    fig.savefig(paths[1], dpi=150, bbox_inches="tight")
    plt.close("all")
    fig = plot_surface(Figure(figsize=(11, 6), layout="constrained"))
    ax = fig.add_subplot(1, 1, 1)
    groups = audit["groups"]
    labels = [title((g["product"], g["variable"])) for g in groups]
    left: FloatArray = np.zeros(len(groups), dtype=np.float64)
    statuses = sorted({status for g in groups for status in g["status_counts"]})
    for index, status in enumerate(statuses):
        label = {"OK": "검증 가능 (선택 관측 정책 충족)",
                 "TARGET_OBSERVATION_UNAVAILABLE": "검증 관측 기간 미확보"}.get(status, status)
        color = {"OK": "#228833", "TARGET_OBSERVATION_UNAVAILABLE": "#BBBBBB"}.get(
            status, ("#CCBB44", "#4477AA", "#AA3377")[index % 3])
        values = [g["status_counts"].get(status, 0) for g in groups]
        bars = ax.barh(labels, values, left=left, label=label, color=color)
        _ = ax.bar_label(bars, labels=[str(v) if v >= 90 else "" for v in values], label_type="center")
        left += np.asarray(values, dtype=np.float64)
    _ = ax.set_title("관측 정책 상태별 검증 관측 가용성")
    _ = ax.set_xlabel("예보 사례 수 (서로 독립인 관측 수가 아님)")
    _ = ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncols=3, fontsize=9)
    fig.savefig(paths[2], dpi=150, bbox_inches="tight")
    plt.close("all")
    return paths


def run(root: Path) -> None:
    """Generate only from completed outputs, without waiting or polling."""
    output = root / "outputs"
    required = [
        "data_audit.json", "run_summary.json", "matched_predictions.csv.gz",
        "calibration_fits.csv", "metrics_overall.csv", "metrics_by_lead.csv",
        "metrics_by_season.csv", "metrics_by_year.csv", "metrics_by_month.csv",
        "validation.json",
        "training_ledger.csv.gz",
    ]
    missing = [name for name in required if not (output / name).is_file()]
    if missing:
        raise SystemExit("Not ready; missing outputs: " + ", ".join(missing))
    audit = read_audit(output / "data_audit.json")
    summary = read_summary(output / "run_summary.json")
    validation = read_validation(output / "validation.json")
    if audit.get("observation_source") != summary.get("observation_source"):
        raise SystemExit("Observation provenance mismatch between audit and run summary")
    if summary["status"] != "PASS":
        raise SystemExit(f"Not ready; run status: {summary['status']}")
    if validation["status"] != "PASS" or validation["cases_verified"] != summary["cases_verified"]:
        raise SystemExit("Independent validation did not pass for all verified cases")
    metrics = read_rows(output / "metrics_overall.csv")
    leads = read_rows(output / "metrics_by_lead.csv")
    predictions = read_rows(output / "matched_predictions.csv.gz")
    fits = read_rows(output / "calibration_fits.csv")
    ledger = read_rows(output / "training_ledger.csv.gz")
    if len(metrics) != 16 or Counter(r["METHOD"] for r in predictions) != summary["method_rows"]:
        raise SystemExit("Input count mismatch: overall table or prediction rows")
    paired = paired_comparisons(predictions)
    paired_path = output / "paired_improvements.csv"
    with paired_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "PRODUCT", "VARIABLE", "METHOD", "N_PAIRED", "N_INIT_YEAR_CLUSTERS",
            "RAW_MINUS_METHOD_CRPS", "RMSE_REDUCTION_PCT", "CRPS_CI025", "CRPS_CI975",
            "RMSE_PCT_CI025", "RMSE_PCT_CI975", "BOOTSTRAP_REPLICATES", "SEED", "CI_STATUS",
        ])
        writer.writerows(p.cells() for p in paired)
    figures = make_figures(output, metrics, leads, audit)
    text = [
        "# GLOSEA6 실제 예보 검증 보고서",
        f"완료 상태: **{summary['status']}**, 전체 {audit['total_cases']:,}개 중 "
        + f"검증 {summary['cases_verified']:,}개, 각 방법 {summary['cases_verified']:,}행. "
        + f"EMOS 적합 실패 {summary['fit_failures']}건; 파이프라인 실행 {summary['elapsed_seconds']:.2f}초.",
        "## 1. 자료와 선택 편향: 결과 해석 전에 확인",
        f"관측: {audit['observation_start']}–{audit['observation_end']}; "
        + f"예보 초기일: {audit['forecast_init_start']}–{audit['forecast_init_end']}.",
        station_coverage(audit) + ".",
        *observation_source_lines(audit),
        *station_audit(root, audit),
        qdm_audit_note(root, audit),
        observation_policy(audit)
        + "평균에 62/n을 곱하지 않으며 누락 지점 값을 추정하거나 보간하지 않는다. "
        + "`1mon`은 주간 구간, `3mon`은 M01–M06의 **개별 달력 월**이며 3개월 합계가 아니다. "
        + "기온은 구간 평균(°C), 강수는 구간 누적(mm)이다.",
        "훈련 OBS의 기준은 사용자 승인 일별 정책(기온: 제공 일평균의 구간 평균; "
        + "강수: 제공 일값의 구간 합)이다. 새로 채택한 혼합 기여 지점 구간은 제공 기간 참조값과 "
        + "다를 수 있어 모든 source reference가 일치한다고 주장하지 않는다. "
        + "REFERENCE_CHECK는 MATCHED, DAILY_MEAN_POLICY_DIFFERENCE, "
        + "NEW_OBSERVATION_SOURCE_DIFFERENCE를 구별한다. "
        + "원본 정책에서 모든 날 62지점인 구간만 기존 참조 일치 검사(허용오차 0.0001)를 강제한다. "
        + "재수집 정책은 원본 참조값 차이를 기록하되 학습에 재수집 OBS를 사용하며, "
        + "독립 검산은 모든 채택 OBS를 원 일별 자료에서 정확히 재집계한다. "
        + "1991–2020 평년값은 관측값이나 훈련 삼분위를 대체하지 않는다.",
        table(["상품/변수", "차이 단위", "채택 훈련 행", "MATCHED", "정책/새 출처 차이",
                "정책 차이 행 최대 절대차"], reference_policy_rows(ledger, predictions)),
        "위 표는 검증된 사례가 사용한 STATUS=OK source-year 행 수이다. "
        + "동일 역사 구간이 여러 사례에 반복되므로 서로 다른 구간 수나 독립 표본 수가 아니다. "
        + "최대 차이는 정책 차이 행에만 적용하며 기온·강수 단위를 합산하지 않는다.",
    ]
    coverage: list[list[str]] = []
    statuses = sorted({status for g in audit["groups"] for status in g["status_counts"]})
    for g in audit["groups"]:
        count = sum(r["METHOD"] == "RAW" and (r["PRODUCT"], r["VARIABLE"]) == (g["product"], g["variable"]) for r in predictions)
        coverage.append([title((g["product"], g["variable"])), str(g["total"]), str(count),
                         f"{100 * count / g['total']:.1f}%",
                         *(str(g["status_counts"].get(status, 0)) for status in statuses)])
    text.append(table(["상품/변수", "전체", "검증", "유지율", *statuses], coverage))
    selection: list[list[str]] = []
    for group in GROUPS:
        raw = [r for r in predictions if r["METHOD"] == "RAW" and (r["PRODUCT"], r["VARIABLE"]) == group]
        years = Counter(r["INIT_DATE"][:4] for r in raw)
        windows = len({(r["VALID_START"], r["VALID_END"]) for r in raw})
        events = Counter("BN" if number(r, "OBS") <= number(r, "Q33") else
                         "NN" if number(r, "OBS") <= number(r, "Q67") else "AN" for r in raw)
        selection.append([title(group), "; ".join(f"{y}: {n}" for y, n in sorted(years.items())),
                          str(windows), *(f"{events[e]} ({100 * events[e] / len(raw):.1f}%)" for e in ("BN", "NN", "AN"))])
    text.extend([
        table(["상품/변수", "채택 INIT 연도: 사례 수", "서로 다른 검증 구간", "관측 BN", "관측 NN", "관측 AN"], selection),
        "**범주별 skill은 위 표의 실제 관측 범주 빈도와 함께 해석한다.** "
        + "빈도는 각 사례의 관측 기후 삼분위 경계로 분류한 값이며 중복 구간도 사례별로 센다. "
        + "서로 다른 구간 수도 독립 표본 수가 아니다. 전체 계절·연도 모집단의 기술로 일반화하지 않는다.",
        "## 2. 검증 설계와 보정",
        "원자료 hindcast는 1993–2016년 체계 6,104사례와 1993–2022년 체계 476사례로 구성되며 "
        + "후자는 2026-05-11 초기일부터 등장한다. 동일 사례의 source-year 예보/관측 쌍만 훈련한다. "
        + "**HIST_END < INIT_DATE, SOURCE_YEAR != target year** 조건을 강제한다. "
        + "무작위 교차검증이 아니며 hindcast 자체의 skill을 주장하는 결과도 아니다. "
        + "연도별 동일 가중치를 사용하고 연도마다 다른 앙상블 멤버 수를 보존한다. "
        + "보정 참조 출력은 알려진 누출과 legacy Kelvin 차이 때문에 보정·검증에 사용하지 않았다.",
        "QM: 경험적 분위수 매핑, 양 끝 확률 범위를 클리핑한다. "
        + "QDM: 원래 할당된 현재 앙상블 순위에서의 대수적 변화 관계; "
        + "기온은 가산 변화, 강수는 비율 변화이며 발행 분포의 정렬된 분위수 변화나 "
        + "기후 추세 보존을 보장하지 않는다. "
        + "건조 분모 0.1 mm 처리 예외를 기록한다. "
        + "EMOS: 기온 Gaussian / 강수 0에서 censored Gaussian의 CRPS 최소화, "
        + "4개 계수 a,b,c,d, b,d≥0 및 c>0 분산 하한 제약과 2개 초기점. "
        + "강수 예측 평균은 검열에 의한 0의 확률질량을 포함하며 잠재 μ가 아니다.",
        "구체적 식: H는 연도별 동일 가중치 재예측 경험분포, O는 해당 연도의 관측 경험분포, "
        + "F는 현재 예측 앙상블 경험분포이다. QM(x)=Q_O(F_H(x)); "
        + "QDM 기온=x+Q_O(p)−Q_H(p), QDM 강수=x×Q_O(p)/Q_H(p), p는 현재 앙상블의 동률 중간 순위이다. "
        + "경험분포는 동률 질량을 합친 중간 확률 위치에서 선형 보간한다. 강수 Q_H(p)<0.1 mm이면 "
        + "Q_O(p)를 사용하며 이 분기에서는 비율 변화 보존을 주장하지 않는다. "
        + "EMOS의 μ=a+b×앙상블평균, σ²=c+d×표본분산(ddof=1); 기온 Y~N(μ,σ²), "
        + "강수 Y=max(0,Z), Z~N(μ,σ²)이다. 연도별 평균 CRPS를 최소화하고 검증 관측은 적합에 넣지 않는다.",
        "원시모델은 VALUE 열을 사용했다. RAW_ANOM 및 이미 보정된 참조 출력은 사용하지 않았다. "
        + "원시 예측의 빈 VALUE 68행(기온·강수 각 34행, 총 4사례)은 0으로 채우지 않고 멤버에서 제외했다. "
        + "사례별 원래/유효/결측 멤버 수를 case_audit.csv에 남겼다.",
        "기온의 추세를 별도로 제거하거나 다시 더하지 않았다. QDM 분위수 변화와 EMOS 편향 조정 "
        + "외의 명시적 추세 처리가 있다고 해석해서는 안 된다.",
    ])
    fit_rows: list[list[str]] = []
    for group in GROUPS:
        selected = [r for r in fits if (r["PRODUCT"], r["VARIABLE"]) == group]
        fit_rows.append([title(group), str(len(selected)),
                         f"{min(number(r, 'N_TRAIN') for r in selected):.0f}–{max(number(r, 'N_TRAIN') for r in selected):.0f}",
                         str(sum(int(r["CONVERGED"]) for r in selected)),
                         str(sum(int(r["QDM_DRY_EXCEPTIONS"]) for r in selected)),
                         fmt(sum(number(r, "FIT_CRPS") for r in selected) / len(selected)),
                         fmt(sum(number(r, "INITIAL_CRPS") for r in selected) / len(selected))])
    text.append(table(["상품/변수", "적합 사례", "훈련 연도 수 범위", "수렴", "QDM 건조 예외 수", "평균 적합 CRPS", "평균 초기 CRPS"], fit_rows))
    text.extend([
        "## 3. 전체 성능 (16개 상품·변수·방법 조합)",
        "각 그룹 내부만 비교한다. 기온과 강수 또는 주간과 월간의 단위를 합산하지 않는다. "
        + "Bias=예측−관측; RMSE/MAE/CRPS는 낮을수록, ACC 및 skill은 높을수록 좋다.",
    ])
    for heading, columns in (
        ("### 결정론적 성능", ("BIAS", "RMSE", "MAE", "ACC", "CORRELATION")),
        ("### 확률 성능", ("CRPS", "CRPS_SKILL", "BRIER_SKILL", "RPS_SKILL", "COVERAGE90", "WIDTH90")),
        ("### 범주별 Brier 성능", ("BS_BN", "BS_BN_SKILL", "BS_NN", "BS_NN_SKILL", "BS_AN", "BS_AN_SKILL")),
    ):
        text.extend([heading, table(
            ["상품/변수", "N", "방법", *columns],
            [[title((r["PRODUCT"], r["VARIABLE"])), r["N"], r["METHOD"],
              *(fmt(number(r, c)) for c in columns)] for r in metrics],
        )])
    text.extend([
        "CRPSS=1−평균CRPS/평균기후CRPS; BSS와 RPSS도 같은 비율 정의. "
        + "삼분위는 훈련 관측의 선형 보간 1/3, 2/3 분위수이며 BN≤Q33, Q33<NN≤Q67, AN>Q67. "
        + "Brier는 3범주 제곱오차의 합, RPS는 2개 누적 경계 제곱오차의 합으로 정규화하지 않는다. "
        + "RAW/QM/QDM CRPS는 발행된 경험 분포의 CRPS이며 멤버 수 fairness 보정이 아니다. "
        + "ACC는 사례별 관측 기후 평균을 예측과 관측에서 각각 뺀 상관이다. "
        + "CORRELATION은 원값 상관으로 계절 주기가 포함되어 ACC와 다르다. "
        + "COVERAGE90은 5–95% 구간 포함률, WIDTH90은 같은 물리 단위의 구간 폭이다.",
        "## 4. 지표별 우승 방법과 리드별 결과",
    ])
    for group in GROUPS:
        selected = [r for r in metrics if (r["PRODUCT"], r["VARIABLE"]) == group]
        wins: list[str] = []
        for score in ("RMSE", "MAE", "CRPS", "ACC", "BRIER_SKILL", "RPS_SKILL"):
            finite = [r for r in selected if math.isfinite(number(r, score))]
            if finite:
                winner = min(finite, key=lambda r: number(r, score)) if score in ("RMSE", "MAE", "CRPS") else max(finite, key=lambda r: number(r, score))
                wins.append(f"{score}: {winner['METHOD']} ({fmt(number(winner, score))})")
        text.append(f"- **{title(group)}**: " + "; ".join(wins) + ".")
    lead_rows: list[list[str]] = []
    for group in GROUPS:
        selected = [r for r in leads if (r["PRODUCT"], r["VARIABLE"]) == group]
        for lead in sorted({r["LEAD"] for r in selected}):
            cases = [r for r in selected if r["LEAD"] == lead]
            rmse = min(cases, key=lambda r: number(r, "RMSE"))
            crps = min(cases, key=lambda r: number(r, "CRPS"))
            lead_rows.append([title(group), lead, cases[0]["N"],
                              f"{rmse['METHOD']} / {fmt(number(rmse, 'RMSE'))}",
                              f"{crps['METHOD']} / {fmt(number(crps, 'CRPS'))}",
                              "; ".join(f"{r['METHOD']}: {fmt(number(r, 'CRPS_SKILL'))}" for r in cases)])
    text.append(table(["상품/변수", "리드", "N", "최소 RMSE", "최소 CRPS", "방법별 CRPSS"], lead_rows))
    text.append("0 미만 CRPSS는 해당 사례의 훈련 관측 기후 분포보다 불리함을 뜻한다. "
                + "리드별 표본 수가 달라 단순 리드 추세를 인과 효과로 해석하지 않는다.")
    for dimension in ("season", "year", "month"):
        rows = read_rows(output / f"metrics_by_{dimension}.csv")
        column = {"season": "SEASON", "year": "YEAR", "month": "VALID_MONTH"}[dimension]
        text.append(f"### {column}별 CRPS 최소 방법 (YEAR는 검증 구간 시작 연도)")
        subsets = sorted({(r["PRODUCT"], r["VARIABLE"], r[column]) for r in rows})
        winners: list[list[str]] = []
        for product, variable, value in subsets:
            selected = [r for r in rows if (r["PRODUCT"], r["VARIABLE"], r[column]) == (product, variable, value)]
            best = min(selected, key=lambda r: number(r, "CRPS"))
            winners.append([title((product, variable)), value, best["N"], best["METHOD"],
                            fmt(number(best, "CRPS")), fmt(number(best, "CRPS_SKILL"))])
        text.append(table(["상품/변수", column, "N", "최소 CRPS 방법", "CRPS", "CRPSS"], winners))
    text.extend([
        "## 5. RAW 대비 정확히 같은 사례의 개선과 탐색적 민감도",
        "CASE_ID를 상품·변수 내부에서 정확히 짝지었다. ΔCRPS=RAW−방법, "
        + "RMSE 개선율=100×(RAW RMSE−방법 RMSE)/RAW RMSE이며 양수는 개선이다. "
        + f"INIT 연도 전체 군집을 복원 추출한 {REPLICATES}회 year-block bootstrap, seed={SEED}, "
        + "2.5/97.5 백분위 구간이다. 선택된 연도의 모든 겹치는 사례를 함께 보존하고 RMSE를 매번 재계산한다. "
        + "독립 사례 가정이나 통계적 유의성 주장이 아닌 **탐색적 민감도**이다. "
        + "군집 1개면 구간 산출 불가, 2개면 극히 약한 근거이다. 연도 경계를 넘는 구간의 의존성까지 "
        + "제거하지 못하며 약 5년 자료만으로 일반적 우월성·유의성을 선언할 수 없다.",
        table(["상품/변수", "방법", "짝 N", "INIT 연도 군집", "ΔCRPS [탐색 구간]", "RMSE 개선 % [탐색 구간]"], [
            [title((p.product, p.variable)), p.method, str(p.n), str(p.clusters),
             f"{fmt(p.crps_delta)} " + (f"[{fmt(p.crps_ci[0])}, {fmt(p.crps_ci[1])}]" if p.crps_ci else "[산출 불가]"),
             f"{fmt(p.rmse_pct)} " + (f"[{fmt(p.rmse_ci[0])}, {fmt(p.rmse_ci[1])}]" if p.rmse_ci else "[산출 불가]")]
            for p in paired
        ]),
        "## 6. 한계와 재현",
        "주간·월간 사례와 검증 기간이 겹치며 월간 동일 관측 구간이 여러 초기일에 반복된다. "
        + "관측 미확보 구간, 범주 불균형, 짧은 검증 기간, 운영 당시 모델의 실제 "
        + "가용성과 공간 가중치 미확인 때문에 이 결과는 선택 관측 정책을 충족한 표본에 한정한다. "
        + "HIST_END < INIT_DATE는 날짜 조건이며 재예측 모델의 운영 당시 가용성을 입증하지 않는다. "
        + "QDM은 단일 예보 앙상블 순위 기반 변형으로, 순위 교차 가능성이 있어 발행 분포의 "
        + "정렬된 분위수 변화나 기후 추세 보존을 보장하지 않는다. "
        + "적합 CRPS는 훈련 목적함수이며 실제 발행 예보 CRPS와 혼동하지 않는다.",
        "독립 검산: **PASS**. 전체 채택 사례의 일관측 집계, 재예측 연도·날짜, 확률합, "
        + "직접 멤버 쌍거리 CRPS, Brier/RPS, 전체 요약 지표를 별도 구현으로 재계산했다. "
        + "8개 실제 사례에서는 검증 관측을 변경해도 적합 계수와 예측이 변하지 않음을 재적합으로 확인했다. "
        + "체크 횟수는 반복된 자료 불변조건 검사 수이며 독립 표본 수나 유의성 근거가 아니다. "
        + f"기계 판독 근거는 validation.json ({validation['checks_total']:,}회 검사)이다.",
        "### 생성 및 입력 파일",
        *[f"- `{name}`" for name in required],
        "- `observed_targets.csv`, `case_audit.csv`: 관측 구간 및 제외 사유",
        "- `training_ledger.csv.gz`, `calibrated_members.csv.gz`: 훈련 쌍과 보정 멤버",
        "- `REPORT_KO.md`, `paired_improvements.csv`: 보고서 및 짝 비교",
        *[f"- `{path.name}`" for path in figures],
        *[f"![{path.stem}]({path.name})" for path in figures],
        "### 정확한 실행 명령 (프로젝트 루트)",
        "```sh\n.venv/Scripts/python.exe analysis/run_verification.py\n"
        + ".venv/Scripts/python.exe analysis/validate_results.py\n"
        + ".venv/Scripts/python.exe analysis/make_report.py\n"
        + ".venv/Scripts/python.exe analysis/make_report.py --help\n"
        + "uv run analysis/run_verification.py\nuv run analysis/validate_results.py\n"
        + "uv run analysis/make_report.py\n```",
        "보고서 생성기는 입력 완료 여부를 한 번 확인하고 대기하지 않는다. "
        + "Python ≥3.12, numpy==2.5.3, matplotlib==3.11.2; headless Agg, PNG 150 dpi.",
    ])
    report = output / "REPORT_KO.md"
    _ = report.write_text("\n\n".join(text) + "\n", encoding="utf-8")
    print(f"Verified cases: {summary['cases_verified']}; prediction rows: {len(predictions)}")
    for path in (report, paired_path, *figures):
        print(path)


def main() -> None:
    """CLI matching the pipeline's no-arguments/--help convention."""
    if sys.argv[1:] == ["--help"]:
        print("Usage: python analysis/make_report.py\n"
              + "Read completed outputs/; create REPORT_KO.md, paired_improvements.csv and three PNGs.")
        return
    if sys.argv[1:]:
        raise SystemExit("Unexpected arguments; use --help")
    run(Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    main()
