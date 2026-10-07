"""Dispatcher for every frozen classical subtype; no cost-based omissions."""

from __future__ import annotations

from time import perf_counter

import numpy as np

from analysis.alternative_classical_common import result
from analysis.alternative_classical_local import LOCAL_IDS, fit_local
from analysis.alternative_contracts import (
    AlternativeError,
    FitConfig,
    FitResult,
    FitStatus,
    MethodSpec,
    TrainingSet,
)

CLASSICAL_IDS = tuple(name for name in LOCAL_IDS if name != "emos") + (
    "cdf_mix_fixed50", "cdf_mix_cv", "anomaly_signal_shrink", "tweedie_selected_p",
    "kernel_normal_equal", "kernel_rain_hurdle_equal", "bma_group_normal",
    "bma_group_rain", "bma_component_pool", "pooled_mos_ridge", "pooled_emos_ridge",
    "pooled_emos_cyclic", "detrend_qm", "detrend_qdm", "detrend_emos",
)
RAIN_IDS = tuple(name for name in CLASSICAL_IDS if name.startswith((
    "gamma_", "csg_", "power_", "hurdle_", "gev_", "tweedie_"))) + (
        "kernel_rain_hurdle_equal", "bma_group_rain")
TEMP_IDS = ("kernel_normal_equal", "bma_group_normal")


def fit_classical(spec: MethodSpec, training: TrainingSet, config: FitConfig) -> FitResult:
    """Uniform truth-free fit, domain/support gates, and genuine numerical failures."""
    started = perf_counter()
    name = spec.id
    rain = training.target.variable == "prcp"
    if name not in CLASSICAL_IDS:
        return result(name, training, started, None, status=FitStatus.NOT_APPLICABLE_DOMAIN,
                      reason="UNKNOWN_CLASSICAL_ID")
    if (name in RAIN_IDS and not rain) or (name in TEMP_IDS and rain):
        return result(name, training, started, None, status=FitStatus.NOT_APPLICABLE_DOMAIN,
                      reason="METHOD_VARIABLE_DOMAIN")
    if name.startswith("bma_group_"):
        return result(name, training, started, None, status=FitStatus.GATED_DATA,
                      reason="G3_G4_PHYSICAL_IDENTITY_AND_GENERATION_GROUPS_UNPROVEN",
                      message=".omo/evidence/alternative-input-applicability.md: " +
                      "source labels are structural; no physical identity/group contract")
    if len({row.source_year for row in training.rows}) < 10:
        return result(name, training, started, None, status=FitStatus.INSUFFICIENT_TRAINING,
                      reason="FEWER_THAN_TEN_YEARS")
    if any(row.variable != training.target.variable or row.product != training.target.product
           for row in training.rows):
        return result(name, training, started, None, status=FitStatus.INPUT_CONFLICT,
                      reason="MIXED_PRODUCT_OR_VARIABLE")
    if (not np.all(np.isfinite(training.target.members))
        or any(not np.all(np.isfinite(row.ensemble)) or not np.isfinite(row.observation)
               for row in training.rows)
        or (rain and (np.any(training.target.members < 0)
                      or any(np.any(row.ensemble < 0) or row.observation < 0
                             for row in training.rows)))):
        return result(name, training, started, None, status=FitStatus.INPUT_CONFLICT,
                      reason="INVALID_OR_NEGATIVE_RAIN_INPUT")
    try:
        if name in LOCAL_IDS:
            return fit_local(spec, training, config)
        if name == "tweedie_selected_p":
            from analysis.alternative_classical_selection import fit_selected_tweedie
            return fit_selected_tweedie(spec, training, config)
        if name.startswith(("cdf_mix_", "anomaly_signal_")) or name == "bma_component_pool":
            from analysis.alternative_classical_mixture import fit_mixture
            return fit_mixture(spec, training, config)
        if name.startswith("kernel_"):
            from analysis.alternative_classical_kernel import fit_kernel
            return fit_kernel(spec, training, config)
        if name.startswith("pooled_"):
            from analysis.alternative_classical_pooled import fit_pooled
            return fit_pooled(spec, training, config)
        from analysis.alternative_classical_trend import fit_trend
        return fit_trend(spec, training, config)
    except (AlternativeError, ValueError, FloatingPointError, OverflowError) as exc:
        return result(name, training, started, None, status=FitStatus.FIT_FAILED,
                      reason=exc.code if isinstance(exc, AlternativeError) else type(exc).__name__,
                      message=str(exc))
    except ImportError as exc:
        return result(name, training, started, None, status=FitStatus.FIT_FAILED,
                      reason="DEPENDENCY_IMPORT_FAILED", message=str(exc))
