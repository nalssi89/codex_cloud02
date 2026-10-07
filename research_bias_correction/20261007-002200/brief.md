# GloSea6 대안 편의 보정 조사

Started: 2026-10-06T23:22:00Z

## Core question
QM, QDM, EMOS 이외의 방법 중 현재 GloSea6 주간·개별 월 기온/강수 앙상블에 적용 가능한 방법은 무엇이며 각각의 장단점과 실험 우선순위는 무엇인가?

## Ideal end state
기존 생산 코드·관측·보정 결과를 변경하지 않고, 별도 연구 디렉토리에 한국어 비교 자료, 출처, 프로젝트 적용 요건, 검증 설계와 한계를 남긴다. 성능 우열은 새 실제 자료 실험 없이 확정하지 않는다.

## Tier
HEAVY: 사용자가 정밀 연구를 요구했고 다수 방법의 통계 가정과 적용 판단이 필요하다. 생산 변경·전체 재적합은 범위 밖이다.

## Discovery
- outputs/REPORT_KO.md:7-11: 제공 권역 평균, 개별 지점/격자 자료 아님. 1mon=주간, 3mon=개별 달력 월.
- outputs/REPORT_KO.md:42-58: 과거 자료 24/30년; source-year별 동일 가중치; HIST_END < INIT_DATE와 target-year 제외.
- outputs/method_review/REVIEW_KO.md:144-158: 역사 멤버 3/7, 발행 멤버 수 다름; 소표본 분산·모수 불확실성 중요.
- outputs/method_review/REVIEW_KO.md:79-104: 현재 QDM은 발행 앙상블 순위를 쓰는 변형; 기후 기간 QDM의 추세 보존을 그대로 주장할 수 없음.
- git status / git log: exit 128, 프로젝트는 Git 저장소 아님. 연구 파일의 프로젝트 커밋 불가.
- 기억 glosea6-verification.md 및 glosea6-method-review.md 확인. strict62 결과는 과거 결과이며 최신 originalQC 정책을 기준으로 사용.
- report-style 기억 파일 없음. 비동기 형식 질문 발송, 답변 전에는 Markdown+HTML 기본값으로 진행.

## Axes and roster
1. joint-gaussian (deep-low): Joint Gaussian/BJP/NGR 조건부 예측과 강수 변환/검열.
2. precipitation (deep-low): CSG/Gamma/GEV, hurdle/occurrence-amount, 분포 선택.
3. mixtures (unspecified-low): BMA, kernel dressing, exchangeable-member 위험.
4. dependence (deep-low): ECC/Schaake/dECC, copula, MBCn와 다변량 보정의 구별.
5. parsimonious (unspecified-low): MOS, climatological shrinkage, anomaly/trend/mean-variance 보정.
6. learning (deep-low): QRF, boosting, distributional regression, neural methods의 데이터 요구.
7. validation (unspecified-high): 소표본 계절 예측 검증·풀링·자료 체계 전환.
8. skeptic (ultrabrain): 모든 추천의 반례·누출·독립성·성능 과장 공격.

Parallel lanes: project explore 1, primary literature librarian 2, implementation repo librarian 1, provenance browser 1, supplemental literature librarian 2, supplemental browser 1. 서로 다른 질문을 맡기며 파일 쓰기는 하지 않는다. 브라우징 작업만 임시 캡처 생성 허용.
Lifecycle: research team then refinement team (여러 문헌 영역과 7개 축). 사용 가능 category는 developer catalog의 quick, unspecified-low/high, deep-low/high, ultrabrain, architect, writing, artistry, visual-engineering. 로컬 omo.json은 찾지 못해 catalog 기준.

## Skills
- ulw-research: 조사·출처·반론·수렴·산출물 규약.
- ultimate-browsing/browser: 주요 원문 렌더와 HTML 실제 화면 검증.
- using-superpowers: 적용 지침 확인.
- memory-discipline: 검증된 사실만 지속 기억으로 저장.
- coding-agent-sessions: 이전 감사의 근거 필요 시 복구; 현행 감사 문서가 우선.
- verification-before-completion: 완료 주장 전에 실제 검증.
- frontend/visual-qa: HTML 조립과 화면 검증 단계에서 사용.
- data-scientist: 정량 자료 도표가 필요할 때만 사용. 새로운 성능 수치는 생성하지 않음.
TDD/brainstorming/refactor/git-master: 생산 기능·동작·Git 변경이 없어 해당 없음.

## Deliverable
lane: no-format (answered_by: request)
state: none
formats: md, html (answered_by: default; 비동기 질문 답변 반영)
destination: 이 별도 디렉토리 (answered_by: request)
audience: 현재 프로젝트 연구자, standard (answered_by: request/default)
template: clean analyst register (answered_by: default)
format description: 한눈에 보는 비교표 + 방법별 상세 장단점 + 프로젝트 우선순위 + 참고문헌

## Plan
1. 조사 brief, 디자인 규약, 초안, 인식론 장부를 생성한다.
2. 목표를 loop와 create_goal에 등록한다.
3. 8명 팀과 독립 문헌·코드·브라우징 레인을 동시에 시작한다.
4. 모든 반환을 도착 즉시 기록하고 출처와 주장 및 EXPAND를 연결한다.
5. 추가 조사 파동과 반론을 거쳐 미확인 주장/리드를 닫는다.
6. 계산 가능한 논쟁은 격리된 합성 예제로 검증한다. 실제 성능 실험과 구분한다.
7. 연구팀 종료 후 별도 정제 반론으로 추천을 잠근다.
8. 한국어 Markdown와 HTML, 의사결정 도표를 작성한다.
9. 정적·레이아웃·데스크톱/모바일 시각·한국어 교정 검증한다.
10. 산출물 manifest 검증, 모든 팀/레인/브라우저 종료, 완료 안내.

## Success criteria + QA scenarios
- C1: 주요 방법군 및 Joint Gaussian 비교. report 읽기와 출처 확인: 방법별 원리·장점·단점·기온/강수·현재 자료 요건·우선순위가 모두 있고 출처가 연결되면 PASS. artifacts: SYNTHESIS.md, claim-graph.md, sources-ledger.md.
- C2: 적용 제약·검증 설계. 현재 문서의 자료 단위/기간/멤버/훈련 누출 방지와 비교: 일치하고 실제 성능 미실험을 명시하면 PASS. artifacts: project-evidence.md, debate-log.md.
- C3: 계산 가능한 주장 검증. 격리 driver 실행: Joint Gaussian 조건부 분산/평균, 강수 비음수 처리, 재정렬 주변분포 불변성이 독립 식과 일치하면 PASS. artifact: verify-mechanisms.md.
- C4: HTML 실제 사용. owned browser에서 file:///D:/WORK/Projects/omo/Glosea6/research_bias_correction/20261007-002200/report.html 열기, desktop 1280×900 및 mobile 390×844: 빈 화면·겹침·본문 overflow 없음, 비교표와 출처 탐색 가능이면 PASS. artifact: screenshots, boxes.json, defects.json.
- C5: report-tools outcome verify --session-dir 이 경로: exit 0, 모든 산출물 존재; 모든 연구 작업 terminal, cleanup receipt 있으면 PASS.

## Stop
I'll stop right away when 한국어 비교 자료의 출처·프로젝트 적합성·화면 검증과 작업 정리가 완료되면 종료한다.

## Now
연구 전용 디렉토리와 조사 범위 문서 작성하기

## Todo
대안 보정 방법별 독립 조사 작업 실행하기; 프로젝트 적용 조건과 문헌 근거 교차 검증하기; 쟁점 반론과 추가 조사 결과 기록하기; 한국어 방법 비교 보고서와 근거 목록 작성하기; 보고서 정확성 표현과 산출물 형식 검증하기; 연구 작업 정리하고 최종 보고서 위치 안내하기

## Findings
별도 디렉토리 밖 파일은 읽기 전용으로 다룬다.

## Learnings
역사 멤버 수를 관측 독립 표본 수로 세지 않는다. 일변량 보정과 의존성 복원은 서로 다른 작업이다.

## Timestamp correction
폴더 이름에 수동 시각 오류가 있다. 폴더는 재명명하지 않고 유지한다. 실제 디렉토리 birthtime=2026-10-06T23:17:20.487Z를 fs.stat로 확인했다. outcome startedAt을 이 관측값으로 교정해 약8시간 부풀려진 연구 경과 시간을 보고하지 않는다. 상단 Started는 계획 작성 추정시각이며 실제 시작 기록은 이 교정값이 우선.

## Transition
Now: 프로젝트 적용 조건과 문헌 근거 교차 검증하기
Todo: 쟁점 반론과 추가 조사 결과 기록하기; 한국어 방법 비교 보고서와 근거 목록 작성하기; 보고서 정확성 표현과 산출물 형식 검증하기; 연구 작업 정리하고 최종 보고서 위치 안내하기
All seven method/validation researchers and literature/browsing lanes final; adversarial skeptic still running, no silent approval inferred.

## Transition after claim lock
Now: 한국어 방법 비교 보고서와 근거 목록 작성하기
Todo: 보고서 정확성 표현과 산출물 형식 검증하기; 연구 작업 정리하고 최종 보고서 위치 안내하기
Research round1 andfreshrefinementround2 allreturned; sourceleadconvergenceclosed. NoKoreanefficacyclaim. Formats remainMarkdown+HTML default because asynchronous format question has not received answer.

## Format interview timeout
Userformatquestiontimedoutafter30minutes. ContinueMarkdown+HTMLdefaultwithoutaskingagain. Noformatpreferenceinferredorsavedasuserchoice.

## Concurrent source refresh
Currentprojectinputsupdatedbyotherworkspaceworkduringresearch. LatestsourcefreshKMAAPIHubactual-contributormeans/min50/derivedQC,notolderoriginalQC. Reportandproject-evidenceupdated;24–30annualtraining/regionalweekmonth/currentEMOS/cutoffunchanged. Productionfilesnoteditedbythisresearch. Validitynoteadded:cutoffalonecannotproveactualhistoricalmodelavailability. Ownartifactcitations/gateswillrerunagainstrefreshedMD.

## Final state
Now: 연구 작업 정리하고 최종 보고서 위치 안내하기
Todo: 최종 검증 감시 종료와 프로세스 확인하기
Allreportstatic/layout/pixels/proofreadgatesPASS; finalformatrowsmd/htmldelivered; APIoutcomeverifyOK. All28workers27complete/1retiredcancelled;teams/browsers/profilesclosed. FinalCLIverifyarmedbash_8; afterexit0 recordcleanup, finishmanifest/loop andbriefuser.
Self-review: HEAVY tierheldforresearchjudgment,notproductioncode. Reviewedsource/definition/zero/support/annualunit/score-object/provenanceboundaries; allbindingmethod/QAcriteriaevidenced; no newGloSea6skillclaim. No ulw-plan reviewer gatewastriggered.

## Completed
Now: completed.
Todo: none.
NativeSDKG001/G002/G003checkpointcomplete,9/9criteriapass. Finalqualitygateaccepted
actualcategory:deep-lowAPPROVEandsupportedcurrent-attemptartifacts.29workersterminal,
teams/ownedprofiles/monitorsclosed. Finaloutcomemd+htmldelivered,all4gatesPASS,
0residual;officialbriefing93sources/32domains/97minutes. No morework/polish required.
