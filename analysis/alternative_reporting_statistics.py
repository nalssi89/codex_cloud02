"""Unit-separated summaries and descriptive paired temporal sensitivities."""

from __future__ import annotations

import hashlib
import math
from collections import defaultdict
from collections.abc import Sequence
from datetime import date
from itertools import combinations

import numpy as np

from analysis.alternative_reporting_common import (
    Row,
    decode,
    identity,
    mask_hash,
    mean,
    method,
    number,
    scope,
    text,
    window,
)

SEED = 20261007


def enrich(records: Sequence[Row]) -> list[Row]:
    result: list[Row] = []
    for record in records:
        row = dict(record)
        for upper, lower in (("CASE_ID", "case_id"), ("METHOD", "method_id"),
                             ("PRODUCT", "product"), ("VARIABLE", "variable")):
            if not row.get(upper) and row.get(lower):
                row[upper] = row[lower]
        start = text(row, "VALID_START")
        if start:
            compact = start.replace("-", "")
            year, month = int(compact[:4]), int(compact[4:6])
            _ = row.setdefault("YEAR", year)
            _ = row.setdefault("VALID_MONTH", month)
            _ = row.setdefault("SEASON", ("DJF", "MAM", "JJA", "SON")[(month % 12)//3])
        result.append(row)
    return result


def summaries(records: Sequence[Row], scores: tuple[str, ...],
              surface: str) -> tuple[list[Row], list[Row]]:
    ordinary: list[Row] = []
    weighted: list[Row] = []
    for label, dimensions in (("overall", ()), ("lead", ("LEAD",)),
                              ("month", ("VALID_MONTH",)), ("season", ("SEASON",)),
                              ("year", ("YEAR",))):
        groups: dict[tuple[str, ...], list[Row]] = defaultdict(list)
        for row in records:
            if dimensions and any(not text(row, key) for key in dimensions):
                continue
            groups[(*scope(row), method(row), *(text(row, d) for d in dimensions))].append(row)
        for key, cases in sorted(groups.items()):
            base: Row = {"PRODUCT": key[0], "VARIABLE": key[1], "method_id": key[2],
                         "surface": surface, "group": label, "N": len(cases),
                         **dict(zip(dimensions, key[3:], strict=True))}
            for score in scores:
                losses = [number(row, score) for row in cases]
                present = [v for v in losses if v is not None]
                ordinary.append({**base, "score": score, "scored_N": len(present),
                                 "mean_loss": mean(present), "restriction": "success_only"})
                windows: dict[str, list[float]] = defaultdict(list)
                for row, value in zip(cases, losses, strict=True):
                    if value is not None:
                        windows[window(row)].append(value)
                window_means = [value for values in windows.values()
                                if (value := mean(values)) is not None]
                weighted.append({**base, "score": score, "unique_windows": len(windows),
                                 "mean_loss": mean(window_means),
                                 "weight_rule": "each exact window total 1, split over issuances"})
    return ordinary, weighted


def _day(value: str) -> date:
    value = value.replace("-", "")
    return date(int(value[:4]), int(value[4:6]), int(value[6:8]))


def sensitivity(records: Sequence[Row], scores: tuple[str, ...], surface: str) -> list[Row]:
    """Fixed-seed year and connected-overlap blocks; intervals are descriptive."""
    groups: dict[tuple[str, str], dict[str, dict[str, Row]]] = defaultdict(dict)
    for row in records:
        groups[scope(row)].setdefault(method(row), {})[identity(row)] = row
    result: list[Row] = []
    for (product, variable), methods in sorted(groups.items()):
        for left, right in combinations(sorted(methods), 2):
            ids = sorted(set(methods[left]) & set(methods[right]))
            for score in scores:
                data: list[tuple[str, str, str, float]] = []
                for case_id in ids:
                    a, b = methods[left][case_id], methods[right][case_id]
                    av, bv = number(a, score), number(b, score)
                    if av is not None and bv is not None:
                        data.append((text(a, "YEAR"), window(a), case_id, av-bv))
                if not data:
                    continue
                by_year: dict[str, list[float]] = defaultdict(list)
                by_window: dict[str, list[float]] = defaultdict(list)
                for year, exact_window, _, delta in data:
                    by_year[year].append(delta)
                    by_window[exact_window].append(delta)
                base: Row = {"PRODUCT": product, "VARIABLE": variable, "surface": surface,
                             "left": left, "right": right, "score": score, "N": len(data),
                             "mask_hash": mask_hash(i for _, _, i, _ in data),
                             "years": len(by_year), "seed": SEED,
                             "warning": "descriptive; few actual years; no significance claim"}
                for year, values in sorted(by_year.items()):
                    result.append({**base, "kind": "year_influence", "block": year,
                                   "delta": mean(values), "block_N": len(values)})
                    retained = [d for y, _, _, d in data if y != year]
                    result.append({**base, "kind": "leave_one_year_out", "block": year,
                                   "delta": mean(retained), "block_N": len(retained)})
                window_values = [value for ds in by_window.values()
                                 if (value := mean(ds)) is not None]
                result.append({**base, "kind": "equal_valid_window", "delta": mean(window_values),
                               "block_N": len(window_values)})
                # Exact windows are indivisible. Overlapping windows form connected blocks.
                blocks: list[list[float]] = []
                intervals: list[tuple[date, date, list[float]]] = []
                for exact, values in by_window.items():
                    if exact.startswith("["):
                        decoded = decode(exact)
                        if not isinstance(decoded, list):
                            raise TypeError("component_windows must be JSON array")
                        pairs = [pair for pair in decoded if isinstance(pair, list) and len(pair) == 2]
                        starts = [_day(str(pair[0])) for pair in pairs]
                        ends = [_day(str(pair[1])) for pair in pairs]
                        if not starts:
                            raise ValueError("No joint component windows")
                        start, end = min(starts), max(ends)
                    else:
                        first, last = exact.split("/")
                        start, end = _day(first), _day(last)
                    intervals.append((start, end, values))
                current_end: date | None = None
                for start, end, values in sorted(intervals):
                    if current_end is None or start > current_end:
                        blocks.append([])
                        current_end = end
                    else:
                        current_end = max(current_end, end)
                    blocks[-1].extend(values)
                for kind, clusters in (("year_block", list(by_year.values())),
                                       ("overlap_block", blocks)):
                    digest = hashlib.sha256(f"{SEED}/{product}/{variable}/{left}/{right}/{score}/{kind}".encode())
                    rng = np.random.default_rng(int.from_bytes(digest.digest()[:8], "big"))
                    totals = np.asarray([math.fsum(cluster) for cluster in clusters], dtype=np.float64)
                    sizes = np.asarray([len(cluster) for cluster in clusters], dtype=np.float64)
                    indices = rng.integers(0, len(clusters), (999, len(clusters)))
                    draws = np.sum(totals[indices], axis=1)/np.sum(sizes[indices], axis=1)
                    quantiles = np.quantile(draws, [.025, .975])
                    result.append({**base, "kind": kind, "delta": mean([d for _, _, _, d in data]),
                                   "block_N": len(clusters), "draws": 999,
                                   "descriptive_p025": float(quantiles.item(0)),
                                   "descriptive_p975": float(quantiles.item(1))})
    return result
