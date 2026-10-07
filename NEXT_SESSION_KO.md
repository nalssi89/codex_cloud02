# 다음 세션에서 여기부터 이어가기

## 사용자 요청과 현재 상태

2026-10-07 컴퓨터 종료를 위해 **통계 계산을 중단**했습니다.
현재 요청은 작업과 재개 기록을
`https://github.com/nalssi89/codex_cloud02` 비공개 저장소에 보존하는 것입니다.
사용자가 다시 진행을 요청하기 전에는 비교 계산을 자동 재시작하지 않습니다.

이 백업은 전체 실험 완료본이 아닙니다. 과학 작업은 **44/51개 완료**,
아래 7개 작업이 남아 있습니다. 추가 GitHub 보존 작업은 별도로 기록됩니다.
기존 원격 README와 초기 이력은 유지합니다.

## 처음 읽을 파일

1. 이 파일과 `CHECKPOINT_KO.md`.
2. `.omo/notepads/ulw-alternative-comparison-20261007.md` **전체**.
3. `.omo/notepads/alternative-statistical-plan.md`.
4. `.omo/evidence/alternative-output-schema.md`.
5. `.omo/evidence/alternative-comparison-interruption-20261007.md`.

연구 원문은 `research_bias_correction/20261007-002200/`에 있습니다.
목표를 선호 방법의 일부 또는 좁은 component 검사로 축소하지 않습니다.

## 그대로 유지해야 할 전체 목표

- 17계열과 연구에서 명명된 61개 하위 방법을 빠짐없이 구현하거나 실제
  자료에 근거해 과학적 비적용 이유를 제시합니다.
- RAW/QM/QDM/EMOS 및 훈련 기후값을 포함한 66개 등록 방법을 비교합니다.
- 활성 fresh KMA 관측과 과거 전용 연간 pairs를 사용합니다.
- 전체 6,580개 사례와 현재 평가 가능한 6,432개를 빠짐없이 연결합니다.
- 연속 예측은 실제 원단위 분포·CRPS·범주 확률로 검증합니다.
  범주/결합 방법은 자신의 예측 객체로 평가하며 연속 성능을 조작하지 않습니다.
- 적합/수치 실패와 과학적 게이트를 구별하고, 공통 마스크·실패 포함 정책·
  lead/month/season/year·중복 기간과 의존성 민감도를 유지합니다.
- 비용·난도를 비적용 이유로 사용하지 않습니다. station 값을 보간하거나
  member iid/물리적 identity/과거 운영 가용성/우월성을 만들어내지 않습니다.
- 원본 입력·관측·연구·이전 검증 산출물을 보존합니다.
  Git 커밋 금지는 이번 사용자가 명시적으로 요청한 백업에 한해 해제됐습니다.

## 확실히 완료한 증거

- 독립 기존 baseline 회귀: 9,163,254개 검사 통과, 기존 출력 미변경.
- registry 66개, 17계열/61하위형; 입력 6,580/정답 6,432/제외 148.
- 첫 전 방법 소규모 실행: 352개 작업 계산 완료.
  보고서의 CSV 기본 필드 한도 때문에 `FAILED_REPORTING`, exit 2.
- 이 실행의 실제 저장 분포 **586개**(scalar 152 + analytic joint 434),
  category 8개, joint 98개가 독립 검증 통과.
  energy/variogram 98개와 hot/dry 24개 통과.
- scalar 출처 1,344행/32hash/870fold,
  genuine joint 8hash/560fold 독립 검증 통과.
- 큰 CSV 경계 수정: 실제 최대 **8,180,248자** 필드를 양쪽 reader가
  정확히 읽고 원본 bytes/hash/mtime를 보존. 실제 보고서 CLI도 exit 0.
  실패한 실행의 보고 상태는 정직하게 `INCOMPLETE/SMOKE`로 유지.
- 신규 전체 코드 Ruff/basedpyright 통과. 이후 CSV 수정 3파일도 각각 통과.
- 원본 60파일 보호 해시와 알려진 strict QDM 경고를 유지.
  `1.0345502232667059e-10 > 1e-10` 경고를 숨기거나 tolerance를 완화하지 않음.

자세한 receipt는 `.omo/evidence/`에 있습니다. Component 또는 SMOKE 통과를
FULL SC1/SC2 통과라고 표현하지 않습니다.

## 중단된 실행과 재개 명령

수정 후 재실행 출력:
`outputs/alternative_comparison_root_all_methods_smoke_v2`.
마지막 표시 진행은 `200/352`였습니다. `bash_157`을 종료했고
`mon_QHBCAR39M53DC1JE`의 killed 통지를 확인했습니다.
Fortran의 Windows CLOSE 메시지는 사용자 중단이며 통계 수치 실패가 아닙니다.

`run_summary.json`의 `RUNNING`은 강제 중단 전 기록으로, 살아 있는 작업이
아닙니다. 재개 시 완료된 캐시의 실제 수와 identity를 확인합니다.

```text
.venv/Scripts/python.exe -B analysis/run_alternative_comparison.py --output outputs/alternative_comparison_root_all_methods_smoke_v2 --case-id 20220307_1MON_W01_t15m --case-id 20220307_1MON_W01_prcp --case-id 20220307_3MON_M01_t15m --case-id 20220307_3MON_M01_prcp --workers 4 --resume
```

`.venv`, 자격증명, 대형 `cache/`는 GitHub 백업에서 제외합니다.
원래 PC에는 캐시가 남습니다. 새 복제본에서는 제외된 적합을 다시 계산합니다.
의존성 버전의 실제 기록은
`outputs/alternative_runner_metadata_ready_smoke/run_summary.json`의
`dependency_versions`와 `.omo/evidence/alternative-torch-qa.json`을 읽습니다.
Torch 2.8.0 CPU는 실제 실행 검증됐습니다. 이전 관측 수집이나 PDF 검증을
bootstrap 명목으로 반복하지 않습니다.

## 남은 7개 과학 작업: 이 순서로

1. 재개한 소규모 CLI의 exit 0, 완료 상태, 출처/보호 guard, 66방법 상태,
   실제 표·보고서 및 저장 점수·출처를 확인합니다.
2. 전체 자료의 모든 적용 방법을 실행합니다:
   `.venv/Scripts/python.exe -B analysis/run_alternative_comparison.py --output outputs/alternative_comparison`
3. 전체 독립 검증을 실행합니다:
   `.venv/Scripts/python.exe -B analysis/validate_alternative_comparison.py --output outputs/alternative_comparison`
4. 신규 코드 정적 검사와 관련 기존·신규 회귀를 최종 확인합니다.
5. 최종 전체 비교 보고서·표·모든 그림을 직접 열어 QA합니다.
6. 원본 보존·프로세스/자원 종료·append-only 자체 검토를 완료합니다.
7. 각 요구사항을 실제 FULL 증거에 대조한 완료 감사를 작성한 후에만
   전체 목표를 완료 처리하고 결과를 전달합니다.

전체 실행용 `outputs/alternative_comparison`은 비어 있습니다.
이전 미완료 validator 결과는
`.omo/evidence/alternative-pre-full-validation.json`으로 **보존**했습니다.
새 파일이 생기면 안전 가드를 우회하지 말고 재개/보존 정책을 확인합니다.

## 실행 중 지켜야 할 규칙

실행기의 출처 해시는 모든 `analysis/*.py`와 통계 계획·출력 schema를
포함합니다. 적합 중 코드 수정은 출처 guard를 실패시키므로 먼저 동결합니다.
오래 걸리는 실행은 완료 모니터에 맡기고 polling/sleep을 하지 않습니다.
새 오류는 실제 traceback으로 재현하고 원인을 최소 수정한 뒤 검증합니다.
`run_completed`는 `COMPLETED`만 인정합니다.

자료/결과의 사실이 사용자 기억이나 이 문서와 다르면 현재 실제 파일을 읽어
대조합니다. 전체 목표와 남은 작업을 삭제하거나 완료로 바꾸지 않습니다.
