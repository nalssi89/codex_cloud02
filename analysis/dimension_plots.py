"""Canonical, source-audited comparisons for the dimension PDF."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Final, Literal, TypedDict, assert_never

from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from analysis.data_io import CsvCell
from analysis.pdf_plot_surface import PdfAxes, PdfFigure, figure_surface

Row = Mapping[str, str]
DimensionName = Literal["lead", "month", "season", "year"]
METHODS: Final = ("RAW", "QM", "QDM", "EMOS")
GROUPS: Final = (("1mon", "t15m"), ("1mon", "prcp"), ("3mon", "t15m"), ("3mon", "prcp"))
COLORS: Final = ("#4D4D4D", "#0072B2", "#009E73", "#D55E00")
MARKERS: Final = ("o", "s", "^", "D")
PAGE_SIZE: Final = (11.6929, 8.2677)


@dataclass(frozen=True, slots=True)
class Dimension:
    name: DimensionName
    label: str
    column: str


DIMENSIONS: Final = (
    Dimension("lead", "리드타임", "LEAD"),
    Dimension("month", "월", "VALID_MONTH"),
    Dimension("season", "계절", "SEASON"),
    Dimension("year", "연도", "YEAR"),
)
FAMILIES: Final = (
    ("deterministic", "결정론적 성능", ("BIAS", "MAE", "RMSE", "CORRELATION", "ACC", "N")),
    ("probabilistic", "전체 확률 성능", ("CRPS", "CRPS_SKILL", "BRIER", "BRIER_SKILL", "RPS", "RPS_SKILL")),
    ("tercile", "범주별 확률 성능", ("BS_BN", "BS_BN_SKILL", "BS_NN", "BS_NN_SKILL", "BS_AN", "BS_AN_SKILL")),
    ("interval", "예측구간과 평균값", ("COVERAGE90", "WIDTH90", "OBS_MEAN", "PRED_MEAN")),
)
REFERENCES: Final = {
    "CRPS": "CLIM_CRPS", "BRIER": "CLIM_BRIER", "RPS": "CLIM_RPS",
    "BS_BN": "CLIM_BS_BN", "BS_NN": "CLIM_BS_NN", "BS_AN": "CLIM_BS_AN",
    "PRED_MEAN": "OBS_MEAN",
}


class PageRecord(TypedDict):
    page: int
    kind: str
    dimension: str
    product: str
    variable: str
    family: str
    title: str
    figure: str


def group_name(product: str, variable: str) -> str:
    """Use the package's real weekly/individual-month interpretation."""
    return ("주간" if product == "1mon" else "월간") + (" 기온" if variable == "t15m" else " 강수")


def canonical_bins(dimension: Dimension, product: str) -> tuple[str, ...]:
    """No lexical month sorting and no disappearance of missing calendar bins."""
    match dimension.name:
        case "lead":
            count, prefix = (8, "W") if product == "1mon" else (6, "M")
            return tuple(f"{prefix}{n:02d}" for n in range(1, count + 1))
        case "month":
            return tuple(str(n) for n in range(1, 13))
        case "season":
            return ("DJF", "MAM", "JJA", "SON")
        case "year":
            return tuple(str(n) for n in range(2022, 2027))
    assert_never(dimension.name)


def metric_title(metric: str, variable: str) -> str:
    """Explain orientation and physical units rather than opaque field names."""
    unit = "°C" if variable == "t15m" else "mm / 대상 구간"
    names = {
        "BIAS": f"Bias ({unit}) · 0에 가까울수록 우수",
        "MAE": f"MAE ({unit}) · 낮을수록 우수",
        "RMSE": f"RMSE ({unit}) · 낮을수록 우수",
        "CORRELATION": "원값 상관 · 높을수록 우수",
        "ACC": "ACC (기후평균 제거 상관) · 높을수록 우수",
        "N": "동일 검증 사례 수 N · 독립 관측 수 아님",
        "CRPS": f"CRPS ({unit}) · 낮을수록 우수",
        "BRIER": "3범주 Brier 합 · 낮을수록 우수",
        "RPS": "RPS (2경계 합) · 낮을수록 우수",
        "CRPS_SKILL": "CRPSS · 높을수록 우수",
        "BRIER_SKILL": "BSS · 높을수록 우수",
        "RPS_SKILL": "RPSS · 높을수록 우수",
        "COVERAGE90": "90% 예측구간 포함률 · 기준 0.90",
        "WIDTH90": f"90% 예측구간 폭 ({unit})",
        "OBS_MEAN": f"채택 관측 평균 ({unit})",
        "PRED_MEAN": f"예측 평균 ({unit}) · 점선은 관측 평균",
    }
    if metric in names:
        return names[metric]
    label = metric.split("_")[1]
    if metric.endswith("_SKILL"):
        return f"{label} 범주 BSS · 높을수록 우수"
    return f"{label} 범주 Brier · 낮을수록 우수"


def page_heading(figure: PdfFigure, title: str, page: int) -> None:
    """Shared header, method encoding and footer for every plotted page."""
    _ = figure.text(0.05, 0.954, title, fontsize=17, weight="bold")
    handles = [
        Line2D([], [], color=color, marker=marker, label=method, linewidth=1.5)
        for method, color, marker in zip(METHODS, COLORS, MARKERS, strict=True)
    ]
    handles.append(Line2D([], [], color="#888888", linestyle="--", label="기후/관측 기준"))
    _ = figure.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.047, 0.922), ncols=5,
                      frameon=False, fontsize=10)
    _ = figure.text(0.05, 0.025, "자료: 검증 완료 CSV | 같은 사례의 네 방법 비교 | 공백은 결측, 0 아님",
                    fontsize=8.5, color="#555555")
    _ = figure.text(0.95, 0.025, f"{page} / 68", fontsize=9, ha="right")


def append_series(
    records: list[Mapping[str, CsvCell]], page: int, dimension: Dimension,
    product: str, variable: str, family: str, metric: str, method: str,
    bins: Sequence[str], lookup: Mapping[tuple[str, str], Row], source_file: str,
) -> list[float]:
    """Export exactly what reaches the plot, including explicit absent bins."""
    result: list[float] = []
    source_method = "RAW" if method == "REFERENCE" else method
    for bin_name in bins:
        row = lookup.get((source_method, bin_name))
        value = float(row[metric]) if row is not None and row[metric] else math.nan
        result.append(value)
        records.append({
            "PAGE": page, "DIMENSION": dimension.name, "PRODUCT": product, "VARIABLE": variable,
            "FAMILY": family, "METRIC": metric, "METHOD": method, "BIN": bin_name,
            "VALUE": value if math.isfinite(value) else None,
            "N": int(row["N"]) if row is not None else None,
            "PRESENT": int(row is not None), "SOURCE_FILE": source_file,
        })
    return result


def draw_metric(
    axes: PdfAxes, metric: str, bins: Sequence[str], values: Sequence[Sequence[float]],
    reference: Sequence[float] | None, variable: str, dimension: Dimension,
) -> None:
    """Four method lines share axes; NaN gaps never bridge missing bins."""
    positions = list(range(len(bins)))
    if metric in ("N", "OBS_MEAN"):
        _ = axes.bar(positions, values[0], color="#888888", width=0.55)
    else:
        for series, color, marker in zip(values, COLORS, MARKERS, strict=True):
            _ = axes.plot(positions, series, color=color, marker=marker, linewidth=1.5,
                          markersize=4.5)
    if reference is not None:
        _ = axes.plot(positions, reference, color="#888888", linestyle="--", linewidth=1.1)
    if metric == "BIAS" or metric.endswith("_SKILL") or metric in ("ACC", "CORRELATION"):
        _ = axes.axhline(0, color="#777777", linewidth=0.8, linestyle=":")
    if metric in ("ACC", "CORRELATION"):
        _ = axes.set_ylim(-1.05, 1.05)
    if metric == "COVERAGE90":
        _ = axes.axhline(0.9, color="#777777", linestyle=":", linewidth=1)
        _ = axes.set_ylim(0, 1.05)
    if metric == "N":
        for pos, number in zip(positions, values[0], strict=True):
            if math.isfinite(number):
                _ = axes.text(pos, number, f"{number:.0f}", ha="center", va="bottom", fontsize=8)
        finite = [v for v in values[0] if math.isfinite(v)]
        _ = axes.set_ylim(0, max(finite) * 1.25)
    _ = axes.set_title(metric_title(metric, variable), fontsize=10.5, loc="left", pad=9)
    _ = axes.set_xticks(positions, list(bins), fontsize=9)
    axes.tick_params(axis="y", labelsize=9)
    _ = axes.set_xlabel(dimension.label + (" (검증 구간 시작 기준)" if dimension.name != "lead" else ""),
                        fontsize=9)
    axes.grid(axis="y", alpha=0.2)
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)
    _ = axes.set_xlim(-0.45, len(bins) - 0.55)


def chart_page(
    rows: Sequence[Row], dimension: Dimension, product: str, variable: str,
    family: str, family_label: str, metrics: Sequence[str], page: int,
    records: list[Mapping[str, CsvCell]],
    coverage_note: str = "",
) -> PdfFigure:
    """Make one A4-landscape page with a complete auditable metric family."""
    bins = canonical_bins(dimension, product)
    relevant = [r for r in rows if (r["PRODUCT"], r["VARIABLE"]) == (product, variable)]
    lookup = {(r["METHOD"], r[dimension.column]): r for r in relevant}
    if len(lookup) != len(relevant):
        raise RuntimeError(f"Duplicate grouped score keys: {dimension.name}/{product}/{variable}")
    figure = figure_surface(Figure(figsize=PAGE_SIZE))
    page_heading(figure, f"{dimension.label}별 | {group_name(product, variable)} | {family_label}", page)
    nrows = 3 if len(metrics) == 6 else 2
    figure.subplots_adjust(left=0.075, right=0.97, bottom=0.15, top=0.84, hspace=0.65, wspace=0.24)
    source_file = f"outputs/metrics_by_{dimension.name}.csv"
    exported_reference: set[str] = set()
    for index, metric in enumerate(metrics, 1):
        values = [
            append_series(records, page, dimension, product, variable, family,
                          metric, method, bins, lookup, source_file)
            for method in METHODS
        ]
        reference = None
        if metric in REFERENCES:
            reference_metric = REFERENCES[metric]
            if reference_metric not in exported_reference:
                reference = append_series(records, page, dimension, product, variable, family,
                                          reference_metric, "REFERENCE", bins, lookup, source_file)
                exported_reference.add(reference_metric)
        axes = figure.add_subplot(nrows, 2, index)
        draw_metric(axes, metric, bins, values, reference, variable, dimension)
    note = "N은 네 방법이 공유하는 사례 수이며 회색 막대는 한 번만 표시합니다."
    if dimension.name == "season":
        note += " DJF=12·1·2, MAM=3·4·5, JJA=6·7·8, SON=9·10·11."
    if product == "3mon" and variable == "t15m":
        note = coverage_note + " 중복 구간·범주 빈도를 고려하며 결측은 0이 아닙니다."
    _ = figure.text(0.05, 0.062, note, fontsize=9, color="#7A3A00")
    return figure
