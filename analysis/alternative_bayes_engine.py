"""One proper posterior engine for scalar, trend and full-path Bayesian fits."""

from __future__ import annotations

import numpy as np

from analysis.alternative_bayes_algebra import condition, update
from analysis.alternative_bayes_distribution import forward
from analysis.alternative_bayes_models import ConditionalLaw, target_key
from analysis.alternative_bayes_precision import predictive_report
from analysis.alternative_bayes_sampler import (
    importance_report,
    posterior_failure,
    run_chains,
)
from analysis.alternative_contracts import CaseInput, FitConfig
from analysis.calibration import FloatArray
from analysis.data_io import Json


def transformed_matrix(values: FloatArray, transforms: tuple[str, ...]) -> FloatArray:
    return np.column_stack([
        forward(values[:, j], transform) for j, transform in enumerate(transforms)
    ])


def fit_law(
    method: str, forecast: FloatArray, observations: FloatArray,
    years: FloatArray, targets: tuple[CaseInput, ...], train_hash: str,
    config: FitConfig,
) -> ConditionalLaw:
    """Condition the integrated JOINT predictive, never its unweighted cut."""
    transforms = tuple(
        "temperature" if t.variable == "t15m" else
        "yj" if method == "bjp_yj_fixed" else
        "logsinh" if method == "bjp_logsinh_fixed" else "sqrt"
        for t in targets
    )
    x = transformed_matrix(forecast, transforms)
    y = transformed_matrix(observations, transforms)
    issued = np.asarray([[float(t.members.mean()) for t in targets]])
    predictor = transformed_matrix(issued, transforms).ravel()
    values = np.column_stack((x, y))
    design = np.ones((np.size(values, axis=0), 1))
    prior_variances = np.ones(1)
    target_design = np.ones(1)
    rain_mask = np.asarray([s != "temperature" for s in transforms] * 2)
    censor = np.asarray(np.logical_and(np.equal(values, 0), rain_mask), dtype=float)
    target_censor = np.asarray(
        np.logical_and(np.equal(predictor, 0), rain_mask[:predictor.size]), dtype=float
    )
    nig = method == "bayesian_anomaly_ridge"
    if method in {"bjp_t", "bjp_ti"}:
        design = np.column_stack((design, (years - 2000) / 10))
        target_design = np.asarray([1.0, (targets[0].valid_start.year - 2000) / 10])
        prior_variances = np.asarray([1.0, 4.0 if method == "bjp_t" else 0.04])
    elif nig:
        design = np.column_stack((design, x[:, 0]))
        target_design = np.asarray([1.0, predictor.item(0)])
        prior_variances = np.asarray([4.0, 1.0])
        values = y
        censor = censor[:, x.shape[1]:]
        predictor = np.empty(0)
        target_censor = np.empty(0)
    metadata: dict[str, Json] = {
        "seed": config.seed,
        "estimand": "conditional_regression" if nig else "joint_posterior_predictive_conditioning",
        "fixed_physical_prior": method != "joint_gaussian_plugin",
        "dimension": np.size(values, axis=1), "annual_vectors": np.size(values, axis=0),
        "censored_coordinates": int(np.count_nonzero(censor)),
        "training_response_sd": [
            float(np.std(observations[:, j], ddof=1)) for j in range(len(targets))
        ],
        "prior_iw_df": 8 if nig else np.size(values, axis=1) + 8,
        "prior_iw_scale_diagonal": 6 if nig else 7,
        "prior_row_variances": [float(v) for v in prior_variances.flat],
        "prior_dominance_df_fraction": float(
            (8 + (0 if nig else np.size(values, axis=1))) /
            (8 + (0 if nig else np.size(values, axis=1)) + np.size(values, axis=0))
        ),
    }
    if method == "joint_gaussian_plugin":
        for key in tuple(metadata):
            if key.startswith("prior_"):
                del metadata[key]
        metadata["estimand"] = "plugin_Gaussian_conditioning"
        center = values.mean(axis=0)
        scale = np.maximum(values.std(axis=0, ddof=1), 0.1)
        standardized = (values - center) / scale
        covariance = np.cov(standardized, rowvar=False)
        covariance = 0.9 * covariance + 0.1 * np.diag(np.diag(covariance))
        covariance += 1e-6 * np.eye(np.size(values, axis=1))
        covariance *= np.outer(scale, scale)
        df, location, matrix = condition(center, covariance, predictor, None)
        metadata.update({"algorithm": "non_Bayesian_plugin", "conjugate": False})
    elif not censor.any() and not target_censor.any():
        posterior = update(values, design, prior_variances, nig=nig)
        degrees, mean, student_scale = posterior.predictive(target_design)
        df, location, matrix = condition(mean, student_scale, predictor, degrees)
        metadata.update({
            "algorithm": "exact_conjugate", "conjugate": True,
            "student_matrix_is_scale_not_covariance": True,
            "posterior_iw_df": posterior.iw_df,
        })
    else:
        augmented = bool(target_censor.any())
        for attempt in range(2):
            stream = run_chains(
                values, design, prior_variances, target_design, predictor, censor,
                target_censor, f"{config.seed}:{method}:{train_hash}:{augmented}",
                nig=nig, augmented=augmented,
            )
            retry_augmented = False
            last_report: dict[str, Json] = {}
            for draws in stream:
                importance = importance_report(draws)
                if not augmented and not importance["importance_passed"]:
                    retry_augmented = True
                    break
                last_report = predictive_report(draws, transforms, observations)
                last_report["predictive_estimator"] = "residual_covariance_rao_blackwell_v1"
                last_report["marginalized_parameters"] = (
                    "matrix_normal_coefficients_and_cross_regression"
                )
                last_report["predictor_weight"] = (
                    "unit_augmented_target" if augmented else "integrated_student_density"
                )
                last_report["normal_components_per_retained_iteration"] = 1
                if last_report["passed"] and last_report["predictive_mcse_passed"]:
                    metadata.update(last_report)
                    metadata.update({
                        "algorithm": "coordinate_censored_Gibbs",
                        "conditioning": "augmented_target" if augmented else "importance_density",
                        "conjugate": False,
                    })
                    dimension = len(targets)
                    return ConditionalLaw(
                        method_id=method, train_hash=train_hash,
                        target_hash=target_key(targets), transforms=transforms,
                        locations=draws.locations.reshape(-1, dimension),
                        matrices=draws.covariances.reshape(-1, dimension, dimension),
                        weights=draws.weights().ravel(), df=None,
                        posterior_metadata=metadata,
                    )
            if retry_augmented and attempt == 0:
                augmented = True
                continue
            raise posterior_failure(last_report)
        raise AssertionError("Unreachable posterior budget")
    return ConditionalLaw(
        method_id=method, train_hash=train_hash, target_hash=target_key(targets),
        transforms=transforms, locations=location[None, :],
        matrices=matrix[None, :, :], weights=np.ones(1), df=df,
        posterior_metadata=metadata,
    )
