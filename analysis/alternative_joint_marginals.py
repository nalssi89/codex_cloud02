"""Fixed original EMOS marginal adapter for coupling, never a selected winner."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

import numpy as np

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FitConfig,
    FittedModel,
    PredictiveDistribution,
    TrainingSet,
)
from analysis.alternative_distributions import normal
from analysis.calibration import calibrate
from analysis.data_io import Json


@dataclass(frozen=True, slots=True, kw_only=True)
class EmosMarginal:
    parameters: tuple[float, float, float, float]
    rain: bool

    def predict(self, target: CaseInput) -> PredictiveDistribution:
        a, b, c, d = self.parameters
        variance = float(np.var(target.members, ddof=1)) if target.members.size > 1 else 0.0
        return normal(a + b * float(np.mean(target.members)), sqrt(c + d * variance),
                      censor_zero=self.rain)

    def to_spec(self) -> dict[str, Json]:
        return {"type": "original_emos", "parameters": list(self.parameters), "rain": self.rain}


def fit_emos_marginal(training: TrainingSet, config: FitConfig) -> EmosMarginal:
    """Use the original CRPS-fitted analytic law with its unchanged calibration call."""
    del config
    result = calibrate(
        training.target.members, tuple(row.ensemble for row in training.rows),
        training.local_observations, training.target.variable == "prcp",
    )
    if not result.converged:
        raise AlternativeError("EMOS_ANCESTOR_FIT_FAILED", result.optimizer_message)
    return EmosMarginal(parameters=result.parameters, rain=training.target.variable == "prcp")


def fit_bjp_marginal(training: TrainingSet, config: FitConfig) -> FittedModel:
    """Use the fixed primary BJP law, never target-score-selected Bayesian variants."""
    from analysis.alternative_bayes import bayesian_method_specs, fit_bayes

    identifier = "bjp_sqrt_censored" if training.target.variable == "prcp" else "bjp_niw"
    specification = next(spec for spec in bayesian_method_specs() if spec.id == identifier)
    result = fit_bayes(specification, training, config)
    if result.fitted_model is None:
        raise AlternativeError("BJP_ANCESTOR_FIT_FAILED", result.diagnostics.message)
    return result.fitted_model
