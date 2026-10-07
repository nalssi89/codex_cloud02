"""Registry entry points for the frozen pooled learning algorithms."""

from __future__ import annotations

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    CategoryFitResult,
    CategoryModel,
    CategoryPrediction,
    FitConfig,
    FitDiagnostics,
    FitResult,
    FitStatus,
    MethodSpec,
    TrainingSet,
)
from analysis.calibration import FloatArray

LEARNING_IDS = (
    "ordinal_logit", "elr_threshold_logit", "gamlss_ridge",
    "componentwise_boost", "ngboost_small", "qrf_year_forest",
    "idr_mean_order", "drn_small", "bqn_monotone",
)


def fit_learning(
    spec: MethodSpec, training: TrainingSet, config: FitConfig,
) -> FitResult | CategoryFitResult:
    category = spec.id in ("ordinal_logit", "elr_threshold_logit")
    result_type = CategoryFitResult if category else FitResult
    n_years = len({row.source_year for row in training.rows})
    diagnostic = FitDiagnostics(
        n_rows=len(training.rows), n_years=n_years, train_hash=training.train_hash,
    )
    if spec.id not in LEARNING_IDS:
        raise ValueError(f"Unknown learning method: {spec.id}")
    if n_years < 10:
        return result_type(
            method_id=spec.id, status=FitStatus.INSUFFICIENT_TRAINING,
            fitted_model=None, diagnostics=diagnostic, reason_code="FEWER_THAN_TEN_YEARS",
        )
    try:
        if category:
            from analysis.alternative_learning_category import fit_category

            model, diagnostics = fit_category(spec.id, training)
            return CategoryFitResult(
                method_id=spec.id, status=FitStatus.OK,
                fitted_model=model, diagnostics=diagnostics,
            )
        if spec.id in ("qrf_year_forest", "idr_mean_order"):
            from analysis.alternative_learning_order import fit_order

            continuous_model, diagnostics = fit_order(spec.id, training, config)
        elif spec.id in ("drn_small", "bqn_monotone"):
            from analysis.alternative_learning_neural import fit_neural

            continuous_model, diagnostics = fit_neural(spec.id, training, config)
        else:
            from analysis.alternative_learning_regression import fit_regression

            continuous_model, diagnostics = fit_regression(spec.id, training, config)
        return FitResult(
            method_id=spec.id, status=FitStatus.OK,
            fitted_model=continuous_model, diagnostics=diagnostics,
        )
    except AlternativeError as error:
        return result_type(
            method_id=spec.id, status=FitStatus(error.code), fitted_model=None,
            diagnostics=diagnostic, reason_code=error.detail,
        )


def predict_categories(
    model: CategoryModel, target: CaseInput, thresholds: FloatArray,
) -> CategoryPrediction:
    return model.predict(target, thresholds)
