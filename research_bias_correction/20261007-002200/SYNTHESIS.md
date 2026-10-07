# GloSea6 대안 편의 보정

기온·강수량의 QM·QDM·EMOS 이후 비교 후보와 적용 조건

**결론부터:** 현재 자료에서는 **평균 기반 단변량 BJP**, **기후분포 수축·혼합**, **조건부 풀링을 이용한 분포회귀·QRF**가 다른 추론 접근의 유력한 비교 후보다. 강수에는 **Gamma/CSG 분포 확장**을 먼저 시험할 가치가 있다. 기온의 제한 MOS·상수분산 모형은 새 독립 방법이 아니라 현행 EMOS의 복잡도를 줄이는 대조군이다. **Joint Gaussian이라는 이름만으로 EMOS보다 우수하거나 기온·강수의 의존성이 보정되는 것은 아니다.** 아래 순서는 성능 순위가 아니라 현재 자료의 규모와 구현 위험을 고려한 **제안 실험 순서**다. [Source 6](#source-6) [Source 10](#source-10) [Source 27](#source-27) [Source 40](#source-40) [Source 45](#source-45)

이번 작업은 문헌·현행 자료 계약 조사다. 새 방법을 실제 GloSea6 자료에 적합하거나 점수 우열을 측정하지 않았다. 기존 생산 코드·관측·보정 결과는 변경하지 않았다. 계산 확인은 [합성 메커니즘 검증](verify-mechanisms.md)이며 실제 예측 성능 검증과 다르다.

## 1. 현재 자료에서 중요한 조건

현재 보정 타깃은 **권역 평균**이다. 이 연구에 사용할 예보·관측 보정 인터페이스는 권역 집계이며, 개별 지점·격자에 대응하는 예보와 joint 자료가 확보됐다고 가정하지 않는다. `1mon`은 주간 구간, `3mon`은 개별 달력 월이며 3개월 합계가 아니다. 기온은 구간 평균 °C, 강수는 구간 누적 mm다. 조사 중 다른 작업이 관측을 재수집해 최신 기준이 갱신됐다. 현재 보고서는 KMA API Hub의 지점·날짜 원자료에서 **유효한 실제 기여 지점의 동일 가중 평균, 변수별 최소 50지점, 보간·62/n 확대 없음**을 사용한다. QC는 측정값 유효성·기여 수에서 파생한 검사이며 KMA 원래 기기 QC가 아니다. 이전 strict62·originalQC 결과를 최신 재수집 결과와 섞지 않는다. [Project P1](#src-project-p1)

고정된 발행·목표 조건의 역사 훈련은 연도별 예보-관측 쌍으로 이루어지며 현재 적합 사례의 훈련 연도는 **24~30년**, 역사 멤버는 **3/7개**다. 멤버 수를 곱해 독립 관측 수로 세면 안 된다. 발행 멤버 수는 더 크고 가변적이며, 그 생성·의존성·교환가능성이 이 자료에서 모두 입증된 것은 아니다. 현재 배열은 원래 멤버 ID를 보정 인터페이스까지 보존하지 않는다. [Project P1](#src-project-p1) [Project P2](#src-project-p2) [Project P3](#src-project-p3)

모든 후보는 `HIST_END < INIT_DATE`, 타깃 유효 연도 제외를 유지해야 한다. 이 제한은 최종 회귀만이 아니라 변환, 추세, 기후 기준, 사전분포 설정, 풀링과 하이퍼파라미터 선택에도 적용한다. 단, 날짜 조건만으로 재예측 모델·원자료가 당시 실제로 이용 가능했음이 입증되지는 않으므로, 실시간 효능을 주장하려면 발행 당시 버전·가용성도 확인해야 한다. 과거 관측의 권역 평균·합을 그대로 보정하며 일강수 기준이나 격자별 사건 확률을 권역 집계에 바로 옮기지 않는다. [Project P1](#src-project-p1) [Project P3](#src-project-p3) [Source 10](#source-10) [Source 12](#source-12)

### 방법 목록의 구분

- **다른 추론·예측분포 구성:** Bayesian BJP, BMA·커널·CDF 혼합, hurdle, QRF·IDR, 분포회귀 boosting, 범주 회귀, 신경망.
- **현행 EMOS의 확장·제한 비교군:** CSG/Gamma/GEV 등 응답분포 변경, 변환 척도 변경, 제한 MOS·상수분산, 계수 규제·부분 풀링.
- **주변분포 보정 이후의 결합 층:** ECC·Schaake·잔차 copula. 단변량 보정의 대체물이 아니다.
- **별도 검증이 필요한 기후분포 전이 방법:** MBCp/r/n·OTC/dOTC, 추세 보존형 분포 보정. 기후기간 분포 정합과 발행 예측의 조건부 신뢰성은 다르다. [Source 5](#source-5) [Source 9](#source-9) [Source 26](#source-26) [Source 27](#source-27) [Source 45](#source-45) [Source 60](#source-60) [Source 70](#source-70)

## 2. 한눈에 보는 비교

‘우선’은 첫 비교 실험, ‘조건부’는 자료·목적 확인 뒤, ‘탐색’은 복잡도나 적용 영역의 차이가 커 후순위라는 뜻이다. 비용은 기존 인터페이스에 넣을 때의 정성적 판단이며 실행 시간 측정값이 아니다. [Source 10](#source-10) [Source 40](#source-40)

|방법|기온·강수 적용|주요 장점|주요 단점·필수 조건|현재 판단|
|---|---|---|---|---|
|Joint Gaussian / 단변량 BJP|기온 적합 후보; 강수는 변환·검열|예보-관측 관계, 모수 불확실성, 약한 신호의 기후분포 회귀|정규화·사전·역변환 꼬리; 기본형은 spread 미사용|**우선 비교**, 비용 중~높음 [Source 6](#source-6)|
|기후 CDF 혼합·수축|둘 다|소표본에서 신호 의존도를 제한, ID 불필요|진짜 신호도 약화; 혼합 가중치 과적합|**우선 대조**, 비용 낮음 [Source 65](#source-65)|
|제한 anomaly MOS·상수분산|기온 우선; 강수는 지지집합 처리|낮은 복잡도, 해석 용이|현 EMOS와 중첩; 비선형·강수 왜도 부족|**우선 대조**, 비용 낮음 [Source 40](#source-40) [Source 43](#source-43)|
|Gamma / CSG EMOS|강수|양의 왜도·분산 구조; CSG는 검열 0 질량|shift·꼬리·발생 확률 결합, 모수 불안정|**우선 분포 확장**, 비용 중 [Source 4](#source-4) [Source 27](#source-27)|
|고정 power-censor 회귀|강수|기존 검열 구조 재사용, 적은 추가 복잡도|변환 손실과 원래 mm 손실 다름, 역변환 평균 주의|**소규모 대안**, 비용 중 [Source 30](#source-30)|
|Hurdle 발생-강도|강수|발생과 양의 양을 별도로 조절|dry/wet 표본 분할·분리 현상; 실제 0 빈도 확인|**조건부**, 비용 중 [Source 29](#source-29) [Source 30](#source-30)|
|검열 GEV / Tweedie|강수|꼬리 유연성 / 0·양의 양의 일관된 분포|shape 식별·수치 비용; 소표본 외삽 불안정|**탐색**, 비용 중~높음 [Source 28](#source-28) [Source 31](#source-31)|
|BMA / 동등 가중 커널|둘 다, 강수는 0·양수 성분|혼합 형태·멀티모달 분포, 그룹별 가중|멤버별 가중의 자료 근거 부족; 꼬리·모수 수|기온 커널 **조건부**, BMA는 그룹 확인 뒤 [Source 60](#source-60) [Source 61](#source-61) [Source 64](#source-64)|
|계수 부분 풀링·cyclic smoothing|둘 다|달력·lead의 정보를 빌려 추정 분산 감소|계절·모형 drift를 섞는 편향; 종속 행 증가|**조건부 우선**, 비용 중 [Source 18](#source-18) [Source 40](#source-40)|
|추세 보정 BJP-ti / detrend 후 보정|기온 우선|모형·관측 추세 불일치 명시|추세·prior 외삽, 미래정보 누출|추세 진단 후 **조건부** [Source 3](#source-3) [Source 8](#source-8)|
|Ordinal / ELR|삼분위 확률|적은 계수로 BN/NN/AN 확률을 직접 예측|연속값·전체 CDF의 대체 아님, 희소 범주|범주 상품이면 **조건부 우선** [Source 21](#source-21) [Source 56](#source-56)|
|분포회귀 boosting / GAMLSS|둘 다|작은 비선형·계절·lead 효과와 규제|분포 가정 유지, tuning·pooling 필요|**조건부 비교**, 비용 중 [Source 48](#source-48)|
|QRF / IDR|둘 다|분포족 선택 없이 조건부 분포·0 처리|관측 범위 밖 꼬리 제한, 잎·확률순서의 표본 요구|QRF **조건부**, IDR **탐색** [Source 45](#source-45) [Source 50](#source-50)|
|DRN / BQN|둘 다, 강수 support 별도 설계|비선형 연결·공유 학습·유연한 분위수|많은 가중치·튜닝·공유 표본; 분포·0·교차 제약|**탐색**, 비용 높음 [Source 24](#source-24) [Source 51](#source-51) [Source 52](#source-52)|
|Schaake / ECC / 잔차 copula|기온-강수·여러 lead 결합|공동사건·경로·의존성 산출물|주변분포 성능 개선 아님; 정합된 템플릿 필요|공동 목표가 있을 때 **조건부** [Source 5](#source-5) [Source 26](#source-26) [Source 66](#source-66)|
|다변량 BJP / MBCn / OTC|결합 분포|교차변수 정보·비선형 분포 정합|많은 모수·고차원 표본, 기후기간→계절 전이 검증|**탐색**, 비용 높음 [Source 5](#source-5) [Source 9](#source-9) [Source 70](#source-70)|
|Bayesian finite-member signal-noise|기온부터 탐색|역사·발행 멤버 수의 정밀도 차이를 모델링|독립·동질 오차/체계 비교 가능성 미확인|**조건부 탐색**, 비용 높음 [Source 14](#source-14)|

## 3. Joint Gaussian과 BJP

### 무엇이 ‘joint’인가

기본형에서 joint는 **한 변수의 예측 앙상블 평균 X와 대응 관측 Y**의 결합분포를 뜻한다. 기온과 강수를 함께 예측하는 것은 별도 다변량 확장이다. 변환한 X·Y를 결합 정규로 두면, 고정된 모수에서 다음 조건부 식이 나온다. [Source 6](#source-6)

```text
E(Y|X=x) = μy + Σyx Σxx⁻¹ (x−μx)
Var(Y|X) = Σyy − Σyx Σxx⁻¹ Σxy
```

이 식은 Gaussian MOS 회귀와 밀접하지만, 현재 CRPS 최소화·계수 제약·앙상블 spread에 따른 분산을 가진 EMOS와 **동일한 적합 모형**이라는 뜻은 아니다. 기본 결합 정규의 조건부 잔차 분산은 고정이고, mean-only BJP는 원시 앙상블 spread 정보를 쓰지 않는다. [Source 6](#source-6) [Source 76](#source-76) [Project P3](#src-project-p3)

**BJP**(Bayesian Joint Probability)는 결합분포 모수의 사후분포에 대해 조건부 예측분포를 평균한다. 각 모수에서 정규라도 최종 사후 예측은 일반적으로 단일 정규가 아니며 자동으로 t분포가 되지도 않는다. 일부 원전은 변환 모수를 MAP로 정한 뒤 고정하므로 ‘모든 불확실성을 전파한다’고 설명하면 부정확하다. [Source 5](#source-5) [Source 6](#source-6) [Source 14](#source-14)

### 장점과 단점

- **장점:** 예보-관측의 조건부 관계를 학습한다. 짧은 자료에서 모수 불확실성을 명시하고, 예측 관계가 약하면 관측 기후분포에 가까운 예측을 낼 수 있다. 원시 멤버 ID 없이 연도별 평균-관측 쌍으로 시작할 수 있다.
- **단점:** 변환·prior·MCMC 진단이 필요하고 역변환 꼬리가 민감하다. spread를 추가하면 모수가 늘고, Bayesian이라는 이름 자체가 적절한 calibration을 보장하지 않는다.
- **현재 적용:** 우선 기온의 단변량 평균 기반 BJP를 현행 EMOS와 비교한다. 강수는 정확한 0을 잠재 변환 공간의 검열 사건으로 처리하고, 원래 단위 예측 CDF·평균·분위수를 검산해야 한다. 예측 평균을 단순히 잠재 평균의 역변환으로 계산하지 않는다. [Source 5](#source-5) [Source 6](#source-6) [Source 8](#source-8)

**기온-강수 다변량 BJP는 후순위**다. Schepen 등은 호주 System4 계절 강수·최저·최고기온 실험에서 다변량 적합의 in-sample 이점이 교차검증에서 사라지는 과적합을 관찰했다. 원전은 36개 가용 연도, LOYO 적합별 35개 쌍을 사용했다. 이것은 모든 다변량 모형이 실패한다는 정리가 아니라 현재 짧은 표본에서 공분산 복잡도를 조심하라는 직접 관련 반례다. 동일 원전의 여러 게시 경로는 독립 복제 실험이 아니다. [Source 1](#source-1) [Source 5](#source-5)

## 4. 강수의 분포·발생 모형

### Gamma·CSG 확장

현재 강수 EMOS도 `Y=max(0,Z)`인 검열 정규이므로 **이미 0의 점질량이 있다**. CSG(censored shifted gamma)의 새로운 비교 요소는 양의 강수량의 왜도와 평균·분산·shift 연결이다. 일반적인 예는 다음과 같다. [Source 4](#source-4) [Source 27](#source-27) [Project P3](#src-project-p3)

```text
G ~ Gamma(k, θ), δ ≥ 0
Y = max(0, G−δ)
P(Y=0) = F_G(δ)
F_Y(y) = F_G(y+δ), y ≥ 0
```

**장점:** 비음수·0 질량·양의 왜도를 한 분포로 구성하고 CRPS 기반 적합 경로가 있다. **단점:** 발생 확률과 양의 꼬리가 결합되어 독립 조절이 어렵고, shift와 scale을 유연하게 잡으면 연간 소표본에서 불안정하다. 특정 축약 링크나 고정 shift는 후보 설계이지 모든 CSG 구현의 동일한 정형은 아니다. [Source 4](#source-4) [Source 27](#source-27) [Source 33](#source-33)

**Positive Gamma**는 더 간결하지만 정확한 0 질량이 없다. 훈련 집계에서 0이 거의 없을 때 비교할 수 있으나, 짧은 표본에서 0을 못 봤다는 사실을 모집단 0 확률이 없다는 증명으로 쓰지 않는다. NOAA의 실험 서비스는 7/14일 누적 강수에 CSGD를 사용하므로 주간 누적이라는 시간척도 선례는 있다. 다만 미국 격자·공간/날짜 풀링 자료이지 한국 권역 월·주간의 효능 검증은 아니다. [Source 2](#source-2) [Source 27](#source-27) [Source 31](#source-31)

### Power-censor·hurdle

제곱근·세제곱근 등의 **고정 power-censor**는 기존 정규/검열 구조를 재사용하는 작은 비교군이다. 변환 공간에서 맞춘 CRPS와 원래 mm 공간 CRPS는 일반적으로 다르므로 최종 비교는 원래 단위 CDF로 수행한다. 문헌의 censored logistic 예제를 Gaussian의 실제 검증 결과로 잘못 인용하지 않는다. [Source 28](#source-28) [Source 30](#source-30)

**Hurdle**은 발생 확률과 `Y>0`일 때의 Gamma/lognormal 양을 따로 적합한다. CSG나 BMA의 동의어가 아니다. 별도 발생 효과를 설명하는 장점이 있으나 dry/wet으로 표본이 나뉘며, 전부 wet인 훈련자료에서는 무벌점 logistic 절편이 발산하는 등 식별성 문제가 생긴다. 권역의 주간·월간 합에서는 실제 true-zero/near-zero/positive 빈도를 먼저 확인해야 한다. 일강수 0.1 mm 기준을 그대로 이식하지 않는다. [Source 29](#source-29) [Source 30](#source-30) [Project P1](#src-project-p1)

### GEV·Tweedie와 꼬리

**검열 GEV**는 꼬리에 유연하지만 shape·유한 상한·수치 안정성이 소표본에서 부담이다. 누적 강수에 GEV를 쓰는 것은 조건부 분포 선택이지, 해당 누적량에 극값 정리를 바로 적용했다는 뜻은 아니다. shape를 고정·수축하는 비교부터 고려한다. [Source 28](#source-28)

**Tweedie** (`1 < p < 2`)는 compound Poisson-Gamma 형태로 0과 양의 왜도를 함께 구성한다. 양수 조건부가 단일 Gamma인 것은 아니다. 월간 유역 평균 강수의 기후분포 적합 선례가 있지만, 그것은 예보 입력에 연결된 calibration 성능 근거와 다르다. p·분산 링크 식별과 수치 CDF 비용 때문에 현재는 탐색 후보로 두는 편이 합리적이다. [Source 31](#source-31) [Source 32](#source-32)

기존 자료의 극단 강수에 관심이 있어도 자유 shape 모형을 먼저 선택하지 않는다. 훈련에 관측된 극단 수, 특정 임계값의 held-out Brier, 상위 분위수 calibration과 구간 폭을 함께 확인해야 한다. 이 보고서는 새로운 극단값 정확도를 측정하지 않았다. [Source 27](#source-27) [Source 28](#source-28) [Source 64](#source-64)

## 5. 작은 모형·수축·혼합

### 제한 MOS와 기후 수축

제한 anomaly MOS는 train-only 기후평균에 대해 `μ=μobs+β(f̄−μfcst)`와 잔차 분산을 정의한다. 현재 EMOS의 slope/spread 항을 제한하는 **중첩 대조군**이며, 단일 점예측만으로 전체 분포의 CRPS와 비교해서는 안 된다. 일정 잔차 분산과 완전한 예측 CDF를 함께 발행한다. [Source 40](#source-40) [Source 43](#source-43) [Source 44](#source-44)

기후 수축은 noisy한 신호를 기후 기준 쪽으로 당긴다. 가장 작은 실험은 기존 보정 CDF와 train-only 관측 기후 CDF를 섞는 것이다. [Source 41](#source-41) [Source 42](#source-42) [Source 65](#source-65)

```text
F(y) = λ F_cal(y) + (1−λ) F_clim(y), 0 ≤ λ ≤ 1
```

**장점:** 원 멤버 ID 없이 기온·강수에 적용하고 한 개의 제한된 가중치로 시작할 수 있다. 강수의 0 질량도 각 성분에 맞게 유지된다. **단점:** 좋은 신호를 지울 수 있으며 λ 선택 자체가 과적합될 수 있다. 평균만 섞고 성분 간 차이가 만드는 분산을 누락하면 잘못된 혼합분포가 된다. Bayesian 회귀 수축을 택하면 실제 사후 예측분포를 평가해야 하며, 고정 Gaussian EMOS에 ‘모수 불확실성이 이미 전부 포함됐다’고 쓰면 안 된다. [Source 41](#source-41) [Source 42](#source-42) [Source 65](#source-65) [합성 검증](verify-mechanisms.md)

### BMA·커널 dressing

**BMA**는 성분 예측밀도를 가중 혼합한다. 기온은 Normal 성분, 강수는 0·양의 왜도 성분이 가능하다. **장점:** 성분별 정보를 반영하고 멀티모달 예측을 만들 수 있다. **단점:** 작은 관측 표본에서 가중치·성분 모수가 불안정하고 멤버 구성이 바뀌면 대응이 어려워진다. [Source 29](#source-29) [Source 60](#source-60) [Source 61](#source-61)

현재는 array index에 멤버 고유의 skill 가중치를 붙이는 방법을 권하지 않는다. 과학적으로 확인된 생성 그룹이 있다면 그룹 안의 모수·가중치를 묶는 축약 BMA를 검토할 수 있다. 이것은 제안한 소표본 설계의 자료 gate이지 ‘BMA는 일반적으로 독립 멤버만 가능하다’는 정리는 아니다. 교환가능성과 독립성도 다르다. [Source 61](#source-61) [Project P3](#src-project-p3)

기온의 **동등 가중 Gaussian kernel dressing**은 공통 bias/slope/bandwidth로 각 유효 멤버 주변의 분포를 섞는 ID 불필요 대조군이다. raw 멀티모달 모양과 spread를 살릴 수 있지만 잘못된 raw 꼬리를 계속 물려받을 수 있다. 강수에 음수 support를 가진 일반 Gaussian kernel을 그대로 쓰지 않는다. BMA·dressing이 현행 EMOS보다 낫다는 결론은 이번 조사에 없다. [Source 62](#source-62) [Source 63](#source-63) [Source 64](#source-64)

## 6. 풀링·추세·멤버 수

### 계수 부분 풀링

현재 자료에서 적용 가능한 풀링은 **같은 변수·상품의 비교 가능한 달력 조건·lead에 걸친 계수 공유**다. 인접 달력 조건의 cyclic smoothing이나 intercept/slope/log-scale의 규제를 검토할 수 있다. 개별 지역 자료가 없으므로 지역·관측소 hierarchy를 가진 것처럼 설계하지 않는다. [Source 18](#source-18) [Source 40](#source-40) [Project P1](#src-project-p1)

**장점:** 분리 적합의 분산을 낮춘다. **단점:** 계절·lead drift를 섞어 편향을 만들며 이웃 행은 독립 연도가 아니다. 월·주간 강수량, 기온·강수를 한 응답처럼 섞지 않는다. pooled EMOS/MOS와 pooled ML을 함께 비교해야 ‘방법’의 이점과 ‘더 많은 조건을 공유한’ 효과를 구별할 수 있다. [Source 10](#source-10) [Source 18](#source-18) [Source 40](#source-40)

### 추세 보정

기온에 장기 추세 불일치가 진단되면 **BJP-ti 또는 train-only detrend-보정-retrend**를 고려한다. 현행 forecast-ensemble QDM 변형은 명시적으로 추세를 제거·복원하는 방법이 아니며 원전의 기후기간 QDM 추세 보존을 그대로 주장할 수 없다. [Source 3](#source-3) [Source 74](#source-74) [Project P2](#src-project-p2)

**장점:** 모형과 관측의 시간 의존적 차이를 다룬다. **단점:** 짧은 기록의 slope·prior·외삽이 불안정하다. 추세 논문의 LOYO는 미래자료를 포함할 수 있으므로 운영 개선의 증명이 아니다. 강수에서 detrending하면 잠재 0 검열 경계도 시간에 따라 바뀌며 단순 고정 임계값을 재사용할 수 없다. 호주 공간 pool에서 정한 prior scale을 한국 권역에 그대로 옮기지 않는다. [Source 3](#source-3) [Source 8](#source-8) [Source 10](#source-10) [Source 12](#source-12)

### Finite-member signal-noise

Bayesian signal-noise는 역사 앙상블 평균의 표본 잡음과 발행 평균의 잡음이 멤버 수에 따라 달라짐을 모형화하는 후보다. GloSea5 NAO의 원전은 직접 관련된 계절 예측 사례지만 현재 기온·강수 검증 결과는 아니다. [Source 14](#source-14)

독립·동질 멤버 오차라는 추가 가정하에서 평균 잡음의 분산이 `ση²/M`이 된다. 교환가능성이나 3/7이라는 수만으로 이 법칙은 성립하지 않는다. 멤버가 상관된 오차를 가지면 다른 분산식이 필요하며 현 EMOS에 멤버 수 비율을 곱하는 간단한 교정과 다르다. 생성 체계·lag·오차 의존성 확인 전에는 조건부 탐색으로 남긴다. [Source 11](#source-11) [Source 14](#source-14) [Project P3](#src-project-p3) [합성 검증](verify-mechanisms.md)

## 7. 비선형·범주 예측

### Ordinal·ELR

최종 상품이 BN/NN/AN 확률이면 ordered logistic 또는 ELR이 작은 비교 후보다. 공통 순서 절단점 모형은 일관된 범주 확률을 만들 수 있으며 ELR은 물리적 임계값을 입력하는 관련 접근이다. 둘은 동일 모형이 아니다. 독립 이진 회귀는 교차할 수 있고 빈 범주는 분리·불확실성을 만든다. **범주 확률 모형은 보정된 강수량·기온값이나 연속 CDF의 자동 대체물이 아니다.** 실제 주간/격주 SubX·IRI 적용 선례는 있지만 현재 한국 자료의 성능 근거는 아니다. [Source 21](#source-21) [Source 55](#source-55) [Source 56](#source-56) [Source 57](#source-57)

### 분포회귀 boosting·QRF·IDR

**분포회귀 boosting/GAMLSS:** 위치·scale의 작은 비선형·달력·lead 효과를 규제와 함께 학습한다. EMOS보다 링크가 유연해지는 장점이 있지만 선택한 분포의 support·꼬리 가정은 남는다. 큰 predictor 목록보다 작은 평균/spread/계절/lead 목록과 강한 규제부터 검토한다. componentwise boosting과 NGBoost는 다른 알고리즘이며 Normal 기본값이 강수의 0·음수 support 문제를 해결하지 않는다. [Source 48](#source-48) [Source 49](#source-49) [Source 58](#source-58)

**QRF:** 관측의 조건부 가중 경험분포로 비선형·0값을 처리하고 다양한 분위수를 출력한다. 분포족 선택이 덜 필요하지만 기본형의 꼬리는 훈련 관측 범위를 벗어나지 못한다. 많은 나무가 새 관측 연도를 만들지 않으며 잎별 서로 다른 연도의 지원을 확인해야 한다. 안전한 조건 풀링이 가능하면 비교할 수 있으므로 ‘30개 쌍이면 모든 ML이 불가능하다’고 단정하지 않는다. 다만 관측 범위 밖 극단 extrapolation이 목적이면 별도 꼬리 확장이 필요하다. [Source 45](#source-45) [Source 46](#source-46) [Source 47](#source-47) [Source 59](#source-59)

**IDR:** 지정한 확률순서 아래에서 일관된 조건부 CDF를 학습한다. 해석 가능한 비모수 대조군이지만 평균·spread 둘 다 늘면 강수가 확률적으로 커진다는 등 순서 가정을 검토해야 한다. 무튜닝이 표본 충분성을 뜻하지 않고, 원전의 일강수 적용에서는 EMOS/BMA보다 많은 훈련자료를 요구한다고 설명한다. 경험적 꼬리 한계도 있다. [Source 50](#source-50)

직접 월간 QRF 문헌은 존재하지만 탄자니아의 공간 cluster·격자·lagged predictor 기반 예측이며 현재 한 권역의 앙상블 보정과 다르다. 원전의 train/test 구분 없는 normalization 정책도 복제하지 않는다. 월간 타깃이 같다는 것만으로 데이터 규모·누출 없는 검증이 같아지지 않는다. [Source 25](#source-25)

### DRN·BQN

**DRN**은 신경망으로 선택한 예측분포의 모수를 연결한다. Gaussian DRN은 비선형 mean/scale일 뿐 Bayesian 사후분포를 자동 적분하는 것은 아니다. **BQN**은 분위수 함수를 직접 구성해 유연하지만, 원래 Bremnes 구현은 단조성을 강제하지 않았으므로 교차가 드물었다는 결과를 무교차 보장으로 설명하면 안 된다. 다항 분위수의 유계 꼬리·강수 0 원자 처리는 별도 설계가 필요하다. [Source 51](#source-51) [Source 52](#source-52) [Source 53](#source-53)

신경망의 계절·준계절 선례도 있다. 그러나 Alpine SEAS5 논문은 **1개월 lead의 일별 격자 타깃**이지 월간 권역 평균·합이 아니다. 전 지구 격주 신경망과 NOAA 주간 강수도 공간 풀링 자료를 사용한다. 현재 단일 권역의 고정 조건별 연간 표본에 그 학습 설정을 그대로 옮길 근거는 없다. 작은 pooled 모델은 조건부 실험, 큰 NN은 탐색 단계로 구분한다. [Source 2](#source-2) [Source 24](#source-24) [Source 54](#source-54)

## 8. 공동사건·예측 경로

### Schaake·ECC·잔차 copula

기온과 강수의 **고온-건조 공동확률**, 여러 주·월의 경로가 필요하면 주변분포 보정 이후 결합 층을 추가한다. 이것이 현재 단변량 CRPS를 더 좋게 만드는 방법이라는 설명은 잘못이다. [Source 5](#source-5) [Source 66](#source-66) [Source 68](#source-68)

- **Schaake shuffle:** 같은 역사 연도·정합된 달력 창의 관측 벡터 순위를 템플릿으로 재정렬한다. 원 멤버 ID는 불필요하지만 연도·유효 창이 일치한 관측 벡터는 필요하다. 구현이 단순하고 계절 비교 선례가 있으나 기후적 의존성을 쓰므로 흐름 의존적 변화나 짧은 템플릿의 잡음에 취약하다.
- **ECC:** 발행 raw 멤버의 변수·lead 간 순위를 사용한다. 해당 발행의 물리적으로 일치한 원 멤버가 필요하고 array position은 그 증거가 아니다. raw 의존성이 좋으면 저비용이나 잘못된 의존성도 보존한다.
- **잔차 Gaussian copula:** 과거의 조건부 보정 CDF/PIT에 대한 잠재 잔차 의존성을 적합한다. 무조건부 관측 상관을 넣는 것과 다르다. raw ID 없이 가능하지만 강수 0 원자는 잠재 검열 구간 또는 정당화한 randomized PIT가 필요하고, 상관 수축·꼬리·공분산 안정성을 점검해야 한다. plug-in copula는 Bayesian joint posterior와 다르다. [Source 5](#source-5) [Source 26](#source-26) [Source 66](#source-66) [Source 68](#source-68) [Source 71](#source-71)

**같은 주변 값 multiset을 순열로 바꾸는 단계만** 평균·분위수·삼분위 확률·empirical CRPS를 보존한다. 분석적 EMOS에서 유한 분위수·시나리오를 생성하는 단계는 그 분포의 근사이므로 exact analytic CRPS와 같다는 뜻이 아니다. 현재 QDM의 순위 역전 때문에 과거 index 그대로의 출력이 ECC라고 주장할 수도 없다. [Source 5](#source-5) [Project P2](#src-project-p2) [합성 검증](verify-mechanisms.md)

**dECC**는 역사 오차의 시간 상관을 이용해 여러 lead 경로의 ranking을 보강하는 후속 후보다. 원전은 시간별 풍속이며, 단일 주간·월간 scalar에는 결합할 경로 자체가 없다. 필요한 joint 목표와 멤버 정합성 없이 추가하지 않는다. [Source 67](#source-67)

### 다변량 분포 전이

MBCp/r/n은 주변분포를 넘어 Pearson/Spearman 또는 다변량 분포를 조정한다. OTC/dOTC는 분포 사이 transport를 사용한다. 비선형 의존성 보정이 장점이지만 기후기간의 분포를 맞추는 것만으로 발행 계절 예측의 조건부 calibration이 검증되지는 않는다. MBCn에는 held-out 기후 평가가 존재하므로 ‘검증이 전혀 없다’고 설명하지 않고 **현재 GloSea6 조건부 계절 효능 미확인**이라고 한정한다. [Source 9](#source-9) [Source 69](#source-69) [Source 70](#source-70)

현재라면 두 변수·동일 주/월 stratum의 작은 연구 비교부터 가능하며, random rotation·반복 수·비음수 강수·순서 보존·단위 scaling을 점검해야 한다. 역사 멤버와 관측 벡터를 독립 복제 표본으로 부풀리거나 하나의 발행 앙상블을 원전의 미래 기후기간과 자동 동일시하지 않는다. [Source 9](#source-9) [Source 70](#source-70) [Source 71](#source-71)

## 9. 권장하는 첫 실험

**최소 메뉴부터 시작하는 것을 권한다.** 아래 판단은 식별성·구현 비용 기준이며 새 방법을 모두 동시에 구현하라는 뜻이 아니다. [Source 10](#source-10) [Source 40](#source-40) [Source 65](#source-65)

|순서|먼저 비교할 것|확인할 질문|보류 조건|
|---|---|---|---|
|공통 기준|RAW·훈련 기후·현행 QM/QDM/EMOS, 제한 MOS/상수분산 또는 기후 CDF 혼합 하나|복잡도를 낮춰도 신뢰성과 점수가 유지되는가?|단순 점예측만으로 분포 점수 비교하지 않음|
|새 추론 비교|기온의 단변량 평균 기반 BJP|모수 불확실성·변환의 이점이 held-out에서 남는가?|posterior/prior/역변환 진단 전 운영 적용 금지|
|강수 분포 비교|zero 빈도 감사 후 lean Gamma 또는 CSG 하나|왜도·분산/0 확률이 현 검열 정규보다 적절한가?|support 불일치·식별성 부족이면 축약|
|공유 정보 실험|같은 변수·상품의 규제 풀링; pooled EMOS 대 작은 boosting/QRF|방법 효과와 풀링 효과가 구별되는가?|계절·lead/기간 섞기 또는 타깃 누출 금지|
|목적별 분기|범주 목적: ordinal/ELR; 공동 목적: Schaake 및 조건부 ECC/copula|최종 의사결정에 필요한 예측 객체인가?|연속값 또는 단변량 개선의 대체로 해석하지 않음|

추세 보정, finite-member model, 그룹 BMA, GEV/Tweedie, MBC/OT와 대형 NN은 해당 진단·자료 gate가 열린 뒤로 미룬다. 이는 ‘쓸 수 없다’는 판정이 아니라 현재 첫 실험 메뉴를 작게 유지하기 위한 설계 선택이다. [Source 3](#source-3) [Source 14](#source-14) [Source 28](#source-28) [Source 31](#source-31) [Source 61](#source-61)

## 10. 공정한 검증 설계

1. **예측 객체를 정의한다.** 실제 발행 앙상블은 empirical CRPS, 연속·혼합 predictive CDF는 해당 분포 CRPS로 평가한다. 시나리오 근사와 analytic CDF를 구분하고 baseline을 조용히 이산화하지 않는다. [Source 11](#source-11) [Project P3](#src-project-p3)
2. **연간 쌍을 훈련 단위로 둔다.** 평균 기반 MOS/BJP는 연도당 한 쌍이다. 멤버별 loss로 확장하면 연도 내 멤버 가중치의 합이 해당 연도의 총 가중치가 되도록 한다. 경험분포의 equal-year weighting을 모든 모형의 보편 likelihood 공식으로 이식하지 않는다. [Source 6](#source-6) [Source 14](#source-14) [Project P3](#src-project-p3)
3. **과거만 사용하는 outer 검증을 유지한다.** 타깃 연도 제외·과거 끝일 cutoff를 모든 학습 단계에 적용한다. LOYO나 이웃 연도 제외 CV는 미래 추세 정보를 쓸 수 있어 운영 검증과 별도로 표시한다. [Source 3](#source-3) [Source 8](#source-8) [Source 10](#source-10) [Source 12](#source-12)
4. **동일 사례·QC·기후 경계를 비교한다.** 새 방법의 적합 실패·대상 유지율을 별도 보고하고 성공 사례만 남겨 순위를 만들지 않는다. 강수 0 동률·삼분위 경계의 규칙을 명시한다. [Source 16](#source-16) [Project P1](#src-project-p1)
5. **중복 유효 창의 의존성을 다룬다.** 반복 발행은 실제 의사결정 사례이지만 독립 관측 반복이 아니다. all-issuance 결과와 equal-valid-window 가중 민감도를 함께 보고, paired 연도/의존성 블록과 연도별 영향을 확인한다. 약 다섯 발행 연도만으로 강한 유의성이나 견고한 CI를 주장하지 않는다. [Source 16](#source-16) [Source 17](#source-17) [Project P1](#src-project-p1)
6. **점수·신뢰성을 함께 본다.** 연속 CRPS·bias·RMSE, 삼분위 RPS/Brier·reliability, PIT(0 질량이면 해당 규칙), interval coverage/width, 사전 정의한 강수 상위 임계값을 사용한다. 공동 목적에는 단위 scaling을 훈련에서 정한 energy/variogram·joint-event Brier를 추가한다. [Source 5](#source-5) [Source 27](#source-27) [Source 56](#source-56) [Source 71](#source-71)
7. **자료 체계의 민감도를 분리한다.** 동일 최근 타깃에서 공통 역사기간과 확장기간 적합을 비교한다. APCC 공식 설명에는 KMA 구성의 해양 초기화 자료 경계가 기록되어 있지만, 현재 공급 행에 대한 정확한 매핑과 편의 변화의 원인은 미확인이다. 기간 확대의 효과를 특정 초기장 변화에 인과 귀속하지 않는다. [Source 13](#source-13) [Source 19](#source-19) [Source 20](#source-20)

fair CRPS를 공식 점수의 자동 교정으로 쓰지 않는다. 멤버 생성·의존성·평가 estimand가 점수 이론의 가정을 충족할 때만 별도 민감도로 검토하며, 교환가능성만으로 iid 보정이 정당화되지 않는다. [Source 11](#source-11) [Project P3](#src-project-p3)

## 11. 실행 경로와 남은 한계

|방법군|확인한 구현 경로|도입 전에 할 일|
|---|---|---|
|BJP|CSIRO R 패키지 메타데이터|API·license·posterior/검열 규약 실제 확인 [Source 39](#source-39)|
|CSG·검열 회귀|R ensembleMOS / crch; Python scoringrules CRPS 후보|shift 부호·원래 단위 점수·M=1/spread=0 처리 검증 [Source 30](#source-30) [Source 33](#source-33) [Source 34](#source-34)|
|BMA|R ensembleBMA|그룹 metadata와 변하는 멤버 수 정책, rain 성분 확인 [Source 61](#source-61)|
|QRF·boosting|quantile-forest; gamboostLSS/crch; 별도 NGBoost|지원 response family와 train-only tuning/pooling 확인 [Source 45](#source-45) [Source 48](#source-48) [Source 58](#source-58)|
|IDR·DRN/BQN|저자 공개 구현|확률순서·0·꼬리·비교 대상·학습 규모 확인 [Source 50](#source-50) [Source 51](#source-51) [Source 52](#source-52)|
|Schaake·MBCn/OT|nmc_met_base; R MBC; SBCK|정합 배열, GPL/native build, 시간·계절 conditioning 확인 [Source 9](#source-9) [Source 68](#source-68) [Source 70](#source-70)|

패키지·소스 존재는 실행 성공·정확한 API·현재 환경 호환성의 증거가 아니다. 후보 패키지를 설치·적합하여 검증한 것으로 보고하지 않는다. SHA를 고정한 README·Schaake 코드 근거와 추가 구현 URL은 [출처 장부](sources-ledger.md), [의존성·혼합 dossier](wave-2-dependence-mixtures.md), [학습 dossier](wave-2-learning.md)에 있다.

**남은 질문:** 실제 훈련 창의 0 빈도, source-year·변수·lead의 정합, 원 멤버 생성/ID, 기존 초기일 가중 처리, 풀링 조건의 유사성, prior·공분산 식별성, 새 방법의 held-out 점수다. 이것들은 문헌 이름을 추가하는 것보다 다음 실험의 품질에 중요하다. 해당 자료가 없다고 평균 기반 BJP나 관측 Schaake까지 불가능하다고 확대하지 않는다. [Source 5](#source-5) [Source 14](#source-14) [Source 19](#source-19) [Source 61](#source-61) [Source 68](#source-68)

틀린 출처 정체성·접근 실패도 보존했다. Famien CDF-t/Africa 페이지를 Cannon MBCn으로 인용하지 않았고, HESS 404·무관한 mixture DOI는 근거에서 제외했다. ECC 출판사 화면은 challenge였으므로 본문 접근을 주장하지 않았으며 저자 원문 경로를 별도로 사용했다. [Source 9](#source-9) [Source 66](#source-66) [조사 일지](journal.md)

## 12. 참고문헌·조사 방법

핵심부터 읽으려면: BJP 원리 **[Source 6](#source-6)**, 계절 다변량 반례 **[Source 5](#source-5)**, 강수 CSG **[Source 4](#source-4)/[Source 27](#source-27)**, 주간 적용 선례 **[Source 2](#source-2)**, 소표본·풀링 **[Source 10](#source-10)/[Source 40](#source-40)**, QRF **[Source 45](#source-45)**, ECC **[Source 66](#source-66)** 순서가 좋다.

전체 번호별 URL·접근 수준·관측일은 아래 참고목록과 [출처 장부](sources-ledger.md)에 있다. 원문 방법·실험 설정, 기관 메타데이터, 소프트웨어 문서는 서로 다른 근거 층이다. 서로 다른 domain 수나 조사자의 일치가 동일 논문을 독립 효능 복제로 만들지는 않는다.

조사는 방법군별 담당, 독립 문헌·코드·브라우징 레인, 두 단계의 리드 확장과 수집 팀의 반론, 새 정제 팀의 판정으로 수행했다. 주장-관측-출처 연결은 [claim graph](claim-graph.md), [관측 manifest](observation-manifest.md), [반론 기록](debate-log.md)에 남겼다. 자료 계약과 미확인 원인은 명시했으며 생산 결함을 수정했다는 주장은 없다.

고정 Gaussian 조건부 식, 강수 0의 log 문제, 재정렬의 주변 CRPS 불변성, 혼합분산·상관 멤버의 반례를 합성 입력으로 실행했다. 이 검증은 계산 메커니즘만 증명하며 후보 적합·한국 효능을 증명하지 않는다. 최종 산출물의 정적·레이아웃·화면·한국어 교정과 정리 상태는 `outcome.json`, `qa-verdict.md`에 별도로 기록한다. [합성 검증](verify-mechanisms.md)

### 프로젝트 근거

- <span id="src-project-p1"></span>**P1:** `outputs/REPORT_KO.md:5-21,126,155-173,404-406`: 조사 중 갱신된 KMA API Hub 관측·타깃 단위·훈련 계약과 모델 가용성 한계. 최신 수집 시각 2026-10-06T23:42:09.597Z. `outputs/run_summary.json`의 현행 관측 출처도 대조했다.
- <span id="src-project-p2"></span>**P2:** `outputs/method_review/REVIEW_KO.md:79-158`: 이전 originalQC 감사의 QDM 해석과 표본·멤버 수 방법론 한계. 최신 재수집 점수의 독립 재감사라고 해석하지 않는다.
- <span id="src-project-p3"></span>**P3:** `analysis/calibration.py:132-246`, `analysis/run_verification.py:90-164`, `analysis/audit_scoring_sensitivity.py:95-101`: 보정 인터페이스·시간 제외·sampling 가정.

### 번호별 전체 출처

접근 기준일: 2026-10-06 UTC. 공개 기록/초록만 확인한 항목과 unexecuted software는 각 행과 dossier에 표시한다. 아래 목록은 URL 수이며 독립 논문·실험 수와 같지 않다.

[전체 출처 장부](sources-ledger.md)

<span id="source-1"></span>

**[Source 1]** Schepen/Everingham/Wang2020 title metadata, lead personally fetched, access2026-10-06, partial abstract only.

https://researchonline.jcu.edu.au/67563/

<span id="source-2"></span>

**[Source 2]** NOAA weekly CSGD+RUFCO documentation, lead personally fetched, access2026-10-06.

https://www.psl.noaa.gov/forecasts/s2s_NNprecip/info.html

<span id="source-3"></span>

**[Source 3]** Shao et al.2021 trend-aware BJP, lead personally fetched, access2026-10-06.

https://journals.ametsoc.org/view/journals/mwre/149/8/MWR-D-20-0318.1.xml

<span id="source-4"></span>

**[Source 4]** Baran/Nemoda CSG EMOS, rendered live abstract+DOI by top-source-browser, access2026-10-06.

https://arxiv.org/abs/1512.04068

<span id="source-5"></span>

**[Source 5]** Schepen/Everingham/Wang2020 full body, dependence observer, access2026-10-06.

https://journals.ametsoc.org/view/journals/mwre/148/1/mwr-d-19-0046.1.xml

<span id="source-6"></span>

**[Source 6]** Schepen/Wang2013 seasonal BJP, primary-web-recovery full methods, access2026-10-06.

https://journals.ametsoc.org/view/journals/mwre/141/12/mwr-d-12-00253.1.xml

<span id="source-7"></span>

**[Source 7]** Schepen/Wang/Robertson2014 calibration/bridging, full primary, access2026-10-06.

https://journals.ametsoc.org/view/journals/mwre/142/5/mwr-d-13-00248.1.xml

<span id="source-8"></span>

**[Source 8]** Shao2022 rainfall trend, full primary, access2026-10-06.

https://journals.ametsoc.org/view/journals/hydr/23/1/JHM-D-21-0099.1.xml

<span id="source-9"></span>

**[Source 9]** Cannon MBCn canonical2018 paper, live rendered full text, access2026-10-06.

https://link.springer.com/article/10.1007/s00382-017-3580-6

<span id="source-10"></span>

**[Source 10]** Sansom2016 recalibration, validation full primary, access2026-10-06.

https://empslocal.ex.ac.uk/people/staff/dbs202/publications/2016/sansom.pdf

<span id="source-11"></span>

**[Source 11]** Ferro fair scores, validation full primary, access2026-10-06.

https://empslocal.ex.ac.uk/people/staff/ferro/Publications/ferro2013.pdf

<span id="source-12"></span>

**[Source 12]** Risbey2021 future CV, validation full primary, access2026-10-06.

https://pmc.ncbi.nlm.nih.gov/articles/PMC8285537/

<span id="source-13"></span>

**[Source 13]** APCC model metadata p11, external provenance only, validation observer, access2026-10-06.

https://www.apcc21.org/prediction/file/download?lang=ko&targetKind=Model_Description%2Fen%2F&targetName=%28ENG%29_APCC_MME_model_description.pdf

<span id="source-14"></span>

**[Source 14]** Siegert2016 Bayesian signal-noise, validation full primary, access2026-10-06.

https://arxiv.org/pdf/1504.01933

<span id="source-15"></span>

**[Source 15]** Manzanas2022 hindcast/ensemble sizes, validation full primary, access2026-10-06.

https://upcommons.upc.edu/server/api/core/bitstreams/13e78798-309f-4387-a83d-b7b2f89387b1/content

<span id="source-16"></span>

**[Source 16]** Testing the Tests2018, validation primary, access2026-10-06.

https://journals.ametsoc.org/view/journals/mwre/146/6/mwr-d-17-0295.1.xml

<span id="source-17"></span>

**[Source 17]** Gilleland2020 block bootstrap, partial long fetch with methods checked, access2026-10-06.

https://journals.ametsoc.org/view/journals/atot/37/11/JTECH-D-20-0069.1.xml

<span id="source-18"></span>

**[Source 18]** Sampling Errors2009 pooling, validation full primary, access2026-10-06.

https://journals.ametsoc.org/view/journals/mwre/137/3/2008mwr2560.1.xml

<span id="source-19"></span>

**[Source 19]** Kim2022 KMA GloSea6 operational metadata, full Korean primary, access2026-10-06.

https://j-komes.or.kr/_PR/view/index.php?aidx=35356&bidx=3169

<span id="source-20"></span>

**[Source 20]** institution-specific guide, validation primary, access2026-10-06.

https://www.metoffice.gov.uk/research/climate/seasonal-to-decadal/gpc-outlooks/user-guide/global-seasonal-forecasting-system-glosea6

<span id="source-21"></span>

**[Source 21]** operational ELR, validation primary, access2026-10-06.

https://iri.columbia.edu/our-expertise/climate/forecasts/seasonal-climate-forecasts/methodology/

<span id="source-22"></span>

**[Source 22]** CBaM operational implementation, validation primary, access2026-10-06.

https://www.cpc.ncep.noaa.gov/products/people/sstrazzo/cbam/about.php

<span id="source-23"></span>

**[Source 23]** Beverley2024 trend diagnostics, validation full primary, access2026-10-06.

https://www.nature.com/articles/s41612-024-00832-w

<span id="source-24"></span>

**[Source 24]** Uttarwar2025 seasonal NN daily gridpoint targets, learning full primary, access2026-10-06.

https://publikationen.bibliothek.kit.edu/1000184833/165786127

<span id="source-25"></span>

**[Source 25]** Tanzania monthly QRF hybrid, learning full primary, access2026-10-06.

https://journals.ametsoc.org/view/journals/apme/63/10/JAMC-D-24-0014.1.xml

<span id="source-26"></span>

**[Source 26]** Möller2013 plug-in Gaussian copula, dependence full primary, access2026-10-06.

https://arxiv.org/html/1202.3956

<span id="source-27"></span>

**[Source 27]** Scheuerer/Hamill2015 CSG, full primary, access2026-10-06.

https://journals.ametsoc.org/view/journals/mwre/143/11/mwr-d-15-0061.1.xml

<span id="source-28"></span>

**[Source 28]** Scheuerer2014 GEV, full primary, access2026-10-06.

https://arxiv.org/html/1302.0893

<span id="source-29"></span>

**[Source 29]** Sloughter2007 rainBMA, full primary, access2026-10-06.

https://journals.ametsoc.org/view/journals/mwre/135/9/mwr3441.1.xml

<span id="source-30"></span>

**[Source 30]** crch2016 method/software, full primary, access2026-10-06.

https://journal.r-project.org/articles/RJ-2016-012/

<span id="source-31"></span>

**[Source 31]** Svensson2017 monthlycatchment distributions, full primary, access2026-10-06.

https://nora.nerc.ac.uk/515472/1/N515472JA.pdf

<span id="source-32"></span>

**[Source 32]** Hasan2010 abstract-only, access2026-10-06.

https://researchportalplus.anu.edu.au/en/publications/a-simple-poisson-gamma-model-for-modelling-rainfall-occurrence-an/

<span id="source-33"></span>

**[Source 33]** implementation reference not run, access2026-10-06.

https://search.r-project.org/CRAN/refmans/ensembleMOS/html/ensembleMOScsg0.html

<span id="source-34"></span>

**[Source 34]** located implementation API not run, access2026-10-06.

https://scoringrules.readthedocs.io/en/latest/generated/scoringrules.crps_csg0.html

<span id="source-35"></span>

**[Source 35]** HCLR vsBMA training-dependent comparison, primary, access2026-10-06.

https://journals.ametsoc.org/view/journals/mwre/145/5/mwr-d-16-0251.1.xml

<span id="source-36"></span>

**[Source 36]** transformed hierarchical rain preprint, primary, access2026-10-06.

https://arxiv.org/html/1804.09233

<span id="source-37"></span>

**[Source 37]** seasonal monthly copula agriculture, primary, access2026-10-06.

https://journals.ametsoc.org/view/journals/apme/59/3/jamc-d-19-0093.1.xml

<span id="source-38"></span>

**[Source 38]** Gaussian copula tail math abstract only, access2026-10-06.

https://arxiv.org/abs/1607.04736

<span id="source-39"></span>

**[Source 39]** CSIRO BJP Rpackages metadata only, access2026-10-06.

https://researchdata.edu.au/bayesian-joint-probability-r-packages/1449950

<span id="source-40"></span>

**[Source 40]** Kharin2017 seasonal smoothing, full primary.

https://journals.ametsoc.org/view/journals/mwre/145/9/mwr-d-16-0337.1.xml

<span id="source-41"></span>

**[Source 41]** Tippett2014 estimated Gaussian regression uncertainty, primary.

https://doi.org/10.1175/JCLI-D-13-00565.1

<span id="source-42"></span>

**[Source 42]** Siegert/Sansom/Williams2016 recalibration parameter uncertainty, primary.

https://doi.org/10.1002/qj.2716

<span id="source-43"></span>

**[Source 43]** Kharin/Zwiers2003 seasonal rescaling, primary.

https://doi.org/10.1175/1520-0442(2003)016%3C1684%3AISPF%3E2.0.CO%3B2

<span id="source-44"></span>

**[Source 44]** Landman/Goddard2002 regional rainfall MOS, primary.

https://doi.org/10.1175/1520-0442(2002)015%3C2038%3ASROGFO%3E2.0.CO%3B2

<span id="source-45"></span>

**[Source 45]** QRF2006 full foundational primary.

https://www.jmlr.org/papers/volume7/meinshausen06a/meinshausen06a.pdf

<span id="source-46"></span>

**[Source 46]** Taillardat2016 temperature/wind QRF, primary.

https://journals.ametsoc.org/view/journals/mwre/144/6/mwr-d-15-0260.1.xml

<span id="source-47"></span>

**[Source 47]** Taillardat2019 rainQRF/EGP, primary.

https://journals.ametsoc.org/view/journals/wefo/34/3/waf-d-18-0149_1.xml

<span id="source-48"></span>

**[Source 48]** Messner2017 distributional boosting, primary.

https://journals.ametsoc.org/view/journals/mwre/145/1/mwr-d-16-0088.1.xml

<span id="source-49"></span>

**[Source 49]** Benacek2023 limitedtraining comparison, primary.

https://journals.ametsoc.org/view/journals/wefo/38/1/WAF-D-22-0006.1.xml

<span id="source-50"></span>

**[Source 50]** Henzi2021IDR, full institutional manuscript also read.

https://arxiv.org/abs/1909.03725

<span id="source-51"></span>

**[Source 51]** Rasp/Lerch2018DRN, primary.

https://journals.ametsoc.org/view/journals/mwre/146/11/mwr-d-18-0187.1.xml

<span id="source-52"></span>

**[Source 52]** Bremnes2020BQN, primary.

https://journals.ametsoc.org/view/journals/mwre/148/1/mwr-d-19-0227.1.xml

<span id="source-53"></span>

**[Source 53]** Schulz/Lerch2022 benchmark, primary.

https://journals.ametsoc.org/view/journals/mwre/150/1/MWR-D-21-0150.1.xml

<span id="source-54"></span>

**[Source 54]** Horat/Lerch2024subseasonalCNN, primary.

https://journals.ametsoc.org/view/journals/mwre/152/3/MWR-D-23-0150.1.xml

<span id="source-55"></span>

**[Source 55]** Messner2014ordered/logistic, primary.

https://journals.ametsoc.org/view/journals/mwre/142/8/mwr-d-13-00355.1.xml

<span id="source-56"></span>

**[Source 56]** Robertson2023weeklyELR, primary.

https://journals.ametsoc.org/view/journals/wefo/38/6/WAF-D-22-0160.1.xml

<span id="source-57"></span>

**[Source 57]** Wilks2009ELR foundation.

https://rmets.onlinelibrary.wiley.com/doi/abs/10.1002/met.134

<span id="source-58"></span>

**[Source 58]** NGBoost2020 primary.

https://proceedings.mlr.press/v119/duan20a.html

<span id="source-59"></span>

**[Source 59]** Finnis2012nonlinearSVR30annualcases, full primary.

https://goapp.ocean.dal.ca/docs/various/Finnis_et_al.pdf

<span id="source-60"></span>

**[Source 60]** Raftery2005BMA, primary.

https://journals.ametsoc.org/view/journals/mwre/133/5/mwr2906.1.xml

<span id="source-61"></span>

**[Source 61]** Fraley2010exchangeableBMA, primary.

https://journals.ametsoc.org/view/journals/mwre/138/1/2009mwr3046.1.xml

<span id="source-62"></span>

**[Source 62]** Roulston/Smith2003dressing.

https://doi.org/10.1034/j.1600-0870.2003.201378.x

<span id="source-63"></span>

**[Source 63]** Brocker/Smith2008adaptive dressing.

https://doi.org/10.1111/j.1600-0870.2008.00333.x

<span id="source-64"></span>

**[Source 64]** Kleiber2008mixturetails, primary.

https://journals.ametsoc.org/view/journals/mwre/136/12/2008mwr2565.1.xml

<span id="source-65"></span>

**[Source 65]** Baran/Lerch2018CDFpools, primary.

https://arxiv.org/html/1607.08096v3

<span id="source-66"></span>

**[Source 66]** ECC2013 full manuscript, publisher browser access blocked.

https://arxiv.org/html/1302.7149

<span id="source-67"></span>

**[Source 67]** dECC2016full manuscript.

https://arxiv.org/html/1511.05877

<span id="source-68"></span>

**[Source 68]** Clark2004Schaake source identity and primary body via publisher.

https://pubs.usgs.gov/publication/70027101

<span id="source-69"></span>

**[Source 69]** Cannon2016MBCp/r, primary main body.

https://journals.ametsoc.org/view/journals/clim/29/19/jcli-d-15-0679.1.xml

<span id="source-70"></span>

**[Source 70]** Robin2019OTC/dOTC, full primary.

https://hess.copernicus.org/articles/23/773/2019/

<span id="source-71"></span>

**[Source 71]** Lerch2020multivariate simulationcomparison.

https://npg.copernicus.org/articles/27/349/2020/

<span id="source-72"></span>

**[Source 72]** Shrestha2020abstract-only accumulationwarning.

https://agris.fao.org/search/en/providers/122535/records/65e00a5663b8185d9cb0d2e9

<span id="source-73"></span>

**[Source 73]** Hempel2013trend-preserving climateimpact adjustment.

https://doi.org/10.5194/esd-4-219-2013

<span id="source-74"></span>

**[Source 74]** Cannon2015QDM projectionmechanism.

https://doi.org/10.1175/JCLI-D-14-00754.1

<span id="source-75"></span>

**[Source 75]** Maraun2016biascorrectionreview.

https://doi.org/10.1007/s40641-016-0050-x

<span id="source-76"></span>

**[Source 76]** Gneiting2005EMOS foundational, correct DOI.

https://doi.org/10.1175/MWR2904.1

<span id="source-77"></span>

**[Source 77]** Luo2007hydrologicalclimatologyprior, conceptual only.

https://doi.org/10.1029/2006JD007655

<span id="source-78"></span>

**[Source 78]** Doblas-Reyes2005seasonalcalibration/combination canonicalrecord, legacy DOI differs.

https://doi.org/10.3402/tellusa.v57i3.14658

<span id="source-79"></span>

**[Source 79]** SBCK pinned README, implementation-only, API not executed.

https://github.com/yrobink/SBCK/blob/3210dda44215dfbd6214fe7beadc38a70fa14f10/README.md

<span id="source-80"></span>

**[Source 80]** Schaake pinned source, implementation-only, no real-data execution.

https://github.com/nmcdev/nmc_met_base/blob/9b90ef72a3b31fc40707e253cca9b9b45c2cc3b6/nmc_met_base/ensemble.py

<span id="source-81"></span>

**[Source 81]** Vannitsem2021 postprocessing review, broad weather scope.

https://journals.ametsoc.org/abstract/journals/bams/102/3/BAMS-D-19-0308.1.xml

<span id="source-82"></span>

**[Source 82]** QRF implementation README, not executed.

https://github.com/zillow/quantile-forest

<span id="source-83"></span>

**[Source 83]** R IDR author implementation, not executed.

https://github.com/AlexanderHenzi/isodistrreg

<span id="source-84"></span>

**[Source 84]** Python IDR adaptation, not executed.

https://github.com/evwalz/isodisreg

<span id="source-85"></span>

**[Source 85]** DRN author implementation, not executed.

https://github.com/slerch/ppnn

<span id="source-86"></span>

**[Source 86]** DRN/BQN benchmark implementation, not executed.

https://github.com/benediktschulz/paper_pp_wind_gusts

<span id="source-87"></span>

**[Source 87]** NGBoost implementation, not executed.

https://github.com/stanfordmlgroup/ngboost

<span id="source-88"></span>

**[Source 88]** MBCn/OTC/dOTC implementation, not executed.

https://github.com/yrobink/SBCK-python

<span id="source-89"></span>

**[Source 89]** MBC current manual, not executed.

https://cran.r-project.org/web/packages/MBC/refman/MBC.html

<span id="source-90"></span>

**[Source 90]** BMA groups/missing-member manual, not executed.

https://search.r-project.org/CRAN/refmans/ensembleBMA/html/ensembleBMA.html

<span id="source-91"></span>

**[Source 91]** Alpine daily seasonal NN implementation, not executed.

https://github.com/Sam-Uttarwar/NN_arch

<span id="source-92"></span>

**[Source 92]** global biweekly NN implementation, not executed.

https://github.com/HoratN/pp-s2s

<span id="source-93"></span>

**[Source 93]** dependence simulation implementation, not executed.

https://github.com/slerch/multiv_pp

