"""Regression for shared restoration of issued Bayesian and nested laws."""

from __future__ import annotations

import json
from time import perf_counter

import numpy as np

from analysis.alternative_bayes import bayesian_method_specs, fit_bayes
from analysis.alternative_bayes_audit import synthetic
from analysis.alternative_contracts import FitConfig, FitStatus, PredictiveDistribution
from analysis.alternative_distributions import distribution_from_spec, mixture, normal
from analysis.alternative_validation_io import decode, mapping


def check(law: PredictiveDistribution) -> None:
    serialized = mapping(decode(json.dumps(law.to_spec(), allow_nan=False)))
    restored = distribution_from_spec(serialized)
    probabilities = np.asarray([0.05, 1 / 3, 0.5, 2 / 3, 0.95])
    quantiles = law.quantile(probabilities)
    np.testing.assert_allclose(restored.quantile(probabilities), quantiles, atol=1e-10, rtol=0)
    np.testing.assert_allclose(restored.cdf(quantiles), law.cdf(quantiles), atol=1e-12, rtol=0)
    np.testing.assert_allclose(restored.cdf_left(quantiles), law.cdf_left(quantiles),
                               atol=1e-12, rtol=0)
    np.testing.assert_allclose(restored.mean(), law.mean(), atol=1e-12, rtol=0)
    np.testing.assert_allclose(restored.atom_mass(0), law.atom_mass(0), atol=1e-12, rtol=0)
    probe = float(quantiles.item(2))
    np.testing.assert_allclose(restored.crps(probe), law.crps(probe), atol=1e-10, rtol=0)
    np.testing.assert_allclose(restored.log_density(probe), law.log_density(probe),
                               atol=1e-12, rtol=0)


def main() -> None:
    started = perf_counter()
    checks = 0
    for rain, method in ((False, "bjp_niw"), (True, "bjp_sqrt_censored")):
        training = synthetic(rain)
        spec = next(spec for spec in bayesian_method_specs() if spec.id == method)
        result = fit_bayes(spec, training, FitConfig(workers=1))
        assert result.status == FitStatus.OK and result.fitted_model is not None
        law = result.fitted_model.predict(training.target)
        check(law)
        nested = mixture((normal(10, 2, censor_zero=rain), law), np.asarray([0.25, 0.75]))
        check(nested)
        checks += 2
    print(json.dumps({"status": "PASS", "restored_laws": checks,
                      "elapsed_seconds": perf_counter() - started}, allow_nan=False))


if __name__ == "__main__":
    main()
