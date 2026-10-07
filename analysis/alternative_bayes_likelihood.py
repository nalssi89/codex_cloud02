"""Observed censored Gaussian likelihood oracle for augmentation audits."""

from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad
from scipy.special import log_ndtr, ndtr
from scipy.stats import multivariate_normal

from analysis.calibration import FloatArray


def censored_loglikelihood(
    value: FloatArray, mean: FloatArray, covariance: FloatArray,
    censored: FloatArray, log_jacobian: float = 0.0,
) -> float:
    """Revealed-coordinate density times a CONDITIONAL joint rectangle.

    The <=2 censor-coordinate branch uses deterministic one-dimensional
    quadrature. Higher-dimensional rectangles use SciPy's randomized numerical
    integration with a fixed RNG, not independent marginal probabilities.
    Gibbs fitting itself does not need a numerical rectangle likelihood.
    """
    hidden = np.flatnonzero(censored)
    revealed = np.flatnonzero(np.equal(censored, 0))
    result = log_jacobian
    cm = mean[hidden]
    cc = covariance[np.ix_(hidden, hidden)]
    if revealed.size:
        block = covariance[np.ix_(revealed, revealed)]
        delta = value[revealed] - mean[revealed]
        diagonal: FloatArray = np.diag(np.linalg.cholesky(block))
        determinant = 2 * math.fsum(math.log(v) for v in diagonal.flat)
        result -= 0.5 * (
            revealed.size * math.log(2 * math.pi) + determinant
            + float(delta @ np.linalg.solve(block, delta))
        )
        cross = covariance[np.ix_(hidden, revealed)]
        cm = cm + cross @ np.linalg.solve(block, delta)
        cc = cc - cross @ np.linalg.solve(block, cross.T)
    if hidden.size == 0:
        return float(result)
    if hidden.size == 1:
        return result + float(log_ndtr(-cm.item(0) / math.sqrt(cc.item(0, 0))))
    if hidden.size == 2:
        sd0, sd1 = math.sqrt(cc.item(0, 0)), math.sqrt(cc.item(1, 1))
        rho = cc.item(0, 1) / (sd0 * sd1)
        a, b = -cm.item(0) / sd0, -cm.item(1) / sd1
        probability, _ = quad(
            lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
            * float(ndtr((b - rho * z) / math.sqrt(1 - rho * rho))),
            -np.inf, float(a), epsabs=1e-12, epsrel=1e-10,
        )
    else:
        probability = float(multivariate_normal.cdf(
            np.zeros(hidden.size), mean=cm, cov=cc,
            maxpts=1_000_000, abseps=1e-9, releps=1e-8,
            rng=np.random.default_rng(20261007),
        ))
    return result + math.log(probability) if probability > 0 else -math.inf
