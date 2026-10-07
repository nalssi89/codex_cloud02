"""Strict coordinate-censored Gaussian Gibbs and target-conditioned mixtures."""

from __future__ import annotations

import hashlib
import math
from collections.abc import Generator
from dataclasses import dataclass
from typing import final

import numpy as np
from scipy.special import log_ndtr, logsumexp, ndtri_exp

from analysis.alternative_bayes_algebra import (
    draw_parameters,
    parameter_monitor,
    residual_predictive,
    update,
)
from analysis.alternative_contracts import AlternativeError
from analysis.calibration import FloatArray
from analysis.data_io import Json


@dataclass(frozen=True, slots=True, kw_only=True)
class MixtureDraws:
    """Chain order is retained, without thinning, for all diagnostics."""

    locations: FloatArray
    covariances: FloatArray
    log_weights: FloatArray
    monitors: FloatArray

    def weights(self) -> FloatArray:
        return np.exp(self.log_weights - logsumexp(self.log_weights))


@final
class Chain:
    """Persistent random stream and completed-data state across budget increases."""

    def __init__(
        self, values: FloatArray, design: FloatArray, variances: FloatArray,
        target_design: FloatArray, predictor: FloatArray, censored: FloatArray,
        target_censored: FloatArray, seed: int, *, nig: bool, augmented: bool,
    ) -> None:
        self.rng = np.random.default_rng(seed)
        self.values = values.copy()
        self.design = design.copy()
        self.variances = variances
        self.target_design = target_design
        self.predictor = predictor
        self.nig = nig
        self.augmented = augmented
        self.nx = predictor.size
        self.censored = censored.astype(bool)
        self.missing = np.zeros(values.shape, dtype=bool)
        if augmented:
            target = np.zeros(np.size(values, axis=1))
            target[:self.nx] = predictor
            self.values = np.vstack((self.values, target))
            self.design = np.vstack((self.design, target_design))
            target_mask = np.zeros(np.size(values, axis=1), dtype=bool)
            target_mask[:self.nx] = target_censored.astype(bool)
            self.censored = np.vstack((self.censored, target_mask))
            missing = np.zeros(np.size(values, axis=1), dtype=bool)
            missing[self.nx:] = True
            self.missing = np.vstack((self.missing, missing))
        self.values[self.censored] = -np.abs(
            self.rng.normal(size=int(np.count_nonzero(self.censored)))
        )
        self.coefficients, self.covariance = draw_parameters(
            update(self.values, self.design, variances, nig=nig), self.rng
        )
        self.rows, self.columns = np.nonzero(self.censored | self.missing)

    def step(self) -> tuple[FloatArray, FloatArray, float, FloatArray]:
        """Every coordinate uses the full precision conditional, not its marginal."""
        precision = np.linalg.inv(self.covariance)
        means = self.design @ self.coefficients
        for row, column in zip(self.rows, self.columns, strict=True):
            sd = math.sqrt(1.0 / precision.item(column, column))
            centered = self.values[row:row + 1].ravel() - means[row:row + 1].ravel()
            mu = self.values.item(row, column) - float(
                precision[column:column + 1].ravel() @ centered / precision.item(column, column)
            )
            if self.censored[row, column]:
                log_probability = float(log_ndtr(-mu / sd))
                normal_draw = float(ndtri_exp(
                    log_probability + math.log(self.rng.uniform())
                ))
            else:
                normal_draw = float(self.rng.normal())
            self.values[row, column] = mu + sd * normal_draw
        posterior = update(self.values, self.design, self.variances, nig=self.nig)
        self.coefficients, self.covariance = draw_parameters(posterior, self.rng)
        x = self.values[-1, :self.nx] if self.augmented else self.predictor
        conditional_mean, conditional_covariance, integrated_log_weight = residual_predictive(
            posterior, self.covariance, self.target_design, x
        )
        log_weight = 0.0 if self.augmented else integrated_log_weight
        monitor = parameter_monitor(
            self.coefficients, self.covariance, self.values[self.censored]
        )
        return conditional_mean, conditional_covariance, log_weight, monitor


def run_chains(
    values: FloatArray, design: FloatArray, variances: FloatArray,
    target_design: FloatArray, predictor: FloatArray, censored: FloatArray,
    target_censored: FloatArray, seed_key: str, *, nig: bool, augmented: bool,
) -> Generator[MixtureDraws, None, None]:
    """Yield fixed diagnostic checkpoints while preserving all four streams."""
    chains = [
        Chain(
            values, design, variances, target_design, predictor, censored,
            target_censored,
            int.from_bytes(hashlib.sha256(f"{seed_key}:{i}".encode()).digest()[:8]),
            nig=nig, augmented=augmented,
        ) for i in range(4)
    ]
    saved: list[list[tuple[FloatArray, FloatArray, float, FloatArray]]] = [
        [] for _ in chains
    ]
    for chain in chains:
        for _ in range(1024):
            _ = chain.step()
    for retained in (2048, 8192, 32768):
        for chain, draws in zip(chains, saved, strict=True):
            for _ in range(retained - len(draws)):
                draws.append(chain.step())
        yield MixtureDraws(
            locations=np.asarray([[d[0] for d in chain] for chain in saved]),
            covariances=np.asarray([[d[1] for d in chain] for chain in saved]),
            log_weights=np.asarray([[d[2] for d in chain] for chain in saved]),
            monitors=np.asarray([[d[3] for d in chain] for chain in saved]),
        )


def importance_report(draws: MixtureDraws) -> dict[str, Json]:
    weights = draws.weights()
    effective = 1.0 / float(np.sum(weights * weights))
    maximum = float(weights.max())
    return {
        "importance_effective_count": effective, "maximum_weight": maximum,
        "importance_passed": effective >= 400 and maximum <= 0.05,
    }


class PosteriorFailure(AlternativeError):
    diagnostics: dict[str, Json]

    def __init__(self, diagnostics: dict[str, Json]) -> None:
        self.diagnostics = diagnostics
        super().__init__("POSTERIOR_DIAGNOSTICS_FAILED", str(diagnostics))


def posterior_failure(diagnostics: dict[str, Json]) -> PosteriorFailure:
    return PosteriorFailure(diagnostics)
