# Runnable alternative comparison runner: implementation receipt

Date: 2026-10-07. Owner: st_01a11476. Production runner sources are FROZEN.
The full 6,432-truth / 6,580-input experiment is NOT executed or claimed PASS
by this receipt; root owns stable all-method small, FULL, independent validation
and final science QA.

## Delivered interface

```text
.venv/Scripts/python.exe -B analysis/run_alternative_comparison.py --output outputs/alternative_comparison
```

Callable: `run(root: Path, output: Path, options: RunOptions) -> dict[str, Json]`.
Options: exact comma-separated registry IDs, repeatable case ID, workers 1..6,
seed (default 20261007), resume. Subsets are always SMOKE. Help exits 0;
unknown flags, unknown methods and protected output locations exit 2 before fit.
Nonempty output requires resume.

All 66 registry IDs have real dispatch paths: baseline, classical, Bayesian,
learning/category and joint. Coupling EMOS/BJP sensitivities are separately
named. No failed method receives a forecast substitute. The reporter alone
exports separately named deployable climatology-on-failure policy scores.

Ownership changes: only `analysis/run_alternative_comparison.py`,
`analysis/alternative_runner*.py`, and this receipt.
No git commit, old runner execution, baseline/source/observation/research write.

## Actual serialization and provenance

* Published RAW/QM/QDM/EMOS rows and issued laws are read from protected actual
  artifacts only after exact local annual observation/date/member agreement.
  Published P05/P95 stay unchanged; CONTRACT_P05/P95 identify finite-law inverses.
* Original-unit laws, fitted-model JSON, genuine content-keyed model references,
  numeric version-1 NPZ law shards, actual joint scenario arrays/weights,
  scalar and vector ancestry, partial/full horizons, and component manifests
  are emitted. Scalar/category/analytic-marginal/scenario-marginal surfaces
  remain separate. Existing score_prediction/generate_summaries are unchanged.
* Every input appears in case_inventory.csv; all 148 unavailable targets and
  the 16 latest absent-history IDs remain explicit. Missing targets are not fit.
* Run metadata contains the actual global seed, per-6,580-case availability/
  source-observation/history/selection records, complete evaluated and skipped
  gate receipts, measured timings/cache counts, active daily SHA256, actual
  Python/NumPy/SciPy/Torch versions, source hashes and all 60 protected receipts.
* Fit ledger exposes actual fit_hash, algorithm_version, fixed_parameters,
  used per-method seed (blank for deterministic/reused baseline controls),
  global_seed, convergence, numerical_error and posterior diagnostics.
  model_ref resolves exactly to cache/fits/{fit_ref}.json; complete model data
  are not fabricated or replaced by parameter-grid forecasts.

### Genuine joint ancestry contract

`joint_training_manifest.csv.gz` contains joint_train_hash, source_year,
ordered component_case_ids/row_ids, historical initialization, forecast_means,
observations, cutoff/catalog_cutoff and held_out_years.
`joint_component_manifest.csv` contains the ordered original component LOCAL
training hashes and ordered source_years. The exact delivered aligned_joint
hash is SHA256 of those component hash strings concatenated in order, followed
by repr(source_years tuple). Each component scalar content hash has its own
single-unit training ledger. Mixed-unit joint hashes are never forged into
scalar content hashes. Genuine joint residual folds are exported separately.

## Cache/scheduling contract

Fit/prediction identities include algorithm/version, fixed parameters, actual
accepted training content/dates/ancestry, seed, source/provenance hashes and
actual known target inputs where required. No observed target or score value
is a fit-key field. All Bayesian scalar/vector fits are input-conditioned;
another issued member array cannot reuse a train-hash-only fit.

Proven target-independent reuse is limited to the actual nine pooled
regression/boosting/QRF/neural IDs; category and target-stratified IDR are
excluded. Shared fits serialize once per key. In-memory models are LRU-bounded;
training ledgers stream once per genuine hash, not per method. Input parsing
and pool/count/required-fold caches are run-local over actual immutable inputs,
with fresh content proofs before/after. BLAS environment threads are 1;
Torch neural fits use one thread and a whole-fit RNG lock.

Only BMA min-10 prequential and selected CDF/Tweedie min-15/latest-5 candidates
are scheduled. Fixed pooled/NN/QRF algorithms get no invented CV. Exported
category ancestry comes from actual fitted own-condition labels.

## Guard-safe reporting

Actual tables -> input/protected/source guards -> PREDICTIONS_COMPLETED ->
real generate_reports API -> canonical top-level report table copies ->
final source/protected guards -> COMPLETED.
FULL only then refreshes the real completed report once more and guards again;
the reporter's run_completed predicate remains COMPLETED-only. This second
real report invocation has additional report CPU cost but avoids promoting
pending runs or writing a stub manifest.

A source change writes FAILED_SOURCE_CHANGED, exit code 2, actual partial
counts, before/after hashes, changed paths and timing; it does not leave RUNNING
or claim successful completion. Reporting failure is likewise terminal.
Source tracking intentionally covers ALL analysis/*.py (including production,
runner, reports, validation and audit owner paths), plus the frozen plan/schema.
Root must freeze these dependencies before the binding FULL run.

## Executed evidence

Native commands, both clean:

```text
.venv/Scripts/python.exe -B -m ruff check analysis/alternative_runner*.py analysis/run_alternative_comparison.py
.venv/Scripts/python.exe -B -m basedpyright analysis/alternative_runner*.py analysis/run_alternative_comparison.py
```

Ruff PASS; basedpyright 0 errors, 0 warnings, 0 notes. Helpers are below 250
nonblank/noncomment lines. Best-effort LSP fluctuated between no errors and
namespace-import resolution errors; native project-venv checks are authoritative.

### FINAL actual metadata readiness pilot (not an old source-changed pilot)

```text
.venv/Scripts/python.exe -B analysis/run_alternative_comparison.py --output outputs/alternative_runner_metadata_ready_smoke --methods RAW,QM,QDM,EMOS,climatology_empirical,bjp_niw --case-id 20220307_1MON_W01_t15m --workers 1
```

Monitor mon_K1KD3N51G0C087DP / bash_50. Actual terminal summary:
COMPLETED, SMOKE, 6 continuous rows, seed 20261007, 6,580 case records,
6 gate receipts, Python 3.13.13, elapsed 66.93589330000032 seconds.
Actual active daily SHA256:
30aae6da5e383bfcadf4e8e652e0b58654828fab95333b07c8f0d55052512747.
All 60 protected hashes before/after match; source guard passed.

Independent functions executed on this exact pilot:

* metadata_checks: PASS, 6 genuine cache identities, 19,664 paired-comparison
  rows and 105 nonempty masks.
* summary_checks: PASS, 5 tables and 30 groups.
* ancestry_checks: PASS, 24 actual rows, 1 scalar training hash.
* Genuine model references dereferenced; baseline seed blanks are deliberate
  non-RNG reuse, BJP actual derived seed is 4178644591.

### Earlier actual surface and cache evidence

* outputs/alternative_runner_smoke_scalar_final: COMPLETED/SMOKE, 152.4812942s,
  36 continuous +2 category predictions, 38 OK /9 domain mismatches /1 gate,
  no fit/score failures. All 36 laws decoded; 8 published baseline rows matched
  exact CSV strings for observed/mean/CRPS/P05/P95/probabilities/Brier/RPS;
  category-only fields had no invented continuous values. 224 genuine
  own-condition category-label ancestor records.
* outputs/alternative_runner_smoke_monthly_final: COMPLETED/SMOKE, 121.4934964s,
  5 continuous +8 joint predictions, real Bayesian rain transforms and
  separately named EMOS/BJP Schaake variants.
* The first weekly OT/MBC caller pilot surfaced INVALID_FIXED_MARGINAL_METHOD
  because an empty coupling setting was passed to non-coupling algorithms.
  Repaired caller passes the untouched non-coupling specification.
  outputs/alternative_runner_smoke_joint_repaired produced 14 genuine scored
  joint rows across dimensions 2/6/8/12/16, then correctly terminated
  FAILED_SOURCE_CHANGED after an import-format edit; it is NOT the final
  source-stable completion claim. Root's independent readiness audit verified
  its six genuine joint hashes and 84 joint residual folds.
* outputs/alternative_runner_final_ready_smoke, mon_21WV7EHTNHTDQK2F/bash_44:
  actual COMPLETED/SMOKE exit0, 71.3730879s, 10 original baseline/climatology
  continuous rows plus14 genuine scored joint rows. This source-stable
  both-product caller/report-export proof preceded the final metadata additions;
  the final schema-preflight authority is the metadata_ready_smoke above.
* Root validator's independent four authentic-fixture audit: 18.9540104s,
  grouped coverage/paired masks and genuine scalar/joint ancestry PASS,
  five actual artifact corruptions rejected; every SMOKE was rejected by the
  FULL inventory gate. No weakening of hashes, counts or FULL-vs-SMOKE rules.
* Actual maximum weekly-rain pool scheduling:
  outputs/alternative_runner_cache_profile/profile.json,
  20260831_1MON_W01_prcp, 45,756 pooled rows, 54 scalar/category schedule tasks,
  0.8165973s, two required-fold and two count-cache entries.
  Known-input changes changed BJP fit keys; held-out truth sentinel 1e9 changed
  scores but not the law/key; worker 1 vs6 laws were identical.
* Explicit adversarial source-hash fixture, on a real climatology forecast:
  outputs/alternative_runner_guard_qa, FAILED_SOURCE_CHANGED, exit2,
  one real partial continuous row and all60 protected after-receipts.
  The injected marker was clearly QA-only, not a claimed source hash.
* Personally inspected actual score_1mon_9a3f6c9b03_CRPS.png: SMOKE title,
  original degC units, success-only label, per-method N=1 and coverage warning.

## Handoff

Production runner is callable, actual-data exercised, metadata-preflight
clean and FROZEN. Independent validator/report owners retain their exclusive
files; reporter predicate was not broadened. Parent owns stable all-method
small and the first binding FULL run/validation. No FULL artifact PASS,
new skill ranking or full scientific completion is asserted here.
