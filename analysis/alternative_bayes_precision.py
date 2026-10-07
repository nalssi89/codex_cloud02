"""Posterior predictive probability, mean and CRPS Monte Carlo precision gates."""

from __future__ import annotations

import math
from typing import Protocol

import numpy as np
from scipy.special import ndtr

from analysis.alternative_bayes_diagnostics import diagnose, mcse
from analysis.alternative_bayes_distribution_transforms import forward, inverse
from analysis.alternative_bayes_sampler import MixtureDraws, importance_report
from analysis.calibration import FloatArray
from analysis.data_io import Json


class ScalarPrecisionParameters(Protocol):
    @property
    def locations(self) -> FloatArray: ...
    @property
    def scales(self) -> FloatArray: ...
    @property
    def weights(self) -> FloatArray: ...
    @property
    def transform(self) -> str: ...
    @property
    def chain_shape(self) -> tuple[int, int] | None: ...
    @property
    def training_sd(self) -> float | None: ...


def normal_moments(mu: FloatArray, variance: FloatArray, transform: str) -> FloatArray:
    """Original-unit first moments per Gaussian draw, not inverse of its mean."""
    if transform == "temperature":
        return 10 + 10 * mu
    sd: FloatArray = np.sqrt(variance)
    a = mu / sd
    density: FloatArray = np.exp(-0.5 * a * a)
    density /= math.sqrt(2 * math.pi)
    probability: FloatArray = ndtr(a)
    first = mu * probability + sd * density
    second = (mu * mu + variance) * probability + mu * sd * density
    if transform == "sqrt":
        return 100 * second
    if transform == "yj":
        return 100 * (first + second / 4)
    # Smooth tail integration avoids Hermite's non-smooth censor-boundary error.
    nodes, weights = np.polynomial.legendre.leggauss(96)
    u = (nodes + 1) / 2
    z = u / (1 - u)
    derivative: FloatArray = np.exp(-2 * (z + math.log(math.sinh(1))))
    derivative = 100 / np.sqrt(1 + derivative)
    result = np.zeros(mu.shape)
    for point, weight, jac in zip(z.flat, weights.flat, derivative.flat, strict=True):
        survival: FloatArray = ndtr((mu - point) / sd)
        result += weight / (2 * (1 - point / (1 + point)) ** 2) * jac * survival
    return result


def crps_influence(
    mu: FloatArray, sd: FloatArray, weights: FloatArray, transform: str,
    thresholds: FloatArray, nodes_count: int = 128,
) -> FloatArray:
    """Functional delta-method influence of the ACTUAL mixture CRPS at probes."""
    nodes, gauss_weights = np.polynomial.legendre.leggauss(nodes_count)
    u = (nodes + 1) / 2
    if transform == "temperature":
        z: FloatArray = np.tan(np.pi * (u - 0.5))
        jacobian = 10 * np.pi * (1 + z * z)
    else:
        z = u / (1 - u)
        jacobian = 1 / ((1 - u) * (1 - u))
        if transform == "sqrt":
            jacobian *= 200 * z
        elif transform == "yj":
            jacobian *= 100 + 50 * z
        else:
            exponent: FloatArray = np.exp(-2 * (z + math.log(math.sinh(1))))
            jacobian *= 100 / np.sqrt(1 + exponent)
    physical = inverse(z, transform)
    result = np.zeros((*mu.shape, thresholds.size))
    quadrature_weights = gauss_weights * jacobian / 2
    for point, value, quadrature_weight in zip(
        z.flat, physical.flat, quadrature_weights.flat, strict=True
    ):
        component: FloatArray = ndtr((point - mu) / sd)
        mixture_cdf = float(np.sum(weights * component))
        factors = 2 * (mixture_cdf - np.greater_equal(value, thresholds))
        result += quadrature_weight * (
            (component - mixture_cdf)[..., None] * factors
        )
    return result


def predictive_report(
    draws: MixtureDraws, transforms: tuple[str, ...], observations: FloatArray,
) -> dict[str, Json]:
    weights = draws.weights()
    importance = importance_report(draws)
    # SNIS estimator influences include N*w, not an iid weighted-ESS fiction.
    multiplier = weights * weights.size
    mean_errors: list[Json] = []
    probability_errors: list[Json] = []
    crps_errors: list[Json] = []
    quadrature_errors: list[Json] = []
    zero_monitors: list[FloatArray] = []
    passed = True
    for j, transform in enumerate(transforms):
        mu = draws.locations[..., j]
        variance = draws.covariances[..., j, j]
        sd = np.sqrt(variance)
        mean = normal_moments(mu, variance, transform)
        weighted_mean = float(np.sum(weights * mean))
        mean_error = mcse((multiplier * (mean - weighted_mean))[..., None]).item(0)
        probes = np.quantile(observations[:, j], [1 / 3, 1 / 2, 2 / 3])
        latent_probes = forward(probes, transform)
        probability: FloatArray = ndtr(
            (latent_probes[None, None, :] - mu[..., None]) / sd[..., None]
        )
        if transform != "temperature":
            zero = ndtr(-mu / sd)
            zero_monitors.append(zero[..., None])
            probability = np.concatenate((zero[..., None], probability), axis=-1)
        centered = probability - np.sum(weights[..., None] * probability, axis=(0, 1))
        probability_error = float(np.max(mcse(multiplier[..., None] * centered)))
        influence = crps_influence(mu, sd, weights, transform, probes)
        refined = crps_influence(mu, sd, weights, transform, probes, 256)
        crps_error = float(np.max(mcse(multiplier[..., None] * refined)))
        quadrature_difference: FloatArray = np.abs(mcse(
            multiplier[..., None] * (refined - influence)
        ))
        quadrature_error = float(np.max(quadrature_difference))
        training_sd = float(np.std(observations[:, j], ddof=1))
        passed &= (
            mean_error <= 0.01 * training_sd and probability_error <= 0.005
            and crps_error <= 0.005 * training_sd
            and quadrature_error <= 0.0005 * training_sd
        )
        mean_errors.append(mean_error)
        probability_errors.append(probability_error)
        crps_errors.append(crps_error)
        quadrature_errors.append(quadrature_error)
    monitored = np.concatenate((draws.monitors, *zero_monitors), axis=-1)
    diagnostics = diagnose(monitored)
    return {
        **diagnostics, **importance, "predictive_mcse_passed": bool(passed),
        "mean_mcse": mean_errors, "probability_mcse": probability_errors,
        "crps_mcse": crps_errors, "crps_mcse_quadrature_difference": quadrature_errors,
        "crps_mcse_probes": "training terciles and median; no target truth",
        "chains": 4, "warmup_per_chain": 1024,
        "retained_per_chain": np.size(draws.locations, axis=1),
    }


def score_crps_precision(
    distribution: ScalarPrecisionParameters, observation: float,
) -> tuple[float, float, bool]:
    """Truth is allowed only at scoring, never to fit or condition a posterior.

    Fit-time tercile/median probes cannot certify an unseen score. This final
    observation-specific influence check is invoked by the issued law's CRPS.
    """
    if distribution.chain_shape is None or distribution.training_sd is None:
        return 0.0, 0.0, True
    shape = distribution.chain_shape
    mu = distribution.locations.reshape(shape)
    sd = distribution.scales.reshape(shape)
    weights = distribution.weights.reshape(shape)
    multiplier = (weights * weights.size)[..., None]
    probe = np.asarray([observation])
    influence = crps_influence(mu, sd, weights, distribution.transform, probe)
    refined = crps_influence(mu, sd, weights, distribution.transform, probe, 256)
    error = mcse(multiplier * (refined - influence)).item(0)
    estimate = mcse(multiplier * refined).item(0)
    return estimate, error, (
        estimate <= 0.005 * distribution.training_sd
        and error <= 0.0005 * distribution.training_sd
    )
