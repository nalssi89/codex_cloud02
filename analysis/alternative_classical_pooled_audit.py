"""Executable synthetic mathematical checks for pooled and deterministic trends."""

from __future__ import annotations

import json
from dataclasses import replace
from math import exp, pi, sqrt
from time import perf_counter
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
from scipy.special import ndtr

from analysis.alternative_classical import fit_classical
from analysis.alternative_classical_pooled import IDS as POOLED_IDS
from analysis.alternative_classical_pooled import fit_pooled
from analysis.alternative_classical_pooled_audit_gradient import (
    audit_optimizer,
    synthetic_spec,
    synthetic_training,
)
from analysis.alternative_classical_trend import IDS as TREND_IDS
from analysis.alternative_classical_trend import fit_trend
from analysis.alternative_classical_trend_audit_math import (
    audit_mapping,
    audit_restoration,
)
from analysis.alternative_contracts import (
    FitConfig,
    FitStatus,
)
from analysis.calibration import FloatArray, gaussian_crps


def main() -> None:
    """Exercise laws, mathematical identities, weighting, gates and solver failure."""
    started = perf_counter()
    config = FitConfig(workers=1)
    evidence: list[dict[str, object]] = []
    for pooled, ids, fit in ((True, POOLED_IDS, fit_pooled), (False, TREND_IDS, fit_trend)):
        for rain in (False, True):
            training = synthetic_training(rain, pooled)
            for method in ids:
                if pooled:
                    with audit_optimizer(training, method):
                        result = fit_classical(synthetic_spec(method, pooled), training, config)
                else:
                    result = fit_classical(synthetic_spec(method, pooled), training, config)
                assert result.status == FitStatus.OK, (method, rain, result.diagnostics)
                model = result.fitted_model
                assert model is not None and result.diagnostics.convergence
                law = model.predict(training.target)
                cdf = law.cdf(np.array([-np.inf, 0., 10., np.inf]))
                assert cdf[0] == 0 and cdf[-1] == 1 and np.all(np.diff(cdf) >= 0)
                assert np.isfinite(law.mean()) and np.isfinite(law.crps(5.))
                quantile = law.quantile(np.array([.05, .5, .95]))
                assert np.all(np.diff(quantile) >= 0)
                assert not rain or (quantile.min() >= 0 and law.cdf(np.array([-1.]))[0] == 0)
                singleton = replace(training.target, members=np.array([0.]))
                singleton_law = model.predict(singleton)
                assert np.isfinite(singleton_law.mean()) and np.isfinite(singleton_law.crps(0.))
                _ = json.dumps(model.to_spec(), allow_nan=False)
                _ = json.dumps(law.to_spec(), allow_nan=False)
                if pooled:
                    duplicate = replace(training, rows=training.rows*2,
                                        year_weights=np.tile(training.year_weights/2, 2))
                    duplicate_result = fit(synthetic_spec(method, pooled), duplicate, config)
                    assert duplicate_result.fitted_model is not None
                    duplicate_quantile = duplicate_result.fitted_model.predict(training.target).quantile(
                        np.array([.05, .5, .95]))
                    np.testing.assert_allclose(duplicate_quantile, quantile, atol=3e-4, rtol=3e-4)
                else:
                    from analysis.alternative_classical_trend import TrendModel

                    assert isinstance(model, TrendModel)
                    audit_restoration(model, training, result.diagnostics.objective)
                    audit_mapping(model, training)
                    t = np.array([(r.source_year-model.time_center)/10 for r in training.rows])
                    response = np.sqrt(training.local_observations/model.unit_scale) if rain else (
                        training.local_observations)
                    expected = float(t @ (response-response.mean())) / (float(t @ t)+1)
                    np.testing.assert_allclose(model.observed_slope, expected, atol=1e-12)
                    if method == "detrend_emos" and rain:
                        a, b, c, d = (model.parameters.item(i) for i in range(4))
                        time = (training.target.valid_start.year-model.time_center)/10
                        latent_members: FloatArray = np.array([
                            sqrt(training.target.members.item(i)/model.unit_scale)
                            for i in range(training.target.members.size)
                        ])
                        x = latent_members-model.forecast_slope*time
                        mu = a + b*float(x.mean()) + model.observed_slope*time
                        sigma = sqrt(c+d*float(x.var(ddof=1)))
                        probabilities: FloatArray = ndtr(np.array([-mu/sigma, mu/sigma]))
                        expected_atom = probabilities.item(0)
                        np.testing.assert_allclose(law.cdf(np.array([0.])).item(0), expected_atom, atol=1e-12)
                        expected_mean = model.unit_scale*((mu*mu+sigma*sigma)*probabilities.item(1)
                            + mu*sigma*exp(-.5*(mu/sigma)**2)/sqrt(2*pi))
                        np.testing.assert_allclose(law.mean(), expected_mean, rtol=1e-6, atol=1e-6)
                evidence.append({"method": method, "rain": rain, "status": str(result.status),
                                 "elapsed_seconds": result.diagnostics.elapsed_seconds,
                                 "objective": result.diagnostics.objective})
            insufficient = replace(training, rows=training.rows[:3],
                                   year_weights=training.year_weights[:3])
            assert fit(synthetic_spec(ids[0], pooled), insufficient, config).status == FitStatus.INSUFFICIENT_TRAINING
            failed = SimpleNamespace(success=False, message="injected optimizer failure")
            module = "pooled" if pooled else "trend"
            optimized = ids[0] if pooled else ids[2]
            with patch(f"analysis.alternative_classical_{module}.minimize", return_value=failed):
                failure = fit(synthetic_spec(optimized, pooled), training, config)
                assert failure.status == FitStatus.FIT_FAILED and failure.fitted_model is None
        dry = synthetic_training(True, pooled, zeros=True)
        for method in ids:
            dry_result = fit(synthetic_spec(method, pooled), dry, config)
            assert dry_result.status == FitStatus.OK, (method, dry_result.diagnostics)
            assert dry_result.fitted_model is not None
            dry_law = dry_result.fitted_model.predict(dry.target)
            assert np.isfinite(dry_law.mean()) and np.isfinite(dry_law.crps(0.))
    # Independent normal CRPS identity at the median.
    score = gaussian_crps(np.array([0.]), np.array([2.]), np.array([0.])).item(0)
    np.testing.assert_allclose(score, 2*(sqrt(2)-1)/sqrt(pi), atol=1e-12)
    print(json.dumps({"fits": evidence, "checks": "12 primary fits plus six all-dry fits, singleton "
                     + "zero forecasts, duplicate-year-weight invariance, "
                     + "original-unit F9 objective and independent finite-difference gradients, "
                     + "ridge normal equations, restored rain atom/mean, laws, serialization, "
                     + "variable censor boundaries, 20-year future restoration, original QM/QDM "
                     + "mapping parity including ties, dispatcher routing by mismatched subtype, "
                     + "insufficient years, injected solver failure, normal CRPS identity",
                     "elapsed_seconds": perf_counter()-started}, indent=2))


if __name__ == "__main__":
    main()
