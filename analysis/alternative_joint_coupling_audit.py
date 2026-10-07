"""Executable adversarial coupling, atom-PIT, ancestry and MBC replay oracles."""

from __future__ import annotations

from dataclasses import replace
from types import MappingProxyType

import numpy as np
from scipy.special import ndtr

from analysis.alternative_contracts import AlternativeError, FitConfig, TrainingSet
from analysis.alternative_distributions import normal, weighted_empirical
from analysis.alternative_joint_audit_data import fixture
from analysis.alternative_joint_coordinates import correlation, forward, inverse
from analysis.alternative_joint_coupling import (
    dual_ecc,
    gaussian_copula,
    physical_template,
    rank_couple,
)
from analysis.alternative_joint_folds import prequential_folds, validate_residuals
from analysis.alternative_joint_marginals import EmosMarginal
from analysis.alternative_joint_mbc import (
    AffineStep,
    empirical_step,
    fit_map,
    map_from_spec,
)
from analysis.alternative_joint_residuals import PITResidualSet, generate_residuals
from analysis.calibration import FloatArray
from analysis.data_io import Json


def run() -> dict[str, Json]:
    """Independent mathematical identities fail if ranks, maps or ancestry are wrong."""
    config = FitConfig()
    training = fixture()
    laws = (normal(10, 2), normal(-0.3, 1.2, censor_zero=True))
    template = training.observations
    years = tuple(str(y) for y in training.source_years)
    coupled = rank_couple(template, laws, years, config.seed)
    n = len(years)
    grid = (np.arange(n) + 0.5) / n
    for j, law in enumerate(laws):
        assert np.array_equal(np.sort(coupled[:, j]), law.quantile(grid))
        finite = weighted_empirical(coupled[:, j], np.full(n, 1.0 / n))
        reference = weighted_empirical(law.quantile(grid), np.full(n, 1.0 / n))
        assert abs(finite.crps(0.7) - reference.crps(0.7)) < 1e-14
    rain_finite = weighted_empirical(coupled[:, -1], np.full(n, 1.0 / n))
    assert abs(rain_finite.crps(0.7) - laws[-1].crps(0.7)) > 1e-12, (
        "Finite quantiles must not masquerade as the analytic marginal CRPS."
    )
    shuffled = np.random.default_rng(321).permutation(n)
    shuffled_keys = tuple(years[shuffled.item(i)] for i in range(n))
    recoupled = rank_couple(template[shuffled], laws, shuffled_keys, config.seed)
    assert np.array_equal(coupled[shuffled], recoupled), "Tie order depends on row order."
    assert np.array_equal(inverse(np.asarray([[-2.0, -3.0]]), (1,)),
                          np.asarray([[-2.0, 0.0]])), "Negative rain was squared before censoring."
    duplicate = replace(training.targets[0], member_keys=("a", "a", "b"))
    try:
        _ = physical_template((duplicate, training.targets[1]))
    except AlternativeError as error:
        assert error.code == "G3_DUPLICATE_KEYS"
    else:
        raise AssertionError("Duplicated physical keys passed.")
    raw, keys, _ = physical_template(training.targets)
    dual = dual_ecc(raw, laws, keys, np.asarray([[1.0, 0.4], [0.4, 1.0]]),
                    np.ones(2), config.seed)
    for j, law in enumerate(laws):
        assert np.array_equal(np.sort(dual[:, j]), law.quantile((np.arange(3) + 0.5) / 3))
    residuals = generate_residuals(training, config, method_id="residual_gaussian_copula")
    assert isinstance(residuals, PITResidualSet)
    validate_residuals(training, residuals)
    assert residuals.years[0] == 2003 and len(residuals.years) == 14
    for _, past, fold in prequential_folds(training):
        assert past.catalog_cutoff == training.catalog_cutoff
        assert all(row.hist_end < fold.pseudo_init
                   for rows in past.rows_by_year.values() for row in rows)
        assert len(fold.training_row_ids) == 2 * len(past.source_years)
        assert set(fold.validation_row_ids).isdisjoint(fold.training_row_ids)
    zeros = [i for i, year in enumerate(residuals.years)
             if training.rows_by_year[year][1].observation == 0]
    assert zeros
    assert residuals.clipping_counts[0] >= len(zeros), "Extreme atom clips must be disclosed."

    def known_law(past: TrainingSet, settings: FitConfig) -> EmosMarginal:
        del settings
        return EmosMarginal(parameters=(0.0, 0.0, 1.0, 0.0), rain=past.target.variable == "prcp")

    atom_oracle = generate_residuals(
        training, config, method_id="residual_gaussian_copula", marginal_fitter=known_law,
    )
    assert isinstance(atom_oracle, PITResidualSet)
    first_pit = ndtr(atom_oracle.normal_score_repeats[0])
    other_pit = ndtr(atom_oracle.normal_score_repeats[1])
    assert np.allclose(first_pit[zeros, 1], 0.5 * atom_oracle.uniform_repeats[0][zeros, 1],
                       rtol=0, atol=1e-14), "Randomized atom PIT is not F(left)+v*mass."
    assert not np.array_equal(first_pit[zeros, 1], other_pit[zeros, 1]), "Atom uniforms were not used."
    forged = replace(residuals, fold_refs=(
        replace(residuals.fold_refs[0], training_row_ids=residuals.fold_refs[0].validation_row_ids),
        *residuals.fold_refs[1:],
    ))
    try:
        validate_residuals(training, forged)
    except AlternativeError as error:
        assert error.code == "NONPREQUENTIAL_RESIDUAL"
    else:
        raise AssertionError("In-sample residual ancestry passed.")
    shrunk = correlation(residuals.residual_matrix)
    assert float(np.linalg.eigvalsh(shrunk).min()) >= 0.5 - 1e-12
    scenarios = gaussian_copula(shrunk, laws, config.seed)
    larger = gaussian_copula(shrunk, laws, config.seed, 512)
    assert np.array_equal(scenarios, larger[:256]), "Sobol sensitivity is not nested."
    independent = gaussian_copula(np.eye(2), laws, config.seed)
    assert not np.array_equal(scenarios, independent)
    x, y = forward(training.forecast_means, (1,)), forward(training.observations, (1,))
    query = np.asarray([[8.5, 0.44], [-50, 4], [80, -1]])
    replay_errors: dict[str, Json] = {}
    predictions: list[FloatArray] = []
    for method in ("mbcp_annual", "mbcr_annual", "mbcn_annual"):
        mapping = fit_map(method, x, y, config.seed)
        replay = map_from_spec(mapping.to_spec())
        predicted = mapping.apply(query)
        assert np.array_equal(predicted, replay.apply(query))
        replay_errors[method] = float(np.linalg.norm(predicted - replay.apply(query), ord=np.inf))
        predictions.append(predicted)
        errors = generate_residuals(training, config, method_id=method)
        validate_residuals(training, errors)
        assert float(np.linalg.norm(errors.residual_matrix, ord=np.inf)) > 0.01
        if method == "mbcp_annual":
            future_year = training.source_years[-1]
            changed_rows = dict(training.rows_by_year)
            changed_rows[future_year] = tuple(
                replace(row, observation=row.observation + 1e6)
                for row in changed_rows[future_year]
            )
            changed_y = training.observations.copy()
            changed_y[-1] += 1e6
            changed = replace(training, rows_by_year=MappingProxyType(changed_rows),
                              observations=changed_y, train_hash="changed-future-training-truth")
            future_errors = generate_residuals(changed, config, method_id=method)
            assert np.array_equal(errors.residual_matrix[:-1], future_errors.residual_matrix[:-1]), (
                "A future accepted observation leaked into past residual fits."
            )
    assert not np.array_equal(predictions[0], predictions[1]), "MBCr was relabeled Pearson."
    full = fit_map("mbcn_annual", x, y, config.seed)
    prefix = fit_map("mbcn_annual", x[:12], y[:12], config.seed)
    full_rotations = [s.matrix for s in full.steps if isinstance(s, AffineStep)]
    past_rotations = [s.matrix for s in prefix.steps if isinstance(s, AffineStep)]
    assert all(np.array_equal(a, b) for a, b in zip(full_rotations, past_rotations, strict=True))
    tied = empirical_step(np.asarray([[0.0], [0.0], [2.0]]), np.asarray([[2.0], [4.0], [8.0]]))
    assert np.array_equal(tied.apply(np.asarray([[0.0], [0.0]])), np.asarray([[3.0], [3.0]]))
    constant = empirical_step(np.ones((4, 1)), np.arange(4.0)[:, None])
    assert np.array_equal(constant.apply(np.asarray([[-99.0], [99.0]])), np.asarray([[1.5], [1.5]]))
    return {
        "coupling_multisets": "PASS", "tie_shuffle": "PASS", "censor_before_square": "PASS",
        "duplicate_physical_keys": "REJECTED", "prequential_years": len(residuals.years),
        "whole_year_ancestry": "PASS", "atom_randomizations": 4,
        "atom_randomization_differences": len(zeros), "in_sample_ancestry": "REJECTED",
        "copula_minimum_eigenvalue": float(np.linalg.eigvalsh(shrunk).min()),
        "sobol_nested_256_512": "PASS", "mbc_replay_max_error": replay_errors,
        "mbcn_prefix_rotation_identity": "PASS", "ties_constants": "PASS",
        "future_observation_sentinel_past_residuals": "IDENTICAL",
        "finite_crps_permutation": "PASS", "analytic_discretization_difference": "NONZERO",
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2))
