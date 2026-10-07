# Verification economics
기존 전체 파이프라인 재실행은 생산 변경 없는 문헌 조사에 불필요하다. 메커니즘 합성 검증은 성능 검증이 아니다.
각 proof decision: claim, risk, error cost, verification cost/time, chosen path, defer/verify, outcome, residual risk.

|claim|risk|error cost|cost|chosen path|decision|outcome|residual risk|
|---|---|---|---|---|---|---|---|
|Fixed Joint Gaussian conditional is linear with Schur variance|normal|misdescribe BJP vs EMOS|one eval cell|independent Schur arithmetic|verify|PASS verify-mechanisms.md|does not test fit/posterior|
|Reorder does not improve marginal empirical CRPS|normal|wrong recommendation objective|same cell|actual pairwise CRPS on two orderings|verify|PASS|dependence template skill unknown|
|Naive log rain has zero singularity|normal|invalid preprocessing|same cell|Math.log(0), censor output|verify|PASS|actual zero occurrence not counted here|
