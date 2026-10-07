# Frozen learning implementation audit

Status: PASS. Owned learning implementations, mathematical audits and
actual-example fit/predict/serialization QA are complete. This is not a claim
that the root's full all-case comparison experiment has been executed.

Owned entry points:

```python
fit_learning(spec: MethodSpec, training: TrainingSet, config: FitConfig
             ) -> FitResult | CategoryFitResult
predict_categories(model: CategoryModel, target: CaseInput,
                   thresholds: FloatArray) -> CategoryPrediction
```

Required IDs: `ordinal_logit`, `elr_threshold_logit`, `gamlss_ridge`,
`componentwise_boost`, `ngboost_small`, `qrf_year_forest`, `idr_mean_order`,
`drn_small`, `bqn_monotone`.

Source authority: frozen plan section 7 and sections 2.1-2.3; actual input
applicability receipt; keyword-only truth-separated contracts. No existing
baseline, observation, data, research, or other owner's modules were edited.

## Completed independent check

Exact executed driver from repository root:

```text
.venv/Scripts/python.exe -B -c 'from analysis.alternative_learning_checks import check_ancestry; check_ancestry(); print("ANCESTRY MASS PASS")'
```

Exit 0; output `ANCESTRY MASS PASS`.

The synthetic adversarial case has thirty source-year blocks, two distinct
conditions per block, and a 2022 original-case catalog vintage. Historical
validation years retain this outer-frozen catalog rather than falsely filtering
it by pseudo-issue year. The audit requires 40 eligible labels, >=10 distinct
own-condition past years per label, response end strictly before historical
initialization, no validation-year ancestor, no self ancestor, and catalog
issuance at or before the actual outer cutoff. Independent ordinal checks
require nonnegative masses summing to one and decreasing below-normal
probability with increasing predictor.

Exact executed regression mathematical driver:

```text
.venv/Scripts/python.exe -B -m analysis.alternative_learning_regression_checks --math-only
```

Exit 0; output:

```json
{"gradient_errors": {"rain": 3.0260505212709177e-10, "temperature": 3.6562930461059295e-10}}
```

Central finite differences check every ordinary link-score gradient against
the actual Normal/hurdle-Gamma likelihood. The oracle independently constructs
the expected Fisher diagonal, requires its product with the computed natural
gradient to recover the ordinary gradient, and requires natural and ordinary
gradients to differ by more than 0.1. It separately checks occurrence-intercept
penalty derivatives, reported Fisher clipping, finite all-wet initialization,
and the exact weighted depth-one regression-tree split.

Exact executed independent order-model driver:

```text
.venv/Scripts/python.exe -B -m unittest analysis.alternative_learning_order_checks.OrderChecks.test_pava_independent_quadratic_oracle analysis.alternative_learning_order_checks.OrderChecks.test_bootstrap_multiplicity_leaf_mass analysis.alternative_learning_order_checks.OrderChecks.test_child_year_support_can_overlap analysis.alternative_learning_order_checks.OrderChecks.test_ancestor_gates_before_feature_fit
```

Exit 0; `Ran 4 tests in 0.004s`, `OK`. Decreasing PAVA is compared with an
independent constrained quadratic-program optimizer. A known source-year
bootstrap with uneven row multiplicities must produce the exact within-leaf
distribution weights. An adversarial split places every one of five years in
both children and requires the distinct-year support rule, not a row-count
surrogate. Temporal gate checks reject validation-year ancestors, cutoff-equal
response windows, future original catalog vintages, and source/valid-calendar
crossing leakage before feature fitting.

Protected-artifact driver:

```text
.venv/Scripts/python.exe -B -c 'from pathlib import Path; from analysis.alternative_validation_io import preserved; import json; report=preserved(Path.cwd()); print(json.dumps(report,indent=2)); assert report["status"]=="PASS"'
```

Exit 0, `{"status": "PASS", "files_checked": 60, "failures": []}`.

## Real shared-adapter fit/predict checks

The root's actual `alternative_data` facade, eight-feature implementation and
original-unit distribution constructors are now present and were read before
these executions. No fake adapter or feature fallback was installed.

```text
.venv/Scripts/python.exe -B -m analysis.alternative_learning_checks
```

Exit 0; own-past ancestry/mass and category fit/tied-cuts/empty-middle checks
passed. Fixed-input objectives:

|Method|Variable climate|Objective|
|---|---|---:|
|ordinal_logit|varying|6.861710425850081|
|elr_threshold_logit|varying|4.460575025071375|
|ordinal_logit|constant|2.470685314299689|
|elr_threshold_logit|constant|1.8118718876375037|

```text
.venv/Scripts/python.exe -B -m unittest analysis.alternative_learning_order_checks -v
.venv/Scripts/python.exe -B -m analysis.alternative_learning_regression_checks
```

Both exited 0. All seven order tests passed in 0.414 seconds. The complete
QRF driver proves all 64 bootstrap draws, multiplicity-normalized leaf weights,
minimum five distinct years per child, entire-year OOB exclusion, deterministic
reproducibility, and exact empirical CDF/CRPS rather than point-tree predictions.
The IDR driver verifies tied predictors, CDF threshold nesting, antitonic
predictor order, interpolation and explicitly reported local fallback.

Regression objectives:

```json
{
  "componentwise_boost:rain": 37.670476769903004,
  "componentwise_boost:temperature": 8.242998374187398,
  "gamlss_ridge:rain": 4.2563806849912424,
  "gamlss_ridge:temperature": -17.02630509664698,
  "ngboost_small:rain": 28.050063264205836,
  "ngboost_small:temperature": 4.148296087104482
}
```

Every regression subtype runs both response families through its actual
prediction law, with monotone finite quantiles, finite original-unit mean,
nonnegative rain support, explicit zero mass and valid JSON. The first saved
NGBoost stump must equal the exact natural-gradient fitted stump and differ
from the ordinary-score-gradient stump. Degenerate/all-dry and constant-positive
checks passed with explicit diagnostics.

## Read actual known-input example

The actual loader and `training_for(..., "pooled")` were executed in a read-only
driver; exit 0. No held-out truth was passed to any fit. Measured receipt:

```json
{
  "case_id": "20220307_1MON_W01_t15m",
  "issue": "2022-03-07",
  "window": ["2022-03-07", "2022-03-13"],
  "member_count": 28,
  "archive_era": "three_24",
  "pool_rows": 192,
  "years": 24,
  "catalog_cutoff": "2022-03-07",
  "train_hash": "d76468a5f88405653317fdb956f193ce0d315317a419d84b8e6d3714ae79ac0d",
  "thresholds": [3.527188940092166, 5.476651305683564]
}
```

Final all-ID manual QA driver is
`analysis.alternative_learning_actual_checks`; it fixes the first weekly and
monthly T/P cases before fitting, compares own-past category cuts with the real root
`row_thresholds` API, checks every annual total weight equals one, verifies
catalog/cutoff/year ancestry, and executes fit/predict/serialize for every ID.
The all-nine-ID run exited 0 with 36 checks in 87.35940610000034 seconds.
The Torch dependency is installed by root and all neural checks below have
passed; no cost-based method exclusion or fake adapter was used.

## Actual nonneural smoke result

Exact command:

```text
.venv/Scripts/python.exe -B -c 'from analysis.alternative_learning_actual_checks import main; from analysis.alternative_learning import LEARNING_IDS; main(LEARNING_IDS[:7])'
```

Exit 0; `{"scope": "SMOKE", "checks": 14, "seconds": 31.189385100000436}`.
This is explicitly a partial-method development smoke, not completion of the
neural lane or the full experiment. All source/year masks, unit annual weights,
root row-threshold equality, finite laws and serialization checks passed.

Both pools contain 192 annual rows and 24 distinct source years. IDR's
lead/quarter selection retains 24 rows and all 24 years, explicitly reported
as pooled stratum scope. Rain train hash:
`cd81d7ddadd3728035dfca4f9e0b552fb5c62ae028c5e1ac0c4f83151a74f812`.

|Actual method|T mean|P mean|T fit seconds|P fit seconds|
|---|---:|---:|---:|---:|
|gamlss_ridge|6.013372993823327|4.728362294711733|0.036936|0.072907|
|componentwise_boost|9.260895270151549|10.24357330131841|0.080236|0.126034|
|ngboost_small|7.900746907288812|5.194997633272469|0.149580|0.210604|
|qrf_year_forest|6.4802003333888765|6.3346520143661795|0.308473|0.242249|
|idr_mean_order|7.882163787234889|4.029062318571169|0.004301|0.001131|

|Actual category method|T probabilities|P probabilities|T/P fit seconds|
|---|---|---|---|
|ordinal_logit|[0.3147739940455755, 0.29066243984829276, 0.39456356610613175]|[0.5254825621039105, 0.21031457554286448, 0.264202862353225]|0.141498 / 0.046715|
|elr_threshold_logit|[0.19982630976214114, 0.11409029100740328, 0.6860833992304556]|[0.4849988604512169, 0.11184517526348259, 0.40315596428530054]|0.032354 / 0.033233|

Actual hurdle rain atoms are finite: ridge 0.03840689774523281, componentwise
0.04619953726306873, NGBoost 0.03520330361837239. QRF preserves the training
zero through its actual empirical leaf law (atom 0.0009422943955587701).
IDR's conditional stratum may legitimately issue zero atom zero.
The three numerically null features (fixed duration and both archive indicators)
are explicitly logged by componentwise boosting, not fabricated into slopes.

## Complete actual weekly/monthly QA

Exact executed command:

```text
.venv/Scripts/python.exe -B -m analysis.alternative_learning_actual_checks
```

Exit 0, final output:

```json
{"scope": "ALL_LEARNING_EXAMPLE_IDS", "checks": 36, "seconds": 87.35940610000034}
```

This covers every required ID on four fixed actual cases:
`20220307_1MON_W01_t15m`, `20220307_1MON_W01_prcp`,
`20220307_3MON_M01_t15m`, `20220307_3MON_M01_prcp`.
Weekly pools have 192 rows, monthly pools 144 rows, each with 24 source years.
Every annual total weight is one. IDR retains 24 rows and all 24 years in its
lead/quarter stratum. Every continuous law was exercised through CDF,
left-CDF, PPF, original-unit mean, CRPS, rain atom and JSON serialization;
category laws were exercised through the actual threshold API. Target truth
was never supplied to a fit.

Captured neural predictions:

|Case|Method|Mean|CRPS at own mean|Zero atom|Fit/predict seconds|
|---|---|---:|---:|---:|---:|
|weekly T|drn_small|7.472861251514473|0.3560085198346491|0|7.139346100000694|
|weekly T|bqn_monotone|7.202638313868595|0.4196365491499817|0|7.103617000000668|
|weekly P|drn_small|5.222851127990966|1.612061894329598|0.07171495202778636|2.8522669000012684|
|weekly P|bqn_monotone|6.647530061647338|4.0291985834216515|0.6064838758269533|8.177223000002414|
|monthly T|drn_small|11.645499657059721|0.34669617402339803|0|2.052165099998092|
|monthly T|bqn_monotone|11.11201176147296|0.39568504967851154|0|6.993279099999199|
|monthly P|drn_small|83.62833707200906|10.917013900319496|0.03670315075710949|2.418266600001516|
|monthly P|bqn_monotone|165.3153935530355|42.69808341376109|0.13435832914392035|6.958993799999007|

These are numerical QA values, not held-out skill claims.

## Full Torch, crossing-kink and actual-data BQN proof

Neural child executed the fresh integrated driver:

```text
.venv/Scripts/python.exe -B -m analysis.alternative_learning_neural_checks
```

Exit 0: all eight method/fixture combinations, repeated two-seed fits,
999-point PPF monotonicity and determinism, CDF/left-CDF checks, proper mass,
finite scoring, Torch gradcheck, all-wet, all-dry and constant-positive rain
checks passed. Fixed-input maximum 64/128/256-node CRPS errors were
1.8e-15 / 1.3e-14 / 1.8e-15. The 999-point checks were retained.
Algorithms remain CPU/float64, four tanh units, exactly 400 full-batch
`torch.optim.Adam` steps per seed, learning rate 0.01 and gradient norm cap 5.

The BQN objective splits the positive-quantile interval at Q(v)=y and treats
the rain atom analytically. Detached crossing inversion is legitimate because
the pinball integrand is zero at the moving boundary; p0 terms remain in the
autograd graph. Gauss-Legendre integrates the resulting degree-six pieces,
so increasing nodes does not hide a crossing discontinuity.

Parent independently reran the actual trained-component oracle:

```text
.venv/Scripts/python.exe -B -c 'from analysis.alternative_learning_actual_checks import main; main(("bqn_monotone",))'
```

Exit 0, four checks in 96.88224459999765 seconds. Both trained seeds are
compared with an independent strict CDF integral at physical-unit reference
quantiles of safe historical responses; no target truth or target tuning.
Maximum absolute errors, unchanged limit 1e-7:

|Actual case|64 nodes|128 nodes|256 nodes|
|---|---:|---:|---:|
|weekly T|7.105427357601002e-15|1.3322676295501878e-14|3.552713678800501e-15|
|weekly P|1.0658141036401503e-14|4.263256414560601e-14|1.7763568394002505e-15|
|monthly T|2.1316282072803006e-14|1.2434497875801753e-14|1.9539925233402755e-14|
|monthly P|1.4210854715202004e-13|6.252776074688882e-13|3.552713678800501e-14|

## Exact Bernstein scalar-kernel gate

The shared tiny-array inversion measured 0.624724299999798 seconds for a
single two-part mixture quantile. Owned `learning_bernstein` retains the
canonical bounded degree-five law, support, PPF, density, mean, atom and JSON;
its 64 bisection steps use centered scalar Horner evaluation. Centering avoids
large-location cancellation. This is not a lower-node approximation or
an alternative method.

```text
.venv/Scripts/python.exe -B -m analysis.alternative_learning_bernstein_checks
```

Exit 0. Actual float64/shape, CDF/left-CDF, PPF, mean, atom, JSON, CRPS and
log-density comparisons passed. Canonical CDF error and independent 80-digit
near-degenerate inversion error were both 2.220446049250313e-16.
Accelerated single-mixture-quantile time was 0.005270300000120187 seconds;
timing is recorded, not used as a flaky pass criterion.

Approval and completed neural proof are recorded in
`.omo/evidence/alternative-learning-bernstein-validation.json`.

## Year-crossing source/valid masks

The final category driver also constructs December historical issues whose
valid windows fall wholly in January. Source-year blocking and valid-window
calendar blocking are kept separate: a validation initialization year must not
incorrectly remove the preceding January's legitimate past response.
Forty eligible labels match the actual root `row_thresholds` helper exactly,
including the ten-past-year boundary. Existing future-catalog, cross-window,
self-year and tied-cut/empty-category checks remain active.

```text
.venv/Scripts/python.exe -B -m analysis.alternative_learning_checks
```

Exit 0; final line:
`YEAR-CROSSING PAST LABELS MATCH DATA HELPER PASS`.

## Final diagnostics, size and immutable baseline

Exact final commands:

```text
.venv/Scripts/python.exe -m basedpyright analysis/alternative_learning*.py
.venv/Scripts/python.exe -m ruff check analysis/alternative_learning*.py
```

Both exited 0: **0 errors, 0 warnings, 0 notes**; **All checks passed**.
No casts, ignores, configuration weakening or optimizer substitution.
The language server's inability to resolve existing `analysis` imports is a
namespace limitation; native project diagnostics above are clean.

All fourteen owned Python modules are below 250 pure nonblank,
noncomment/non-docstring lines:

|Suffix after alternative_learning|Pure lines|
|---|---:|
|entry point|66|
|actual_checks|141|
|bernstein|54|
|bernstein_checks|85|
|category|193|
|checks|153|
|neural|214|
|neural_checks|106|
|neural_math|55|
|order|232|
|order_checks|194|
|regression|200|
|regression_checks|177|
|regression_math|114|

The protected-artifact command above was repeated after the final edits:
exit 0, **60 files checked, no failures**.

Residual scientific limitations are explicit: bounded empirical/quantile tails,
only 24 source years in the examples despite more pooled rows, and all-dry
intensity identified only by declared regularization. Fixed neural-budget
completion is not a claim of optimizer stationarity. There are no remaining
owned implementation or validation blockers.
