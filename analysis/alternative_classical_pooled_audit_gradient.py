"""Original-unit objective and finite-difference gradient oracles for family nine."""

from __future__ import annotations

import json
from collections.abc import Callable, Generator
from contextlib import contextmanager
from datetime import date
from math import cos, exp, pi, sin, sqrt
from time import perf_counter
from typing import Literal
from unittest.mock import patch

import numpy as np
from scipy.optimize import OptimizeResult, minimize

from analysis.alternative_classical_pooled import IDS, PooledModel, fit_pooled
from analysis.alternative_contracts import (
    CaseInput,
    FitConfig,
    FitStatus,
    MethodSpec,
    TrainingRow,
    TrainingSet,
)
from analysis.calibration import FloatArray, gaussian_crps


def synthetic_training(rain: bool, pooled: bool, zeros: bool = False) -> TrainingSet:
    target = CaseInput(case_id="synthetic", init=date(2025, 1, 1),
                       valid_start=date(2025, 2, 1), valid_end=date(2025, 2, 7),
                       product="1mon", lead="1", variable="prcp" if rain else "t15m",
                       members=np.array([4., 6., 9.]) if rain else np.array([12., 13., 15.]),
                       member_keys=("a", "b", "c"), provenance_hash="synthetic")
    rows: list[TrainingRow] = []
    for year in range(1993, 2017):
        for lead in range(1, 3 if pooled else 2):
            signal = sin(year * 0.7)
            mean = 2 + 0.15*(year-1993) + 0.5*lead + signal
            members = np.array([mean-0.8, mean, mean+1.2])
            response = 1 + 0.1*(year-1993) + 0.6*mean + 0.5*cos(year)
            if rain:
                members = members**2
                response = 0.0 if zeros or year % 7 == 0 else response**2
            rows.append(TrainingRow(
                row_id=f"{year}_{lead}", source_case_id=f"case_{lead}",
                source_case_init=date(2024, 1, 1), source_year=year,
                source_init=date(year, 1, 1), hist_start=date(year, lead, 1),
                hist_end=date(year, lead, 7), product=target.product, lead=str(lead),
                variable=target.variable, ensemble=members, observation=response,
                member_keys=target.member_keys, provenance_hash="synthetic", archive_era="3_24",
            ))
    y = np.array([r.observation for r in rows])
    return TrainingSet(target=target, rows=tuple(rows),
                       year_weights=np.full(len(rows), 0.5 if pooled else 1.0),
                       cutoff=target.init, catalog_cutoff=target.init, held_out_years=(2025,),
                       train_hash="synthetic", local_observations=y, thresholds=np.quantile(y, [1/3, 2/3]))


def synthetic_spec(method: str, pooled: bool) -> MethodSpec:
    return MethodSpec(id=method, family_no=9 if pooled else 10, subtype="different_registry_subtype",
                      domain="both", surface="continuous", fit_scope="pooled" if pooled else "local",
                      algorithm_version="frozen_F9_F10", owner="classical")


def _objective(training: TrainingSet, method: str, p: FloatArray) -> float:
    """Reconstruct the physical law, without implementation latent/gradient helpers."""
    weights = training.year_weights/training.year_weights.sum()
    observed = np.array([row.observation for row in training.rows])
    rain = training.target.variable == "prcp"
    center = 0.0 if rain else float(weights @ observed)
    positive = observed > 0
    unit = float(weights[positive] @ observed[positive]/weights[positive].sum()) if (
        np.any(positive)) else 1.0
    scale = max(unit if rain else float(np.sqrt(weights @ (observed-center)**2)), 1.0)
    leads = tuple(sorted({row.lead for row in training.rows}))
    n = len(leads)
    locations: list[float] = []
    spreads: list[float] = []
    for row in training.rows:
        lead = leads.index(row.lead)
        standardized_mean = (float(row.ensemble.mean())-center)/scale
        mu = p.item(0)+p.item(2+lead)+p.item(2+n+lead)*standardized_mean
        offset = 2+2*n
        log_variance = p.item(offset)
        spread_variance = 0.0
        cursor = offset+1
        if method != "pooled_mos_ridge":
            log_variance += p.item(cursor+lead)
            cursor += n
            if row.ensemble.size > 1:
                spread_variance = p.item(cursor)*float(row.ensemble.var(ddof=1))/scale**2
            cursor += 1
        if method == "pooled_emos_cyclic":
            midpoint = row.hist_start+(row.hist_end-row.hist_start)/2
            phase = 2*pi*(midpoint-date(midpoint.year, 1, 1)).days/(
                date(midpoint.year+1, 1, 1)-date(midpoint.year, 1, 1)).days
            for k in (1, 2):
                coefficients: FloatArray = np.array([sin(k*phase), cos(k*phase)])
                index = cursor+2*(k-1)
                mu += float(coefficients @ p[index:index+2])
                log_variance += 2*float(coefficients @ p[index+4:index+6])
        locations.append(float(center+scale*mu))
        spreads.append(scale*sqrt(exp(log_variance)+spread_variance))
    loss = float(weights @ gaussian_crps(np.array(locations), np.array(spreads), observed, rain))
    penalty = 0.5*p.item(1)**2
    for lead in range(n):
        penalty += 0.5*(p.item(2+lead)**2+(p.item(2+n+lead)-p.item(1))**2)
    cursor = 3+2*n
    if method != "pooled_mos_ridge":
        penalty += 0.5*float(p[cursor:cursor+n] @ p[cursor:cursor+n])
        cursor += n+1
    if method == "pooled_emos_cyclic":
        for k in (1, 2):
            for index in (cursor+2*(k-1), cursor+4+2*(k-1)):
                penalty += 0.5*k**4*float(p[index:index+2] @ p[index:index+2])
    return loss+penalty/len({row.source_year for row in training.rows})


@contextmanager
def audit_optimizer(training: TrainingSet, method_id: str) -> Generator[None]:
    """Inspect the real optimizer's callbacks and then run that optimizer unchanged."""
    calls = 0

    def checked_minimize(fun: Callable[[FloatArray], float], x0: FloatArray, *,
                         method: Literal["L-BFGS-B"], jac: Callable[[FloatArray], FloatArray],
                         bounds: list[tuple[float | None, float | None]],
                         options: dict[str, int | float]) -> OptimizeResult:
        nonlocal calls
        calls += 1
        np.testing.assert_allclose(fun(x0), _objective(training, method_id, x0),
                                   rtol=1e-12, atol=1e-12)
        n = len({row.lead for row in training.rows})
        probe = x0.copy()
        probe[0] += 0.37
        probe[1] = 0.7
        probe[2:2+n] = np.linspace(0.1, 0.2, n)
        probe[2+n:2+2*n] = np.linspace(0.9, 1.1, n)
        probe[2+2*n] = -0.2
        cursor = 3+2*n
        if method_id != "pooled_mos_ridge":
            probe[cursor:cursor+n] = np.linspace(0.1, -0.1, n)
            cursor += n
            probe[cursor] = 0.4
            cursor += 1
        if method_id == "pooled_emos_cyclic":
            probe[cursor:cursor+8] = np.array([.1, -.08, .05, .03, -.05, .1, -.03, .04])
        np.testing.assert_allclose(fun(probe), _objective(training, method_id, probe),
                                   rtol=1e-12, atol=1e-12)
        numerical = np.empty(probe.size)
        for index in range(probe.size):
            epsilon = 1e-5*max(1.0, abs(probe.item(index)))
            high, low = probe.copy(), probe.copy()
            high[index] += epsilon
            low[index] -= epsilon
            numerical[index] = (_objective(training, method_id, high)
                                - _objective(training, method_id, low))/(2*epsilon)
        np.testing.assert_allclose(jac(probe), numerical, rtol=1e-5, atol=1e-6)
        return minimize(fun, x0, method=method, jac=jac, bounds=bounds,
                        options={"maxiter": int(options["maxiter"]), "ftol": options["ftol"],
                                 "gtol": options["gtol"]})

    with patch("analysis.alternative_classical_pooled.minimize", side_effect=checked_minimize):
        yield
    assert calls == 2, "both frozen optimizer starts must be gradient-audited"


def main() -> None:
    """Audit all six F9 fits without the separate duplicate-fit invariance check."""
    started = perf_counter()
    evidence: list[dict[str, object]] = []
    for rain in (False, True):
        training = synthetic_training(rain, pooled=True)
        for method_id in IDS:
            with audit_optimizer(training, method_id):
                result = fit_pooled(synthetic_spec(method_id, pooled=True), training, FitConfig(workers=1))
            assert result.status == FitStatus.OK, (method_id, rain, result.diagnostics)
            model = result.fitted_model
            assert isinstance(model, PooledModel) and result.diagnostics.convergence
            assert result.diagnostics.objective is not None
            oracle = _objective(training, method_id, model.parameters)
            np.testing.assert_allclose(result.diagnostics.objective, oracle, rtol=1e-12, atol=1e-12)
            law = model.predict(training.target)
            assert np.isfinite(law.mean()) and np.isfinite(law.crps(5.))
            evidence.append({"method": method_id, "rain": rain, "status": str(result.status),
                             "objective": result.diagnostics.objective, "oracle": oracle,
                             "mean": law.mean(), "crps": law.crps(5.)})
    print(json.dumps({"fits": evidence, "checks": "original-unit objectives and finite-difference gradients",
                      "elapsed_seconds": perf_counter()-started},
                     indent=2))


if __name__ == "__main__":
    main()
