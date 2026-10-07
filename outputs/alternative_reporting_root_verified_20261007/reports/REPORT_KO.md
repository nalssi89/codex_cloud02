# 통계 대안 공정 비교 보고서

- 실행 범위: `REPORTING_SMOKE`; 보고 상태: `INCOMPLETE`.
- 원실행 상태: `UNRECORDED`. 진행·중단·실패 실행은 완료 보고가 아니다.
- 고정 난수 시드: 20261007. 이 문서는 저장된 실제 예측만 분석한다.
- 전체 실험 완료 또는 통계적 유의성을 이 보고서만으로 주장하지 않는다.

## 1. 성능 비교에 앞선 실제 적용·성공 범위
|상품|변수/벡터|방법|계열|제공|도메인 적용|과학적 게이트|결측 정답|평가 가능|평가 성공|적합 실패|수치/점수 실패|미기록|
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|1mon|prcp|RAW|0|61|61|0|1|60|60|0|0|0|
|1mon|t15m|RAW|0|61|61|0|1|60|60|0|0|0|
|3mon|prcp|RAW|0|61|61|0|1|60|60|0|0|0|
|3mon|t15m|RAW|0|61|61|0|1|60|60|0|0|0|
|1mon|prcp|QM|0|61|61|0|1|60|60|0|0|0|
|1mon|t15m|QM|0|61|61|0|1|60|60|0|0|0|
|3mon|prcp|QM|0|61|61|0|1|60|60|0|0|0|
|3mon|t15m|QM|0|61|61|0|1|60|60|0|0|0|
|1mon|prcp|QDM|0|61|61|0|1|60|60|0|0|0|
|1mon|t15m|QDM|0|61|61|0|1|60|60|0|0|0|
|3mon|prcp|QDM|0|61|61|0|1|60|60|0|0|0|
|3mon|t15m|QDM|0|61|61|0|1|60|60|0|0|0|
|1mon|prcp|EMOS|0|61|61|0|1|60|60|0|0|0|
|1mon|t15m|EMOS|0|61|61|0|1|60|60|0|0|0|
|3mon|prcp|EMOS|0|61|61|0|1|60|60|0|0|0|
|3mon|t15m|EMOS|0|61|61|0|1|60|60|0|0|0|

## 2. 실제 원단위 및 범주·결합 점수
주간(1mon: 7일)과 월간(3mon: 개별 달), 기온(degC)과 강수(mm)는 합치지 않는다.
아래 값은 성공 사례 제한 평균이다. 서로 다른 N의 평균을 전체 우열로 해석하지 않는다.
|상품|변수/벡터|방법|점수|평가 N|평균 손실|
|---|---|---|---|---:|---:|
|1mon|prcp|EMOS|CRPS|60|6.007211247640281|
|1mon|prcp|EMOS|BRIER|60|0.7617425778254497|
|1mon|prcp|EMOS|RPS|60|0.5178811156432175|
|1mon|prcp|QDM|CRPS|60|5.978435652433718|
|1mon|prcp|QDM|BRIER|60|0.6814094387755102|
|1mon|prcp|QDM|RPS|60|0.48635204081632655|
|1mon|prcp|QM|CRPS|60|6.368309734863303|
|1mon|prcp|QM|BRIER|60|0.7272427721088435|
|1mon|prcp|QM|RPS|60|0.5141634778911565|
|1mon|prcp|RAW|CRPS|60|6.192266801090046|
|1mon|prcp|RAW|BRIER|60|0.596875|
|1mon|prcp|RAW|RPS|60|0.39488201530612244|
|1mon|t15m|EMOS|CRPS|60|1.4019190809902324|
|1mon|t15m|EMOS|BRIER|60|0.6632583391254622|
|1mon|t15m|EMOS|RPS|60|0.4732173532148586|
|1mon|t15m|QDM|CRPS|60|1.3522331553355684|
|1mon|t15m|QDM|BRIER|60|0.6363201530612245|
|1mon|t15m|QDM|RPS|60|0.4324936224489796|
|1mon|t15m|QM|CRPS|60|1.3968664694937387|
|1mon|t15m|QM|BRIER|60|0.6680272108843538|
|1mon|t15m|QM|RPS|60|0.44363307823129255|
|1mon|t15m|RAW|CRPS|60|1.7067400347783748|
|1mon|t15m|RAW|BRIER|60|0.7431122448979592|
|1mon|t15m|RAW|RPS|60|0.5657791241496599|
|3mon|prcp|EMOS|CRPS|60|18.309134269697232|
|3mon|prcp|EMOS|BRIER|60|0.6181272654237602|
|3mon|prcp|EMOS|RPS|60|0.43364342970137754|
|3mon|prcp|QDM|CRPS|60|18.816070760477086|
|3mon|prcp|QDM|BRIER|60|0.5981622794758336|
|3mon|prcp|QDM|RPS|60|0.4162874992782607|
|3mon|prcp|QM|CRPS|60|19.884068596673682|
|3mon|prcp|QM|BRIER|60|0.628940376787289|
|3mon|prcp|QM|RPS|60|0.4260985241415239|
|3mon|prcp|RAW|CRPS|60|21.034976948827754|
|3mon|prcp|RAW|BRIER|60|0.6469199856833165|
|3mon|prcp|RAW|RPS|60|0.4577557163393907|
|3mon|t15m|EMOS|CRPS|60|0.6761712399445204|
|3mon|t15m|EMOS|BRIER|60|0.5798332953778822|
|3mon|t15m|EMOS|RPS|60|0.4317983863585547|
|3mon|t15m|QDM|CRPS|60|0.6450525583159814|
|3mon|t15m|QDM|BRIER|60|0.5212351124863526|
|3mon|t15m|QDM|RPS|60|0.36785656874632566|
|3mon|t15m|QM|CRPS|60|0.6616137095817085|
|3mon|t15m|QM|BRIER|60|0.5141918553686907|
|3mon|t15m|QM|RPS|60|0.36231006773851515|
|3mon|t15m|RAW|CRPS|60|0.7897605136085978|
|3mon|t15m|RAW|BRIER|60|0.683749801521689|
|3mon|t15m|RAW|RPS|60|0.5263830370593453|

## 3. 동일 성공 마스크의 비교
paired_comparison.csv는 동일 사례에서만 손실 차이를 계산한다. 음수는 첫 방법의 작은 손실을 뜻한다.
common_masks.csv에 모든 정확한 사례 ID, SHA256, 사전 지정 레지스트리 family_no 교집합을 보존한다.
저장된 공통마스크 점수 행: 192. 빈 교집합도 숨기지 않는다.
lead/month/season/year별 결과는 각 점수 표에 있으며 범주 전용은 RPS/Brier만 산출한다.
다음은 EMOS가 포함된 동일 사례 손실 차이의 실제 수치이며 우월성·유의성 판정이 아니다.
|상품|변수|첫 방법−둘째 방법|점수|공통 N|손실 차이|마스크 SHA256|
|---|---|---|---|---:|---:|---|
|1mon|prcp|["EMOS", "QDM"]|CRPS|60|0.0287755952065627|8ed7c367efa602369bf41627a2f07bc6320034e60704ba98fe1662f8da88e683|
|1mon|prcp|["EMOS", "QDM"]|BRIER|60|0.08033313904993955|8ed7c367efa602369bf41627a2f07bc6320034e60704ba98fe1662f8da88e683|
|1mon|prcp|["EMOS", "QDM"]|RPS|60|0.031529074826890935|8ed7c367efa602369bf41627a2f07bc6320034e60704ba98fe1662f8da88e683|
|1mon|prcp|["EMOS", "QM"]|CRPS|60|-0.36109848722302207|8ed7c367efa602369bf41627a2f07bc6320034e60704ba98fe1662f8da88e683|
|1mon|prcp|["EMOS", "QM"]|BRIER|60|0.03449980571660627|8ed7c367efa602369bf41627a2f07bc6320034e60704ba98fe1662f8da88e683|
|1mon|prcp|["EMOS", "QM"]|RPS|60|0.0037176377520610204|8ed7c367efa602369bf41627a2f07bc6320034e60704ba98fe1662f8da88e683|
|1mon|prcp|["EMOS", "RAW"]|CRPS|60|-0.18505555344976532|8ed7c367efa602369bf41627a2f07bc6320034e60704ba98fe1662f8da88e683|
|1mon|prcp|["EMOS", "RAW"]|BRIER|60|0.1648675778254497|8ed7c367efa602369bf41627a2f07bc6320034e60704ba98fe1662f8da88e683|
|1mon|prcp|["EMOS", "RAW"]|RPS|60|0.12299910033709505|8ed7c367efa602369bf41627a2f07bc6320034e60704ba98fe1662f8da88e683|
|1mon|t15m|["EMOS", "QDM"]|CRPS|60|0.04968592565466401|3731a7e0b9074690ed2b5c3288c0e34706bc389a7394a620a1be7b1a4134ef13|
|1mon|t15m|["EMOS", "QDM"]|BRIER|60|0.0269381860642377|3731a7e0b9074690ed2b5c3288c0e34706bc389a7394a620a1be7b1a4134ef13|
|1mon|t15m|["EMOS", "QDM"]|RPS|60|0.040723730765878985|3731a7e0b9074690ed2b5c3288c0e34706bc389a7394a620a1be7b1a4134ef13|
|1mon|t15m|["EMOS", "QM"]|CRPS|60|0.00505261149649372|3731a7e0b9074690ed2b5c3288c0e34706bc389a7394a620a1be7b1a4134ef13|
|1mon|t15m|["EMOS", "QM"]|BRIER|60|-0.004768871758891624|3731a7e0b9074690ed2b5c3288c0e34706bc389a7394a620a1be7b1a4134ef13|
|1mon|t15m|["EMOS", "QM"]|RPS|60|0.029584274983566028|3731a7e0b9074690ed2b5c3288c0e34706bc389a7394a620a1be7b1a4134ef13|
|1mon|t15m|["EMOS", "RAW"]|CRPS|60|-0.30482095378814233|3731a7e0b9074690ed2b5c3288c0e34706bc389a7394a620a1be7b1a4134ef13|
|1mon|t15m|["EMOS", "RAW"]|BRIER|60|-0.07985390577249707|3731a7e0b9074690ed2b5c3288c0e34706bc389a7394a620a1be7b1a4134ef13|
|1mon|t15m|["EMOS", "RAW"]|RPS|60|-0.09256177093480134|3731a7e0b9074690ed2b5c3288c0e34706bc389a7394a620a1be7b1a4134ef13|
|3mon|prcp|["EMOS", "QDM"]|CRPS|60|-0.5069364907798537|c46364945989395682dbebcd4f0217b16afad9f8bae4a7f0d3580777d450247b|
|3mon|prcp|["EMOS", "QDM"]|BRIER|60|0.019964985947926617|c46364945989395682dbebcd4f0217b16afad9f8bae4a7f0d3580777d450247b|
|3mon|prcp|["EMOS", "QDM"]|RPS|60|0.01735593042311684|c46364945989395682dbebcd4f0217b16afad9f8bae4a7f0d3580777d450247b|
|3mon|prcp|["EMOS", "QM"]|CRPS|60|-1.5749343269764502|c46364945989395682dbebcd4f0217b16afad9f8bae4a7f0d3580777d450247b|
|3mon|prcp|["EMOS", "QM"]|BRIER|60|-0.010813111363528805|c46364945989395682dbebcd4f0217b16afad9f8bae4a7f0d3580777d450247b|
|3mon|prcp|["EMOS", "QM"]|RPS|60|0.007544905559853654|c46364945989395682dbebcd4f0217b16afad9f8bae4a7f0d3580777d450247b|
|3mon|prcp|["EMOS", "RAW"]|CRPS|60|-2.7258426791305226|c46364945989395682dbebcd4f0217b16afad9f8bae4a7f0d3580777d450247b|
|3mon|prcp|["EMOS", "RAW"]|BRIER|60|-0.02879272025955637|c46364945989395682dbebcd4f0217b16afad9f8bae4a7f0d3580777d450247b|
|3mon|prcp|["EMOS", "RAW"]|RPS|60|-0.02411228663801318|c46364945989395682dbebcd4f0217b16afad9f8bae4a7f0d3580777d450247b|
|3mon|t15m|["EMOS", "QDM"]|CRPS|60|0.031118681628539036|d3ab443a5936e8e72c8d8b685169d8f21f1a75704f6acf848298b37b1a3a6bc4|
|3mon|t15m|["EMOS", "QDM"]|BRIER|60|0.05859818289152963|d3ab443a5936e8e72c8d8b685169d8f21f1a75704f6acf848298b37b1a3a6bc4|
|3mon|t15m|["EMOS", "QDM"]|RPS|60|0.06394181761222906|d3ab443a5936e8e72c8d8b685169d8f21f1a75704f6acf848298b37b1a3a6bc4|
|3mon|t15m|["EMOS", "QM"]|CRPS|60|0.014557530362811932|d3ab443a5936e8e72c8d8b685169d8f21f1a75704f6acf848298b37b1a3a6bc4|
|3mon|t15m|["EMOS", "QM"]|BRIER|60|0.06564144000919148|d3ab443a5936e8e72c8d8b685169d8f21f1a75704f6acf848298b37b1a3a6bc4|
|3mon|t15m|["EMOS", "QM"]|RPS|60|0.06948831862003957|d3ab443a5936e8e72c8d8b685169d8f21f1a75704f6acf848298b37b1a3a6bc4|
|3mon|t15m|["EMOS", "RAW"]|CRPS|60|-0.11358927366407734|d3ab443a5936e8e72c8d8b685169d8f21f1a75704f6acf848298b37b1a3a6bc4|
|3mon|t15m|["EMOS", "RAW"]|BRIER|60|-0.10391650614380676|d3ab443a5936e8e72c8d8b685169d8f21f1a75704f6acf848298b37b1a3a6bc4|
|3mon|t15m|["EMOS", "RAW"]|RPS|60|-0.09458465070079058|d3ab443a5936e8e72c8d8b685169d8f21f1a75704f6acf848298b37b1a3a6bc4|

## 4. 실패를 포함한 운용 정책과 손실 한계
failure_inclusive_policy.csv의 method+climatology_on_failure는 별도 정책이다.
실패한 원방법 상태·분포를 변경하지 않으며, 같은 외부 훈련 경험 기후값으로 실패 사례를 평가한다.
미기록 또는 미실행 상태는 성공도 실패 대체도 아니다. 정책이 불완전하면 평균은 비운다.
비음수 점수의 미평가 손실 한계는 [성공 손실 합/N, +inf]이며 유한 벌점을 만들지 않는다.
정책 행: 48; 상세 대체 출처는 failure_policy_cases.csv에 있다.

## 5. 반복 관측창·연도 민감도
동일 변수/상품/정확한 VALID_START-END 창 총 가중치 1을 발행들에 나눈다.
year_overlap_sensitivity.csv는 같은 창을 묶은 연도 블록 및 연결된 중첩창 블록 재표본화(999회),
연도별 차이와 한 연도 제외 차이를 기록한다. 실제 약 5개 검증 연도로 강한 유의성·인과 주장을 하지 않는다.

## 6. 분포·강수 사건·결합 근사
원래 해석적 주변분포 점수와 유한 시나리오 투영 주변점수는 별도 산출물이다.
결합 ENERGY/VARIOGRAM 및 실제 저장된 사건 Brier는 벡터 범위별로만 비교한다.
PIT는 F(y-)와 F(y) 사이 원자 질량을 고정 시드로 무작위화한다.
상위 강수 사건은 외부 훈련 90% 분위수 초과로 고정되며 검증 정답으로 임계값을 고르지 않는다.
원분포 진단 행: 960; 원분포가 없거나 복원 실패하면 MISSING/ERROR를 표시한다.

## 7. 완전성·근거 및 해석 한계
필수 산출물 결측: ['category_predictions.csv.gz', 'joint_predictions.csv.gz', 'training_ledger.csv.gz', 'fit_ledger.csv.gz', 'fit_schedule.csv', 'fold_ancestry.csv.gz', 'distribution_specs.jsonl.gz', 'joint_scenarios.npz', 'joint_training_manifest.csv.gz', 'joint_fold_ancestry.csv.gz', 'joint_scenario_marginals.csv.gz', 'joint_analytic_marginals.csv.gz', 'joint_key_status.csv.gz', 'joint_component_manifest.csv'].
report_manifest.json은 범위·시드·필수 산출물·진단 결측·마스크 정의·그림 경로를 기록한다.
모든 방법 전체 실행, 독립 검증 및 최종 수동 QA는 별도 증거가 필요하다.
유리한 일부 사례나 성공만으로 최선·우월·실험 PASS라고 주장하지 않는다.
RAW/QM/QDM/EMOS 비교도 위와 동일한 적용범위·공통마스크·실패정책 규칙을 따른다.
