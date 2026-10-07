"""Real fit dispatch edges: sparse wet years, invalid rain and zero spread."""

from __future__ import annotations

from dataclasses import replace

import numpy as np

from analysis.alternative_contracts import FitConfig, FitStatus, MethodSpec
from analysis.alternative_validation_learning import fixture
from analysis.data_io import Json


def specification(identifier: str, rain: bool, family: int) -> MethodSpec:
    return MethodSpec(id=identifier, family_no=family, subtype=identifier,
                      domain="precipitation" if rain else "temperature",
                      surface="continuous", fit_scope="local", algorithm_version="frozen-v1",
                      owner="classical")


def fit_edge_checks() -> dict[str, Json]:
    from analysis.alternative_classical import fit_classical

    base = fixture()
    target = replace(base.target, variable="prcp", members=np.array([0.]))
    sparse_rows = tuple(replace(
        row, variable="prcp", observation=5. if index == 0 else 0.)
        for index, row in enumerate(base.rows))
    sparse = replace(base, target=target, rows=sparse_rows,
                     local_observations=np.array([row.observation for row in sparse_rows]))
    result: dict[str, Json] = {"status": "PASS"}
    for method in ("hurdle_gamma", "hurdle_lognormal"):
        fitted = fit_classical(specification(method, True, 6), sparse, FitConfig(workers=1))
        if fitted.status != FitStatus.INSUFFICIENT_TRAINING or fitted.fitted_model is not None:
            raise AssertionError("one-positive-year hurdle fabricated intensity fit")
        result[method] = {"status": str(fitted.status), "reason": fitted.reason_code}
    gamma = fit_classical(specification("gamma_positive", True, 4), sparse, FitConfig())
    if gamma.status != FitStatus.GATED_DATA or gamma.fitted_model is not None:
        raise AssertionError("positive Gamma with exact zeros not scientifically gated")
    invalid = replace(sparse, target=replace(target, members=np.array([-1.])))
    rejected = fit_classical(specification("hurdle_gamma", True, 6), invalid, FitConfig())
    if rejected.status != FitStatus.INPUT_CONFLICT:
        raise AssertionError("negative rain did not fail at real fit boundary")
    constant = replace(base, target=replace(base.target, members=np.array([3.])),
                       rows=tuple(replace(row, ensemble=np.array([3.])) for row in base.rows))
    fitted = fit_classical(specification("mos_unit_slope", False, 3), constant,
                           FitConfig(workers=1))
    if fitted.status != FitStatus.OK or fitted.fitted_model is None:
        raise AssertionError(f"constant predictor/spread rejected: {fitted.reason_code}")
    law = fitted.fitted_model.predict(constant.target)
    if not np.isfinite(law.mean()) or not np.isfinite(law.crps(2.)):
        raise AssertionError("constant predictor fit lacks finite original-unit law")
    result["positive_gamma"] = "GATED_DATA_WITH_ZEROS"
    result["negative_rain"] = "INPUT_CONFLICT"
    result["constant_predictor_M1"] = {"mean": law.mean(), "crps": law.crps(2.)}
    return result
