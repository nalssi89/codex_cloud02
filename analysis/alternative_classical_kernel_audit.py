"""Executable independent synthetic audit: python -m analysis.alternative_classical_kernel_audit."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, replace
from datetime import date
from math import log
from unittest.mock import patch

import numpy as np
from scipy.special import expit
from scipy.stats import gamma as gamma_stat
from scipy.stats import norm

from analysis.alternative_classical_kernel import (
    KernelModel,
    fit_kernel,
    kernel_log_likelihood,
    kernel_penalty,
)
from analysis.alternative_contracts import (
    CaseInput,
    FitConfig,
    FitStatus,
    MethodSpec,
    TrainingRow,
    TrainingSet,
)
from analysis.alternative_distributions import distribution_from_spec
from analysis.calibration import FloatArray


@dataclass(frozen=True)
class FailedSolve:
    """Preserve the actual unsuccessful optimizer result interface in the audit."""

    success: bool = False
    fun: float = 0.0
    nit: int = 500
    message: str = "audit forced iteration limit"

    @property
    def x(self) -> FloatArray:
        return np.zeros(3, dtype=np.float64)


def synthetic(rain: bool, all_wet: bool = False, single: bool = False) -> TrainingSet:
    rng = np.random.default_rng(20261007)
    variable = "prcp" if rain else "t15m"
    target = CaseInput(case_id="synthetic", init=date(2026, 1, 1),
                       valid_start=date(2026, 2, 1), valid_end=date(2026, 2, 7),
                       product="1mon", lead="1", variable=variable,
                       members=np.array([0.0, 6.0, 12.0] if rain else [-1.0, 1.0, 3.0]),
                       member_keys=(), provenance_hash="synthetic")
    rows: list[TrainingRow] = []
    for i, year in enumerate(range(1993, 2023)):
        mean = float(rng.uniform(0.1, 15) if rain else rng.normal(1, 3))
        ensemble: FloatArray = np.array([mean] if single else
                                       [mean - 0.1, mean, mean + 0.1])
        observation = (float(rng.gamma(3, (2 + mean) / 3)) if rain else
                       float(1 + 0.7 * mean + rng.normal(0, 1.5)))
        if rain and not all_wet and i % 7 == 0:
            observation = 0.0
        if rain and i == 1:
            observation = 0.001  # Positive amounts are never thresholded to dry.
        rows.append(TrainingRow(
            row_id=str(year), source_case_id="synthetic", source_case_init=date(2025, 1, 1),
            source_year=year, source_init=date(year, 1, 1),
            hist_start=date(year, 2, 1), hist_end=date(year, 2, 7),
            product="1mon", lead="1", variable=variable, ensemble=ensemble,
            observation=observation, member_keys=(), provenance_hash="synthetic", archive_era=""))
    obs: FloatArray = np.array([r.observation for r in rows])
    return TrainingSet(target=target, rows=tuple(rows), year_weights=np.ones(30),
                       cutoff=target.init, catalog_cutoff=target.init, held_out_years=(2026,),
                       train_hash="synthetic", local_observations=obs,
                       thresholds=np.quantile(obs, [1/3, 2/3]))


def method(rain: bool) -> MethodSpec:
    return MethodSpec(id="kernel_rain_hurdle_equal" if rain else "kernel_normal_equal",
                      family_no=8, subtype="equal", domain="precipitation" if rain else "temperature",
                      surface="continuous", fit_scope="local", algorithm_version="frozen-f8",
                      owner="classical")


def audit() -> list[dict[str, object]]:
    # Independent original-unit likelihood oracle, including exact zero masses.
    f: FloatArray = np.array([0.0, 0.5, 2.0])
    for rain in (False, True):
        p: FloatArray = np.array([0.7, 0.9, log(1.3), -1.0, 0.4] if rain else
                                [0.7, 0.9, log(1.3)])
        for y in ((0.0, 0.0001, 1.5) if rain else (-1.0, 1.5)):
            if rain:
                pzero = expit(-1 + 0.4 * np.log1p(f))
                means = np.logaddexp(0, 0.7 + 0.9*f) + 1e-6
                density = (pzero if y == 0 else
                           (1-pzero) * gamma_stat.pdf(y, a=1.3, scale=means/1.3) / 7)
            else:
                density = norm.pdf(y, loc=0.7 + 0.9*f, scale=1.3) / 7
            actual = kernel_log_likelihood(p, f, y, rain, 7)
            assert np.isclose(actual, log(float(np.mean(density))), atol=1e-12)
            repeated: FloatArray = np.tile(f, 4)
            assert np.isclose(kernel_log_likelihood(p, repeated, y, rain, 7), actual)
        expected = 0.5*0.9**2 + ((1+0.4**2)/8 if rain else 0)
        assert np.isclose(kernel_penalty(p, rain), expected)
    records: list[dict[str, object]] = []
    for rain, all_wet, single in ((False, False, False), (True, False, False),
                                 (True, True, False), (False, False, True)):
        training = synthetic(rain, all_wet, single)
        fit = fit_kernel(method(rain), training, FitConfig())
        assert fit.status == FitStatus.OK, fit.diagnostics.message
        model = fit.fitted_model
        assert isinstance(model, KernelModel)
        law = model.predict(training.target)
        restored = distribution_from_spec(law.to_spec())
        x: FloatArray = np.array([-1, 0, 0.001, 3, 100], dtype=np.float64)
        assert np.allclose(law.cdf(x), restored.cdf(x), atol=1e-12)
        assert np.all(np.diff(law.cdf(x)) >= 0)
        assert np.isfinite(law.mean()) and np.isfinite(law.crps(2))
        q: FloatArray = np.array([0.1, 0.5, 0.9])
        assert np.all(np.diff(law.quantile(q)) >= 0)
        repeated_target = replace(training.target, members=np.tile(training.target.members, 3))
        assert np.allclose(law.cdf(x), model.predict(repeated_target).cdf(x))
        permuted = replace(training.target, members=training.target.members[::-1])
        assert np.allclose(law.cdf(x), model.predict(permuted).cdf(x))
        annual = 0.0
        for i, row in enumerate(training.rows):
            issued = model.predict(replace(training.target, members=row.ensemble))
            ll = (log(issued.atom_mass(0)) if rain and row.observation == 0
                  else issued.log_density(row.observation))
            annual -= float(training.year_weights.item(i)) * ll
        assert np.isclose(annual, model.training_nll, atol=1e-8)
        assert fit.diagnostics.objective is not None
        assert np.isclose(annual + model.penalty, fit.diagnostics.objective)
        if rain:
            assert 0 < law.atom_mass(0) < 1
            assert float(law.cdf_left(np.array(0.0))) == 0
        records.append({"method": method(rain).id, "all_wet": all_wet, "single": single,
                        "objective": fit.diagnostics.objective,
                        "elapsed_seconds": fit.diagnostics.elapsed_seconds,
                        "solver": fit.diagnostics.message,
                        "mean": law.mean(), "p_zero": law.atom_mass(0)})
    training = synthetic(True)
    scarce = replace(training, rows=tuple(replace(r, observation=0.0) for r in training.rows))
    assert fit_kernel(method(True), scarce, FitConfig()).reason_code == (
        "FEWER_THAN_THREE_POSITIVE_YEARS")
    invalid = replace(training, rows=(replace(training.rows[0], observation=-1),
                                      *training.rows[1:]))
    assert fit_kernel(method(True), invalid, FitConfig()).status == FitStatus.INPUT_CONFLICT
    with patch("analysis.alternative_classical_common.minimize", return_value=FailedSolve()):
        failure = fit_kernel(method(False), synthetic(False), FitConfig())
    assert failure.status == FitStatus.FIT_FAILED and failure.fitted_model is None
    assert failure.reason_code == "SOLVER_NOT_CONVERGED"
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.parse_args()
    print(json.dumps({"checks": "PASS", "fits": audit()}, indent=2))


if __name__ == "__main__":
    main()
