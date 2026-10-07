"""Common mathematical audit for a single saved original-unit predictive law."""

from __future__ import annotations

import math

import numpy as np

from analysis.alternative_validation_distributions import reconstruct
from analysis.alternative_validation_oracles import close
from analysis.alternative_validation_reference import (
    reference_cdf,
    reference_crps,
    reference_mean,
)
from analysis.data_io import Json


def saved_law_checks(row: dict[str, str], spec: dict[str, Json]) -> dict[str, Json]:
    law, cdf = reconstruct(spec), reference_cdf(spec)
    close(cdf(-math.inf), 0, "independent saved CDF lower limit", atol=1e-12)
    close(cdf(math.inf), 1, "independent saved CDF upper limit", atol=1e-12)
    p_grid = np.array([.001, .01, .05, .1, 1/3, .5, 2/3, .9, .95, .99, .999])
    quantile_grid = law.quantile(p_grid)
    if not np.all(np.isfinite(quantile_grid)) or np.any(np.diff(quantile_grid) < 0):
        raise AssertionError("saved law interior quantiles nonfinite/unordered")
    f_grid = law.cdf(quantile_grid)
    left_grid = law.cdf_left(quantile_grid)
    if (not np.all(np.isfinite(f_grid)) or not np.all(np.isfinite(left_grid)) or
            np.any(np.diff(f_grid) < -1e-10) or np.any(f_grid < p_grid-2e-7)):
        raise AssertionError("saved law finite CDF monotonicity/quantile inversion fails")
    if np.any(left_grid > p_grid+2e-7):
        raise AssertionError("saved law left generalized inverse fails")
    for index in range(len(p_grid)):
        close(float(f_grid.take(index)), cdf(float(quantile_grid.take(index))),
              "independent saved CDF across quantile grid")
    q = law.quantile(np.array([.05, .95]))
    expected_mean = reference_mean(spec)
    expected_crps = reference_crps(spec, float(row["OBS"]))
    close(float(row["PRED_MEAN"]), expected_mean, "saved original-unit mean", atol=2e-6, rtol=2e-6)
    close(float(row["CRPS"]), expected_crps, "saved original-unit CRPS", atol=2e-6, rtol=2e-6)
    for threshold, column in ((float(row["Q33"]), "P_BN"), (float(row["Q67"]), "P_AN")):
        expected = cdf(threshold)
        close(float(row[column]), expected if column == "P_BN" else 1-expected,
              "saved original-unit tercile CDF", atol=2e-7)
    if row["method_id"] not in {"RAW", "QM", "QDM", "raw", "qm", "qdm"}:
        close(float(row["P05"]), float(q.take(0)), "saved P05")
        close(float(row["P95"]), float(q.take(1)), "saved P95")
    elif spec.get("tag") == "weighted_empirical":
        if "CONTRACT_P05" not in row or "CONTRACT_P95" not in row:
            raise AssertionError("baseline generalized-inverse diagnostics unlabeled")
        close(float(row["CONTRACT_P05"]), float(q.take(0)), "baseline contract P05")
        close(float(row["CONTRACT_P95"]), float(q.take(1)), "baseline contract P95")
    if row["variable"] == "prcp" and (cdf(-1) != 0 or float(q.take(0)) < 0):
        raise AssertionError("saved rain law has negative support")
    # Local import is one-way: both surfaces call this same category contract.
    from analysis.alternative_validation_category import category_score
    category_score(row)
    if not row["fit_ref"]:
        raise AssertionError("prediction has no fit reference")
    return {"expected_mean": expected_mean, "expected_crps": expected_crps,
            "expected_cdf_q33": cdf(float(row["Q33"])), "expected_cdf_q67": cdf(float(row["Q67"]))}
