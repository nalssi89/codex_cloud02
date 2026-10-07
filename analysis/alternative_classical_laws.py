"""Original-unit predictive laws for classical local regressions."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log, pow, sqrt

from scipy.special import expit

from analysis.alternative_classical_common import Coordinates, moments, softplus
from analysis.alternative_contracts import CaseInput, PredictiveDistribution
from analysis.alternative_distributions import (
    censored_gev,
    gamma,
    hurdle,
    logistic,
    lognormal,
    normal,
    power_censored,
    tweedie,
)
from analysis.calibration import FloatArray
from analysis.data_io import Json


@dataclass(frozen=True, slots=True)
class LocalModel:
    method_id: str
    parameters: FloatArray
    coord: Coordinates
    rain: bool
    climate_mean: float = 0.0
    tweedie_power: float = 1.5

    def law(self, ensemble: FloatArray) -> PredictiveDistribution:
        p = self.parameters
        a, b, c = (p.item(i) for i in range(3))
        m, v = moments(ensemble, self.coord)
        s = sqrt(v)
        name = self.method_id
        d = p.item(3) if p.size > 3 else 0.0
        if name in ("emos", "anomaly_mos", "emos_constant_variance", "mos_unit_slope"):
            mu = self.climate_mean + b * (m - self.coord.mean_center
                                         ) if name == "anomaly_mos" else a + b * m
            return normal(self.coord.offset + self.coord.scale * mu,
                          self.coord.scale * sqrt(c + d * v), self.rain)
        if name in ("gamma_positive", "csg_fixed_shift", "csg_estimated_shift"):
            mu = softplus(a + b * m) + 1e-6
            var = softplus(c) + softplus(d) * v + 1e-6
            delta = (softplus(p.item(4)) if name == "csg_estimated_shift"
                     else 0.1 if name == "csg_fixed_shift" else 0.0)
            return gamma(mu * mu / var, self.coord.scale * var / mu,
                         shift=-self.coord.scale * delta,
                         censor_zero=name != "gamma_positive")
        if name.startswith("power_"):
            power = 0.5 if name.endswith("sqrt") else 1.0 / 3.0
            powered = (ensemble / self.coord.scale)**power
            ps = float(powered.std(ddof=1)) if powered.size > 1 else 0.0
            mu = a + b * pow(max(m, 0.0), power)
            scale = exp(c + d * log(1.0 + ps))
            base = logistic(mu, scale) if "logistic" in name else normal(mu, scale)
            return power_censored(base, power, self.coord.scale)
        if name.startswith("hurdle_"):
            x = (m - self.coord.mean_center) / self.coord.mean_scale
            p0 = float(expit(p.item(3) + p.item(4) * x))
            if name == "hurdle_gamma":
                mu, shape = exp(a + b * x), exp(c)
                positive = gamma(shape, self.coord.scale * mu / shape)
            else:
                positive = lognormal(log(self.coord.scale) + a + b * x, exp(c))
            return hurdle(p0, positive)
        if name.startswith("gev_"):
            xi = p.item(4) if p.size > 4 else 0.0
            return censored_gev(self.coord.scale * (a + b * m),
                                self.coord.scale * exp(c + d * log(1.0 + s)), xi)
        if name.startswith("tweedie_"):
            x = (log(1.0 + max(m, 0.0)) - self.coord.log_center) / self.coord.log_scale
            mu = exp(a + b * x)
            return tweedie(self.coord.scale * mu,
                           exp(c) * pow(self.coord.scale, 2.0 - self.tweedie_power),
                           self.tweedie_power)
        raise ValueError(f"Unrecognized local law: {name}")

    def predict(self, target: CaseInput) -> PredictiveDistribution:
        return self.law(target.members)

    def to_spec(self) -> dict[str, Json]:
        return {"kind": "classical_local", "method_id": self.method_id,
                "parameters": self.parameters.tolist(),
                "coordinate_offset": self.coord.offset, "coordinate_scale": self.coord.scale,
                "mean_center": self.coord.mean_center, "mean_scale": self.coord.mean_scale,
                "log_center": self.coord.log_center, "log_scale": self.coord.log_scale,
                "rain": self.rain, "climate_mean": self.climate_mean,
                "tweedie_power": self.tweedie_power}
