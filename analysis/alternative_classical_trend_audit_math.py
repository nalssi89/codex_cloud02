"""Independent row-boundary and restored-trend mathematical audit."""

from __future__ import annotations

from dataclasses import replace
from datetime import date
from math import log, sqrt

import numpy as np
from scipy.special import log_ndtr

from analysis.alternative_classical_trend import TrendModel
from analysis.alternative_contracts import CaseInput, TrainingSet
from analysis.alternative_distributions import normal, power_censored
from analysis.calibration import FloatArray, calibrate


def audit_restoration(model: TrendModel, training: TrainingSet,
                      objective: float | None) -> None:
    """Future forecast trend is removed, while observed trend alone is restored."""
    target = training.target
    delta = 2.0  # Twenty years is two decades; no wall-clock waiting.
    latent = np.sqrt(target.members/model.unit_scale) if model.rain else target.members
    future_latent = latent + model.forecast_slope*delta
    if model.rain:
        assert np.all(future_latent >= 0)
    future = replace(target, init=date(target.init.year+20, target.init.month, target.init.day),
                     valid_start=date(target.valid_start.year+20, target.valid_start.month,
                                      target.valid_start.day),
                     valid_end=date(target.valid_end.year+20, target.valid_end.month,
                                    target.valid_end.day),
                     members=model.unit_scale*future_latent**2 if model.rain else future_latent)
    probability = np.array([0.05, 0.5, 0.95])
    old = model.predict(target)
    new = model.predict(future)
    if not model.rain:
        np.testing.assert_allclose(new.quantile(probability),
                                   old.quantile(probability)+model.observed_slope*delta,
                                   rtol=1e-10, atol=1e-10)
    elif model.method_id == "detrend_emos":
        time = (target.valid_start.year-model.time_center)/10
        residual_members = latent-model.forecast_slope*time
        a, b, c, d = (model.parameters.item(i) for i in range(4))
        mu = float(a+b*residual_members.mean()+model.observed_slope*time)
        sigma = sqrt(c+d*float(residual_members.var(ddof=1)))
        latent_quantiles = normal(mu, sigma).quantile(probability)
        expected = model.unit_scale*np.maximum(
            latent_quantiles+model.observed_slope*delta, 0)**2
        np.testing.assert_allclose(new.quantile(probability), expected, rtol=1e-10, atol=1e-10)
    else:
        audit_mapping(model, training, future)
    if not model.rain or model.method_id != "detrend_emos":
        return
    assert objective is not None
    weights = training.year_weights
    boundaries: list[float] = []
    dry_boundaries: list[float] = []
    losses: list[float] = []
    dry_fixed_loss = 0.0
    dry_variable_loss = 0.0
    for row, index in zip(training.rows, range(weights.size), strict=True):
        weight = weights.item(index)
        time = (row.source_year-model.time_center)/10
        boundary = -model.observed_slope*time
        boundaries.append(boundary)
        x = np.sqrt(row.ensemble/model.unit_scale)-model.forecast_slope*time
        a, b, c, d = (model.parameters.item(i) for i in range(4))
        residual_mu = float(a+b*x.mean())
        sigma = sqrt(c+d*float(x.var(ddof=1)))
        restored = power_censored(
            normal(residual_mu+model.observed_slope*time, sigma),
            power=0.5, unit_scale=model.unit_scale,
        )
        if row.observation == 0:
            dry_boundaries.append(boundary)
            log_masses: FloatArray = log_ndtr(np.array([
                (boundary-residual_mu)/sigma, -residual_mu/sigma,
            ]))
            expected_log_mass = log_masses.item(0)
            actual_log_mass = log(restored.atom_mass(0.0))
            np.testing.assert_allclose(actual_log_mass, expected_log_mass, atol=1e-12)
            losses.append(-actual_log_mass)
            dry_variable_loss -= float(weight)*expected_log_mass
            dry_fixed_loss -= float(weight)*log_masses.item(1)
        else:
            losses.append(-restored.log_density(row.observation))
    # The dry rows must span distinct positive and negative residual boundaries.
    assert min(boundaries) < 0 < max(boundaries)
    assert np.ptp(dry_boundaries) > 1e-3
    assert abs(dry_variable_loss-dry_fixed_loss) > 1e-3
    b, d = model.parameters.item(1), model.parameters.item(3)
    oracle = float(weights @ np.array(losses)) + 0.5*float(b*b+d*d)
    np.testing.assert_allclose(objective, oracle, rtol=1e-11, atol=1e-10)


def audit_mapping(model: TrendModel, training: TrainingSet,
                  future: CaseInput | None = None) -> None:
    """Compare signed detrended QM/QDM to the existing calibration implementation."""
    if model.method_id == "detrend_emos":
        return
    historical = tuple(
        (np.sqrt(row.ensemble/model.unit_scale) if model.rain else row.ensemble)
        - model.forecast_slope*(row.source_year-model.time_center)/10
        for row in training.rows
    )
    actual = np.array([
        (sqrt(row.observation/model.unit_scale) if model.rain else row.observation)
        - model.observed_slope*(row.source_year-model.time_center)/10
        for row in training.rows
    ])
    targets = [training.target]
    if future is not None:
        targets.append(future)
    # Tied issued members must preserve the original average-rank convention.
    targets.append(replace(training.target, members=np.array([0.0, 0.0, 8.0, 8.0])))
    for target in targets:
        time = (target.valid_start.year-model.time_center)/10
        members = np.sqrt(target.members/model.unit_scale) if model.rain else target.members
        forecast = members-model.forecast_slope*time
        # False is deliberate: the frozen rain QDM is additive on signed latent
        # coordinates, not the existing multiplicative original-mm rain QDM.
        original = calibrate(forecast, historical, actual, precipitation=False)
        mapped = original.qm if model.method_id == "detrend_qm" else original.qdm
        restored = mapped+model.observed_slope*time
        if model.rain:
            restored = model.unit_scale*np.maximum(restored, 0.0)**2
        law = model.predict(target)
        np.testing.assert_allclose(law.mean(), restored.mean(), rtol=1e-12, atol=1e-12)
        expected_values, counts = np.unique(restored, return_counts=True)
        probability = (np.arange(restored.size)+0.5)/restored.size
        np.testing.assert_allclose(law.quantile(probability), np.sort(restored),
                                   rtol=1e-12, atol=1e-12)
        # Compare masses between knots, not exact floating-point interpolation
        # outputs whose final-bit accumulation order can differ.
        probes = np.concatenate(((expected_values[:-1]+expected_values[1:])/2,
                                 [expected_values[-1]+1]))
        np.testing.assert_allclose(law.cdf(probes), np.cumsum(counts)/counts.sum(),
                                   rtol=1e-12, atol=1e-12)
