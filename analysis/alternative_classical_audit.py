"""Executable mathematical and adversarial checks for classical local fits."""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import date
from math import log
from time import perf_counter

import numpy as np

from analysis.alternative_classical import fit_classical
from analysis.alternative_classical_common import coordinates, moments
from analysis.alternative_classical_laws import LocalModel
from analysis.alternative_classical_local import LOCAL_IDS, log_likelihood
from analysis.alternative_contracts import (
    CaseInput,
    FitConfig,
    FitStatus,
    MethodSpec,
    TrainingRow,
    TrainingSet,
)
from analysis.calibration import FloatArray


def synthetic(rain: bool, zeros: int = 3) -> TrainingSet:
    """Twenty-four annual observations with known issue/window ancestry."""
    variable = "prcp" if rain else "t15m"
    target = CaseInput(case_id="synthetic", init=date(2026, 2, 1),
                       valid_start=date(2026, 2, 2), valid_end=date(2026, 2, 8),
                       product="1mon", lead="1", variable=variable,
                       members=np.array([4.0, 7.0, 9.0]) if rain else np.array([8.0]),
                       member_keys=(), provenance_hash="synthetic")
    rng = np.random.default_rng(20261007)
    rows: list[TrainingRow] = []
    for i, year in enumerate(range(1993, 2017)):
        mean = 2.0 + i / 3
        ensemble = np.maximum(0, mean + np.array([-1.0, 0.0, 2.0])) if rain else (
            mean + np.array([-1.0, 0.0, 2.0]))
        y = max(0, 1.0 + .8 * mean + float(rng.normal())) if rain else (
            1.0 + .8 * mean + float(rng.normal()))
        if rain and i < zeros:
            y = 0.0
        rows.append(TrainingRow(row_id=str(year), source_case_id="archive",
                                source_case_init=date(2022, 2, 1), source_year=year,
                                source_init=date(year, 2, 1), hist_start=date(year, 2, 2),
                                hist_end=date(year, 2, 8), product="1mon", lead="1",
                                variable=variable, ensemble=ensemble, observation=y,
                                member_keys=(), provenance_hash="synthetic", archive_era="3"))
    values = np.array([row.observation for row in rows])
    return TrainingSet(target=target, rows=tuple(rows), year_weights=np.ones(24),
                       cutoff=target.init, catalog_cutoff=target.init, held_out_years=(2026,),
                       train_hash=f"synthetic-{rain}-{zeros}", local_observations=values,
                       thresholds=np.quantile(values, [1 / 3, 2 / 3]))


def method(name: str) -> MethodSpec:
    return MethodSpec(id=name, subtype=name, family_no=3, domain="both",
                      surface="continuous", fit_scope="local", algorithm_version="1",
                      owner="classical")


def mathematical_checks() -> int:
    """Compare likelihood objectives against the actually issued densities/atoms."""
    training = synthetic(True)
    coord = coordinates(training)
    mv: FloatArray = np.array([moments(row.ensemble, coord) for row in training.rows])
    y: FloatArray = training.local_observations / coord.scale
    count = 0
    parameters = {
        "emos_constant_variance": [0.5, 0.4, 0.7, 0.0],
        "mos_unit_slope": [0.5, 1.0, 0.7, 0.0],
        "gamma_positive": [0.5, 0.4, -0.7, -1.0],
        "csg_fixed_shift": [0.5, 0.4, -0.7, -1.0],
        "csg_estimated_shift": [0.5, 0.4, -0.7, -1.0, -2.0],
        "power_gaussian_sqrt": [0.2, 0.4, -0.5, 0.2],
        "power_gaussian_cuberoot": [0.2, 0.4, -0.5, 0.2],
        "power_logistic_sqrt": [0.2, 0.4, -0.5, 0.2],
        "power_logistic_cuberoot": [0.2, 0.4, -0.5, 0.2],
        "hurdle_gamma": [0.2, 0.4, -0.5, -1.0, 0.2],
        "hurdle_lognormal": [0.2, 0.4, -0.5, -1.0, 0.2],
        "gev_censored_gumbel": [0.2, 0.4, -0.5, 0.2],
        "gev_censored_shrunk_shape": [0.2, 0.4, -0.5, 0.2, -0.1],
    }
    for name, values in parameters.items():
        p: FloatArray = np.asarray(values)
        model = LocalModel(name, p, coord, True)
        ll = log_likelihood(name, p, mv[:, 0], mv[:, 1], y, training, coord, 1.5)
        for i, row in enumerate(training.rows):
            if name == "gamma_positive" and row.observation == 0:
                continue
            law = model.law(row.ensemble)
            expected = log(law.atom_mass(0)) if row.observation == 0 else (
                law.log_density(row.observation) + log(coord.scale))
            assert abs(ll.item(i) - expected) < 1e-9, (name, i, ll.item(i), expected)
            count += 1
    temperature = synthetic(False)
    c = coordinates(temperature)
    t_moments: FloatArray = np.array([moments(row.ensemble, c) for row in temperature.rows])
    t_y = (temperature.local_observations - c.offset) / c.scale
    p = np.array([0.5, 0.7, 0.3, 0.0])
    ll = log_likelihood("emos_constant_variance", p, t_moments[:, 0], t_moments[:, 1],
                        t_y, temperature, c, 1.5)
    model = LocalModel("emos_constant_variance", p, c, False)
    for i, row in enumerate(temperature.rows):
        expected = model.law(row.ensemble).log_density(row.observation) + log(c.scale)
        assert abs(ll.item(i) - expected) < 1e-10
        count += 1
    return count


def main() -> None:
    started = perf_counter()
    checks = mathematical_checks()
    records: list[dict[str, str | float]] = []
    config = FitConfig(workers=1)
    for rain in (False, True):
        training = synthetic(rain)
        names = LOCAL_IDS[1:] if rain else LOCAL_IDS[1:4]
        for name in names:
            fit = fit_classical(method(name), training, config)
            if name == "gamma_positive":
                assert fit.status == FitStatus.GATED_DATA
            else:
                assert fit.status == FitStatus.OK, (name, fit.reason_code, fit.diagnostics.message)
                assert fit.fitted_model is not None
                law = fit.fitted_model.predict(training.target)
                assert np.isfinite(law.mean())
                assert law.crps(0.0) >= 0
                assert 0 <= law.atom_mass(0) <= 1
                assert np.all(np.diff(law.cdf(np.array([-100, 0, 1, 10, 100]))) >= 0)
            records.append({"id": name, "variable": training.target.variable,
                            "status": str(fit.status), "seconds": fit.diagnostics.elapsed_seconds})
    wet = synthetic(True, 0)
    for name in ("gamma_positive", "hurdle_gamma", "hurdle_lognormal"):
        fit = fit_classical(method(name), wet, config)
        assert fit.status == FitStatus.OK, (name, fit.diagnostics.message)
        assert fit.fitted_model is not None
        if name.startswith("hurdle_"):
            assert 0 < fit.fitted_model.predict(wet.target).atom_mass(0) < 1
    bad = replace(wet, target=replace(wet.target, members=np.array([-1.0])))
    assert fit_classical(method("hurdle_gamma"), bad, config).status == FitStatus.INPUT_CONFLICT
    for name in ("bma_group_normal", "bma_group_rain"):
        data = wet if name.endswith("rain") else synthetic(False)
        assert fit_classical(method(name), data, config).status == FitStatus.GATED_DATA
    allzero = synthetic(True, 24)
    for name in ("hurdle_gamma", "hurdle_lognormal"):
        assert fit_classical(method(name), allzero, config).status == FitStatus.INSUFFICIENT_TRAINING
    constant = replace(synthetic(False), rows=tuple(
        replace(row, ensemble=np.ones(3), observation=2.0) for row in synthetic(False).rows),
        local_observations=np.full(24, 2.0), thresholds=np.array([2.0, 2.0]))
    fitted = fit_classical(method("mos_unit_slope"), constant, config)
    assert fitted.status == FitStatus.OK, fitted.diagnostics.message
    assert fitted.fitted_model is not None
    assert abs(fitted.fitted_model.predict(replace(constant.target, members=np.ones(1))).mean() - 2) < 1e-5
    base = fit_classical(method("emos_constant_variance"), synthetic(False), config)
    shuffled = synthetic(False)
    shuffled = replace(shuffled, rows=shuffled.rows[::-1],
                       year_weights=shuffled.year_weights[::-1])
    reordered = fit_classical(method("emos_constant_variance"), shuffled, config)
    assert base.fitted_model is not None and reordered.fitted_model is not None
    assert abs(base.fitted_model.predict(shuffled.target).mean()
               - reordered.fitted_model.predict(shuffled.target).mean()) < 1e-6
    print(json.dumps({"likelihood_identity_checks": checks, "fits": records,
                      "allwet_occurrence_penalty": "PASS", "negative_rain": "PASS",
                      "physical_group_gates": "PASS", "constant_single_member": "PASS",
                      "allzero_intensity_gate": "PASS", "row_permutation": "PASS",
                      "seconds": perf_counter() - started}, indent=2))


if __name__ == "__main__":
    main()
