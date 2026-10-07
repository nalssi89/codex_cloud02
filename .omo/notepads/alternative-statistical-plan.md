# All applicable GloSea6 statistical alternatives: executable implementation design

Date: 2026-10-07. Design authority: the current instruction to FIT ALL scientifically
applicable methods supersedes the research report's literature-only scope and
small-first-menu recommendation. This is an implementation specification, not a
claim that any new method has already been fitted or outperformed EMOS.

## 0. Dispatch first: ownership, signatures, dependency waves

Use new modules only. Do not modify `calibration.py`, `scoring.py`, `data_io.py`,
the current runner, supplied inputs, active observations, research, or baseline
outputs. The root already captured the 60-file preservation receipt at
`.omo/evidence/alternative-baseline-hashes.json`. Verify it before and after the
experiment. Do not run the old output-writing runner as a prerequisite. There is
no git repository and no authorization to create commits.

|Wave|Owner/category|Exclusive write scope|Deliverable and dependency|
|---|---|---|---|
|0|Root, contracts/data; deep-high for contract decisions|`analysis/alternative_contracts.py`, `analysis/alternative_data.py`, `analysis/alternative_registry.py`|Frozen types below; immutable historical-only datasets, training IDs/folds, all 17-family inventory. Audit child supplies facts, not model decisions.|
|1A|Distribution owner, deep-low|`analysis/alternative_distributions.py`|Original-unit CDF/left-CDF/PPF/mean/CRPS implementations and serialization; depends only on contracts.|
|1B|Classical owner, deep-low|`analysis/alternative_classical.py`|Families 2-9 and deterministic trend wrappers; depends on contracts and distribution constructor signatures, not unfinished implementations.|
|1C|Bayesian owner, deep-high|`analysis/alternative_bayes.py`|Families 1, 10 Bayesian, 16 MBJP, 17; true posterior computations and diagnostics.|
|1D|Learning owner, deep-low|`analysis/alternative_learning.py`|Families 11-14, including both boosting algorithms; small pooled models, no target access.|
|1E|Joint/transport owner, deep-high|`analysis/alternative_joint.py`|Families 15, 16 except MBJP; aligned annual vectors and separately named predictive adaptations.|
|1F|Independent validator, deep-low|`analysis/validate_alternative_comparison.py`|Independent formulas, leakage, inventory, preservation and saved-output tests. May read all new modules but must not copy implementation formulas as its only oracle.|
|2|Root integration|`analysis/run_alternative_comparison.py`, `analysis/alternative_reporting.py`|Registry wiring, exact CLI below, fit ledger, separate continuous/category/joint score surfaces. Reuse `scoring.score_prediction` and `generate_summaries` UNCHANGED for continuous rows.|
|3|Owners repair their own files; root verifies|Same disjoint scopes|One real case per applicable registry entry; edge cases; then full eligible run, independent validation, report and manual QA. No method is dropped because it is slow.|

Dispatch 1A-1F together once wave 0 types are written. Owners may implement against
the signatures immediately; only execution waits for dependencies. No two owners
write the registry or runner. An owner returns method IDs, checks actually run,
remaining factual gates, serialized law examples, and timing, not just source code.

Binding commands, from repository root:

```text
.venv/Scripts/python.exe -B analysis/run_alternative_comparison.py --output outputs/alternative_comparison
.venv/Scripts/python.exe -B analysis/validate_alternative_comparison.py --output outputs/alternative_comparison
```

Add `--help`, `--methods ID[,ID...]`, `--case-id ID`, `--seed 20261007`,
`--workers 1..6`, and `--resume`. A subset run is visibly `scope=SMOKE`, never a
completed full experiment. Unknown flags/methods and output paths overlapping
protected trees fail before fitting. Default seed is 20261007, default workers 4,
BLAS/Torch threads 1 per worker. `--resume` reuses only fully matched cache keys.
Do not require a new package service, database, web application, or refactor.

## 1. Established evidence and non-negotiable estimands

Read evidence: `SYNTHESIS.md` all 17 rows and sections 3-11; its primary-recovery,
parsimonious, precipitation, learning and dependence dossiers; complete
`analysis/calibration.py`, `scoring.py`, `run_verification.py`, `data_io.py`;
source dictionary/configuration; current run summary and audit conventions.

* Current saved run has 6,580 supplied cases, 6,432 verified cases, 148 unavailable
  target observations, four baseline methods with 6,432 rows each, zero recorded
  EMOS fit failures and 156,408 training rows. These are saved evidence, not new
  experiment results.
* `1mon` is a seven-day window; `3mon` is an individual calendar month, not a
  three-month total. Temperature is the interval mean in degC; precipitation is
  the interval sum in mm. Retain leap days and explicit historical dates.
* Active source is `observations/kmahub_refresh`, resolved and hash-checked by
  `observation_provenance`. Use actual contributing-station means, minimum 50
  contributors per variable, no imputation and no 62/n inflation. Never mix
  shipped period references with fresh daily-derived observations as responses.
* The original package configuration explicitly accepted some leakage for a
  legacy workflow. That is NOT authorization here. Do not consume supplied
  corrected products, legacy probability samples or that old leakage policy.
* There are approximately 24-30 annual forecast/observation pairs per local fit.
  Historical ensembles of 3/7 members are covariates/distributions, not 3/7
  independent observations of that year's response.
* RAW, QM and QDM are the actually issued finite empirical laws; EMOS is the
  actual analytic Normal or zero-censored Normal. Do not replace EMOS with 99
  quantiles and call that its original CRPS. No automatic fair-CRPS correction.
* A stored physical `MEMBER` string is not by itself proof of cross-variable,
  cross-lead or historical/forecast identity. Array position is never identity.
* All new numerical choices below are fixed in advance. Numerical convergence
  checks may refine computation, not optimize verified-target skill.

Baseline adapter calls `calibrate(forecast, historical, observations, rain)` and
wraps its returned QM/QDM arrays and EMOS parameters without altering them.
Reusing previously verified baseline records is allowed only when case,
observation, training set, thresholds, implementation and provenance hashes match.
If a stronger date audit changes a training set, leave the saved baseline intact
and create explicitly named `*_strict_training` companion fits on that set.

Actual-data evidence received from the root/independent audit during design:
Full measured receipt and exact executed read-only drivers:
`.omo/evidence/alternative-input-applicability.md` (17-family decisions at
lines45-61). It verifies all60 protected hashes/byte counts unchanged.
Numerical zero refers to the ACTIVE DERIVED source; RN_DAY=-9 was mapped to0
under its recorded kmahub policy, not independently certified instrument truth.

* All 156,408 retained annual pairs are OK, exact daily reaggregation difference
  0, and have no HIST_END>=INIT, excluded source year, or historical valid-window
  intersection with the target year. Thus preserve baseline semantics exactly;
  the extra valid-year test is redundant for current local sets, but required
  as an assertion and new-pool guard. It must not silently alter a baseline.
* Weekly rain: 217 zero repeated rows/45,756; 30 zero windows/6,100 unique
  windows. Positive <=0.1 mm:1,045 rows; positive <=1 mm:5,276. These remain wet.
  Of 1,874 cases, 1,681 all-wet, 169 one dry, 24 two dry; minimum22 positive years.
  Positive Gamma therefore runs on 1,681 weekly strata and gates193.
* Monthly rain: no zeros/32,448 rows or316 unique windows, minimum3.47258 mm;
  all1,342 strata all-wet. Positive Gamma runs; regularized hurdles still run.
* All6,432 local mean/response covariance determinants are positive. No constant
  predictor/response gate blocks BJP/MOS. Same-window T/P annual alignment has
  45,756 weekly and32,448 monthly vectors with24/30years, opening G2.
* Complete T/P+ALL-LEAD vectors: weekly232 issuances (218x24years,14x30years),
  16 response components; monthly213 issuances, all24years,12 components.
  Include this combined path target in addition to pair and single-variable
  paths. Do not guess four weekly/three monthly leads from product names.
  Partial end-horizon issuances remain in the ledger as incomplete full paths
  and still receive every available scalar/pair/shorter-path prediction.
* Source labels `YYYYMMDD_m100`, MEMBER_NUMBER100, SOURCE_DATE and conversion
  SOURCE_FILE paths structurally match T/P and paths, but no dictionary defines
  perturbed/lagged physical identity or iid errors. G3/G4/G5 remain closed.
  Common full-path issued label counts:weekly24/28/56/58/70,
  monthly18/32/40/42/84. Structural labels are not physical proof.
* Exact historical regimes:3members/24years1993-2016 through2022-10-10;
  7members/24years2022-10-17 through2026-05-04;7members/30years1993-2022
  from2026-05-11. Compare common1993-2016 history as a labeled sensitivity;
  do not infer a causal change in initialization physics.
* Original source key(product,var,SOURCE_DATE,LEAD,MEMBER) has1,039,416
  unique rows and NO duplicate copies across case vintages. Never assume
  future copies identical or collapse distinct forecasts on repeated obs.
  Safe pooled original-case INIT<=outer gives weekly192..45,756 annual feature
  rows and192..6,100 unique windows; monthly144..32,448 and144..316, still
  only24..30annual years. First outer excludes45,564 future weekly and32,304
  future monthly feature rows. This conservative pool rule is binding.

## 2. Data, filtering, pooling and temporal validation

### 2.1 Training records and exclusion predicates

Each `TrainingRow` contains row ID, source case ID, source initialization year,
actual reconstructed source initialization date, HIST_START/HIST_END, product,
lead, variable, ensemble values, annual observed value, original member strings
when available, and provenance/version identifiers. Each row is one paired
annual response for one condition. Never expand the observation into member rows.

For every outer target and every inner pseudo-target:

1. Reconstruct windows with `expected_window`; match explicit reference dates.
2. Require QC-valid response and finite, nonnegative rain inputs.
3. Require `HIST_END < target.init` strictly.
4. Exclude `SOURCE_YEAR == target.valid_start.year`, preserving the current rule.
5. Additionally exclude a historical valid window intersecting the held-out
   target calendar year. This closes source-year/valid-year crossing ambiguity.
   Record exclusions separately so the stronger check cannot silently change a
   baseline comparison.
6. Apply these predicates before computing ANY transform, center, scale, prior
   scale, season smoother, residual, bootstrap, covariance, threshold or tuning.
7. Reject using a row's target observation as a forecast feature. Prediction
   objects do not contain target observations by type.

At least 10 distinct accepted source years are required for local methods; this
matches the existing minimum and is an eligibility rule, not proof of
identifiability. Constant predictors are allowed with slope identified by its
penalty/prior; a point-mass observation history is a valid degenerate climate
distribution, not a divide-by-zero invitation.

### 2.2 Pooled rows

Pool only one `(product, variable)` at a time, with lead and season explicit.
Never pool weekly sums and monthly sums as one raw response, or T and P as one
response. For ML and pooled regression, transform P by its prescribed link and
standardize using training-only statistics; target duration in days is an
explicit feature, not an undocumented conversion from sums to rates.

Deduplicate exact replicas arising from the same historical initialization,
lead, product, variable, model-vintage/provenance and observed window. All equal
keys must have equal member multisets and response; contradictory replicas are
`INPUT_CONFLICT`, not averaged. A later original case's hindcast copy may enter
an earlier outer fit only if the audit proves it is the same hindcast vintage
and exactly the same underlying record available in the accepted pool. Without
that proof restrict source case issue dates to `<= outer.init`; this is a
deterministic restriction, not a global veto on pooling.

For a source year containing K distinct pooled condition rows, each receives
weight `1/K`; total weight per source year is 1. Normalize only inside objectives
that require mean loss. Report both row count and distinct years. This is a
year-balanced composite predictive loss for dependent conditions, not an
independent-row generative likelihood or a fabricated Bayesian sample size.
Do not feed these fractional weights to NIW and call it ordinary conjugacy.
Bayesian local/joint fits use one complete vector per annual block instead.

Features, in fixed order: standardized ensemble mean, standardized
`log1p(sample_sd)` (M=1 -> sd=0), sin/cos of target-window midpoint annual phase,
lead index scaled to [0,1] within product, duration in days standardized by the
training pool, indicator for the seven-member historical archive era, indicator
for the extended1993-2022 historical archive era. These EIGHT features explicitly
condition on the measured archive regimes without asserting their physical
cause. Issue indicators use its known archive configuration, not current issued
member count as a surrogate for historical era. No station embeddings or spatial predictors exist. Standardize
the first two and duration by training mean and SD, SD floor 1e-6; sin/cos and
lead stay fixed. Precipitation models using a power feature apply the same
fixed power to each annual ensemble mean, not an undocumented mean of powers.

### 2.3 Inner selection / residual construction

There is no random row-wise CV. The default algorithms have fixed architecture,
penalties and optimization budgets. Where this plan explicitly selects a
mixture weight or iteration count, use up to the latest five distinct
historical pseudo-issue years having >=15 earlier eligible source years. For
each pseudo-target use its historical initialization date and target year,
then re-run ALL predicates and fit its transforms inside that fold. Remove the
whole validation source/valid-year block from every pooled condition. Weight
fold scores equally by year.

For prequential residual collections use EVERY eligible past validation year
with >=10 earlier training years, not just five. Require >=8 residual years for
transport/MBC predictive dressing and residual copulas. Historical rows with
no past-only training history are omitted from residual fitting, not fitted
in-sample. Each cached residual carries its own ancestor training IDs. Fold
thresholds are fold training quantiles; outer thresholds remain fixed outer
local-observation terciles, including for pooled methods.

If a selection rule has fewer than three valid folds, its selected subtype is
`INSUFFICIENT_INNER_FOLDS`; a separately registered fixed-hyperparameter subtype
still runs. Never silently change a selected method to a fixed method.

### 2.4 Factual gates, not convenience exclusions

The independent actual-data audit must supply machine-readable receipts:

|Gate|Fact required|Affected methods|Failure action|
|---|---|---|---|
|G0|Per accepted set: exact zeros, positive count, near-zero diagnostics, unique years|Positive Gamma; hurdle diagnostics; censored Bayesian branch|Gamma only when all training y>0; no arbitrary 0.1-mm wet threshold. Other rain models still fit.|
|G1|Unique historical row/vintage provenance, pool duplicates and retained years|Pooled learners/smoothers|Use conservative source-case-date pool above; gate only if <10 years.|
|G2|Aligned annual response/predictor vectors and exact windows|Schaake, copula, MBJP, MBC, OT, joint events|Use common complete-year intersection; gate only the unavailable joint key.|
|G3|Physical member keys consistent across variables/leads, valid missing policy|ECC/dECC; member-specific/group BMA|Gate affected subtype; equal-weight kernels and annual-mean joint methods still run.|
|G4|Documented scientifically comparable generation groups, stable group meanings|Grouped BMA|No arbitrary array-position groups. Gate only grouped weights.|
|G5|Evidence supporting iid homogeneous conditional member errors, or known covariance law|Finite-member signal-noise|Gate; never infer a 1/M law from counts or exchangeability alone.|
|G6|Two comparable historical time blocks with >=10 aligned years each|dOTC temporal adaptation|Gate dynamic subtype if absent; stationary OTC/MBC still run.|
|G7|Physical units/calendar and model-vintage comparability across blocks|Canonical climate-period transfer claims|Do not claim climate trend preservation if unproved; run explicitly labeled predictive adaptations.|

Zero-free training is not evidence that population rain has no atom at zero.
Positive-Gamma predictions assign zero probability to an exactly zero target;
the resulting finite CRPS remains valid and the zero-support/log-score caveat is
reported. All-wet hurdle samples still produce finite regularized occurrence
probabilities. Lack of zeros is not a reason to suppress CSG, GEV or Tweedie.

## 3. Shared callable and serialization contracts

The following signatures are binding. Dataclasses are frozen. `FloatArray`
means float64 NDArray; JSON artifacts use explicit tagged distributions, not
pickle. All dates and IDs are serializable, ordered and included in hashes.

```python
# alternative_contracts.py
class PredictiveDistribution(Protocol):
    def cdf(self, value: FloatArray) -> FloatArray: ...
    def cdf_left(self, value: FloatArray) -> FloatArray: ...
    def quantile(self, probability: FloatArray) -> FloatArray: ...
    def mean(self) -> float: ...
    def crps(self, observation: float) -> float: ...
    def to_spec(self) -> dict[str, Json]: ...

# Likelihood-capable components additionally implement log_density(value:float)
# and atom_mass(value:float). BMA uses mixture atom mass at an atom, never
# continuous density plus atomic mass. Its prescribed components support both.
# Fields, rather than a free-form bag:
# CaseInput(case_id, init, valid_start, valid_end, product, lead, variable,
#           members, member_keys, provenance_hash); NO target observation.
# TrainingSet(rows, year_weights, cutoff, held_out_years, train_hash,
#             local_observations, thresholds, feature_spec, fold_specs).
# FitConfig(seed, numerical_tolerance, fixed_registry_parameters, workers).
# FitDiagnostics(objective, convergence, n_rows, n_years, train_hash,
#                parameter_count, boundary_flags, numerical_error,
#                posterior_diagnostics, elapsed_seconds, message).
# MethodSpec(id, family_no, subtype, domain, surface, fit_scope,
#            algorithm_version, fixed_parameters, gate_ids, owner).
# FitResult(method_id, status, fitted_model: FittedModel|CategoryModel|None,
#           diagnostics, reason_code).
# ContinuousPrediction(case_id, method_id, distribution, fit_ref).
# CategoryPrediction(case_id, method_id, thresholds, probabilities, fit_ref).
# JointPrediction(joint_id, method_id, component_case_ids, samples, weights,
#                 marginal_refs, approximation_metadata, fit_ref).

class FittedModel(Protocol):
    def predict(self, target: CaseInput) -> PredictiveDistribution: ...
    def to_spec(self) -> dict[str, Json]: ...

# alternative_data.py
def load_experiment(root: Path) -> ExperimentInputs: ...
def training_for(target: CaseInput, inputs: ExperimentInputs,
                 scope: Literal["local", "pooled"]) -> TrainingSet: ...
def inner_folds(training: TrainingSet, target: CaseInput,
                min_years: int, last_n: int | None) -> tuple[FoldSpec, ...]: ...
def aligned_joint(component_cases: tuple[CaseInput, ...],
                  inputs: ExperimentInputs) -> JointTrainingSet: ...
def gate_report(spec: MethodSpec, training: TrainingSet | JointTrainingSet,
                inputs: ExperimentInputs) -> GateResult: ...

# alternative_distributions.py
def distribution_from_spec(spec: Mapping[str, Json]) -> PredictiveDistribution: ...
def weighted_empirical(values: FloatArray, weights: FloatArray) -> PredictiveDistribution: ...
def normal(mu: float, sigma: float, censor_zero: bool = False) -> PredictiveDistribution: ...
def student_t(df: float, loc: float, scale: float) -> PredictiveDistribution: ...
def logistic(loc: float, scale: float) -> PredictiveDistribution: ...
def lognormal(log_mu: float, log_sigma: float) -> PredictiveDistribution: ...
def affine(base: PredictiveDistribution, offset: float,
           scale: float) -> PredictiveDistribution: ...
def gamma(shape: float, scale: float, shift: float = 0.0,
          censor_zero: bool = False) -> PredictiveDistribution: ...
def power_censored(base: PredictiveDistribution, power: float,
                   unit_scale: float) -> PredictiveDistribution: ...
def hurdle(p_zero: float, positive: PredictiveDistribution) -> PredictiveDistribution: ...
def mixture(parts: tuple[PredictiveDistribution, ...],
            weights: FloatArray) -> PredictiveDistribution: ...
def censored_gev(loc: float, scale: float, shape: float) -> PredictiveDistribution: ...
def tweedie(mu: float, phi: float, power: float) -> PredictiveDistribution: ...
def bernstein(coefficients: FloatArray, p_zero: float = 0.0) -> PredictiveDistribution: ...
def cdf_crps(distribution: PredictiveDistribution, observation: float,
             scale: float, tolerance: float = 1e-7) -> NumericIntegral: ...

# alternative_classical.py / alternative_bayes.py / alternative_learning.py
def fit_classical(spec: MethodSpec, training: TrainingSet,
                  config: FitConfig) -> FitResult: ...
def fit_bayes(spec: MethodSpec, training: TrainingSet,
              config: FitConfig) -> FitResult: ...
def fit_learning(spec: MethodSpec, training: TrainingSet,
                 config: FitConfig) -> FitResult: ...
def fit_mbjp(spec: MethodSpec, training: JointTrainingSet,
             config: FitConfig) -> JointFitResult: ...  # Bayesian module
def predict_categories(model: CategoryModel, target: CaseInput,
                       thresholds: FloatArray) -> CategoryPrediction: ...

# alternative_joint.py
def fit_joint(spec: MethodSpec, training: JointTrainingSet,
              residuals: ResidualSet | None, config: FitConfig) -> JointFitResult: ...
def predict_joint(model: JointModel, targets: tuple[CaseInput, ...],
                  marginals: tuple[PredictiveDistribution, ...],
                  config: FitConfig) -> JointPrediction: ...

# alternative_registry.py
def method_registry() -> tuple[MethodSpec, ...]: ...

# alternative_reporting.py / runner / validator
def score_continuous(prediction: ContinuousPrediction, truth: ScoreTruth) -> ScoreRow: ...
def score_categories(prediction: CategoryPrediction, truth: ScoreTruth) -> CategoryScoreRow: ...
def score_joint(prediction: JointPrediction, truth: JointTruth) -> JointScoreRow: ...
def write_comparison(results: ExperimentResults, output: Path) -> None: ...
def run(root: Path, output: Path, options: RunOptions) -> RunSummary: ...
def validate(root: Path, output: Path) -> ValidationSummary: ...
```

`ScoreTruth` alone contains held-out observed values. Method fitting and
prediction must work when target observation files are inaccessible.
`CategoryModel` and `JointModel` have their own `to_spec`/prediction protocol;
they do NOT masquerade as a `PredictiveDistribution`.

Concrete companion fields:
`FoldSpec(fold_id,validation_row_ids,training_row_ids,pseudo_init,
held_out_years,ancestor_hash)`;
`JointTrainingSet(component_keys,rows_by_year,source_years,
historical_initializations,historical_windows,train_hash,gate_receipts)`;
`ResidualSet(component_keys,years,residual_matrix,weights,fold_refs)`;
`GateResult(allowed,reason_code,evidence_refs,counts)`;
`JointFitResult(method_id,status,fitted_model:JointModel|None,diagnostics,
reason_code)`. `CategoryModel.predict(target,thresholds)` returns the
CategoryPrediction; `JointModel.predict(targets,marginals,config)` returns
JointPrediction. The registry binds explicit fit/predict callables.

Status vocabulary: `OK`, `NOT_APPLICABLE_DOMAIN`, `GATED_DATA`,
`INSUFFICIENT_TRAINING`, `INSUFFICIENT_INNER_FOLDS`, `INPUT_CONFLICT`,
`FIT_FAILED`, `POSTERIOR_DIAGNOSTICS_FAILED`, `NUMERICAL_DISTRIBUTION_FAILED`,
`TARGET_UNAVAILABLE`. Every supplied case/method combination has a terminal
ledger record. Failure messages retain the solver/exception, case, train hash
and parameters; failed fits never get an `OK` predictive object.

### Distribution details

CDF is right-continuous, with `cdf(-inf)=0`, `cdf(+inf)=1`.
`cdf_left(x)=P(Y<x)` makes atoms explicit. Quantile is the generalized inverse
`inf{x:F(x)>=p}` for 0<p<1; endpoints return support endpoints (possibly
infinite). Rain CDF is zero at negative y; `cdf(0)` includes its atom.
A tie-merged empirical distribution stores unique sorted values and positive
masses summing to one, not interpolated pseudo-members. Mean and CRPS must be
finite; output is in degC or mm, never an unlabelled transformed score.

General CRPS oracle:
`integral[-inf,y] F(z)^2 dz + integral[y,inf] (1-F(z))^2 dz`.
Use survival functions in upper tails, split at atoms/support boundaries and
the observation. SciPy adaptive quadrature uses abs tolerance `1e-8*unit_scale`,
relative tolerance 1e-7 and limit 200; report estimated error and refine once
at 10x tolerance if the bound is exceeded. Use analytic Normal/censored-Normal,
weighted empirical and Normal-mixture formulas where available; never average
component CRPS to obtain mixture CRPS. Independent oracle checks remain required.
Means use analytic formulas or survival integration, not inverse-transform(mu).

For mixture PPF, bracket by component PPFs at the requested p, then monotone
bisection (atoms tested explicitly); unbounded bracketing uses component support
and logarithmic tail search. Weighted empirical CRPS is
`sum_i w_i |x_i-y| - sum_i w_i*x_i*(2*cumw_i-w_i-1)`.
Serialize component parameters/weights or posterior mixture parameters, including
transforms and unit scales; 100 stored quantiles are not a replacement law.

Stored baseline P05/P95 use NumPy linear sample quantiles for RAW/QM/QDM. Preserve
those existing records. In new uniform interval diagnostics use the baseline
empirical generalized-inverse quantiles as separately labeled
`CONTRACT_P05/P95`; disclose the convention difference. Baseline CRPS, means,
CDF probabilities and issued member values remain unchanged.

## 4. Exhaustive registry inventory: all 17 research rows

Every ID below is registered, even if a factual gate yields no fit. The registry
expands braces into distinct IDs; aliases do not count as separate experiments.
T/P indicate temperature/precipitation; C/K/J indicate continuous/category/joint.
Baselines and `climatology_empirical` are additional controls, not extra families.

|Family|Required method IDs/subtypes|Domain/surface|Scope and disposition|
|---|---|---|---|
|1 Joint Gaussian/BJP|`joint_gaussian_plugin`, `bjp_niw`, `bjp_sqrt_censored`, `bayesian_anomaly_ridge`|T C; rain sqrt C|Local annual pairs; genuine posterior in BJP/ridge IDs; plugin explicitly non-Bayesian.|
|2 Climate mixture/shrinkage|`cdf_mix_fixed50`, `cdf_mix_cv`, `anomaly_signal_shrink`|T/P C|EMOS + local empirical climate; selected/fixed weights separate; deterministic signal shrink is not CDF mixture.|
|3 Restricted MOS/constant variance|`anomaly_mos`, `emos_constant_variance`, `mos_unit_slope`|T/P C|Gaussian or censored Gaussian controls, explicitly nested/restricted EMOS.|
|4 Gamma/CSG EMOS|`gamma_positive`, `csg_fixed_shift`, `csg_estimated_shift`|P C|Positive Gamma G0; both shifted variants attempt all eligible rain sets.|
|5 Fixed power-censor|`power_{gaussian,logistic}_{sqrt,cuberoot}`|P C|Four concrete variants, original-mm evaluation. Logistic is not called Gaussian.|
|6 Hurdle|`hurdle_gamma`, `hurdle_lognormal`|P C|Regularized separate occurrence/intensity including all-wet sets.|
|7 GEV/Tweedie|`gev_censored_gumbel`, `gev_censored_shrunk_shape`, `tweedie_p15`, `tweedie_selected_p`|P C|Actual fits required; no expense-only gate.|
|8 BMA/kernel|`kernel_normal_equal`, `kernel_rain_hurdle_equal`, `bma_group_normal`, `bma_group_rain`, `bma_component_pool`|T/P C|ID-free equal kernels; groups G3/G4; component pool uses named predictive models, not raw member identities.|
|9 Pooling/smoothing|`pooled_mos_ridge`, `pooled_emos_ridge`, `pooled_emos_cyclic`|T/P C|Same safe pools as learning methods; distinguish sharing benefit from model-family benefit.|
|10 Trends|`bjp_t`, `bjp_ti`, `detrend_{qm,qdm,emos}`|T/P C|Train-only distinct forecast/observed trends. Rain censor boundary handled explicitly.|
|11 Ordinal/ELR|`ordinal_logit`, `elr_threshold_logit`|T/P K|Coherent terciles; no invented CDF/mean/continuous CRPS.|
|12 Distribution regression|`gamlss_ridge`, `componentwise_boost`, `ngboost_small`|T/P C|Different algorithms, fixed small features and supported rain law.|
|13 QRF/IDR|`qrf_year_forest`, `idr_mean_order`|T/P C|Weighted empirical predictive laws; bounded tails disclosed.|
|14 Neural|`drn_small`, `bqn_monotone`|T/P C|Small pooled deterministic models; BQN ordered coefficients and explicit rain atom.|
|15 Coupling|`schaake_window`, `schaake_block`, `ecc_q`, `decc_path_shrunk_error`, `residual_gaussian_copula`|T/P combinations and paths J|Annual aligned observation templates; identity G3 only for ECC/dECC.|
|16 Multivariate/transfer|`mbjp_niw`, `mbjp_sqrt_censored`, `mbcp_annual`, `mbcr_annual`, `mbcn_annual`, `otc_annual`, `dotc_annual`|T/P combinations J, derived C marginals separately labeled|G2 complete annual vectors; dynamic G6; honest annual-mean predictive adaptations below.|
|17 Finite-member Bayes|`finite_member_iid_signal_noise`, `finite_member_known_covariance`|T initially C|G5 required. Second subtype only for a supplied justified covariance law, not an estimated count ratio.|

Named transform variants in the literature are handled explicitly: identity T
and fixed square-root rain are the primary Bayesian transforms; Yeo-Johnson
and log-sinh are scientifically permissible alternatives, specified in section
6 and registered as `bjp_yj_fixed` and `bjp_logsinh_fixed`. They are not silently
claimed by `bjp_sqrt_censored`. Literature spatial CNNs/station-embedding DRNs,
SST bridging, daily-grid targets and independent physical model combinations
have no corresponding inputs here: record these as input-domain mismatches,
not failures of the corresponding small regional family. Climate-period QDM/
trend-preservation claims are not implied by the existing forecast QDM.

## 5. Classical, precipitation, mixtures, pooling and deterministic trends

### Shared fitting conventions

Local T working coordinates are `(y-mean_train_y)/max(sd_train_y,1 degC)`.
P uses `y/sP`, `sP=max(mean_train_positive_y,1 mm)` (sP=1 if none). Features use
training-only centers/scales. In the formulas below m is annual ensemble mean
on the specified working scale, v its sample variance, s=sqrt(v). M=1 has v=0.
No target-derived scaling. Normal location `a+b*m`, b>=0, and variance
`c+d*v`, c>=1e-6,d>=0, are the familiar baseline link.

Unless stated otherwise, fit weighted sum negative log likelihood plus
`0.5*sum(non-intercept coefficient^2)` on standardized features, using L-BFGS-B
maxiter 500, ftol 1e-10, gtol 1e-6. This is a penalized distributional regression,
not a posterior. Report the training objective and penalty separately.
Initialize at training climate moments and slope 0, and at slope 1 with
moment residual scale; choose the best CONVERGED finite objective. No
unconverged initialization is relabeled a fitted method. Parameters with
intrinsic constraints use log/softplus links; mean slopes fixed/nonnegative
where stated. Bounds on log scales [-12,12] are numerical admissibility on
standardized units; hitting them is a recorded boundary warning, and density/
moment validity is still checked.

**F2:** `cdf_mix_fixed50` is `0.5 F_EMOS + 0.5 F_clim`.
For `cdf_mix_cv`, evaluate lambda=0,.1,...,1 on the strict inner folds and choose
minimum mean original-unit CRPS, ties within 1e-10 prefer smaller lambda;
refit EMOS on outer training, never fit lambda on outer targets.
`anomaly_signal_shrink`: replace EMOS mean anomaly by
`lambda*(mu_EMOS-mu_clim)`, lambda=.5 fixed, retain its latent residual scale;
for rain apply this on the censored latent location. This is a distinct
distribution, not an equivalent representation of the CDF mixture.

**F3:** `anomaly_mos`: `mu=mean_y+b*(m-mean_m)`, b in [0,1], constant sigma;
fit original-unit Gaussian/censored Gaussian CRPS with the existing
`gaussian_crps`. `emos_constant_variance` fits a,b,c with d=0, b>=0.
`mos_unit_slope` fixes b=1,d=0 and fits intercept/constant variance.
All issue full distributions, not just point forecasts.

**F4:** Gamma regression uses `mu=softplus(a+b*m)+1e-6`, b>=0,
`var=softplus(c)+softplus(d)*v+1e-6`,
`k=mu^2/var`, `theta=var/mu`. Positive Gamma uses positive density and G0.
For CSG define G~Gamma(k,theta), Y=max(0,G-delta);
`F(y)=GammaCDF(y+delta)` for y>=0 and atom `GammaCDF(delta)`.
`csg_fixed_shift`: delta=.1 in scaled units.
`csg_estimated_shift`: delta=softplus(e), penalty additionally
`0.5*(delta/.5)^2`, initialization .1. Fit zero log-CDF and positive log-density;
neither shifts observations nor adds epsilon to measured zero. Finite exact
mean is `k*theta*SF_Gamma(k+1)(delta)-delta*SF_Gamma(k)(delta)`.
This is likelihood-fitted Gamma/CSG EMOS-family regression, explicitly not a
claim to reproduce a particular paper's CRPS links. Evaluate original-unit CRPS.

**F5:** r=1/2 or 1/3; Z Gaussian or Logistic(mu,scale), Y=sP*max(0,Z)^(1/r).
Use `mu=a+b*(raw_mean/sP)^r`, scale `exp(c+d*log1p(sd_of_power_members))`.
Fit zeros with log F_Z(0), positives with log density at `(y/sP)^r` and the
Jacobian. For y>=0, F_Y(y)=F_Z((y/sP)^r).
Square/cube inverse moments are finite for Normal/Logistic; compute censored
moments by survival integration. Do not square a negative latent quantile.
Zeros, variance zero and negative latent locations must all work.

**F6:** p0=logistic(a0+b0*standardized_mean), both coefficients ridge SD 2
(penalty coefficient 1/8 including the intercept to prevent all-wet separation).
Positive Gamma has log mean linear in mean and constant log shape; lognormal
has log-location linear in mean and constant log SD. Positive likelihood is
weighted only for y>0, occurrence uses all years. At least three positive years
are required for intensity; otherwise `INSUFFICIENT_TRAINING` with counts.
All-wet training remains legal due to occurrence penalty; no 0.1-mm threshold.
F(y)=p0+(1-p0)F_positive(y), y>=0; mean=(1-p0)*positive_mean.

**F7 GEV:** latent GEV CDF
`H(z)=exp(-(1+xi*(z-mu)/sigma)^(-1/xi))` on its support; use the Gumbel limit
at xi=0, correct endpoints outside support, Y=max(0,Z). Links:
mu=a+b*m,b>=0; sigma=exp(c+d*log1p(s)), d>=0.
Gumbel fixes xi=0. Shrunk-shape fits xi in [-.25,.25] with penalty
`0.5*(xi/.1)^2`. Every allowed xi has finite mean and CRPS. Positive observations
outside a finite endpoint give infinite objective, not clipped density.
Zeros use log H(0). Implement survival/PPF carefully near xi=0 and endpoints.
Do not call accumulated rain an extreme-value sample because this family is used.

**F7 Tweedie:** mu=exp(a+b*standardized_log1p_mean), b>=0; phi=exp(c),
1<p<2. p15 fixes p=1.5; selected-p evaluates {1.2,1.5,1.8} on inner original-mm
CRPS, then refits. Compound law:
`lambda=mu^(2-p)/(phi*(2-p))`, `alpha=(2-p)/(p-1)`,
`theta=phi*(p-1)*mu^(p-1)`, N~Poisson(lambda),
Y|N=n~Gamma(n*alpha,theta), atom exp(-lambda). Positive conditional law is NOT
a single Gamma. CDF/density sum Poisson-weighted Gamma terms centered at the
Poisson mode, evaluated in log space; retain terms until omitted Poisson mass
<1e-12. For scoring, additionally control omitted first moment using
`theta*alpha*lambda*P(Poisson(lambda) outside shifted retained indices)`.
Increase the series range until both mass and original-unit moment error
<1e-8*sP. Density needs its OWN error bound: omitted Poisson probability
does not bound omitted density. Consecutive positive-y density terms have ratio
`r_n=lambda/(n+1)*(y/theta)^alpha*Gamma(n*alpha)/Gamma((n+1)*alpha)`.
Evaluate log ratios, locate density term mode, then expand both directions.
Ratios decrease; once r_N<1, right remainder<=t_N*r_N/(1-r_N). The reversed
ratio analog bounds a remaining left tail, otherwise sum down to n=1.
Require density absolute remainder<=1e-12 AND relative remainder<=1e-9 of the
accumulated density before evaluating log likelihood. Retain the union of the
density/CDF/moment ranges. A computational ceiling is a numerical failure to fix, not a data gate
or permission to substitute Gamma. Mean is mu exactly. Fit compound log
likelihood; PPF via monotone inversion. Large-lambda cases need a certified
series/saddlepoint implementation if the direct sum is impractical; its error
must meet the same oracle checks before it can be used.

**F8 kernels:** temperature equal-weight mixture of Normal(a+b*f_j,h^2),
b>=0,h>0, one component per actually issued member. Fit shared a,b,h using
ONE mixture log likelihood per historical year, `log(mean_j density(y_i))`,
not member-wise response replication. ID-free and no iid member requirement.
Rain kernel is an equal mixture of shared-coefficient hurdles:
p0_j=logistic(a0+b0*log1p(f_j/sP)), positive Gamma mean
`softplus(a+b*f_j/sP)+1e-6`, common shape; same annual mixture likelihood.
Regularize occurrence as in F6.

Group BMA: only justified groups; group mass pi_g=softmax(eta_g), uniform
within group, shared correction within group, one global residual scale/shape.
Prior/penalty on weights is Dirichlet(2,...,2), i.e. add `-sum log pi_g`;
group coefficient deviations penalized N(0,1), occurrence intercepts as above.
Missing entire groups cause a per-case gate unless the training/issuing group
availability policy is justified; do not redistribute a historically learned
weight by array index. Within-group variable member counts use pi_g/M_g.
Normal T and hurdle-Gamma P variants are separate IDs.

`bma_component_pool` mixes named EMOS, constant-variance MOS and BJP predictive
densities, fitted using their STRICT prequential distributions and Dirichlet(2)
weight penalty. It is a model-component BMA-style predictive mixture, not
evidence of raw-member skill or a fully Bayesian posterior over model truth.
All three prescribed components expose density/atom methods internally, even
though public scoring only needs CDF. Outer component distributions refit on
outer training. Require >=8 common prequential years.
Do not replace this objective with CRPS stacking. Such stacking would be a
different experiment, outside the frozen required inventory.

**F9:** all pooled comparisons use identical rows/weights to learning methods.
`pooled_mos_ridge`: lead-specific intercept and slope around common intercept/
slope, constant residual scale, Normal/censored Normal.
`pooled_emos_ridge`: same means plus lead-specific log residual variance and
nonnegative spread coefficient. Penalize every lead deviation by .5*delta^2;
common slopes by .5*b^2, intercept unpenalized, no empirical-Bayes tuning.
`pooled_emos_cyclic`: add harmonics k=1,2 of annual phase to location and log
scale; cyclic penalty `.5*sum k^4*(sincoef_k^2+coscoef_k^2)`.
Use mean weighted CRPS plus penalty divided by distinct-year count, preserving
an explicit effective regularization scale. Smoothing shares information; it
does not multiply independent years.

**F10 deterministic detrend:** separately regress forecast annual means and
observations on centered source time (decades), slopes ridge N(0,1) in
standardized coordinates. T: detrend historical members with forecast slope,
detrend observations with observed slope, fit QM/QDM/EMOS, and add the observed
trend at the target year. Forecast mean is detrended at its target valid year.
This is not the package's older supplied DQM output.

Rain: work in fixed square-root/sP coordinates. Historical zeros after
subtracting observed trend have censor boundary
`c_i=0-beta_y*time_i`. QM/QDM empirical mappings operate on these signed
detrended values and are restored then censored/squared, explicitly labeled
additive latent-scale QDM rather than multiplicative-mm QDM. For EMOS fit
heterogeneous-censor likelihood (density above c_i, CDF at c_i), not fixed-zero
censored CRPS. At issue add beta_y*time_target, censor at zero, square and
restore sP. Restored mean is integrated, never transformed latent mean.

## 6. Genuine Bayesian designs, transforms, trends and finite-member gate

### 6.1 Primary univariate BJP and the non-Bayesian control

`joint_gaussian_plugin` fits annual mean/observation bivariate Gaussian moments,
using covariance shrinkage `.9*S+.1*diag(S)+1e-6 I` in standardized coordinates.
Condition by the Schur complement. It is a plug-in constant-residual model,
explicitly NOT BJP, despite Gaussian joint notation.

For `bjp_niw`, fixed-physical-scale annual vectors z=(forecast mean, observed T) obey
N_d(mu,Sigma), d=2. Prior:
`Sigma~InverseWishart(nu0=d+8, Psi0=(nu0-d-1)*I)`;
`mu|Sigma~N(0,Sigma/kappa0)`, kappa0=1.
Use g(T)=(T-10 degC)/(10 degC) and g(P)=sqrt(P/(100 mm)) for forecast
annual means and observations. No fitted response center/scale or fitted prior
enters this fixed-hyperparameter posterior. Return through the physical inverse.

Posterior:
`kn=k0+n`, `mn=(k0*m0+n*zbar)/kn`, `nun=nu0+n`,
`Psin=Psi0+sum(z-zbar)(z-zbar)' + k0*n/kn*(zbar-m0)(zbar-m0)'`.
Joint posterior predictive is t with df `v=nun-d+1`, location mn, scale matrix
`S=(kn+1)/(kn*v)*Psin`. Condition that predictive t on issued x:
location `my+Syx*Sxx^-1*(x-mx)`, df `v+dx`,
scale matrix `(v+delta)/(v+dx)*(Syy-Syx*Sxx^-1*Sxy)`,
delta=(x-mx)'Sxx^-1(x-mx). This is an EXACT NIW posterior-predictive-conditioning
variant, not a universal claim that all BJP mixtures are Student t.
S is Student SCALE, not covariance; covariance=df/(df-2)*scale when df>2.
The scalar Student constructor takes sqrt(the scalar scale entry), not its SD.

The alternative convention averaging conditional Normals under p(theta|D)
without updating by issued x is different. Do not conflate the two.
The frozen inventory uses joint-predictive conditioning ONLY. The alternative
cut convention is described to prevent an implementation error, not an open
choice or an additional required subtype.

`bayesian_anomaly_ridge` is separately labeled Bayesian conditional regression:
Y=X beta+epsilon, beta|sigma2~N(b0,sigma2 V0),
sigma2~InvGamma(a0=4,b0scale=3), design [1, fixed-physical-scale mean anomaly],
prior beta center [0,0], V0=diag(4,1). Use exact normal-inverse-Gamma updates
and Student posterior predictive with variance factor `1+x'Vn*x`.
This genuinely integrates coefficient/variance uncertainty; it is not joint BJP.
Rain counterpart uses the censored square-root likelihood/augmentation below.

### 6.2 Rain and alternative monotone transforms

Primary `bjp_sqrt_censored` fixes sP=100 mm and takes Z=sqrt(Y/sP); Y=0 means Z<=0,
positive Y reveals Z exactly with its transformation Jacobian. Forecast
predictor is sqrt(raw annual mean/sP), transforming the mean FIRST. Strict
joint rainfall also treats a zero forecast mean as its latent coordinate<=0.
With no zero coordinate NIW updates are exact. With zeros, coordinatewise Gibbs
samples each censored coordinate conditional on ALL the other coordinates,
truncated to(-inf,0], then draws NIW parameters from completed annual vectors.
Do not sample independent marginal truncated Normals. Row likelihood is exact
Gaussian density for revealed coordinates times the conditional joint
rectangle probability for zero coordinates times positive-rain Jacobians.
This is genuine censored joint inference, not replacing zeros with epsilon.

Use four deterministic-seeded chains, 1,024 warmup and initially 2,048 retained
draws per chain. Draw inverse-Wishart by Bartlett decomposition and means
conditionally. Assess split rank-normalized R-hat<=1.01, bulk/tail ESS>=400
for means, log SDs, correlations and zero predictive probability; increase to
8,192 then 32,768 retained draws if needed, preserving random streams. Failure
after the fixed diagnostic budget is `POSTERIOR_DIAGNOSTICS_FAILED`.
Do not thin to manufacture ESS or ignore divergences/chain disagreement.
Also monitor latent censor coordinates, slopes and covariance eigenvalues.
Require MCSE<=.01*training response SD for mean, <=.005 for zero/tercile
probabilities, <=.005*training response SD for CRPS (split-chain/batch estimates).

For predictor-conditioned posterior prediction in the censored branch,
posterior parameter draws are reweighted by p(x_target|theta) before mixing
p(y|x_target,theta); logsumexp weights, effective importance count >=400 and
no single weight >.05. If this fails, include x_target with missing response
in the Gibbs conditional-update system and draw directly from p(theta|D,x);
this is the same predictive estimand, not a different model. Preserve the
finite mixture representation and report posterior numerical approximation.
For zero target forecast mean condition on latent X<=0, not X=0. Use
target-augmented Gibbs in that case, including the censored predictor and
missing target response; no observed target Y is supplied. For positive
predictors importance weights are densities; for zero predictors they are
rectangle probabilities. Store the correctly target-conditioned mixture.
Mean of Y=sP*max(0,Z)^2 uses censored second moments per Normal component;
for Z~N(m,v), its mean is
`100*((m*m+v)*Phi(m/sqrt(v))+m*sqrt(v)*phi(m/sqrt(v)))`.
the NIW prior df ensures finite required moments. A Normal latent mean squared
is not the predictive rain mean.

`bjp_yj_fixed`: use Yeo-Johnson lambda=.5 for nonnegative rain:
g(y)=2*(sqrt(1+y/sP)-1), zero boundary 0, inverse
sP*((1+z/2)^2-1) for z>0 and zero otherwise. It is a fixed YJ transform, not a
MAP-estimated-transform reproduction. Predictor uses the same g(raw mean).
`bjp_logsinh_fixed`: g(y)=log(sinh(1+y/sP)) minus log(sinh(1)),
implemented stably; inverse
sP*(asinh(exp(z+log(sinh(1))))-1), censor at zero. This inverse grows linearly
in the upper tail and has finite posterior moments. Location parameter 1 and
scale sP=100 mm are fixed by this design, not fitted on observations or targets.
Do not use exp(Student t) for a lognormal Bayesian forecast: its positive mean
does not exist. Fixed log-sinh is deliberately chosen to avoid that defect.

### 6.3 BJP-t / BJP-ti and MBJP

Trend Bayesian model is multivariate regression of the joint transformed vector
on h=(1, centered time in decades):
Z=H B+E, rows E~N_d(0,Sigma),
`B|Sigma~MatrixNormal(B0,V0,Sigma)`, Sigma IW as above.
B0=0, intercept prior row variance 1; trend variance 4 for `bjp_t` and .04 for
`bjp_ti` (weak-trend prior). This models separate X/Y trends jointly; no
Australian spatially calibrated prior is imported. Use fixed physical
coordinates above and t=(valid_year-2000)/10. Posterior updates are
`Vn=(V0^-1+H'H)^-1`, `Bn=Vn*(V0^-1*B0+H'Z)`,
`Sn=S0+Z'Z+B0'V0^-1*B0-Bn'Vn^-1*Bn`, `nun=nu0+n`.
At target h: location=h*Bn, df=nun-d+1,
Student scale=`(1+h*Vn*h')/(nun-d+1)*Sn`.
Use these conjugate matrix-normal/IW updates, then the multivariate t
posterior predictive at target time, then condition on target predictors.
These are explicitly named conjugate trend-aware BJP variants, not claimed
byte-identical reproductions of the papers. Censored rain uses Gibbs completion
with observation threshold g(0) in the raw latent regression; if coding
detrended latent residuals instead, boundary is g(0)-h*B_y for EACH row/draw.
Subtract the entire removed mean: both intercept and slope if both were
removed; slope alone only if intercept was retained. Forecast-rain censoring
follows the same rule.

`mbjp_niw` extends the SAME proper posterior to temperature-only paths.
For same-window T/P use vector `(X_T,X_P,Y_T,Y_P)`,d=4 under
`mbjp_sqrt_censored`, which censors rain
coordinates (forecast and response) and uses fixed sqrt transform. Condition on both X values jointly;
response dimension is 2. No raw cross-member identity is needed to align means.
Use one response vector per aligned source year, and the same NIW prior rule
nu0=d+8, never independent univariate fits relabeled MBJP.
For same-variable multi-lead paths apply d=2*number_of_components only when
G2 passes; all requested product leads are allowed with this strong prior,
report covariance dimension and prior dominance. Joint prediction uses fixed
Sobol uniforms/Normal or Student construction with 256 scenarios, 512 for a
numerical sensitivity; univariate marginals remain exact/posterior-mixture laws.

### 6.4 Finite-member signal/noise: executable only after G5

Temperature standardized model:
s_i~N(0,tau2),
X_ij=mu_x+s_i+epsilon_ij,
Y_i=mu_y+beta*s_i+eta_i.
Conditional errors epsilon~N(0,sigma_x2), eta~N(0,sigma_y2), independent only
when supported by the generation audit. Fix X signal loading to 1 to identify
the latent scale; beta~N(0,1), mu_x/mu_y~N(0,4),
tau2/sigma_x2/sigma_y2~InvGamma(4,3). Annual likelihood contains one Y and the
member vector under the justified law, not M repeated Y values.
Gibbs sample signals, regression coefficients and variance parameters; same
four-chain diagnostics as above.

For an issued iid ensemble mean xbar of M members, conditional signal variance
V=(1/tau2+M/sigma_x2)^-1 and mean V*M*(xbar-mu_x)/sigma_x2.
Conditional Y is Normal(mu_y+beta*signal_mean, sigma_y2+beta^2*V);
average over the genuine posterior. A known covariance subtype substitutes
the GLS sufficient statistic and precision `1' C^-1 1`, with C supplied by
the justified covariance model. Exchangeability alone cannot supply C.
Absent G5, both entries retain evidence-backed gates; ordinary BJP remains
applicable. Do not multiply EMOS variance by 3/M or 7/M.

## 7. Pooled category, distributional, tree, isotonic and neural models

All these methods use section 2's identical safe pool and year-balanced loss;
they may run with 24 annual blocks despite many dependent condition rows.
Report weak data support and model complexity, rather than claiming ML is
automatically impossible or that pooling creates independent years.

**Ordinal:** eta=b'x, ordered cuts k1 and k2=k1+softplus(delta).
P_BN=logistic(k1-eta), P_NN=logistic(k2-eta)-P_BN,
P_AN=1-logistic(k2-eta). Fit categorical log likelihood plus .5*||b||^2 and
.125*(k1^2+k2^2), using each training row's OWN historical-only climatological
tercile labels. Construct these labels with its fold history, not the outer
target's observational value. An exact tied pair of forecast thresholds has
NN probability 0; fit/predict the corresponding binary collapsed ordinal model
for that stratum instead of retaining impossible middle-category mass.

**ELR:** standardized physical threshold t enters
F(t|x)=logistic(a+softplus(c)*t+b'x), guaranteeing threshold monotonicity.
Fit binary exceedance/complement observations at the two training-only
tercile thresholds with each row's weight split equally between thresholds;
penalty .5*||b||^2+.125*a^2+.5*c^2. This is a constrained extended logistic
threshold regression, not the ordered-cutpoint model. Return only its requested
tercile probabilities; do not extrapolate it into a claimed full temperature/
rain predictive law. Identical thresholds automatically yield middle mass zero.

**GAMLSS ridge:** Normal(mu,exp(logsigma)) for T; zero-hurdle Gamma for P
(p0, log mean, log shape). Additive parameter predictors use intercept, the
eight features, centered squared ensemble mean and sin/cos second harmonic.
Ridge penalty .5 per coefficient, occurrence intercept penalty .125.
Joint penalized likelihood optimization. Shape is constant for P to limit
complexity. This is a small penalized GAMLSS variant, not boosting.

**Componentwise boosting:** same response families, parameter links and fixed
base learners (single standardized feature or second harmonic).
Initialize intercept-only climate fit. At each of 100 iterations compute
negative log-score gradients for every free parameter, fit a weighted
one-feature least-squares learner to each gradient, select the largest
training-loss reduction across parameter/feature candidates, update with
learning rate .05. Fix P shape from the intercept-only positive fit; update
occurrence and log mean. No target-tuned stopping or overclaim of exact paper
replication. Use the finite penalized all-wet intercept initialization.

**NGBoost small:** genuinely natural-gradient boosting, not the preceding
algorithm with another name. T parameters (mu,logsigma), expected Fisher
diag(1/sigma^2,2). For hurdle Gamma with fixed shape k, use parameters
(logit p0, log positive mean); Fisher diagonal
(p0*(1-p0),(1-p0)*k). Compute score gradient/Fisher natural gradient per row;
avoid constructing nonexistent negative-rain Normal distributions.
Fit depth-1 weighted regression trees to natural-gradient components.
Use scalar step from {1,.5,.25,.125,.0625} minimizing training log score, then
multiply by .05; exactly 100 iterations. p0 remains finite via bounded logits
[-12,12] and intercept regularization. Store links, fixed k and every stump.
Small Fisher entries are evaluated stably; clipping is logged, not hidden.

**QRF:** implement or pin an audited weighted QRF, NOT a forest of point
predictions mislabeled quantiles. 64 trees, maximum depth 4, minimum 5 distinct
source years in EACH child leaf, three randomly selected features per split.
Bootstrap source YEAR blocks, then use year-balanced row weights, not member or
row iid bootstrap. Weighted CART variance splits; ties sorted by feature index/
threshold. A prediction's observation weight is the average over trees of
within-leaf normalized training weights, including bootstrap multiplicity.
Merge duplicate observed values and issue the resulting weighted empirical
law. Mean/CDF/CRPS exact; support bounded by training observations. No invented
tail extrapolation. OOB rows from the same held-out year are excluded together.

**IDR:** single partial order is ensemble-mean order; spread is NOT assumed
stochastically increasing. Fit separately by lead and quarter-season within
the safe product/variable pool, with local fallback only as a separately
recorded scope when fewer than 10 years survive. At each unique observed
threshold y, fit antitonic weighted isotonic regression of `1(obs<=y)` against
forecast mean using PAVA. Sorting/ties share one fitted level; the resulting
CDF must also be monotone in y (the nested response construction provides this;
assert it). At unseen x use linear interpolation of neighboring fitted CDFs,
constant extrapolation outside predictor range. Predictive masses are adjacent
CDF differences on observed support, with rounding correction <=1e-12 only.
Report the stochastic-order assumption and bounded tails. Do not label a
mean+spread arbitrary total sorting as the original partial-order IDR.

**DRN:** eight features -> one hidden layer, four tanh units -> two T outputs
(mu, softplus sigma+1e-4); P has three outputs (p0, log positive mean,
softplus positive shape+.1). P law is hurdle Gamma. Use float64 CPU and
deterministic seeds, 400 full-batch Adam steps, learning rate .01, gradient
norm cap 5, coefficient L2 penalty .01 and occurrence intercept penalty .125.
Initialize output intercepts from training climate, other weights Xavier with
the fixed method seed. Select the lowest finite TRAINING penalized objective
iterate (not a verified-target best epoch). Fit two fixed seeds and average
their complete distributions with weights .5/.5; report this ensemble as the
actual issued DRN law, not a posterior. Numerical nonconvergence is explicit.

**BQN:** same hidden architecture and optimization; Bernstein degree K=5,
Q(u)=sum_{k=0}^5 c_k*B_{k,5}(u).
T c0 unconstrained; c_k=c_(k-1)+softplus(delta_k)+1e-6.
Rain positive c0=softplus(a0)+1e-6, same positive increments, plus p0 sigmoid.
Rain full quantile is 0 for u<=p0 and Q_positive((u-p0)/(1-p0)) otherwise.
Ordered coefficients guarantee noncrossing; this is a deliberate monotone
BQN variant, not a claim the original implementation imposed monotonicity.
Fit CRPS using `2*integral_0^1 pinball_u(y-Q(u)) du`, 64-point Gauss-Legendre,
splitting at the zero atom; verify 128/256 nodes against the CDF oracle.
Use the same weight penalty and exact derivative/autodiff through coefficients.
Mean T is sum(c)/6; rain mean=(1-p0)*sum(c)/6. PPF is the polynomial; CDF
inverts the monotone polynomial by bisection including endpoints/atom. Tails
are bounded by endpoints, deliberately disclosed; no Gaussian tail graft.

Implementation dependency policy: use NumPy/SciPy for non-neural models and
Torch2.8.0 CPU float64 for the fixed DRN/BQN Adam algorithm, with deterministic
algorithms enabled, one intra-op thread, and version recorded. Put any required
pin only in the NEW runner's dependency declaration/environment; do not change
protected files. There is no optimizer-substitution choice in this design.
Missing package installation is an implementation task, not a scientific gate.

## 8. Joint targets, dependence and distribution-transfer methods

Create joint keys for (a) same issued window T/P, (b) all available weekly
leads for one variable, (c) all available individual-month leads for one
variable, and (d) the combined T/P all-lead paths of16weekly/12monthly response
components. Partial-horizon dimension-matched keys remain explicit. A complete aligned annual vector uses the SAME source initialization
year and matching component windows. Take complete cases, no missing-value
imputation. G2 requires >=10 complete years. Do not infer member pairing to form
these mean/observation vectors.

All joint scores standardize components using OUTER TRAINING observed means/
SDs (SD floor 1 in each component's native unit). Save that scale. Report energy
score, variogram score with exponent .5 and weights `1/[d*(d-1)/2]`, and
predefined hot/dry event Brier `T>q67_T and P<=q33_P`.
Use exact weighted empirical expectations for saved scenario laws; report the
scenario approximation separately from continuous marginal CRPS.

### 8.1 Schaake, ECC, dECC, residual copula

Default coupling marginals are fixed EMOS, NOT whichever method wins target
scores; a second explicit coupling run uses univariate BJP. Each coupling ID
has a marginal-method suffix in output so unlike base distributions are not
pooled under one name.

Schaake window: same-condition historical observed ranks, one complete annual
vector per year. With n templates assign quantiles (j-.5)/n to marginal j-th
ranks and reorder by each template component. Schaake block: preserve one
historical year's ENTIRE lead path across components; no independently chosen
year per lead. For scalar T/P it agrees with window Schaake and is recorded as
an exact alias, not duplicated evidence. Rank ties use stable source-year order
with a fixed hash-based tie permutation shared only where an actual tie occurs.
No Gaussian jitter is added to observed rain zeros.

ECC-Q requires G3: intersect physically identified valid issued members across
ALL components, n>=2; report retained fraction and discarded member IDs.
Reorder the same n marginal quantiles by raw component ranks on this physical
intersection. Individual components with missing values are not independently
sorted after their arrays lose the common keys. Corrected QM/QDM array positions
are not automatically ECC ranks.

dECC: only multi-lead paths with G3 and >=8 prequential residual years.
Start from ECC scenarios; form raw-to-calibrated member increments on each lead
after training-unit standardization. Compute temporal correlation of
prequential raw forecast-mean errors, shrink as R=.5*R_sample+.5*I, Cholesky L.
Apply L to each member's increment vector, add to corresponding raw vector,
use resulting component ranks as a new template, and reorder the ORIGINAL
calibrated marginal quantile multisets. Register this explicitly as
`decc_path_shrunk_error`, an error-correlation dual-ECC variant; no statement
that it improves hourly wind or this data without scoring. The rank operation
preserves only the finite quantile multisets, not exact analytic EMOS CRPS.

Residual Gaussian copula: strict prequential fitted marginal PITs; for an atom
use randomized distributional transform
u=F(y-)+v*(F(y)-F(y-)), v fixed seeded uniform per row/component.
Store v and repeat four fixed randomizations as a diagnostic, not target tuning.
Normal scores Phi^-1(u), clipping only at machine-safe 1e-12 and logging clips;
estimate Pearson correlation, shrink .5 toward I, normalize diagonal to 1,
require positive-definiteness. Issue 256 Sobol Gaussian-copula scenarios, map
through original marginal generalized inverses; compare 512 scenarios for
Monte Carlo/discretization sensitivity. This is a plug-in residual copula,
not unconditional observed correlation and not Bayesian joint inference.

### 8.2 MBC/OT annual predictive adaptations

Canonical climate-period distribution transfer is not automatically a
conditional forecast method. Nevertheless aligned annual forecast means and
observations permit small, honestly named predictive adaptations NOW.
Do not gate all MBC/OT because physical member IDs are absent.

Use d=2 same-window T/P, same-variable paths, and audited combined all-lead paths.
Fixed source coordinates for ALL transfer operations are
`g(T,P)=(T/(1 degC),sqrt(P/(100 mm)))`, transforming annual means FIRST.
No response-dependent rescaling or separate forecast/observation metric.
Inverse `h(z)=(z_T degC,100*max(0,z_P)^2 mm)` applies AFTER adding a WHOLE
residual vector. Operations target dependence in sqrt-rain space, not native-mm
Pearson dependence. Equal annual masses; no daily/grid expansion.

Univariate mapping for these algorithms: empirical CDF midranks and quantile
linear interpolation on unique knots; ties merged; constant endpoint extension.
Source midpoint probability is(count below+.5*count equal)/n; destination
quantiles interpolate sorted observations at(r-.5)/n, constant at endpoints.
A constant source has a constant map. Tied sources cannot be deterministically
split into different destinations; do not claim exact empirical matching there.
This is an explicit out-of-sample transform, not a guessed future climate CDF.
Any negative final rain latent value is censored at zero before squaring.
All maps are fitted without outer target observations or target-member ranks.

`mbcp_annual`: start with componentwise mapping; iterate a Pearson covariance
adjustment `z -> mu_y+L_y*L_z^-1*(z-mu_z)` followed by componentwise
empirical remapping, 20 iterations. Use
C(A)=.5*S(A)+.5*diag(S(A))+1e-6 I and its Cholesky factor L.
Save every affine map and 1-D map and
apply the same sequence to new forecast-mean vectors. This is a fixed-iteration
Pearson MBC-like annual-mean adaptation, not Cannon QDM trend preservation.
`mbcr_annual`: map source coordinates to empirical midpoint-rank probabilities,
and observations to their corresponding rank probabilities. Recolor current
ranks toward target ranks, then fit/apply current-coordinate empirical-CDF
interpolation, 20 iterations; finish through observation coordinate quantiles.
Save every rank/scalar/affine map. It targets rank dependence and does NOT use a Pearson
algorithm with only the display name changed.

`mbcn_annual`: initial componentwise mapping then30 deterministic Haar rotations from QR of seeded Normal matrices
(positive-diagonal QR convention); rotate current corrected forecast/observed
latent vectors, fit 1-D empirical maps on each rotated coordinate, map the
forecast vectors, rotate back. Finish with a componentwise marginal remap.
Use the same fixed rotation sequence across prefix and full fits.
Store all rotations/maps for new-vector application. This is random-rotation
MBCn-like annual correction, no claim of original future-period QDM mechanism.

These three deterministic maps alone are not predictive distributions.
Attach joint residual dressing from STRICT prequential fits of the ENTIRE
mapping: residual r_i=latent_y_i-map_past(latent_x_i). Require >=8 residual
years; issue equal-weight vectors `h(map_outer(g(raw_target_mean))+r_i)`.
No recentering, bandwidth or independent-coordinate resampling; censor rain
BEFORE squaring AFTER whole-vector addition. Their empirical marginals are genuine issued laws,
not analytic baseline replacements. Do not use in-sample transport residuals
(which can be almost zero by construction). Save residual ancestry and bounded/
tail diagnostics. Marginal improvements, if any, must be measured. Shorter
prefix-fit residual laws need not equal final-fit errors: this is a disclosed
finite-sample prequential approximation, not a calibration guarantee.

`otc_annual`: exact balanced empirical optimal transport, not a label for
matching sorted components. Cost squared Euclidean in the saved transformed
training units; equal annual source/target masses. Solve the n-by-n assignment
(equal n complete annual vectors) with SciPy linear_sum_assignment; this is an
extreme-point optimal plan of the balanced Kantorovich problem. For ties use
deterministic lexicographic tie-breaking with perturbation below verified
cost tolerance, and retain true unperturbed cost.
For a new annual mean vector x, take the three closest source training vectors
(ties by source year). Uniformly average their CONDITIONAL plan rows
K_ij=pi_ij/(1/n), so `w_j=sum_{i in nearest3} K_ij/3`.
This also applies at exact matches; no inverse-distance alternative.
Issue a weighted empirical law on observed TARGET vectors. This is
an explicitly conditional nearest-source OTC adaptation, not a Gaussian
forecast and not original-member transport. Positive rain support is exact;
tail is bounded by observed joint support.

`dotc_annual`: require >=20 complete annual years and comparable model vintage.
Sort years; reference block is earliest floor(n/2), evolved block the rest.
Use separate historical model reference/evolved annual-mean laws and observed
reference law; DO NOT call the single issued ensemble the evolved climate.
Fit P_ji from early observations y0_j to early source means x0_i; fit R_ik
from early source x0_i to recent source x1_k. For each positive-mass path create
`v_jik=y0_j+(x1_k-x0_i)` and `omega_jik=P_ji*R_ik/a_i`,
where a_i=1/n0. This full-plan composition conserves total mass1 and transfers
the historical correction onto the evolved source. Evolution multiplier is
identity in the FIXED latent units. Project rain coordinates max(0,v_P),
merge duplicate atoms with summed masses, and report projected probability mass.
Fit a FINAL balanced OT plan S from recent source masses b_k=1/n1 to this
synthetic evolved target measure. Use scipy.optimize.linprog(method="highs")
for rectangular/nonuniform transport; require primal row/column residual<=1e-9,
nonnegative mass and converged objective. Assignment is only for equal square
uniform problems. Do not stop at the first two plans.
At issue uniformly average S_kell/b_k over the three nearest RECENT source
means; emit h(v_ell) with those weights. Synthetic support may exceed observed
support. Recent observations do not enter the evolved-target construction.
No verified observation or target-year data may define either block.
Report it as a historical-block dynamic-OT predictive adaptation, not a
validated future-climate trend-preserving product.
Canonical future-climate claims remain G7, not a gate on this adaptation.
Report distribution matching as PAIRING-BLIND: x=(0,1,2), paired y=(2,1,0)
have identical marginal distributions but reversed predictive relationship.
Nearest-three OT mixtures and projected/dressed empirical laws are actual
issued finite-sample predictive adaptations, not proofs of conditional
calibration or exact preservation of the original MBC training marginals.

## 9. Deterministic cost control and leakage-proof caches

Count work before execution: number of distinct outer train hashes, inner
fold hashes, pooled fits per `(product,variable,cutoff,heldout-year,provenance)`,
complete joint keys, posterior-censor cases and selected-subtype folds.
Emit this schedule to `fit_schedule.csv`; it is not grounds to omit a family.

Cache key includes algorithm/version and complete fixed parameters, ordered
training row IDs plus values/member-array hashes, date cutoff, held-out years,
active observation daily hash, forecast/hindcast source hashes, local threshold
definition, transforms, pool weight rule, inner fold ancestry and seed.
Never cache on month/lead alone; never reuse an outer model inside a past fold.
No fit key includes target observation/score. Models independent of target
members are reusable across targets with the same full training key; predictions
have a separate key including issued values and component identities.

* Parse gzip inputs once; cache QC aggregate per (variable,start,end,obs hash).
* Share local ensemble moments, positive counts, transforms and NIW sufficient
  statistics only for identical accepted sets/transform specifications.
* Pooled models with identical cutoff/heldout years/retained rows fit once and
  predict many cases. Year-balanced deduplication must precede cache hashing.
* Reuse prequential EMOS/BJP fits among BMA, copula, MBC residuals and tuning only
  when EVERY ancestor key matches. MBC residuals still require MBC past fits.
* Start posterior computation with analytic NIW for zero-free sets, not MCMC
  for all 6,432 cases. Censored posterior parallelism is by independent fit,
  deterministic seeds from SHA256(global_seed, method_id, train_hash, chain).
* QRF trees, MBC rotations, neural initialization and PIT randomizations use
  separately named seed streams; scheduling never changes results.
* Baseline calibration is reused/cached, not re-run inside every method.
* Numerical CDF and Tweedie series caches include all distribution parameters;
  no target-observation-conditioned quadrature cache is reused as a model fit.

Profile one real fit from every product/variable family and a zero/censor case
if present, then report measured projected CPU hours. Bounds: local simple
optimization is O(n*p*iterations), trees O(trees*depth*N_pool*features),
NIW O(n*d^2+d^3), MBC O(iterations*n*d^3), exact n<=30 transport O(n^3).
Posterior and neural costs are separately measured. Timeouts are operational
errors to resume/fix, never `NOT_APPLICABLE`. Serialize successful fit results
atomically so interrupted full runs can resume without duplicating outputs.

## 10. Outputs and fair, failure-inclusive comparison

Write ONLY below the requested new output directory:

* `run_summary.json`: scope, active provenance, config/dependency/seed hashes,
  protected hashes before/after, expected/attempted/completed registry entries,
  case statuses, timings, cache counts, all unresolved factual gate receipts.
* `method_inventory.csv`: each family/subtype, exact ID/algorithm, surface,
  applicability, evidence/gate, attempted/OK/failure counts; aliases explicit.
* `case_method_status.csv.gz`, `training_ledger.csv.gz`, `fit_ledger.csv.gz`,
  `fit_schedule.csv`, `fold_ancestry.csv.gz`.
* `distribution_specs.jsonl.gz` plus numeric arrays in versioned NPZ shards;
  original-unit distributions reconstructable without refitting.
* `continuous_predictions.csv.gz`, `category_predictions.csv.gz`,
  `joint_predictions.csv.gz`, `joint_scenarios.npz` and component key manifests.
* Ordinary continuous `metrics_*.csv` through unchanged `generate_summaries`,
  plus `paired_comparison.csv`, `coverage_and_failures.csv`,
  `failure_inclusive_policy.csv`, `equal_valid_window_metrics.csv`.
* `category_metrics.csv`, `joint_metrics.csv`, calibration/PIT/interval and
  upper-rain-event diagnostics, a concise Korean comparison report and plots.
* `validation.json` and CLI/QA receipts; no claims of new performance without
  actual fitted predictions and independent score checks.

Continuous scoring uses original-unit mean, original predictive CRPS, common
OUTER LOCAL observed terciles (`np.quantile(...,[1/3,2/3])`), and probabilities
`[F(q33), F(q67)-F(q33), 1-F(q67)]`.
BN <= q33, NN q33<Y<=q67, AN>q67; equal thresholds give NN=0.
Use existing `score_prediction`; category-only rows use only its probability
logic, never a fake mean or CRPS to pass a continuous writer.

For each comparison publish:

1. Total eligible count, scientific gates, missing targets, fit/numerical
   failures and success fraction BEFORE any skill ranking.
2. Pairwise common-success mask scores and paired deltas, with exact mask hash.
   Also a common-success mask within prespecified families; do not shrink the
   entire experiment to intersection of all methods and hide lost cases.
3. An explicit deployable policy: on FIT/numerical failure, use the same local
   empirical climatology and score ALL scientifically eligible targets.
   Label this `method+climatology_on_failure`, never change failed method status
   or pretend the fallback was the fitted forecast. Gated-data methods are not
   ranked as if applicable; their gate counts remain visible.
4. Failure-inclusive nonnegative-score bounds `[sum(success losses)/N, +inf)`
   if no fallback policy is desired; there is no finite invented penalty that
   establishes a method's missing forecast skill.
5. All-issuance weights and equal-valid-window sensitivity
   (each variable/product/window total weight 1, split over issuances).
   Paired year/overlap-block resampling must keep repeated valid windows
   together. With only about five verification years, show yearwise influence
   and leave-one-year-out differences; do not claim strong significance.

Fixed rain upper event is exceeding the OUTER training 90th percentile;
no target-chosen threshold. Randomized PIT respects atoms as specified above,
and all plotted PIT seeds are recorded. Never mix T and P CRPS units or weekly
and monthly amounts in a raw averaged winner score.

## 11. Independent proof and full manual QA

Follow the existing audit-script convention; no decorative test framework is
needed. The new independent validator may use analytical identities, separate
numerical quadrature and saved real predictions. Every formula check needs an
asserted tolerance justified by numerical accuracy, not a relaxed threshold
chosen after looking at a failure.

### Formula/oracle checks

* Reconstruct every tagged distribution and check CDF limits, monotonicity,
  atom size, generalized-inverse inequalities `F(q)>=p` and `F(q-)<=p`,
  total mass, finite mean, and nonnegative rain support.
* Normal/censored-Normal CRPS vs independent CDF integration; unchanged
  baseline values/issued members and original output hashes.
* Weighted empirical CRPS vs O(n^2) pair formula; ties, unequal weights and
  singleton point masses. Mixture CRPS vs cross-component expectation, showing
  that averaging component CRPS is wrong.
* CSG mean from incomplete-Gamma survival vs integration, correct shift sign
  and zero mass; hurdle vs CSG distinction; transformed sqrt/cube mean vs
  quadrature and Jensen counterexample.
* GEV Gumbel limit, xi both signs, finite endpoints, all mass censored, tails;
  Tweedie atom exp(-lambda), exact mean/variance, series mass/moment truncation,
  quantile inversion and Poisson-Gamma convolution reference.
* NIW/NIG and MNIW updates vs independent small matrix calculation; exact
  posterior predictive vs many independently generated posterior draws on a
  synthetic small case; correct conditional t df/scale; parameter uncertainty
  measurably differs from plug-in at small n. Censored posterior verifies zero
  likelihood and R-hat/ESS, not just a plausible fitted mean.
* Bayesian inverse-transform moment existence, including an adversarial
  exp(Student-t) example that MUST be rejected.
* QRF leaf weights reproduce observed distribution mass and year-bootstrap
  membership; forest point predictions alone cannot pass.
* IDR stochastic/CDF monotonicity and tied x/y; BQN ordered coefficients,
  endpoint support/zero atom, exact Bernstein mean and CRPS quadrature.
* Natural-gradient unit test verifies Fisher scaling is actually used;
  componentwise learner and NGBoost do not have identical update equations.
* Ordinal/ELR normalization, no crossing, equal thresholds, empty categories.
* Schaake/ECC permutation preserves FINITE marginal multisets/empirical CRPS;
  analytic-to-finite sampling error is separately nonzero and labeled.
  Duplicate/misaligned physical IDs must gate ECC, never pass via array order.
* Copula fits residual PIT dependence, not raw observed correlation; SPD
  shrinkage and zero-atom randomization; joint independent/correlated synthetic
  examples give distinct energy/event scores.
* OT row/column mass constraints and true squared-distance objective; MBC
  out-of-sample transform replay equals saved composition; dynamic transport
  uses two HISTORICAL blocks, never the current member ensemble as a period.

### Adversarial leakage and degeneracy checks

Change held-out truth to an extreme sentinel and demand byte-identical fitted
parameters/predictions; scores alone change. Add a row with HIST_END==INIT_DATE,
a future row, held-out source year, a year-crossing valid window and a duplicate
future-case copy: each must be excluded or conflict as specified.
Shuffle input order and worker count: deterministic predictions agree within
declared floating-point tolerances, IDs/masks/hashes agree exactly.
Change only excluded rows: predictions do not change. Change accepted training
truth: training hash changes. Change active observation hash: no stale cache hit.
Test M=1 target, constant means/spread, all-zero/all-wet rain, one positive year,
very large precipitation, negative rain input, coincident terciles, empty
allowed pool, incomplete joint year and contradictory duplicate source rows.
Do not weaken existing known tight QDM sensitivity alerts; report them separately.

### Real execution / tier checks

1. Run `.venv/Scripts/python.exe -B analysis/run_alternative_comparison.py --help`
   and the validator help: exit 0 and real documented flags.
2. Run each with `--invalid`: nonzero, helpful error, no writes/fits.
3. Run a representative actual eligible case per variable/product and EVERY
   applicable method, plus a complete actual joint key. Check distributions,
   fits, probabilities, scores and emitted status ledger personally.
4. Run the full binding command on all supplied cases, then the independent
   validator. Completion requires every scientifically applicable registered
   subtype to have actual attempted fits/predictions and failures accounted.
   A family name with only one easy subtype is not coverage.
5. Run project-venv Ruff and basedpyright on new modules; diagnostics before
   the full run. Existing audit formulas are behavior of record. Preserve
   unrelated pre-existing exceptions rather than editing them green.
6. Manually open the report/tables and render plots: method coverage/failures,
   original-unit scores, category-only blank continuous fields, joint labels,
   warning annotations and saved provenance must match data. If a browser
   page is generated, inspect desktop/mobile; otherwise inspect actual figures.
7. Re-hash all 60 protected files and verify equality. Ensure new artifacts
   stay under the new output path, no source edits/processes remain, and no
   verified-target selection occurred.

## 12. Acceptance checklist and remaining facts

Design completion means every row/subtype above has one algorithm, one support/
zero/tail decision, explicit fit/predict/score surface, leakage-safe training
and a legitimate factual gate. Experiment completion additionally requires
real fits, full inventory/status accounting, independent proof and manual QA.

G0, conservative G1, and same-window/full-path G2 now have the measured receipts
in section1; implementations must verify and persist them, not await new
scientific decisions. Remaining factual gates are G3 physical member identity,
G4 generation groups, G5 justified member-error covariance, G6 per-key
comparable10+10historical blocks, and G7 canonical future-climate/real-time
availability claims. G6 is expected to open for measured24/30year complete
vectors; it is checked per key, not guessed. These gates affect only dependent
subtypes; all other algorithms and their constants are frozen above. No user
approval loop or further speculative review is needed before dispatch.

The design intentionally rejects: plug-in MOS renamed BJP; iid member laws
inferred from M; future-aware tuning/normalization; baseline discretization;
category-only forecasts with fabricated CRPS; in-sample copula/MBC residuals;
one issue's ensemble renamed a future climate period; expense-only exclusions;
and successful-fit-only rankings with hidden failure coverage.
