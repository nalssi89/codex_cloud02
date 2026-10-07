# GloSea6 작업 중단 체크포인트

2026-10-07 사용자의 컴퓨터 종료 요청으로 비교 계산을 중단했습니다.
이 저장소는 **진행 중인 작업 백업**이며 전체 실험 완료 결과가 아닙니다.

## 보존한 작업

- 17개 연구 계열과 61개 하위 방법의 적용성 판정 및 구현.
- RAW/QM/QDM/EMOS/훈련 기후값을 포함한 66개 방법 실행기.
- 연속·범주·결합 예측 분포와 과거 전용 학습·독립 검증 코드.
- 연구 자료, 원본 입력, 관측 스냅샷, 기존 검증 결과와 작업 증거.
- 상세 작업 기록: `.omo/notepads/ulw-alternative-comparison-20261007.md`.
- 중단·재개 안내:
  `.omo/evidence/alternative-comparison-interruption-20261007.md`.

## 완료한 검증과 남은 작업

기존 baseline 9,163,254개 검사가 통과했습니다. 첫 전 방법 소규모 실행은
보고서 CSV 필드 한도 문제로 종료됐지만, 저장된 예측 586개 분포,
98개 결합 점수 및 학습 출처가 독립 검증을 통과했습니다.
CSV 경계를 수정하고 실제 최대 8,180,248자 필드의 무손실 읽기와 보고서
생성을 검증했습니다. 코드 Ruff·타입 검사도 통과했습니다.

수정 후 소규모 CLI 재실행은 마지막 표시 `200/352` 상태에서 사용자가
중단했습니다. 해당 `run_summary.json`의 `RUNNING`은 중단 전 저장값이며
현재 살아 있는 프로세스나 완료 결과를 뜻하지 않습니다.

**전체 자료 비교, 전체 독립 검증, 최종 보고서·그림 QA는 미완료입니다.**
기존 strict QDM 정밀도 경고는 그대로 유지합니다.

## 재개

먼저 가상환경과 코드의 현재 출처를 확인하고, 중단 안내의 소규모 명령에
`--resume`를 붙여 완료된 캐시만 엄격한 identity 검사 후 재사용합니다.
가상환경, 비밀키, 대형 실행 캐시는 GitHub에 올리지 않았습니다.
캐시는 원래 컴퓨터에 남아 있으므로 GitHub의 새 복제본에서는 해당 적합을
다시 계산해야 합니다. 완료되지 않은 checkpoint를 성공 예측으로 쓰지 않습니다.

소규모 실행 완료와 결과 확인 후:

```text
.venv/Scripts/python.exe -B analysis/run_alternative_comparison.py --output outputs/alternative_comparison
.venv/Scripts/python.exe -B analysis/validate_alternative_comparison.py --output outputs/alternative_comparison
```

원본·관측·연구·기존 결과를 덮어쓰지 않고 모든 적용 가능한 방법을 끝까지
실행·검증해야 합니다. 비용이나 난도를 과학적 제외 이유로 사용하지 않습니다.
