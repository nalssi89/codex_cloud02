"""Original-unit predictive distributions and explicit tagged JSON restoration.

Gamma ``shift`` is an additive location: CSG uses ``shift=-delta``.
Power ``power`` is the forward physical-to-latent exponent (sqrt: 0.5).
"""

from __future__ import annotations

import math
from collections.abc import Mapping

import numpy as np

from analysis.alternative_contracts import PredictiveDistribution
from analysis.alternative_distribution_base import (
    Empirical,
    ScientificLaw,
    array,
    empirical,
    floats,
    normalized,
)
from analysis.alternative_distribution_bernstein import Bernstein
from analysis.alternative_distribution_integrals import cdf_crps
from analysis.alternative_distribution_mixture import Mixture
from analysis.alternative_distribution_transforms import Affine, Hurdle, PowerCensored
from analysis.calibration import FloatArray
from analysis.data_io import Json

__all__ = ["affine", "bernstein", "cdf_crps", "censored_gev", "distribution_from_spec",
           "gamma", "hurdle", "logistic", "lognormal", "mixture", "normal",
           "power_censored", "student_t", "tweedie", "weighted_empirical"]


def _finite(*values: float) -> None:
    if not all(math.isfinite(x) for x in values):
        raise ValueError("distribution parameters must be finite")


def weighted_empirical(values: FloatArray, weights: FloatArray) -> PredictiveDistribution:
    return empirical(values, weights)


def _point(value: float) -> PredictiveDistribution:
    return empirical(array([value]), array([1.0]))


def normal(mu: float, sigma: float, censor_zero: bool = False) -> PredictiveDistribution:
    _finite(mu, sigma)
    if sigma < 0:
        raise ValueError("sigma must be nonnegative")
    if sigma == 0:
        return _point(max(0, mu) if censor_zero else mu)
    return ScientificLaw(tag="normal", parameters=(mu, sigma), censor_zero=censor_zero)


def student_t(df: float, loc: float, scale: float) -> PredictiveDistribution:
    _finite(df, loc, scale)
    if df <= 1 or scale < 0:
        raise ValueError("Student df must exceed 1 (finite mean), scale nonnegative")
    return _point(loc) if scale == 0 else ScientificLaw(tag="student_t", parameters=(df, loc, scale))


def logistic(loc: float, scale: float) -> PredictiveDistribution:
    _finite(loc, scale)
    if scale < 0:
        raise ValueError("scale must be nonnegative")
    return _point(loc) if scale == 0 else ScientificLaw(tag="logistic", parameters=(loc, scale))


def lognormal(log_mu: float, log_sigma: float) -> PredictiveDistribution:
    _finite(log_mu, log_sigma)
    if log_sigma < 0 or log_mu+log_sigma**2/2 > math.log(np.finfo(float).max):
        raise ValueError("lognormal must have nonnegative sigma and finite mean")
    return (_point(math.exp(log_mu)) if log_sigma == 0 else
            ScientificLaw(tag="lognormal", parameters=(log_mu, log_sigma)))


def affine(base: PredictiveDistribution, offset: float, scale: float) -> PredictiveDistribution:
    _finite(offset, scale)
    return _point(offset) if scale == 0 else Affine(base=base, offset=offset, scale=scale)


def gamma(shape: float, scale: float, shift: float = 0.0,
          censor_zero: bool = False) -> PredictiveDistribution:
    _finite(shape, scale, shift)
    if shape <= 0 or scale < 0:
        raise ValueError("Gamma shape positive, scale nonnegative required")
    if scale == 0:
        return _point(max(0, shift) if censor_zero else shift)
    return ScientificLaw(tag="gamma", parameters=(shape, scale, shift), censor_zero=censor_zero)


def power_censored(base: PredictiveDistribution, power: float,
                   unit_scale: float) -> PredictiveDistribution:
    _finite(power, unit_scale)
    if power <= 0 or unit_scale <= 0:
        raise ValueError("power and unit_scale must be positive")
    if (isinstance(base, ScientificLaw) and base.tag == "student_t"
            and base.parameters[0] <= 1/power):
        raise ValueError("latent Student df must exceed inverse power for a finite rain mean")
    return PowerCensored(base=base, power=power, unit_scale=unit_scale)


def hurdle(p_zero: float, positive: PredictiveDistribution) -> PredictiveDistribution:
    _finite(p_zero)
    if not 0 <= p_zero <= 1 or float(positive.cdf(array(0))) != 0:
        raise ValueError("hurdle needs p_zero in [0,1] and strictly positive intensity")
    return _point(0) if p_zero == 1 else Hurdle(p_zero=p_zero, positive=positive)


def mixture(parts: tuple[PredictiveDistribution, ...],
            weights: FloatArray) -> PredictiveDistribution:
    w = normalized(weights)
    if len(parts) != w.size:
        raise ValueError("one weight is required per component")
    retained = tuple(part for part, weight in zip(parts, floats(w)) if weight > 0)
    w = normalized(w[w > 0])
    if len(retained) == 1:
        return retained[0]
    empirical_parts = tuple(part for part in retained if isinstance(part, Empirical))
    if len(empirical_parts) == len(retained):
        values = array([x for part in empirical_parts for x in floats(part.values)])
        masses = array([weight*mass for part, weight in zip(empirical_parts, floats(w))
                        for mass in floats(part.weights)])
        return empirical(values, masses)
    return Mixture(parts=retained, weights=w)


def censored_gev(loc: float, scale: float, shape: float) -> PredictiveDistribution:
    _finite(loc, scale, shape)
    if scale < 0 or shape >= 1:
        raise ValueError("GEV needs nonnegative scale and shape<1 for finite mean")
    if scale == 0:
        return _point(max(0, loc))
    return ScientificLaw(tag="censored_gev", parameters=(loc, scale, shape), censor_zero=True)


def tweedie(mu: float, phi: float, power: float) -> PredictiveDistribution:
    from analysis.alternative_distribution_tweedie import Tweedie

    return Tweedie(mu=mu, phi=phi, power=power)


def bernstein(coefficients: FloatArray, p_zero: float = 0.0) -> PredictiveDistribution:
    c = array(coefficients).copy()
    _finite(p_zero)
    if (c.ndim != 1 or c.size < 1 or np.any(~np.isfinite(c))
            or np.any(np.diff(c) < 0) or not 0 <= p_zero <= 1):
        raise ValueError("finite nondecreasing coefficient vector and p_zero in [0,1] required")
    if p_zero > 0 and c[0] <= 0:
        raise ValueError("rain Bernstein intensity must be strictly positive")
    c.flags.writeable = False
    return _point(0) if p_zero == 1 else Bernstein(coefficients=c, p_zero=p_zero)


def _number(spec: Mapping[str, Json], key: str) -> float:
    value = spec[key]
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"{key} must be numeric")
    return float(value)


def _vector(spec: Mapping[str, Json], key: str) -> FloatArray:
    value = spec[key]
    if not isinstance(value, list):
        raise TypeError(f"{key} must be a numeric list")
    numbers: list[float] = []
    for x in value:
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            raise TypeError(f"{key} must contain numbers")
        numbers.append(float(x))
    return array(numbers)


def _nested(spec: Mapping[str, Json], key: str) -> PredictiveDistribution:
    value = spec[key]
    if not isinstance(value, dict):
        raise TypeError(f"{key} must be a tagged distribution object")
    return distribution_from_spec(value)


def distribution_from_spec(spec: Mapping[str, Json]) -> PredictiveDistribution:
    if spec.get("kind") == "bayesian_scalar":
        from analysis.alternative_bayes_distribution import (
            distribution_from_spec as restore_bayesian_scalar,
        )

        return restore_bayesian_scalar(spec)
    tag = spec.get("tag")
    if tag == "weighted_empirical":
        return weighted_empirical(_vector(spec, "values"), _vector(spec, "weights"))
    if tag in ("normal", "student_t", "logistic", "lognormal", "gamma", "censored_gev"):
        p = floats(_vector(spec, "parameters"))
        censor = spec.get("censor_zero", False)
        if not isinstance(censor, bool):
            raise ValueError("censor_zero must be boolean")
        if tag == "normal" and len(p) == 2:
            return normal(float(p[0]), float(p[1]), censor)
        if tag == "student_t" and len(p) == 3:
            return student_t(float(p[0]), float(p[1]), float(p[2]))
        if tag == "logistic" and len(p) == 2:
            return logistic(float(p[0]), float(p[1]))
        if tag == "lognormal" and len(p) == 2:
            return lognormal(float(p[0]), float(p[1]))
        if tag == "gamma" and len(p) == 3:
            return gamma(float(p[0]), float(p[1]), float(p[2]), censor)
        if tag == "censored_gev" and len(p) == 3:
            return censored_gev(float(p[0]), float(p[1]), float(p[2]))
        raise ValueError(f"invalid parameter count for {tag}")
    if tag == "affine":
        return affine(_nested(spec, "base"), _number(spec, "offset"), _number(spec, "scale"))
    if tag == "power_censored":
        return power_censored(_nested(spec, "base"), _number(spec, "power"),
                              _number(spec, "unit_scale"))
    if tag == "hurdle":
        return hurdle(_number(spec, "p_zero"), _nested(spec, "positive"))
    if tag == "mixture":
        parts = spec["parts"]
        if not isinstance(parts, list):
            raise ValueError("parts must be a list")
        laws: list[PredictiveDistribution] = []
        for part in parts:
            if not isinstance(part, dict):
                raise TypeError("each mixture part must be a tagged object")
            laws.append(distribution_from_spec(part))
        return mixture(tuple(laws), _vector(spec, "weights"))
    if tag == "tweedie":
        return tweedie(_number(spec, "mu"), _number(spec, "phi"), _number(spec, "power"))
    if tag == "bernstein":
        return bernstein(_vector(spec, "coefficients"), _number(spec, "p_zero"))
    raise ValueError(f"unknown distribution tag: {tag!r}")
