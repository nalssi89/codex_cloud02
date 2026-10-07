# 통계 대안 공정 비교 보고서

- 실행 범위: `SMOKE`; 보고 상태: `INCOMPLETE`.
- 원실행 상태: `FAILED_REPORTING`. 진행·중단·실패 실행은 완료 보고가 아니다.
- 고정 난수 시드: 20261007. 이 문서는 저장된 실제 예측만 분석한다.
- 전체 실험 완료 또는 통계적 유의성을 이 보고서만으로 주장하지 않는다.

## 1. 성능 비교에 앞선 실제 적용·성공 범위
|상품|변수/벡터|방법|계열|제공|도메인 적용|과학적 게이트|결측 정답|평가 가능|평가 성공|적합 실패|수치/점수 실패|미기록|
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|1mon|prcp|RAW|0|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|RAW|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|RAW|0|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|RAW|0|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|QM|0|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|QM|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|QM|0|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|QM|0|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|QDM|0|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|QDM|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|QDM|0|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|QDM|0|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|EMOS|0|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|EMOS|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|EMOS|0|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|EMOS|0|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|climatology_empirical|0|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|climatology_empirical|0|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|climatology_empirical|0|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|climatology_empirical|0|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|joint_gaussian_plugin|1|1880|0|1|0|0|0|0|0|1879|
|1mon|t15m|joint_gaussian_plugin|1|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|joint_gaussian_plugin|1|1410|0|1|0|0|0|0|0|1409|
|3mon|t15m|joint_gaussian_plugin|1|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|bjp_niw|1|1880|0|1|0|0|0|0|0|1879|
|1mon|t15m|bjp_niw|1|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|bjp_niw|1|1410|0|1|0|0|0|0|0|1409|
|3mon|t15m|bjp_niw|1|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|bjp_sqrt_censored|1|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|bjp_sqrt_censored|1|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|bjp_sqrt_censored|1|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|bjp_sqrt_censored|1|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|bjp_yj_fixed|1|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|bjp_yj_fixed|1|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|bjp_yj_fixed|1|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|bjp_yj_fixed|1|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|bjp_logsinh_fixed|1|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|bjp_logsinh_fixed|1|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|bjp_logsinh_fixed|1|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|bjp_logsinh_fixed|1|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|bayesian_anomaly_ridge|1|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|bayesian_anomaly_ridge|1|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|bayesian_anomaly_ridge|1|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|bayesian_anomaly_ridge|1|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|cdf_mix_fixed50|2|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|cdf_mix_fixed50|2|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|cdf_mix_fixed50|2|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|cdf_mix_fixed50|2|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|cdf_mix_cv|2|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|cdf_mix_cv|2|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|cdf_mix_cv|2|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|cdf_mix_cv|2|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|anomaly_signal_shrink|2|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|anomaly_signal_shrink|2|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|anomaly_signal_shrink|2|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|anomaly_signal_shrink|2|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|anomaly_mos|3|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|anomaly_mos|3|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|anomaly_mos|3|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|anomaly_mos|3|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|emos_constant_variance|3|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|emos_constant_variance|3|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|emos_constant_variance|3|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|emos_constant_variance|3|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|mos_unit_slope|3|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|mos_unit_slope|3|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|mos_unit_slope|3|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|mos_unit_slope|3|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|gamma_positive|4|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|gamma_positive|4|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|gamma_positive|4|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|gamma_positive|4|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|csg_fixed_shift|4|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|csg_fixed_shift|4|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|csg_fixed_shift|4|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|csg_fixed_shift|4|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|csg_estimated_shift|4|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|csg_estimated_shift|4|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|csg_estimated_shift|4|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|csg_estimated_shift|4|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|power_gaussian_sqrt|5|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|power_gaussian_sqrt|5|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|power_gaussian_sqrt|5|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|power_gaussian_sqrt|5|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|power_gaussian_cuberoot|5|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|power_gaussian_cuberoot|5|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|power_gaussian_cuberoot|5|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|power_gaussian_cuberoot|5|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|power_logistic_sqrt|5|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|power_logistic_sqrt|5|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|power_logistic_sqrt|5|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|power_logistic_sqrt|5|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|power_logistic_cuberoot|5|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|power_logistic_cuberoot|5|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|power_logistic_cuberoot|5|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|power_logistic_cuberoot|5|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|hurdle_gamma|6|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|hurdle_gamma|6|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|hurdle_gamma|6|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|hurdle_gamma|6|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|hurdle_lognormal|6|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|hurdle_lognormal|6|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|hurdle_lognormal|6|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|hurdle_lognormal|6|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|gev_censored_gumbel|7|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|gev_censored_gumbel|7|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|gev_censored_gumbel|7|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|gev_censored_gumbel|7|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|gev_censored_shrunk_shape|7|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|gev_censored_shrunk_shape|7|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|gev_censored_shrunk_shape|7|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|gev_censored_shrunk_shape|7|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|tweedie_p15|7|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|tweedie_p15|7|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|tweedie_p15|7|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|tweedie_p15|7|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|tweedie_selected_p|7|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|tweedie_selected_p|7|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|tweedie_selected_p|7|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|tweedie_selected_p|7|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|kernel_normal_equal|8|1880|0|1|0|0|0|0|0|1879|
|1mon|t15m|kernel_normal_equal|8|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|kernel_normal_equal|8|1410|0|1|0|0|0|0|0|1409|
|3mon|t15m|kernel_normal_equal|8|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|kernel_rain_hurdle_equal|8|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|kernel_rain_hurdle_equal|8|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|kernel_rain_hurdle_equal|8|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|kernel_rain_hurdle_equal|8|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|bma_group_normal|8|1880|0|1|0|0|0|0|0|1879|
|1mon|t15m|bma_group_normal|8|1880|1880|1|6|1873|0|0|0|1879|
|3mon|prcp|bma_group_normal|8|1410|0|1|0|0|0|0|0|1409|
|3mon|t15m|bma_group_normal|8|1410|1410|1|68|1341|0|0|0|1409|
|1mon|prcp|bma_group_rain|8|1880|1880|1|6|1873|0|0|0|1879|
|1mon|t15m|bma_group_rain|8|1880|0|1|0|0|0|0|0|1879|
|3mon|prcp|bma_group_rain|8|1410|1410|1|68|1341|0|0|0|1409|
|3mon|t15m|bma_group_rain|8|1410|0|1|0|0|0|0|0|1409|
|1mon|prcp|bma_component_pool|8|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|bma_component_pool|8|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|bma_component_pool|8|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|bma_component_pool|8|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|pooled_mos_ridge|9|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|pooled_mos_ridge|9|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|pooled_mos_ridge|9|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|pooled_mos_ridge|9|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|pooled_emos_ridge|9|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|pooled_emos_ridge|9|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|pooled_emos_ridge|9|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|pooled_emos_ridge|9|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|pooled_emos_cyclic|9|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|pooled_emos_cyclic|9|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|pooled_emos_cyclic|9|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|pooled_emos_cyclic|9|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|bjp_t|10|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|bjp_t|10|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|bjp_t|10|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|bjp_t|10|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|bjp_ti|10|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|bjp_ti|10|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|bjp_ti|10|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|bjp_ti|10|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|detrend_qm|10|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|detrend_qm|10|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|detrend_qm|10|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|detrend_qm|10|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|detrend_qdm|10|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|detrend_qdm|10|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|detrend_qdm|10|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|detrend_qdm|10|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|detrend_emos|10|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|detrend_emos|10|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|detrend_emos|10|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|detrend_emos|10|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|ordinal_logit|11|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|ordinal_logit|11|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|ordinal_logit|11|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|ordinal_logit|11|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|elr_threshold_logit|11|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|elr_threshold_logit|11|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|elr_threshold_logit|11|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|elr_threshold_logit|11|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|gamlss_ridge|12|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|gamlss_ridge|12|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|gamlss_ridge|12|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|gamlss_ridge|12|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|componentwise_boost|12|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|componentwise_boost|12|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|componentwise_boost|12|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|componentwise_boost|12|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|ngboost_small|12|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|ngboost_small|12|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|ngboost_small|12|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|ngboost_small|12|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|qrf_year_forest|13|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|qrf_year_forest|13|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|qrf_year_forest|13|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|qrf_year_forest|13|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|idr_mean_order|13|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|idr_mean_order|13|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|idr_mean_order|13|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|idr_mean_order|13|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|drn_small|14|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|drn_small|14|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|drn_small|14|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|drn_small|14|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|bqn_monotone|14|1880|1880|0|6|1874|1|0|0|1879|
|1mon|t15m|bqn_monotone|14|1880|1880|0|6|1874|1|0|0|1879|
|3mon|prcp|bqn_monotone|14|1410|1410|0|68|1342|1|0|0|1409|
|3mon|t15m|bqn_monotone|14|1410|1410|0|68|1342|1|0|0|1409|
|1mon|prcp|finite_member_iid_signal_noise|17|1880|0|1|0|0|0|0|0|1879|
|1mon|t15m|finite_member_iid_signal_noise|17|1880|1880|1|6|1873|0|0|0|1879|
|3mon|prcp|finite_member_iid_signal_noise|17|1410|0|1|0|0|0|0|0|1409|
|3mon|t15m|finite_member_iid_signal_noise|17|1410|1410|1|68|1341|0|0|0|1409|
|1mon|prcp|finite_member_known_covariance|17|1880|0|1|0|0|0|0|0|1879|
|1mon|t15m|finite_member_known_covariance|17|1880|1880|1|6|1873|0|0|0|1879|
|3mon|prcp|finite_member_known_covariance|17|1410|0|1|0|0|0|0|0|1409|
|3mon|t15m|finite_member_known_covariance|17|1410|1410|1|68|1341|0|0|0|1409|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|decc_path_shrunk_error__bjp|15|1|1|1|0|0|0|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|decc_path_shrunk_error__emos|15|1|1|1|0|0|0|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|dotc_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|ecc_q__bjp|15|1|1|1|0|0|0|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|ecc_q__emos|15|1|1|1|0|0|0|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbcn_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbcp_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbcr_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbjp_niw|16|1|0|1|0|0|0|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbjp_sqrt_censored|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|otc_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|residual_gaussian_copula__bjp|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|residual_gaussian_copula__emos|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_block__bjp|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_block__emos|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_window__bjp|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_window__emos|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|decc_path_shrunk_error__bjp|15|1|1|1|0|0|0|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|decc_path_shrunk_error__emos|15|1|1|1|0|0|0|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|dotc_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|ecc_q__bjp|15|1|1|1|0|0|0|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|ecc_q__emos|15|1|1|1|0|0|0|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcn_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcp_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcr_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbjp_niw|16|1|0|1|0|0|0|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbjp_sqrt_censored|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|otc_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|residual_gaussian_copula__bjp|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|residual_gaussian_copula__emos|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_block__bjp|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_block__emos|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_window__bjp|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_window__emos|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|decc_path_shrunk_error__bjp|15|1|1|1|0|0|0|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|decc_path_shrunk_error__emos|15|1|1|1|0|0|0|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|dotc_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|ecc_q__bjp|15|1|1|1|0|0|0|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|ecc_q__emos|15|1|1|1|0|0|0|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|mbcn_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|mbcp_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|mbcr_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|mbjp_niw|16|1|0|1|0|0|0|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|mbjp_sqrt_censored|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|otc_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|residual_gaussian_copula__bjp|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|residual_gaussian_copula__emos|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|schaake_block__bjp|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|schaake_block__emos|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|schaake_window__bjp|15|1|1|0|0|1|1|0|0|0|
|1mon|["prcp:W01","t15m:W01"]|schaake_window__emos|15|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|decc_path_shrunk_error__bjp|15|1|1|1|0|0|0|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|decc_path_shrunk_error__emos|15|1|1|1|0|0|0|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|dotc_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|ecc_q__bjp|15|1|1|1|0|0|0|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|ecc_q__emos|15|1|1|1|0|0|0|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcn_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcp_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcr_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbjp_niw|16|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbjp_sqrt_censored|16|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|otc_annual|16|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|residual_gaussian_copula__bjp|15|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|residual_gaussian_copula__emos|15|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_block__bjp|15|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_block__emos|15|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_window__bjp|15|1|1|0|0|1|1|0|0|0|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_window__emos|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|decc_path_shrunk_error__bjp|15|1|1|1|0|0|0|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|decc_path_shrunk_error__emos|15|1|1|1|0|0|0|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|dotc_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|ecc_q__bjp|15|1|1|1|0|0|0|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|ecc_q__emos|15|1|1|1|0|0|0|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbcn_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbcp_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbcr_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbjp_niw|16|1|0|1|0|0|0|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbjp_sqrt_censored|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|otc_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|residual_gaussian_copula__bjp|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|residual_gaussian_copula__emos|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_block__bjp|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_block__emos|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_window__bjp|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_window__emos|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|decc_path_shrunk_error__bjp|15|1|1|1|0|0|0|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|decc_path_shrunk_error__emos|15|1|1|1|0|0|0|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|dotc_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|ecc_q__bjp|15|1|1|1|0|0|0|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|ecc_q__emos|15|1|1|1|0|0|0|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcn_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcp_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcr_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbjp_niw|16|1|0|1|0|0|0|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbjp_sqrt_censored|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|otc_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|residual_gaussian_copula__bjp|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|residual_gaussian_copula__emos|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_block__bjp|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_block__emos|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_window__bjp|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_window__emos|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|decc_path_shrunk_error__bjp|15|1|1|1|0|0|0|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|decc_path_shrunk_error__emos|15|1|1|1|0|0|0|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|dotc_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|ecc_q__bjp|15|1|1|1|0|0|0|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|ecc_q__emos|15|1|1|1|0|0|0|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|mbcn_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|mbcp_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|mbcr_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|mbjp_niw|16|1|0|1|0|0|0|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|mbjp_sqrt_censored|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|otc_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|residual_gaussian_copula__bjp|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|residual_gaussian_copula__emos|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|schaake_block__bjp|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|schaake_block__emos|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|schaake_window__bjp|15|1|1|0|0|1|1|0|0|0|
|3mon|["prcp:M01","t15m:M01"]|schaake_window__emos|15|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|decc_path_shrunk_error__bjp|15|1|1|1|0|0|0|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|decc_path_shrunk_error__emos|15|1|1|1|0|0|0|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|dotc_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|ecc_q__bjp|15|1|1|1|0|0|0|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|ecc_q__emos|15|1|1|1|0|0|0|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcn_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcp_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcr_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbjp_niw|16|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbjp_sqrt_censored|16|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|otc_annual|16|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|residual_gaussian_copula__bjp|15|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|residual_gaussian_copula__emos|15|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_block__bjp|15|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_block__emos|15|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_window__bjp|15|1|1|0|0|1|1|0|0|0|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_window__emos|15|1|1|0|0|1|1|0|0|0|

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
|1mon|prcp|anomaly_signal_shrink|CRPS|1|8.60004113426203|
|1mon|prcp|anomaly_signal_shrink|BRIER|1|0.5681504825767174|
|1mon|prcp|anomaly_signal_shrink|RPS|1|0.49623079409763116|
|1mon|prcp|bayesian_anomaly_ridge|CRPS|1|8.293653962714624|
|1mon|prcp|bayesian_anomaly_ridge|BRIER|1|0.5082472599832457|
|1mon|prcp|bayesian_anomaly_ridge|RPS|1|0.4895817631323275|
|1mon|prcp|bjp_logsinh_fixed|CRPS|1|7.704128918766808|
|1mon|prcp|bjp_logsinh_fixed|BRIER|1|0.453817333138286|
|1mon|prcp|bjp_logsinh_fixed|RPS|1|0.44871157399779166|
|1mon|prcp|bjp_sqrt_censored|CRPS|1|8.47966456343849|
|1mon|prcp|bjp_sqrt_censored|BRIER|1|0.5065143290826821|
|1mon|prcp|bjp_sqrt_censored|RPS|1|0.48943527438195145|
|1mon|prcp|bjp_t|CRPS|1|9.085470448120333|
|1mon|prcp|bjp_t|BRIER|1|0.5361275554976013|
|1mon|prcp|bjp_t|RPS|1|0.5224486796298846|
|1mon|prcp|bjp_ti|CRPS|1|8.685369285538235|
|1mon|prcp|bjp_ti|BRIER|1|0.5166233708624132|
|1mon|prcp|bjp_ti|RPS|1|0.5008155450234062|
|1mon|prcp|bjp_yj_fixed|CRPS|1|9.026269171756642|
|1mon|prcp|bjp_yj_fixed|BRIER|1|0.46228791633521715|
|1mon|prcp|bjp_yj_fixed|RPS|1|0.459246581825114|
|1mon|prcp|bma_component_pool|CRPS|1|8.492965191856994|
|1mon|prcp|bma_component_pool|BRIER|1|0.5865870457126925|
|1mon|prcp|bma_component_pool|RPS|1|0.5328531995255097|
|1mon|prcp|bqn_monotone|CRPS|1|12.412454529294157|
|1mon|prcp|bqn_monotone|BRIER|1|1.1294593979281147|
|1mon|prcp|bqn_monotone|RPS|1|1.1174201991668558|
|1mon|prcp|cdf_mix_cv|CRPS|1|9.364690829997453|
|1mon|prcp|cdf_mix_cv|BRIER|1|0.7184502743542309|
|1mon|prcp|cdf_mix_cv|RPS|1|0.6297250394692667|
|1mon|prcp|cdf_mix_fixed50|CRPS|1|9.364690829997453|
|1mon|prcp|cdf_mix_fixed50|BRIER|1|0.7184502743542309|
|1mon|prcp|cdf_mix_fixed50|RPS|1|0.6297250394692667|
|1mon|prcp|climatology_empirical|CRPS|1|8.255435147849468|
|1mon|prcp|climatology_empirical|BRIER|1|0.6666666666666664|
|1mon|prcp|climatology_empirical|RPS|1|0.5555555555555554|
|1mon|prcp|componentwise_boost|CRPS|1|7.5050481736920736|
|1mon|prcp|componentwise_boost|BRIER|1|0.5386050468841844|
|1mon|prcp|componentwise_boost|RPS|1|0.4155648616974584|
|1mon|prcp|csg_estimated_shift|CRPS|1|10.116260484825032|
|1mon|prcp|csg_estimated_shift|BRIER|1|0.7991167686571754|
|1mon|prcp|csg_estimated_shift|RPS|1|0.6985514150717859|
|1mon|prcp|csg_fixed_shift|CRPS|1|9.436378485579546|
|1mon|prcp|csg_fixed_shift|BRIER|1|0.7180062654973058|
|1mon|prcp|csg_fixed_shift|RPS|1|0.5953124961291887|
|1mon|prcp|detrend_emos|CRPS|1|11.645546535547314|
|1mon|prcp|detrend_emos|BRIER|1|0.9391125607008316|
|1mon|prcp|detrend_emos|RPS|1|0.7393440407094081|
|1mon|prcp|detrend_qdm|CRPS|1|10.301193868619068|
|1mon|prcp|detrend_qdm|BRIER|1|0.806122448979592|
|1mon|prcp|detrend_qdm|RPS|1|0.7602040816326532|
|1mon|prcp|detrend_qm|CRPS|1|10.626828443096453|
|1mon|prcp|detrend_qm|BRIER|1|0.9489795918367347|
|1mon|prcp|detrend_qm|RPS|1|0.8673469387755103|
|1mon|prcp|drn_small|CRPS|1|11.26281158978624|
|1mon|prcp|drn_small|BRIER|1|0.9041920729735754|
|1mon|prcp|drn_small|RPS|1|0.7515100023294419|
|1mon|prcp|emos_constant_variance|CRPS|1|8.83531419864255|
|1mon|prcp|emos_constant_variance|BRIER|1|0.5672080002111781|
|1mon|prcp|emos_constant_variance|RPS|1|0.4683130035446122|
|1mon|prcp|gamlss_ridge|CRPS|1|12.136810652069206|
|1mon|prcp|gamlss_ridge|BRIER|1|1.0083395942580848|
|1mon|prcp|gamlss_ridge|RPS|1|0.7975917209269416|
|1mon|prcp|gamma_positive|CRPS|1|10.117164252752179|
|1mon|prcp|gamma_positive|BRIER|1|0.7992161380758178|
|1mon|prcp|gamma_positive|RPS|1|0.6986861181505086|
|1mon|prcp|gev_censored_gumbel|CRPS|1|8.746818672299106|
|1mon|prcp|gev_censored_gumbel|BRIER|1|0.6070965541052451|
|1mon|prcp|gev_censored_gumbel|RPS|1|0.4789206532229824|
|1mon|prcp|gev_censored_shrunk_shape|CRPS|1|8.960500199266084|
|1mon|prcp|gev_censored_shrunk_shape|BRIER|1|0.6429512201428462|
|1mon|prcp|gev_censored_shrunk_shape|RPS|1|0.5015970761273733|
|1mon|prcp|hurdle_gamma|CRPS|1|12.989657935242418|
|1mon|prcp|hurdle_gamma|BRIER|1|1.087060298493952|
|1mon|prcp|hurdle_gamma|RPS|1|0.9233020039780717|
|1mon|prcp|hurdle_lognormal|CRPS|1|12.37610285253487|
|1mon|prcp|hurdle_lognormal|BRIER|1|1.0549101689691651|
|1mon|prcp|hurdle_lognormal|RPS|1|0.9757831317841388|
|1mon|prcp|idr_mean_order|CRPS|1|13.149762190614204|
|1mon|prcp|idr_mean_order|BRIER|1|1.056553698269168|
|1mon|prcp|idr_mean_order|RPS|1|0.7329846698602909|
|1mon|prcp|kernel_rain_hurdle_equal|CRPS|1|12.183792959109576|
|1mon|prcp|kernel_rain_hurdle_equal|BRIER|1|1.0228976948867303|
|1mon|prcp|kernel_rain_hurdle_equal|RPS|1|0.895017368649152|
|1mon|prcp|mos_unit_slope|CRPS|1|9.924911518704764|
|1mon|prcp|mos_unit_slope|BRIER|1|0.6919867221742122|
|1mon|prcp|mos_unit_slope|RPS|1|0.6079743746204037|
|1mon|prcp|ngboost_small|CRPS|1|11.566601269515102|
|1mon|prcp|ngboost_small|BRIER|1|0.9434497257343576|
|1mon|prcp|ngboost_small|RPS|1|0.7523600857187449|
|1mon|prcp|pooled_emos_cyclic|CRPS|1|9.929637075295297|
|1mon|prcp|pooled_emos_cyclic|BRIER|1|0.7305717636566164|
|1mon|prcp|pooled_emos_cyclic|RPS|1|0.6793360657480245|
|1mon|prcp|pooled_emos_ridge|CRPS|1|9.649943848384401|
|1mon|prcp|pooled_emos_ridge|BRIER|1|0.724294497288939|
|1mon|prcp|pooled_emos_ridge|RPS|1|0.6849583617730339|
|1mon|prcp|pooled_mos_ridge|CRPS|1|9.514835172961373|
|1mon|prcp|pooled_mos_ridge|BRIER|1|0.7678611762048184|
|1mon|prcp|pooled_mos_ridge|RPS|1|0.7493285444103109|
|1mon|prcp|power_gaussian_cuberoot|CRPS|1|11.572057636571126|
|1mon|prcp|power_gaussian_cuberoot|BRIER|1|0.9629267685774957|
|1mon|prcp|power_gaussian_cuberoot|RPS|1|0.7261596158860372|
|1mon|prcp|power_gaussian_sqrt|CRPS|1|10.941181612068503|
|1mon|prcp|power_gaussian_sqrt|BRIER|1|0.8703340160863462|
|1mon|prcp|power_gaussian_sqrt|RPS|1|0.6527537297404583|
|1mon|prcp|power_logistic_cuberoot|CRPS|1|11.567746605773236|
|1mon|prcp|power_logistic_cuberoot|BRIER|1|0.9955672143906285|
|1mon|prcp|power_logistic_cuberoot|RPS|1|0.7253843885188926|
|1mon|prcp|power_logistic_sqrt|CRPS|1|11.313774946588792|
|1mon|prcp|power_logistic_sqrt|BRIER|1|0.9455789072084764|
|1mon|prcp|power_logistic_sqrt|RPS|1|0.6919301889894007|
|1mon|prcp|qrf_year_forest|CRPS|1|11.22756429091062|
|1mon|prcp|qrf_year_forest|BRIER|1|0.899506278941826|
|1mon|prcp|qrf_year_forest|RPS|1|0.7185274920307934|
|1mon|prcp|tweedie_p15|CRPS|1|12.315406502043947|
|1mon|prcp|tweedie_p15|BRIER|1|1.0582479739042092|
|1mon|prcp|tweedie_p15|RPS|1|0.7635024173459757|
|1mon|prcp|tweedie_selected_p|CRPS|1|12.779736010359759|
|1mon|prcp|tweedie_selected_p|BRIER|1|1.0837409125750745|
|1mon|prcp|tweedie_selected_p|RPS|1|0.8481243888568185|
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
|1mon|t15m|anomaly_signal_shrink|CRPS|1|1.7875083476161107|
|1mon|t15m|anomaly_signal_shrink|BRIER|1|0.21951260445179005|
|1mon|t15m|anomaly_signal_shrink|RPS|1|0.12545306987488258|
|1mon|t15m|bayesian_anomaly_ridge|CRPS|1|1.7180313409004362|
|1mon|t15m|bayesian_anomaly_ridge|BRIER|1|0.33427875945635|
|1mon|t15m|bayesian_anomaly_ridge|RPS|1|0.31072277208147003|
|1mon|t15m|bjp_niw|CRPS|1|2.098861005725978|
|1mon|t15m|bjp_niw|BRIER|1|0.44005200134015754|
|1mon|t15m|bjp_niw|RPS|1|0.4166757879797336|
|1mon|t15m|bjp_t|CRPS|1|2.4948675745335938|
|1mon|t15m|bjp_t|BRIER|1|0.5353705648118391|
|1mon|t15m|bjp_t|RPS|1|0.5163582057557468|
|1mon|t15m|bjp_ti|CRPS|1|2.2270077109491018|
|1mon|t15m|bjp_ti|BRIER|1|0.47198024759361096|
|1mon|t15m|bjp_ti|RPS|1|0.4501403010970288|
|1mon|t15m|bma_component_pool|CRPS|1|0.7538477378410089|
|1mon|t15m|bma_component_pool|BRIER|1|0.017480342112953857|
|1mon|t15m|bma_component_pool|RPS|1|0.013038429700429408|
|1mon|t15m|bqn_monotone|CRPS|1|0.7893581989540664|
|1mon|t15m|bqn_monotone|BRIER|1|0.0627324247016576|
|1mon|t15m|bqn_monotone|RPS|1|0.03249957307399382|
|1mon|t15m|cdf_mix_cv|CRPS|1|0.6431704080659334|
|1mon|t15m|cdf_mix_cv|BRIER|1|0.012740756491768868|
|1mon|t15m|cdf_mix_cv|RPS|1|0.006642081422455888|
|1mon|t15m|cdf_mix_fixed50|CRPS|1|1.4899597561819653|
|1mon|t15m|cdf_mix_fixed50|BRIER|1|0.2105671734908937|
|1mon|t15m|cdf_mix_fixed50|RPS|1|0.16824905789597516|
|1mon|t15m|climatology_empirical|CRPS|1|3.034965037762418|
|1mon|t15m|climatology_empirical|BRIER|1|0.6666666666666664|
|1mon|t15m|climatology_empirical|RPS|1|0.5555555555555554|
|1mon|t15m|componentwise_boost|CRPS|1|0.8109447126950116|
|1mon|t15m|componentwise_boost|BRIER|1|0.023404521981852177|
|1mon|t15m|componentwise_boost|RPS|1|0.01646056283142404|
|1mon|t15m|detrend_emos|CRPS|1|0.6517792002457553|
|1mon|t15m|detrend_emos|BRIER|1|0.013280352643052655|
|1mon|t15m|detrend_emos|RPS|1|0.006927800961245345|
|1mon|t15m|detrend_qdm|CRPS|1|0.3297501823675385|
|1mon|t15m|detrend_qdm|BRIER|1|0.0|
|1mon|t15m|detrend_qdm|RPS|1|0.0|
|1mon|t15m|detrend_qm|CRPS|1|0.7185915834688721|
|1mon|t15m|detrend_qm|BRIER|1|0.0|
|1mon|t15m|detrend_qm|RPS|1|0.0|
|1mon|t15m|drn_small|CRPS|1|0.6807040226869625|
|1mon|t15m|drn_small|BRIER|1|0.01577135347931427|
|1mon|t15m|drn_small|RPS|1|0.008262859084440738|
|1mon|t15m|emos_constant_variance|CRPS|1|0.7536781287282655|
|1mon|t15m|emos_constant_variance|BRIER|1|0.003296897285438633|
|1mon|t15m|emos_constant_variance|RPS|1|0.0016572149823235857|
|1mon|t15m|gamlss_ridge|CRPS|1|1.716111130505851|
|1mon|t15m|gamlss_ridge|BRIER|1|0.24165608962759055|
|1mon|t15m|gamlss_ridge|RPS|1|0.15094244597409698|
|1mon|t15m|idr_mean_order|CRPS|1|0.4606271787812819|
|1mon|t15m|idr_mean_order|BRIER|1|0.0|
|1mon|t15m|idr_mean_order|RPS|1|0.0|
|1mon|t15m|joint_gaussian_plugin|CRPS|1|0.9055254998513345|
|1mon|t15m|joint_gaussian_plugin|BRIER|1|0.01965499644535406|
|1mon|t15m|joint_gaussian_plugin|RPS|1|0.010104699167099917|
|1mon|t15m|kernel_normal_equal|CRPS|1|0.7001882688567427|
|1mon|t15m|kernel_normal_equal|BRIER|1|0.004696938756672592|
|1mon|t15m|kernel_normal_equal|RPS|1|0.0023697212544390236|
|1mon|t15m|mos_unit_slope|CRPS|1|0.3949078215285348|
|1mon|t15m|mos_unit_slope|BRIER|1|0.0003419205682021181|
|1mon|t15m|mos_unit_slope|RPS|1|0.0001714914269303331|
|1mon|t15m|ngboost_small|CRPS|1|0.5146643523185853|
|1mon|t15m|ngboost_small|BRIER|1|0.011010866180842491|
|1mon|t15m|ngboost_small|RPS|1|0.005886441479602106|
|1mon|t15m|pooled_emos_cyclic|CRPS|1|0.6791517271365343|
|1mon|t15m|pooled_emos_cyclic|BRIER|1|0.009703695217709266|
|1mon|t15m|pooled_emos_cyclic|RPS|1|0.004979822797503577|
|1mon|t15m|pooled_emos_ridge|CRPS|1|0.6054075958816872|
|1mon|t15m|pooled_emos_ridge|BRIER|1|0.008948288560325948|
|1mon|t15m|pooled_emos_ridge|RPS|1|0.004620393389213328|
|1mon|t15m|pooled_mos_ridge|CRPS|1|0.6155176171621847|
|1mon|t15m|pooled_mos_ridge|BRIER|1|0.015291238295012204|
|1mon|t15m|pooled_mos_ridge|RPS|1|0.00810905617113442|
|1mon|t15m|qrf_year_forest|CRPS|1|1.0245718221783777|
|1mon|t15m|qrf_year_forest|BRIER|1|0.07704565843841468|
|1mon|t15m|qrf_year_forest|RPS|1|0.05409112133873791|
|3mon|prcp|EMOS|CRPS|1|31.143514002291543|
|3mon|prcp|EMOS|BRIER|1|1.176278918432268|
|3mon|prcp|EMOS|RPS|1|1.1035241426086548|
|3mon|prcp|QDM|CRPS|1|22.19758711792214|
|3mon|prcp|QDM|BRIER|1|0.6541950113378684|
|3mon|prcp|QDM|RPS|1|0.6179138321995463|
|3mon|prcp|QM|CRPS|1|27.59709368412048|
|3mon|prcp|QM|BRIER|1|0.626984126984127|
|3mon|prcp|QM|RPS|1|0.6264172335600907|
|3mon|prcp|RAW|CRPS|1|38.51309781223027|
|3mon|prcp|RAW|BRIER|1|1.0963718820861676|
|3mon|prcp|RAW|RPS|1|1.06859410430839|
|3mon|prcp|anomaly_mos|CRPS|1|25.661636898935722|
|3mon|prcp|anomaly_mos|BRIER|1|1.0654154657384667|
|3mon|prcp|anomaly_mos|RPS|1|0.966126289492953|
|3mon|prcp|anomaly_signal_shrink|CRPS|1|24.286141189071778|
|3mon|prcp|anomaly_signal_shrink|BRIER|1|0.9986291995673119|
|3mon|prcp|anomaly_signal_shrink|RPS|1|0.9056736686867404|
|3mon|prcp|bayesian_anomaly_ridge|CRPS|1|25.173005377402045|
|3mon|prcp|bayesian_anomaly_ridge|BRIER|1|0.5854368040106829|
|3mon|prcp|bayesian_anomaly_ridge|RPS|1|0.5627098201711733|
|3mon|prcp|bjp_logsinh_fixed|CRPS|1|19.86645102334868|
|3mon|prcp|bjp_logsinh_fixed|BRIER|1|0.6727530209941461|
|3mon|prcp|bjp_logsinh_fixed|RPS|1|0.6228806370369304|
|3mon|prcp|bjp_sqrt_censored|CRPS|1|24.27763406162303|
|3mon|prcp|bjp_sqrt_censored|BRIER|1|0.5247514471331693|
|3mon|prcp|bjp_sqrt_censored|RPS|1|0.5047493549669182|
|3mon|prcp|bjp_t|CRPS|1|47.14418126823569|
|3mon|prcp|bjp_t|BRIER|1|0.879393678837064|
|3mon|prcp|bjp_t|RPS|1|0.865522701260568|
|3mon|prcp|bjp_ti|CRPS|1|30.19299059659082|
|3mon|prcp|bjp_ti|BRIER|1|0.63966443065133|
|3mon|prcp|bjp_ti|RPS|1|0.6213560226370618|
|3mon|prcp|bjp_yj_fixed|CRPS|1|21.3093488446701|
|3mon|prcp|bjp_yj_fixed|BRIER|1|0.5916896038809534|
|3mon|prcp|bjp_yj_fixed|RPS|1|0.5591592189068366|
|3mon|prcp|bma_component_pool|CRPS|1|28.142981712186014|
|3mon|prcp|bma_component_pool|BRIER|1|1.044414339714323|
|3mon|prcp|bma_component_pool|RPS|1|0.9783341369043849|
|3mon|prcp|bqn_monotone|CRPS|1|37.04391576374521|
|3mon|prcp|bqn_monotone|BRIER|1|0.5521359368934537|
|3mon|prcp|bqn_monotone|RPS|1|0.5413638635644138|
|3mon|prcp|cdf_mix_cv|CRPS|1|31.143542568271762|
|3mon|prcp|cdf_mix_cv|BRIER|1|1.1762803035776785|
|3mon|prcp|cdf_mix_cv|RPS|1|1.103525439539832|
|3mon|prcp|cdf_mix_fixed50|CRPS|1|22.46732330535593|
|3mon|prcp|cdf_mix_fixed50|BRIER|1|0.8934002667757477|
|3mon|prcp|cdf_mix_fixed50|RPS|1|0.8024785903562941|
|3mon|prcp|climatology_empirical|CRPS|1|15.654953517025127|
|3mon|prcp|climatology_empirical|BRIER|1|0.6666666666666667|
|3mon|prcp|climatology_empirical|RPS|1|0.5555555555555558|
|3mon|prcp|componentwise_boost|CRPS|1|18.85385297458018|
|3mon|prcp|componentwise_boost|BRIER|1|0.602944385517392|
|3mon|prcp|componentwise_boost|RPS|1|0.5558454126907323|
|3mon|prcp|csg_estimated_shift|CRPS|1|20.3661701828689|
|3mon|prcp|csg_estimated_shift|BRIER|1|0.7395589962672994|
|3mon|prcp|csg_estimated_shift|RPS|1|0.674103171967511|
|3mon|prcp|csg_fixed_shift|CRPS|1|21.012619361853783|
|3mon|prcp|csg_fixed_shift|BRIER|1|0.7607596221956067|
|3mon|prcp|csg_fixed_shift|RPS|1|0.6958184609302935|
|3mon|prcp|detrend_emos|CRPS|1|47.717850631218404|
|3mon|prcp|detrend_emos|BRIER|1|1.5689419774489295|
|3mon|prcp|detrend_emos|RPS|1|1.5286460661416248|
|3mon|prcp|detrend_qdm|CRPS|1|40.005283697177646|
|3mon|prcp|detrend_qdm|BRIER|1|1.007936507936508|
|3mon|prcp|detrend_qdm|RPS|1|0.9716553287981857|
|3mon|prcp|detrend_qm|CRPS|1|42.55476262298505|
|3mon|prcp|detrend_qm|BRIER|1|0.9625850340136058|
|3mon|prcp|detrend_qm|RPS|1|0.9348072562358282|
|3mon|prcp|drn_small|CRPS|1|12.71198098520426|
|3mon|prcp|drn_small|BRIER|1|0.5465034828416458|
|3mon|prcp|drn_small|RPS|1|0.45810255648701487|
|3mon|prcp|emos_constant_variance|CRPS|1|30.25345783184901|
|3mon|prcp|emos_constant_variance|BRIER|1|1.1983693525138048|
|3mon|prcp|emos_constant_variance|RPS|1|1.1104872677801216|
|3mon|prcp|gamlss_ridge|CRPS|1|14.18535929716983|
|3mon|prcp|gamlss_ridge|BRIER|1|0.6018211264138033|
|3mon|prcp|gamlss_ridge|RPS|1|0.5136436491475619|
|3mon|prcp|gamma_positive|CRPS|1|20.366131138918913|
|3mon|prcp|gamma_positive|BRIER|1|0.7395575769473614|
|3mon|prcp|gamma_positive|RPS|1|0.6741017523651196|
|3mon|prcp|gev_censored_gumbel|CRPS|1|25.705434068609364|
|3mon|prcp|gev_censored_gumbel|BRIER|1|1.141369401036829|
|3mon|prcp|gev_censored_gumbel|RPS|1|0.9952274850209943|
|3mon|prcp|gev_censored_shrunk_shape|CRPS|1|25.64662413871234|
|3mon|prcp|gev_censored_shrunk_shape|BRIER|1|1.139902980180296|
|3mon|prcp|gev_censored_shrunk_shape|RPS|1|0.9932973534307957|
|3mon|prcp|hurdle_gamma|CRPS|1|28.20873622251266|
|3mon|prcp|hurdle_gamma|BRIER|1|1.0995809988075713|
|3mon|prcp|hurdle_gamma|RPS|1|1.0087738576025669|
|3mon|prcp|hurdle_lognormal|CRPS|1|26.87572316290376|
|3mon|prcp|hurdle_lognormal|BRIER|1|1.0916497550212338|
|3mon|prcp|hurdle_lognormal|RPS|1|0.9816573381335061|
|3mon|prcp|idr_mean_order|CRPS|1|29.321319442750728|
|3mon|prcp|idr_mean_order|BRIER|1|1.53125|
|3mon|prcp|idr_mean_order|RPS|1|1.140625|
|3mon|prcp|kernel_rain_hurdle_equal|CRPS|1|22.55092447166235|
|3mon|prcp|kernel_rain_hurdle_equal|BRIER|1|0.594711869425617|
|3mon|prcp|kernel_rain_hurdle_equal|RPS|1|0.5604642869242451|
|3mon|prcp|mos_unit_slope|CRPS|1|25.59799560377605|
|3mon|prcp|mos_unit_slope|BRIER|1|1.0586105490439226|
|3mon|prcp|mos_unit_slope|RPS|1|0.9610107566035974|
|3mon|prcp|ngboost_small|CRPS|1|20.64989466272449|
|3mon|prcp|ngboost_small|BRIER|1|0.646902948179368|
|3mon|prcp|ngboost_small|RPS|1|0.6017211306496667|
|3mon|prcp|pooled_emos_cyclic|CRPS|1|31.59643096452839|
|3mon|prcp|pooled_emos_cyclic|BRIER|1|1.2591109142762327|
|3mon|prcp|pooled_emos_cyclic|RPS|1|1.1676587012659867|
|3mon|prcp|pooled_emos_ridge|CRPS|1|30.988146110690764|
|3mon|prcp|pooled_emos_ridge|BRIER|1|1.215590463595421|
|3mon|prcp|pooled_emos_ridge|RPS|1|1.1306565176960888|
|3mon|prcp|pooled_mos_ridge|CRPS|1|29.208839587535437|
|3mon|prcp|pooled_mos_ridge|BRIER|1|0.7844393775693791|
|3mon|prcp|pooled_mos_ridge|RPS|1|0.7596386015061869|
|3mon|prcp|power_gaussian_cuberoot|CRPS|1|26.116818196655398|
|3mon|prcp|power_gaussian_cuberoot|BRIER|1|1.114619913972793|
|3mon|prcp|power_gaussian_cuberoot|RPS|1|0.9919251027597498|
|3mon|prcp|power_gaussian_sqrt|CRPS|1|27.292258226181325|
|3mon|prcp|power_gaussian_sqrt|BRIER|1|1.1435882899809635|
|3mon|prcp|power_gaussian_sqrt|RPS|1|1.0287606235655522|
|3mon|prcp|power_logistic_cuberoot|CRPS|1|26.729643916311375|
|3mon|prcp|power_logistic_cuberoot|BRIER|1|1.1457812251043484|
|3mon|prcp|power_logistic_cuberoot|RPS|1|1.0175264771571475|
|3mon|prcp|power_logistic_sqrt|CRPS|1|27.445396647398436|
|3mon|prcp|power_logistic_sqrt|BRIER|1|1.160511461151684|
|3mon|prcp|power_logistic_sqrt|RPS|1|1.0400553570969082|
|3mon|prcp|qrf_year_forest|CRPS|1|28.338802247962057|
|3mon|prcp|qrf_year_forest|BRIER|1|1.0512996263973429|
|3mon|prcp|qrf_year_forest|RPS|1|0.9404228424317462|
|3mon|prcp|tweedie_p15|CRPS|1|31.003739414116186|
|3mon|prcp|tweedie_p15|BRIER|1|1.2150337608472546|
|3mon|prcp|tweedie_p15|RPS|1|1.1205273841055028|
|3mon|prcp|tweedie_selected_p|CRPS|1|31.157784791573693|
|3mon|prcp|tweedie_selected_p|BRIER|1|1.2230014665145008|
|3mon|prcp|tweedie_selected_p|RPS|1|1.1300491706976057|
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
|3mon|t15m|anomaly_mos|CRPS|1|0.4958444635455497|
|3mon|t15m|anomaly_mos|BRIER|1|0.23480626688543782|
|3mon|t15m|anomaly_mos|RPS|1|0.15142336658130184|
|3mon|t15m|anomaly_signal_shrink|CRPS|1|0.8424040876487214|
|3mon|t15m|anomaly_signal_shrink|BRIER|1|0.41218614356118755|
|3mon|t15m|anomaly_signal_shrink|RPS|1|0.37750365147308224|
|3mon|t15m|bayesian_anomaly_ridge|CRPS|1|1.3117949552834909|
|3mon|t15m|bayesian_anomaly_ridge|BRIER|1|0.49041330515080395|
|3mon|t15m|bayesian_anomaly_ridge|RPS|1|0.4798470669328283|
|3mon|t15m|bjp_niw|CRPS|1|1.3818697123626393|
|3mon|t15m|bjp_niw|BRIER|1|0.5109825474241365|
|3mon|t15m|bjp_niw|RPS|1|0.5012073130928297|
|3mon|t15m|bjp_t|CRPS|1|1.4456749727441043|
|3mon|t15m|bjp_t|BRIER|1|0.4826964454998318|
|3mon|t15m|bjp_t|RPS|1|0.47488006114878994|
|3mon|t15m|bjp_ti|CRPS|1|1.4017854377723709|
|3mon|t15m|bjp_ti|BRIER|1|0.5009497998120087|
|3mon|t15m|bjp_ti|RPS|1|0.4919090185401341|
|3mon|t15m|bma_component_pool|CRPS|1|0.6595300315671501|
|3mon|t15m|bma_component_pool|BRIER|1|0.30473163034297784|
|3mon|t15m|bma_component_pool|RPS|1|0.2572789787962915|
|3mon|t15m|bqn_monotone|CRPS|1|1.727204124115062|
|3mon|t15m|bqn_monotone|BRIER|1|1.0389996968304733|
|3mon|t15m|bqn_monotone|RPS|1|0.9161220218232135|
|3mon|t15m|cdf_mix_cv|CRPS|1|0.7080112741713799|
|3mon|t15m|cdf_mix_cv|BRIER|1|0.3140504339477005|
|3mon|t15m|cdf_mix_cv|RPS|1|0.28223003817538567|
|3mon|t15m|cdf_mix_fixed50|CRPS|1|0.8381900107819829|
|3mon|t15m|cdf_mix_fixed50|BRIER|1|0.47223037515026717|
|3mon|t15m|cdf_mix_fixed50|RPS|1|0.4067670446393271|
|3mon|t15m|climatology_empirical|CRPS|1|1.0725647468760442|
|3mon|t15m|climatology_empirical|BRIER|1|0.6666666666666664|
|3mon|t15m|climatology_empirical|RPS|1|0.5555555555555554|
|3mon|t15m|componentwise_boost|CRPS|1|3.28500052576622|
|3mon|t15m|componentwise_boost|BRIER|1|0.016810479391623088|
|3mon|t15m|componentwise_boost|RPS|1|0.015556594042617704|
|3mon|t15m|detrend_emos|CRPS|1|0.7611155815198128|
|3mon|t15m|detrend_emos|BRIER|1|0.35492222707015103|
|3mon|t15m|detrend_emos|RPS|1|0.3216914498764262|
|3mon|t15m|detrend_qdm|CRPS|1|0.4817827472577343|
|3mon|t15m|detrend_qdm|BRIER|1|0.21882086167800463|
|3mon|t15m|detrend_qdm|RPS|1|0.1729024943310658|
|3mon|t15m|detrend_qm|CRPS|1|0.3961292798096403|
|3mon|t15m|detrend_qm|BRIER|1|0.08956916099773243|
|3mon|t15m|detrend_qm|RPS|1|0.0844671201814059|
|3mon|t15m|drn_small|CRPS|1|1.2872086097079334|
|3mon|t15m|drn_small|BRIER|1|0.759326717289597|
|3mon|t15m|drn_small|RPS|1|0.664796690967402|
|3mon|t15m|emos_constant_variance|CRPS|1|0.5687337720363829|
|3mon|t15m|emos_constant_variance|BRIER|1|0.28760830458783704|
|3mon|t15m|emos_constant_variance|RPS|1|0.18807853505569366|
|3mon|t15m|gamlss_ridge|CRPS|1|4.041302451067577|
|3mon|t15m|gamlss_ridge|BRIER|1|1.621391084880246|
|3mon|t15m|gamlss_ridge|RPS|1|1.6166551936049154|
|3mon|t15m|idr_mean_order|CRPS|1|0.48142767085224325|
|3mon|t15m|idr_mean_order|BRIER|1|0.0|
|3mon|t15m|idr_mean_order|RPS|1|0.0|
|3mon|t15m|joint_gaussian_plugin|CRPS|1|0.5650121823921588|
|3mon|t15m|joint_gaussian_plugin|BRIER|1|0.2855727902903625|
|3mon|t15m|joint_gaussian_plugin|RPS|1|0.1904513615199665|
|3mon|t15m|kernel_normal_equal|CRPS|1|0.5522508711479214|
|3mon|t15m|kernel_normal_equal|BRIER|1|0.2743164883920082|
|3mon|t15m|kernel_normal_equal|RPS|1|0.19431566408666665|
|3mon|t15m|mos_unit_slope|CRPS|1|0.39415874023304637|
|3mon|t15m|mos_unit_slope|BRIER|1|0.15982080205435784|
|3mon|t15m|mos_unit_slope|RPS|1|0.09881200699794256|
|3mon|t15m|ngboost_small|CRPS|1|0.42598581416095005|
|3mon|t15m|ngboost_small|BRIER|1|0.17564973180082066|
|3mon|t15m|ngboost_small|RPS|1|0.12364229546569051|
|3mon|t15m|pooled_emos_cyclic|CRPS|1|0.564956292581554|
|3mon|t15m|pooled_emos_cyclic|BRIER|1|0.2740122688347285|
|3mon|t15m|pooled_emos_cyclic|RPS|1|0.21334083958543254|
|3mon|t15m|pooled_emos_ridge|CRPS|1|0.5431510196934959|
|3mon|t15m|pooled_emos_ridge|BRIER|1|0.2564073004577842|
|3mon|t15m|pooled_emos_ridge|RPS|1|0.1993324828660905|
|3mon|t15m|pooled_mos_ridge|CRPS|1|0.5117762406272819|
|3mon|t15m|pooled_mos_ridge|BRIER|1|0.22101485983930186|
|3mon|t15m|pooled_mos_ridge|RPS|1|0.12390064583715887|
|3mon|t15m|qrf_year_forest|CRPS|1|0.7702163542120937|
|3mon|t15m|qrf_year_forest|BRIER|1|0.3905934192010955|
|3mon|t15m|qrf_year_forest|RPS|1|0.33669359594935216|
|1mon|prcp|elr_threshold_logit|BRIER|1|0.6039560408369076|
|1mon|prcp|elr_threshold_logit|RPS|1|0.5914466976071884|
|1mon|prcp|ordinal_logit|BRIER|1|0.8617615715302527|
|1mon|prcp|ordinal_logit|RPS|1|0.8175293508444774|
|1mon|t15m|elr_threshold_logit|BRIER|1|0.15149078081401468|
|1mon|t15m|elr_threshold_logit|RPS|1|0.1384741863118607|
|1mon|t15m|ordinal_logit|BRIER|1|0.5501205967520908|
|1mon|t15m|ordinal_logit|RPS|1|0.4656359428135283|
|3mon|prcp|elr_threshold_logit|BRIER|1|0.6158839203053518|
|3mon|prcp|elr_threshold_logit|RPS|1|0.607149987085037|
|3mon|prcp|ordinal_logit|BRIER|1|0.6606997610824477|
|3mon|prcp|ordinal_logit|RPS|1|0.5953891797191577|
|3mon|t15m|elr_threshold_logit|BRIER|1|0.20159307060158294|
|3mon|t15m|elr_threshold_logit|RPS|1|0.19799698026327253|
|3mon|t15m|ordinal_logit|BRIER|1|0.40148855343516215|
|3mon|t15m|ordinal_logit|RPS|1|0.33865870908452855|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|dotc_annual|ENERGY|1|2.843437350171811|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|dotc_annual|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|dotc_annual|VARIOGRAM|1|0.20452581076214454|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbcn_annual|ENERGY|1|4.977271021020047|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbcn_annual|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbcn_annual|VARIOGRAM|1|0.3698906473749334|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbcp_annual|ENERGY|1|4.2534510325289885|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbcp_annual|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbcp_annual|VARIOGRAM|1|0.32180654567609057|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbcr_annual|ENERGY|1|5.286618477029736|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbcr_annual|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbcr_annual|VARIOGRAM|1|0.37072738273784067|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbjp_sqrt_censored|ENERGY|1|2.8204529212479423|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbjp_sqrt_censored|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|mbjp_sqrt_censored|VARIOGRAM|1|0.23557162713053623|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|otc_annual|ENERGY|1|2.9874279677976006|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|otc_annual|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|otc_annual|VARIOGRAM|1|0.2860626179294348|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|residual_gaussian_copula__bjp|ENERGY|1|3.0430156854503014|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|residual_gaussian_copula__bjp|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|residual_gaussian_copula__bjp|VARIOGRAM|1|0.2615871417215046|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|residual_gaussian_copula__emos|ENERGY|1|2.5485121782995104|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|residual_gaussian_copula__emos|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|residual_gaussian_copula__emos|VARIOGRAM|1|0.2048287924268132|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_block__bjp|ENERGY|1|3.135045600746567|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_block__bjp|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_block__bjp|VARIOGRAM|1|0.26210654340677214|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_block__emos|ENERGY|1|2.614647845455165|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_block__emos|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_block__emos|VARIOGRAM|1|0.19854720590177632|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_window__bjp|ENERGY|1|3.135181711970545|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_window__bjp|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_window__bjp|VARIOGRAM|1|0.26221650693412013|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_window__emos|ENERGY|1|2.614647845455165|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_window__emos|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","prcp:W02","prcp:W03","prcp:W04","prcp:W05","prcp:W06","prcp:W07","prcp:W08"]|schaake_window__emos|VARIOGRAM|1|0.19854720590177632|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|dotc_annual|ENERGY|1|3.799238094743094|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|dotc_annual|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|dotc_annual|VARIOGRAM|1|0.25836813847251544|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcn_annual|ENERGY|1|4.176990587566992|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcn_annual|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcn_annual|VARIOGRAM|1|0.27673347018295663|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcp_annual|ENERGY|1|6.159649308769293|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcp_annual|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcp_annual|VARIOGRAM|1|0.41494709701798066|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcr_annual|ENERGY|1|5.65705810517211|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcr_annual|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbcr_annual|VARIOGRAM|1|0.3425194103701103|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbjp_sqrt_censored|ENERGY|1|3.627798481022582|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbjp_sqrt_censored|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|mbjp_sqrt_censored|VARIOGRAM|1|0.33591381492145217|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|otc_annual|ENERGY|1|3.0543996332280323|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|otc_annual|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|otc_annual|VARIOGRAM|1|0.21089171222395553|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|residual_gaussian_copula__bjp|ENERGY|1|4.205823836806701|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|residual_gaussian_copula__bjp|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|residual_gaussian_copula__bjp|VARIOGRAM|1|0.4597096664606587|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|residual_gaussian_copula__emos|ENERGY|1|2.922171438551632|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|residual_gaussian_copula__emos|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|residual_gaussian_copula__emos|VARIOGRAM|1|0.16796489849676435|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_block__bjp|ENERGY|1|4.400034856009123|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_block__bjp|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_block__bjp|VARIOGRAM|1|0.4326404688991193|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_block__emos|ENERGY|1|3.0065981028131494|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_block__emos|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_block__emos|VARIOGRAM|1|0.16926890809067574|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_window__bjp|ENERGY|1|4.40074155884477|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_window__bjp|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_window__bjp|VARIOGRAM|1|0.432714632440276|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_window__emos|ENERGY|1|3.0065981028131494|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_window__emos|HOT_DRY_BRIER|0|None|
|1mon|["prcp:W01","t15m:W01","prcp:W02","t15m:W02","prcp:W03","t15m:W03","prcp:W04","t15m:W04","prcp:W05","t15m:W05","prcp:W06","t15m:W06","prcp:W07","t15m:W07","prcp:W08","t15m:W08"]|schaake_window__emos|VARIOGRAM|1|0.16926890809067574|
|1mon|["prcp:W01","t15m:W01"]|dotc_annual|ENERGY|1|0.8602481483464253|
|1mon|["prcp:W01","t15m:W01"]|dotc_annual|HOT_DRY_BRIER|1|0.0|
|1mon|["prcp:W01","t15m:W01"]|dotc_annual|VARIOGRAM|1|0.04230670344748287|
|1mon|["prcp:W01","t15m:W01"]|mbcn_annual|ENERGY|1|0.3668772199655329|
|1mon|["prcp:W01","t15m:W01"]|mbcn_annual|HOT_DRY_BRIER|1|0.02040816326530612|
|1mon|["prcp:W01","t15m:W01"]|mbcn_annual|VARIOGRAM|1|0.019955659457132496|
|1mon|["prcp:W01","t15m:W01"]|mbcp_annual|ENERGY|1|1.1667312790177955|
|1mon|["prcp:W01","t15m:W01"]|mbcp_annual|HOT_DRY_BRIER|1|0.18367346938775503|
|1mon|["prcp:W01","t15m:W01"]|mbcp_annual|VARIOGRAM|1|0.2643663894033223|
|1mon|["prcp:W01","t15m:W01"]|mbcr_annual|ENERGY|1|1.1649402485217832|
|1mon|["prcp:W01","t15m:W01"]|mbcr_annual|HOT_DRY_BRIER|1|0.18367346938775503|
|1mon|["prcp:W01","t15m:W01"]|mbcr_annual|VARIOGRAM|1|0.24362942858377107|
|1mon|["prcp:W01","t15m:W01"]|mbjp_sqrt_censored|ENERGY|1|1.438041380007816|
|1mon|["prcp:W01","t15m:W01"]|mbjp_sqrt_censored|HOT_DRY_BRIER|1|0.0396881103515625|
|1mon|["prcp:W01","t15m:W01"]|mbjp_sqrt_censored|VARIOGRAM|1|0.38064675707004897|
|1mon|["prcp:W01","t15m:W01"]|otc_annual|ENERGY|1|0.5027948907025043|
|1mon|["prcp:W01","t15m:W01"]|otc_annual|HOT_DRY_BRIER|1|0.0|
|1mon|["prcp:W01","t15m:W01"]|otc_annual|VARIOGRAM|1|0.00974949905693539|
|1mon|["prcp:W01","t15m:W01"]|residual_gaussian_copula__bjp|ENERGY|1|1.4613210581587115|
|1mon|["prcp:W01","t15m:W01"]|residual_gaussian_copula__bjp|HOT_DRY_BRIER|1|0.03814697265625|
|1mon|["prcp:W01","t15m:W01"]|residual_gaussian_copula__bjp|VARIOGRAM|1|0.3769200862620345|
|1mon|["prcp:W01","t15m:W01"]|residual_gaussian_copula__emos|ENERGY|1|1.0813749728602748|
|1mon|["prcp:W01","t15m:W01"]|residual_gaussian_copula__emos|HOT_DRY_BRIER|1|0.1682281494140625|
|1mon|["prcp:W01","t15m:W01"]|residual_gaussian_copula__emos|VARIOGRAM|1|0.08803311947763355|
|1mon|["prcp:W01","t15m:W01"]|schaake_block__bjp|ENERGY|1|1.4601807300973877|
|1mon|["prcp:W01","t15m:W01"]|schaake_block__bjp|HOT_DRY_BRIER|1|0.062499999999999986|
|1mon|["prcp:W01","t15m:W01"]|schaake_block__bjp|VARIOGRAM|1|0.28932029100030965|
|1mon|["prcp:W01","t15m:W01"]|schaake_block__emos|ENERGY|1|1.0986030698517322|
|1mon|["prcp:W01","t15m:W01"]|schaake_block__emos|HOT_DRY_BRIER|1|0.17361111111111113|
|1mon|["prcp:W01","t15m:W01"]|schaake_block__emos|VARIOGRAM|1|0.10641129189946458|
|1mon|["prcp:W01","t15m:W01"]|schaake_window__bjp|ENERGY|1|1.4601807300973877|
|1mon|["prcp:W01","t15m:W01"]|schaake_window__bjp|HOT_DRY_BRIER|1|0.062499999999999986|
|1mon|["prcp:W01","t15m:W01"]|schaake_window__bjp|VARIOGRAM|1|0.28932029100030965|
|1mon|["prcp:W01","t15m:W01"]|schaake_window__emos|ENERGY|1|1.0986030698517322|
|1mon|["prcp:W01","t15m:W01"]|schaake_window__emos|HOT_DRY_BRIER|1|0.17361111111111113|
|1mon|["prcp:W01","t15m:W01"]|schaake_window__emos|VARIOGRAM|1|0.10641129189946458|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|dotc_annual|ENERGY|1|2.1948472708287365|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|dotc_annual|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|dotc_annual|VARIOGRAM|1|0.12249274336035311|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcn_annual|ENERGY|1|2.970725025373561|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcn_annual|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcn_annual|VARIOGRAM|1|0.31683042673882034|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcp_annual|ENERGY|1|2.2995465704231868|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcp_annual|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcp_annual|VARIOGRAM|1|0.41095015732910606|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcr_annual|ENERGY|1|2.243114948690102|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcr_annual|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbcr_annual|VARIOGRAM|1|0.44768454963440185|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbjp_niw|ENERGY|1|2.537893872341632|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbjp_niw|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbjp_niw|VARIOGRAM|1|0.5656643925211519|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbjp_sqrt_censored|ENERGY|1|2.546097828190433|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbjp_sqrt_censored|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|mbjp_sqrt_censored|VARIOGRAM|1|0.5698533708496002|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|otc_annual|ENERGY|1|1.6884171949372555|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|otc_annual|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|otc_annual|VARIOGRAM|1|0.11466390826475074|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|residual_gaussian_copula__bjp|ENERGY|1|2.692614637704355|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|residual_gaussian_copula__bjp|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|residual_gaussian_copula__bjp|VARIOGRAM|1|0.6030474761853071|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|residual_gaussian_copula__emos|ENERGY|1|1.431743107546354|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|residual_gaussian_copula__emos|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|residual_gaussian_copula__emos|VARIOGRAM|1|0.12773387183316512|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_block__bjp|ENERGY|1|2.7258926676162663|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_block__bjp|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_block__bjp|VARIOGRAM|1|0.5208775057854922|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_block__emos|ENERGY|1|1.4547997718456709|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_block__emos|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_block__emos|VARIOGRAM|1|0.10634535951468553|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_window__bjp|ENERGY|1|2.7258926676162663|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_window__bjp|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_window__bjp|VARIOGRAM|1|0.5208775057854922|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_window__emos|ENERGY|1|1.4547997718456709|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_window__emos|HOT_DRY_BRIER|0|None|
|1mon|["t15m:W01","t15m:W02","t15m:W03","t15m:W04","t15m:W05","t15m:W06","t15m:W07","t15m:W08"]|schaake_window__emos|VARIOGRAM|1|0.10634535951468553|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|dotc_annual|ENERGY|1|2.1235041295398513|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|dotc_annual|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|dotc_annual|VARIOGRAM|1|0.1522817598338472|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbcn_annual|ENERGY|1|4.462904331488964|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbcn_annual|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbcn_annual|VARIOGRAM|1|0.33822978324747327|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbcp_annual|ENERGY|1|3.6559587457560685|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbcp_annual|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbcp_annual|VARIOGRAM|1|0.33423460443912856|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbcr_annual|ENERGY|1|4.0250293805221435|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbcr_annual|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbcr_annual|VARIOGRAM|1|0.3626225661471984|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbjp_sqrt_censored|ENERGY|1|2.0990271960372184|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbjp_sqrt_censored|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|mbjp_sqrt_censored|VARIOGRAM|1|0.15784645905861025|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|otc_annual|ENERGY|1|2.76644999996574|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|otc_annual|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|otc_annual|VARIOGRAM|1|0.24947284716483584|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|residual_gaussian_copula__bjp|ENERGY|1|1.9932076483560883|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|residual_gaussian_copula__bjp|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|residual_gaussian_copula__bjp|VARIOGRAM|1|0.1838853043844769|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|residual_gaussian_copula__emos|ENERGY|1|2.025404184022949|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|residual_gaussian_copula__emos|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|residual_gaussian_copula__emos|VARIOGRAM|1|0.2002352167306446|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_block__bjp|ENERGY|1|2.0128887571389877|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_block__bjp|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_block__bjp|VARIOGRAM|1|0.15073896934946102|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_block__emos|ENERGY|1|2.069722043161481|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_block__emos|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_block__emos|VARIOGRAM|1|0.18964263670778378|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_window__bjp|ENERGY|1|2.0128887571389877|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_window__bjp|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_window__bjp|VARIOGRAM|1|0.15073896934946102|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_window__emos|ENERGY|1|2.069722043161481|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_window__emos|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","prcp:M02","prcp:M03","prcp:M04","prcp:M05","prcp:M06"]|schaake_window__emos|VARIOGRAM|1|0.18964263670778378|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|dotc_annual|ENERGY|1|2.0237870148752695|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|dotc_annual|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|dotc_annual|VARIOGRAM|1|0.18983550398303864|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcn_annual|ENERGY|1|2.6301400073600476|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcn_annual|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcn_annual|VARIOGRAM|1|0.24478705445854562|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcp_annual|ENERGY|1|5.539526574659876|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcp_annual|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcp_annual|VARIOGRAM|1|0.34343721125979654|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcr_annual|ENERGY|1|3.7665923003252613|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcr_annual|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbcr_annual|VARIOGRAM|1|0.3141131002560891|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbjp_sqrt_censored|ENERGY|1|3.628596861193273|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbjp_sqrt_censored|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|mbjp_sqrt_censored|VARIOGRAM|1|0.6717899877448255|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|otc_annual|ENERGY|1|3.030180263954204|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|otc_annual|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|otc_annual|VARIOGRAM|1|0.21615272161168564|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|residual_gaussian_copula__bjp|ENERGY|1|4.13102510439893|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|residual_gaussian_copula__bjp|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|residual_gaussian_copula__bjp|VARIOGRAM|1|0.9160297675763652|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|residual_gaussian_copula__emos|ENERGY|1|2.2806237393093207|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|residual_gaussian_copula__emos|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|residual_gaussian_copula__emos|VARIOGRAM|1|0.2061519972857364|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_block__bjp|ENERGY|1|4.016804833167916|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_block__bjp|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_block__bjp|VARIOGRAM|1|0.8198159014038346|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_block__emos|ENERGY|1|2.3046062230810347|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_block__emos|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_block__emos|VARIOGRAM|1|0.19574942269361928|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_window__bjp|ENERGY|1|4.016804833167916|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_window__bjp|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_window__bjp|VARIOGRAM|1|0.8198159014038346|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_window__emos|ENERGY|1|2.3046062230810347|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_window__emos|HOT_DRY_BRIER|0|None|
|3mon|["prcp:M01","t15m:M01","prcp:M02","t15m:M02","prcp:M03","t15m:M03","prcp:M04","t15m:M04","prcp:M05","t15m:M05","prcp:M06","t15m:M06"]|schaake_window__emos|VARIOGRAM|1|0.19574942269361928|
|3mon|["prcp:M01","t15m:M01"]|dotc_annual|ENERGY|1|0.837250599056476|
|3mon|["prcp:M01","t15m:M01"]|dotc_annual|HOT_DRY_BRIER|1|0.44444444444444453|
|3mon|["prcp:M01","t15m:M01"]|dotc_annual|VARIOGRAM|1|0.0017140275499409078|
|3mon|["prcp:M01","t15m:M01"]|mbcn_annual|ENERGY|1|2.118310559909834|
|3mon|["prcp:M01","t15m:M01"]|mbcn_annual|HOT_DRY_BRIER|1|1.0|
|3mon|["prcp:M01","t15m:M01"]|mbcn_annual|VARIOGRAM|1|0.18333466593817407|
|3mon|["prcp:M01","t15m:M01"]|mbcp_annual|ENERGY|1|1.4392861201718998|
|3mon|["prcp:M01","t15m:M01"]|mbcp_annual|HOT_DRY_BRIER|1|1.0|
|3mon|["prcp:M01","t15m:M01"]|mbcp_annual|VARIOGRAM|1|0.09736956712912676|
|3mon|["prcp:M01","t15m:M01"]|mbcr_annual|ENERGY|1|1.4283611626924162|
|3mon|["prcp:M01","t15m:M01"]|mbcr_annual|HOT_DRY_BRIER|1|1.0|
|3mon|["prcp:M01","t15m:M01"]|mbcr_annual|VARIOGRAM|1|0.0647558149758114|
|3mon|["prcp:M01","t15m:M01"]|mbjp_sqrt_censored|ENERGY|1|1.3435897614551227|
|3mon|["prcp:M01","t15m:M01"]|mbjp_sqrt_censored|HOT_DRY_BRIER|1|0.6538238525390625|
|3mon|["prcp:M01","t15m:M01"]|mbjp_sqrt_censored|VARIOGRAM|1|0.07896715994401388|
|3mon|["prcp:M01","t15m:M01"]|otc_annual|ENERGY|1|0.5328058103540164|
|3mon|["prcp:M01","t15m:M01"]|otc_annual|HOT_DRY_BRIER|1|0.44444444444444453|
|3mon|["prcp:M01","t15m:M01"]|otc_annual|VARIOGRAM|1|0.1805046734994268|
|3mon|["prcp:M01","t15m:M01"]|residual_gaussian_copula__bjp|ENERGY|1|1.3709720103639516|
|3mon|["prcp:M01","t15m:M01"]|residual_gaussian_copula__bjp|HOT_DRY_BRIER|1|0.6665191650390625|
|3mon|["prcp:M01","t15m:M01"]|residual_gaussian_copula__bjp|VARIOGRAM|1|0.0778540954315768|
|3mon|["prcp:M01","t15m:M01"]|residual_gaussian_copula__emos|ENERGY|1|0.9337128808949822|
|3mon|["prcp:M01","t15m:M01"]|residual_gaussian_copula__emos|HOT_DRY_BRIER|1|0.8570709228515625|
|3mon|["prcp:M01","t15m:M01"]|residual_gaussian_copula__emos|VARIOGRAM|1|0.050518100714530265|
|3mon|["prcp:M01","t15m:M01"]|schaake_block__bjp|ENERGY|1|1.407535872749535|
|3mon|["prcp:M01","t15m:M01"]|schaake_block__bjp|HOT_DRY_BRIER|1|0.765625|
|3mon|["prcp:M01","t15m:M01"]|schaake_block__bjp|VARIOGRAM|1|0.02201135556223523|
|3mon|["prcp:M01","t15m:M01"]|schaake_block__emos|ENERGY|1|0.9556914292345757|
|3mon|["prcp:M01","t15m:M01"]|schaake_block__emos|HOT_DRY_BRIER|1|0.9184027777777779|
|3mon|["prcp:M01","t15m:M01"]|schaake_block__emos|VARIOGRAM|1|0.06229551276933892|
|3mon|["prcp:M01","t15m:M01"]|schaake_window__bjp|ENERGY|1|1.407535872749535|
|3mon|["prcp:M01","t15m:M01"]|schaake_window__bjp|HOT_DRY_BRIER|1|0.765625|
|3mon|["prcp:M01","t15m:M01"]|schaake_window__bjp|VARIOGRAM|1|0.02201135556223523|
|3mon|["prcp:M01","t15m:M01"]|schaake_window__emos|ENERGY|1|0.9556914292345757|
|3mon|["prcp:M01","t15m:M01"]|schaake_window__emos|HOT_DRY_BRIER|1|0.9184027777777779|
|3mon|["prcp:M01","t15m:M01"]|schaake_window__emos|VARIOGRAM|1|0.06229551276933892|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|dotc_annual|ENERGY|1|1.208965222411599|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|dotc_annual|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|dotc_annual|VARIOGRAM|1|0.12600895935922873|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcn_annual|ENERGY|1|1.15627290185566|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcn_annual|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcn_annual|VARIOGRAM|1|0.12340846539628261|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcp_annual|ENERGY|1|1.5429431793501946|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcp_annual|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcp_annual|VARIOGRAM|1|0.21084422391671068|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcr_annual|ENERGY|1|1.2677007125940154|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcr_annual|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbcr_annual|VARIOGRAM|1|0.1803788833015119|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbjp_niw|ENERGY|1|3.034743898941435|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbjp_niw|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbjp_niw|VARIOGRAM|1|1.6661421203533109|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbjp_sqrt_censored|ENERGY|1|3.0516841164474506|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbjp_sqrt_censored|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|mbjp_sqrt_censored|VARIOGRAM|1|1.6794341724304913|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|otc_annual|ENERGY|1|1.3492365507086077|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|otc_annual|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|otc_annual|VARIOGRAM|1|0.12952879283381333|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|residual_gaussian_copula__bjp|ENERGY|1|3.4606767254084243|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|residual_gaussian_copula__bjp|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|residual_gaussian_copula__bjp|VARIOGRAM|1|1.9978857703683977|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|residual_gaussian_copula__emos|ENERGY|1|1.118964630848612|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|residual_gaussian_copula__emos|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|residual_gaussian_copula__emos|VARIOGRAM|1|0.1881669114153239|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_block__bjp|ENERGY|1|3.317219309117994|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_block__bjp|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_block__bjp|VARIOGRAM|1|1.6409645020256012|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_block__emos|ENERGY|1|1.1027748561549604|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_block__emos|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_block__emos|VARIOGRAM|1|0.15029303172080127|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_window__bjp|ENERGY|1|3.317219309117994|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_window__bjp|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_window__bjp|VARIOGRAM|1|1.6409645020256012|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_window__emos|ENERGY|1|1.1027748561549604|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_window__emos|HOT_DRY_BRIER|0|None|
|3mon|["t15m:M01","t15m:M02","t15m:M03","t15m:M04","t15m:M05","t15m:M06"]|schaake_window__emos|VARIOGRAM|1|0.15029303172080127|

## 3. 동일 성공 마스크의 비교
paired_comparison.csv는 동일 사례에서만 손실 차이를 계산한다. 음수는 첫 방법의 작은 손실을 뜻한다.
common_masks.csv에 모든 정확한 사례 ID, SHA256, 사전 지정 레지스트리 family_no 교집합을 보존한다.
저장된 공통마스크 점수 행: 25128. 빈 교집합도 숨기지 않는다.
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
|1mon|prcp|["EMOS", "anomaly_signal_shrink"]|CRPS|1|2.0356426578220965|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "anomaly_signal_shrink"]|BRIER|1|0.21258086357107175|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "anomaly_signal_shrink"]|RPS|1|0.2156452386733323|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bayesian_anomaly_ridge"]|CRPS|1|2.342029829369503|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bayesian_anomaly_ridge"]|BRIER|1|0.27248408616454345|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bayesian_anomaly_ridge"]|RPS|1|0.22229426963863597|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_logsinh_fixed"]|CRPS|1|2.9315548733173182|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_logsinh_fixed"]|BRIER|1|0.3269140130095032|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_logsinh_fixed"]|RPS|1|0.2631644587731718|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_sqrt_censored"]|CRPS|1|2.1560192286456363|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_sqrt_censored"]|BRIER|1|0.27421701706510704|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_sqrt_censored"]|RPS|1|0.222440758389012|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_t"]|CRPS|1|1.5502133439637937|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_t"]|BRIER|1|0.2446037906501879|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_t"]|RPS|1|0.18942735314107884|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_ti"]|CRPS|1|1.950314506545892|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_ti"]|BRIER|1|0.264107975285376|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_ti"]|RPS|1|0.21106048774755726|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_yj_fixed"]|CRPS|1|1.6094146203274846|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_yj_fixed"]|BRIER|1|0.318443429812572|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bjp_yj_fixed"]|RPS|1|0.25262945094584943|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bma_component_pool"]|CRPS|1|2.1427186002271323|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bma_component_pool"]|BRIER|1|0.19414430043509667|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bma_component_pool"]|RPS|1|0.17902283324545376|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bma_group_rain"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bma_group_rain"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bma_group_rain"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|prcp|["EMOS", "bqn_monotone"]|CRPS|1|-1.7767707372100308|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bqn_monotone"]|BRIER|1|-0.3487280517803255|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "bqn_monotone"]|RPS|1|-0.4055441663958923|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "cdf_mix_cv"]|CRPS|1|1.2709929620866731|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "cdf_mix_cv"]|BRIER|1|0.06228107179355824|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "cdf_mix_cv"]|RPS|1|0.08215099330169673|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "cdf_mix_fixed50"]|CRPS|1|1.2709929620866731|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "cdf_mix_fixed50"]|BRIER|1|0.06228107179355824|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "cdf_mix_fixed50"]|RPS|1|0.08215099330169673|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "climatology_empirical"]|CRPS|1|2.3802486442346584|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "climatology_empirical"]|BRIER|1|0.11406467948112275|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "climatology_empirical"]|RPS|1|0.1563204772154081|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "componentwise_boost"]|CRPS|1|3.130635618392053|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "componentwise_boost"]|BRIER|1|0.24212629926360474|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "componentwise_boost"]|RPS|1|0.2963111710735051|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "csg_estimated_shift"]|CRPS|1|0.5194233072590944|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "csg_estimated_shift"]|BRIER|1|-0.01838542250938624|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "csg_estimated_shift"]|RPS|1|0.013324617699177588|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "csg_fixed_shift"]|CRPS|1|1.1993053065045807|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "csg_fixed_shift"]|BRIER|1|0.06272508065048332|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "csg_fixed_shift"]|RPS|1|0.11656353664177477|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "detrend_emos"]|CRPS|1|-1.009862743463188|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "detrend_emos"]|BRIER|1|-0.15838121455304244|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "detrend_emos"]|RPS|1|-0.027468007938444616|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "detrend_qdm"]|CRPS|1|0.3344899234650587|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "detrend_qdm"]|BRIER|1|-0.025391102831802792|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "detrend_qdm"]|RPS|1|-0.04832804886168973|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "detrend_qm"]|CRPS|1|0.00885534898767304|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "detrend_qm"]|BRIER|1|-0.16824824568894559|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "detrend_qm"]|RPS|1|-0.15547090600454683|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "drn_small"]|CRPS|1|-0.6271277977021139|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "drn_small"]|BRIER|1|-0.12346072682578624|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "drn_small"]|RPS|1|-0.03963396955847842|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "emos_constant_variance"]|CRPS|1|1.8003695934415767|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "emos_constant_variance"]|BRIER|1|0.21352334593661104|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "emos_constant_variance"]|RPS|1|0.24356302922635126|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gamlss_ridge"]|CRPS|1|-1.5011268599850798|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gamlss_ridge"]|BRIER|1|-0.22760824811029567|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gamlss_ridge"]|RPS|1|-0.08571568815597819|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gamma_positive"]|CRPS|1|0.5185195393319475|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gamma_positive"]|BRIER|1|-0.018484791928028654|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gamma_positive"]|RPS|1|0.013189914620454823|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gev_censored_gumbel"]|CRPS|1|1.8888651197850201|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gev_censored_gumbel"]|BRIER|1|0.17363479204254406|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gev_censored_gumbel"]|RPS|1|0.23295537954798107|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|CRPS|1|1.6751835928180423|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|BRIER|1|0.13778012600494294|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|RPS|1|0.2102789566435902|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "hurdle_gamma"]|CRPS|1|-2.3539741431582915|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "hurdle_gamma"]|BRIER|1|-0.30632895234616275|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "hurdle_gamma"]|RPS|1|-0.21142597120710827|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "hurdle_lognormal"]|CRPS|1|-1.7404190604507441|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "hurdle_lognormal"]|BRIER|1|-0.27417882282137596|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "hurdle_lognormal"]|RPS|1|-0.26390709901317533|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "idr_mean_order"]|CRPS|1|-2.514078398530078|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "idr_mean_order"]|BRIER|1|-0.27582235212137873|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "idr_mean_order"]|RPS|1|-0.02110863708932742|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|CRPS|1|-1.5481091670254497|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|BRIER|1|-0.24216634873894116|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|RPS|1|-0.1831413358781886|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "mos_unit_slope"]|CRPS|1|0.7107722733793622|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "mos_unit_slope"]|BRIER|1|0.08874462397357696|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "mos_unit_slope"]|RPS|1|0.10390165815055974|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "ngboost_small"]|CRPS|1|-0.9309174774309756|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "ngboost_small"]|BRIER|1|-0.16271837958656843|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "ngboost_small"]|RPS|1|-0.04048405294778146|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "pooled_emos_cyclic"]|CRPS|1|0.7060467167888298|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "pooled_emos_cyclic"]|BRIER|1|0.050159582491172805|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "pooled_emos_cyclic"]|RPS|1|0.03253996702293893|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "pooled_emos_ridge"]|CRPS|1|0.9857399436997252|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "pooled_emos_ridge"]|BRIER|1|0.05643684885885014|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "pooled_emos_ridge"]|RPS|1|0.02691767099792952|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "pooled_mos_ridge"]|CRPS|1|1.1208486191227536|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "pooled_mos_ridge"]|BRIER|1|0.012870169942970744|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "pooled_mos_ridge"]|RPS|1|-0.037452511639347486|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_gaussian_cuberoot"]|CRPS|1|-0.9363738444869991|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_gaussian_cuberoot"]|BRIER|1|-0.18219542242970654|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_gaussian_cuberoot"]|RPS|1|-0.014283583115073717|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_gaussian_sqrt"]|CRPS|1|-0.3054978199843763|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_gaussian_sqrt"]|BRIER|1|-0.08960266993855703|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_gaussian_sqrt"]|RPS|1|0.05912230303050514|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_logistic_cuberoot"]|CRPS|1|-0.9320628136891091|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_logistic_cuberoot"]|BRIER|1|-0.2148358682428393|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_logistic_cuberoot"]|RPS|1|-0.01350835574792919|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_logistic_sqrt"]|CRPS|1|-0.6780911545046653|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_logistic_sqrt"]|BRIER|1|-0.1648475610606872|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "power_logistic_sqrt"]|RPS|1|0.019945843781562722|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "qrf_year_forest"]|CRPS|1|-0.5918804988264927|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "qrf_year_forest"]|BRIER|1|-0.11877493279403684|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "qrf_year_forest"]|RPS|1|-0.006651459259829906|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "tweedie_p15"]|CRPS|1|-1.6797227099598206|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "tweedie_p15"]|BRIER|1|-0.27751662775642005|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "tweedie_p15"]|RPS|1|-0.05162638457501223|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "tweedie_selected_p"]|CRPS|1|-2.1440522182756325|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "tweedie_selected_p"]|BRIER|1|-0.3030095664272854|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
|1mon|prcp|["EMOS", "tweedie_selected_p"]|RPS|1|-0.13624835608585506|628c948e825a2a26ea78c2cff6ce510e6e3d1500716c119084e2c83f83da8d50|
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
|1mon|t15m|["EMOS", "anomaly_signal_shrink"]|CRPS|1|-1.1443379048629094|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "anomaly_signal_shrink"]|BRIER|1|-0.20677180936792158|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "anomaly_signal_shrink"]|RPS|1|-0.11881096735268615|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|CRPS|1|-1.074860898147235|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|BRIER|1|-0.32153796437248156|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|RPS|1|-0.3040806695592736|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bjp_niw"]|CRPS|1|-1.4556905629727765|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bjp_niw"]|BRIER|1|-0.4273112062562891|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bjp_niw"]|RPS|1|-0.41003368545753716|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bjp_t"]|CRPS|1|-1.8516971317803925|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bjp_t"]|BRIER|1|-0.5226297697279706|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bjp_t"]|RPS|1|-0.5097161032335503|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bjp_ti"]|CRPS|1|-1.5838372681959005|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bjp_ti"]|BRIER|1|-0.4592394525097425|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bjp_ti"]|RPS|1|-0.44349819857483236|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bma_component_pool"]|CRPS|1|-0.11067729508780766|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bma_component_pool"]|BRIER|1|-0.004739547029085394|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bma_component_pool"]|RPS|1|-0.0063963271782329755|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bma_group_normal"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bma_group_normal"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bma_group_normal"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|1mon|t15m|["EMOS", "bqn_monotone"]|CRPS|1|-0.14618775620086522|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bqn_monotone"]|BRIER|1|-0.049991629617789135|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "bqn_monotone"]|RPS|1|-0.02585747055179739|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "cdf_mix_cv"]|CRPS|1|3.4687267835842306e-08|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "cdf_mix_cv"]|BRIER|1|3.8592099595863294e-08|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "cdf_mix_cv"]|RPS|1|2.109974054417124e-08|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "cdf_mix_fixed50"]|CRPS|1|-0.8467893134287641|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "cdf_mix_fixed50"]|BRIER|1|-0.19782637840702524|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "cdf_mix_fixed50"]|RPS|1|-0.16160695537377873|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "climatology_empirical"]|CRPS|1|-2.391794595009217|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "climatology_empirical"]|BRIER|1|-0.6539258715827979|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "climatology_empirical"]|RPS|1|-0.5489134530333589|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "componentwise_boost"]|CRPS|1|-0.16777426994181033|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "componentwise_boost"]|BRIER|1|-0.010663726897983714|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "componentwise_boost"]|RPS|1|-0.009818460309227606|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "detrend_emos"]|CRPS|1|-0.008608757492554076|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "detrend_emos"]|BRIER|1|-0.0005395575591841915|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "detrend_emos"]|RPS|1|-0.0002856984390489127|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "detrend_qdm"]|CRPS|1|0.31342026038566273|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "detrend_qdm"]|BRIER|1|0.012740795083868463|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "detrend_qdm"]|RPS|1|0.006642102522196432|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "detrend_qm"]|CRPS|1|-0.07542114071567085|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "detrend_qm"]|BRIER|1|0.012740795083868463|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "detrend_qm"]|RPS|1|0.006642102522196432|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "drn_small"]|CRPS|1|-0.037533579933761274|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "drn_small"]|BRIER|1|-0.003030558395445807|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "drn_small"]|RPS|1|-0.001620756562244306|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "emos_constant_variance"]|CRPS|1|-0.11050768597506422|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "emos_constant_variance"]|BRIER|1|0.00944389779842983|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "emos_constant_variance"]|RPS|1|0.004984887539872846|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
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
|1mon|t15m|["EMOS", "joint_gaussian_plugin"]|CRPS|1|-0.2623550570981332|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "joint_gaussian_plugin"]|BRIER|1|-0.006914201361485597|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "joint_gaussian_plugin"]|RPS|1|-0.003462596644903485|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "kernel_normal_equal"]|CRPS|1|-0.05701782610354145|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "kernel_normal_equal"]|BRIER|1|0.008043856327195871|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "kernel_normal_equal"]|RPS|1|0.004272381267757409|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "mos_unit_slope"]|CRPS|1|0.2482626212246664|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "mos_unit_slope"]|BRIER|1|0.012398874515666345|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "mos_unit_slope"]|RPS|1|0.006470611095266099|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "ngboost_small"]|CRPS|1|0.12850609043461592|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "ngboost_small"]|BRIER|1|0.001729928903025972|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "ngboost_small"]|RPS|1|0.000755661042594326|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "pooled_emos_cyclic"]|CRPS|1|-0.035981284383333034|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "pooled_emos_cyclic"]|BRIER|1|0.003037099866159198|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "pooled_emos_cyclic"]|RPS|1|0.0016622797246928552|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "pooled_emos_ridge"]|CRPS|1|0.03776284687151399|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "pooled_emos_ridge"]|BRIER|1|0.003792506523542516|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "pooled_emos_ridge"]|RPS|1|0.0020217091329831046|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "pooled_mos_ridge"]|CRPS|1|0.02765282559101656|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "pooled_mos_ridge"]|BRIER|1|-0.002550443211143741|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "pooled_mos_ridge"]|RPS|1|-0.0014669536489379884|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "qrf_year_forest"]|CRPS|1|-0.3814013794251765|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "qrf_year_forest"]|BRIER|1|-0.06430486335454622|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|1mon|t15m|["EMOS", "qrf_year_forest"]|RPS|1|-0.04744901881654148|d32ac43bdaf946e9942c2a9ee3a9c433e228413e0e3207e70dc6441f062de082|
|3mon|prcp|["EMOS", "QDM"]|CRPS|1|8.945926884369403|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "QDM"]|BRIER|1|0.5220839070943996|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "QDM"]|RPS|1|0.4856103104091085|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "QM"]|CRPS|1|3.5464203181710623|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "QM"]|BRIER|1|0.549294791448141|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "QM"]|RPS|1|0.4771069090485641|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "RAW"]|CRPS|1|-7.369583809938728|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "RAW"]|BRIER|1|0.0799070363461003|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "RAW"]|RPS|1|0.034930038300264865|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "anomaly_mos"]|CRPS|1|5.481877103355821|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "anomaly_mos"]|BRIER|1|0.11086345269380127|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "anomaly_mos"]|RPS|1|0.13739785311570185|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "anomaly_signal_shrink"]|CRPS|1|6.857372813219765|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "anomaly_signal_shrink"]|BRIER|1|0.17764971886495606|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "anomaly_signal_shrink"]|RPS|1|0.19785047392191446|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bayesian_anomaly_ridge"]|CRPS|1|5.970508624889497|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bayesian_anomaly_ridge"]|BRIER|1|0.5908421144215851|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bayesian_anomaly_ridge"]|RPS|1|0.5408143224374815|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_logsinh_fixed"]|CRPS|1|11.277062978942862|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_logsinh_fixed"]|BRIER|1|0.5035258974381218|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_logsinh_fixed"]|RPS|1|0.4806435055717244|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_sqrt_censored"]|CRPS|1|6.865879940668513|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_sqrt_censored"]|BRIER|1|0.6515274712990986|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_sqrt_censored"]|RPS|1|0.5987747876417366|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_t"]|CRPS|1|-16.00066726594415|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_t"]|BRIER|1|0.29688523959520396|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_t"]|RPS|1|0.23800144134808687|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_ti"]|CRPS|1|0.9505234057007215|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_ti"]|BRIER|1|0.5366144877809379|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_ti"]|RPS|1|0.48216811997159303|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_yj_fixed"]|CRPS|1|9.834165157621442|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_yj_fixed"]|BRIER|1|0.5845893145513146|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bjp_yj_fixed"]|RPS|1|0.5443649237018182|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bma_component_pool"]|CRPS|1|3.0005322901055287|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bma_component_pool"]|BRIER|1|0.13186457871794488|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bma_component_pool"]|RPS|1|0.12519000570426997|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bma_group_rain"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bma_group_rain"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bma_group_rain"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|prcp|["EMOS", "bqn_monotone"]|CRPS|1|-5.900401761453669|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bqn_monotone"]|BRIER|1|0.6241429815388142|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "bqn_monotone"]|RPS|1|0.562160279044241|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "cdf_mix_cv"]|CRPS|1|-2.8565980219497078e-05|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "cdf_mix_cv"]|BRIER|1|-1.3851454105928696e-06|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "cdf_mix_cv"]|RPS|1|-1.2969311771193759e-06|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "cdf_mix_fixed50"]|CRPS|1|8.676190696935613|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "cdf_mix_fixed50"]|BRIER|1|0.28287865165652026|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "cdf_mix_fixed50"]|RPS|1|0.30104555225236074|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "climatology_empirical"]|CRPS|1|15.488560485266415|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "climatology_empirical"]|BRIER|1|0.5096122517656012|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "climatology_empirical"]|RPS|1|0.547968587053099|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "componentwise_boost"]|CRPS|1|12.289661027711361|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "componentwise_boost"]|BRIER|1|0.5733345329148759|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "componentwise_boost"]|RPS|1|0.5476787299179225|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "csg_estimated_shift"]|CRPS|1|10.777343819422644|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "csg_estimated_shift"]|BRIER|1|0.4367199221649686|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "csg_estimated_shift"]|RPS|1|0.4294209706411438|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "csg_fixed_shift"]|CRPS|1|10.13089464043776|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "csg_fixed_shift"]|BRIER|1|0.4155192962366613|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "csg_fixed_shift"]|RPS|1|0.4077056816783613|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "detrend_emos"]|CRPS|1|-16.57433662892686|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "detrend_emos"]|BRIER|1|-0.39266305901666154|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "detrend_emos"]|RPS|1|-0.42512192353296996|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "detrend_qdm"]|CRPS|1|-8.861769694886103|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "detrend_qdm"]|BRIER|1|0.16834241049576004|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "detrend_qdm"]|RPS|1|0.1318688138104691|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "detrend_qm"]|CRPS|1|-11.41124862069351|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "detrend_qm"]|BRIER|1|0.2136938844186621|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "detrend_qm"]|RPS|1|0.16871688637282667|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "drn_small"]|CRPS|1|18.431533017087283|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "drn_small"]|BRIER|1|0.6297754355906221|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "drn_small"]|RPS|1|0.6454215861216399|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "emos_constant_variance"]|CRPS|1|0.8900561704425343|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "emos_constant_variance"]|BRIER|1|-0.02209043408153688|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "emos_constant_variance"]|RPS|1|-0.0069631251714668|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "gamlss_ridge"]|CRPS|1|16.958154705121714|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "gamlss_ridge"]|BRIER|1|0.5744577920184647|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "gamlss_ridge"]|RPS|1|0.589880493461093|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "gamma_positive"]|CRPS|1|10.77738286337263|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "gamma_positive"]|BRIER|1|0.4367213414849066|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "gamma_positive"]|RPS|1|0.42942239024353523|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "gev_censored_gumbel"]|CRPS|1|5.438079933682179|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "gev_censored_gumbel"]|BRIER|1|0.034909517395439016|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "gev_censored_gumbel"]|RPS|1|0.1082966575876605|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|CRPS|1|5.496889863579202|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|BRIER|1|0.03637593825197194|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "gev_censored_shrunk_shape"]|RPS|1|0.11022678917785911|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "hurdle_gamma"]|CRPS|1|2.9347777797788837|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "hurdle_gamma"]|BRIER|1|0.07669791962469663|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "hurdle_gamma"]|RPS|1|0.09475028500608795|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "hurdle_lognormal"]|CRPS|1|4.267790839387782|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "hurdle_lognormal"]|BRIER|1|0.0846291634110341|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "hurdle_lognormal"]|RPS|1|0.12186680447514875|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "idr_mean_order"]|CRPS|1|1.822194559540815|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "idr_mean_order"]|BRIER|1|-0.35497108156773205|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "idr_mean_order"]|RPS|1|-0.037100857391345166|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|CRPS|1|8.592589530629194|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|BRIER|1|0.5815670490066509|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "kernel_rain_hurdle_equal"]|RPS|1|0.5430598556844097|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "mos_unit_slope"]|CRPS|1|5.545518398515494|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "mos_unit_slope"]|BRIER|1|0.11766836938834535|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "mos_unit_slope"]|RPS|1|0.14251338600505747|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "ngboost_small"]|CRPS|1|10.493619339567054|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "ngboost_small"]|BRIER|1|0.5293759702529|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "ngboost_small"]|RPS|1|0.5018030119589881|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "pooled_emos_cyclic"]|CRPS|1|-0.4529169622368485|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "pooled_emos_cyclic"]|BRIER|1|-0.08283199584396472|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "pooled_emos_cyclic"]|RPS|1|-0.06413455865733186|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "pooled_emos_ridge"]|CRPS|1|0.15536789160077902|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "pooled_emos_ridge"]|BRIER|1|-0.03931154516315294|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "pooled_emos_ridge"]|RPS|1|-0.027132375087433935|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "pooled_mos_ridge"]|CRPS|1|1.9346744147561061|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "pooled_mos_ridge"]|BRIER|1|0.39183954086288886|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "pooled_mos_ridge"]|RPS|1|0.34388554110246794|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "power_gaussian_cuberoot"]|CRPS|1|5.026695805636145|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "power_gaussian_cuberoot"]|BRIER|1|0.06165900445947492|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "power_gaussian_cuberoot"]|RPS|1|0.11159903984890507|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "power_gaussian_sqrt"]|CRPS|1|3.851255776110218|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "power_gaussian_sqrt"]|BRIER|1|0.03269062845130444|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "power_gaussian_sqrt"]|RPS|1|0.07476351904310263|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "power_logistic_cuberoot"]|CRPS|1|4.413870085980168|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "power_logistic_cuberoot"]|BRIER|1|0.030497693327919517|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "power_logistic_cuberoot"]|RPS|1|0.08599766545150733|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "power_logistic_sqrt"]|CRPS|1|3.698117354893107|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "power_logistic_sqrt"]|BRIER|1|0.01576745728058393|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "power_logistic_sqrt"]|RPS|1|0.06346878551174662|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "qrf_year_forest"]|CRPS|1|2.8047117543294853|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "qrf_year_forest"]|BRIER|1|0.12497929203492508|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "qrf_year_forest"]|RPS|1|0.1631013001769086|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "tweedie_p15"]|CRPS|1|0.13977458817535648|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "tweedie_p15"]|BRIER|1|-0.03875484241498661|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "tweedie_p15"]|RPS|1|-0.017003241496847954|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "tweedie_selected_p"]|CRPS|1|-0.014270789282150531|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "tweedie_selected_p"]|BRIER|1|-0.04672254808223286|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|prcp|["EMOS", "tweedie_selected_p"]|RPS|1|-0.026525028088950853|8fc4ec8323116b6a8c04bccc252631bc10c86350103210550c4d059614f0573a|
|3mon|t15m|["EMOS", "QDM"]|CRPS|1|0.3102248929457968|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "QDM"]|BRIER|1|0.12017293128979084|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "QDM"]|RPS|1|0.13427092693671266|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "QM"]|CRPS|1|0.3717995311911908|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "QM"]|BRIER|1|0.25509356621042584|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "QM"]|RPS|1|0.22554076820655394|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "RAW"]|CRPS|1|-1.2564645478538554|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "RAW"]|BRIER|1|-0.9421853453542|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "RAW"]|RPS|1|-0.862894605943106|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "anomaly_mos"]|CRPS|1|0.21216701961515205|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "anomaly_mos"]|BRIER|1|0.07924421542476123|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "anomaly_mos"]|RPS|1|0.1308067440288802|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "anomaly_signal_shrink"]|CRPS|1|-0.1343926044880197|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "anomaly_signal_shrink"]|BRIER|1|-0.09813566125098849|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "anomaly_signal_shrink"]|RPS|1|-0.09527354086290019|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|CRPS|1|-0.6037834721227892|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|BRIER|1|-0.1763628228406049|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bayesian_anomaly_ridge"]|RPS|1|-0.19761695632264625|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bjp_niw"]|CRPS|1|-0.6738582292019376|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bjp_niw"]|BRIER|1|-0.19693206511393746|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bjp_niw"]|RPS|1|-0.21897720248264768|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bjp_t"]|CRPS|1|-0.7376634895834026|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bjp_t"]|BRIER|1|-0.16864596318963276|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bjp_t"]|RPS|1|-0.1926499505386079|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bjp_ti"]|CRPS|1|-0.6937739546116691|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bjp_ti"]|BRIER|1|-0.18689931750180966|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bjp_ti"]|RPS|1|-0.20967890792995203|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bma_component_pool"]|CRPS|1|0.04848145159355166|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bma_component_pool"]|BRIER|1|0.009318851967221209|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bma_component_pool"]|RPS|1|0.024951131813890526|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bma_group_normal"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bma_group_normal"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bma_group_normal"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "bqn_monotone"]|CRPS|1|-1.0191926409543601|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bqn_monotone"]|BRIER|1|-0.7249492145202743|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "bqn_monotone"]|RPS|1|-0.6338919112130315|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "cdf_mix_cv"]|CRPS|1|2.089893218482075e-07|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "cdf_mix_cv"]|BRIER|1|4.836249856143837e-08|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "cdf_mix_cv"]|RPS|1|7.243479638319172e-08|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "cdf_mix_fixed50"]|CRPS|1|-0.13017852762128113|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "cdf_mix_fixed50"]|BRIER|1|-0.15817989284006811|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "cdf_mix_fixed50"]|RPS|1|-0.12453693402914506|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "climatology_empirical"]|CRPS|1|-0.36455326371534247|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "climatology_empirical"]|BRIER|1|-0.35261618435646735|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "climatology_empirical"]|RPS|1|-0.2733254449453733|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "componentwise_boost"]|CRPS|1|-2.5769890426055184|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "componentwise_boost"]|BRIER|1|0.29724000291857594|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "componentwise_boost"]|RPS|1|0.26667351656756433|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "detrend_emos"]|CRPS|1|-0.05310409835911112|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "detrend_emos"]|BRIER|1|-0.04087174475995198|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "detrend_emos"]|RPS|1|-0.03946133926624418|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "detrend_qdm"]|CRPS|1|0.22622873590296744|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "detrend_qdm"]|BRIER|1|0.09522962063219442|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "detrend_qdm"]|RPS|1|0.10932761627911625|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "detrend_qm"]|CRPS|1|0.3118822033510614|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "detrend_qm"]|BRIER|1|0.22448132131246662|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "detrend_qm"]|RPS|1|0.19776299042877615|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "drn_small"]|CRPS|1|-0.5791971265472317|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "drn_small"]|BRIER|1|-0.44527623497939794|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "drn_small"]|RPS|1|-0.38256658035721997|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "emos_constant_variance"]|CRPS|1|0.13927771112431886|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "emos_constant_variance"]|BRIER|1|0.026442177722362015|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "emos_constant_variance"]|RPS|1|0.09415157555448839|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "finite_member_iid_signal_noise"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "finite_member_iid_signal_noise"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "finite_member_iid_signal_noise"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "finite_member_known_covariance"]|CRPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "finite_member_known_covariance"]|BRIER|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "finite_member_known_covariance"]|RPS|0|None|4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945|
|3mon|t15m|["EMOS", "gamlss_ridge"]|CRPS|1|-3.3332909679068754|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "gamlss_ridge"]|BRIER|1|-1.307340602570047|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "gamlss_ridge"]|RPS|1|-1.3344250829947333|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "idr_mean_order"]|CRPS|1|0.22658381230845848|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "idr_mean_order"]|BRIER|1|0.31405048231019905|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "idr_mean_order"]|RPS|1|0.28223011061018205|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "joint_gaussian_plugin"]|CRPS|1|0.14299930076854295|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "joint_gaussian_plugin"]|BRIER|1|0.028477692019836576|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "joint_gaussian_plugin"]|RPS|1|0.09177874909021555|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "kernel_normal_equal"]|CRPS|1|0.15576061201278035|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "kernel_normal_equal"]|BRIER|1|0.03973399391819088|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "kernel_normal_equal"]|RPS|1|0.0879144465235154|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "mos_unit_slope"]|CRPS|1|0.31385274292765536|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "mos_unit_slope"]|BRIER|1|0.15422968025584122|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "mos_unit_slope"]|RPS|1|0.18341810361223948|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "ngboost_small"]|CRPS|1|0.2820256689997517|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "ngboost_small"]|BRIER|1|0.1384007505093784|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "ngboost_small"]|RPS|1|0.15858781514449155|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "pooled_emos_cyclic"]|CRPS|1|0.14305519057914773|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "pooled_emos_cyclic"]|BRIER|1|0.04003821347547054|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "pooled_emos_cyclic"]|RPS|1|0.06888927102474951|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "pooled_emos_ridge"]|CRPS|1|0.16486046346720584|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "pooled_emos_ridge"]|BRIER|1|0.05764318185241485|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "pooled_emos_ridge"]|RPS|1|0.08289762774409154|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "pooled_mos_ridge"]|CRPS|1|0.19623524253341984|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "pooled_mos_ridge"]|BRIER|1|0.0930356224708972|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "pooled_mos_ridge"]|RPS|1|0.15832946477302318|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "qrf_year_forest"]|CRPS|1|-0.06220487105139194|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "qrf_year_forest"]|BRIER|1|-0.07654293689089647|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|
|3mon|t15m|["EMOS", "qrf_year_forest"]|RPS|1|-0.054463485339170115|7353515a446415fe8e0cffad0a482431c1f538425a8ade662a6ed07ad9c018bb|

## 4. 실패를 포함한 운용 정책과 손실 한계
failure_inclusive_policy.csv의 method+climatology_on_failure는 별도 정책이다.
실패한 원방법 상태·분포를 변경하지 않으며, 같은 외부 훈련 경험 기후값으로 실패 사례를 평가한다.
미기록 또는 미실행 상태는 성공도 실패 대체도 아니다. 정책이 불완전하면 평균은 비운다.
비음수 점수의 미평가 손실 한계는 [성공 손실 합/N, +inf]이며 유한 벌점을 만들지 않는다.
정책 행: 946; 상세 대체 출처는 failure_policy_cases.csv에 있다.

## 5. 반복 관측창·연도 민감도
동일 변수/상품/정확한 VALID_START-END 창 총 가중치 1을 발행들에 나눈다.
year_overlap_sensitivity.csv는 같은 창을 묶은 연도 블록 및 연결된 중첩창 블록 재표본화(999회),
연도별 차이와 한 연도 제외 차이를 기록한다. 실제 약 5개 검증 연도로 강한 유의성·인과 주장을 하지 않는다.

## 6. 분포·강수 사건·결합 근사
원래 해석적 주변분포 점수와 유한 시나리오 투영 주변점수는 별도 산출물이다.
결합 ENERGY/VARIOGRAM 및 실제 저장된 사건 Brier는 벡터 범위별로만 비교한다.
PIT는 F(y-)와 F(y) 사이 원자 질량을 고정 시드로 무작위화한다.
상위 강수 사건은 외부 훈련 90% 분위수 초과로 고정되며 검증 정답으로 임계값을 고르지 않는다.
원분포 진단 행: 152; 원분포가 없거나 복원 실패하면 MISSING/ERROR를 표시한다.

## 7. 완전성·근거 및 해석 한계
필수 산출물 결측: [].
report_manifest.json은 범위·시드·필수 산출물·진단 결측·마스크 정의·그림 경로를 기록한다.
모든 방법 전체 실행, 독립 검증 및 최종 수동 QA는 별도 증거가 필요하다.
유리한 일부 사례나 성공만으로 최선·우월·실험 PASS라고 주장하지 않는다.
RAW/QM/QDM/EMOS 비교도 위와 동일한 적용범위·공통마스크·실패정책 규칙을 따른다.
