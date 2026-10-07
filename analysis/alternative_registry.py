"""Exhaustive research subtypes, including visible scientific input gates."""

from dataclasses import replace
from typing import Final

from analysis.alternative_contracts import MethodSpec

VERSION: Final = "research20261007.1"


def _variants(template: MethodSpec, ids: tuple[str, ...]) -> tuple[MethodSpec, ...]:
    """Share family metadata, never imply that distinct IDs are aliases."""
    return tuple(replace(template, id=method_id, subtype=method_id) for method_id in ids)


def method_registry() -> tuple[MethodSpec, ...]:
    """Register every frozen subtype; failure/gating cannot remove its row."""
    return (
        *_variants(MethodSpec(
            id="RAW", subtype="RAW", family_no=0, domain="both", surface="continuous",
            fit_scope="local", algorithm_version=VERSION, owner="baseline",
        ), ("RAW", "QM", "QDM", "EMOS", "climatology_empirical")),
        *_variants(MethodSpec(
            id="bjp_niw", subtype="bjp_niw", family_no=1, domain="temperature",
            surface="continuous", fit_scope="local", algorithm_version=VERSION, owner="bayes",
        ), ("joint_gaussian_plugin", "bjp_niw")),
        *_variants(MethodSpec(
            id="bjp_sqrt_censored", subtype="bjp_sqrt_censored", family_no=1,
            domain="precipitation", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="bayes",
        ), ("bjp_sqrt_censored", "bjp_yj_fixed", "bjp_logsinh_fixed")),
        MethodSpec(
            id="bayesian_anomaly_ridge", subtype="bayesian_anomaly_ridge", family_no=1,
            domain="both", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="bayes",
        ),
        *_variants(MethodSpec(
            id="cdf_mix_fixed50", subtype="cdf_mix_fixed50", family_no=2,
            domain="both", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="classical",
        ), ("cdf_mix_fixed50", "cdf_mix_cv", "anomaly_signal_shrink")),
        *_variants(MethodSpec(
            id="anomaly_mos", subtype="anomaly_mos", family_no=3,
            domain="both", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="classical",
        ), ("anomaly_mos", "emos_constant_variance", "mos_unit_slope")),
        MethodSpec(
            id="gamma_positive", subtype="gamma_positive", family_no=4,
            domain="precipitation", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="classical", gate_ids=("G0",),
        ),
        *_variants(MethodSpec(
            id="csg_fixed_shift", subtype="csg_fixed_shift", family_no=4,
            domain="precipitation", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="classical",
        ), ("csg_fixed_shift", "csg_estimated_shift")),
        *_variants(MethodSpec(
            id="power_gaussian_sqrt", subtype="power_gaussian_sqrt", family_no=5,
            domain="precipitation", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="classical",
        ), ("power_gaussian_sqrt", "power_gaussian_cuberoot",
            "power_logistic_sqrt", "power_logistic_cuberoot")),
        *_variants(MethodSpec(
            id="hurdle_gamma", subtype="hurdle_gamma", family_no=6,
            domain="precipitation", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="classical",
        ), ("hurdle_gamma", "hurdle_lognormal")),
        *_variants(MethodSpec(
            id="gev_censored_gumbel", subtype="gev_censored_gumbel", family_no=7,
            domain="precipitation", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="classical",
        ), ("gev_censored_gumbel", "gev_censored_shrunk_shape",
            "tweedie_p15", "tweedie_selected_p")),
        MethodSpec(
            id="kernel_normal_equal", subtype="kernel_normal_equal", family_no=8,
            domain="temperature", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="classical",
        ),
        MethodSpec(
            id="kernel_rain_hurdle_equal", subtype="kernel_rain_hurdle_equal", family_no=8,
            domain="precipitation", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="classical",
        ),
        MethodSpec(
            id="bma_group_normal", subtype="bma_group_normal", family_no=8,
            domain="temperature", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="classical", gate_ids=("G3", "G4"),
        ),
        MethodSpec(
            id="bma_group_rain", subtype="bma_group_rain", family_no=8,
            domain="precipitation", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="classical", gate_ids=("G3", "G4"),
        ),
        MethodSpec(
            id="bma_component_pool", subtype="bma_component_pool", family_no=8,
            domain="both", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="classical",
        ),
        *_variants(MethodSpec(
            id="pooled_mos_ridge", subtype="pooled_mos_ridge", family_no=9,
            domain="both", surface="continuous", fit_scope="pooled",
            algorithm_version=VERSION, owner="classical", gate_ids=("G1",),
        ), ("pooled_mos_ridge", "pooled_emos_ridge", "pooled_emos_cyclic")),
        *_variants(MethodSpec(
            id="bjp_t", subtype="bjp_t", family_no=10,
            domain="both", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="bayes",
        ), ("bjp_t", "bjp_ti")),
        *_variants(MethodSpec(
            id="detrend_qm", subtype="detrend_qm", family_no=10,
            domain="both", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="classical",
        ), ("detrend_qm", "detrend_qdm", "detrend_emos")),
        *_variants(MethodSpec(
            id="ordinal_logit", subtype="ordinal_logit", family_no=11,
            domain="both", surface="category", fit_scope="pooled",
            algorithm_version=VERSION, owner="learning", gate_ids=("G1",),
        ), ("ordinal_logit", "elr_threshold_logit")),
        *_variants(MethodSpec(
            id="gamlss_ridge", subtype="gamlss_ridge", family_no=12,
            domain="both", surface="continuous", fit_scope="pooled",
            algorithm_version=VERSION, owner="learning", gate_ids=("G1",),
        ), ("gamlss_ridge", "componentwise_boost", "ngboost_small")),
        *_variants(MethodSpec(
            id="qrf_year_forest", subtype="qrf_year_forest", family_no=13,
            domain="both", surface="continuous", fit_scope="pooled",
            algorithm_version=VERSION, owner="learning", gate_ids=("G1",),
        ), ("qrf_year_forest", "idr_mean_order")),
        *_variants(MethodSpec(
            id="drn_small", subtype="drn_small", family_no=14,
            domain="both", surface="continuous", fit_scope="pooled",
            algorithm_version=VERSION, owner="learning", gate_ids=("G1",),
        ), ("drn_small", "bqn_monotone")),
        *_variants(MethodSpec(
            id="schaake_window", subtype="schaake_window", family_no=15,
            domain="both", surface="joint", fit_scope="joint",
            algorithm_version=VERSION, owner="joint", gate_ids=("G2",),
        ), ("schaake_window", "schaake_block", "residual_gaussian_copula")),
        *_variants(MethodSpec(
            id="ecc_q", subtype="ecc_q", family_no=15,
            domain="both", surface="joint", fit_scope="joint",
            algorithm_version=VERSION, owner="joint", gate_ids=("G2", "G3"),
        ), ("ecc_q", "decc_path_shrunk_error")),
        MethodSpec(
            id="mbjp_niw", subtype="mbjp_niw", family_no=16,
            domain="temperature", surface="joint", fit_scope="joint",
            algorithm_version=VERSION, owner="bayes", gate_ids=("G2",),
        ),
        MethodSpec(
            id="mbjp_sqrt_censored", subtype="mbjp_sqrt_censored", family_no=16,
            domain="both", surface="joint", fit_scope="joint",
            algorithm_version=VERSION, owner="bayes", gate_ids=("G2",),
        ),
        *_variants(MethodSpec(
            id="mbcp_annual", subtype="mbcp_annual", family_no=16,
            domain="both", surface="joint", fit_scope="joint",
            algorithm_version=VERSION, owner="joint", gate_ids=("G2",),
        ), ("mbcp_annual", "mbcr_annual", "mbcn_annual", "otc_annual")),
        MethodSpec(
            id="dotc_annual", subtype="dotc_annual", family_no=16,
            domain="both", surface="joint", fit_scope="joint",
            algorithm_version=VERSION, owner="joint", gate_ids=("G2", "G6"),
        ),
        *_variants(MethodSpec(
            id="finite_member_iid_signal_noise", subtype="finite_member_iid_signal_noise",
            family_no=17, domain="temperature", surface="continuous", fit_scope="local",
            algorithm_version=VERSION, owner="bayes", gate_ids=("G5",),
        ), ("finite_member_iid_signal_noise", "finite_member_known_covariance")),
    )
