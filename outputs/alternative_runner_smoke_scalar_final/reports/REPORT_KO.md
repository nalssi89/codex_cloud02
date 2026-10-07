# 통계 대안 공정 비교 보고서

- 실행 범위: `SMOKE`; 보고 상태: `INCOMPLETE`.
- 원실행 상태: `RUNNING`. 진행·중단·실패 실행은 완료 보고가 아니다.
- 고정 난수 시드: 20261007. 이 문서는 저장된 실제 예측만 분석한다.
- 전체 실험 완료 또는 통계적 유의성을 이 보고서만으로 주장하지 않는다.

## 1. 성능 비교에 앞선 실제 적용·성공 범위
|상품|변수/벡터|방법|계열|제공|도메인 적용|과학적 게이트|결측 정답|평가 가능|평가 성공|적합 실패|수치/점수 실패|미기록|
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|1mon|prcp|RAW|0|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|RAW|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|RAW|0|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|RAW|0|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|QM|0|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|QM|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|QM|0|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|QM|0|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|QDM|0|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|QDM|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|QDM|0|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|QDM|0|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|EMOS|0|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|EMOS|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|EMOS|0|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|EMOS|0|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|climatology_empirical|0|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|climatology_empirical|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|climatology_empirical|0|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|climatology_empirical|0|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|joint_gaussian_plugin|1|1880|0|0|0|0|0|0|0|1880|
|1mon|t15m|joint_gaussian_plugin|1|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|joint_gaussian_plugin|1|1410|0|0|0|0|0|0|0|1410|
|3mon|t15m|joint_gaussian_plugin|1|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|bjp_niw|1|1880|0|1|0|0|0|0|0|1879|
|1mon|t15m|bjp_niw|1|1880|1880|0|6|1874|1|0|0|1879|
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
|1mon|prcp|cdf_mix_fixed50|2|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|cdf_mix_fixed50|2|1880|1880|0|6|1874|1|0|0|1879|
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
|1mon|prcp|anomaly_mos|3|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|anomaly_mos|3|1880|1880|0|6|1874|1|0|0|1879|
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
|1mon|prcp|gamma_positive|4|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|gamma_positive|4|1880|0|1|0|0|0|0|0|1879|
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
|1mon|prcp|power_gaussian_sqrt|5|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|power_gaussian_sqrt|5|1880|0|1|0|0|0|0|0|1879|
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
|1mon|prcp|hurdle_gamma|6|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|hurdle_gamma|6|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|hurdle_gamma|6|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|hurdle_gamma|6|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|hurdle_lognormal|6|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|hurdle_lognormal|6|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|hurdle_lognormal|6|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|hurdle_lognormal|6|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|gev_censored_gumbel|7|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|gev_censored_gumbel|7|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|gev_censored_gumbel|7|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|gev_censored_gumbel|7|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|gev_censored_shrunk_shape|7|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|gev_censored_shrunk_shape|7|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|gev_censored_shrunk_shape|7|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|gev_censored_shrunk_shape|7|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|tweedie_p15|7|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|tweedie_p15|7|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|tweedie_p15|7|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|tweedie_p15|7|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|tweedie_selected_p|7|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|tweedie_selected_p|7|1880|0|0|0|0|0|0|0|1880|
|3mon|prcp|tweedie_selected_p|7|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|tweedie_selected_p|7|1410|0|0|0|0|0|0|0|1410|
|1mon|prcp|kernel_normal_equal|8|1880|0|1|0|0|0|0|0|1879|
|1mon|t15m|kernel_normal_equal|8|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|kernel_normal_equal|8|1410|0|0|0|0|0|0|0|1410|
|3mon|t15m|kernel_normal_equal|8|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|kernel_rain_hurdle_equal|8|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|kernel_rain_hurdle_equal|8|1880|0|1|0|0|0|0|0|1879|
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
|1mon|prcp|pooled_mos_ridge|9|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|pooled_mos_ridge|9|1880|1880|0|6|1874|1|0|0|1879|
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
|1mon|prcp|bjp_t|10|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|bjp_t|10|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|bjp_t|10|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|bjp_t|10|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|bjp_ti|10|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|bjp_ti|10|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|bjp_ti|10|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|bjp_ti|10|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|detrend_qm|10|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|detrend_qm|10|1880|1880|0|6|1874|1|0|0|1879|
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
|1mon|prcp|ordinal_logit|11|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|ordinal_logit|11|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|ordinal_logit|11|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|ordinal_logit|11|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|elr_threshold_logit|11|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|elr_threshold_logit|11|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|elr_threshold_logit|11|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|elr_threshold_logit|11|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|gamlss_ridge|12|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|gamlss_ridge|12|1880|1880|0|6|1874|1|0|0|1879|
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
|1mon|prcp|qrf_year_forest|13|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|qrf_year_forest|13|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|qrf_year_forest|13|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|qrf_year_forest|13|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|idr_mean_order|13|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|idr_mean_order|13|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|idr_mean_order|13|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|idr_mean_order|13|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|drn_small|14|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|drn_small|14|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|drn_small|14|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|drn_small|14|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|bqn_monotone|14|1880|1880|0|6|1874|0|0|0|1880|
|1mon|t15m|bqn_monotone|14|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|bqn_monotone|14|1410|1410|0|68|1342|0|0|0|1410|
|3mon|t15m|bqn_monotone|14|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|finite_member_iid_signal_noise|17|1880|0|1|0|0|0|0|0|1879|
|1mon|t15m|finite_member_iid_signal_noise|17|1880|1880|1|6|1873|0|0|0|1879|
|3mon|prcp|finite_member_iid_signal_noise|17|1410|0|0|0|0|0|0|0|1410|
|3mon|t15m|finite_member_iid_signal_noise|17|1410|1410|0|68|1342|0|0|0|1410|
|1mon|prcp|finite_member_known_covariance|17|1880|0|0|0|0|0|0|0|1880|
|1mon|t15m|finite_member_known_covariance|17|1880|1880|0|6|1874|0|0|0|1880|
|3mon|prcp|finite_member_known_covariance|17|1410|0|0|0|0|0|0|0|1410|
|3mon|t15m|finite_member_known_covariance|17|1410|1410|0|68|1342|0|0|0|1410|

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
다음은 EMOS가 포함된 동일 사례 손실 차이의 실제 수치이며 우월성·유의성 판정이 아니다.
|상품|변수|첫 방법−둘째 방법|점수|공통 N|손실 차이|마스크 SHA256|
|---|---|---|---|---:|---:|---|
|1mon|prcp|["EMOS", "QDM"]|CRPS|1|0.8435179144372764|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "QDM"]|BRIER|1|-0.02539110283180268|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "QDM"]|RPS|1|-0.04832804886168962|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "QM"]|CRPS|1|-0.27780541137800796|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "QM"]|BRIER|1|-0.16824824568894547|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "QM"]|RPS|1|-0.15547090600454672|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "RAW"]|CRPS|1|3.2439601823079567|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "RAW"]|BRIER|1|0.3827721624743198|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "RAW"]|RPS|1|0.4414678695056573|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "anomaly_mos"]|CRPS|1|1.7570135076789644|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "anomaly_mos"]|BRIER|1|0.19952215749284208|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "anomaly_mos"]|RPS|1|0.21755320338240197|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
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
|1mon|prcp|["EMOS", "bjp_t"]|CRPS|1|1.5502133439637937|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_t"]|BRIER|1|0.2446037906501879|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_t"]|RPS|1|0.18942735314107884|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
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
|1mon|prcp|["EMOS", "cdf_mix_fixed50"]|CRPS|1|1.2709929620866731|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "cdf_mix_fixed50"]|BRIER|1|0.06228107179355824|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "cdf_mix_fixed50"]|RPS|1|0.08215099330169673|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "climatology_empirical"]|CRPS|1|2.3802486442346584|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "climatology_empirical"]|BRIER|1|0.11406467948112275|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "climatology_empirical"]|RPS|1|0.1563204772154081|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
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
|1mon|prcp|["EMOS", "detrend_qm"]|CRPS|1|0.00885534898767304|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "detrend_qm"]|BRIER|1|-0.16824824568894559|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "detrend_qm"]|RPS|1|-0.15547090600454683|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "drn_small"]|CRPS|1|-0.6271277977021139|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "drn_small"]|BRIER|1|-0.12346072682578624|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "drn_small"]|RPS|1|-0.03963396955847842|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "emos_constant_variance"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "emos_constant_variance"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "emos_constant_variance"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gamlss_ridge"]|CRPS|1|-1.5011268599850798|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gamlss_ridge"]|BRIER|1|-0.22760824811029567|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gamlss_ridge"]|RPS|1|-0.08571568815597819|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gamma_positive"]|CRPS|1|0.5185195393319475|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gamma_positive"]|BRIER|1|-0.018484791928028654|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gamma_positive"]|RPS|1|0.013189914620454823|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gev_censored_gumbel"]|CRPS|1|1.8888651197850201|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gev_censored_gumbel"]|BRIER|1|0.17363479204254406|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gev_censored_gumbel"]|RPS|1|0.23295537954798107|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "hurdle_gamma"]|CRPS|1|-2.3539741431582915|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "hurdle_gamma"]|BRIER|1|-0.30632895234616275|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "hurdle_gamma"]|RPS|1|-0.21142597120710827|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "hurdle_lognormal"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "hurdle_lognormal"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "hurdle_lognormal"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "idr_mean_order"]|CRPS|1|-2.514078398530078|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "idr_mean_order"]|BRIER|1|-0.27582235212137873|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "idr_mean_order"]|RPS|1|-0.02110863708932742|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|CRPS|1|-1.5481091670254497|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|BRIER|1|-0.24216634873894116|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|RPS|1|-0.1831413358781886|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
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
|1mon|prcp|["EMOS", "pooled_mos_ridge"]|CRPS|1|1.1208486191227536|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "pooled_mos_ridge"]|BRIER|1|0.012870169942970744|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "pooled_mos_ridge"]|RPS|1|-0.037452511639347486|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_gaussian_cuberoot"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_gaussian_cuberoot"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_gaussian_cuberoot"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_gaussian_sqrt"]|CRPS|1|-0.3054978199843763|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_gaussian_sqrt"]|BRIER|1|-0.08960266993855703|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_gaussian_sqrt"]|RPS|1|0.05912230303050514|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_logistic_cuberoot"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_logistic_cuberoot"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_logistic_cuberoot"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_logistic_sqrt"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_logistic_sqrt"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "power_logistic_sqrt"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "qrf_year_forest"]|CRPS|1|-0.5918804988264927|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "qrf_year_forest"]|BRIER|1|-0.11877493279403684|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "qrf_year_forest"]|RPS|1|-0.006651459259829906|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "tweedie_p15"]|CRPS|1|-1.6797227099598206|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "tweedie_p15"]|BRIER|1|-0.27751662775642005|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "tweedie_p15"]|RPS|1|-0.05162638457501223|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
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
|1mon|t15m|["EMOS", "anomaly_mos"]|CRPS|1|-0.07802331393545614|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "anomaly_mos"]|BRIER|1|0.012205140585656872|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "anomaly_mos"]|RPS|1|0.0063740824092137875|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "anomaly_signal_shrink"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "anomaly_signal_shrink"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "anomaly_signal_shrink"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bjp_niw"]|CRPS|1|-1.4556905629727765|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bjp_niw"]|BRIER|1|-0.4273112062562891|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bjp_niw"]|RPS|1|-0.41003368545753716|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bjp_t"]|CRPS|1|-1.8516971317803925|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bjp_t"]|BRIER|1|-0.5226297697279706|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bjp_t"]|RPS|1|-0.5097161032335503|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
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
|1mon|t15m|["EMOS", "cdf_mix_fixed50"]|CRPS|1|-0.8467893134287641|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "cdf_mix_fixed50"]|BRIER|1|-0.19782637840702524|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "cdf_mix_fixed50"]|RPS|1|-0.16160695537377873|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
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
|1mon|t15m|["EMOS", "detrend_qm"]|CRPS|1|-0.07542114071567085|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "detrend_qm"]|BRIER|1|0.012740795083868463|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "detrend_qm"]|RPS|1|0.006642102522196432|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "drn_small"]|CRPS|1|-0.037533579933761274|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "drn_small"]|BRIER|1|-0.003030558395445807|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "drn_small"]|RPS|1|-0.001620756562244306|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "emos_constant_variance"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "emos_constant_variance"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "emos_constant_variance"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "finite_member_iid_signal_noise"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "finite_member_iid_signal_noise"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "finite_member_iid_signal_noise"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "finite_member_known_covariance"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "finite_member_known_covariance"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "finite_member_known_covariance"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "gamlss_ridge"]|CRPS|1|-1.0729406877526497|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "gamlss_ridge"]|BRIER|1|-0.2289152945437221|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "gamlss_ridge"]|RPS|1|-0.14430034345190054|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "idr_mean_order"]|CRPS|1|0.18254326397191933|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "idr_mean_order"]|BRIER|1|0.012740795083868463|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "idr_mean_order"]|RPS|1|0.006642102522196432|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "joint_gaussian_plugin"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "joint_gaussian_plugin"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "joint_gaussian_plugin"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "kernel_normal_equal"]|CRPS|1|-0.05701782610354145|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "kernel_normal_equal"]|BRIER|1|0.008043856327195871|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "kernel_normal_equal"]|RPS|1|0.004272381267757409|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
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
|1mon|t15m|["EMOS", "pooled_mos_ridge"]|CRPS|1|0.02765282559101656|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "pooled_mos_ridge"]|BRIER|1|-0.002550443211143741|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "pooled_mos_ridge"]|RPS|1|-0.0014669536489379884|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "qrf_year_forest"]|CRPS|1|-0.3814013794251765|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "qrf_year_forest"]|BRIER|1|-0.06430486335454622|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "qrf_year_forest"]|RPS|1|-0.04744901881654148|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
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
|3mon|t15m|["EMOS", "QDM"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "QDM"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "QDM"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "QM"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "QM"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "QM"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "RAW"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "RAW"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "RAW"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
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
|3mon|t15m|["EMOS", "climatology_empirical"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "climatology_empirical"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "climatology_empirical"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
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
원분포 진단 행: 36; 원분포가 없거나 복원 실패하면 MISSING/ERROR를 표시한다.

## 7. 완전성·근거 및 해석 한계
필수 산출물 결측: [].
report_manifest.json은 범위·시드·필수 산출물·진단 결측·마스크 정의·그림 경로를 기록한다.
모든 방법 전체 실행, 독립 검증 및 최종 수동 QA는 별도 증거가 필요하다.
유리한 일부 사례나 성공만으로 최선·우월·실험 PASS라고 주장하지 않는다.
RAW/QM/QDM/EMOS 비교도 위와 동일한 적용범위·공통마스크·실패정책 규칙을 따른다.
