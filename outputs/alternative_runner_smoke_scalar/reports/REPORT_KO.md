# 통계 대안 공정 비교 보고서

- 실행 범위: `SMOKE`; 보고 상태: `INCOMPLETE`.
- 고정 난수 시드: 20261007. 이 문서는 저장된 실제 예측만 분석한다.
- 전체 실험 완료 또는 통계적 유의성을 이 보고서만으로 주장하지 않는다.

## 1. 성능 비교에 앞선 실제 적용·성공 범위
|상품|변수/벡터|방법|제공|도메인 적용|과학적 게이트|결측 정답|평가 가능|평가 성공|실패|미기록|
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
|1mon|prcp|RAW|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|RAW|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|RAW|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|RAW|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|QM|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|QM|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|QM|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|QM|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|QDM|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|QDM|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|QDM|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|QDM|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|EMOS|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|EMOS|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|EMOS|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|EMOS|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|climatology_empirical|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|climatology_empirical|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|climatology_empirical|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|climatology_empirical|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|joint_gaussian_plugin|1880|0|0|0|0|0|0|1880|
|1mon|t15m|joint_gaussian_plugin|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|joint_gaussian_plugin|1410|0|0|0|0|0|0|1410|
|3mon|t15m|joint_gaussian_plugin|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|bjp_niw|1880|0|1|0|0|0|0|1879|
|1mon|t15m|bjp_niw|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|bjp_niw|1410|0|0|0|0|0|0|1410|
|3mon|t15m|bjp_niw|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|bjp_sqrt_censored|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|bjp_sqrt_censored|1880|0|1|0|0|0|0|1879|
|3mon|prcp|bjp_sqrt_censored|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|bjp_sqrt_censored|1410|0|0|0|0|0|0|1410|
|1mon|prcp|bjp_yj_fixed|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|bjp_yj_fixed|1880|0|0|0|0|0|0|1880|
|3mon|prcp|bjp_yj_fixed|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|bjp_yj_fixed|1410|0|0|0|0|0|0|1410|
|1mon|prcp|bjp_logsinh_fixed|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|bjp_logsinh_fixed|1880|0|0|0|0|0|0|1880|
|3mon|prcp|bjp_logsinh_fixed|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|bjp_logsinh_fixed|1410|0|0|0|0|0|0|1410|
|1mon|prcp|bayesian_anomaly_ridge|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|bayesian_anomaly_ridge|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|bayesian_anomaly_ridge|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|bayesian_anomaly_ridge|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|cdf_mix_fixed50|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|cdf_mix_fixed50|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|cdf_mix_fixed50|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|cdf_mix_fixed50|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|cdf_mix_cv|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|cdf_mix_cv|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|cdf_mix_cv|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|cdf_mix_cv|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|anomaly_signal_shrink|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|anomaly_signal_shrink|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|anomaly_signal_shrink|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|anomaly_signal_shrink|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|anomaly_mos|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|anomaly_mos|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|anomaly_mos|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|anomaly_mos|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|emos_constant_variance|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|emos_constant_variance|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|emos_constant_variance|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|emos_constant_variance|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|mos_unit_slope|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|mos_unit_slope|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|mos_unit_slope|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|mos_unit_slope|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|gamma_positive|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|gamma_positive|1880|0|1|0|0|0|0|1879|
|3mon|prcp|gamma_positive|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|gamma_positive|1410|0|0|0|0|0|0|1410|
|1mon|prcp|csg_fixed_shift|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|csg_fixed_shift|1880|0|0|0|0|0|0|1880|
|3mon|prcp|csg_fixed_shift|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|csg_fixed_shift|1410|0|0|0|0|0|0|1410|
|1mon|prcp|csg_estimated_shift|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|csg_estimated_shift|1880|0|0|0|0|0|0|1880|
|3mon|prcp|csg_estimated_shift|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|csg_estimated_shift|1410|0|0|0|0|0|0|1410|
|1mon|prcp|power_gaussian_sqrt|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|power_gaussian_sqrt|1880|0|1|0|0|0|0|1879|
|3mon|prcp|power_gaussian_sqrt|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|power_gaussian_sqrt|1410|0|0|0|0|0|0|1410|
|1mon|prcp|power_gaussian_cuberoot|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|power_gaussian_cuberoot|1880|0|0|0|0|0|0|1880|
|3mon|prcp|power_gaussian_cuberoot|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|power_gaussian_cuberoot|1410|0|0|0|0|0|0|1410|
|1mon|prcp|power_logistic_sqrt|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|power_logistic_sqrt|1880|0|0|0|0|0|0|1880|
|3mon|prcp|power_logistic_sqrt|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|power_logistic_sqrt|1410|0|0|0|0|0|0|1410|
|1mon|prcp|power_logistic_cuberoot|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|power_logistic_cuberoot|1880|0|0|0|0|0|0|1880|
|3mon|prcp|power_logistic_cuberoot|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|power_logistic_cuberoot|1410|0|0|0|0|0|0|1410|
|1mon|prcp|hurdle_gamma|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|hurdle_gamma|1880|0|1|0|0|0|0|1879|
|3mon|prcp|hurdle_gamma|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|hurdle_gamma|1410|0|0|0|0|0|0|1410|
|1mon|prcp|hurdle_lognormal|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|hurdle_lognormal|1880|0|0|0|0|0|0|1880|
|3mon|prcp|hurdle_lognormal|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|hurdle_lognormal|1410|0|0|0|0|0|0|1410|
|1mon|prcp|gev_censored_gumbel|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|gev_censored_gumbel|1880|0|1|0|0|0|0|1879|
|3mon|prcp|gev_censored_gumbel|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|gev_censored_gumbel|1410|0|0|0|0|0|0|1410|
|1mon|prcp|gev_censored_shrunk_shape|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|gev_censored_shrunk_shape|1880|0|0|0|0|0|0|1880|
|3mon|prcp|gev_censored_shrunk_shape|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|gev_censored_shrunk_shape|1410|0|0|0|0|0|0|1410|
|1mon|prcp|tweedie_p15|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|tweedie_p15|1880|0|1|0|0|0|0|1879|
|3mon|prcp|tweedie_p15|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|tweedie_p15|1410|0|0|0|0|0|0|1410|
|1mon|prcp|tweedie_selected_p|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|tweedie_selected_p|1880|0|0|0|0|0|0|1880|
|3mon|prcp|tweedie_selected_p|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|tweedie_selected_p|1410|0|0|0|0|0|0|1410|
|1mon|prcp|kernel_normal_equal|1880|0|1|0|0|0|0|1879|
|1mon|t15m|kernel_normal_equal|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|kernel_normal_equal|1410|0|0|0|0|0|0|1410|
|3mon|t15m|kernel_normal_equal|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|kernel_rain_hurdle_equal|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|kernel_rain_hurdle_equal|1880|0|1|0|0|0|0|1879|
|3mon|prcp|kernel_rain_hurdle_equal|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|kernel_rain_hurdle_equal|1410|0|0|0|0|0|0|1410|
|1mon|prcp|bma_group_normal|1880|0|0|0|0|0|0|1880|
|1mon|t15m|bma_group_normal|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|bma_group_normal|1410|0|0|0|0|0|0|1410|
|3mon|t15m|bma_group_normal|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|bma_group_rain|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|bma_group_rain|1880|0|0|0|0|0|0|1880|
|3mon|prcp|bma_group_rain|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|bma_group_rain|1410|0|0|0|0|0|0|1410|
|1mon|prcp|bma_component_pool|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|bma_component_pool|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|bma_component_pool|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|bma_component_pool|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|pooled_mos_ridge|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|pooled_mos_ridge|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|pooled_mos_ridge|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|pooled_mos_ridge|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|pooled_emos_ridge|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|pooled_emos_ridge|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|pooled_emos_ridge|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|pooled_emos_ridge|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|pooled_emos_cyclic|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|pooled_emos_cyclic|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|pooled_emos_cyclic|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|pooled_emos_cyclic|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|bjp_t|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|bjp_t|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|bjp_t|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|bjp_t|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|bjp_ti|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|bjp_ti|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|bjp_ti|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|bjp_ti|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|detrend_qm|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|detrend_qm|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|detrend_qm|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|detrend_qm|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|detrend_qdm|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|detrend_qdm|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|detrend_qdm|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|detrend_qdm|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|detrend_emos|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|detrend_emos|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|detrend_emos|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|detrend_emos|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|ordinal_logit|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|ordinal_logit|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|ordinal_logit|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|ordinal_logit|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|elr_threshold_logit|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|elr_threshold_logit|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|elr_threshold_logit|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|elr_threshold_logit|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|gamlss_ridge|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|gamlss_ridge|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|gamlss_ridge|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|gamlss_ridge|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|componentwise_boost|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|componentwise_boost|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|componentwise_boost|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|componentwise_boost|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|ngboost_small|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|ngboost_small|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|ngboost_small|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|ngboost_small|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|qrf_year_forest|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|qrf_year_forest|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|qrf_year_forest|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|qrf_year_forest|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|idr_mean_order|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|idr_mean_order|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|idr_mean_order|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|idr_mean_order|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|drn_small|1880|1880|0|6|1874|1|0|1879|
|1mon|t15m|drn_small|1880|1880|0|6|1874|1|0|1879|
|3mon|prcp|drn_small|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|drn_small|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|bqn_monotone|1880|1880|0|6|1874|0|0|1880|
|1mon|t15m|bqn_monotone|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|bqn_monotone|1410|1410|0|68|1342|0|0|1410|
|3mon|t15m|bqn_monotone|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|finite_member_iid_signal_noise|1880|0|1|0|0|0|0|1879|
|1mon|t15m|finite_member_iid_signal_noise|1880|1880|1|6|1873|0|0|1879|
|3mon|prcp|finite_member_iid_signal_noise|1410|0|0|0|0|0|0|1410|
|3mon|t15m|finite_member_iid_signal_noise|1410|1410|0|68|1342|0|0|1410|
|1mon|prcp|finite_member_known_covariance|1880|0|0|0|0|0|0|1880|
|1mon|t15m|finite_member_known_covariance|1880|1880|0|6|1874|0|0|1880|
|3mon|prcp|finite_member_known_covariance|1410|0|0|0|0|0|0|1410|
|3mon|t15m|finite_member_known_covariance|1410|1410|0|68|1342|0|0|1410|

## 2. 실제 원단위 및 범주·결합 점수
주간(1mon: 7일)과 월간(3mon: 개별 달), 기온(degC)과 강수(mm)는 합치지 않는다.
아래 값은 성공 사례 제한 평균이다. 서로 다른 N의 평균을 전체 우열로 해석하지 않는다.
|상품|변수/벡터|방법|점수|평가 N|평균 손실|
|---|---|---|---|---:|---:|
|1mon|prcp|EMOS|CRPS|1|10.635683792084127|
|1mon|prcp|EMOS|BRIER|1|0.7807313461477892|
|1mon|prcp|EMOS|RPS|1|0.7118760327709635|
|1mon|prcp|QDM|CRPS|1|9.79216587764685|
|1mon|prcp|QDM|BRIER|1|0.8061224489795918|
|1mon|prcp|QDM|RPS|1|0.7602040816326531|
|1mon|prcp|QM|CRPS|1|10.913489203462134|
|1mon|prcp|QM|BRIER|1|0.9489795918367346|
|1mon|prcp|QM|RPS|1|0.8673469387755102|
|1mon|prcp|RAW|CRPS|1|7.39172360977617|
|1mon|prcp|RAW|BRIER|1|0.3979591836734694|
|1mon|prcp|RAW|RPS|1|0.27040816326530615|
|1mon|prcp|anomaly_mos|CRPS|1|8.878670284405162|
|1mon|prcp|anomaly_mos|BRIER|1|0.5812091886549471|
|1mon|prcp|anomaly_mos|RPS|1|0.4943228293885615|
|1mon|prcp|bjp_sqrt_censored|CRPS|1|8.47966456343849|
|1mon|prcp|bjp_sqrt_censored|BRIER|1|0.5065143290826821|
|1mon|prcp|bjp_sqrt_censored|RPS|1|0.48943527438195145|
|1mon|prcp|bjp_t|CRPS|1|9.085470448120333|
|1mon|prcp|bjp_t|BRIER|1|0.5361275554976013|
|1mon|prcp|bjp_t|RPS|1|0.5224486796298846|
|1mon|prcp|cdf_mix_fixed50|CRPS|1|9.364690829997453|
|1mon|prcp|cdf_mix_fixed50|BRIER|1|0.7184502743542309|
|1mon|prcp|cdf_mix_fixed50|RPS|1|0.6297250394692667|
|1mon|prcp|climatology_empirical|CRPS|1|8.255435147849468|
|1mon|prcp|climatology_empirical|BRIER|1|0.6666666666666664|
|1mon|prcp|climatology_empirical|RPS|1|0.5555555555555554|
|1mon|prcp|detrend_qm|CRPS|1|10.626828443096453|
|1mon|prcp|detrend_qm|BRIER|1|0.9489795918367347|
|1mon|prcp|detrend_qm|RPS|1|0.8673469387755103|
|1mon|prcp|drn_small|CRPS|1|11.26281158978624|
|1mon|prcp|drn_small|BRIER|1|0.9041920729735754|
|1mon|prcp|drn_small|RPS|1|0.7515100023294419|
|1mon|prcp|gamlss_ridge|CRPS|1|12.136810652069206|
|1mon|prcp|gamlss_ridge|BRIER|1|1.0083395942580848|
|1mon|prcp|gamlss_ridge|RPS|1|0.7975917209269416|
|1mon|prcp|gamma_positive|CRPS|1|10.117164252752179|
|1mon|prcp|gamma_positive|BRIER|1|0.7992161380758178|
|1mon|prcp|gamma_positive|RPS|1|0.6986861181505086|
|1mon|prcp|gev_censored_gumbel|CRPS|1|8.746818672299106|
|1mon|prcp|gev_censored_gumbel|BRIER|1|0.6070965541052451|
|1mon|prcp|gev_censored_gumbel|RPS|1|0.4789206532229824|
|1mon|prcp|hurdle_gamma|CRPS|1|12.989657935242418|
|1mon|prcp|hurdle_gamma|BRIER|1|1.087060298493952|
|1mon|prcp|hurdle_gamma|RPS|1|0.9233020039780717|
|1mon|prcp|idr_mean_order|CRPS|1|13.149762190614204|
|1mon|prcp|idr_mean_order|BRIER|1|1.056553698269168|
|1mon|prcp|idr_mean_order|RPS|1|0.7329846698602909|
|1mon|prcp|kernel_rain_hurdle_equal|CRPS|1|12.183792959109576|
|1mon|prcp|kernel_rain_hurdle_equal|BRIER|1|1.0228976948867303|
|1mon|prcp|kernel_rain_hurdle_equal|RPS|1|0.895017368649152|
|1mon|prcp|pooled_mos_ridge|CRPS|1|9.514835172961373|
|1mon|prcp|pooled_mos_ridge|BRIER|1|0.7678611762048184|
|1mon|prcp|pooled_mos_ridge|RPS|1|0.7493285444103109|
|1mon|prcp|power_gaussian_sqrt|CRPS|1|10.941181612068503|
|1mon|prcp|power_gaussian_sqrt|BRIER|1|0.8703340160863462|
|1mon|prcp|power_gaussian_sqrt|RPS|1|0.6527537297404583|
|1mon|prcp|qrf_year_forest|CRPS|1|11.22756429091062|
|1mon|prcp|qrf_year_forest|BRIER|1|0.899506278941826|
|1mon|prcp|qrf_year_forest|RPS|1|0.7185274920307934|
|1mon|prcp|tweedie_p15|CRPS|1|12.315406502043947|
|1mon|prcp|tweedie_p15|BRIER|1|1.0582479739042092|
|1mon|prcp|tweedie_p15|RPS|1|0.7635024173459757|
|1mon|t15m|EMOS|CRPS|1|0.6431704427532012|
|1mon|t15m|EMOS|BRIER|1|0.012740795083868463|
|1mon|t15m|EMOS|RPS|1|0.006642102522196432|
|1mon|t15m|QDM|CRPS|1|0.3922315157259754|
|1mon|t15m|QDM|BRIER|1|0.0|
|1mon|t15m|QDM|RPS|1|0.0|
|1mon|t15m|QM|CRPS|1|0.4495992441132993|
|1mon|t15m|QM|BRIER|1|0.0|
|1mon|t15m|QM|RPS|1|0.0|
|1mon|t15m|RAW|CRPS|1|1.3104675743910463|
|1mon|t15m|RAW|BRIER|1|0.0|
|1mon|t15m|RAW|RPS|1|0.0|
|1mon|t15m|anomaly_mos|CRPS|1|0.7211937566886574|
|1mon|t15m|anomaly_mos|BRIER|1|0.0005356544982115913|
|1mon|t15m|anomaly_mos|RPS|1|0.00026802011298264467|
|1mon|t15m|bjp_niw|CRPS|1|2.098861005725978|
|1mon|t15m|bjp_niw|BRIER|1|0.44005200134015754|
|1mon|t15m|bjp_niw|RPS|1|0.4166757879797336|
|1mon|t15m|bjp_t|CRPS|1|2.4948675745335938|
|1mon|t15m|bjp_t|BRIER|1|0.5353705648118391|
|1mon|t15m|bjp_t|RPS|1|0.5163582057557468|
|1mon|t15m|cdf_mix_fixed50|CRPS|1|1.4899597561819653|
|1mon|t15m|cdf_mix_fixed50|BRIER|1|0.2105671734908937|
|1mon|t15m|cdf_mix_fixed50|RPS|1|0.16824905789597516|
|1mon|t15m|climatology_empirical|CRPS|1|3.034965037762418|
|1mon|t15m|climatology_empirical|BRIER|1|0.6666666666666664|
|1mon|t15m|climatology_empirical|RPS|1|0.5555555555555554|
|1mon|t15m|detrend_qm|CRPS|1|0.7185915834688721|
|1mon|t15m|detrend_qm|BRIER|1|0.0|
|1mon|t15m|detrend_qm|RPS|1|0.0|
|1mon|t15m|drn_small|CRPS|1|0.6807040226869625|
|1mon|t15m|drn_small|BRIER|1|0.01577135347931427|
|1mon|t15m|drn_small|RPS|1|0.008262859084440738|
|1mon|t15m|gamlss_ridge|CRPS|1|1.716111130505851|
|1mon|t15m|gamlss_ridge|BRIER|1|0.24165608962759055|
|1mon|t15m|gamlss_ridge|RPS|1|0.15094244597409698|
|1mon|t15m|idr_mean_order|CRPS|1|0.4606271787812819|
|1mon|t15m|idr_mean_order|BRIER|1|0.0|
|1mon|t15m|idr_mean_order|RPS|1|0.0|
|1mon|t15m|kernel_normal_equal|CRPS|1|0.7001882688567427|
|1mon|t15m|kernel_normal_equal|BRIER|1|0.004696938756672592|
|1mon|t15m|kernel_normal_equal|RPS|1|0.0023697212544390236|
|1mon|t15m|pooled_mos_ridge|CRPS|1|0.6155176171621847|
|1mon|t15m|pooled_mos_ridge|BRIER|1|0.015291238295012204|
|1mon|t15m|pooled_mos_ridge|RPS|1|0.00810905617113442|
|1mon|t15m|qrf_year_forest|CRPS|1|1.0245718221783777|
|1mon|t15m|qrf_year_forest|BRIER|1|0.07704565843841468|
|1mon|t15m|qrf_year_forest|RPS|1|0.05409112133873791|
|1mon|prcp|ordinal_logit|BRIER|1|0.8617615715302527|
|1mon|prcp|ordinal_logit|RPS|1|0.8175293508444774|
|1mon|t15m|ordinal_logit|BRIER|1|0.5501205967520908|
|1mon|t15m|ordinal_logit|RPS|1|0.4656359428135283|

## 3. 동일 성공 마스크의 비교
paired_comparison.csv는 동일 사례에서만 손실 차이를 계산한다. 음수는 첫 방법의 작은 손실을 뜻한다.
common_masks.csv에 모든 정확한 사례 ID, SHA256, 사전 지정 레지스트리 family_no 교집합을 보존한다.
저장된 공통마스크 점수 행: 19664. 빈 교집합도 숨기지 않는다.
lead/month/season/year별 결과는 각 점수 표에 있으며 범주 전용은 RPS/Brier만 산출한다.

## 4. 실패를 포함한 운용 정책과 손실 한계
failure_inclusive_policy.csv의 method+climatology_on_failure는 별도 정책이다.
실패한 원방법 상태·분포를 변경하지 않으며, 같은 외부 훈련 경험 기후값으로 실패 사례를 평가한다.
미기록 또는 미실행 상태는 성공도 실패 대체도 아니다. 정책이 불완전하면 평균은 비운다.
비음수 점수의 미평가 손실 한계는 [성공 손실 합/N, +inf]이며 유한 벌점을 만들지 않는다.
정책 행: 640; 상세 대체 출처는 failure_policy_cases.csv에 있다.

## 5. 반복 관측창·연도 민감도
동일 변수/상품/정확한 VALID_START-END 창 총 가중치 1을 발행들에 나눈다.
year_overlap_sensitivity.csv는 같은 창을 묶은 연도 블록 및 연결된 중첩창 블록 재표본화(999회),
연도별 차이와 한 연도 제외 차이를 기록한다. 실제 약 5개 검증 연도로 강한 유의성·인과 주장을 하지 않는다.

## 6. 분포·강수 사건·결합 근사
원래 해석적 주변분포 점수와 유한 시나리오 투영 주변점수는 별도 산출물이다.
결합 ENERGY/VARIOGRAM 및 실제 저장된 사건 Brier는 벡터 범위별로만 비교한다.
PIT는 F(y-)와 F(y) 사이 원자 질량을 고정 시드로 무작위화한다.
상위 강수 사건은 외부 훈련 90% 분위수 초과로 고정되며 검증 정답으로 임계값을 고르지 않는다.
원분포 진단 행: 37; 원분포가 없거나 복원 실패하면 MISSING/ERROR를 표시한다.

## 7. 완전성·근거 및 해석 한계
필수 산출물 결측: [].
report_manifest.json은 범위·시드·필수 산출물·진단 결측·마스크 정의·그림 경로를 기록한다.
모든 방법 전체 실행, 독립 검증 및 최종 수동 QA는 별도 증거가 필요하다.
유리한 일부 사례나 성공만으로 최선·우월·실험 PASS라고 주장하지 않는다.
RAW/QM/QDM/EMOS 비교도 위와 동일한 적용범위·공통마스크·실패정책 규칙을 따른다.
