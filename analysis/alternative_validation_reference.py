"""SC2 reference: reconstruct CDFs independently from saved parameter tags.

Uses SciPy reference probability laws and scalar Bernstein polynomial inversion,
not production distribution classes, production score expressions or saved scores.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping

import numpy as np
from scipy.optimize import brentq
from scipy.special import comb
from scipy.stats import gamma, logistic, lognorm, norm, t

from analysis.alternative_validation_io import mapping, number, sequence, text
from analysis.alternative_validation_oracles import (
    close,
    crps_integral,
    empirical_crps,
    floats,
    mean_integral,
    normal_absolute,
    tweedie_reference,
)
from analysis.calibration import FloatArray
from analysis.data_io import Json


def vector(value: Json) -> FloatArray:
    return np.array([number(v) for v in sequence(value)], dtype=np.float64)


def integration_splits(spec: Mapping[str, Json]) -> tuple[float, ...]:
    tag = spec.get("tag")
    if tag == "weighted_empirical":
        return floats(vector(spec["values"]))
    if tag == "bernstein":
        values = floats(vector(spec["coefficients"]))
        return (0., values[0], values[-1])
    if tag == "gamma":
        return (0., number(sequence(spec["parameters"])[2]))
    if tag == "mixture":
        return tuple(sorted({x for part in sequence(spec["parts"])
                             for x in integration_splits(mapping(part))}))
    if tag == "hurdle":
        return (0., *integration_splits(mapping(spec["positive"])))
    if tag == "affine":
        offset, scale = number(spec["offset"]), number(spec["scale"])
        return tuple(offset+scale*x for x in integration_splits(mapping(spec["base"])))
    if tag == "censored_gev":
        loc, scale, shape = floats(vector(spec["parameters"]))
        return (0., loc-scale/shape) if shape else (0.,)
    return (0.,)


def reference_cdf(spec: Mapping[str, Json]) -> Callable[[float], float]:
    if spec.get("kind") == "bayesian_scalar":
        locations, scales = vector(spec["locations"]), vector(spec["scales"])
        weights = vector(spec["weights"])
        degrees, transform = spec["df"], text(spec["transform"])
        if transform not in {"temperature", "sqrt", "yj", "logsinh"}:
            raise AssertionError("unsupported Bayesian transform; exp(Student) is forbidden")
        def bayes_cdf(value: float) -> float:
            if math.isinf(value):
                return 0. if value < 0 else 1.
            if transform != "temperature" and value < 0:
                return 0.
            if transform == "temperature":
                latent = (value-10)/10
            elif transform == "sqrt":
                latent = math.sqrt(value/100)
            elif transform == "yj":
                latent = 2*(math.sqrt(1+value/100)-1)
            else:
                u = 1+value/100
                latent = u+math.log1p(-math.exp(-2*u))-math.log(2)-math.log(math.sinh(1))
            standardized = (latent-locations)/scales
            probability = norm.cdf(standardized) if degrees is None else t.cdf(
                standardized, number(degrees))
            return float(np.sum(weights*probability))
        return bayes_cdf
    tag = text(spec["tag"])
    if tag == "weighted_empirical":
        values, weights = vector(spec["values"]), vector(spec["weights"])
        if abs(float(weights.sum()) - 1) > 1e-10 or np.any(weights <= 0):
            raise AssertionError("saved empirical mass is not normalized positive")
        return lambda x: float(np.sum(weights[values <= x]))
    if tag in ("normal", "student_t", "logistic", "lognormal", "gamma", "censored_gev"):
        p = floats(vector(spec["parameters"]))
        censor = spec.get("censor_zero", False)
        if tag == "normal":
            law = norm(loc=p[0], scale=p[1])
        elif tag == "student_t":
            law = t(df=p[0], loc=p[1], scale=p[2])
        elif tag == "logistic":
            law = logistic(loc=p[0], scale=p[1])
        elif tag == "lognormal":
            law = lognorm(s=p[1], scale=math.exp(p[0]))
        elif tag == "gamma":
            law = gamma(a=p[0], loc=p[2], scale=p[1])
        else:
            location, scale, shape = p
            def gev_cdf(value: float) -> float:
                if value < 0:
                    return 0.
                z = (value-location)/scale
                if shape:
                    support = 1+shape*z
                    if support <= 0:
                        return 1. if shape < 0 else 0.
                    log_exponent = -math.log(support)/shape
                else:
                    log_exponent = -z
                return 0. if log_exponent > math.log(745.) else math.exp(-math.exp(log_exponent))
            return gev_cdf
        return lambda x: 0. if censor and x < 0 else float(law.cdf(x))
    if tag == "affine":
        base = reference_cdf(mapping(spec["base"]))
        offset, scale = number(spec["offset"]), number(spec["scale"])
        if scale <= 0:
            raise AssertionError("reference affine requires strictly positive scale")
        return lambda x: base((x-offset)/scale)
    if tag == "power_censored":
        base = reference_cdf(mapping(spec["base"]))
        power, unit = number(spec["power"]), number(spec["unit_scale"])
        return lambda x: 0. if x < 0 else base(math.pow(x/unit, power))
    if tag == "hurdle":
        positive = reference_cdf(mapping(spec["positive"]))
        p0 = number(spec["p_zero"])
        return lambda x: 0. if x < 0 else p0+(1-p0)*positive(x)
    if tag == "mixture":
        parts = tuple(reference_cdf(mapping(p)) for p in sequence(spec["parts"]))
        weights = vector(spec["weights"])
        if len(parts) != len(weights) or abs(float(weights.sum())-1) > 1e-10:
            raise AssertionError("reference mixture mass does not sum to 1")
        return lambda x: math.fsum(w*part(x) for w, part in zip(floats(weights), parts, strict=True))
    if tag == "tweedie":
        mu, phi, power = number(spec["mu"]), number(spec["phi"]), number(spec["power"])
        return lambda x: (0. if x < 0 else 1. if math.isinf(x) else
                          tweedie_reference(mu, phi, power, x)[0])
    if tag == "bernstein":
        coefficients = floats(vector(spec["coefficients"]))
        n = len(coefficients)-1
        p0 = number(spec["p_zero"])
        if np.any(np.diff(np.array(coefficients)) < 0):
            raise AssertionError("saved Bernstein coefficients cross")
        def cdf(x: float) -> float:
            if p0 and x < 0:
                return 0.
            if x < coefficients[0]:
                return p0 if x >= 0 else 0.
            if x >= coefficients[-1]:
                return 1.
            def polynomial(p: float) -> float:
                return math.fsum(coefficients[k]*float(comb(n, k)) *
                                 p**k*(1-p)**(n-k) for k in range(n+1))-x
            probability = brentq(polynomial, 0, 1, xtol=1e-13)
            return p0+(1-p0)*float(probability)
        return cdf
    raise AssertionError(f"independent reference lacks distribution tag {tag}")


def reference_mean(spec: Mapping[str, Json]) -> float:
    if spec.get("kind") == "bayesian_scalar":
        if spec["transform"] == "temperature":
            return 10+10*float(np.sum(vector(spec["locations"])*vector(spec["weights"])))
        if spec["df"] is not None:
            minimum = 2 if spec["transform"] in {"sqrt", "yj"} else 1
            if number(spec["df"]) <= minimum:
                raise AssertionError("Bayesian inverse-transform mean does not exist")
        return mean_integral(reference_cdf(spec), 100., integration_splits(spec))
    tag = text(spec["tag"])
    if tag == "weighted_empirical":
        return float(vector(spec["values"]) @ vector(spec["weights"]))
    if tag == "tweedie":
        return number(spec["mu"])
    if tag == "bernstein":
        return (1-number(spec["p_zero"]))*float(np.mean(vector(spec["coefficients"])))
    if tag == "mixture":
        return math.fsum(number(w)*reference_mean(mapping(p)) for w, p in zip(
            sequence(spec["weights"]), sequence(spec["parts"]), strict=True))
    if tag == "affine":
        return number(spec["offset"])+number(spec["scale"])*reference_mean(mapping(spec["base"]))
    if tag == "hurdle":
        return (1-number(spec["p_zero"]))*reference_mean(mapping(spec["positive"]))
    scale = 1.
    if tag in {"normal", "logistic", "student_t", "lognormal", "gamma", "censored_gev"}:
        parameters = floats(vector(spec["parameters"]))
        if tag in {"normal", "logistic"}:
            if not spec.get("censor_zero"):
                return parameters[0]
            scale = max(1., abs(parameters[0]), parameters[1])
        elif tag == "student_t":
            if parameters[0] <= 1:
                raise AssertionError("Student original-unit mean does not exist")
            return parameters[1]
        elif tag == "lognormal":
            return math.exp(parameters[0]+parameters[1]**2/2)
        elif tag == "gamma":
            if not spec.get("censor_zero"):
                return parameters[0]*parameters[1]+parameters[2]
            scale = max(1., parameters[0]*parameters[1], abs(parameters[2]))
        else:
            scale = max(1., abs(parameters[0]), parameters[1])
    elif tag == "power_censored":
        scale = number(spec["unit_scale"])
    return mean_integral(reference_cdf(spec), scale, integration_splits(spec))


def reference_crps(spec: Mapping[str, Json], observation: float) -> float:
    tag = spec.get("tag")
    if tag == "weighted_empirical":
        return empirical_crps(vector(spec["values"]), vector(spec["weights"]), observation)
    splits = integration_splits(spec)
    scale = max(1., abs(reference_mean(spec)))
    return crps_integral(reference_cdf(spec), observation, splits, scale).value


def reference_examples() -> dict[str, Json]:
    """SC2 machine receipt with independently computed EXPECTED values."""
    specifications: dict[str, dict[str, Json]] = {
        "normal": {"tag": "normal", "parameters": [0., 1.], "censor_zero": False},
        "censored_normal": {"tag": "normal", "parameters": [-2., 1.], "censor_zero": True},
        "weighted_ties": {"tag": "weighted_empirical", "values": [0., 2., 5.],
                          "weights": [.3, .3, .4]},
        "mixture": {"tag": "mixture", "parts": [
            {"tag": "normal", "parameters": [-2., 1.], "censor_zero": False},
            {"tag": "normal", "parameters": [2., 1.], "censor_zero": False}],
            "weights": [.5, .5]},
        "sqrt_inverse": {"tag": "power_censored", "base": {
            "tag": "normal", "parameters": [0., 1.], "censor_zero": False},
            "power": .5, "unit_scale": 100.},
    }
    records: dict[str, Json] = {}
    for name, spec in specifications.items():
        records[name] = {"distribution_spec": spec, "observation": 1.,
                         "expected_mean": reference_mean(spec),
                         "expected_crps": reference_crps(spec, 1.),
                         "expected_cdf_at_zero": reference_cdf(spec)(0.)}
    close(reference_crps(specifications["normal"], 1.),
          normal_absolute(1., 1.)-1/math.sqrt(math.pi), "SC2 known Normal")
    close(reference_crps(specifications["weighted_ties"], 1.), 1.06, "SC2 pair oracle")
    close(reference_mean(specifications["sqrt_inverse"]), 50., "SC2 Jensen inverse")
    return {"status": "PASS", "formulas": "SCIPY_CDF_QUADRATURE_AND_O_N_SQUARED_EXPECTATION",
            "expected_not_copied_from_production_scores": records}
