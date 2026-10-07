"""Conjugate Gaussian algebra in fixed physical coordinates.

Student matrices in this module are scale matrices, NEVER covariance matrices.
The matrix-normal representation includes NIW as its intercept-only special case.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from analysis.calibration import FloatArray


@dataclass(frozen=True, slots=True, kw_only=True)
class Posterior:
    """Matrix-normal/inverse-Wishart posterior sufficient statistics."""

    coefficients: FloatArray
    row_covariance: FloatArray
    iw_scale: FloatArray
    iw_df: float

    def predictive(self, design: FloatArray) -> tuple[float, FloatArray, FloatArray]:
        dimension = np.size(self.iw_scale, axis=0)
        df = self.iw_df - dimension + 1
        multiplier = 1.0 + float(design @ self.row_covariance @ design)
        return df, design @ self.coefficients, multiplier / df * self.iw_scale


def update(
    values: FloatArray, design: FloatArray, prior_variances: FloatArray,
    *, nig: bool = False,
) -> Posterior:
    """Exact proper MNIW update; d=1 NIG uses IG(4,3), not IW(9,7)."""
    n, dimension = np.size(values, axis=0), np.size(values, axis=1)
    precision = np.diag(1.0 / prior_variances)
    vn = np.linalg.inv(precision + design.T @ design)
    bn = vn @ design.T @ values
    residual = values - design @ bn
    # Residual + prior quadratic avoids subtraction of large cross products.
    scale = (6.0 if nig else 7.0) * np.eye(dimension)
    scale += residual.T @ residual + bn.T @ precision @ bn
    return Posterior(
        coefficients=bn, row_covariance=vn, iw_scale=(scale + scale.T) / 2,
        iw_df=float((8 if nig else dimension + 8) + n),
    )


def condition(
    location: FloatArray, matrix: FloatArray, predictor: FloatArray,
    df: float | None,
) -> tuple[float | None, FloatArray, FloatArray]:
    """Condition a joint Normal or Student, updating Student degrees of freedom."""
    nx = predictor.size
    if nx == 0:
        return df, location.copy(), matrix.copy()
    cross = matrix[nx:, :nx]
    solved = np.linalg.solve(matrix[:nx, :nx], predictor - location[:nx])
    mean = location[nx:] + cross @ solved
    schur = matrix[nx:, nx:] - cross @ np.linalg.solve(
        matrix[:nx, :nx], matrix[:nx, nx:]
    )
    if df is not None:
        delta = float((predictor - location[:nx]) @ solved)
        schur = schur * ((df + delta) / (df + nx))
        df += nx
    return df, mean, (schur + schur.T) / 2


def draw_parameters(
    posterior: Posterior, rng: np.random.Generator,
) -> tuple[FloatArray, FloatArray]:
    """Bartlett IW draw followed by the full matrix-normal coefficient draw."""
    dimension = np.size(posterior.iw_scale, axis=0)
    bartlett = np.tril(rng.normal(size=(dimension, dimension)), -1)
    for i in range(dimension):
        bartlett[i, i] = np.sqrt(rng.chisquare(posterior.iw_df - i))
    root = np.linalg.cholesky(posterior.iw_scale)
    factor = np.linalg.solve(bartlett, root.T).T
    covariance = factor @ factor.T
    coefficients = posterior.coefficients + (
        np.linalg.cholesky(posterior.row_covariance)
        @ rng.normal(size=posterior.coefficients.shape) @ factor.T
    )
    return coefficients, covariance


def residual_predictive(
    posterior: Posterior, covariance: FloatArray,
    design: FloatArray, predictor: FloatArray,
) -> tuple[FloatArray, FloatArray, float]:
    """Rao--Blackwellize the entire predictive law given completed data and Omega.

    Under MNIW, Omega=Sigma_yy.x is IW_q(nu,Psi_yy.x). Integrating coefficient
    and cross-regression uncertainty leaves Normal(ell,k*Omega), not a Student
    component. Predictor weights integrate the independent predictor parameters.
    This changes emitted Monte Carlo components, never Gibbs states or draws.
    """
    mean = design @ posterior.coefficients
    multiplier = 1.0 + float(design @ posterior.row_covariance @ design)
    nx = predictor.size
    if nx == 0:
        return mean, multiplier * covariance, 0.0
    psi = posterior.iw_scale
    delta = predictor - mean[:nx]
    solved = np.linalg.solve(psi[:nx, :nx], delta)
    distance = float(delta @ solved)
    location = mean[nx:] + psi[nx:, :nx] @ solved
    omega = covariance[nx:, nx:] - covariance[nx:, :nx] @ np.linalg.solve(
        covariance[:nx, :nx], covariance[:nx, nx:]
    )
    matrix = (multiplier + distance) * (omega + omega.T) / 2
    degrees = posterior.iw_df - np.size(psi, axis=0) + 1
    diagonal: FloatArray = np.diag(np.linalg.cholesky(psi[:nx, :nx]))
    log_determinant = 2 * math.fsum(math.log(v) for v in diagonal.flat)
    # Student_x(df=degrees, scale=multiplier/degrees*Psi_xx), simplified
    # to avoid a redundant scale matrix and cancellation of log(degrees).
    log_weight = (
        math.lgamma((degrees + nx) / 2) - math.lgamma(degrees / 2)
        - 0.5 * (nx * math.log(multiplier * math.pi) + log_determinant)
        - 0.5 * (degrees + nx) * math.log1p(distance / multiplier)
    )
    return location, matrix, log_weight


def parameter_monitor(
    coefficients: FloatArray, covariance: FloatArray, latent: FloatArray,
) -> FloatArray:
    """Means/slopes, log SD, all correlations/eigenvalues and censored latents."""
    sd = np.sqrt(np.diag(covariance))
    correlation = covariance / np.outer(sd, sd)
    indices = np.triu_indices(sd.size, 1)
    return np.concatenate((
        coefficients.ravel(), np.log(sd), correlation[indices],
        np.log(np.linalg.eigvalsh(covariance)), latent,
    ))
