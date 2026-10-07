"""Physical censor support must not evaluate an irrelevant extreme latent CDF."""

from __future__ import annotations

import json
import math
import warnings

import numpy as np

from analysis.alternative_distribution_base import ScientificLaw, array, floats
from analysis.alternative_distributions import censored_gev, gamma, normal


def main() -> None:
    laws = (censored_gev(1., 2., 0.), censored_gev(1., 2., -.2),
            censored_gev(1., 2., .2), normal(1., 2., censor_zero=True),
            gamma(2., 3., shift=-1., censor_zero=True))
    shapes = (array(-10000.), array([-math.inf, -10000., -1.]),
              array([[-10000., -1.], [0., 2.]]), array([math.nan, math.inf]),
              array([]))
    with warnings.catch_warnings(action="error"):
        for law in laws:
            assert isinstance(law, ScientificLaw)
            for values in shapes:
                cdf, left, sf = law.cdf(values), law.cdf_left(values), law.sf(values)
                assert cdf.shape == values.shape == left.shape == sf.shape
                negative = values < 0
                np.testing.assert_array_equal(cdf[negative], 0.)
                np.testing.assert_array_equal(left[negative], 0.)
                np.testing.assert_array_equal(sf[negative], 1.)
                np.testing.assert_allclose((cdf + sf)[~np.isnan(values)], 1.,
                                           atol=1e-15, rtol=0)
                assert np.all(np.isnan(cdf[np.isnan(values)]))
                assert np.all(np.isnan(sf[np.isnan(values)]))
            assert law.cdf_left(array(0.)).item() == 0.
            assert law.cdf(array(0.)).item() == law.atom_mass(0.)
        gumbel = laws[0]
        positive = array([0., 2., 10.])
        oracle = array([math.exp(-math.exp(-(x-1.)/2.)) for x in floats(positive)])
        np.testing.assert_allclose(gumbel.cdf(positive), oracle, atol=1e-15, rtol=0)
    print(json.dumps({"status": "PASS", "laws": len(laws), "shapes": len(shapes),
                      "warnings_are_errors": True}))


if __name__ == "__main__":
    main()
