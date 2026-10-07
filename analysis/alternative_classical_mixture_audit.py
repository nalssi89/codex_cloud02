"""Executable mathematical and actual-fit audits for the owned mixture methods."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from dataclasses import replace
from datetime import date
from math import cos, log, sin
from time import perf_counter

import numpy as np
from scipy.integrate import quad
from scipy.stats import norm

from analysis.alternative_classical_mixture import fit_mixture, validation_case
from analysis.alternative_classical_mixture_weights import (
    component_log_likelihood,
    fit_weights,
)
from analysis.alternative_classical_serialization import restore_distribution
from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FitConfig,
    FitStatus,
    MethodSpec,
    PredictiveDistribution,
    TrainingRow,
    TrainingSet,
)
from analysis.alternative_distribution_base import ScientificLaw, empirical
from analysis.calibration import FloatArray
from analysis.data_io import Json


class AuditOptions(argparse.Namespace):
    fits: bool = False
    fixed_fits: bool = False
    rain_bma: bool = False


def mathematical_audit() -> dict[str, object]:
    censored = ScientificLaw(tag="normal", parameters=(-1., 2.), censor_zero=True)
    continuous = ScientificLaw(tag="normal", parameters=(0., .01))
    second = ScientificLaw(tag="normal", parameters=(1., 1.), censor_zero=True)
    logs = component_log_likelihood((censored, continuous, second), 0)
    np.testing.assert_allclose(logs[[0, 2]], norm.logcdf([.5, -1]), atol=1e-13)
    assert np.isneginf(logs.item(1)), "Continuous density must not compete with atom masses"
    positive = component_log_likelihood((censored, continuous, second), 1)
    np.testing.assert_allclose(positive, [
        norm.logpdf(1, -1, 2), norm.logpdf(1, 0, .01), norm.logpdf(1, 1, 1)])
    counts = (3, 5, 7)
    total = sum(counts)
    atoms = tuple(empirical(np.array([float(i)]), np.ones(1)) for i in range(3))
    likelihood: FloatArray = np.vstack([component_log_likelihood(atoms, float(i))
                                       for i, count in enumerate(counts) for _ in range(count)])
    weights, objective, error = fit_weights(likelihood, np.ones(total))
    expected_weights: FloatArray = np.asarray([(count+1)/(total+3) for count in counts])
    np.testing.assert_allclose(weights, expected_weights, atol=1e-8)
    expected = -sum((count+1)*log(weights.item(i)) for i, count in enumerate(counts))
    np.testing.assert_allclose(objective, expected, atol=1e-10)
    equal, _, _ = fit_weights(np.zeros((8, 3)), np.ones(8))
    np.testing.assert_allclose(equal, np.ones(3)/3, atol=1e-13)
    try:
        _ = fit_weights(np.full((8, 3), -np.inf), np.ones(8))
    except AlternativeError as failure:
        assert failure.code == "INVALID_COMPONENT_LIKELIHOOD"
    else:
        raise AssertionError("Unsupported common likelihood was accepted")
    return {"atom_measure": "PASS", "dirichlet_closed_form": "PASS",
            "uniform_identical_components": "PASS", "unsupported_law": "PASS",
            "weight_stationarity_error": error}


def synthetic_training(rain: bool, n: int = 24) -> TrainingSet:
    """Deterministic annual pairs with actual dates, not mocked fitted models."""
    variable = "prcp" if rain else "t15m"
    target = CaseInput(case_id=f"mixture-audit-{variable}", init=date(2026, 1, 1),
                       valid_start=date(2026, 1, 2), valid_end=date(2026, 1, 8),
                       product="1mon", lead="1", variable=variable,
                       members=np.array([4., 6., 8.]), member_keys=("a", "b", "c"),
                       provenance_hash="mixture-audit")
    rows: list[TrainingRow] = []
    for i in range(n):
        year = 1993 + i
        mean = 3 + .35*i + .7*sin(i)
        observation = 1 + .7*mean + .8*cos(2.1*i)
        if rain and i % 7 == 0:
            observation = 0.
        rows.append(TrainingRow(
            row_id=f"mixture-audit-{variable}-{year}", source_case_id=target.case_id,
            source_case_init=target.init, source_year=year, source_init=date(year, 1, 1),
            hist_start=date(year, 1, 2), hist_end=date(year, 1, 8),
            product="1mon", lead="1", variable=variable,
            ensemble=np.array([mean-1, mean, mean+1]), observation=float(observation),
            member_keys=target.member_keys, provenance_hash="mixture-audit", archive_era=""))
    observations: FloatArray = np.array([row.observation for row in rows])
    return TrainingSet(target=target, rows=tuple(rows), year_weights=np.ones(n),
                       cutoff=target.init, catalog_cutoff=target.init, held_out_years=(2026,),
                       train_hash=f"mixture-audit-{variable}-{n}", local_observations=observations,
                       thresholds=np.quantile(observations, [1/3, 2/3]))


def cdf_oracle(law: PredictiveDistribution, observation: float, rain: bool) -> float:
    def cdf(z: float) -> float:
        value: FloatArray = np.asarray(z, dtype=np.float64)
        return law.cdf(value).item()

    left = quad(lambda z: cdf(z)**2, 0 if rain else -np.inf, observation,
                epsabs=1e-7, limit=200)[0]
    right = quad(lambda z: (1-cdf(z))**2, observation, np.inf,
                 epsabs=1e-7, limit=200)[0]
    return left + right


def fit_audit(rain_bma: bool, fixed_only: bool = False) -> dict[str, object]:
    from analysis.alternative_classical_local import fit_local
    from analysis.alternative_distributions import mixture, weighted_empirical

    report: dict[str, object] = {}
    config = FitConfig(workers=1)
    for rain in (False, True):
        training = synthetic_training(rain)
        methods = ["cdf_mix_fixed50", "anomaly_signal_shrink"]
        if not fixed_only:
            methods += ["cdf_mix_cv"]
        if not fixed_only and (not rain or rain_bma):
            methods += ["bma_component_pool"]
        spec = MethodSpec(id="cdf_mix_cv", family_no=2,
                          subtype="cdf_mix_cv", domain="both", surface="continuous",
                          fit_scope="local", algorithm_version="mixture-audit",
                          owner="classical")
        for kind in methods:
            spec = MethodSpec(id=kind, family_no=8 if kind.startswith("bma") else 2,
                              subtype="audit_registry_label", domain="both", surface="continuous",
                              fit_scope="local", algorithm_version="mixture-audit",
                              owner="classical")
            fitted = fit_mixture(spec, training, config)
            assert fitted.status == FitStatus.OK, (kind, fitted.reason_code,
                                                   fitted.diagnostics.message,
                                                   fitted.diagnostics.posterior_diagnostics)
            assert fitted.fitted_model is not None
            law = fitted.fitted_model.predict(training.target)
            observation = 5.0
            np.testing.assert_allclose(law.crps(observation), cdf_oracle(law, observation, rain),
                                       rtol=2e-5, atol=2e-5)
            _ = json.dumps(fitted.fitted_model.to_spec(), allow_nan=False)
            restored = round_trip(law)
            np.testing.assert_allclose(restored.mean(), law.mean(), rtol=1e-10, atol=1e-9)
            np.testing.assert_allclose(restored.crps(observation), law.crps(observation),
                                       rtol=1e-9, atol=1e-8)
            np.testing.assert_allclose(restored.cdf(np.array([0., 1., 5., 20.])),
                                       law.cdf(np.array([0., 1., 5., 20.])), atol=1e-12)
            np.testing.assert_allclose(restored.atom_mass(0), law.atom_mass(0), atol=1e-12)
            if kind == "bma_component_pool":
                years = fitted.diagnostics.posterior_diagnostics["common_prequential_years"]
                assert isinstance(years, list) and len(years) >= 8
            if kind == "cdf_mix_cv":
                from analysis.alternative_data import fold_training, inner_folds

                folds = inner_folds(training, training.target, min_years=15, last_n=5)
                assert 3 <= len(folds) <= 5
                scores: FloatArray = np.zeros(11)
                for fold in folds:
                    ancestor = fold_training(training, fold)
                    assert ancestor.catalog_cutoff == training.catalog_cutoff
                    assert all(row.hist_end < fold.pseudo_init for row in ancestor.rows)
                    fit = fit_local(replace(spec, id="emos", subtype="emos"), ancestor, config)
                    assert fit.fitted_model is not None
                    climate = weighted_empirical(ancestor.local_observations,
                                                 np.ones(len(ancestor.local_observations)))
                    rows = [r for r in training.rows if r.row_id in fold.validation_row_ids]
                    for row in rows:
                        emos = fit.fitted_model.predict(validation_case(row))
                        for i in range(11):
                            lam = i / 10
                            scores[i] += mixture((emos, climate), np.array([lam, 1-lam])
                                                 ).crps(row.observation)/len(rows)/len(folds)
                saved: FloatArray = np.asarray(
                    fitted.diagnostics.posterior_diagnostics["cv_grid_crps"], dtype=np.float64)
                np.testing.assert_allclose(scores, saved, rtol=1e-12, atol=1e-12)
            report[f"{training.target.variable}:{kind}"] = {
                "status": str(fitted.status), "mean": law.mean(), "crps": law.crps(observation),
                "seconds": fitted.diagnostics.elapsed_seconds,
                "common_prequential_years": fitted.diagnostics.posterior_diagnostics.get(
                    "common_prequential_years", []),
                "fold_failures": fitted.diagnostics.posterior_diagnostics.get("fold_failures", []),
                "weights": fitted.diagnostics.posterior_diagnostics.get("mixture_weights", []),
                "serialized_mean_crps": "PASS"}
            print(f"FITTED {training.target.variable} {kind} "
                  + f"{fitted.diagnostics.elapsed_seconds:.3f}s", flush=True)
        if not fixed_only:
            short = synthetic_training(rain, 17)
            spec = replace(spec, id="cdf_mix_cv", subtype="cdf_mix_cv", family_no=2)
            insufficient = fit_mixture(spec, short, config)
            assert insufficient.status == FitStatus.INSUFFICIENT_INNER_FOLDS
            assert insufficient.fitted_model is None
    return report


def round_trip(law: PredictiveDistribution,
               parse: Callable[[str], Json] = json.loads) -> PredictiveDistribution:
    """Exercise a JSON round trip, retaining every posterior mixture parameter."""
    payload = parse(json.dumps(law.to_spec(), allow_nan=False))
    if not isinstance(payload, dict):
        raise TypeError("Serialized law must be an object")
    return restore_distribution(payload)


def main() -> None:
    started = perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--fits", action="store_true", help="Exercise real strict-fold model fits")
    _ = parser.add_argument("--fixed-fits", action="store_true", help="Exercise fixed F2 fits only")
    _ = parser.add_argument("--rain-bma", action="store_true", help="Also exercise censored BJP BMA fits")
    options = parser.parse_args(namespace=AuditOptions())
    report = mathematical_audit()
    if options.fits or options.fixed_fits:
        report["actual_fits"] = fit_audit(options.rain_bma, fixed_only=options.fixed_fits)
    report["elapsed_seconds"] = perf_counter() - started
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
