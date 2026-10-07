"""Focused executable Bayesian surface QA; never reruns baseline production."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import replace
from datetime import date
from pathlib import Path
from time import perf_counter

import numpy as np

from analysis.alternative_bayes import (
    bayesian_method_specs,
    fit_bayes,
    fit_mbjp,
    model_from_spec,
)
from analysis.alternative_bayes_models import ScalarModel
from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FitConfig,
    FitStatus,
    JointTrainingSet,
    TrainingRow,
    TrainingSet,
)
from analysis.data_io import Json


def synthetic(rain: bool, dry: bool = False) -> TrainingSet:
    rng = np.random.default_rng(187)
    means = np.linspace(0.2, 1.3, 24)
    latent = 0.2 + 0.6 * means + rng.normal(0, 0.22, 24)
    observed = 100 * np.maximum(latent, 0) ** 2 if rain else 10 + 10 * latent
    forecasts = 100 * means**2 if rain else 10 + 10 * means
    if dry:
        observed[0] = 0
    target = CaseInput(
        case_id=f"synthetic_{rain}_{dry}", init=date(2023, 1, 1),
        valid_start=date(2023, 1, 8), valid_end=date(2023, 1, 14),
        product="1mon", lead="1", variable="prcp" if rain else "t15m",
        members=np.asarray([35., 45., 55.]) if rain else np.asarray([16., 17., 18.]),
        member_keys=("a", "b", "c"), provenance_hash="synthetic",
    )
    rows = tuple(TrainingRow(
        row_id=f"{target.case_id}_{year}", source_case_id=target.case_id,
        source_case_init=target.init, source_year=year, source_init=date(year, 1, 1),
        hist_start=date(year, 1, 8), hist_end=date(year, 1, 14), product="1mon",
        lead="1", variable=target.variable,
        ensemble=np.asarray([forecasts.item(i) * 0.9, forecasts.item(i), forecasts.item(i) * 1.1]),
        observation=observed.item(i), member_keys=("a", "b", "c"),
        provenance_hash="synthetic", archive_era="three_24",
    ) for i, year in enumerate(range(1993, 2017)))
    return TrainingSet(
        target=target, rows=rows, year_weights=np.ones(24), cutoff=target.init,
        catalog_cutoff=target.init, held_out_years=(2023,), train_hash=target.case_id,
        local_observations=observed, thresholds=np.quantile(observed, [1 / 3, 2 / 3]),
    )


def scalar_check(
    training: TrainingSet, method: str, score_observation: float | None = None,
) -> dict[str, Json]:
    spec = next(s for s in bayesian_method_specs() if s.id == method)
    result = fit_bayes(spec, training, FitConfig(workers=1))
    if result.status != FitStatus.OK or result.fitted_model is None:
        raise AssertionError(f"{method}: {result.status}: {result.diagnostics.message}")
    distribution = result.fitted_model.predict(training.target)
    probabilities = np.asarray([0.05, 0.33, 0.5, 0.67, 0.95])
    quantiles = distribution.quantile(probabilities)
    assert np.all(np.diff(quantiles) >= 0)
    assert math.isfinite(distribution.mean())
    observation = training.local_observations.item(12) if score_observation is None else score_observation
    score = distribution.crps(observation)
    assert math.isfinite(score) and score >= 0
    _ = json.dumps(result.fitted_model.to_spec(), allow_nan=False)
    restored = model_from_spec(result.fitted_model.to_spec())
    assert isinstance(restored, ScalarModel)
    np.testing.assert_allclose(restored.predict(training.target).quantile(probabilities), quantiles)
    if training.target.variable == "prcp":
        assert distribution.atom_mass(0) > 0
        assert distribution.cdf(np.asarray([-1.])).item(0) == 0
    return {
        "method": method, "case": training.target.case_id,
        "elapsed_seconds": result.diagnostics.elapsed_seconds,
        "mean": distribution.mean(), "crps_probe": score,
        "score_probe": "training" if score_observation is None else "verified_truth_scoring_only",
        "posterior": dict(result.diagnostics.posterior_diagnostics),
    }


def synthetic_joint(components: int) -> JointTrainingSet:
    scalar = synthetic(False)
    rng = np.random.default_rng(711)
    targets = tuple(replace(scalar.target, case_id=f"path_{j}") for j in range(components))
    forecast = 10 + 10 * rng.normal(size=(24, components))
    observed = 0.7 * forecast + rng.normal(size=(24, components))
    return JointTrainingSet(
        targets=targets, component_keys=tuple(t.case_id for t in targets),
        rows_by_year={}, source_years=tuple(range(1993, 2017)),
        historical_initializations=tuple(r.source_init for r in scalar.rows),
        historical_windows=(), forecast_means=forecast, observations=observed,
        cutoff=scalar.cutoff, catalog_cutoff=scalar.catalog_cutoff,
        held_out_years=(2023,), train_hash=f"synthetic_joint_{components}",
    )


def joint_check(training: JointTrainingSet, method: str) -> dict[str, Json]:
    spec = next(s for s in bayesian_method_specs() if s.id == method)
    result = fit_mbjp(spec, training, FitConfig(workers=1))
    assert result.status == FitStatus.OK, result.diagnostics.message
    assert result.fitted_model is not None
    prediction = result.fitted_model.predict(training.targets, (), FitConfig())
    assert prediction.samples.shape == (256, len(training.targets))
    assert np.all(np.isfinite(prediction.samples))
    _ = json.dumps(result.fitted_model.to_spec(), allow_nan=False)
    restored = model_from_spec(result.fitted_model.to_spec())
    assert not isinstance(restored, ScalarModel)
    np.testing.assert_array_equal(
        prediction.samples, restored.predict(training.targets, (), FitConfig()).samples
    )
    return {"method": method, "components": len(training.targets),
            "elapsed_seconds": result.diagnostics.elapsed_seconds,
            "posterior": {
                key: value for key, value in result.diagnostics.posterior_diagnostics.items()
                if key not in {"rhat", "ess_bulk", "ess_tail"}
            }}


def run_synthetic(censored: bool) -> list[dict[str, Json]]:
    results: list[dict[str, Json]] = []
    methods = (
        ("joint_gaussian_plugin", False), ("bjp_niw", False),
        ("bayesian_anomaly_ridge", False), ("bjp_t", False), ("bjp_ti", False),
        ("bjp_sqrt_censored", True), ("bjp_yj_fixed", True),
        ("bjp_logsinh_fixed", True), ("bayesian_anomaly_ridge", True),
        ("bjp_t", True), ("bjp_ti", True),
    )
    for method, rain in methods:
        result = scalar_check(synthetic(rain, dry=censored and rain), method)
        results.append(result)
        print(json.dumps(result), flush=True)
    for dimension in (2, 12, 16):
        results.append(joint_check(synthetic_joint(dimension), "mbjp_niw"))
    # G5 stays closed even though counts and distinct stored labels exist.
    for spec in bayesian_method_specs():
        if spec.family_no == 17:
            assert fit_bayes(spec, synthetic(False), FitConfig()).status == FitStatus.GATED_DATA
    training = synthetic(False)
    spec = next(s for s in bayesian_method_specs() if s.id == "bjp_niw")
    authoritative = fit_bayes(replace(spec, subtype="bjp_t"), training, FitConfig())
    assert authoritative.fitted_model is not None
    reference = fit_bayes(spec, training, FitConfig())
    assert reference.fitted_model is not None
    assert authoritative.fitted_model.to_spec() == reference.fitted_model.to_spec()
    try:
        _ = fit_bayes(replace(spec, id="unknown"), training, FitConfig())
    except AlternativeError as error:
        assert error.code == "UNKNOWN_BAYES_METHOD"
    else:
        raise AssertionError("Unknown authoritative ID did not raise typed failure")
    assert fit_bayes(spec, replace(training, rows=training.rows[:9]), FitConfig()).status == FitStatus.INSUFFICIENT_TRAINING
    repeated = replace(training, rows=(*training.rows, training.rows[0]))
    assert fit_bayes(spec, repeated, FitConfig()).status == FitStatus.INPUT_CONFLICT
    if censored:
        training = synthetic(True, True)
        zero_target = replace(training.target, members=np.zeros(3), case_id="zero_target")
        results.append(scalar_check(replace(training, target=zero_target), "bjp_sqrt_censored"))
    return results


def run_real() -> list[dict[str, Json]]:
    from analysis.alternative_data import aligned_joint, load_experiment, training_for

    print("WORKING loading active original catalog for small Bayesian QA", flush=True)
    inputs = load_experiment(Path(__file__).resolve().parents[1])
    selected: dict[str, TrainingSet] = {}
    for target in inputs.cases:
        if target.case_id not in inputs.historical:
            continue
        label = f"{target.product}_{target.variable}"
        training = training_for(target, inputs, "local")
        if target.variable == "prcp" and np.any(np.equal(training.local_observations, 0)):
            label += "_dry"
        if label not in selected:
            selected[label] = training
        if len(selected) == 5:
            break
    results: list[dict[str, Json]] = []
    for label, training in selected.items():
        method = "bjp_niw" if training.target.variable == "t15m" else "bjp_sqrt_censored"
        methods = (
            "bjp_sqrt_censored", "bjp_yj_fixed", "bjp_logsinh_fixed",
            "bayesian_anomaly_ridge", "bjp_t", "bjp_ti",
        ) if label.endswith("_dry") else (method,)
        for method in methods:
            result = scalar_check(
                training, method, inputs.truths[training.target.case_id].observation
            )
            result["stratum"] = label
            results.append(result)
            print(json.dumps({"verified": method, "stratum": label,
                              "elapsed_seconds": result["elapsed_seconds"]}), flush=True)
    first = selected["1mon_t15m"].target
    path = tuple(t for t in inputs.cases if t.init == first.init and t.product == first.product)
    results.append(joint_check(aligned_joint(path, inputs), "mbjp_sqrt_censored"))
    monthly = selected["3mon_t15m"].target
    path = tuple(t for t in inputs.cases if t.init == monthly.init and t.product == monthly.product)
    results.append(joint_check(aligned_joint(path, inputs), "mbjp_sqrt_censored"))
    return results


class Arguments(argparse.Namespace):
    censored: bool = False
    real: bool = False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--censored", action="store_true", help="Include genuine four-chain censored fits")
    _ = parser.add_argument("--real", action="store_true", help="Read active source and fit only small real strata")
    args = Arguments()
    _ = parser.parse_args(namespace=args)
    started = perf_counter()
    print("WORKING Bayesian focused numerical QA", flush=True)
    results = run_real() if args.real else run_synthetic(args.censored)
    print(json.dumps({"status": "PASS", "fits": results,
                      "elapsed_seconds": perf_counter() - started}, indent=2), flush=True)


if __name__ == "__main__":
    main()
