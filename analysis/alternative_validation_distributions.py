"""Production-law probes against independent formulas and CDF integration."""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping

import numpy as np
from scipy.special import gammaincc, ndtr
from scipy.stats import gamma as gamma_law
from scipy.stats import poisson

from analysis.alternative_contracts import PredictiveDistribution
from analysis.alternative_validation_oracles import (
    close,
    crps_integral,
    empirical_crps,
    floats,
    integrate,
    mean_integral,
    normal_mixture_crps,
    tweedie_reference,
)
from analysis.alternative_validation_reference import integration_splits, reference_cdf
from analysis.data_io import Json


def scalar_cdf(law: PredictiveDistribution, value: float) -> float:
    return float(law.cdf(np.asarray([value], dtype=np.float64)).take(0))


def law_checks(law: PredictiveDistribution, rain: bool = False,
               observations: tuple[float, ...] = (0., 1., 5.)) -> dict[str, Json]:
    """Original-unit checks work on any reconstructable law, including atoms."""
    p = np.array([.001, .01, .05, .1, .333, .5, .667, .9, .95, .99, .999])
    q = law.quantile(p)
    if not np.all(np.isfinite(q)) or not np.all(np.diff(q) >= 0):
        raise AssertionError("nonfinite or unordered interior quantiles")
    if rain and (np.any(q < 0) or scalar_cdf(law, -1) != 0):
        raise AssertionError("negative rain support")
    close(scalar_cdf(law, -math.inf), 0, "CDF lower limit", atol=1e-12)
    close(scalar_cdf(law, math.inf), 1, "CDF upper limit", atol=1e-12)
    grid = np.unique(np.concatenate((q, np.array([0., *observations]))))
    f, left = law.cdf(grid), law.cdf_left(grid)
    reference = reference_cdf(law.to_spec())
    for value, actual in zip(floats(grid), floats(f), strict=True):
        close(actual, reference(value), "independently reconstructed CDF", atol=2e-7)
    if np.any(np.diff(f) < -1e-10) or np.any(f < 0) or np.any(f > 1):
        raise AssertionError("CDF is not a probability CDF")
    if np.any(left > f + 1e-10):
        raise AssertionError("left CDF exceeds right CDF")
    for x, a, b in zip(floats(grid), floats(left), floats(f), strict=True):
        close(law.atom_mass(x), b - a, "atom/right-left", atol=1e-9)
    if np.any(law.cdf(q) < p - 2e-7) or np.any(law.cdf_left(q) > p + 2e-7):
        raise AssertionError("generalized-inverse inequalities fail")
    mean = law.mean()
    if not math.isfinite(mean):
        raise AssertionError("issued mean is nonfinite")
    scale = max(1., abs(mean), float(q.take(-1) - q.take(0)))
    splits = (*integration_splits(law.to_spec()),
              *(x for x, mass in zip(floats(grid), floats(f-left), strict=True) if mass > 0))
    cdf: Callable[[float], float] = lambda x: scalar_cdf(law, x)
    close(mean, mean_integral(cdf, scale, splits), "original-unit mean",
          atol=1e-7 * scale, rtol=2e-6)
    errors: list[Json] = []
    for y in observations:
        reference = crps_integral(cdf, y, splits, scale)
        close(law.crps(y), reference.value, "original-unit CRPS",
              atol=2e-7 * scale, rtol=2e-6)
        errors.append(reference.error)
    return {"status": "PASS", "mean": mean, "quadrature_errors": errors}


def production_checks() -> dict[str, Json]:
    """Never return PASS when the production module is unavailable."""
    from analysis import alternative_distributions as d

    records: dict[str, Json] = {}
    for mu, sigma, censor in ((0., 1., False), (-2., 1., True), (3., 2., True)):
        law = d.normal(mu, sigma, censor)
        records[f"normal:{mu}:{censor}"] = law_checks(law, censor)
        independent_cdf: Callable[[float], float] = lambda x, censored=censor, m=mu, s=sigma: (
            0. if censored and x < 0 else float(ndtr((x - m) / s)))
        close(law.crps(1), crps_integral(independent_cdf, 1, (0,)).value,
              "Normal independent CDF")
    for values, weights in (
        (np.array([0., 0., 2., 5.]), np.array([.1, .2, .3, .4])),
        (np.array([3.]), np.array([1.])),
    ):
        law = d.weighted_empirical(values, weights)
        for y in (0., 1., 4.):
            close(law.crps(y), empirical_crps(values, weights, y), "empirical O(n^2)")
        records[f"empirical:{len(values)}"] = law_checks(law, True)
    mus, sds, weights = np.array([-2., 2.]), np.array([1., 1.5]), np.array([.4, .6])
    law = d.mixture(tuple(d.normal(m, s) for m, s in zip(floats(mus), floats(sds), strict=True)),
                    weights)
    close(law.crps(1), normal_mixture_crps(mus, sds, weights, 1), "mixture cross term")
    records["mixture"] = law_checks(law)
    csg = d.gamma(2., 3., shift=-1.5, censor_zero=True)
    mean = 6 * float(gammaincc(3, .5)) - 1.5 * float(gammaincc(2, .5))
    close(csg.mean(), mean, "CSG survival mean")
    close(scalar_cdf(csg, 0), 1 - float(gammaincc(2, .5)), "CSG shift sign")
    records["csg"] = law_checks(csg, True)
    hurdle = d.hurdle(.3, d.gamma(2., 3.))
    close(hurdle.mean(), 4.2, "hurdle mean")
    close(hurdle.atom_mass(0), .3, "hurdle independent occurrence")
    records["hurdle"] = law_checks(hurdle, True)
    for power in (.5, 1 / 3):
        transformed = d.power_censored(d.normal(0, 1), power, 100)
        exponent = 1 / power
        expected = 100 * integrate(
            lambda z, e=exponent: math.pow(z, e) * math.exp(-z*z/2) / math.sqrt(2*math.pi),
            0, math.inf).value
        close(transformed.mean(), expected, "power Jensen original-mm mean")
        records[f"power:{power}"] = law_checks(transformed, True)
    for shape in (0., -.2, .2):
        gev = d.censored_gev(1., 2., shape)
        if shape == 0:
            close(scalar_cdf(gev, 3), math.exp(-math.exp(-1)), "Gumbel limit")
        else:
            endpoint = 1 - 2 / shape
            close(scalar_cdf(gev, endpoint), 1 if shape < 0 else 0, "GEV endpoint")
        records[f"gev:{shape}"] = law_checks(gev, True)
    for power in (1.2, 1.5, 1.8):
        law = d.tweedie(3, 2, power)
        cdf, atom, mean, _ = tweedie_reference(3, 2, power, 2)
        close(scalar_cdf(law, 2), cdf, "Tweedie convolution", atol=1e-9)
        close(law.atom_mass(0), atom, "Tweedie atom", atol=1e-12)
        close(law.mean(), mean, "Tweedie mean")
        second_moment = integrate(
            lambda z, distribution=law: 2*z*(1-scalar_cdf(distribution, z)),
            0, math.inf, 100.).value
        close(second_moment-9, 2*math.pow(3, power), "Tweedie variance by survival",
              atol=2e-6, rtol=2e-6)
        rate = math.pow(3, 2-power)/(2*(2-power))
        shape = (2-power)/(power-1)
        unit = 2*(power-1)*math.pow(3, power-1)
        indices = np.arange(1, 257, dtype=np.float64)
        masses = np.asarray(poisson.pmf(indices, rate), dtype=np.float64)
        for point in (.1, 2., 20.):
            expected_density = float(np.sum(masses*gamma_law.pdf(
                point, indices*shape, scale=unit)))
            close(math.exp(law.log_density(point)), expected_density,
                  "Tweedie independent density convolution", atol=1e-12, rtol=1e-8)
        from analysis.alternative_distribution_tweedie import Tweedie
        if not isinstance(law, Tweedie):
            raise TypeError("Tweedie constructor returned substitute law")
        if law.cdf_mass_bound > 1e-12 or law.cdf_first_moment_bound > 1e-8:
            raise AssertionError("Tweedie series mass/moment truncation uncertified")
        records[f"tweedie:{power}"] = law_checks(law, True)
    coefficients = np.array([.2, 1., 2., 4.])
    bqn = d.bernstein(coefficients, p_zero=.2)
    close(bqn.mean(), .8 * float(np.mean(coefficients)), "Bernstein exact mean")
    close(bqn.atom_mass(0), .2, "Bernstein zero atom")
    records["bernstein"] = law_checks(bqn, True)
    for name, edge in (
        ("all_zero", d.weighted_empirical(np.zeros(3), np.ones(3)/3)),
        ("constant_normal", d.normal(2., 0.)),
        ("all_mass_censored_gev", d.censored_gev(-10., 1., -.2)),
        ("large_rain", d.weighted_empirical(np.array([0., 1e6]), np.array([.1, .9]))),
    ):
        restored = d.distribution_from_spec(edge.to_spec())
        np.testing.assert_allclose(edge.cdf(np.array([0., 1., 1e6])),
                                   restored.cdf(np.array([0., 1., 1e6])), atol=1e-12)
        close(edge.crps(3), restored.crps(3), "serialized edge CRPS")
        records[name] = {"status": "PASS", "mean": edge.mean()}
    for bad in (np.array([-1., 1.]), np.array([np.nan, 1.])):
        try:
            _ = d.weighted_empirical(np.array([0., 1.]), bad)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid masses accepted")
    try:
        _ = d.power_censored(d.student_t(2., 0., 1.), .5, 100.)
    except ValueError:
        records["infinite_inverse_moment_rejected"] = "PASS"
    else:
        raise AssertionError("inverse Student square has infinite mean but was accepted")
    tied = d.weighted_empirical(np.array([2., 2.]), np.array([.2, .8]))
    probability = scalar_cdf(tied, 2.)
    close(probability, 1, "coincident tercile")
    close(scalar_cdf(tied, 2.)-probability, 0, "coincident tercile middle category")
    return records


def reconstruct(spec: Mapping[str, Json]) -> PredictiveDistribution:
    from analysis.alternative_distributions import distribution_from_spec

    return distribution_from_spec(spec)
