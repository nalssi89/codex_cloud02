# JOINT implementation and executable evidence

Date: 2026-10-07. Scope: frozen design section 8, families 15 and 16 except
Bayesian-owned MBJP. This is implementation/representative-input evidence, not
the root experiment's full-comparison completion or a skill claim.

## Interfaces and IDs

`analysis.alternative_joint.fit_joint(spec, training, residuals, config)` returns
`JointFitResult`; `predict_joint(model, targets, marginals, config)` returns the
actual weighted `JointPrediction`. All target arguments are truth-free CaseInput.

Implemented IDs: `schaake_window`, `schaake_block`, `ecc_q`,
`decc_path_shrunk_error`, `residual_gaussian_copula`, `mbcp_annual`,
`mbcr_annual`, `mbcn_annual`, `otc_annual`, `dotc_annual`.

Coupling uses `spec.fixed_parameters["marginal_method"]` equal to `emos`
(default) or `bjp`; output IDs have explicit `__emos`/`__bjp` suffixes.
`schaake_block` at a single T/P window declares an exact `schaake_window` alias
in prediction metadata. Whole-year path rows are retained, never sampled
independently by coordinate. Analytic marginal laws are NOT replaced by finite
scenario CRPS; metadata declares the quantile discretization and its mean error.

Residual wiring:

```python
from analysis.alternative_joint_residuals import generate_residuals
from analysis.alternative_joint_marginals import fit_bjp_marginal, fit_emos_marginal

residuals = generate_residuals(
    joint_training, config,
    method_id="residual_gaussian_copula",
    marginal_fitter=fit_bjp_marginal,  # omit for original analytic EMOS
    marginal_method="bjp",           # default "emos"
    randomization=0,                # fixed primary; all four are stored
)
```

The callback signature is `(TrainingSet, FitConfig) -> FittedModel`.
For MBC, use its actual method ID; every eligible ancestor refits the ENTIRE
correction. `fit_joint(..., residuals=None, ...)` generates the prescribed
residuals automatically, including fixed BJP when requested.
`PITResidualSet` extends the shared frozen ResidualSet with four stored uniform
arrays, four normal-score arrays and clipping counts. Generic pit-normal arrays
without those diagnostics are rejected. Each whole-year vector retains an
exact FoldSpec; supplied ancestry is checked against reconstructed past folds.
Historical pseudo-issues tighten response dates and held-out years, while
`catalog_cutoff` remains the actual original-case outer issuance. This is NOT
proof that 2022-vintage reforecasts were released in historical real time.

Frozen maps expose `fit_map`, `FrozenMap.apply`, `to_spec`, `map_from_spec`.
Transport exposes `fit_ot`, `FrozenTransport.predict`, `to_spec`,
`transport_from_spec`; all three dOTC plans, full positive-path composition,
projected probability mass and exact row/column residuals are serialized.

## Numerical decisions

All transfer coordinates are T in degC and sqrt(P/100 mm), transforming annual
means first. Inversion is AFTER whole-vector residual addition; negative rain
latents are censored BEFORE squaring. No response-dependent transport metric.
MBCp has 20 Pearson recolor/remap iterations, MBCr has 20 rank-space iterations
and a final observed-quantile map, MBCn has 30 fixed Haar rotations and a final
marginal map. Source ties have merged midpoint knots and constant endpoints.

OTC uses true squared-distance balanced assignment, deterministic bounded
perturbation and lexicographic optimal-face resolution. Prediction averages the
three nearest source conditional rows EVEN at exact matches. dOTC sorts two
historical blocks, composes every positive P*R/a path, projects/merges atoms,
then solves the FINAL recent-source to synthetic-target balanced plan.
Rectangular/nonuniform plans use HiGHS LP, primal tolerance <=1e-9.

G3 is closed for actual data, so ECC/dECC return `GATED_DATA` with
`G3_PHYSICAL_IDENTITY_UNPROVED`. Structural MEMBER labels cannot open it.
Their real keyed/permutation implementations were executed using explicit
synthetic physical-identity evidence, not presented as source-data proof.
G6 requires >=20 complete annual years and an explicit receipt or a single
nonempty archive cohort from one original-case vintage. No current issued
ensemble is ever treated as a climate-period block. G7 future-climate claims
are not made.

## Executed mathematical and library checks

Commands from repository root:

```text
.venv/Scripts/python.exe -B -m analysis.alternative_joint_coupling_audit
.venv/Scripts/python.exe -B -m analysis.alternative_joint_transport_audit
.venv/Scripts/python.exe -B -m analysis.alternative_joint_audit
.venv/Scripts/python.exe -B -m analysis.alternative_joint_audit --actual
.venv/Scripts/python.exe -B -m analysis.alternative_joint_audit --help
.venv/Scripts/python.exe -B -m analysis.alternative_joint_audit --invalid
.venv/Scripts/basedpyright.exe analysis/alternative_joint*.py
.venv/Scripts/ruff.exe check analysis/alternative_joint*.py
```

- Native basedpyright: **0 errors, 0 warnings**. Ruff: **all checks passed**.
  LSP was run first; its transient namespace-import failures were distinguished
  from the decisive project-native results.
- Coupling multiset, tie/shuffle, censor-before-square, duplicate physical-ID
  rejection and complete annual ancestry checks passed. Invalid in-sample
  ancestry is rejected. There are 14 past-only residual years for the 24-year
  synthetic case. Copula minimum eigenvalue: **0.7576554372119075**.
- Finite-law CRPS is invariant under rank permutation to 1e-14, while its
  analytic censored-Normal CRPS difference is explicitly **nonzero**; both
  assertions passed in the final coupling audit.
- All four atom transformations are stored. A known censored Normal atom
  independently verifies `u=0.5*v` to 1e-14; three atom years differ between
  randomizations. A deliberately overconfident EMOS synthetic fixture clips
  three atom PITs to 1e-12; this is recorded, NOT hidden or used for tuning.
- Changing the last historical response by +1e6 leaves every earlier MBC
  prequential residual **exactly identical**. This checks actual whole-map
  refitting, not merely a string-based ancestry assertion.
- Sobol 256/512 sequences have exactly identical first 256 scenarios.
  Independent/correlated constructions differ. All three MBC saved-map
  out-of-sample replay errors are **0.0**. Prefix/full MBCn rotations match
  exactly. Tied and constant-source mapping oracles passed.
- Known assignment objective: **2.5**. Independent exhaustive 5! permutation
  oracle: **2.2439292684260246**. Rectangular unequal-mass constraints,
  lexicographic ties, and nearest-three-at-exact-match checks passed.
- dOTC 24-year case: 12 synthetic atoms, mass 1, final row/column residual 0.
  Odd 25-year case: **24 synthetic atoms**, mass 1, final row error 0,
  column error **1.3877787807814457e-17**. The split-mass case exercises full
  composition rather than a barycentric or single-assignment substitute.
  Altering all recent observations by +1e6 leaves plan/support identical.
  Projected duplicate atoms merge to one atom of mass 1. Frozen replay passed.
- Synthetic fit/predict entry-point QA: **3.889031 seconds**, exit 0.
  Both 2D and 4D cases execute every eligible ID; synthetic G3 evidence also
  executes ECC/dECC. Worker-count replay is identical.
- Help exits 0. Unknown `--invalid` exits 2 with an explicit argument error
  before fitting. No files are written by these audit executables.
- Independent protected-file receipt: **60/60 hashes and byte sizes unchanged**.
  All 15 owned executable modules are below 250 pure LOC (largest 168 at
  measurement). The root-owned `alternative_joint_data.py` was not edited.

## Actual-input evidence

Actual pair, single-variable paths, combined full paths and available partial
paths were fitted using the original catalog and active historical observations.
The final measured run exited 0 in **64.6444633 seconds**, including catalog
loading, original outer EMOS fits, all strict inner marginal/map refits,
prediction, 512-scenario sensitivity, and deterministic replay assertions.
BLAS/OpenMP thread limits were 1:

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/Scripts/python.exe -B -m analysis.alternative_joint_audit --actual
```

All ten joint keys produced **8 OK + 2 G3-gated outputs** each, with zero
unexpected failures. The three fixed-BJP coupling outputs on the monthly pair
were also OK. This is 83 issued outputs and 20 explicit gates, including the
declared Schaake aliases; aliases are NOT extra independent experiments.

|Actual key|Dimension|Annual years|Copula seconds|MBCp|MBCr|MBCn|OTC|dOTC|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|20220307 1MON W01 T/P|2|24|0.616176|0.272686|0.187032|0.192082|0.031392|0.006718|
|20220307 1MON W01-W08 T path|8|24|1.255727|0.362555|0.341083|0.480823|0.011145|0.010361|
|20220307 1MON W01-W08 P path|8|24|1.384269|0.370061|0.322451|0.472860|0.045018|0.012011|
|20220307 1MON combined full path|16|24|2.909911|0.631722|0.530184|0.870454|0.022313|0.018653|
|20260831 1MON W01-W05 partial combined|10|30|2.405096|0.515223|0.436210|0.610661|0.014359|0.015219|
|20220307 3MON M01 T/P|2|24|0.305581|0.166393|0.139723|0.156965|0.005195|0.004321|
|20220307 3MON M01-M06 T path|6|24|0.722088|0.247585|0.217844|0.265728|0.007335|0.010609|
|20220307 3MON M01-M06 P path|6|24|1.004897|0.247526|0.230097|0.436855|0.008271|0.011104|
|20220307 3MON combined full path|12|24|2.042331|0.503094|0.432832|0.608852|0.012994|0.015350|
|20260831 3MON M01 partial combined|2|30|0.410631|0.222957|0.241991|0.233909|0.011018|0.008162|

Schaake window/block execute in 0.002608-0.020024 seconds per recorded call
in this run. Each row's times include fit plus two issued predictions (the
second has a changed worker count), while original outer marginal fits occur
before the timed loop. This is measured representative cost, not a full-run
CPU-hour estimate.

24-year cases use 14 prequential residual years, 2003-2016; 30-year cases use
20, 2003-2022. MBC scenarios retain one of these complete annual residual
vectors each. OTC/dOTC issued three support atoms in these particular real
keys, but the odd-block adversary above proves nonuniform/split-mass handling.

Fixed-BJP monthly-pair execution (component order P then T):

|ID|Fit seconds|Issued P mean mm|Issued T mean degC|
|---|---:|---:|---:|
|schaake_window__bjp|0.001440|107.92538713|11.99670444|
|schaake_block__bjp (declared alias)|0.003014|107.92538713|11.99670444|
|residual_gaussian_copula__bjp|0.049886|109.17760319|11.98090497|

### Saved QQ evidence: prequential marginal normal scores

The following are diagnostic QQ coordinates, NOT evidence of calibration or
Gaussianity. Reference column is Phi^-1(p); empirical columns are linear sample
quantiles of strict prequential randomized-PIT normal scores. No verified
target appears in their construction. Rain and temperature are distinct
columns, not averaged units.

|p|Normal reference|20220307 weekly W01 rain|Weekly temperature|20220307 monthly M01 rain|Monthly temperature|
|---:|---:|---:|---:|---:|---:|
|0.05|-1.64485363|-1.06241341|-2.11561868|-0.45226853|-1.18209315|
|0.25|-0.67448975|-0.15912013|-0.72202827|0.00598095|-0.77800919|
|0.50|0|0.16012671|0.22791306|0.26405791|0.13849733|
|0.75|0.67448975|0.49413604|0.61543459|1.18074730|0.40325350|
|0.95|1.64485363|1.96790018|1.66578526|2.39075506|0.82073265|

For 20260831 monthly M01 (30-year training), rain QQ values at the same p are
[-1.24344663, -0.66966839, -0.23639568, 0.29807333, 1.14430212];
temperature values are
[-1.20718031, -0.39276621, 0.11206022, 0.68821185, 1.10434397].

Sobol 512-minus-256 mean sensitivities (P mm, T degC) are:
weekly pair (0.01181148, 0.00218922), monthly pair (0.04683503, 0.00360773),
latest monthly partial pair (0.20506248, 0.00109380).
They are explicit discretization diagnostics, not target-tuned corrections.

The representative-key selector explicitly reports absent-history latest-issue
keys: 20260831 weekly W06-W08 for both variables (6 keys), and monthly M02-M06
for both variables (10 keys). They must remain in the root status ledger;
this lane does not invent histories or silently claim those keys were fitted.
The available weekly W01-W05 and monthly M01 partial horizons remain fitted.

## Remaining scope and limitations

No unresolved implementation dependency remains for these ten IDs. MBJP,
full-experiment scheduling/scoring and absent-history status accounting are
root/other-lane responsibilities. Canonical climate transfer, real-time
historical release, physical member identity and conditional calibration are
not claimed. No baseline, data, observation, research, other-lane file,
environment package, or repository history was modified. Audit processes
terminate; queued helper children were cancelled before starting, leaving no
background computation.
