#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.3", "matplotlib==3.11.2", "pypdf==6.19.0"]
# ///
# How to run: uv run analysis/make_dimension_pdf.py
"""Produce the complete four-dimension PDF without changing verification scores."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Final

import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
from pypdf import PdfReader, PdfWriter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.data_io import CsvCell, write_csv
from analysis.dimension_plots import (
    DIMENSIONS,
    FAMILIES,
    GROUPS,
    PAGE_SIZE,
    PageRecord,
    chart_page,
    group_name,
)
from analysis.make_report import (
    monthly_temperature_note,
    qdm_audit_note,
    read_audit,
    read_rows,
    read_summary,
    read_validation,
    title,
)
from analysis.pdf_plot_surface import PdfFigure, figure_surface, pdf_sink

PDF_NAME: Final = "GLOSEA6_verification_by_dimension_KO.pdf"


def source_digest(path: Path) -> str:
    """Snapshot source bytes so independent QA can detect accidental edits."""
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def prose_page(title: str, paragraphs: Sequence[str], page: int) -> PdfFigure:
    """Explicit line breaks keep Korean clauses together and text selectable."""
    figure = figure_surface(Figure(figsize=PAGE_SIZE))
    _ = figure.text(0.055, 0.91, title, fontsize=23, weight="bold")
    y = 0.81
    for paragraph in paragraphs:
        _ = figure.text(0.055, y, paragraph, fontsize=12, va="top", linespacing=1.5)
        y -= 0.037 * (paragraph.count("\n") + 1) + 0.025
    if y < 0.06:
        raise RuntimeError(f"Front matter overflows page {page}")
    if page == 2:
        _ = figure.text(0.055, 0.105, "재현: .venv/Scripts/python.exe analysis/make_dimension_pdf.py",
                        fontsize=9, color="#555555")
        _ = figure.text(0.055, 0.075, "검산: .venv/Scripts/python.exe analysis/validate_dimension_pdf.py",
                        fontsize=9, color="#555555")
    _ = figure.text(0.055, 0.028, "GloSea6 | 선택 관측 정책 충족 권역 평균 검증 | 완료 결과 시각화",
                    fontsize=9, color="#555555")
    _ = figure.text(0.95, 0.028, f"{page} / 68", fontsize=9, ha="right")
    return figure


def summary_page(rows: Sequence[Mapping[str, str]], probability: bool, page: int,
                 coverage_note: str = "") -> PdfFigure:
    """Complete sixteen-row overall summary, not only the winning methods."""
    figure = figure_surface(Figure(figsize=PAGE_SIZE))
    title = "전체 확률 성능 요약" if probability else "전체 결정론적 성능 요약"
    _ = figure.text(0.055, 0.92, title, fontsize=22, weight="bold")
    columns = ("CRPS", "CRPS_SKILL", "BRIER_SKILL", "RPS_SKILL", "COVERAGE90", "WIDTH90") \
        if probability else ("BIAS", "MAE", "RMSE", "CORRELATION", "ACC")
    labels = ["상품·변수", "N", "방법", *columns]
    body: list[list[str]] = []
    for product, variable in GROUPS:
        for method in ("RAW", "QM", "QDM", "EMOS"):
            row = next(r for r in rows if (r["PRODUCT"], r["VARIABLE"], r["METHOD"]) ==
                       (product, variable, method))
            body.append([group_name(product, variable), row["N"], method,
                         *(f"{float(row[c]):.3f}" if row[c] else "결측" for c in columns)])
    axes = figure.add_axes((0.04, 0.15, 0.92, 0.68))
    axes.set_axis_off()
    table = axes.table(cellText=body, colLabels=labels, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.95)
    for (row_index, _), cell in table.get_celld().items():
        cell.set_edgecolor("#DDDDDD")
        if row_index == 0:
            cell.set_facecolor("#E8EEF4")
        elif row_index % 2 == 0:
            cell.set_facecolor("#F6F8FA")
    _ = figure.text(0.055, 0.11, "기온: °C / 강수: mm·대상구간 누적. 상관·skill·포함률은 무차원.",
                    fontsize=10)
    _ = figure.text(0.055, 0.075, coverage_note + " 사례 수는 독립 관측 수가 아닙니다.",
                    fontsize=10, color="#7A3A00")
    _ = figure.text(0.95, 0.028, f"{page} / 68", fontsize=9, ha="right")
    return figure


def run(root: Path) -> None:
    """Generate 64 chart pages, four context pages, audited plot points and bookmarks."""
    output = root / "outputs"
    summary = read_summary(output / "run_summary.json")
    validation = read_validation(output / "validation.json")
    audit = read_audit(output / "data_audit.json")
    provenance = audit.get("observation_source", {})
    if provenance != summary.get("observation_source", {}):
        raise RuntimeError("Observation provenance differs between audit and run summary")
    if (summary["status"] != "PASS" or validation["status"] != "PASS"
            or validation["cases_verified"] != summary["cases_verified"]):
        raise RuntimeError("Original verification must pass before PDF reporting")
    source_files = [
        *(f"outputs/metrics_by_{d.name}.csv" for d in DIMENSIONS),
        "outputs/metrics_overall.csv", "outputs/data_audit.json",
        "outputs/run_summary.json", "outputs/validation.json",
        "outputs/matched_predictions.csv.gz",
    ]
    daily_path = str(provenance.get(
        "daily_relative_path",
        "GLOSEA6_KMA_20220301-20260831_v1/data/asos/asos_kma_daily.csv.gz",
    ))
    source_files.append(daily_path)
    if provenance.get("selected"):
        directory = str(provenance["relative_directory"])
        source_files.extend(f"{directory}/{name}" for name in (
            "provenance.json", "coverage_audit.json", "station_daily.csv.gz", "coverage_gaps.csv",
        ))
        if (root / directory / "independent_audit.json").is_file():
            source_files.append(f"{directory}/independent_audit.json")
    if (output / "method_review/qm_qdm_audit.json").is_file():
        source_files.append("outputs/method_review/qm_qdm_audit.json")
    hashes = {name: source_digest(root / name) for name in source_files}
    matplotlib.rcParams.update({
        "font.family": ["Malgun Gothic", "DejaVu Sans"],
        "axes.unicode_minus": False, "pdf.fonttype": 42, "ps.fonttype": 42,
    })
    figures = output / "dimension_figures"
    figures.mkdir(exist_ok=True)
    temporary = output / ".dimension_raw.pdf"
    final = output / PDF_NAME
    pages: list[PageRecord] = []
    points: list[Mapping[str, CsvCell]] = []
    predictions = read_rows(output / "matched_predictions.csv.gz")
    coverage_note = monthly_temperature_note(predictions)
    group_counts = [
        f"{title((g['product'], g['variable']))} "
        + f"{sum(r['METHOD'] == 'RAW' and (r['PRODUCT'], r['VARIABLE']) == (g['product'], g['variable']) for r in predictions):,}"
        for g in audit["groups"]
    ]
    statuses: dict[str, int] = {}
    for group in audit["groups"]:
        for status, count in group["status_counts"].items():
            statuses[status] = statuses.get(status, 0) + count
    status_line = " / ".join(f"{status}: {count:,}" for status, count in sorted(statuses.items()))
    fresh = bool(provenance.get("selected"))
    source_line = (
        f"관측: KMA API Hub / nalssi89/kmahub 정책 / 최신 완결일 {provenance['source_end']}\n"
        + f"수집 완료 UTC: {provenance['retrieved_at_utc']}"
        if fresh else "관측: 원본 제공 권역 일평균 / 수집 시각 기록 없음"
    )
    reference_note = (
        "재수집 OBS 사용; 원본 기간 참조값 차이는 기록하며 일치를 강제하지 않습니다."
        if fresh else "원본: 모든 날 62지점 구간만 참조 일치 강제; 혼합 구간은 정책 차이 기록."
    )
    contributor_ranges = " / ".join(
        f"{label} {min(map(int, counts))}~{max(map(int, counts))}지점"
        for label, counts in (
            ("기온", audit["daily_temperature_station_counts"]),
            ("강수", audit["daily_precipitation_station_counts"]),
        )
    )
    station_note = (
        f"수집 지점·날짜 행 {provenance['station_date_rows']} / 기대 {provenance['expected_station_date_rows']}.\n"
        + "행 존재와 변수별 측정 유효성은 다릅니다. 지점별 수치·누락 코드: REPORT_KO.md."
        if fresh else "개별 지점 행 미제공; 지점별 측정 유효성·기기 QC 확인 불가."
    )
    cover = [
        "리드타임 · 월 · 계절 · 연도별 비교\nRAW(원시모델) / QM / QDM / EMOS",
        source_line + "\n" + f"예보 초기일: {audit['forecast_init_start']} ~ {audit['forecast_init_end']}\n"
        + f"관측 제공 기간: {audit['observation_start']} ~ {audit['observation_end']}",
        f"전체 {audit['total_cases']:,}사례 중 {summary['cases_verified']:,}사례 검증 · 네 방법 동일 사례\n"
        + " / ".join(group_counts[:2]) + "\n" + " / ".join(group_counts[2:])
        + "\n관측 정책 상태: " + status_line,
        "목차: 안내 2쪽 · 전체 요약 3~4쪽\n"
        + "리드타임 5~20쪽 · 월 21~36쪽 · 계절 37~52쪽 · 연도 53~68쪽",
        coverage_note + "\n"
        + reference_note + "\n"
        + "학습 OBS: 일별 기온 평균·강수 합. 최신 완결일 이후 모델 구간은 관측 미확보 제외.",
        qdm_audit_note(root, audit),
    ]
    guidance = [
        "월·계절·연도는 검증 구간 시작일(VALID_START) 기준입니다.\n"
        + "주간 구간이 월 경계를 지나도 날짜별로 분할하지 않습니다. 연도는 초기일 연도가 아닙니다.",
        "W01~W08: 주간 리드 / M01~M06: 개별 달력 월 리드입니다.\n"
        + "3mon 상품명은 3개월 누적이 아닙니다. 계절: DJF / MAM / JJA / SON.",
        "Bias는 예측−관측, 0이 기준입니다. MAE·RMSE·CRPS·Brier·RPS는 낮을수록 좋습니다.\n"
        + "ACC·상관·skill은 높을수록 좋습니다. skill=0은 훈련 관측 기후 분포와 같은 점수입니다.",
        "QM: 경험적 분위수 매핑 / QDM: 예보 앙상블 순위 기반 가산·비율 변형.\n"
        + "순위 교차·건조 분모 대체로 정렬된 분위수·기후 추세 보존을 보장하지 않습니다.",
        "훈련: 같은 사례의 과거 source-year 쌍, HIST_END < INIT_DATE, target year 제외.\n"
        + "재예측 모델의 운영 당시 가용성은 미확인. EMOS: 기온 정규·강수 0 검열, 평균 CRPS 최소화.",
        f"관측소 목록 {audit['declared_stations']}개; 실제 변수별 기여: {contributor_ranges}.\n"
        + ("최소 50지점 동일 가중 평균; QC는 파생 유효성·기여 수 검사, 원래 기기 QC 아님.\n"
           if fresh else "제공 QC=OK·일별 최소 기여 기준 충족; 62지점 완전성 보장 아님.\n")
        + "62/n 재조정·누락 지점 추정 없음. 1991–2020 평년값으로 훈련 삼분위 대체 안 함.\n"
        + station_note,
    ]
    overall = read_rows(output / "metrics_overall.csv")
    front = [
        prose_page("GloSea6 예측 성능 검증 보고서", cover, 1),
        prose_page("자료·방법·그래프 읽는 법", guidance, 2),
        summary_page(overall, False, 3, coverage_note), summary_page(overall, True, 4, coverage_note),
    ]
    with PdfPages(temporary, metadata={"Title": "GloSea6 차원별 검증 보고서",
                                    "Author": "GloSea6 verification workflow"}) as raw_pdf:
        pdf = pdf_sink(raw_pdf)
        for index, figure in enumerate(front, 1):
            pdf.savefig(figure)
            pages.append({
                "page": index, "kind": "frontmatter", "dimension": "", "product": "",
                "variable": "", "family": "", "title": ("표지", "읽는 법", "결정론 요약", "확률 요약")[index - 1],
                "figure": "",
            })
            figure.clear()
        for dimension in DIMENSIONS:
            rows = read_rows(output / f"metrics_by_{dimension.name}.csv")
            for product, variable in GROUPS:
                for family, family_label, metrics in FAMILIES:
                    page = len(pages) + 1
                    figure = chart_page(rows, dimension, product, variable, family, family_label,
                                        metrics, page, points, coverage_note)
                    filename = f"{dimension.name}_{product}_{variable}_{family}.png"
                    path = figures / filename
                    figure.savefig(path, dpi=150)
                    pdf.savefig(figure)
                    pages.append({
                        "page": page, "kind": "chart", "dimension": dimension.name,
                        "product": product, "variable": variable, "family": family,
                        "title": f"{dimension.label}별 {group_name(product, variable)} {family_label}",
                        "figure": path.relative_to(root).as_posix(),
                    })
                    figure.clear()
            print(f"FIGURES_COMPLETE {dimension.name}:16 pages", flush=True)
    if len(pages) != 68:
        raise RuntimeError(f"Unexpected PDF coverage: {len(pages)}")
    reader = PdfReader(temporary)
    writer = PdfWriter()
    writer.append(reader)
    _ = writer.add_outline_item("표지 및 자료 안내", 0)
    _ = writer.add_outline_item("전체 결정론·확률 요약", 2)
    for index, dimension in enumerate(DIMENSIONS):
        parent = writer.add_outline_item(f"{dimension.label}별 검증", 4 + index * 16)
        for group_index, (product, variable) in enumerate(GROUPS):
            _ = writer.add_outline_item(group_name(product, variable), 4 + index * 16 + group_index * 4,
                                        parent=parent)
    writer.add_metadata({"/Title": "GloSea6 차원별 검증 보고서", "/Author": "GloSea6 verification workflow"})
    staged = output / ".dimension_completed.pdf"
    with staged.open("wb") as handle:
        _ = writer.write(handle)
    writer.close()
    try:
        _ = staged.replace(final)
    except PermissionError:
        # An observed Windows viewer lock must not destroy or close the user's copy.
        final = output / "GLOSEA6_verification_by_dimension_KO_final.pdf"
        _ = staged.replace(final)
        print(f"VIEWER_LOCK preserved original; finalized separate copy: {final}", flush=True)
    finalized_alias = output / "GLOSEA6_verification_by_dimension_KO_final.pdf"
    if final != finalized_alias:
        alias_staged = output / ".dimension_final_alias.pdf"
        _ = shutil.copyfile(final, alias_staged)
        try:
            _ = alias_staged.replace(finalized_alias)
        except PermissionError:
            final = output / "GLOSEA6_verification_by_dimension_KO_refreshed.pdf"
            _ = alias_staged.replace(final)
            print(f"VIEWER_LOCK preserved locked final; refreshed report: {final}", flush=True)
    temporary.unlink()
    write_csv(output / "pdf_plot_data.csv", points)
    manifest = {
        "pdf": final.relative_to(root).as_posix(), "total_pages": len(pages),
        "source_hashes": hashes, "pages": pages,
        "generator": "analysis/make_dimension_pdf.py",
        "grouping": "month/season/year = VALID_START; lead = package LEAD",
        "missing_bins": "NaN gaps; not zero-filled or bridged",
        "observation_source": provenance,
    }
    with (output / "pdf_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
    if any(source_digest(root / name) != digest for name, digest in hashes.items()):
        raise RuntimeError("Original source artifacts changed during PDF generation")
    print(f"PDF_COMPLETE pages={len(pages)} plots={len(pages)-4} points={len(points)} path={final}", flush=True)


def main() -> None:
    """Actual PDF generation CLI; no arbitrary arguments or placeholder dry-run."""
    if sys.argv[1:] == ["--help"]:
        print("Usage: python analysis/make_dimension_pdf.py\n" +
              "Render all verified dimension/method metrics into a Korean 68-page PDF and PNGs.")
        return
    if sys.argv[1:]:
        raise SystemExit("Unexpected arguments; use --help")
    run(Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    main()
