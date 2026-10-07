"""Actual matplotlib Agg figures, separated by native unit and product."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Protocol

import matplotlib
from matplotlib.figure import Figure

matplotlib.use("Agg")

from analysis.alternative_reporting_common import Row, method, number, scope, text
from analysis.alternative_reporting_statistics import SEED


class AxesSurface(Protocol):
    def bar(self, x: Sequence[int], height: Sequence[float], *,
            bottom: Sequence[float] | None = None, label: str = "") -> object: ...
    def set_xticks(self, ticks: Sequence[int], labels: Sequence[str], *,
                   rotation: int, ha: str, fontsize: int) -> object: ...
    def set_ylabel(self, ylabel: str) -> object: ...
    def set_title(self, label: str) -> object: ...
    def legend(self) -> object: ...


class FigureSurface(Protocol):
    def add_subplot(self, nrows: int, ncols: int, index: int) -> AxesSurface: ...
    def text(self, x: float, y: float, s: str, *, fontsize: int) -> object: ...
    def tight_layout(self, *, rect: tuple[float, float, float, float] = (0, 0, 1, 1)) -> None: ...
    def savefig(self, fname: Path, *, dpi: int, metadata: Mapping[str, str]) -> None: ...
    def clear(self) -> None: ...


def figure_surface(figure: FigureSurface) -> FigureSurface:
    return figure


def score_label(row: Row) -> str:
    return f"{method(row)}\nN={text(row, 'scored_N')}"


def plots(output: Path, counts: list[Row], metrics: list[Row],
          run_scope: str) -> list[str]:
    files: list[str] = []
    groups: dict[tuple[str, str, str], list[Row]] = defaultdict(list)
    for row in metrics:
        if text(row, "group") == "overall" and number(row, "mean_loss") is not None:
            groups[(*scope(row), text(row, "score"))].append(row)
    for (product, variable, score), records in sorted(groups.items()):
        records.sort(key=method)
        fig = figure_surface(Figure(figsize=(max(8, len(records)*.24), 5)))
        ax = fig.add_subplot(1, 1, 1)
        _ = ax.bar(list(range(len(records))), [number(row, "mean_loss") or 0 for row in records])
        _ = ax.set_xticks(list(range(len(records))), [score_label(row) for row in records],
                      rotation=75, ha="right", fontsize=8)
        unit = "degC" if variable == "t15m" and score == "CRPS" else (
            "mm" if variable == "prcp" and score == "CRPS" else "score")
        _ = ax.set_ylabel(f"{score} ({unit}); success-only")
        _ = ax.set_title(f"{run_scope} | {product} | {variable} | seed={SEED}")
        _ = fig.text(.02, .01, "Coverage first; different restricted N are not a skill ranking.",
                 fontsize=9)
        fig.tight_layout(rect=(0, .04, 1, 1))
        token = hashlib.sha256(variable.encode()).hexdigest()[:10]
        name = f"score_{product}_{token}_{score}.png"
        fig.savefig(output / name, dpi=150, metadata={"Software": "alternative_reporting"})
        fig.clear()
        files.append(name)
    by_scope: dict[tuple[str, str], list[Row]] = defaultdict(list)
    for row in counts:
        by_scope[scope(row)].append(row)
    for (product, variable), records in sorted(by_scope.items()):
        records.sort(key=method)
        fig = figure_surface(Figure(figsize=(max(8, len(records)*.24), 5)))
        ax = fig.add_subplot(1, 1, 1)
        ok = [number(row, "scored_count") or 0 for row in records]
        failed = [(number(row, "eligible_count") or 0)-success
                  for row, success in zip(records, ok, strict=True)]
        _ = ax.bar(list(range(len(records))), ok, label="Scored")
        _ = ax.bar(list(range(len(records))), failed, bottom=ok, label="Eligible unscored")
        _ = ax.set_xticks(list(range(len(records))), [
            f"{method(row)}\nN={text(row, 'scored_count')}/{text(row, 'eligible_count')}"
            for row in records],
                      rotation=75, ha="right", fontsize=8)
        _ = ax.set_title(f"{run_scope} | {product} | {variable} | seed={SEED}")
        _ = ax.set_ylabel("Actual target counts (gates excluded)")
        _ = ax.legend()
        fig.tight_layout()
        token = hashlib.sha256(variable.encode()).hexdigest()[:10]
        name = f"coverage_{product}_{token}.png"
        fig.savefig(output / name, dpi=150, metadata={"Software": "alternative_reporting"})
        fig.clear()
        files.append(name)
    return files
