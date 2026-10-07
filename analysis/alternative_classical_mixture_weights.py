"""Strict mixed-measure component likelihood and Dirichlet(2) weight fitting."""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp, softmax

from analysis.alternative_contracts import AlternativeError, PredictiveDistribution
from analysis.calibration import FloatArray


def component_log_likelihood(
    parts: tuple[PredictiveDistribution, ...], observation: float,
) -> FloatArray:
    """At any component atom, use only masses under the common mixed measure."""
    atoms: FloatArray = np.asarray([part.atom_mass(observation) for part in parts])
    if np.any(atoms > 0):
        with np.errstate(divide="ignore"):
            return np.log(atoms)
    return np.asarray([part.log_density(observation) for part in parts])


def fit_weights(
    log_likelihood: FloatArray, year_weights: FloatArray,
) -> tuple[FloatArray, float, float]:
    """Maximize prequential likelihood with an actual Dirichlet(2) MAP penalty."""
    if (log_likelihood.ndim != 2 or log_likelihood.shape[1] != 3
            or not np.all(np.any(np.isfinite(log_likelihood), axis=1))
            or np.any(np.isnan(log_likelihood)) or np.any(np.isposinf(log_likelihood))):
        raise AlternativeError("INVALID_COMPONENT_LIKELIHOOD", "No finite common law")

    def objective(eta: FloatArray) -> tuple[float, FloatArray]:
        logits: FloatArray = np.concatenate((eta, np.zeros(1)))
        log_weights: FloatArray = logits - logsumexp(logits)
        responsibilities: FloatArray = softmax(log_likelihood + log_weights, axis=1)
        predictive_logs: FloatArray = logsumexp(log_likelihood + log_weights, axis=1)
        loss = -(year_weights @ predictive_logs).item()
        loss -= log_weights.sum().item()
        gradient: FloatArray = ((year_weights.sum().item() + 3) * np.exp(log_weights)
                                - year_weights @ responsibilities - 1)
        return loss, gradient[:2]

    result = minimize(objective, np.zeros(2), jac=True, method="L-BFGS-B",
                      options={"maxiter": 500, "ftol": 1e-10, "gtol": 1e-6})
    parameters: FloatArray = np.asarray(result.x, dtype=np.float64)
    loss, gradient = objective(parameters)
    magnitude: FloatArray = np.abs(gradient)
    error = magnitude.max().item()
    if not result.success or not np.isfinite(loss) or error > 1e-5:
        raise AlternativeError("WEIGHT_SOLVER_FAILED", str(result.message))
    logits: FloatArray = np.concatenate((parameters, np.zeros(1)))
    weights: FloatArray = softmax(logits)
    return weights, loss, error
