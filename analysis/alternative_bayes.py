"""Frozen family 1/10/16/17 Bayesian fitting interfaces.

Each local model is explicitly target-conditioned on known issued inputs.
Reusing it for different predictors requires a new fit; no truth is accessible.
"""

from __future__ import annotations

from time import perf_counter

import numpy as np

from analysis.alternative_bayes_engine import fit_law
from analysis.alternative_bayes_models import (
    MultivariateModel,
    ScalarModel,
    model_from_spec,
)
from analysis.alternative_bayes_sampler import PosteriorFailure
from analysis.alternative_contracts import (
    AlternativeError,
    FitConfig,
    FitDiagnostics,
    FitResult,
    FitStatus,
    JointFitResult,
    JointTrainingSet,
    MethodSpec,
    TrainingSet,
)

__all__ = ["bayesian_method_specs", "fit_bayes", "fit_mbjp", "model_from_spec"]


def _failure_status(error: AlternativeError | np.linalg.LinAlgError | FloatingPointError) -> FitStatus:
    match error:
        case AlternativeError(code="POSTERIOR_DIAGNOSTICS_FAILED"):
            return FitStatus.POSTERIOR_DIAGNOSTICS_FAILED
        case AlternativeError(code="NUMERICAL_DISTRIBUTION_FAILED"):
            return FitStatus.NUMERICAL_DISTRIBUTION_FAILED
        case _:
            return FitStatus.FIT_FAILED


def bayesian_method_specs() -> tuple[MethodSpec, ...]:
    """Inventory entries for the root registry; G5 is an evidence-backed gate."""
    entries = (
        ("joint_gaussian_plugin", 1, "temperature", "continuous"),
        ("bjp_niw", 1, "temperature", "continuous"),
        ("bjp_sqrt_censored", 1, "precipitation", "continuous"),
        ("bayesian_anomaly_ridge", 1, "both", "continuous"),
        ("bjp_yj_fixed", 1, "precipitation", "continuous"),
        ("bjp_logsinh_fixed", 1, "precipitation", "continuous"),
        ("bjp_t", 10, "both", "continuous"),
        ("bjp_ti", 10, "both", "continuous"),
        ("mbjp_niw", 16, "temperature", "joint"),
        ("mbjp_sqrt_censored", 16, "both", "joint"),
        ("finite_member_iid_signal_noise", 17, "temperature", "continuous"),
        ("finite_member_known_covariance", 17, "temperature", "continuous"),
    )
    result: list[MethodSpec] = []
    for method, family, domain, surface in entries:
        result.append(MethodSpec(
            id=method, family_no=family, subtype=method,
            domain="both" if domain == "both" else (
                "temperature" if domain == "temperature" else "precipitation"
            ),
            surface="joint" if surface == "joint" else "continuous",
            fit_scope="joint" if surface == "joint" else "local",
            algorithm_version="bayes-fixed-physical-v1", owner="bayes",
            gate_ids=("G5",) if family == 17 else (("G2",) if family == 16 else ()),
            fixed_parameters={"physical_temperature_center": 10.0,
                              "physical_temperature_scale": 10.0,
                              "physical_rain_scale": 100.0},
        ))
    return tuple(result)


def fit_bayes(spec: MethodSpec, training: TrainingSet, config: FitConfig) -> FitResult:
    started = perf_counter()
    n = len(training.rows)
    years = {r.source_year for r in training.rows}
    base = FitDiagnostics(n_rows=n, n_years=len(years), train_hash=training.train_hash)
    if spec.id in {"finite_member_iid_signal_noise", "finite_member_known_covariance"}:
        return FitResult(
            method_id=spec.id, status=FitStatus.GATED_DATA, fitted_model=None,
            diagnostics=FitDiagnostics(
                n_rows=n, n_years=len(years), train_hash=training.train_hash,
                message="G5 closed: no justified iid homogeneous error or supplied covariance law.",
                posterior_diagnostics={"gate": "G5", "evidence":
                                       ".omo/evidence/alternative-input-applicability.md"},
            ), reason_code="G5_MEMBER_ERROR_LAW_UNPROVEN",
        )
    allowed = {s.id: s for s in bayesian_method_specs() if s.surface == "continuous"}
    if spec.id not in allowed:
        raise AlternativeError("UNKNOWN_BAYES_METHOD", spec.id)
    domain = allowed[spec.id].domain
    rain = training.target.variable == "prcp"
    if (domain == "temperature" and rain) or (domain == "precipitation" and not rain):
        return FitResult(method_id=spec.id, status=FitStatus.NOT_APPLICABLE_DOMAIN,
                         fitted_model=None, diagnostics=base, reason_code="VARIABLE_DOMAIN")
    if len(years) < 10:
        return FitResult(method_id=spec.id, status=FitStatus.INSUFFICIENT_TRAINING,
                         fitted_model=None, diagnostics=base, reason_code="FEWER_THAN_10_YEARS")
    if len(years) != n:
        return FitResult(method_id=spec.id, status=FitStatus.INPUT_CONFLICT,
                         fitted_model=None, diagnostics=base, reason_code="REPEATED_ANNUAL_VECTOR")
    try:
        law = fit_law(
            spec.id, np.asarray([[float(r.ensemble.mean())] for r in training.rows]),
            np.asarray([[r.observation] for r in training.rows]),
            np.asarray([r.hist_start.year for r in training.rows], dtype=float),
            (training.target,), training.train_hash, config,
        )
        diagnostics = FitDiagnostics(
            convergence=True, n_rows=n, n_years=len(years), train_hash=training.train_hash,
            parameter_count=3 if spec.id == "bayesian_anomaly_ridge" else (
                7 if spec.id in {"bjp_t", "bjp_ti"} else 5
            ),
            elapsed_seconds=perf_counter() - started,
            posterior_diagnostics=law.posterior_metadata,
            message="Plug-in, not Bayesian." if spec.id == "joint_gaussian_plugin" else
                    "Fixed proper prior; known-input target-conditioned posterior law.",
        )
        return FitResult(method_id=spec.id, status=FitStatus.OK,
                         fitted_model=ScalarModel(law=law), diagnostics=diagnostics)
    except (AlternativeError, np.linalg.LinAlgError, FloatingPointError) as error:
        status = _failure_status(error)
        return FitResult(
            method_id=spec.id, status=status, fitted_model=None,
            diagnostics=FitDiagnostics(
                n_rows=n, n_years=len(years), train_hash=training.train_hash,
                elapsed_seconds=perf_counter() - started, message=str(error),
                posterior_diagnostics=error.diagnostics if isinstance(error, PosteriorFailure) else {},
            ), reason_code=error.code if isinstance(error, AlternativeError) else type(error).__name__,
        )


def fit_mbjp(
    spec: MethodSpec, training: JointTrainingSet, config: FitConfig,
) -> JointFitResult:
    started = perf_counter()
    n = len(training.source_years)
    base = FitDiagnostics(n_rows=n, n_years=n, train_hash=training.train_hash)
    if spec.id not in {"mbjp_niw", "mbjp_sqrt_censored"}:
        raise AlternativeError("UNKNOWN_MBJP_METHOD", spec.id)
    if spec.id == "mbjp_niw" and any(t.variable == "prcp" for t in training.targets):
        return JointFitResult(method_id=spec.id, status=FitStatus.NOT_APPLICABLE_DOMAIN,
                              fitted_model=None, diagnostics=base, reason_code="TEMPERATURE_ONLY")
    if n < 10 or any(not receipt.allowed for receipt in training.gate_receipts):
        return JointFitResult(method_id=spec.id, status=FitStatus.GATED_DATA,
                              fitted_model=None, diagnostics=base, reason_code="G2_ALIGNMENT")
    if len(set(training.source_years)) != n:
        return JointFitResult(method_id=spec.id, status=FitStatus.INPUT_CONFLICT,
                              fitted_model=None, diagnostics=base, reason_code="REPEATED_ANNUAL_VECTOR")
    try:
        law = fit_law(
            spec.id, training.forecast_means, training.observations,
            np.asarray(training.source_years, dtype=float),
            training.targets, training.train_hash, config,
        )
        d = 2 * len(training.targets)
        return JointFitResult(
            method_id=spec.id, status=FitStatus.OK, fitted_model=MultivariateModel(law=law),
            diagnostics=FitDiagnostics(
                convergence=True, n_rows=n, n_years=n, train_hash=training.train_hash,
                parameter_count=d + d * (d + 1) // 2,
                posterior_diagnostics=law.posterior_metadata,
                elapsed_seconds=perf_counter() - started,
                message="One complete annual joint vector; no member identity/iid assumption.",
            ),
        )
    except (AlternativeError, np.linalg.LinAlgError, FloatingPointError) as error:
        status = _failure_status(error)
        return JointFitResult(
            method_id=spec.id, status=status, fitted_model=None,
            diagnostics=FitDiagnostics(
                n_rows=n, n_years=n, train_hash=training.train_hash,
                elapsed_seconds=perf_counter() - started, message=str(error),
                posterior_diagnostics=error.diagnostics if isinstance(error, PosteriorFailure) else {},
            ), reason_code=error.code if isinstance(error, AlternativeError) else type(error).__name__,
        )
