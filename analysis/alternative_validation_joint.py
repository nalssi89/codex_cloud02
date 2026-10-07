"""Coupling checks: physical IDs, finite marginals and residual dependence."""

from __future__ import annotations

from dataclasses import replace

import numpy as np

from analysis.alternative_contracts import AlternativeError
from analysis.alternative_validation_io import number
from analysis.alternative_validation_learning import fixture
from analysis.alternative_validation_oracles import close, empirical_crps
from analysis.calibration import FloatArray
from analysis.data_io import Json


def coupling_checks() -> dict[str, Json]:
    from analysis.alternative_distributions import normal, weighted_empirical
    from analysis.alternative_joint_coordinates import correlation
    from analysis.alternative_joint_coupling import (
        gaussian_copula,
        physical_template,
        rank_couple,
    )

    marginals = (weighted_empirical(np.array([0., 1., 2., 4.]), np.ones(4)/4),
                 normal(0., 1.))
    template = np.array([[2., -1.], [0., 1.], [1., 1.], [3., -2.]])
    coupled = rank_couple(template, marginals, ("a", "b", "c", "d"), 42)
    probabilities = np.array([.125, .375, .625, .875])
    errors: list[Json] = []
    for column, marginal in enumerate(marginals):
        finite = marginal.quantile(probabilities)
        np.testing.assert_allclose(np.sort(coupled[:, column]), finite, atol=1e-12)
        close(empirical_crps(coupled[:, column], np.ones(4)/4, 1),
              empirical_crps(finite, np.ones(4)/4, 1), "finite empirical coupling CRPS")
        errors.append(empirical_crps(finite, np.ones(4)/4, 1)-marginal.crps(1))
    if abs(number(errors[1])) < 1e-4:
        raise AssertionError("analytic-to-finite sampling error falsely zero")
    target = fixture().target
    first = replace(target, members=np.array([1., 2., 3.]), member_keys=("a", "b", "c"))
    second = replace(target, case_id="second", members=np.array([30., 10., 20.]),
                     member_keys=("c", "a", "b"))
    joined, keys, _ = physical_template((first, second))
    if keys != ("a", "b", "c"):
        raise AssertionError("physical template did not retain keyed order")
    np.testing.assert_allclose(joined, np.array([[1., 10.], [2., 20.], [3., 30.]]))
    for bad in (
        replace(second, member_keys=("a", "a", "c")),
        replace(second, member_keys=("d", "e", "f")),
    ):
        try:
            _ = physical_template((first, bad))
        except AlternativeError as error:
            if not error.code.startswith("G3"):
                raise
        else:
            raise AssertionError("duplicate/misaligned physical IDs passed ECC")
    # Correlation is formed from explicitly different PIT-residual vectors.
    residual: FloatArray = np.array(
        [[-2., -1.8], [-1., -.8], [0., -.2], [1., 1.2], [2., 1.9]], dtype=np.float64)
    matrix = correlation(residual)
    expected_correlation = .5 * float(np.corrcoef(residual.T).take(1))
    close(float(matrix.take(1)), expected_correlation, "prescribed half-shrink residual correlation",
          atol=1e-12)
    if np.min(np.linalg.eigvalsh(matrix)) <= 0:
        raise AssertionError("residual dependence shrinkage is not SPD")
    laws = (normal(0., 1.), normal(0., 1.))
    independent = gaussian_copula(np.eye(2), laws, 42)
    dependent = gaussian_copula(matrix, laws, 42)
    full = gaussian_copula(matrix, laws, 42, 512)
    np.testing.assert_allclose(dependent, full[:256], atol=1e-12)
    independent_corr = float(np.corrcoef(independent.T).take(1))
    dependent_corr = float(np.corrcoef(dependent.T).take(1))
    if abs(independent_corr) > .1 or abs(dependent_corr-expected_correlation) > .1:
        raise AssertionError("Gaussian copula ignores residual PIT dependence")
    return {"status": "PASS", "analytic_finite_crps_differences": errors,
            "independent_scenario_correlation": independent_corr,
            "dependent_scenario_correlation": dependent_corr,
            "physical_key_join": "PASS", "Sobol_nested_256_512": "PASS"}
