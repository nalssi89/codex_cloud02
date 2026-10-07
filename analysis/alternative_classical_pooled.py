"""Year-balanced, lead-sharing CRPS regressions (frozen family nine)."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
from math import cos, log, pi, sin, sqrt
from time import perf_counter

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize
from scipy.special import ndtr

from analysis.alternative_classical_pooled_rows import canonical_rows
from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FitConfig,
    FitDiagnostics,
    FitResult,
    FitStatus,
    MethodSpec,
    PredictiveDistribution,
    TrainingSet,
)
from analysis.alternative_distributions import normal
from analysis.calibration import FloatArray, gaussian_crps, normal_pdf
from analysis.data_io import Json

IDS = ("pooled_mos_ridge", "pooled_emos_ridge", "pooled_emos_cyclic")


def _harmonics(start: date, end: date) -> FloatArray:
    # Dates are mid-window phases, with leap-year length preserved.
    midpoint = start + (end - start) / 2
    phase = 2 * pi * (midpoint - date(midpoint.year, 1, 1)).days / (
        date(midpoint.year + 1, 1, 1) - date(midpoint.year, 1, 1)
    ).days
    return np.array([sin(phase), cos(phase), sin(2 * phase), cos(2 * phase)])


def _moments(members: FloatArray, center: float, scale: float) -> tuple[float, float]:
    return ((float(members.mean()) - center) / scale,
            float(members.var(ddof=1)) / scale**2 if members.size > 1 else 0.0)


@dataclass(frozen=True, slots=True, kw_only=True)
class PooledModel:
    method_id: str
    leads: tuple[str, ...]
    parameters: FloatArray
    center: float
    scale: float
    rain: bool
    years: int

    def latent(self, mean: FloatArray, variance: FloatArray, lead: NDArray[np.int64],
                harmonic: FloatArray) -> tuple[FloatArray, FloatArray]:
        p, n = self.parameters, len(self.leads)
        mu: FloatArray = p.item(0) + p[2:2+n][lead] + p[2+n:2+2*n][lead] * mean
        offset = 2 + 2*n
        log_variance = np.full(mean.shape, p.item(offset))
        if self.method_id != IDS[0]:
            log_variance += p[offset+1:offset+1+n][lead]
            offset += n + 1
            spread = p.item(offset) * variance
            offset += 1
        else:
            spread = np.zeros_like(mean)
            offset += 1
        if self.method_id == IDS[2]:
            mu += harmonic @ p[offset:offset+4]
            log_variance += 2 * (harmonic @ p[offset+4:offset+8])
        sigma = np.sqrt(np.exp(log_variance) + spread)
        return mu, sigma

    def predict(self, target: CaseInput) -> PredictiveDistribution:
        if target.lead not in self.leads:
            raise ValueError(f"untrained lead {target.lead}")
        mean, variance = _moments(target.members, self.center, self.scale)
        mu, sigma = self.latent(
            np.array([mean]), np.array([variance]),
            np.array([self.leads.index(target.lead)], dtype=np.int64),
            _harmonics(target.valid_start, target.valid_end)[None, :],
        )
        return normal(self.center + self.scale * mu.item(0),
                      self.scale * sigma.item(0), censor_zero=self.rain)

    def to_spec(self) -> dict[str, Json]:
        return {"kind": self.method_id, "parameters": self.parameters.tolist(),
                "leads": list(self.leads), "center": self.center, "scale": self.scale,
                "rain": self.rain, "distinct_years": self.years}


def fit_pooled(spec: MethodSpec, training: TrainingSet, config: FitConfig) -> FitResult:
    """Fit both climate/slope-one starts; issue only a converged minimizer."""
    del config
    started = perf_counter()
    years = len({r.source_year for r in training.rows})
    base = FitDiagnostics(n_rows=len(training.rows), n_years=years, train_hash=training.train_hash)
    if spec.id not in IDS:
        raise ValueError(f"unknown pooled method {spec.id}")
    if years < 10:
        return FitResult(method_id=spec.id, status=FitStatus.INSUFFICIENT_TRAINING,
                         fitted_model=None, diagnostics=base,
                         reason_code="FEWER_THAN_TEN_YEARS")
    try:
        rows, raw_weights = canonical_rows(training)
    except AlternativeError as error:
        return FitResult(method_id=spec.id, status=FitStatus.INPUT_CONFLICT,
                         fitted_model=None, diagnostics=replace(base, message=str(error)),
                         reason_code=error.code)
    base = replace(base, n_rows=len(rows))
    rain = training.target.variable == "prcp"
    if any((r.product, r.variable) != (training.target.product, training.target.variable)
           for r in rows):
        raise ValueError("pooled rows must share product and variable")
    observed = np.array([r.observation for r in rows], dtype=np.float64)
    weights = raw_weights
    weights = weights / weights.sum()
    center = 0.0 if rain else float(weights @ observed)
    positive = observed > 0
    positive_mean = float(weights[positive] @ observed[positive] / weights[positive].sum()) if (
        np.any(positive)) else 1.0
    scale = max(positive_mean if rain else
                float(np.sqrt(weights @ (observed-center)**2)), 1.0)
    y = (observed-center) / scale
    moments = np.array([_moments(r.ensemble, center, scale) for r in rows])
    mean, variance = moments[:, 0], moments[:, 1]
    leads = tuple(sorted({r.lead for r in rows}))
    n = len(leads)
    lead = np.array([leads.index(r.lead) for r in rows], dtype=np.int64)
    harmonic = np.array([_harmonics(r.hist_start, r.hist_end) for r in rows])
    offset = 2 + 2*n
    size = offset + 1 + (n+2 if spec.id != IDS[0] else 0) + (8 if spec.id == IDS[2] else 0)
    bounds: list[tuple[float | None, float | None]] = [(None, None)] * size
    bounds[1] = (0.0, None)
    bounds[2+n:2+2*n] = [(0.0, None)] * n
    bounds[offset] = (-12.0, 12.0)
    if spec.id != IDS[0]:
        bounds[offset+1:offset+1+n] = [(-12.0, 12.0)] * n
        bounds[offset+n+1] = (0.0, None)

    def model(p: FloatArray) -> PooledModel:
        return PooledModel(method_id=spec.id, leads=leads, parameters=p, center=center,
                           scale=scale, rain=rain, years=years)

    def parts(p: FloatArray) -> tuple[float, float]:
        mu, sigma = model(p).latent(mean, variance, lead, harmonic)
        loss = scale * float(weights @ gaussian_crps(mu, sigma, y, rain))
        penalty = 0.5 * float(p.item(1)**2 + np.sum(p[2:2+n]**2)
                             + np.sum((p[2+n:2+2*n]-p.item(1))**2))
        cursor = offset + 1
        if spec.id != IDS[0]:
            penalty += 0.5 * float(np.sum(p[cursor:cursor+n]**2))
            cursor += n + 1
        if spec.id == IDS[2]:
            curvature = np.array([1.0, 1.0, 16.0, 16.0])
            penalty += 0.5 * float(curvature @ (
                p[cursor:cursor+4]**2 + p[cursor+4:cursor+8]**2))
        return loss, penalty

    def objective(p: FloatArray) -> float:
        loss, penalty = parts(p)
        return loss + penalty / years

    def gradient(p: FloatArray) -> FloatArray:
        mu, sigma = model(p).latent(mean, variance, lead, harmonic)
        z = (y-mu)/sigma
        gmu = 1-2*ndtr(z)
        gsigma: FloatArray = 2*normal_pdf(z)-1/sqrt(pi)
        if rain:
            a0 = -mu/sigma
            probability = ndtr(a0)
            gmu += probability**2
            gsigma += -2*probability*normal_pdf(a0)+ndtr(sqrt(2)*a0)/sqrt(pi)
        gmu *= scale * weights
        gsigma *= scale * weights
        g = np.zeros(size)
        g[0] = gmu.sum()
        g[1] = (p.item(1)+np.sum(p.item(1)-p[2+n:2+2*n]))/years
        g[2:2+n] = np.bincount(lead, weights=gmu, minlength=n) + p[2:2+n]/years
        g[2+n:2+2*n] = np.bincount(lead, weights=gmu*mean, minlength=n)
        g[2+n:2+2*n] += (p[2+n:2+2*n]-p.item(1))/years
        spread = p.item(offset+n+1)*variance if spec.id != IDS[0] else 0
        glog: FloatArray = gsigma*(sigma**2-spread)/(2*sigma)
        g[offset] = glog.sum()
        cursor = offset+1
        if spec.id != IDS[0]:
            g[cursor:cursor+n] = np.bincount(lead, weights=glog, minlength=n)
            g[cursor:cursor+n] += p[cursor:cursor+n]/years
            cursor += n
            g[cursor] = np.sum(gsigma*variance/(2*sigma))
            cursor += 1
        if spec.id == IDS[2]:
            curvature = np.array([1., 1., 16., 16.])
            g[cursor:cursor+4] = harmonic.T @ gmu + curvature*p[cursor:cursor+4]/years
            g[cursor+4:cursor+8] = 2*harmonic.T @ glog + curvature*p[cursor+4:cursor+8]/years
        return g

    solutions: list[tuple[float, FloatArray, str]] = []
    messages: list[str] = []
    for slope in (0.0, 1.0):
        initial = np.zeros(size)
        initial[0] = float(weights @ (y-slope*mean))
        initial[1] = slope
        initial[2+n:2+2*n] = slope
        residual: FloatArray = y - initial.item(0) - slope*mean
        initial[offset] = min(max(log(max(float(weights @ residual**2), 1e-6)), -12), 12)
        result = minimize(objective, initial, method="L-BFGS-B", jac=gradient, bounds=bounds,
                          options={"maxiter": 500, "ftol": 1e-10, "gtol": 1e-6})
        messages.append(str(result.message))
        if result.success and np.isfinite(result.fun) and np.all(np.isfinite(result.x)):
            solutions.append((float(result.fun), np.asarray(result.x), str(result.message)))
    if not solutions:
        return FitResult(method_id=spec.id, status=FitStatus.FIT_FAILED, fitted_model=None,
                         diagnostics=replace(base, elapsed_seconds=perf_counter()-started,
                                             message="; ".join(messages)),
                         reason_code="NO_CONVERGED_FINITE_OPTIMUM")
    value, parameters, message = min(solutions, key=lambda result: result[0])
    fitted = model(parameters)
    loss, penalty = parts(parameters)
    boundary = tuple(f"parameter_{i}_bound" for i, (lo, hi) in enumerate(bounds)
                     if (lo is not None and abs(parameters.item(i)-lo) < 1e-6)
                     or (hi is not None and abs(parameters.item(i)-hi) < 1e-6))
    return FitResult(
        method_id=spec.id, status=FitStatus.OK, fitted_model=fitted,
        diagnostics=replace(
            base, objective=value, convergence=True, parameter_count=size,
            boundary_flags=boundary, elapsed_seconds=perf_counter()-started,
            message=f"{message}; weighted_CRPS={loss}; penalty={penalty}; penalty_divisor={years}; "
            + f"input_rows={len(training.rows)}; canonical_rows={len(rows)}",
        ),
    )
