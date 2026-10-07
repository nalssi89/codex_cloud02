"""Section-8 annual coupling and transport fit/predict entry points."""

from __future__ import annotations

import time

import numpy as np

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FitConfig,
    FitDiagnostics,
    FitStatus,
    JointFitResult,
    JointModel,
    JointPrediction,
    JointTrainingSet,
    MethodSpec,
    PredictiveDistribution,
    ResidualSet,
)
from analysis.alternative_joint_coordinates import correlation, forward, rain_columns
from analysis.alternative_joint_coupling import physical_template
from analysis.alternative_joint_folds import validate_residuals
from analysis.alternative_joint_gates import (
    check_dynamic,
    check_physical,
    check_training,
)
from analysis.alternative_joint_marginals import fit_bjp_marginal
from analysis.alternative_joint_mbc import FrozenMap, fit_map
from analysis.alternative_joint_model import AnnualJointModel
from analysis.alternative_joint_ot import FrozenTransport, fit_ot
from analysis.alternative_joint_residuals import PITResidualSet, generate_residuals
from analysis.calibration import FloatArray


def fit_joint(
    spec: MethodSpec, training: JointTrainingSet, residuals: ResidualSet | None,
    config: FitConfig,
) -> JointFitResult:
    """Fit exact annual algorithms; factual gates never mask computational expense."""
    started = time.perf_counter()
    try:
        check_training(training)
        method = spec.id
        marginal_method = spec.fixed_parameters.get("marginal_method", "emos")
        if marginal_method not in ("emos", "bjp"):
            raise AlternativeError("INVALID_FIXED_MARGINAL_METHOD", str(marginal_method))
        marginal_name = str(marginal_method)
        mapping: FrozenMap | None = None
        transport: FrozenTransport | None = None
        dependence: FloatArray | None = None
        rain = rain_columns(training.targets)
        if method in ("ecc_q", "decc_path_shrunk_error"):
            check_physical(training, path=method == "decc_path_shrunk_error")
            _ = physical_template(training.targets)
        if method == "dotc_annual":
            check_dynamic(training)
        needs_residual = method in (
            "mbcp_annual", "mbcr_annual", "mbcn_annual",
            "residual_gaussian_copula", "decc_path_shrunk_error",
        )
        fitted_residuals = residuals
        if needs_residual:
            if fitted_residuals is None:
                fitted_residuals = generate_residuals(
                    training, config, method_id=method,
                    marginal_fitter=fit_bjp_marginal if marginal_name == "bjp" else None,
                    marginal_method=marginal_name,
                )
            validate_residuals(training, fitted_residuals)
            wanted = "pit_normal" if method == "residual_gaussian_copula" else "latent_error"
            if fitted_residuals.kind != wanted:
                raise AlternativeError("WRONG_RESIDUAL_COORDINATES", fitted_residuals.kind)
            if method == "residual_gaussian_copula" and not isinstance(fitted_residuals, PITResidualSet):
                raise AlternativeError("MISSING_PIT_RANDOMIZATION_EVIDENCE", "Use generate_residuals for four saved PIT transforms.")
            if isinstance(fitted_residuals, PITResidualSet) and fitted_residuals.marginal_method != marginal_name:
                raise AlternativeError("PIT_MARGINAL_MISMATCH", fitted_residuals.marginal_method)
        match method:
            case "schaake_window" | "schaake_block" | "ecc_q":
                pass
            case "decc_path_shrunk_error" | "residual_gaussian_copula":
                if fitted_residuals is None:
                    raise AlternativeError("MISSING_RESIDUALS", method)
                dependence = correlation(fitted_residuals.residual_matrix)
            case "mbcp_annual" | "mbcr_annual" | "mbcn_annual":
                mapping = fit_map(method, forward(training.forecast_means, rain),
                                  forward(training.observations, rain), config.seed)
            case "otc_annual" | "dotc_annual":
                transport = fit_ot(method, forward(training.forecast_means, rain),
                                   forward(training.observations, rain),
                                   training.source_years, rain, tolerance=1e-9)
            case _:
                raise AlternativeError("UNKNOWN_JOINT_METHOD", method)
        model = AnnualJointModel(
            method_id=spec.id, algorithm=method, marginal_method=marginal_name,
            train_hash=training.train_hash,
            signature=tuple((t.product, t.variable, t.lead) for t in training.targets),
            source_years=training.source_years, rain=rain,
            observed_template=training.observations.copy(),
            training_mean=np.mean(training.observations, axis=0),
            training_scale=np.maximum(1.0, np.std(training.observations, axis=0, ddof=1)),
            residuals=fitted_residuals, dependence=dependence, mapping=mapping, transport=transport,
        )
        return JointFitResult(
            method_id=spec.id, status=FitStatus.OK, fitted_model=model,
            diagnostics=FitDiagnostics(
                convergence=True, n_rows=len(training.source_years),
                n_years=len(training.source_years), train_hash=training.train_hash,
                elapsed_seconds=time.perf_counter() - started,
                message="Fixed section-8 annual predictive adaptation; no target truth used.",
            ),
        )
    except (AlternativeError, ValueError, np.linalg.LinAlgError) as error:
        code = error.code if isinstance(error, AlternativeError) else "JOINT_NUMERICAL_FAILURE"
        status = FitStatus.FIT_FAILED
        if code.startswith(("G3", "G6", "DECC_REQUIRES")):
            status = FitStatus.GATED_DATA
        elif code.startswith("INSUFFICIENT"):
            status = FitStatus.INSUFFICIENT_TRAINING
        elif code.startswith(("JOINT_", "MISALIGNED", "INCOMPLETE", "NEGATIVE", "NONPREQUENTIAL")):
            status = FitStatus.INPUT_CONFLICT
        return JointFitResult(
            method_id=spec.id, status=status, fitted_model=None, reason_code=code,
            diagnostics=FitDiagnostics(
                n_rows=len(training.source_years), n_years=len(training.source_years),
                train_hash=training.train_hash, elapsed_seconds=time.perf_counter() - started,
                message=str(error),
            ),
        )


def predict_joint(
    model: JointModel, targets: tuple[CaseInput, ...],
    marginals: tuple[PredictiveDistribution, ...], config: FitConfig,
) -> JointPrediction:
    return model.predict(targets, marginals, config)
