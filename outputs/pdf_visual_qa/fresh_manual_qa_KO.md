# 신규 관측 재검증: 루트 직접 사용·시각 QA

대상: `outputs/GLOSEA6_verification_by_dimension_KO_refreshed.pdf`

PDF SHA256: `e673c90839e09fe9bd97038b160a8db6d27a599c43faa922cac6eefdb2daa6a0`

관측 스냅샷: 1991-01-01–2026-10-05. 아래 검토는 이번 실행 후 새로
렌더링한 68쪽과 17개 contact sheet에 대한 루트의 직접 확인이다.
이전 PDF 승인이나 이전 수치 검사를 재사용하지 않았다.

## 실제 실행 QA

| 시나리오 | 실제 명령·사용 | 관찰 결과 | 판정·근거 |
| --- | --- | --- | --- |
| 신규 원자료 완전성·결측 구분 | `node analysis/collect_observations.mjs --auth-stdin --end 20261005` | 62개 고정 ID, 13,062일, 809,820/809,844 지점·날짜 행; 행 누락 24개와 반환된 기온값 결측 258개를 별도 기록 | PASS: `observations/kmahub_refresh/{provenance,coverage_audit}.json`, `coverage_gaps.csv` |
| 원응답→지점 행→일평균 독립 재계산 | `python analysis/audit_fresh_observations.py` | 450개 원응답 해시, 지점 export, 결측 장부, 날짜 범위, 평균 검산 PASS; 최대 평균 차이 기온 2.13e-14, 강수 2.84e-14 | PASS: `observations/kmahub_refresh/independent_audit.json` |
| 원본 경로 회귀 | 소스 활성화 전 `load_daily(source)` 직접 실행 | 기존 13,027일과 2022-05-20의 기온 61/강수 62 기여 수·OK 상태 유지 | PASS: 이번 세션의 `ORIGINAL_SOURCE_DRIVER_PASS` 실행 기록 |
| 새 소스 선택 | 활성화 후 `observation_provenance`, `load_daily`, `check_manifest` 직접 실행 | 선택된 새 자료 13,062일, 일자료 해시 일치; 원본 24개 manifest 해시 일치 | PASS: `observations/active_source.json`, 신규 독립 감사, `outputs/run_summary.json` |
| 실제 검증 진입점 정상 사용 | `python analysis/run_verification.py` | 6,580개 모두 처리, 검증 6,432개, 4방법 각각 6,432행, EMOS 적합 실패 0개 | PASS: `outputs/run_summary.json`, `case_audit.csv`, `matched_predictions.csv.gz` |
| 도움말·잘못된 입력 | 같은 진입점의 `--help`, `--invalid` 직접 실행 | 도움말은 종료 0, 잘못된 인자는 `Unexpected arguments; use --help` 및 종료 1; 생산 출력 재실행 없음 | PASS: 세션 실제 CLI 기록; 아래 관찰 transcript |
| 전체 수치·누출 경계 | `python analysis/validate_results.py`, `audit_training.py` | 9,163,254개 독립 검사 PASS; 156,408개 채택 연도 쌍, 훈련/검증 OBS 최대 차이 0; 초기일 이후 관측 제외 | PASS: `outputs/validation.json`, `outputs/method_review/training_audit.json` |
| 보정·점수 독립 재현 | `audit_emos.py`, `audit_scoring_sensitivity.py`, `audit_qm_qdm.py` | EMOS 6,432 적합·32 민감도 사례와 점수 감사 통과. QM/QDM 엄격 경고 1개를 종료 1로 보존, 계산 순서 기준 실패 0개 | 기대 경고 유지 PASS: 새 `outputs/method_review/*audit.json`, `scoring_sensitivity.json`; 엄격 oracle 자체를 clean PASS로 주장하지 않음 |
| 코드 검사 | 프로젝트 `.venv`의 Ruff 및 basedpyright 전체 `analysis` 검사 | 린트 통과, 타입 오류 0·경고 0. 일부 도구 LSP의 경로/스텁 해석 문제는 실제 venv 검사와 구분 | PASS: 이번 세션 최종 실제 검사 출력 |
| 원본 유지 | 신규 실행 후 `check_manifest` 직접 실행 | 원본 24개 해시 일치. 작업 중 사라진 CSV 7개는 기존 파일을 덮어쓰지 않고 원본 압축본에서 누락분만 복구; 삭제 원인은 미확인 | PASS: 신규 독립 감사와 `ORIGINAL_24_INPUT_HASHES_PASS 24` 실행 기록 |
| 사용자 PDF 잠금 | 실제 Windows 잠금 상태에서 PDF 생성 실행 | 잠긴 `_final.pdf`는 닫거나 덮어쓰지 않음; 새 `_refreshed.pdf` 발행 및 manifest 연결 | PASS: `outputs/pdf_manifest.json`, 실제 `VIEWER_LOCK`·`PDF_COMPLETE` 실행 기록 |
| 실제 PDF의 수치·기능 검사 | `python analysis/validate_dimension_pdf.py` | 78,431개 검사, 10,640개 plot record 비교, 68쪽 150dpi 새 렌더, 오류 0 | PASS: `outputs/pdf_validation.json`, `outputs/pdf_qa/pages/` |

### 직접 관찰한 CLI transcript

```text
$ .venv/Scripts/python.exe analysis/run_verification.py --help
Usage: python analysis/run_verification.py
Verify RAW, QM, QDM and EMOS on all source-QC-valid cases; write outputs/.
[exit 0]

$ .venv/Scripts/python.exe analysis/run_verification.py --invalid
Unexpected arguments; use --help
[exit 1]
```

## 전 페이지 시각 확인

모든 contact sheet는 실제 도구로 열어 보았다. 확인 항목: 페이지 순서와
번호, 표·본문·제목의 잘림/겹침, 한글 글리프, 축·단위·범례, 회색 공통 N
막대, 네 방법의 구분, 기후/관측 기준선, 월간 기온의 범주 불균형 주석,
읽을 수 있는 여백·footer, 비어 있거나 미완성인 화면 여부.
새 표지에서 새 관측 출처·마감일·6,432개 사례·미세 경고를 직접 확인했다.
웹/모바일/다크 모드/동작·키보드 상태는 정적 PDF에 해당하지 않는다.

| 확인한 쪽 | 실제 확인 이미지 | 판정 |
| --- | --- | --- |
| 1–4 | `outputs/pdf_qa/contact_sheets/contact_001.png` | 1/2/3/4쪽 모두 PASS |
| 5–8 | `outputs/pdf_qa/contact_sheets/contact_002.png` | 5/6/7/8쪽 모두 PASS |
| 9–12 | `outputs/pdf_qa/contact_sheets/contact_003.png` | 9/10/11/12쪽 모두 PASS |
| 13–16 | `outputs/pdf_qa/contact_sheets/contact_004.png` | 13/14/15/16쪽 모두 PASS |
| 17–20 | `outputs/pdf_qa/contact_sheets/contact_005.png` | 17/18/19/20쪽 모두 PASS |
| 21–24 | `outputs/pdf_qa/contact_sheets/contact_006.png` | 21/22/23/24쪽 모두 PASS |
| 25–28 | `outputs/pdf_qa/contact_sheets/contact_007.png` | 25/26/27/28쪽 모두 PASS |
| 29–32 | `outputs/pdf_qa/contact_sheets/contact_008.png` | 29/30/31/32쪽 모두 PASS |
| 33–36 | `outputs/pdf_qa/contact_sheets/contact_009.png` | 33/34/35/36쪽 모두 PASS |
| 37–40 | `outputs/pdf_qa/contact_sheets/contact_010.png` | 37/38/39/40쪽 모두 PASS |
| 41–44 | `outputs/pdf_qa/contact_sheets/contact_011.png` | 41/42/43/44쪽 모두 PASS |
| 45–48 | `outputs/pdf_qa/contact_sheets/contact_012.png` | 45/46/47/48쪽 모두 PASS |
| 49–52 | `outputs/pdf_qa/contact_sheets/contact_013.png` | 49/50/51/52쪽 모두 PASS |
| 53–56 | `outputs/pdf_qa/contact_sheets/contact_014.png` | 53/54/55/56쪽 모두 PASS |
| 57–60 | `outputs/pdf_qa/contact_sheets/contact_015.png` | 57/58/59/60쪽 모두 PASS |
| 61–64 | `outputs/pdf_qa/contact_sheets/contact_016.png` | 61/62/63/64쪽 모두 PASS |
| 65–68 | `outputs/pdf_qa/contact_sheets/contact_017.png` | 65/66/67/68쪽 모두 PASS |

## 판정 범위

직접 사용·정적 PDF 화면 검토: **PASS**. 개별 기기 QC나 62지점의 모든
변수값이 항상 존재함을 인증하지 않는다. QDM 엄격 반올림 경고 1개,
기여 지점 구성·공간 대표성, 기간 중첩과 통계적 한계는 새 보고서와 방법
검토에 공개했다. 최종 독립 gate 검토는 별도 항목이다.
