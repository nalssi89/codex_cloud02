"""Year-block weighted QRF and mean-ordered isotonic distributions."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
from time import perf_counter

import numpy as np
from numpy.typing import NDArray

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FeatureSpec,
    FitConfig,
    FitDiagnostics,
    FittedModel,
    PredictiveDistribution,
    TrainingSet,
)
from analysis.calibration import FloatArray
from analysis.data_io import Json


@dataclass(frozen=True, slots=True, kw_only=True)
class Tree:
    feature: int = -1
    threshold: float = 0.0
    left: Tree | None = None
    right: Tree | None = None
    indices: tuple[int, ...] = ()
    masses: tuple[float, ...] = ()
    bootstrap_year_counts: tuple[tuple[int, int], ...] = ()

    def leaf(self, x: FloatArray) -> Tree:
        if self.feature < 0:
            return self
        child = self.left if x[self.feature] <= self.threshold else self.right
        assert child is not None
        return child.leaf(x)

    def to_spec(self) -> dict[str, Json]:
        if self.feature < 0:
            result: dict[str, Json] = {"indices": list(self.indices), "masses": list(self.masses)}
        else:
            assert self.left is not None and self.right is not None
            result = {"feature": self.feature, "threshold": self.threshold,
                      "left": self.left.to_spec(), "right": self.right.to_spec()}
        if self.bootstrap_year_counts:
            result["bootstrap_year_counts"] = [[year, count] for year, count in self.bootstrap_year_counts]
        return result


def fit_tree(x: FloatArray, y: FloatArray, years: NDArray[np.int64], weights: FloatArray,
          indices: NDArray[np.int64], rng: np.random.Generator, depth: int = 0) -> Tree:
    w = weights[indices]
    total = w.sum()
    best_loss, best_feature, best_threshold, best_left = np.inf, -1, 0.0, None
    if depth < 4 and len(np.unique(years[indices])) >= 5:
        for feature in sorted(int(f) for f in rng.choice(np.size(x, axis=1), size=3, replace=False).flat):
            column = x.take([feature], axis=1).ravel()
            order = indices[np.argsort(column[indices], kind="stable")]
            z, v, a = column[order], y[order], weights[order]
            _, first = np.unique(years[order], return_index=True)
            _, reversed_first = np.unique(years[order][::-1], return_index=True)
            last = len(order) - 1 - reversed_first
            left_years = np.cumsum(np.bincount(first, minlength=len(order)))
            right_years = np.cumsum(np.bincount(last, minlength=len(order))[::-1])[::-1]
            cw, cy, cy2 = np.cumsum(a), np.cumsum(a * v), np.cumsum(a * v * v)
            candidates = np.flatnonzero((z[:-1] < z[1:]) &
                                       (left_years[:-1] >= 5) & (right_years[1:] >= 5))
            if not len(candidates):
                continue
            j = candidates
            loss = (cy2[j] - cy[j] ** 2 / cw[j] + cy2.item(-1) - cy2[j]
                    - (cy.item(-1) - cy[j]) ** 2 / (cw.item(-1) - cw[j]))
            k = j.item(int(np.argmin(loss)))
            if loss.min() < best_loss:
                best_loss, best_feature, best_threshold = float(loss.min()), feature, z.item(k)
                best_left = column[indices] <= best_threshold
    parent_loss = float(np.sum(w * y[indices] ** 2) - np.sum(w * y[indices]) ** 2 / total)
    if best_left is None or best_loss >= parent_loss:
        return Tree(indices=tuple(int(i) for i in indices.flat),
                    masses=tuple(float(a) for a in (w / total).flat))
    return Tree(feature=best_feature, threshold=best_threshold,
                left=fit_tree(x, y, years, weights, indices[best_left], rng, depth + 1),
                right=fit_tree(x, y, years, weights, indices[~best_left], rng, depth + 1))


def antitonic(values: FloatArray, weights: FloatArray) -> FloatArray:
    """Weighted decreasing PAVA; equal predictor groups are already merged."""
    levels: list[float] = []
    masses: list[float] = []
    sizes: list[int] = []
    for value, weight in zip(values.flat, weights.flat, strict=True):
        levels.append(float(value))
        masses.append(float(weight))
        sizes.append(1)
        while len(levels) > 1 and levels[-2] < levels[-1]:
            mass = masses[-2] + masses[-1]
            level = (levels[-2] * masses[-2] + levels[-1] * masses[-1]) / mass
            size = sizes[-2] + sizes[-1]
            levels[-2:], masses[-2:], sizes[-2:] = [level], [mass], [size]
    return np.repeat(levels, sizes).astype(np.float64)


def _quarter(start: date, end: date) -> int:
    return ((start + (end - start) / 2).month - 1) // 3


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderModel:
    method_id: str
    observations: FloatArray
    row_ids: tuple[str, ...]
    source_years: tuple[int, ...]
    train_hash: str
    scope: str
    lead: str
    quarter: int
    product: str
    variable: str
    feature_spec: FeatureSpec | None = None
    trees: tuple[Tree, ...] = ()
    predictor_levels: FloatArray | None = None
    cdf_levels: FloatArray | None = None

    def predict(self, target: CaseInput) -> PredictiveDistribution:
        from analysis.alternative_distributions import weighted_empirical

        if target.product != self.product or target.variable != self.variable:
            raise AlternativeError("INPUT_CONFLICT", "order model product/variable mismatch")
        if self.method_id == "qrf_year_forest":
            from analysis.alternative_data import features_for_case

            assert self.feature_spec is not None
            x = features_for_case(target, self.feature_spec)
            weights = np.zeros(len(self.observations), dtype=np.float64)
            for tree in self.trees:
                leaf = tree.leaf(x)
                weights[list(leaf.indices)] += np.asarray(leaf.masses) / 64
            keep = weights > 0
            return weighted_empirical(self.observations[keep], weights[keep])
        if target.lead != self.lead or _quarter(target.valid_start, target.valid_end) != self.quarter:
            raise AlternativeError("INPUT_CONFLICT", "IDR prediction outside fitted lead/quarter")
        assert self.predictor_levels is not None and self.cdf_levels is not None
        mean = float(np.mean(target.members))
        j = int(np.searchsorted(self.predictor_levels, mean))
        if j == 0:
            cdf = self.cdf_levels.take([0], axis=0).ravel()
        elif j == len(self.predictor_levels):
            cdf = self.cdf_levels.take([-1], axis=0).ravel()
        else:
            fraction = ((mean - self.predictor_levels.item(j - 1)) /
                        (self.predictor_levels.item(j) - self.predictor_levels.item(j - 1)))
            cdf = ((1 - fraction) * self.cdf_levels.take([j - 1], axis=0).ravel()
                   + fraction * self.cdf_levels.take([j], axis=0).ravel())
        masses = np.diff(np.concatenate((np.array([0.0], dtype=np.float64), cdf), dtype=np.float64))
        if np.maximum(-masses, 0).sum() + abs(masses.sum() - 1) > 1e-12:
            raise AlternativeError("NUMERICAL_DISTRIBUTION_FAILED", "IDR nonnested CDF")
        masses = masses.clip(0, None)
        keep = masses > 0
        return weighted_empirical(self.observations[keep],
                                  masses.take(np.flatnonzero(keep)) / np.sum(masses, dtype=np.float64))

    def to_spec(self) -> dict[str, Json]:
        result: dict[str, Json] = {
            "type": self.method_id, "observations": self.observations.tolist(),
            "row_ids": list(self.row_ids), "source_years": list(self.source_years),
            "train_hash": self.train_hash, "scope": self.scope, "lead": self.lead,
            "quarter": self.quarter, "quarter_definition": "valid_window_midpoint",
            "product": self.product, "variable": self.variable, "bounded_tails": True,
        }
        if self.trees:
            assert self.feature_spec is not None
            result.update({"trees": [tree.to_spec() for tree in self.trees],
                           "n_trees": 64, "max_depth": 4, "min_child_years": 5,
                           "split_features": 3, "bootstrap_unit": "source_year",
                           "features": {"names": list(self.feature_spec.names),
                                        "center": self.feature_spec.center.tolist(),
                                        "scale": self.feature_spec.scale.tolist(),
                                        "predictor_power": self.feature_spec.predictor_power}})
        else:
            assert self.predictor_levels is not None and self.cdf_levels is not None
            result.update({"order": "ensemble_mean_only_stochastically_increasing",
                           "predictor_levels": self.predictor_levels.tolist(),
                           "cdf_levels": self.cdf_levels.tolist()})
        return result


def fit_order(method_id: str, training: TrainingSet,
              config: FitConfig) -> tuple[FittedModel, FitDiagnostics]:
    start = perf_counter()
    if method_id not in ("qrf_year_forest", "idr_mean_order"):
        raise AlternativeError("INPUT_CONFLICT", f"unknown order method {method_id}")
    rows = training.rows
    for row in rows:
        if (row.hist_end >= training.cutoff or row.source_case_init > training.catalog_cutoff
                or row.source_year in training.held_out_years
                or any(row.hist_start.year <= y <= row.hist_end.year for y in training.held_out_years)
                or (row.product, row.variable) != (training.target.product, training.target.variable)):
            raise AlternativeError("INPUT_CONFLICT", f"invalid order training ancestor {row.row_id}")
    scope = "pooled"
    quarter = _quarter(training.target.valid_start, training.target.valid_end)
    mask = np.ones(len(rows), dtype=bool)
    if method_id == "idr_mean_order":
        mask = np.asarray([r.lead == training.target.lead and
                           _quarter(r.hist_start, r.hist_end) == quarter for r in rows])
        if len({r.source_year for r, keep in zip(rows, mask, strict=True) if keep}) < 10:
            mask = np.asarray([r.source_case_id == training.target.case_id and
                               r.lead == training.target.lead for r in rows])
            scope = "local_fallback"
    selected = tuple(r for r, keep in zip(rows, mask, strict=True) if keep)
    years = np.asarray([r.source_year for r in selected], dtype=np.int64)
    if len(np.unique(years)) < 10:
        raise AlternativeError("INSUFFICIENT_TRAINING", f"{scope} order fit requires 10 source years")
    y = np.asarray([r.observation for r in selected], dtype=np.float64)
    # Rebalance after stratum selection; each surviving source year has unit mass.
    _, year_inverse, year_counts = np.unique(years, return_inverse=True, return_counts=True)
    weights = 1.0 / year_counts[year_inverse]
    model = OrderModel(method_id=method_id, observations=y,
                       row_ids=tuple(r.row_id for r in selected),
                       source_years=tuple(int(year) for year in years.flat), train_hash=training.train_hash,
                       scope=scope, lead=training.target.lead, quarter=quarter,
                       product=training.target.product, variable=training.target.variable)
    if method_id == "qrf_year_forest":
        from analysis.alternative_data import features_for_training

        x, feature_spec = features_for_training(training)
        rng, unique_years = np.random.default_rng(config.seed), np.unique(years)
        trees: list[Tree] = []
        for _ in range(64):
            drawn = rng.choice(len(unique_years), size=len(unique_years), replace=True)
            counts = np.bincount(drawn, minlength=len(unique_years))
            multiplicity = counts[year_inverse]
            boot_weights = weights * multiplicity
            tree = fit_tree(x, y, years, boot_weights, np.flatnonzero(boot_weights > 0), rng)
            trees.append(replace(tree, bootstrap_year_counts=tuple(
                (int(year), int(count)) for year, count in zip(unique_years.flat, counts.flat, strict=True))))
        model = replace(model, feature_spec=feature_spec, trees=tuple(trees))
    else:
        means = np.asarray([np.mean(r.ensemble) for r in selected])
        levels, inverse = np.unique(means, return_inverse=True)
        support = np.unique(y)
        group_weights = np.bincount(inverse, weights=weights)
        cdfs = np.column_stack([antitonic(
            np.bincount(inverse, weights=weights * (y <= value)) / group_weights,
            group_weights) for value in support.flat])
        if np.min(np.diff(cdfs, axis=1), initial=0) < -1e-12:
            raise AlternativeError("NUMERICAL_DISTRIBUTION_FAILED", "IDR threshold nesting failed")
        model = replace(model, observations=support, predictor_levels=levels, cdf_levels=cdfs)
    diagnostics = FitDiagnostics(convergence=True, n_rows=len(selected), n_years=len(np.unique(years)),
                                 train_hash=training.train_hash, elapsed_seconds=perf_counter() - start,
                                 boundary_flags=("bounded_empirical_tails", scope),
                                 message="year-balanced; mean stochastic order" if not model.trees
                                 else "64 year-block bootstrap trees; multiplicity-weighted empirical leaves")
    return model, diagnostics
