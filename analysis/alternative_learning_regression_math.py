"""Exact log-score derivatives and weighted small learners for regression."""

from __future__ import annotations

from math import exp, log, log1p, pi, sqrt

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize, minimize_scalar
from scipy.special import expit, gammaln

from analysis.calibration import FloatArray


def score_gradient(
    y: FloatArray, eta: FloatArray, rain: bool, shape: float,
) -> tuple[FloatArray, FloatArray]:
    """Negative log score and its ordinary link-coordinate gradient per row."""
    if not rain:
        residual = y - eta[:, 0]
        inverse_variance = np.exp(-2 * eta[:, 1])
        loss = .5 * log(2 * pi) + eta[:, 1] + .5 * residual**2 * inverse_variance
        return loss, np.column_stack((-residual * inverse_variance,
                                      1 - residual**2 * inverse_variance))
    zero = np.equal(y, 0)
    wet: NDArray[np.bool_] = ~zero
    ratio = y * np.exp(-eta[:, 1])
    positive_loss: FloatArray = (shape * eta[:, 1] + shape * ratio
                     - (shape - 1) * np.log(np.where(wet, y, 1))
                     - shape * log(shape) + gammaln(shape))
    loss = np.asarray(np.logaddexp(0, eta[:, 0]) - zero * eta[:, 0] + wet * positive_loss)
    gradient = np.column_stack((expit(eta[:, 0]) - zero, wet * shape * (1 - ratio)))
    return loss, gradient


def natural_gradient(
    eta: FloatArray, gradient: FloatArray, rain: bool, shape: float,
) -> tuple[FloatArray, int]:
    """Expected Fisher inverse, NOT the empirical squared-score approximation."""
    if rain:
        p0 = expit(eta[:, 0])
        fisher = np.column_stack((p0 * (1 - p0), (1 - p0) * shape))
    else:
        fisher = np.column_stack((np.exp(-2 * eta[:, 1]), np.full(len(eta), 2.)))
    clipped = int(np.count_nonzero(fisher < 1e-10))
    return gradient / np.maximum(fisher, 1e-10), clipped


def penalized_boost_score(
    y: FloatArray, eta: FloatArray, weights: FloatArray, rain: bool, shape: float,
) -> tuple[float, FloatArray]:
    """Regularize the occurrence intercept (weighted mean additive predictor).

    Decomposing each stump into a weighted-centered tree plus a constant makes
    this the intercept penalty, without penalizing centered tree contrasts.
    """
    losses, gradient = score_gradient(y, eta, rain, shape)
    value = np.sum(weights * losses).item()
    if rain:
        intercept = float(np.average(eta[:, 0], weights=weights))
        value += .125 * intercept**2
        gradient[:, 0] += .25 * intercept / weights.sum()
    return value, gradient


def initial_fit(y: FloatArray, weights: FloatArray, rain: bool) -> tuple[FloatArray, float]:
    """Climate fit with finite penalized occurrence even for all-wet data."""
    if not rain:
        mean = float(np.average(y, weights=weights))
        variance = float(np.average((y - mean)**2, weights=weights))
        sigma = max(sqrt(variance), 1e-4)
        return np.array([mean, log(sigma)]), 1.
    wet = np.greater(y, 0)
    mean = float(np.average(y[wet], weights=weights[wet])) if np.any(wet) else 1.
    def shape_objective(logshape: float) -> float:
        k = exp(logshape)
        loss = (k * log(mean) + k * y[wet] / mean - (k - 1) * np.log(y[wet])
                - k * log(k) + gammaln(k))
        return np.sum(weights[wet] * loss).item()
    shape = 1.
    if np.any(wet):
        fitted = minimize_scalar(shape_objective, bounds=(-8., 8.), method="bounded")
        if not fitted.success:
            raise ValueError(str(fitted.message))
        shape = exp(fitted.x)
    def occurrence(a: FloatArray) -> tuple[float, FloatArray]:
        link = a.item(0)
        softplus = max(link, 0.) + log1p(exp(-abs(link)))
        loss = np.sum(weights * (softplus - (~wet) * link)).item() + .125*link**2
        grad = np.sum(weights * (expit(a).item(0) - (~wet))).item() + .25*link
        return loss, np.array([grad])
    occurrence_fit = minimize(occurrence, np.array([0.]), jac=True,
                              bounds=[(-12., 12.)], method="L-BFGS-B")
    if not occurrence_fit.success:
        raise ValueError(str(occurrence_fit.message))
    return np.array([occurrence_fit.x.item(0), log(mean)]), shape


def expanded_features(x: FloatArray, square_center: float) -> FloatArray:
    """Eight contracted features plus centered mean square and harmonic two."""
    return np.column_stack((x, x[:, 0]**2 - square_center,
                            2*x[:, 2]*x[:, 3], x[:, 3]**2-x[:, 2]**2))


def bound_links(eta: FloatArray, rain: bool) -> tuple[FloatArray, int]:
    bounded = eta.copy()
    bounded[:, 1] = np.clip(bounded[:, 1], -12., 12.)
    if rain:
        bounded[:, 0] = np.clip(bounded[:, 0], -12., 12.)
    different = np.not_equal(eta, bounded)
    return bounded, int(np.count_nonzero(different))


def stump_fit(x: FloatArray, response: FloatArray, weights: FloatArray) -> tuple[int, float, float, float]:
    """Exact depth-one weighted CART, deterministic feature/threshold ties."""
    total_weight = weights.sum()
    total_response = np.sum(weights * response).item()
    mean = total_response / total_weight
    best = (-1, 0., mean, mean)
    best_gain = 0.
    for feature in range(np.size(x, 1)):
        order = np.argsort(x[:, feature], kind="stable")
        values, w, z = np.take(x[:, feature], order), weights[order], response[order]
        cw, cz = np.cumsum(w)[:-1], np.cumsum(w*z)[:-1]
        valid = np.less(values[:-1], values[1:]) & (cw > 0) & (cw < total_weight)
        gain = cz**2 / np.maximum(cw, 1e-30)
        gain += (total_response-cz)**2 / np.maximum(total_weight-cw, 1e-30)
        gain -= total_response**2 / total_weight
        gain[~valid] = -np.inf
        if not len(gain):
            continue
        split = int(np.argmax(gain))
        if gain[split] > best_gain:
            best_gain = gain.item(split)
            best = (feature, (values.item(split)+values.item(split+1))/2,
                    cz.item(split)/cw.item(split),
                    (total_response-cz.item(split))/(total_weight-cw.item(split)))
    return best


def stump_predict(x: FloatArray, stump: tuple[int, float, float, float]) -> FloatArray:
    feature, threshold, left, right = stump
    if feature < 0:
        return np.full(len(x), left)
    return np.where(x[:, feature] <= threshold, left, right)
