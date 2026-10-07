# GloSea6 KMA-area data package

이 패키지는 GloSea6 RAW에서 ASOS 기반 보정 예측을 재현하고 정량·확률검증을
수행하기 위한 KMA 권역평균 자료다. `hcst_mapping`은 SOURCE_YEAR가 있는 현재
DQM/QM 입력이고, `hcst_legacy_probability`는 기존 RAW 확률용 분포 표본이다.
두 자료를 혼용하지 않는다.

온도는 1993–2022 HCST와 같은 기간 ASOS의 추세를 각각 제거한 뒤 Gaussian
DQM하고, HCST에는 source-year ASOS trend, FCST에는 target-year ASOS trend를
복원한다. 강수는 1993–2022 경험분포끼리 QM한다. 보정 HCST 평균은 anomaly
기준이며 보정 HCST P33/P66은 BN/NN/AN 기준이다.

`MANIFEST.csv`는 파일·행 수·SHA256을, `DATA_DICTIONARY.csv`는 열 의미를,
`cases/verification_cases.csv`는 사례별 표본 수와 완성 상태를 제공한다.
