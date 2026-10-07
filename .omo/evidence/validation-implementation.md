# Independent validation implementation

## Saved analytic joint marginal identity repair: FINAL FROZEN

The subsequent genuine `duplicate saved law` failure is repaired. Distribution
exports with a `joint_id` are not scalar aliases: their exact identity is
`(joint_id,case_id,method_id,fit_ref)`. Every such law must exactly match the
separate `joint_analytic_marginals.csv.gz` table, an actual component of its joint
prediction, the same parent fit reference, and an OK fitted method matching that
parent. Actual duplicate objects, absent laws, foreign components and mismatched
fit identities fail. Scalar `(case_id,method_id)` coverage remains exact, with
additional saved-law/score fit-reference equality. Joint-only fixtures are valid
saved-score inputs with zero scalar laws, not a fabricated continuous surface.

Both surfaces execute the same original-unit law audit: independent CDF endpoints
and the entire interior quantile grid; finite monotone CDF/quantiles and left
generalized inverse; independent mean and CRPS; both tercile CDFs; saved P05/P95;
nonnegative rain support; category probabilities, Brier/RPS and empty middle
category when thresholds tie. Existing mathematical tolerances are unchanged.
Original RAW/QM/QDM linear interval conventions and separate CONTRACT quantiles
remain untouched. No law is discarded to evade the duplicate check.

Literal final command:

```text
.venv/Scripts/python.exe -B -W error -m analysis.alternative_validation_marginal_audit
```

**Exit 0**, `status=PASS`, `scope=ACTUAL_SAVED_SCORE_SMOKE_NOT_FULL`,
elapsed **10.974761900000885 seconds**, `read_only=true` (actual fixture byte
sizes and modification times unchanged). Numerical warnings are errors.

|Authentic fixture|All laws|Scalar laws / scores|Analytic joint marginals|Category scores|Energy/variogram rows|Hot/dry rows|
|---|---:|---:|---:|---:|---:|---:|
|alternative_runner_smoke_scalar_final|36|36 / 36|0|2|no joint rows|no joint rows|
|alternative_runner_smoke_monthly_final|57|5 / 5|52|0|8|2|
|alternative_runner_smoke_joint_final|8|0 / 0|8|0|1|0|

All 60 analytic joint marginals are independently scored, including identical
case/method pairs issued for different joint IDs. Actual `joint_score_checks`
passes both monthly and joint fixture energy, variogram and supported event
scores. Eleven deterministic corruptions of actual exports are rejected:
duplicate/missing/wrong-fit laws; wrong CRPS/mean/P05/tercile probability;
foreign component/fit and duplicate score row; positive middle mass at tied
thresholds. The correct tied-threshold zero-middle case passes. No fixtures,
runner/reporter files, physical observations or baseline artifacts were edited.

Native final command:

```text
.venv/Scripts/basedpyright.exe analysis/alternative_validation*.py analysis/validate_alternative_comparison.py
```

**Exit 0: 0 errors, 0 warnings, 0 notes**. Final validator-wide Ruff:
**All checks passed!** LSP again had its known namespace-only missing-import
false positives on the newly added analytic module; native project checking
resolves these without suppressions. No additional actual numerical/export
defect was found in this requested replay.

Root reports its separately verified final metadata-ready smoke is completed
and schema-authoritative. This lane does not rewrite the older fixtures to gain
those metadata fields, does not claim FULL, and does not await FULL. The optional
scenario-projection-table expansion was dropped to honor the surgical freeze;
it is not a missing analytic-law or requested joint-score check.
**All validation source edits are now FINAL FROZEN.** Root must take a fresh
all-analysis source guard snapshot before its next stable small/all-method/FULL
execution. No additional panels, refactoring or unrelated repairs are planned.

## Authentic smoke readiness repair receipt (subsequent root resume)

Both new validator-owned blockers are repaired without runner/reporter edits.
Coverage is recomputed independently by `PRODUCT,VARIABLE,method_id,surface`,
including absent-case UNRECORDED states, actual target availability, scientific
support/domain gates, eligible IDs, score presence and SHA256 success masks.
Scalar component coverage is not substituted for genuine joint-key statuses.
Actual report fields are `scientific_gates,missing_targets,fit_failures,
numerical_or_score_failures,scored_count,status_counts`, not obsolete method-global
`ok_count` fields. FULL inventory/case-universe checks remain binding.

Joint content hashes independently replay the actual `aligned_joint` wire:
SHA256 of ordered component LOCAL training-hash strings followed by
`repr(tuple(sorted(source_years)))`. Every component hash is independently
recomputed from its original scalar rows. Ordered case/row source links, complete
annual intersections, original observations/ensemble means, cutoff/catalog and
whole-vector alignment are checked. Genuine joint folds independently replay
SHA256 of `"|".join((outer_joint_hash,pseudo_init,*training_row_ids))`, with
whole-year source/valid holdouts and chronological ancestors. No arbitrary
nonempty hash string is accepted. Successful vector fits now reference verified
joint manifests rather than incorrectly requiring their hashes in scalar pools.
All three joint manifest files are now required full-artifact inputs.

Literal command, personally executed without fits, FULL, or fixture writes:

```text
.venv/Scripts/python.exe -B -m analysis.alternative_validation_readiness_audit
```

Exit **0**, `status=PASS`, `scope=AUTHENTIC_SMOKE_READINESS_NOT_FULL`,
elapsed **18.954010400000698 seconds**. Actual captures:

|Authentic output suffix|Scalar rows / hashes / folds|Genuine joint hashes / folds|Coverage groups|Paired rows / nonempty|
|---|---:|---:|---:|---:|
|alternative_runner_smoke_scalar_final|432 / 4 / 224|0 / 0|216|19664 / 1902|
|alternative_runner_smoke_monthly_final|288 / 12 / 0|4 / 0|224|19700 / 84|
|alternative_runner_smoke_joint_final|384 / 16 / 0|3 / 0|225|19715 / 0|
|alternative_runner_smoke_joint_repaired|672 / 28 / 0|6 / 84|UNAVAILABLE|UNAVAILABLE|

The repaired joint pilot is guarded `FAILED_SOURCE_CHANGED` and has no report
exports; its genuine ancestry passes, not its overall run. The regression rejects
five deliberate corruptions of real exports (grouped score count, joint content
hash, component hash, original observation, foreign row). All four authentic
SMOKE fixtures still fail full inventory validation; none is promoted to FULL.
In-memory corruption seams retain real export decoding and source replay.

Actual paired tables now use uppercase PRODUCT/VARIABLE, JSON `methods`,
`mask_kind,surface,method_id,score,N,mask_hash,mean_loss,
delta_first_minus_second`. All original-unit loss means/deltas and exact common
masks are independently recomputed, including empty masks. Joint variable scope
is reconstructed from actual component case IDs, not guessed from scalar fields.
Persisted `model_ref` is accepted only at the exact
`cache/fits/{fit_ref}.json` path; its actual file must match fit_ref/train_hash
and contain a model object. Embedded `model_spec` remains a valid representation.

Native validator-wide basedpyright: exit **0**, **0 errors, 0 warnings, 0 notes**.
Ruff validator-wide: **All checks passed!**. LSP initially reproduced its known
namespace-resolution false positives on coverage; native project diagnostics are
the decisive receipt. A real import cycle found by native checking was repaired
by extracting the independent scalar wire replay, not suppressed.

Exact remaining runner-owned readiness fields were sent to `st_01a11476`.
Actual preflight on `outputs/alternative_runner_final_ready_smoke` exited **1**:

```text
AssertionError: run summary: missing metadata ['cache_counts', 'case_statuses', 'gate_receipts', 'seed', 'timings']
```

These values must be scientifically complete, not dummy aliases. Subsequent
requirements remain active observation `daily_sha256`, dependency `python`, and
fit ledger `fit_hash,algorithm_version,fixed_parameters,seed,
posterior_diagnostics,convergence,numerical_error`. Root reports runner is adding
these fields; no claim is made that historical smoke exports were updated.
Seed/hash/source/ancestry/posterior gates are not waived. Full execution,
full SC2 and final-report QA remain root-owned and unrun in this narrow resume.

The read-only interface is `validate(root: Path, output: Path) -> dict[str, Json]`.
The CLI alone writes `output/validation.json`. Missing helpers and saved artifacts
are reported UNAVAILABLE/INCOMPLETE, never PASS. Exit zero requires full coverage.

## Runner schema coordination required

Section 10 gives filenames but not field names. The implementation currently
requires lowercase identity/provenance fields and unchanged uppercase scoring
fields. These are explicit checks, not guessed successful validation:

- JSONL law: `case_id`, `method_id`, `fit_ref`, `distribution` (tagged law object).
- Continuous CSV: `case_id`, `method_id`, `variable`, `fit_ref`, plus unchanged
  `OBS,Q33,Q67,PRED_MEAN,CRPS,P_BN,P_NN,P_AN,P05,P95,BRIER,RPS`.
- Baseline finite laws additionally `CONTRACT_P05,CONTRACT_P95`; original
  baseline linear-quantile P05/P95 are not overwritten.
- Inventory: `method_id,family_no,surface`.
- Status: `case_id,method_id,status,reason_code,surface`.
- Fit: `method_id,status,train_hash`.
- Training: `row_id,train_hash,source_case_init,source_year,hist_start,hist_end,
  cutoff,catalog_cutoff,held_out_years,product,variable,year_weight`.
- Fold: `fold_id,training_row_ids,validation_row_ids,pseudo_init,held_out_years,
  ancestor_hash,outer_train_hash,catalog_cutoff`.
  Lists are JSON arrays; held-out years are integer arrays.
- Failure policy: `method_id,policy,eligible_count,scored_count`.
- Joint: `joint_id,method_id,scenario_key,units,approximation_metadata`, with
  corresponding 2D finite-array key in `joint_scenarios.npz`.

The independent SC2 CDF reference uses SciPy tagged-law reconstruction,
O(n²) empirical expectations, and separate quadrature. It does not copy saved
scores or rely solely on production formulas. Its functions are
`reference_cdf`, `reference_mean`, `reference_crps` in the owned reference module.

## Executed evidence and terminal lane result

This lane is code/readiness complete; **full experiment validation is pending**.
No full SC2 PASS or new-method skill result is claimed. The root owns the future
full-artifact run. There is no waiting dependency on the runner.

The binding command genuinely executed:

```text
.venv/Scripts/python.exe -B analysis/validate_alternative_comparison.py --output outputs/alternative_comparison
```

Measured receipt: elapsed **18.5525487 seconds**, exit **1**, `status=FAIL`,
`full_experiment_validated=false`. Of 18 check groups: 15 PASS, two FAIL, and
`full_saved_artifacts=UNAVAILABLE` (23 expected files absent). All 60 protected
files matched SHA256 and byte size both before and after. The complete machine
capture is `outputs/alternative_comparison/validation.json`.

### Actual defects found outside this lane's edit scope

1. `analysis/alternative_training.py:inner_folds` leaves a validation
   SOURCE_YEAR in the pooled ancestors when a historical monthly window crosses
   New Year. The executable `crossing_fold_checks()` creates December
   pseudo-issuances and an earlier-month pooled condition. Actual failure:

   ```text
   cross/prequential/2005: validation SOURCE_YEAR=2005 retained pooled rows
   ['early:validation:2005:0']; held_out_years=(2006,)
   ```

   This check implements section 2.3's whole validation source/valid-year block.
   The outer original-case catalog remains frozen at the actual outer issuance;
   it is NOT tightened to historical pseudo-issuance. Root must repair the
   SOURCE-year exclusion and replay/hash the same fold exclusions, or explicitly
   reconcile this rule with the frozen contract. This lane did not edit data code.

2. `analysis/alternative_distribution_base.py:153` evaluates a latent
   Gumbel CDF for negative physical rain before applying the censor mask.
   Four `RuntimeWarning: overflow encountered in exp` warnings were captured
   from SciPy `_continuous_distns.py:3437`. All 22 mathematical distribution
   fixtures passed their numerical assertions; the warning still fails the
   enclosing check, rather than being suppressed or mislabeled clean.
   Independent minimal reproduction, actually executed (exit 1):

   ```text
   .venv/Scripts/python.exe -B -W error -c 'import numpy as np; from analysis.alternative_distributions import censored_gev; print(censored_gev(1.,2.,0.).cdf(np.array([-10000.])))'
   ```

   The traceback reaches `ScientificLaw.cdf` at line153 and the SciPy overflow.
   This lane did not edit the distribution owner's files.

### Real oracle results

- Known Normal CRPS at zero: `0.23369497725510913`.
- Normal mixture CRPS: `0.7343976021023053`; the incorrect averaged component
  CRPS is `1.4527918216859033`.
- Tied weighted empirical mean/CRPS at observation1: `2.6 / 1.06`.
- CSG mean: `4.54897994784475`; hurdle mean: `4.2`; square/cube censored
  inverse means: `50 / 79.78845608028655`, demonstrating Jensen's distinction.
- Tweedie powers1.2/1.5/1.8: actual CDF, atom, density convolution, variance
  survival integration, and mass/first-moment truncation bounds checked.
  p1.5 atom: `0.17692120631776423`, exact mean3.
- NIW/NIG/MNIW independent matrix calculations passed; 65,536 independent
  SciPy inverse-Wishart posterior draws gave CDF `0.8326850377876538` versus
  exact conditional-t `0.8328590283026712`, MCSE `0.0004946020638841315`,
  importance ESS `60273.20619285162`, conditional df14 and scale-SD
  `0.9071577407871845`.
- Correlated two-zero Gaussian rectangle: `0.39758361765043326`, not the
  independent product0.25. IID R-hat/ESS passed; separated chains had
  R-hat `2.6984837096415246`; sticky chains bulk ESS `257.88692408382775`
  failed the required convergence limits.
- Bayesian temperature/sqrt/YJ/log-sinh independent inverse means and CRPS
  passed. `exp(Student)` divergent positive moment is an explicit counterexample;
  an inverse Student square with df2 is actually rejected.
- Exact Fisher scaling, independent constrained-isotonic solution, coherent
  ordinal/ELR empty middle categories, all-wet finite occurrence fit passed.
- QRF's 64 stored trees were replayed independently: every leaf's source-year
  bootstrap membership and normalized masses were checked; its issued CDF and
  CRPS match the independent leaf mixture. Actual synthetic QRF mean/CRPS:
  `2.685768224830725 / 0.5038080554549313`. IDR: `2.5 / 0.25`.
- Real classical dispatch calls: one-positive-year hurdles return
  `INSUFFICIENT_TRAINING/FEWER_THAN_THREE_POSITIVE_YEARS`; Gamma with zeros
  returns GATED_DATA; negative rain returns INPUT_CONFLICT; constant predictor,
  zero spread and M1 successfully fit unit-slope MOS, mean
  `2.850000028501236`, CRPS `0.5981160742846204`.
- Held-out truth sentinel1e12, five excluded-row perturbations, actual refits,
  worker config1/6 and input-order hashing passed. Ten valid historical folds
  retain 2022-vintage original cases under the outer-frozen catalog. Empty pool
  fails explicitly; a missing joint annual component leaves exactly19 complete
  years without imputation.
- Finite coupling preserves exact marginal multisets/empirical CRPS;
  analytic-to-finite Normal CRPS difference `0.0015223944238377252` is nonzero
  and labeled. Duplicate/disjoint physical IDs fail. Independent/correlated
  scenario correlations `0.0032289371937385203 / 0.4992337568816802` reflect
  the prescribed half-shrunk PIT-residual dependence; Sobol256/512 are nested.
- MBCp/MBCr/MBCn independent out-of-sample saved-composition replay passed,
  respectively41/42/92 operations and three probes.
- OT brute-force assignment optimum1.25; independent rectangular monotone
  plan cost0.8; full dynamic final-plan cost4.0. Historical blocks are
  1990-1999 /2000-2010. Changing only recent observations to1e12 gives
  byte-identical dynamic transport. Pairing-blindness counterexample passed.
- Prototype CSV/JSON roundtrips passed and seven deliberate schema/score
  corruptions were rejected. The saved training wire prototype replays actual
  adapter hash `76f7c0488e4469796bc310b07fde2677059d689727addbfb7da24e04e6731c0c`.
  It is explicitly `SYNTHETIC_SCHEMA_ONLY_NOT_FULL_EXPERIMENT`.

SC2 expected JSON numbers are produced by the independent reference module,
not copied from production score rows. Full saved-score checks will recompute
every original-unit score and record independent reference examples/source hash.
The frozen inventory contains **61 required IDs across all17 families**;
baselines/climatology and explicitly named coupling variants are additional.

### CLI and read-only manual QA

Actually executed: `--help` exit0; `--invalid` exit2 with
`unrecognized arguments: --invalid`; `--output outputs` exit2 with
`output must be a new child directory of outputs`. Neither invalid invocation
fits or writes. The binding CLI writes only its own new `validation.json`.

Actual read-only library driver:

```python
from pathlib import Path
import json
from analysis.validate_alternative_comparison import validate
root = Path.cwd()
out = root / "outputs/alternative_comparison"
before = {str(p): (p.stat().st_size, p.stat().st_mtime_ns)
          for p in out.rglob("*") if p.is_file()}
result = validate(root, out)
after = {str(p): (p.stat().st_size, p.stat().st_mtime_ns)
         for p in out.rglob("*") if p.is_file()}
assert before == after, "validate wrote artifact bytes/mtime"
print(json.dumps({"read_only": True, "status": result["status"],
                  "elapsed_seconds": result["elapsed_seconds"]}, indent=2))
```

Run with `.venv/Scripts/python.exe -B -c` and the quoted driver.
Actual capture: `read_only=true`, `status=FAIL`, elapsed24.2543033seconds
(the captured production warning; no output bytes/mtime changed).

Root repaired the shared Bayesian factory's `kind=bayesian_scalar` dispatch.
I inspected that implementation and personally executed:

```text
.venv/Scripts/python.exe -B -m analysis.alternative_distribution_bayes_audit
```

Actual capture: `{"status":"PASS","restored_laws":4,
"elapsed_seconds":1.6429442999979074}`. This covers scalar T/P and nested
Normal/Bayesian mixtures via JSON -> this lane's decode/mapping -> the repaired
shared factory. The validator now delegates reconstruction to that factory.

Ruff command, actually PASS:

```text
.venv/Scripts/ruff.exe check analysis/alternative_validation*.py analysis/validate_alternative_comparison.py
```

Native basedpyright command covers the same complete owned scope. LSP initially
misresolved the `analysis` namespace; native project diagnostics are decisive.
Final native diagnostic receipt: **exit0, 0 errors, 0 warnings, 0 notes** for
`.venv/Scripts/basedpyright.exe analysis/alternative_validation*.py analysis/validate_alternative_comparison.py`.
All helpers stay below
250 pure LOC. No environment mutation, git operation, baseline/data edit or
foreign-lane edit was performed; short monitor commands terminate normally.

## Full-artifact proof requirements / schema coordination

The root accepted the basic wire fields above. Continuous rows also retain
uppercase `CASE_ID,METHOD,VARIABLE,PRODUCT,INIT_DATE,VALID_START,VALID_END,LEAD,
N_TRAIN`, plus `SEASON,YEAR,VALID_MONTH` required by unchanged generate_summaries.

**Required supplemental metadata discrepancy:** section9/10/11 content-hash and
posterior proof cannot be reconstructed from the initial minimal ledger columns
alone. Current executable full checks also require:

- Training raw identity/value fields: `source_case_id,source_init,lead,observation,
  member_keys,source_files,provenance_hash,archive_era,ensemble`.
  Arrays/lists are JSON wire values; this is sufficient to independently replay
  the frozen mechanical training-content hash.
- Fit computation receipt: `fit_hash,algorithm_version,fixed_parameters,seed,
  posterior_diagnostics,model_spec,convergence,numerical_error`.
- Run summary keys: `active_provenance,config,dependency_versions,seed,
  protected_hashes_before,protected_hashes_after,expected_registry_entries,
  attempted_registry_entries,completed_registry_entries,case_statuses,timings,
  cache_counts,gate_receipts`.
- Paired masks: `method_a,method_b,product,variable,mask_hash,n_pairs,delta_crps`;
  mask hash is SHA256 of JSON compact encoding of sorted common-success case IDs.
- Coverage: `eligible_count,ok_count,failure_count,gate_count,target_unavailable_count`.
- Joint original-unit score metadata additionally `weights_key,observations,centers,
  scales,variables,thresholds,ENERGY,VARIOGRAM,HOT_DRY_P,HOT_DRY_BRIER`.
- All five unchanged metrics CSVs, not merely their filenames being mentioned.

Missing required proof is an explicit failure/incompleteness, never fabricated
SC2 PASS. Root may provide these as additional columns/metadata while retaining
the accepted basic schema; otherwise the mismatch needs reconciliation before
full validation. No full artifact check, complete real-case/all-subtype run,
report/plot manual QA, or full saved performance comparison was executed here:
those artifacts were absent. Original tight QDM warnings are retained separately,
and original analytical EMOS is never discretized to scenario quantiles.
