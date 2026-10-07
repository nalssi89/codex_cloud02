# 통계 대안 공정 비교 보고서

- 실행 범위: `SMOKE`; 보고 상태: `INCOMPLETE`.
- 원실행 상태: `PREDICTIONS_COMPLETED`. 진행·중단·실패 실행은 완료 보고가 아니다.
- 고정 난수 시드: 20261007. 이 문서는 저장된 실제 예측만 분석한다.
- 전체 실험 완료 또는 통계적 유의성을 이 보고서만으로 주장하지 않는다.

## 1. 성능 비교에 앞선 실제 적용·성공 범위
|상품|변수/벡터|방법|계열|제공|도메인 적용|과학적 게이트|결측 정답|평가 가능|평가 성공|적합 실패|수치/점수 실패|미기록|
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|1mon|prcp|RAW|0|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|RAW|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|RAW|0|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|RAW|0|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|QM|0|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|QM|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|QM|0|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|QM|0|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|QDM|0|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|QDM|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|QDM|0|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|QDM|0|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|EMOS|0|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|EMOS|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|EMOS|0|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|EMOS|0|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|climatology_empirical|0|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|climatology_empirical|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|climatology_empirical|0|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|climatology_empirical|0|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|joint_gaussian_plugin|1|1880|0|0|0|0|0|0|0|1880|
|1mon|t15m|joint_gaussian_plugin|1|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|joint_gaussian_plugin|1|1410|0|0|0|0|0|0|0|1410|
|3mon|t15m|joint_gaussian_plugin|1|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|bjp_niw|1|1880|0|0|0|0|0|0|0|1880|
|1mon|t15m|bjp_niw|1|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|bjp_niw|1|1410|0|0|0|0|0|0|0|1410|
|3mon|t15m|bjp_niw|1|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|bjp_sqrt_censored|1|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|bjp_sqrt_censored|1|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|bjp_sqrt_censored|1|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|bjp_sqrt_censored|1|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|bjp_yj_fixed|1|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|bjp_yj_fixed|1|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|bjp_yj_fixed|1|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|bjp_yj_fixed|1|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|bjp_logsinh_fixed|1|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|bjp_logsinh_fixed|1|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|bjp_logsinh_fixed|1|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|bjp_logsinh_fixed|1|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|bayesian_anomaly_ridge|1|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|bayesian_anomaly_ridge|1|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|bayesian_anomaly_ridge|1|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|bayesian_anomaly_ridge|1|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|cdf_mix_fixed50|2|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|cdf_mix_fixed50|2|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|cdf_mix_fixed50|2|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|cdf_mix_fixed50|2|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|cdf_mix_cv|2|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|cdf_mix_cv|2|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|cdf_mix_cv|2|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|cdf_mix_cv|2|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|anomaly_signal_shrink|2|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|anomaly_signal_shrink|2|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|anomaly_signal_shrink|2|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|anomaly_signal_shrink|2|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|anomaly_mos|3|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|anomaly_mos|3|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|anomaly_mos|3|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|anomaly_mos|3|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|emos_constant_variance|3|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|emos_constant_variance|3|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|emos_constant_variance|3|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|emos_constant_variance|3|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|mos_unit_slope|3|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|mos_unit_slope|3|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|mos_unit_slope|3|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|mos_unit_slope|3|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|gamma_positive|4|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|gamma_positive|4|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|gamma_positive|4|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|gamma_positive|4|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|csg_fixed_shift|4|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|csg_fixed_shift|4|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|csg_fixed_shift|4|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|csg_fixed_shift|4|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|csg_estimated_shift|4|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|csg_estimated_shift|4|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|csg_estimated_shift|4|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|csg_estimated_shift|4|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|power_gaussian_sqrt|5|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|power_gaussian_sqrt|5|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|power_gaussian_sqrt|5|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|power_gaussian_sqrt|5|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|power_gaussian_cuberoot|5|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|power_gaussian_cuberoot|5|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|power_gaussian_cuberoot|5|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|power_gaussian_cuberoot|5|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|power_logistic_sqrt|5|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|power_logistic_sqrt|5|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|power_logistic_sqrt|5|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|power_logistic_sqrt|5|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|power_logistic_cuberoot|5|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|power_logistic_cuberoot|5|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|power_logistic_cuberoot|5|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|power_logistic_cuberoot|5|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|hurdle_gamma|6|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|hurdle_gamma|6|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|hurdle_gamma|6|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|hurdle_gamma|6|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|hurdle_lognormal|6|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|hurdle_lognormal|6|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|hurdle_lognormal|6|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|hurdle_lognormal|6|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|gev_censored_gumbel|7|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|gev_censored_gumbel|7|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|gev_censored_gumbel|7|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|gev_censored_gumbel|7|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|gev_censored_shrunk_shape|7|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|gev_censored_shrunk_shape|7|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|gev_censored_shrunk_shape|7|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|gev_censored_shrunk_shape|7|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|tweedie_p15|7|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|tweedie_p15|7|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|tweedie_p15|7|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|tweedie_p15|7|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|tweedie_selected_p|7|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|tweedie_selected_p|7|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|tweedie_selected_p|7|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|tweedie_selected_p|7|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|kernel_normal_equal|8|1880|0|0|0|0|0|0|0|1880|
|1mon|t15m|kernel_normal_equal|8|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|kernel_normal_equal|8|1410|0|0|0|0|0|0|0|1410|
|3mon|t15m|kernel_normal_equal|8|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|kernel_rain_hurdle_equal|8|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|kernel_rain_hurdle_equal|8|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|kernel_rain_hurdle_equal|8|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|kernel_rain_hurdle_equal|8|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|bma_group_normal|8|1880|0|0|0|0|0|0|0|1880|
|1mon|t15m|bma_group_normal|8|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|bma_group_normal|8|1410|0|0|0|0|0|0|0|1410|
|3mon|t15m|bma_group_normal|8|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|bma_group_rain|8|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|bma_group_rain|8|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|bma_group_rain|8|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|bma_group_rain|8|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|bma_component_pool|8|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|bma_component_pool|8|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|bma_component_pool|8|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|bma_component_pool|8|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|pooled_mos_ridge|9|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|pooled_mos_ridge|9|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|pooled_mos_ridge|9|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|pooled_mos_ridge|9|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|pooled_emos_ridge|9|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|pooled_emos_ridge|9|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|pooled_emos_ridge|9|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|pooled_emos_ridge|9|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|pooled_emos_cyclic|9|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|pooled_emos_cyclic|9|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|pooled_emos_cyclic|9|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|pooled_emos_cyclic|9|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|bjp_t|10|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|bjp_t|10|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|bjp_t|10|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|bjp_t|10|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|bjp_ti|10|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|bjp_ti|10|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|bjp_ti|10|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|bjp_ti|10|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|detrend_qm|10|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|detrend_qm|10|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|detrend_qm|10|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|detrend_qm|10|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|detrend_qdm|10|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|detrend_qdm|10|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|detrend_qdm|10|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|detrend_qdm|10|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|detrend_emos|10|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|detrend_emos|10|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|detrend_emos|10|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|detrend_emos|10|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|ordinal_logit|11|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|ordinal_logit|11|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|ordinal_logit|11|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|ordinal_logit|11|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|elr_threshold_logit|11|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|elr_threshold_logit|11|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|elr_threshold_logit|11|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|elr_threshold_logit|11|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|gamlss_ridge|12|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|gamlss_ridge|12|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|gamlss_ridge|12|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|gamlss_ridge|12|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|componentwise_boost|12|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|componentwise_boost|12|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|componentwise_boost|12|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|componentwise_boost|12|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|ngboost_small|12|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|ngboost_small|12|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|ngboost_small|12|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|ngboost_small|12|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|qrf_year_forest|13|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|qrf_year_forest|13|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|qrf_year_forest|13|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|qrf_year_forest|13|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|idr_mean_order|13|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|idr_mean_order|13|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|idr_mean_order|13|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|idr_mean_order|13|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|drn_small|14|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|drn_small|14|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|drn_small|14|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|drn_small|14|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|bqn_monotone|14|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|bqn_monotone|14|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|bqn_monotone|14|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|bqn_monotone|14|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|finite_member_iid_signal_noise|17|1880|0|0|0|0|0|0|0|1880|
|1mon|t15m|finite_member_iid_signal_noise|17|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|finite_member_iid_signal_noise|17|1410|0|0|0|0|0|0|0|1410|
|3mon|t15m|finite_member_iid_signal_noise|17|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|finite_member_known_covariance|17|1880|0|0|0|0|0|0|0|1880|
|1mon|t15m|finite_member_known_covariance|17|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|finite_member_known_covariance|17|1410|0|0|0|0|0|0|0|1410|
|3mon|t15m|finite_member_known_covariance|17|1410|1410|0|68|1342|0|0|0|1410|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcp_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbjp_niw|16|1|0|1|0|0|0|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|otc_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|mbcp_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|mbjp_niw|16|1|0|1|0|0|0|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|otc_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcp_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbjp_niw|16|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|otc_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcp_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbjp_niw|16|1|0|1|0|0|0|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|otc_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|mbcp_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|mbjp_niw|16|1|0|1|0|0|0|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|otc_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcp_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbjp_niw|16|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|otc_annual|16|1|1|0|0|1|1|0|0|0|

## 2. 실제 원단위 및 범주·결합 점수
주간(1mon: 7일)과 월간(3mon: 개별 달), 기온(degC)과 강수(mm)는 합치지 않는다.
아래 값은 성공 사례 제한 평균이다. 서로 다른 N의 평균을 전체 우열로 해석하지 않는다.
|상품|변수/벡터|방법|점수|평가 N|평균 손실|
|---|---|---|---|---:|---:|
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
|1mon|t15m|climatology_empirical|CRPS|1|3.034965037762418|
|1mon|t15m|climatology_empirical|BRIER|1|0.6666666666666664|
|1mon|t15m|climatology_empirical|RPS|1|0.5555555555555554|
|3mon|t15m|EMOS|CRPS|1|0.7080114831607017|
|3mon|t15m|EMOS|BRIER|1|0.31405048231019905|
|3mon|t15m|EMOS|RPS|1|0.28223011061018205|
|3mon|t15m|QDM|CRPS|1|0.3977865902149049|
|3mon|t15m|QDM|BRIER|1|0.1938775510204082|
|3mon|t15m|QDM|RPS|1|0.14795918367346939|
|3mon|t15m|QM|CRPS|1|0.3362119519695109|
|3mon|t15m|QM|BRIER|1|0.058956916099773236|
|3mon|t15m|QM|RPS|1|0.05668934240362811|
|3mon|t15m|RAW|CRPS|1|1.964476031014557|
|3mon|t15m|RAW|BRIER|1|1.256235827664399|
|3mon|t15m|RAW|RPS|1|1.145124716553288|
|3mon|t15m|climatology_empirical|CRPS|1|1.0725647468760442|
|3mon|t15m|climatology_empirical|BRIER|1|0.6666666666666664|
|3mon|t15m|climatology_empirical|RPS|1|0.5555555555555554|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcp_annual|ENERGY|1|6.159649308769293|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcp_annual|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcp_annual|VARIOGRAM|1|0.41494709701798066|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|otc_annual|ENERGY|1|3.0543996332280323|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|otc_annual|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|otc_annual|VARIOGRAM|1|0.21089171222395553|
|1mon|["prcp:W01","t15m:W01"]|mbcp_annual|ENERGY|1|1.1667312790177955|
|1mon|["prcp:W01","t15m:W01"]|mbcp_annual|HOT_DRY_BRIER|1|0.18367346938775503|
|1mon|["prcp:W01","t15m:W01"]|mbcp_annual|VARIOGRAM|1|0.2643663894033223|
|1mon|["prcp:W01","t15m:W01"]|otc_annual|ENERGY|1|0.5027948907025043|
|1mon|["prcp:W01","t15m:W01"]|otc_annual|HOT_DRY_BRIER|1|0.0|
|1mon|["prcp:W01","t15m:W01"]|otc_annual|VARIOGRAM|1|0.00974949905693539|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcp_annual|ENERGY|1|2.2995465704231868|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcp_annual|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcp_annual|VARIOGRAM|1|0.41095015732910606|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbjp_niw|ENERGY|1|2.537893872341632|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbjp_niw|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbjp_niw|VARIOGRAM|1|0.5656643925211519|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|otc_annual|ENERGY|1|1.6884171949372555|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|otc_annual|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|otc_annual|VARIOGRAM|1|0.11466390826475074|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcp_annual|ENERGY|1|5.539526574659876|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcp_annual|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcp_annual|VARIOGRAM|1|0.34343721125979654|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|otc_annual|ENERGY|1|3.030180263954204|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|otc_annual|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|otc_annual|VARIOGRAM|1|0.21615272161168564|
|3mon|["prcp:M01","t15m:M01"]|mbcp_annual|ENERGY|1|1.4392861201718998|
|3mon|["prcp:M01","t15m:M01"]|mbcp_annual|HOT_DRY_BRIER|1|1.0|
|3mon|["prcp:M01","t15m:M01"]|mbcp_annual|VARIOGRAM|1|0.09736956712912676|
|3mon|["prcp:M01","t15m:M01"]|otc_annual|ENERGY|1|0.5328058103540164|
|3mon|["prcp:M01","t15m:M01"]|otc_annual|HOT_DRY_BRIER|1|0.44444444444444453|
|3mon|["prcp:M01","t15m:M01"]|otc_annual|VARIOGRAM|1|0.1805046734994268|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcp_annual|ENERGY|1|1.5429431793501946|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcp_annual|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcp_annual|VARIOGRAM|1|0.21084422391671068|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbjp_niw|ENERGY|1|3.034743898941435|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbjp_niw|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbjp_niw|VARIOGRAM|1|1.6661421203533109|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|otc_annual|ENERGY|1|1.3492365507086077|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|otc_annual|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|otc_annual|VARIOGRAM|1|0.12952879283381333|

## 3. 동일 성공 마스크의 비교
paired_comparison.csv는 동일 사례에서만 손실 차이를 계산한다. 음수는 첫 방법의 작은 손실을 뜻한다.
common_masks.csv에 모든 정확한 사례 ID, SHA256, 사전 지정 레지스트리 family_no 교집합을 보존한다.
저장된 공통마스크 점수 행: 19740. 빈 교집합도 숨기지 않는다.
lead/month/season/year별 결과는 각 점수 표에 있으며 범주 전용은 RPS/Brier만 산출한다.
다음은 EMOS가 포함된 동일 사례 손실 차이의 실제 수치이며 우월성·유의성 판정이 아니다.
|상품|변수|첫 방법−둘째 방법|점수|공통 N|손실 차이|마스크 SHA256|
|---|---|---|---|---:|---:|---|
|1mon|prcp|["EMOS", "QDM"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "QDM"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "QDM"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "QM"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "QM"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "QM"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "RAW"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "RAW"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "RAW"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "anomaly_mos"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "anomaly_mos"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "anomaly_mos"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "anomaly_signal_shrink"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "anomaly_signal_shrink"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "anomaly_signal_shrink"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bayesian_anomaly_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bayesian_anomaly_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bayesian_anomaly_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_logsinh_fixed"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_logsinh_fixed"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_logsinh_fixed"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_sqrt_censored"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_sqrt_censored"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_sqrt_censored"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_t"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_t"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_t"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_ti"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_ti"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_ti"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_yj_fixed"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_yj_fixed"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bjp_yj_fixed"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bma_component_pool"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bma_component_pool"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bma_component_pool"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bma_group_rain"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bma_group_rain"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bma_group_rain"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bqn_monotone"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bqn_monotone"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bqn_monotone"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "cdf_mix_cv"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "cdf_mix_cv"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "cdf_mix_cv"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "cdf_mix_fixed50"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "cdf_mix_fixed50"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "cdf_mix_fixed50"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "climatology_empirical"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "climatology_empirical"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "climatology_empirical"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "componentwise_boost"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "componentwise_boost"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "componentwise_boost"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "csg_estimated_shift"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "csg_estimated_shift"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "csg_estimated_shift"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "csg_fixed_shift"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "csg_fixed_shift"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "csg_fixed_shift"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "detrend_emos"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "detrend_emos"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "detrend_emos"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "detrend_qdm"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "detrend_qdm"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "detrend_qdm"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "detrend_qm"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "detrend_qm"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "detrend_qm"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "drn_small"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "drn_small"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "drn_small"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "emos_constant_variance"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "emos_constant_variance"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "emos_constant_variance"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gamlss_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gamlss_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gamlss_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gamma_positive"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gamma_positive"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gamma_positive"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gev_censored_gumbel"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gev_censored_gumbel"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gev_censored_gumbel"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "hurdle_gamma"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "hurdle_gamma"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "hurdle_gamma"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "hurdle_lognormal"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "hurdle_lognormal"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "hurdle_lognormal"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "idr_mean_order"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "idr_mean_order"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "idr_mean_order"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "mos_unit_slope"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "mos_unit_slope"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "mos_unit_slope"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "ngboost_small"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "ngboost_small"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "ngboost_small"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "pooled_emos_cyclic"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "pooled_emos_cyclic"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "pooled_emos_cyclic"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "pooled_emos_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "pooled_emos_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "pooled_emos_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "pooled_mos_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "pooled_mos_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "pooled_mos_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_gaussian_cuberoot"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_gaussian_cuberoot"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_gaussian_cuberoot"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_gaussian_sqrt"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_gaussian_sqrt"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_gaussian_sqrt"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_logistic_cuberoot"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_logistic_cuberoot"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_logistic_cuberoot"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_logistic_sqrt"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_logistic_sqrt"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_logistic_sqrt"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "qrf_year_forest"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "qrf_year_forest"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "qrf_year_forest"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "tweedie_p15"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "tweedie_p15"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "tweedie_p15"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "tweedie_selected_p"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "tweedie_selected_p"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "tweedie_selected_p"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "QDM"]|CRPS|1|0.2509389270272258|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "QDM"]|BRIER|1|0.012740795083868463|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "QDM"]|RPS|1|0.006642102522196432|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "QM"]|CRPS|1|0.1935711986399019|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "QM"]|BRIER|1|0.012740795083868463|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "QM"]|RPS|1|0.006642102522196432|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "RAW"]|CRPS|1|-0.6672971316378451|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "RAW"]|BRIER|1|0.012740795083868463|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "RAW"]|RPS|1|0.006642102522196432|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "anomaly_mos"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "anomaly_mos"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "anomaly_mos"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "anomaly_signal_shrink"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "anomaly_signal_shrink"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "anomaly_signal_shrink"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bjp_niw"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bjp_niw"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bjp_niw"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bjp_t"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bjp_t"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bjp_t"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bjp_ti"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bjp_ti"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bjp_ti"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bma_component_pool"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bma_component_pool"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bma_component_pool"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bma_group_normal"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bma_group_normal"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bma_group_normal"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bqn_monotone"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bqn_monotone"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bqn_monotone"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "cdf_mix_cv"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "cdf_mix_cv"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "cdf_mix_cv"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "cdf_mix_fixed50"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "cdf_mix_fixed50"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "cdf_mix_fixed50"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "climatology_empirical"]|CRPS|1|-2.391794595009217|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "climatology_empirical"]|BRIER|1|-0.6539258715827979|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "climatology_empirical"]|RPS|1|-0.5489134530333589|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "componentwise_boost"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "componentwise_boost"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "componentwise_boost"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "detrend_emos"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "detrend_emos"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "detrend_emos"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "detrend_qdm"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "detrend_qdm"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "detrend_qdm"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "detrend_qm"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "detrend_qm"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "detrend_qm"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "drn_small"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "drn_small"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "drn_small"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "emos_constant_variance"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "emos_constant_variance"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "emos_constant_variance"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "finite_member_iid_signal_noise"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "finite_member_iid_signal_noise"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "finite_member_iid_signal_noise"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "finite_member_known_covariance"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "finite_member_known_covariance"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "finite_member_known_covariance"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "gamlss_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "gamlss_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "gamlss_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "idr_mean_order"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "idr_mean_order"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "idr_mean_order"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "joint_gaussian_plugin"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "joint_gaussian_plugin"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "joint_gaussian_plugin"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "kernel_normal_equal"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "kernel_normal_equal"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "kernel_normal_equal"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "mos_unit_slope"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "mos_unit_slope"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "mos_unit_slope"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "ngboost_small"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "ngboost_small"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "ngboost_small"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "pooled_emos_cyclic"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "pooled_emos_cyclic"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "pooled_emos_cyclic"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "pooled_emos_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "pooled_emos_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "pooled_emos_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "pooled_mos_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "pooled_mos_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "pooled_mos_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "qrf_year_forest"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "qrf_year_forest"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "qrf_year_forest"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "QDM"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "QDM"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "QDM"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "QM"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "QM"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "QM"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "RAW"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "RAW"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "RAW"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "anomaly_mos"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "anomaly_mos"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "anomaly_mos"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "anomaly_signal_shrink"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "anomaly_signal_shrink"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "anomaly_signal_shrink"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bayesian_anomaly_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bayesian_anomaly_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bayesian_anomaly_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_logsinh_fixed"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_logsinh_fixed"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_logsinh_fixed"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_sqrt_censored"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_sqrt_censored"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_sqrt_censored"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_t"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_t"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_t"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_ti"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_ti"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_ti"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_yj_fixed"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_yj_fixed"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bjp_yj_fixed"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bma_component_pool"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bma_component_pool"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bma_component_pool"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bma_group_rain"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bma_group_rain"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bma_group_rain"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bqn_monotone"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bqn_monotone"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bqn_monotone"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "cdf_mix_cv"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "cdf_mix_cv"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "cdf_mix_cv"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "cdf_mix_fixed50"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "cdf_mix_fixed50"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "cdf_mix_fixed50"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "climatology_empirical"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "climatology_empirical"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "climatology_empirical"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "componentwise_boost"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "componentwise_boost"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "componentwise_boost"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "csg_estimated_shift"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "csg_estimated_shift"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "csg_estimated_shift"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "csg_fixed_shift"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "csg_fixed_shift"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "csg_fixed_shift"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "detrend_emos"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "detrend_emos"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "detrend_emos"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "detrend_qdm"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "detrend_qdm"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "detrend_qdm"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "detrend_qm"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "detrend_qm"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "detrend_qm"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "drn_small"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "drn_small"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "drn_small"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "emos_constant_variance"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "emos_constant_variance"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "emos_constant_variance"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "gamlss_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "gamlss_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "gamlss_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "gamma_positive"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "gamma_positive"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "gamma_positive"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "gev_censored_gumbel"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "gev_censored_gumbel"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "gev_censored_gumbel"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "hurdle_gamma"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "hurdle_gamma"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "hurdle_gamma"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "hurdle_lognormal"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "hurdle_lognormal"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "hurdle_lognormal"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "idr_mean_order"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "idr_mean_order"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "idr_mean_order"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "mos_unit_slope"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "mos_unit_slope"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "mos_unit_slope"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "ngboost_small"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "ngboost_small"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "ngboost_small"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "pooled_emos_cyclic"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "pooled_emos_cyclic"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "pooled_emos_cyclic"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "pooled_emos_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "pooled_emos_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "pooled_emos_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "pooled_mos_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "pooled_mos_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "pooled_mos_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "power_gaussian_cuberoot"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "power_gaussian_cuberoot"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "power_gaussian_cuberoot"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "power_gaussian_sqrt"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "power_gaussian_sqrt"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "power_gaussian_sqrt"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "power_logistic_cuberoot"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "power_logistic_cuberoot"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "power_logistic_cuberoot"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "power_logistic_sqrt"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "power_logistic_sqrt"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "power_logistic_sqrt"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "qrf_year_forest"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "qrf_year_forest"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "qrf_year_forest"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "tweedie_p15"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "tweedie_p15"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "tweedie_p15"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "tweedie_selected_p"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "tweedie_selected_p"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "tweedie_selected_p"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "QDM"]|CRPS|1|0.3102248929457968|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "QDM"]|BRIER|1|0.12017293128979084|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "QDM"]|RPS|1|0.13427092693671266|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "QM"]|CRPS|1|0.3717995311911908|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "QM"]|BRIER|1|0.25509356621042584|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "QM"]|RPS|1|0.22554076820655394|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "RAW"]|CRPS|1|-1.2564645478538554|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "RAW"]|BRIER|1|-0.9421853453542|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "RAW"]|RPS|1|-0.862894605943106|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "anomaly_mos"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "anomaly_mos"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "anomaly_mos"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "anomaly_signal_shrink"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "anomaly_signal_shrink"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "anomaly_signal_shrink"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bjp_niw"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bjp_niw"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bjp_niw"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bjp_t"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bjp_t"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bjp_t"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bjp_ti"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bjp_ti"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bjp_ti"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bma_component_pool"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bma_component_pool"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bma_component_pool"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bma_group_normal"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bma_group_normal"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bma_group_normal"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bqn_monotone"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bqn_monotone"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bqn_monotone"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "cdf_mix_cv"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "cdf_mix_cv"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "cdf_mix_cv"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "cdf_mix_fixed50"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "cdf_mix_fixed50"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "cdf_mix_fixed50"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "climatology_empirical"]|CRPS|1|-0.36455326371534247|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "climatology_empirical"]|BRIER|1|-0.35261618435646735|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "climatology_empirical"]|RPS|1|-0.2733254449453733|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "componentwise_boost"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "componentwise_boost"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "componentwise_boost"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "detrend_emos"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "detrend_emos"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "detrend_emos"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "detrend_qdm"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "detrend_qdm"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "detrend_qdm"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "detrend_qm"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "detrend_qm"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "detrend_qm"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "drn_small"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "drn_small"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "drn_small"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "emos_constant_variance"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "emos_constant_variance"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "emos_constant_variance"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "finite_member_iid_signal_noise"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "finite_member_iid_signal_noise"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "finite_member_iid_signal_noise"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "finite_member_known_covariance"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "finite_member_known_covariance"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "finite_member_known_covariance"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "gamlss_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "gamlss_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "gamlss_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "idr_mean_order"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "idr_mean_order"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "idr_mean_order"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "joint_gaussian_plugin"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "joint_gaussian_plugin"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "joint_gaussian_plugin"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "kernel_normal_equal"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "kernel_normal_equal"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "kernel_normal_equal"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "mos_unit_slope"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "mos_unit_slope"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "mos_unit_slope"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "ngboost_small"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "ngboost_small"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "ngboost_small"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "pooled_emos_cyclic"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "pooled_emos_cyclic"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "pooled_emos_cyclic"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "pooled_emos_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "pooled_emos_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "pooled_emos_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "pooled_mos_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "pooled_mos_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "pooled_mos_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "qrf_year_forest"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "qrf_year_forest"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "qrf_year_forest"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|

## 4. 실패를 포함한 운용 정책과 손실 한계
failure_inclusive_policy.csv의 method+climatology_on_failure는 별도 정책이다.
실패한 원방법 상태·분포를 변경하지 않으며, 같은 외부 훈련 경험 기후값으로 실패 사례를 평가한다.
미기록 또는 미실행 상태는 성공도 실패 대체도 아니다. 정책이 불완전하면 평균은 비운다.
비음수 점수의 미평가 손실 한계는 [성공 손실 합/N, +inf]이며 유한 벌점을 만들지 않는다.
정책 행: 682; 상세 대체 출처는 failure_policy_cases.csv에 있다.

## 5. 반복 관측창·연도 민감도
동일 변수/상품/정확한 VALID_START-END 창 총 가중치 1을 발행들에 나눈다.
year_overlap_sensitivity.csv는 같은 창을 묶은 연도 블록 및 연결된 중첩창 블록 재표본화(999회),
연도별 차이와 한 연도 제외 차이를 기록한다. 실제 약 5개 검증 연도로 강한 유의성·인과 주장을 하지 않는다.

## 6. 분포·강수 사건·결합 근사
원래 해석적 주변분포 점수와 유한 시나리오 투영 주변점수는 별도 산출물이다.
결합 ENERGY/VARIOGRAM 및 실제 저장된 사건 Brier는 벡터 범위별로만 비교한다.
PIT는 F(y-)와 F(y) 사이 원자 질량을 고정 시드로 무작위화한다.
상위 강수 사건은 외부 훈련 90% 분위수 초과로 고정되며 검증 정답으로 임계값을 고르지 않는다.
원분포 진단 행: 10; 원분포가 없거나 복원 실패하면 MISSING/ERROR를 표시한다.

## 7. 완전성·근거 및 해석 한계
필수 산출물 결측: [].
report_manifest.json은 범위·시드·필수 산출물·진단 결측·마스크 정의·그림 경로를 기록한다.
모든 방법 전체 실행, 독립 검증 및 최종 수동 QA는 별도 증거가 필요하다.
유리한 일부 사례나 성공만으로 최선·우월·실험 PASS라고 주장하지 않는다.
RAW/QM/QDM/EMOS 비교도 위와 동일한 적용범위·공통마스크·실패정책 규칙을 따른다.
