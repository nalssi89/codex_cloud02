"""Section-seven ridge, componentwise, and genuine natural-gradient fits."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log
from time import perf_counter

import numpy as np
from scipy.optimize import minimize
from scipy.special import digamma, expit

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FeatureSpec,
    FitConfig,
    FitDiagnostics,
    FittedModel,
    PredictiveDistribution,
    TrainingSet,
)
from analysis.alternative_data import features_for_case, features_for_training
from analysis.alternative_distributions import gamma, hurdle, normal
from analysis.alternative_learning_regression_math import (
    bound_links,
    expanded_features,
    initial_fit,
    natural_gradient,
    penalized_boost_score,
    score_gradient,
    stump_fit,
    stump_predict,
)
from analysis.calibration import FloatArray
from analysis.data_io import Json


@dataclass(frozen=True, slots=True)
class RegressionModel:
    method_id: str
    rain: bool
    feature_spec: FeatureSpec
    square_center: float
    intercept: FloatArray
    coefficients: FloatArray
    shape: float
    stumps: tuple[tuple[int, tuple[int, float, float, float], float], ...] = ()

    def predict(self, target: CaseInput) -> PredictiveDistribution:
        if (target.variable == "prcp") != self.rain:
            raise AlternativeError("INPUT_CONFLICT", "regression variable mismatch")
        base = features_for_case(target, self.feature_spec)[None, :]
        x = expanded_features(base, self.square_center)
        eta = self.intercept[None, :] + x @ self.coefficients
        for component, stump, rate in self.stumps:
            eta[:, component] += rate * stump_predict(base, stump)
            eta, _ = bound_links(eta, self.rain)
        if self.method_id == "ngboost_small":
            eta, _ = bound_links(eta, self.rain)
        if self.rain:
            return hurdle(expit(eta[:, 0]).item(0), gamma(self.shape, exp(eta.item(0, 1))/self.shape))
        return normal(eta.item(0, 0), exp(eta.item(0, 1)))

    def to_spec(self) -> dict[str, Json]:
        return {
            "kind": "distribution_regression", "method_id": self.method_id,
            "rain": self.rain, "square_center": self.square_center,
            "intercept": self.intercept.tolist(), "coefficients": self.coefficients.tolist(),
            "shape": self.shape,
            "links": ["logit_p0", "log_positive_mean"] if self.rain else ["identity_mu", "log_sigma"],
            "stumps": [{"component": c, "feature": s[0], "threshold": s[1],
                        "left": s[2], "right": s[3], "rate": r} for c, s, r in self.stumps],
            "feature_spec": {"names": list(self.feature_spec.names),
                             "center": self.feature_spec.center.tolist(),
                             "scale": self.feature_spec.scale.tolist(),
                             "predictor_power": self.feature_spec.predictor_power},
        }


def _ridge(
    x: FloatArray, y: FloatArray, weights: FloatArray, rain: bool,
    intercept: FloatArray, shape: float,
) -> tuple[FloatArray, float, bool, float]:
    design = np.column_stack((np.ones(len(x)), x))
    initial = np.zeros((design.shape[1], 2))
    initial[0] = intercept
    penalty = np.full(initial.shape, .5)
    if rain:
        penalty[0, 0] = .125
    def objective(parameters: FloatArray) -> tuple[float, FloatArray]:
        coefficients = parameters[:initial.size].reshape(initial.shape)
        k = exp(parameters.item(-1)) if rain else shape
        eta = design @ coefficients
        loss, gradient = score_gradient(y, eta, rain, k)
        value = np.sum(weights * loss).item() + np.sum(penalty * coefficients**2).item()
        grad = (design.T @ (weights[:, None]*gradient) + 2*penalty*coefficients).ravel()
        if rain:
            wet = np.greater(y, 0)
            positive_link = eta[:, 1][wet]
            derivative = k * (positive_link + y[wet]*np.exp(-positive_link)
                              - np.log(y[wet]) - log(k) - 1 + digamma(k))
            grad = np.concatenate((grad, np.array([np.sum(weights[wet] * derivative).item()])))
        return value, grad
    start = initial.ravel()
    bounds: list[tuple[float | None, float | None]] = [(None, None)] * len(start)
    # Bounds apply only to climate links; coefficient penalization controls slopes.
    bounds[1] = (-12., 12.)
    if rain:
        bounds[0] = (-12., 12.)
        start = np.concatenate((start, np.array([log(shape)])))
        bounds.append((-8., 8.))
    fitted = minimize(objective, start, jac=True, method="L-BFGS-B", bounds=bounds,
                      options={"maxiter": 500, "ftol": 1e-10, "gtol": 1e-6})
    if not np.isfinite(fitted.fun) or not np.all(np.isfinite(fitted.x)):
        raise AlternativeError("FIT_FAILED", "nonfinite ridge likelihood")
    if not fitted.success:
        raise AlternativeError("FIT_FAILED", f"ridge nonconvergence: {fitted.message}")
    coefficients = fitted.x[:initial.size].reshape(initial.shape)
    shape = exp(fitted.x.item(-1)) if rain else shape
    return coefficients, shape, bool(fitted.success), float(fitted.fun)


def fit_regression(
    method_id: str, training: TrainingSet, config: FitConfig,
) -> tuple[FittedModel, FitDiagnostics]:
    """Fit the fixed inventory with training-only features and year weights."""
    started = perf_counter()
    if method_id not in ("gamlss_ridge", "componentwise_boost", "ngboost_small"):
        raise AlternativeError("INPUT_CONFLICT", f"unknown regression method {method_id}")
    base, feature_spec = features_for_training(training)
    y = np.array([row.observation for row in training.rows], dtype=np.float64)
    weights = training.year_weights
    rain = training.target.variable == "prcp"
    try:
        intercept, shape = initial_fit(y, weights, rain)
    except ValueError as error:
        raise AlternativeError("FIT_FAILED", str(error)) from error
    square_center = float(np.average(base[:, 0]**2, weights=weights))
    x = expanded_features(base, square_center)
    coefficients = np.zeros((np.size(x, 1), 2))
    eta = np.tile(intercept, (len(y), 1))
    stumps: list[tuple[int, tuple[int, float, float, float], float]] = []
    clipping = 0
    unsupported_features = tuple(j for j in range(np.size(x, 1))
                                 if np.sum(weights*x[:, j]**2).item()
                                 <= weights.sum()*config.numerical_tolerance**2)
    converged = True
    objective = np.sum(weights * score_gradient(y, eta, rain, shape)[0]).item()
    def boost_objective(candidate: FloatArray) -> float:
        value = np.sum(weights * score_gradient(y, candidate, rain, shape)[0]).item()
        if rain and method_id == "ngboost_small":
            value = penalized_boost_score(y, candidate, weights, rain, shape)[0]
        return value
    if method_id == "gamlss_ridge":
        fitted, shape, converged, objective = _ridge(
            x, y, weights, rain, intercept, shape,
        )
        intercept, coefficients = fitted[:1].reshape(-1), fitted[1:]
        eta = intercept[None, :] + x @ coefficients
    else:
        for _ in range(100):
            loss, gradient = score_gradient(y, eta, rain, shape)
            if method_id == "componentwise_boost":
                best_value = np.sum(weights * loss).item()
                best = None
                for component in range(2):
                    for feature in range(np.size(x, 1)):
                        if feature == 8:  # Squared ensemble mean is GAMLSS-only.
                            continue
                        if feature in unsupported_features:
                            continue  # A numerically null column has no identifiable slope.
                        denominator = np.sum(weights * x[:, feature]**2).item()
                        slope = -np.sum(weights*x[:, feature]*gradient[:, component]).item() / max(denominator, 1e-30)
                        candidate = eta.copy()
                        candidate[:, component] += .05*slope*x[:, feature]
                        value = np.sum(weights * score_gradient(y, candidate, rain, shape)[0]).item()
                        if value < best_value:
                            best_value, best = value, (component, feature, slope, candidate)
                if best is not None:
                    component, feature, slope, eta = best
                    coefficients[feature, component] += .05*slope
            else:
                _, gradient = penalized_boost_score(y, eta, weights, rain, shape)
                natural, clipped = natural_gradient(eta, gradient, rain, shape)
                clipping += clipped
                pair = [stump_fit(base, -natural[:, c], weights) for c in range(2)]
                update = np.column_stack([stump_predict(base, s) for s in pair])
                candidates: list[float] = []
                for scalar in (1., .5, .25, .125, .0625):
                    trial, _ = bound_links(eta + scalar*update, rain)
                    candidates.append(boost_objective(trial))
                scalar = (1., .5, .25, .125, .0625)[int(np.argmin(candidates))]
                eta, clipped = bound_links(eta + .05*scalar*update, rain)
                clipping += clipped
                stumps.extend((c, pair[c], .05*scalar) for c in range(2))
        objective = boost_objective(eta)
    if not np.isfinite(objective):
        raise AlternativeError("FIT_FAILED", "nonfinite regression objective")
    fitted_model = RegressionModel(method_id, rain, feature_spec, square_center, intercept,
                                   coefficients, shape, tuple(stumps))
    return fitted_model, FitDiagnostics(
        objective=objective, convergence=converged, n_rows=len(y),
        n_years=len({row.source_year for row in training.rows}), train_hash=training.train_hash,
        parameter_count=24 + int(rain) if method_id == "gamlss_ridge" else (
            2 + int(rain) + (len(stumps)*4 if stumps else int(np.count_nonzero(coefficients)))),
        boundary_flags=((f"link_or_fisher_clipping:{clipping}",) if clipping else ()) +
                       ((f"null_training_features:{unsupported_features}",) if
                        method_id == "componentwise_boost" and unsupported_features else ()) +
                       (("gamma_shape_bound",) if rain and (shape > exp(7.99) or shape < exp(-7.99)) else ()) +
                       (("all_dry_intensity_unidentified",) if rain and not np.any(np.greater(y, 0)) else ()),
        elapsed_seconds=perf_counter()-started,
        message="Joint penalized likelihood" if method_id == "gamlss_ridge" else
                "100 fixed iterations at 0.05; fixed positive shape; no target stopping",
    )
