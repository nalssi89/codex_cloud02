# 조사·검증 집계

## 구성
- 팀 2개, 팀원 총 16명: 방법별 수집·반론 팀 8명, 독립 정제 팀 8명.
- 팀 밖 작업 13개: 초기 조사 8개, 문헌 복구 2개, HTML 조립 1개, 한국어 교정 1개, SDK 최종 gate 1개.
- 총 작업 29개: 앞선 상태 확인 완료 27개와 마지막 gate 완료 1개, 최종 dossier 뒤 종료된 반론 담당 1개 cancelled. 미종료 0개.
- 초기 constrained librarian 4개는 검색 실패로 실질 결과가 inconclusive였으며 근거로 채택하지 않았다. 관련 축과 복구 레인이 원문을 확인했다.

## 조사 흐름
- 개시 수집: 독립 방법·자료·문헌·브라우징 영역 동시 조사.
- 후속 확장 묶음 1: NOAA 주간 CSGD, 월간 QRF/계절 NN, finite-member, 추세·검열, 초기장 provenance.
- 후속 확장 묶음 2: 복구 결과가 낸 새 spread 논문 DOI10.1002/qj.4925의 원문 접근과 MAP 변환·posterior 범위 등의 추가 확인. 접근 불가 lead는 gap으로 닫았다.
- 기존 일지의 wave1/2는 수집·통합 기록 묶음이다. 위 두 후속 탐색 묶음은 비동기 lead routing으로 겹쳐 수행했으며 새로운 대규모 수집 파동을 가장하지 않는다.
- 반론 2단계: 수집 팀 skeptic, 새 정제 팀 8개 관점. 연구 우선순위는 조건부 방법론 판단으로만 잠갔다.
- 별도 excursion: 0개. 모든 lead가 기존 축 소유자에게 귀속됐다.

## 근거와 계산
- 보고서 번호 출처 93개, 프로젝트 근거 P1–P3 별도. URL 수와 독립 논문·재현 실험 수는 다르다.
- 원전·저자 논문 자료로 분류한 URL 67개. 본문·초록·metadata 접근 경계는 출처 장부에 있다. 이 수는 독립 효능 복제 67건이 아니다.
- 위 67개 집계에서 제외한 번호:1,2,13,20,21,22,32,33,34,39,75,79,80,81,82–93. 기관·서비스 설명, software, review/metadata 경로를 구분했다.
- 합성 계산 검증 5개: 고정 Gaussian 조건부, 재정렬 주변 CRPS, log0/검열 예시, 혼합 전체 분산, 상관 멤버 평균잡음 반례.
- 실제 GloSea6 새 후보 적합·성능 실험: 0개. 생산 코드 수정: 이 연구에서 0개.
- 주장 graph의 공급행 provenance C12는 partial이며 실제 체계 변화·인과 효과를 단정하지 않았다. 새 방법 효능은 미측정. 잘못된 URL/DOI는 rejected 근거로 보존했다.

## 산출물 QA
- HTML diagnostics, 공식 static/layout, desktop1280×900/mobile390×844 light/dark, 실제 출처 클릭, 367개 본문·표·수식 복사 보존, 독립 한국어 전체+delta 교정: 모두 PASS.
- 원문 캡처·QA PNG는 보존 산출물이다. browser profiles/watchers/processes는 정리했다.
- `.omo/ulw-loop`와 goal 상태는 실행 제어 기록이며 생산 변경이 아니다.
- Git 저장소가 아니므로 프로젝트 커밋은 생성하지 않았다. 기억 저장 도구의 커밋은 별도 기억 repo 기록이다.
- elapsed/source-domain/manifest 상태는 최종 `closing-briefing.md`의 공식 출력이 기준이다.

## Native loop gate
모든 산출물 QA 후 SDK가 category 기반 gateReview 및현재시도디렉토리의
artifactRefs를요구했다. 실제독립deep-lowfinalgate가APPROVE를반환했다.
PNG네개는현재시도/a0경로에바이트동일(SHA256확인)복제했고CLI/geometry/copy증빙을
그곳에넣었다. 보고서내용재수정/추가탐색은하지않았다.
