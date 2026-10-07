"""Likelihood/CRPS-fitted local classical families, with real solver outcomes."""

from __future__ import annotations

from dataclasses import replace
from math import exp, expm1, log
from time import perf_counter
from types import MappingProxyType

import numpy as np
from numpy.typing import NDArray
from scipy.special import gammaln, log_ndtr
from scipy.stats import gamma as gamma_stat
from scipy.stats import genextreme

from analysis.alternative_classical_common import (
    Coordinates,
    coordinates,
    moments,
    result,
    softplus,
    solve,
)
from analysis.alternative_classical_laws import LocalModel
from analysis.alternative_contracts import (
    AlternativeError,
    FitConfig,
    FitResult,
    FitStatus,
    MethodSpec,
    TrainingSet,
)
from analysis.calibration import FloatArray, gaussian_crps

NORMAL_IDS = ("emos", "anomaly_mos", "emos_constant_variance", "mos_unit_slope")
LOCAL_IDS = (*NORMAL_IDS, "gamma_positive", "csg_fixed_shift", "csg_estimated_shift",
             "power_gaussian_sqrt", "power_gaussian_cuberoot",
             "power_logistic_sqrt", "power_logistic_cuberoot", "hurdle_gamma",
             "hurdle_lognormal", "gev_censored_gumbel", "gev_censored_shrunk_shape",
             "tweedie_p15")


def fit_local(spec: MethodSpec, training: TrainingSet, config: FitConfig,
              tweedie_power: float = 1.5) -> FitResult:
    started = perf_counter()
    name = spec.id
    crps_fit = name in ("emos", "anomaly_mos")
    rain = training.target.variable == "prcp"
    coord = coordinates(training)
    y: FloatArray = np.array([(r.observation - coord.offset) / coord.scale for r in training.rows])
    mv: FloatArray = np.array([moments(r.ensemble, coord) for r in training.rows])
    m: FloatArray = mv[:, 0]
    v: FloatArray = mv[:, 1]
    w = training.year_weights
    climate = float(np.sum(y * w) / w.sum())
    if name == "gamma_positive" and np.any(y <= 0):
        return result(name, training, started, None, status=FitStatus.GATED_DATA,
                      reason="G0_NONPOSITIVE_TRAINING",
                      message=f"exact zero count={sum(r.observation == 0 for r in training.rows)}")
    if name.startswith("hurdle_") and len({r.source_year for r in training.rows
                                        if r.observation > 0}) < 3:
        return result(name, training, started, None,
                      status=FitStatus.INSUFFICIENT_TRAINING,
                      reason="FEWER_THAN_THREE_POSITIVE_YEARS")
    unrestricted = (None, None)
    nonnegative = (0.0, None)
    log_bound = (-12.0, 12.0)
    if name in NORMAL_IDS:
        initial = np.array([climate, 0.0, max(float(y.var()), 1e-6), 0.0])
        bounds = (unrestricted, (0.0, 1.0) if name == "anomaly_mos" else nonnegative,
                  (1e-6, None), nonnegative if name == "emos" else (0.0, 0.0))
        if name == "mos_unit_slope":
            initial[1] = 1.0
            bounds = (unrestricted, (1.0, 1.0), (1e-6, None), (0.0, 0.0))
        if name == "anomaly_mos":
            bounds = ((climate, climate), bounds[1], bounds[2], bounds[3])
    elif name.startswith("hurdle_"):
        wet = y[y > 0]
        intensity_mean = max(float(wet.mean()), 1e-6)
        shape = intensity_mean**2 / max(float(wet.var()), 1e-6)
        p0 = (sum(row.observation == 0 for row in training.rows) + 0.5) / (len(training.rows) + 1)
        initial = np.array([log(intensity_mean), 0.0,
                            min(max(log(shape), -12), 12), log(p0 / (1-p0)), 0.0])
        if name == "hurdle_lognormal":
            initial[0] = float(np.log(wet).mean())
            initial[2] = log(max(float(np.log(wet).std()), 1e-3))
        bounds = (unrestricted, unrestricted, log_bound, unrestricted, unrestricted)
    elif name.startswith(("gamma_", "csg_")):
        delta = 0.0 if name == "gamma_positive" else 0.1
        climate_mu = max(climate + delta, 1e-6)
        variance = max(float(y.var()), 1e-6)
        initial = np.array([climate_mu + log(-expm1(-climate_mu)), 0.0,
                            min(max(variance + log(-expm1(-variance)), -12), 12), -2.0])
        bounds = (unrestricted, nonnegative, log_bound, log_bound)
        if name == "csg_estimated_shift":
            initial = np.append(initial, -2.252168461)
            bounds = (*bounds, log_bound)
    elif name.startswith(("power_", "gev_")):
        power = 0.5 if name.endswith("sqrt") else 1 / 3
        transformed = y**power if name.startswith("power_") else y
        initial = np.array([float(transformed.mean()), 0.0,
                            log(max(float(transformed.std()), 0.1)), 0.0])
        bounds = (unrestricted, nonnegative, log_bound,
                  nonnegative if name.startswith("gev_") else unrestricted)
        if name == "gev_censored_shrunk_shape":
            initial = np.append(initial, 0.0)
            bounds = (*bounds, (-0.25, 0.25))
    elif name.startswith("tweedie_"):
        initial = np.array([log(max(climate, 1e-6)), 0.0,
                            min(max(log(max(float(y.var()), 1e-6))
                                    - tweedie_power * log(max(climate, 1e-6)), -12), 12)])
        bounds = (log_bound, nonnegative, log_bound)
    else:
        raise ValueError(f"Not a local classical method: {name}")

    def objective(p: FloatArray) -> float:
        a, b, c = (p.item(i) for i in range(3))
        d = p.item(3) if p.size > 3 else 0.0
        if crps_fit:
            mu = climate + b * (m - coord.mean_center
                               ) if name == "anomaly_mos" else a + b * m
            scores = gaussian_crps(mu, np.sqrt(c + d * v), y, rain)
            return coord.scale * float(np.sum(scores * w) / w.sum())
        loglike = log_likelihood(name, p, m, v, y, training, coord, tweedie_power)
        if not name.startswith("tweedie_"):
            loglike = loglike - (np.where(y > 0, log(coord.scale), 0.0)
                                if rain else log(coord.scale))
        if not np.all(np.isfinite(loglike)):
            return float("inf")
        penalty = 0.5 * b**2
        if name.startswith("hurdle_"):
            penalty += (d**2 + p.item(4)**2) / 8.0
        elif p.size > 3:
            penalty += 0.5 * d**2
        if name == "gev_censored_shrunk_shape":
            penalty += 0.5 * (p.item(4) / 0.1)**2
        if name == "csg_estimated_shift":
            penalty += 0.5 * (softplus(p.item(4)) / 0.5)**2
        return -float(np.sum(w * loglike)) + penalty

    second: FloatArray = initial.copy()
    second[1] = 1.0
    if name in NORMAL_IDS:
        second[0] = float((y - m).mean()) if name != "anomaly_mos" else climate
        second[2] = max(float((y - m).var()), 1e-6)
    elif name.startswith(("gamma_", "csg_")):
        second[0] -= float(m.mean())
        residual = y - np.logaddexp(0, second.item(0) + m)
        residual_variance = max(float(residual.var()), 1e-6)
        second[2] = min(max(residual_variance + log(-expm1(-residual_variance)), -12), 12)
    elif name.startswith("power_"):
        power = 0.5 if name.endswith("sqrt") else 1 / 3
        second[0] = float((y**power - m**power).mean())
        second[2] = log(max(float((y**power - m**power).std()), exp(-12)))
    try:
        p, loss, message, flags = solve(objective, (initial, second), bounds)
        model = LocalModel(name, p, coord, rain, climate, tweedie_power)
        prediction = model.predict(training.target)
        if not np.isfinite(prediction.mean()) or config.numerical_tolerance <= 0:
            raise AlternativeError("NONFINITE_PREDICTIVE_MEAN", name)
        free_count = sum(lo != hi or lo is None for lo, hi in bounds)
        fitted = result(name, training, started, model, loss, free_count, message, flags)
        if crps_fit:
            likelihood_loss = loss
        else:
            ll = log_likelihood(name, p, m, v, y, training, coord, tweedie_power)
            if not name.startswith("tweedie_"):
                ll = ll - (np.where(y > 0, log(coord.scale), 0.0)
                           if rain else log(coord.scale))
            likelihood_loss = -float(np.sum(w * ll))
        return replace(fitted, diagnostics=replace(
            fitted.diagnostics, posterior_diagnostics=MappingProxyType({
                "training_loss_without_penalty": likelihood_loss,
                "penalty": loss - likelihood_loss,
                "loss_kind": "original_unit_crps" if crps_fit else "negative_log_likelihood",
            })))
    except (AlternativeError, ValueError, FloatingPointError, OverflowError) as exc:
        return result(name, training, started, None, status=FitStatus.FIT_FAILED,
                      reason=exc.code if isinstance(exc, AlternativeError) else type(exc).__name__,
                      message=str(exc))


def log_likelihood(name: str, p: FloatArray, m: FloatArray, v: FloatArray,
                   y: FloatArray, training: TrainingSet,
                   coord: Coordinates, power: float) -> FloatArray:
    """Vectorized stable atom/density objectives except certified Tweedie series."""
    a, b, c = (p.item(i) for i in range(3))
    d = p.item(3) if p.size > 3 else 0.0
    if name in NORMAL_IDS:
        mu, sd = a + b * m, np.sqrt(c + d * v)
        out: FloatArray = -.5*((y-mu)/sd)**2 - np.log(sd) - .5*log(2*np.pi)
        if training.target.variable == "prcp":
            dry_normal = np.array([y.item(i) == 0 for i in range(y.size)], dtype=np.bool_)
            out[dry_normal] = log_ndtr(-mu[dry_normal]/sd[dry_normal])
        return out
    if name.startswith(("gamma_", "csg_")):
        mu = np.logaddexp(0, a + b * m) + 1e-6
        var = softplus(c) + softplus(d) * v + 1e-6
        k, theta = mu**2 / var, var / mu
        delta = softplus(p.item(4)) if p.size == 5 else (
            0.1 if name == "csg_fixed_shift" else 0.0)
        out = np.asarray(gamma_stat.logpdf(y + delta, k, scale=theta), dtype=np.float64)
        dry: NDArray[np.bool_] = np.array([y.item(i) == 0 for i in range(y.size)], dtype=np.bool_)
        out[dry] = gamma_stat.logcdf(delta, k[dry], scale=theta[dry])
        return out
    if name.startswith("power_"):
        r = 0.5 if name.endswith("sqrt") else 1 / 3
        # Transformation of members is specified; transformation of mean is distinct.
        spread = np.array([float(np.std((row.ensemble / coord.scale)**r, ddof=1))
                           if row.ensemble.size > 1 else 0.0 for row in training.rows])
        mu, sd = a + b * m**r, np.exp(c + d * np.log1p(spread))
        z = (y**r - mu) / sd
        wet = y > 0
        out = np.empty_like(y)
        if "logistic" in name:
            out[:] = -np.logaddexp(0, mu / sd)
            out[wet] = -z[wet] - 2 * np.logaddexp(0, -z[wet]) - np.log(sd[wet])
        else:
            out[:] = log_ndtr(-mu / sd)
            out[wet] = -0.5 * z[wet]**2 - 0.5 * log(2 * np.pi) - np.log(sd[wet])
        out[wet] += log(r) + (r - 1) * np.log(y[wet])
        return out
    if name.startswith("gev_"):
        mu, sd = a + b * m, np.exp(c + d * np.log1p(np.sqrt(v)))
        xi = p.item(4) if p.size == 5 else 0.0
        out = np.asarray(genextreme.logpdf(y, -xi, loc=mu, scale=sd), dtype=np.float64)
        gev_dry: NDArray[np.bool_] = np.array([y.item(i) == 0 for i in range(y.size)], dtype=np.bool_)
        out[gev_dry] = genextreme.logcdf(0, -xi, loc=mu[gev_dry], scale=sd[gev_dry])
        return out
    if name.startswith("hurdle_"):
        x = (m - coord.mean_center) / coord.mean_scale
        eta = d + p.item(4) * x
        out = -np.logaddexp(0, -eta)
        wet = y > 0
        out[wet] = -np.logaddexp(0, eta[wet])
        if name == "hurdle_gamma":
            k = exp(c)
            mu = np.exp(a + b * x[wet])
            out[wet] += (k - 1) * np.log(y[wet]) - y[wet] * k / mu - gammaln(k) - k * np.log(mu / k)
        else:
            sd = exp(c)
            z = (np.log(y[wet]) - a - b * x[wet]) / sd
            out[wet] += -np.log(y[wet]) - c - 0.5 * log(2 * np.pi) - 0.5 * z**2
        return out
    model = LocalModel(name, p, coord, True, tweedie_power=power)
    return np.array([log(law.atom_mass(row.observation)) if row.observation == 0
                     else law.log_density(row.observation)
                     for row in training.rows for law in (model.law(row.ensemble),)])
