"""Separate ridge trends and signed latent rain detrending (family ten)."""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from time import perf_counter

import numpy as np
from scipy.optimize import OptimizeResult, minimize
from scipy.special import log_ndtr
from scipy.stats import rankdata

from analysis.alternative_contracts import (
    CaseInput,
    FitConfig,
    FitDiagnostics,
    FitResult,
    FitStatus,
    MethodSpec,
    PredictiveDistribution,
    TrainingSet,
)
from analysis.alternative_distributions import (
    normal,
    power_censored,
    weighted_empirical,
)
from analysis.calibration import FloatArray, gaussian_crps
from analysis.data_io import Json

IDS = ("detrend_qm", "detrend_qdm", "detrend_emos")


def _empirical(values: FloatArray, weights: FloatArray) -> tuple[FloatArray, FloatArray]:
    order = np.argsort(values, kind="stable")
    unique, index = np.unique(values[order], return_index=True)
    mass: FloatArray = np.add.reduceat(weights[order], index)
    mass /= mass.sum()
    return unique, np.cumsum(mass) - 0.5 * mass


@dataclass(frozen=True, slots=True, kw_only=True)
class TrendModel:
    method_id: str
    rain: bool
    unit_scale: float
    time_center: float
    forecast_slope: float
    observed_slope: float
    historical_values: FloatArray
    historical_positions: FloatArray
    observed_values: FloatArray
    observed_positions: FloatArray
    parameters: FloatArray

    def predict(self, target: CaseInput) -> PredictiveDistribution:
        time = (target.valid_start.year - self.time_center) / 10
        members: FloatArray = np.sqrt(target.members/self.unit_scale) if self.rain else target.members
        detrended: FloatArray = members - self.forecast_slope*time
        restore = self.observed_slope*time
        if self.method_id == IDS[2]:
            a, b, c, d = (self.parameters.item(i) for i in range(4))
            mu = float(a + b*detrended.mean() + restore)
            variance = float(detrended.var(ddof=1)) if detrended.size > 1 else 0.0
            law = normal(mu, math.sqrt(c+d*variance))
            return power_censored(law, power=0.5, unit_scale=self.unit_scale) if self.rain else law
        if self.method_id == IDS[0]:
            ranks: FloatArray = np.interp(detrended, self.historical_values, self.historical_positions)
            mapped: FloatArray = np.interp(ranks, self.observed_positions, self.observed_values)
        else:
            ranks = (rankdata(detrended, method="average") - 0.5) / detrended.size
            mapped = detrended + np.interp(ranks, self.observed_positions, self.observed_values)
            mapped -= np.interp(ranks, self.historical_positions, self.historical_values)
        restored: FloatArray = mapped + restore
        if self.rain:
            restored = self.unit_scale * np.maximum(restored, 0.0)**2
        return weighted_empirical(restored, np.full(restored.size, 1.0/restored.size))

    def to_spec(self) -> dict[str, Json]:
        return {"kind": self.method_id, "rain": self.rain, "unit_scale": self.unit_scale,
                "time_center": self.time_center, "forecast_slope": self.forecast_slope,
                "observed_slope": self.observed_slope,
                "historical_values": self.historical_values.tolist(),
                "historical_positions": self.historical_positions.tolist(),
                "observed_values": self.observed_values.tolist(),
                "observed_positions": self.observed_positions.tolist(),
                "parameters": self.parameters.tolist(),
                "qdm_convention": "additive_signed_latent" if self.rain else "additive"}


def fit_trend(spec: MethodSpec, training: TrainingSet, config: FitConfig) -> FitResult:
    """Estimate training-only distinct trends, then map or optimize the residual law."""
    del config
    started = perf_counter()
    rows = training.rows
    years = len({r.source_year for r in rows})
    base = FitDiagnostics(n_rows=len(rows), n_years=years, train_hash=training.train_hash)
    if spec.id not in IDS:
        raise ValueError(f"unknown detrend method {spec.id}")
    if years < 10:
        return FitResult(method_id=spec.id, status=FitStatus.INSUFFICIENT_TRAINING,
                         fitted_model=None, diagnostics=base,
                         reason_code="FEWER_THAN_TEN_YEARS")
    rain = training.target.variable == "prcp"
    y_raw: FloatArray = np.array([r.observation for r in rows], dtype=np.float64)
    positive: FloatArray = y_raw[y_raw > 0]
    unit = max(float(positive.mean()), 1.0) if rain and positive.size else 1.0
    y: FloatArray = np.sqrt(y_raw/unit) if rain else y_raw
    ensembles: tuple[FloatArray, ...] = tuple(
        np.sqrt(r.ensemble/unit) if rain else r.ensemble for r in rows)
    forecast: FloatArray = np.array([math.sqrt(float(r.ensemble.mean())/unit) if rain
                         else float(r.ensemble.mean()) for r in rows])
    weights: FloatArray = np.asarray(training.year_weights, dtype=np.float64)
    weights = weights * years / weights.sum()
    time_center = float(weights @ np.array([r.source_year for r in rows]) / years)
    time: FloatArray = np.array([(r.source_year-time_center)/10 for r in rows])

    def slope(values: FloatArray) -> float:
        center = float(weights @ values / years)
        sd = max(math.sqrt(float(weights @ (values-center)**2 / years)), 1e-6)
        standardized: FloatArray = (values-center)/sd
        return sd * float(weights @ (time*standardized)) / (float(weights @ time**2)+1)

    beta_x, beta_y = slope(forecast), slope(y)
    historical: tuple[FloatArray, ...] = tuple(
        ensemble-beta_x*time.item(i) for i, ensemble in enumerate(ensembles))
    observed: FloatArray = y-beta_y*time
    value_weights: FloatArray = np.concatenate([
        np.full(ensemble.size, weights.item(i)/(years*ensemble.size))
        for i, ensemble in enumerate(historical)
    ])
    hv, hp = _empirical(np.concatenate(historical), value_weights)
    ov, op = _empirical(observed, weights/years)
    parameters: FloatArray = np.empty(0, dtype=np.float64)
    objective_value: float | None = None
    message = "closed-form standardized ridge trends; equal-year empirical mapping"
    flags: tuple[str, ...] = ()
    if spec.id == IDS[2]:
        # Temperature CRPS is evaluated in original units; rain has a distinct
        # row-specific latent censor boundary, never a zero-censored residual fit.
        center = 0.0 if rain else float(weights @ observed / years)
        scale = 1.0 if rain else max(float(np.std(observed)), 1.0)
        means: FloatArray = np.array([(float(x.mean())-center)/scale for x in historical])
        variance: FloatArray = np.array([float(x.var(ddof=1))/scale**2 if x.size > 1 else 0.0
                             for x in historical])
        actual: FloatArray = (observed-center)/scale
        boundary: FloatArray = -beta_y*time
        def objective(p: FloatArray) -> float:
            a, b, c, d = (p.item(i) for i in range(4))
            mu: FloatArray = a+b*means
            sigma: FloatArray = np.sqrt(c+d*variance)
            if not rain:
                return float(weights @ gaussian_crps(mu*scale+center, sigma*scale, observed) / years)
            wet = y_raw > 0
            log_probability: FloatArray = log_ndtr((boundary-mu)/sigma)
            losses: FloatArray = -log_probability
            z: FloatArray = (actual[wet]-mu[wet])/sigma[wet]
            losses[wet] = 0.5*z**2 + np.log(sigma[wet]) + 0.5*math.log(2*math.pi)
            losses[wet] += np.log(2*np.sqrt(unit*y_raw[wet]))
            return float(weights @ losses + 0.5*(b*b+d*d))
        solutions: list[tuple[float, FloatArray, str]] = []
        messages: list[str] = []
        for initial_slope in (0.0, 1.0):
            residual: FloatArray = actual-initial_slope*means
            initial: FloatArray = np.array([float(weights @ residual/years), initial_slope,
                                max(float(np.var(residual)), 1e-6), 0.0])
            result: OptimizeResult = minimize(objective, initial, method="L-BFGS-B",
                              bounds=((None, None), (0, None), (1e-6, math.exp(12)), (0, None)),
                              options={"maxiter": 500, "ftol": 1e-10, "gtol": 1e-6})
            messages.append(str(result.message))
            if result.success and np.isfinite(result.fun) and np.all(np.isfinite(result.x)):
                solutions.append((float(result.fun), np.asarray(result.x), str(result.message)))
        if not solutions:
            return FitResult(method_id=spec.id, status=FitStatus.FIT_FAILED, fitted_model=None,
                             diagnostics=replace(base, elapsed_seconds=perf_counter()-started,
                                                 message="; ".join(messages)),
                             reason_code="NO_CONVERGED_FINITE_OPTIMUM")
        objective_value, p, message = min(solutions, key=lambda result: result[0])
        a, b, c, d = (p.item(i) for i in range(4))
        parameters = np.array([center+scale*a-b*center, b, scale**2*c, d])
        flags = tuple(name for name, value in (("slope_zero", b), ("variance_floor", c-1e-6),
                                               ("variance_ceiling", c-math.exp(12)),
                                               ("spread_zero", d)) if abs(value) < 1e-6)
    fitted = TrendModel(method_id=spec.id, rain=rain, unit_scale=unit, time_center=time_center,
                        forecast_slope=beta_x, observed_slope=beta_y, historical_values=hv,
                        historical_positions=hp, observed_values=ov, observed_positions=op,
                        parameters=parameters)
    return FitResult(
        method_id=spec.id, status=FitStatus.OK, fitted_model=fitted,
        diagnostics=replace(base, objective=objective_value, convergence=True,
                                   parameter_count=2+parameters.size, boundary_flags=flags,
                                   elapsed_seconds=perf_counter()-started, message=message),
    )
