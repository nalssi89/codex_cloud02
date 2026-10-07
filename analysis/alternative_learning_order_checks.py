"""Executable deterministic mathematical and ancestor checks for order models."""

from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import date

import numpy as np
from scipy.optimize import LinearConstraint, minimize

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FitConfig,
    TrainingRow,
    TrainingSet,
)
from analysis.alternative_learning_order import (
    OrderModel,
    Tree,
    antitonic,
    fit_order,
    fit_tree,
)


def fixture() -> TrainingSet:
    target = CaseInput(
        case_id="case", init=date(2026, 1, 1), valid_start=date(2026, 2, 1),
        valid_end=date(2026, 2, 7), product="1mon", lead="W1", variable="t15m",
        members=np.array([4., 6.]), member_keys=("a", "b"), provenance_hash="fixture",
    )
    rows = tuple(
        TrainingRow(
            row_id=f"{year}-{condition}", source_case_id="case",
            source_case_init=target.init, source_year=year, source_init=date(year, 1, 1),
            hist_start=date(year, 2, 1), hist_end=date(year, 2, 7),
            product="1mon", lead="W1", variable="t15m",
            ensemble=np.array([float(year - 1990), float(year - 1988)]),
            observation=float((year - 1990) // 3 + condition),
            member_keys=("a", "b"), provenance_hash="fixture", archive_era="",
        )
        for year in range(1990, 2010) for condition in range(1 + year % 2)
    )
    weights = np.array([1 / (1 + row.source_year % 2) for row in rows])
    return TrainingSet(
        target=target, rows=rows, year_weights=weights, cutoff=target.init,
        catalog_cutoff=target.init, held_out_years=(2026,), train_hash="fixture",
        local_observations=np.array([r.observation for r in rows]),
        thresholds=np.array([2., 4.]),
    )


class OrderChecks(unittest.TestCase):
    def test_pava_independent_quadratic_oracle(self) -> None:
        response, weights = np.array([0., 1., 0., 1.]), np.array([1., 3., 2., 1.])
        actual = antitonic(response, weights)
        oracle = minimize(
            lambda z: float(np.sum(weights * (z - response) ** 2)),
            np.full(4, .5), jac=lambda z: 2 * weights * (z - response),
            constraints=LinearConstraint(np.eye(4)[:-1] - np.eye(4)[1:], 0, np.inf),
            method="SLSQP", options={"ftol": 1e-12},
        )
        self.assertTrue(oracle.success)
        np.testing.assert_allclose(actual, oracle.x, atol=1e-7)

    def test_bootstrap_multiplicity_leaf_mass(self) -> None:
        years = np.repeat(np.arange(10), [1, 2] * 5)
        counts = np.bincount(years)
        drawn = np.array([0, 0, 0, 2, 2, 4, 5, 6, 7, 9])
        w = np.bincount(drawn, minlength=10)[years] / counts[years]
        tree = fit_tree(np.zeros((len(years), 8)), np.ones(len(years)), years, w,
                     np.flatnonzero(w > 0), np.random.default_rng(2))
        self.assertEqual(tree.feature, -1)
        np.testing.assert_allclose(tree.masses, w[w > 0] / 10)

    def test_child_year_support_can_overlap(self) -> None:
        years = np.repeat(np.arange(5, dtype=np.int64), 2)
        y = np.tile(np.array([0., 1.]), 5)
        x = np.repeat(y[:, None], 8, axis=1)
        tree = fit_tree(x, y, years, np.full(10, .5), np.arange(10, dtype=np.int64),
                     np.random.default_rng(4))
        self.assertGreaterEqual(tree.feature, 0)
        assert tree.left is not None and tree.right is not None
        self.assertEqual(len(np.unique(years[list(tree.left.indices)])), 5)
        self.assertEqual(len(np.unique(years[list(tree.right.indices)])), 5)

    def test_empirical_leaf_not_point_prediction(self) -> None:
        from analysis.alternative_distributions import weighted_empirical

        years = np.repeat(np.arange(10, dtype=np.int64), 2)
        counts = np.array([3, 0, 0, 2, 1, 0, 1, 1, 1, 1])
        weights = counts[years] / 2
        observations = np.tile(np.array([0., 10.]), 10)
        tree = fit_tree(np.zeros((20, 8)), observations, years, weights,
                     np.flatnonzero(weights > 0), np.random.default_rng(42))
        law = weighted_empirical(observations[list(tree.indices)], np.array(tree.masses))
        self.assertAlmostEqual(law.atom_mass(0.), .5)
        self.assertAlmostEqual(law.cdf(np.array([0.])).item(0), .5)
        self.assertAlmostEqual(law.quantile(np.array([.75])).item(0), 10)
        self.assertAlmostEqual(law.crps(0.), 2.5)
        self.assertNotEqual(law.crps(0.), abs(law.mean()))

    def test_forest_ancestry_support_and_reproducibility(self) -> None:
        training, config = fixture(), FitConfig(seed=42)
        model, diagnostics = fit_order("qrf_year_forest", training, config)
        assert isinstance(model, OrderModel)
        repeated, _ = fit_order("qrf_year_forest", training, config)
        self.assertEqual(model.to_spec(), repeated.to_spec())
        self.assertEqual(len(model.trees), 64)
        self.assertEqual(diagnostics.n_years, 20)
        years = np.array(sorted(set(model.source_years)), dtype=np.int64)
        drawn = np.asarray(np.random.default_rng(config.seed).choice(years, len(years), replace=True),
                           dtype=np.int64)
        expected_counts = {int(year): int(np.count_nonzero(np.equal(drawn, year))) for year in years.flat}
        self.assertEqual(dict(model.trees[0].bootstrap_year_counts), expected_counts)
        self.assertTrue(any(count > 1 for count in expected_counts.values()))
        self.assertTrue(any(count == 0 for count in expected_counts.values()))
        def visit(node: Tree, bootstrap_counts: dict[int, int], depth: int = 0) -> set[int]:
            self.assertLessEqual(depth, 4)
            if node.feature < 0:
                self.assertAlmostEqual(sum(node.masses), 1)
                weights = np.array([bootstrap_counts[model.source_years[i]] /
                                    model.source_years.count(model.source_years[i])
                                    for i in node.indices], dtype=np.float64)
                np.testing.assert_allclose(node.masses, weights / weights.sum(), atol=1e-15)
                if depth:
                    self.assertGreaterEqual(len({model.source_years[i] for i in node.indices}), 5)
                return set(node.indices)
            else:
                assert node.left is not None and node.right is not None
                return (visit(node.left, bootstrap_counts, depth + 1) |
                        visit(node.right, bootstrap_counts, depth + 1))
        for tree in model.trees:
            bootstrap_counts = dict(tree.bootstrap_year_counts)
            self.assertEqual(sum(bootstrap_counts.values()), diagnostics.n_years)
            included = visit(tree, bootstrap_counts)
            for year in set(model.source_years):
                block = {i for i, value in enumerate(model.source_years) if value == year}
                self.assertEqual(block <= included, bootstrap_counts[year] > 0)
                self.assertEqual(not block & included, bootstrap_counts[year] == 0)
        law = model.predict(training.target)
        from analysis.alternative_data import features_for_case
        assert model.feature_spec is not None
        x = features_for_case(training.target, model.feature_spec)
        expected_weights = np.zeros(len(training.rows))
        for tree in model.trees:
            leaf = tree.leaf(x)
            expected_weights[list(leaf.indices)] += np.array(leaf.masses) / 64
        values = model.observations
        expected_cdf = np.array([expected_weights[values <= y].sum() for y in np.unique(values).flat],
                                dtype=np.float64)
        np.testing.assert_allclose(law.cdf(np.unique(values)), expected_cdf, atol=1e-15)
        expected_crps = float(expected_weights @ np.abs(values - 3.) -
                              .5 * expected_weights @ np.abs(values[:, None] - values) @ expected_weights)
        self.assertAlmostEqual(law.crps(3.), expected_crps)
        self.assertAlmostEqual(law.cdf(np.array([np.inf])).item(0), 1)
        self.assertGreaterEqual(law.mean(), min(r.observation for r in training.rows))
        self.assertLessEqual(law.mean(), max(r.observation for r in training.rows))
        self.assertTrue(np.isfinite(law.crps(3.)))

    def test_ancestor_gates_before_feature_fit(self) -> None:
        training, config = fixture(), FitConfig(seed=42)
        bad = replace(training, held_out_years=(1995,))
        with self.assertRaisesRegex(AlternativeError, "ancestor"):
            _ = fit_order("qrf_year_forest", bad, config)
        late = replace(training.rows[0], hist_end=training.cutoff)
        with self.assertRaisesRegex(AlternativeError, "ancestor"):
            _ = fit_order("qrf_year_forest", replace(training, rows=(late,) + training.rows[1:]), config)
        future = replace(training.rows[0], source_case_init=date(2026, 1, 2))
        with self.assertRaisesRegex(AlternativeError, "ancestor"):
            _ = fit_order("qrf_year_forest", replace(training, rows=(future,) + training.rows[1:]), config)
        crossing = replace(training.rows[0], source_year=1989)
        with self.assertRaisesRegex(AlternativeError, "ancestor"):
            _ = fit_order("qrf_year_forest", replace(training, held_out_years=(1990,),
                                               rows=(crossing,) + training.rows[1:]), config)

    def test_idr_ties_nesting_interpolation_and_fallback(self) -> None:
        training = fixture()
        model, _ = fit_order("idr_mean_order", training, FitConfig())
        assert isinstance(model, OrderModel)
        assert model.cdf_levels is not None and model.predictor_levels is not None
        self.assertTrue(np.all(np.diff(model.cdf_levels, axis=0) <= 1e-12))
        self.assertTrue(np.all(np.diff(model.cdf_levels, axis=1) >= -1e-12))
        self.assertEqual(len(model.predictor_levels), 20)
        x = (model.predictor_levels.item(5) + model.predictor_levels.item(6)) / 2
        target = replace(training.target, members=np.array([x]))
        actual = model.predict(target).cdf(model.observations)
        np.testing.assert_allclose(actual, (model.cdf_levels.take([5], axis=0).ravel() +
                                            model.cdf_levels.take([6], axis=0).ravel()) / 2)
        tied = replace(training, rows=tuple(replace(row, ensemble=np.array([1.]))
                                            for row in training.rows))
        tied_model, _ = fit_order("idr_mean_order", tied, FitConfig())
        assert isinstance(tied_model, OrderModel) and tied_model.predictor_levels is not None
        self.assertEqual(len(tied_model.predictor_levels), 1)
        expected = np.array([np.sum(training.year_weights * (tied.local_observations <= y)) /
                             np.sum(training.year_weights) for y in tied_model.observations.flat],
                            dtype=np.float64)
        np.testing.assert_allclose(tied_model.predict(target).cdf(tied_model.observations), expected)
        other_quarter = replace(training, rows=tuple(
            replace(row, hist_start=date(row.source_year, 8, 1),
                    hist_end=date(row.source_year, 8, 7)) for row in training.rows))
        fallback, diagnostics = fit_order("idr_mean_order", other_quarter, FitConfig())
        assert isinstance(fallback, OrderModel)
        self.assertEqual(fallback.scope, "local_fallback")
        self.assertIn("local_fallback", diagnostics.boundary_flags)
        _ = fallback.predict(training.target)


if __name__ == "__main__":
    _ = unittest.main()
