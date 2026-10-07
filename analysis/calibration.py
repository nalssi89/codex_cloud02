"""Equal-year empirical mapping and CRPS-fitted Gaussian EMOS calibration.

Only historical observations enter calibration; there is no target observation.
Rainfall EMOS describes the latent normal before left censoring at zero.
"""

from dataclasses import dataclass
from math import pi, sqrt

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize
from scipy.special import ndtr
from scipy.stats import rankdata

FloatArray = NDArray[np.float64]
_SQRT_PI = sqrt(pi)
_SQRT_TWO = sqrt(2.0)


@dataclass(frozen=True, slots=True)
class CalibrationResult:
    qm: FloatArray
    qdm: FloatArray
    mu: float
    sigma: float
    parameters: tuple[float, float, float, float]
    converged: bool
    fit_crps: float
    initial_crps: float
    dry_exceptions: int
    optimizer_message: str


def _ensemble(values: FloatArray, name: str, minimum: int = 1) -> FloatArray:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 1 or array.size < minimum or not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must be a finite 1-D array of at least {minimum} values")
    return array


def normal_pdf(values: FloatArray) -> FloatArray:
    """Standard normal density."""
    return np.exp(-0.5 * np.square(values)) / sqrt(2.0 * pi)


def empirical_crps(values: FloatArray, observation: float) -> float:
    """Exact CRPS of an equally weighted discrete ensemble."""
    sample = np.sort(_ensemble(values, "values"))
    if not np.isfinite(observation):
        raise ValueError("observation must be finite")
    n = sample.size
    coefficients = 2.0 * np.arange(1, n + 1) - n - 1.0
    return float(np.abs(sample - observation).mean() - (coefficients * sample).sum() / n**2)


def gaussian_crps(
    mu: FloatArray,
    sigma: FloatArray,
    observed: FloatArray,
    censored: bool = False,
) -> FloatArray:
    """Exact normal or zero-left-censored normal CRPS, with broadcasting."""
    location, spread, actual = np.broadcast_arrays(
        np.asarray(mu, dtype=np.float64),
        np.asarray(sigma, dtype=np.float64),
        np.asarray(observed, dtype=np.float64),
    )
    if (
        not np.all(np.isfinite(location))
        or not np.all(np.isfinite(spread))
        or not np.all(np.isfinite(actual))
        or np.any(spread <= 0.0)
    ):
        raise ValueError("mu and observed must be finite, and sigma finite and positive")
    if censored and np.any(actual < 0.0):
        raise ValueError("censored observations must be nonnegative")
    z = (actual - location) / spread
    score = spread * (z * (2.0 * ndtr(z) - 1.0) + 2.0 * normal_pdf(z) - 1.0 / _SQRT_PI)
    if censored:
        a0 = -location / spread
        probability = ndtr(a0)
        integral = (
            a0 * probability**2
            + 2.0 * probability * normal_pdf(a0)
            - ndtr(_SQRT_TWO * a0) / _SQRT_PI
        )
        score = score - spread * integral
    return np.asarray(score, dtype=np.float64)


def _distribution(values: FloatArray, weights: FloatArray) -> tuple[FloatArray, FloatArray]:
    """Merge ties and assign their total mass's midpoint probability."""
    order = np.argsort(values, kind="stable")
    ordered = values[order]
    unique, starts = np.unique(ordered, return_index=True)
    ends = np.append(starts[1:], ordered.size) - 1
    cumulative = np.cumsum(weights[order])
    mass = np.diff(np.concatenate((np.zeros(1), cumulative[ends])))
    mass = mass / mass.sum()
    positions = np.cumsum(mass) - 0.5 * mass
    return unique, positions


def _objective(
    parameters: FloatArray, means: FloatArray, variances: FloatArray,
    observed: FloatArray, censored: bool,
) -> tuple[float, FloatArray]:
    a, b, c, d = (float(value) for value in parameters.flat)
    mu = a + b * means
    sigma = np.sqrt(c + d * variances)
    z = (observed - mu) / sigma
    grad_mu = 1.0 - 2.0 * ndtr(z)
    grad_sigma = 2.0 * normal_pdf(z) - 1.0 / _SQRT_PI
    if censored:
        a0 = -mu / sigma
        probability = ndtr(a0)
        grad_mu = grad_mu + probability**2
        grad_sigma = (
            grad_sigma - 2.0 * probability * normal_pdf(a0)
            + ndtr(_SQRT_TWO * a0) / _SQRT_PI
        )
    grad_variance = grad_sigma / (2.0 * sigma)
    gradient = np.array(
        [grad_mu.mean(), (grad_mu * means).mean(),
         grad_variance.mean(), (grad_variance * variances).mean()],
        dtype=np.float64,
    )
    return float(gaussian_crps(mu, sigma, observed, censored).mean()), gradient


def calibrate(
    forecast: FloatArray,
    historical: tuple[FloatArray, ...],
    observations: FloatArray,
    precipitation: bool,
) -> CalibrationResult:
    """Fit equal-year QM, QDM and EMOS using historical years only.

    Historical years can have different member counts, but each must contain
    two members for its sample variance. The target may contain one member;
    its variance is then zero.
    """
    target = _ensemble(forecast, "forecast")
    actual = _ensemble(observations, "observations")
    if len(historical) != actual.size:
        raise ValueError("historical must contain one ensemble per observation")
    years = tuple(_ensemble(year, "historical ensemble", 2) for year in historical)
    if precipitation and (
        np.any(target < 0.0) or np.any(actual < 0.0)
        or any(np.any(year < 0.0) for year in years)
    ):
        raise ValueError("rainfall inputs must be nonnegative")

    values = np.concatenate(years)
    weights = np.concatenate(
        [np.full(year.size, 1.0 / (len(years) * year.size)) for year in years]
    )
    historical_values, historical_positions = _distribution(values, weights)
    observed_values, observed_positions = _distribution(
        actual, np.full(actual.size, 1.0 / actual.size)
    )
    probabilities = np.interp(target, historical_values, historical_positions)
    qm = np.interp(probabilities, observed_positions, observed_values)
    ranks = (rankdata(target, method="average") - 0.5) / target.size
    observed_quantiles = np.interp(ranks, observed_positions, observed_values)
    historical_quantiles = np.interp(ranks, historical_positions, historical_values)
    dry_exceptions = 0
    if precipitation:
        dry = historical_quantiles < 0.1
        dry_exceptions = int(np.count_nonzero(dry))
        qdm = observed_quantiles.copy()
        wet = ~dry
        qdm[wet] = target[wet] * observed_quantiles[wet] / historical_quantiles[wet]
        qm = np.maximum(qm, 0.0)
        qdm = np.maximum(qdm, 0.0)
    else:
        qdm = target + observed_quantiles - historical_quantiles

    scale = max(float(actual.std()), 0.1 if precipitation else 1.0)
    shift = 0.0 if precipitation else float(actual.mean())
    scaled_observed = (actual - shift) / scale
    means = np.array([(float(year.mean()) - shift) / scale for year in years])
    variances = np.array([float(year.var(ddof=1)) / scale**2 for year in years])
    residual = scaled_observed - means
    starts = (
        np.array([residual.mean(), 1.0,
                  max(float(residual.var() - variances.mean()), 1e-6), 1.0]),
        np.array([scaled_observed.mean(), 0.0,
                  max(float(scaled_observed.var()), 1e-6), 0.0]),
    )
    initial_scores = [
        _objective(start, means, variances, scaled_observed, precipitation)[0]
        for start in starts
    ]
    best_initial = int(np.argmin(initial_scores))
    best_parameters = starts[best_initial].copy()
    best_score = initial_scores[best_initial]
    successful = False
    messages: list[str] = []
    for start in starts:
        result = minimize(
            _objective, start,
            args=(means, variances, scaled_observed, precipitation),
            method="L-BFGS-B", jac=True,
            bounds=((None, None), (0.0, None), (1e-6, None), (0.0, None)),
            options={"maxiter": 2000, "maxls": 50, "ftol": 1e-12, "gtol": 1e-8},
        )
        messages.append(str(result.message))
        if (
            result.success and np.isfinite(result.fun) and np.all(np.isfinite(result.x))
            and float(result.fun) <= best_score
        ):
            best_parameters = np.asarray(result.x, dtype=np.float64)
            best_score = float(result.fun)
            successful = True

    a, b, c, d = (float(value) for value in best_parameters)
    parameters = (shift + scale * a - b * shift, b, scale**2 * c, d)
    target_mean = float(target.mean())
    target_variance = float(target.var(ddof=1)) if target.size > 1 else 0.0
    mu = parameters[0] + parameters[1] * target_mean
    sigma = sqrt(parameters[2] + parameters[3] * target_variance)
    if not successful:
        messages.append("No successful finite fit improved the best initialization; initialization retained")
    return CalibrationResult(
        qm=np.asarray(qm, dtype=np.float64),
        qdm=np.asarray(qdm, dtype=np.float64),
        mu=mu, sigma=sigma, parameters=parameters, converged=successful,
        fit_crps=scale * best_score,
        initial_crps=scale * initial_scores[best_initial],
        dry_exceptions=dry_exceptions, optimizer_message="; ".join(messages),
    )
