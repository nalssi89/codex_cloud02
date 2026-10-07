"""Executable mathematical/adversarial QA; no targets or output trees touched."""

from __future__ import annotations

import hashlib
import json
import math
import time
from collections.abc import Callable
from pathlib import Path

import numpy as np
from scipy import stats
from scipy.integrate import quad

from analysis import alternative_distributions as d
from analysis.alternative_contracts import PredictiveDistribution
from analysis.alternative_distribution_base import array, floats
from analysis.alternative_distribution_tweedie import Tweedie
from analysis.alternative_validation_distributions import production_checks
from analysis.data_io import Json


def close(actual: float, expected: float, label: str, tolerance: float = 2e-7) -> None:
    if not math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance):
        raise AssertionError(f"{label}: {actual} != {expected}")


def load_json(text: str, parser: Callable[[str], Json] = json.loads) -> Json:
    return parser(text)


def roundtrip(law: PredictiveDistribution) -> None:
    decoded = load_json(json.dumps(law.to_spec(), allow_nan=False))
    if not isinstance(decoded, dict):
        raise TypeError("serialized law is not an object")
    restored = d.distribution_from_spec(decoded)
    grid = array([-math.inf, -10, -1, 0, .1, 1, 10, 1000, math.inf])
    p = array([0, .000001, .05, .5, .95, .999999, 1])
    for first_method, second_method, x in (
        (law.cdf, restored.cdf, grid), (law.cdf_left, restored.cdf_left, grid),
        (law.quantile, restored.quantile, p),
    ):
        if not np.allclose(first_method(x), second_method(x),
                           atol=1e-12, rtol=1e-12):
            raise AssertionError(f"roundtrip CDF/PPF: {law.to_spec()}")
    close(law.mean(), restored.mean(), "roundtrip mean")
    for x in floats(array([-1, 0, .5, 10])):
        close(law.atom_mass(x), restored.atom_mass(x), "roundtrip atom")
        first, second = law.log_density(x), restored.log_density(x)
        if first != second and not math.isclose(first, second, rel_tol=1e-10, abs_tol=1e-10):
            raise AssertionError("roundtrip density")


def extras() -> dict[str, Json]:
    laws = (
        d.normal(-1000, 1, True), d.normal(1000, 2), d.normal(-3, 0, True),
        d.student_t(9, -1, 2), d.logistic(-2, 3), d.lognormal(-1, .7),
        d.lognormal(2, 0), d.gamma(.2, 2), d.gamma(2, 3, -100, True),
        d.power_censored(d.normal(-2, 1), 1/3, 100),
        d.power_censored(d.student_t(9, 0, 1), .5, 100),
        d.hurdle(0, d.gamma(2, 3)), d.hurdle(1, d.gamma(2, 3)),
        d.hurdle(.999999, d.lognormal(0, 1)),
        d.affine(d.normal(0, 1), 50, 3), d.affine(d.normal(0, 1), 50, -3),
        d.affine(d.weighted_empirical(array([0, 1]), array([.3, .7])), 2, -2),
        d.affine(d.normal(0, 1), -1, 0), d.censored_gev(-20, 1, -.25),
        d.censored_gev(1, 2, 1e-9), d.bernstein(array([-2, -1, 1, 3])),
        d.bernstein(array([2, 2, 2])), d.bernstein(array([1, 1, 1]), .2),
        d.mixture((d.normal(0, 1, True), d.gamma(2, 3)), array([.2, .8])),
        d.tweedie(0, 1, 1.5), d.tweedie(.01, 100, 1.2), d.tweedie(100, .01, 1.8),
    )
    for law in laws:
        roundtrip(law)
        close(float(law.cdf(array(-math.inf))), 0, "lower CDF", 1e-12)
        close(float(law.cdf(array(math.inf))), 1, "upper CDF", 1e-12)
        if not math.isfinite(law.mean()):
            raise AssertionError("nonfinite mean")
        p = array([.001, .1, .3, .5, .7, .95, .999])
        q = law.quantile(p)
        if np.any(law.cdf(q) < p-1e-8) or np.any(law.cdf_left(q) > p+1e-8):
            raise AssertionError(f"inverse inequalities: {law.to_spec()}")
    oracle_path = Path(".omo/evidence/alternative-reference-oracles.json")
    oracle = load_json(oracle_path.read_text(encoding="utf-8"))
    if not isinstance(oracle, dict):
        raise TypeError("reference oracle must be an object")
    rain = d.power_censored(d.student_t(9, 0, 1), .5, 100)
    saved_mean, saved_p95 = oracle["sqrt_t9_rain_mean"], oracle["sqrt_t9_rain_p95"]
    if not isinstance(saved_mean, (int, float)) or not isinstance(saved_p95, (int, float)):
        raise TypeError("reference rain moments must be numeric")
    close(rain.mean(), float(saved_mean), "independent saved t9 sqrt mean")
    close(float(rain.quantile(array(.95))), float(saved_p95), "saved t9 p95")
    dry = d.power_censored(d.normal(-1, 0), .5, 100)
    close(dry.mean(), 0, "censor before squaring")
    mixed = d.mixture((d.normal(0, 0), d.normal(10, 0)), array([.5, .5]))
    close(mixed.crps(0), 2.5, "saved mixture after mixing")
    if math.isclose(mixed.crps(0), 5):
        raise AssertionError("averaged component CRPS")
    reflected = d.affine(d.weighted_empirical(array([0, 1]), array([.3, .7])), 2, -2)
    close(float(reflected.quantile(array(.7))), 0, "reflection generalized inverse")
    close(float(reflected.quantile(array(.70001))), 2, "reflection next atom")
    for law, reference in (
        (d.student_t(9, 2, 3), stats.t(9, loc=2, scale=3)),
        (d.logistic(-2, 3), stats.logistic(loc=-2, scale=3)),
        (d.lognormal(-1, .7), stats.lognorm(.7, scale=math.exp(-1))),
    ):
        expected = (quad(lambda x, ref=reference: float(ref.cdf(x))**2,
                         -math.inf, 1, epsabs=1e-10)[0]
                    + quad(lambda x, ref=reference: float(ref.sf(x))**2,
                           1, math.inf, epsabs=1e-10)[0])
        close(law.crps(1), expected, "independent continuous CRPS")
    return {"roundtrip_laws": len(laws), "edge_checks": "PASS",
            "saved_reference_oracle": str(oracle_path),
            "sqrt_t9_mean": rain.mean(), "mixture_crps": mixed.crps(0)}


def preservation() -> int:
    receipt = load_json(Path(".omo/evidence/alternative-baseline-hashes.json")
                        .read_text(encoding="utf-8"))
    if not isinstance(receipt, dict) or not isinstance(receipt["files"], dict):
        raise TypeError("invalid preservation receipt")
    files = receipt["files"]
    for name, record in files.items():
        if not isinstance(record, dict):
            raise TypeError("invalid hash record")
        content = Path(name).read_bytes()
        if len(content) != record["bytes"] or hashlib.sha256(content).hexdigest() != record["sha256"]:
            raise AssertionError(f"protected file changed: {name}")
    return len(files)


def density_and_failures() -> dict[str, Json]:
    law = Tweedie(mu=25, phi=2, power=1.5)
    for x in (1e-8, .1, 1, 25, 100, 1000):
        reference = math.fsum(float(stats.poisson.pmf(n, 5))
                              *float(stats.gamma.pdf(x, n, scale=5))
                              for n in range(1, 201))
        log_density, log_bound, relative = law.density_bounds(x)
        close(math.exp(log_density), reference, "independent CP Gamma density", 1e-10)
        if log_bound > math.log(1e-12) or relative > 1e-9:
            raise AssertionError("density certificate exceeds the frozen bounds")
    zeroth = quad(lambda x: math.exp(law.log_density(x)), 0, math.inf, epsabs=1e-9)[0]
    first = quad(lambda x: x*math.exp(law.log_density(x)), 0, math.inf, epsabs=1e-9)[0]
    second = quad(lambda x: x*x*math.exp(law.log_density(x)), 0, math.inf, epsabs=1e-8)[0]
    close(float(zeroth)+law.atom_mass(0), 1, "Tweedie total atom+density")
    close(float(first), 25, "Tweedie integrated first moment")
    close(float(second)-25**2, 250, "Tweedie integrated variance")
    invalid: tuple[Callable[[], PredictiveDistribution], ...] = (
        lambda: d.normal(0, -1), lambda: d.student_t(1, 0, 1),
        lambda: d.gamma(-1, 2), lambda: d.hurdle(.2, d.normal(0, 1)),
        lambda: d.bernstein(array([2, 1])), lambda: d.tweedie(1, 1, 2),
        lambda: d.power_censored(d.student_t(2, 0, 1), .5, 100),
        lambda: d.mixture((d.normal(0, 1),), array([0])),
        lambda: d.distribution_from_spec({"tag": "unknown"}),
    )
    for constructor in invalid:
        try:
            _ = constructor()
        except (ValueError, TypeError):
            continue
        raise AssertionError("invalid distribution was accepted")
    return {"density_certificate": "PASS", "integrated_mass": float(zeroth)+law.atom_mass(0),
            "integrated_mean": float(first), "integrated_variance": float(second)-625,
            "invalid_inputs_rejected": len(invalid)}


def main() -> None:
    start = time.perf_counter()
    print("WORKING distribution independent mathematical audit", flush=True)
    results = production_checks()
    extra = extras()
    density = density_and_failures()
    count = preservation()
    print(json.dumps({"independent_laws": len(results), "independent_status": "PASS",
                      "extra": extra, "tweedie_density": density,
                      "protected_hashes": count, "elapsed_seconds": time.perf_counter()-start},
                     indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
