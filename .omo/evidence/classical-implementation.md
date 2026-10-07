# Classical implementation and executable evidence

Date: 2026-10-07. The pooled replication blocker is resolved, the final
all-ID actual smoke has passed, and the unchanged full mixed-zero BMA audit
has passed with 14 temperature and nine rain common prequential years.
Historical failed runs and five correctly rejected rain folds remain
documented below. This is not the root's full alternative experiment.

## Interfaces and inventory

`analysis.alternative_classical.fit_classical(spec: MethodSpec,
training: TrainingSet, config: FitConfig) -> FitResult` dispatches these 30 IDs:

```text
cdf_mix_fixed50 cdf_mix_cv anomaly_signal_shrink
anomaly_mos emos_constant_variance mos_unit_slope
gamma_positive csg_fixed_shift csg_estimated_shift
power_gaussian_sqrt power_gaussian_cuberoot
power_logistic_sqrt power_logistic_cuberoot
hurdle_gamma hurdle_lognormal
gev_censored_gumbel gev_censored_shrunk_shape
tweedie_p15 tweedie_selected_p
kernel_normal_equal kernel_rain_hurdle_equal
bma_group_normal bma_group_rain bma_component_pool
pooled_mos_ridge pooled_emos_ridge pooled_emos_cyclic
detrend_qm detrend_qdm detrend_emos
```

Helpers expose `fit_local`, `fit_mixture`, `fit_kernel`, `fit_pooled`,
`fit_trend`, and `fit_selected_tweedie`. All return the frozen `FitResult`
with a truth-free fitted-model `predict(CaseInput)` and `to_spec()` contract.
Distribution construction follows the owner API, including CSG's additive
`shift=-delta`, square/cube forward powers, atom mass, and log density.

The full internal `emos` and explicitly specified `anomaly_mos` use
original-unit Gaussian/censored-Normal CRPS. The other two restricted MOS
controls follow the shared penalized negative-log-likelihood default.
Local diagnostics retain the unpenalized training loss and penalty separately.
Only successful finite solver results can issue fitted models.

The two group-BMA IDs retain G3/G4 evidence-backed gates: actual source labels
do not establish physical member identity or comparable generation groups.
No array-position groups were invented. ID-free kernels run. Positive Gamma
gates exact nonpositive training outcomes; all-wet hurdles still fit with
occurrence intercept and slope penalties. Selected CDF/Tweedie methods use
actual historical pseudo-issues, the frozen outer catalog, and inner ancestry.
Named-model BMA uses prescribed predictive-component likelihoods and a
Dirichlet(2) weight penalty; its final integrated execution passed as
documented below.

## Reproduced pooled blocker and root fix

Before the fix, this UNCHANGED command failed:

```text
.venv/Scripts/python.exe -B -m analysis.alternative_classical_pooled_audit
```

Actual failing assertion: `alternative_classical_pooled_audit.py:72`,
`assert_allclose(..., atol=3e-4, rtol=3e-4)`.
Rain `pooled_emos_cyclic` original quantiles were
`[0, 4.7029427029746325, 17.07449609856448]`; duplicated rows with halved
weights gave `[0, 4.7076966200075985, 17.08508400045717]`.
Maximum violating difference was **0.0105879 mm**. Directly fitting the three
rain pooled subtypes independently reproduced the cyclic discrepancy.

Cause: expanded mathematically identical weighted reductions were not the
same floating-point optimizer problem. The cyclic fit followed a different
L-BFGS-B path in a weakly identified variance/seasonal direction. Merely
accepting both convergence flags did not establish replication invariance.

Fix: `alternative_classical_pooled_rows.canonical_rows` consolidates ONLY
exact replicas with the same provenance row ID, preserving their complete
weight with `math.fsum`, then orders unique row IDs deterministically.
All row metadata and member values must agree; contradictory replicas return
`INPUT_CONFLICT` with no fitted model. Different archive vintages/conditions
remain distinct. The canonical rows feed scaling, the objective, gradients,
and initialization together, producing the identical optimizer problem.
The 500-iteration budget, ftol 1e-10, gtol 1e-6, two starts, mathematical
objective, penalties, and existing assertion/tolerances were NOT changed.

### Actual post-fix output

Unchanged combined pooled/trend audit: **exit 0**, **1.7767341999988275 s**.
All 12 primary fits and six all-dry fits passed. Its checks include:
original-unit F9 objective and independently expressed finite-difference
gradients; unchanged duplicate-weight assertion; singleton forecasts;
ridge normal equations; restored rain atom/mean; variable censor boundaries;
20-year trend restoration; original QM/QDM parity and ties; serialization;
insufficient years; injected solver failures; independent Normal CRPS identity.

Additional exact driver:

```text
.venv/Scripts/python.exe -B -m analysis.alternative_classical_pooled_replication_audit
```

**Exit 0**, **0.9798611999995046 s**. Eighteen actual fits cover all three
pooled IDs in both variables, original/duplicated/permuted inputs.
Parameters and predicted quantiles were **array-identical** in every pair.
All six recorded maximum quantile differences were **0.0**.
Rain cyclic original and replicated quantiles were both exactly
`[0, 4.7029427029746325, 17.07449609856448]`.
Contradictory duplicates returned `INPUT_CONFLICT`, no fitted model.

Static checks after the fix:

```text
.venv/Scripts/python.exe -m basedpyright analysis/alternative_classical_pooled*.py analysis/alternative_classical_trend*.py
0 errors, 0 warnings, 0 notes

.venv/Scripts/python.exe -m ruff check analysis/alternative_classical_pooled*.py analysis/alternative_classical_trend*.py
All checks passed!
```

LSP was invoked before execution; its namespace falsely reports unresolved
`analysis.*` imports. Native project diagnostics above are decisive.

## Other actual verification already captured

```text
.venv/Scripts/python.exe -B -m analysis.alternative_classical_audit
```

Final shared-NLL/explicit-CRPS version: **exit 0**, **4.856023499998628 s**.
**333** point-density/atom log-likelihood identities compare fitting objectives
against the actually issued laws. Actual fits cover all local subtypes,
including compound Tweedie. All-wet occurrence penalty, negative rain rejection,
physical group gates, constant/single-member prediction, all-zero intensity
eligibility, and row permutation checks passed. Local native diagnostics
were zero errors/warnings and Ruff passed.

```text
.venv/Scripts/python.exe -B -m analysis.alternative_classical_kernel_audit
```

**Exit 0**. Both ID-free kernels, all-wet rain, and singleton members fitted
with actual annual-mixture likelihoods and converged solver diagnostics.
Representative synthetic fit timings: Normal 0.376 s, mixed-zero rain
0.837 s, all-wet rain 1.041 s, singleton Normal 0.379 s.

The first real smoke executed all 120 combinations (30 IDs, four actual
product/variable cases), but its final coverage assertion failed because
`bma_component_pool` lacked common successful prequential fits. All other
27 nongated IDs had actual successful real-case predictions. Both 60-file
preservation assertions ran before that final coverage assertion.
This first smoke predates the last restricted-MOS loss correction and pooled
replica fix; it is not a final-version pass.

## Final all-ID actual smoke: completed

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/Scripts/python.exe -B -m analysis.alternative_classical_real_audit
```

**Exit 0**, **186.94027930000084 s**, `scope=SMOKE`.
All 30 owned IDs were executed for each of:

```text
20220307_1MON_W01_prcp
20220307_1MON_W01_t15m
20220307_3MON_M01_prcp
20220307_3MON_M01_t15m
```

Actual 120-record ledger: **82 OK**, **34 NOT_APPLICABLE_DOMAIN**, **4
GATED_DATA**. There were **no failed/insufficient fits**. Every one of the
28 nongated IDs had a successful actual prediction; the two group-BMA IDs
remain honestly G3/G4-gated. Both preservation receipts assert all **60
protected byte counts and SHA256 hashes unchanged**.

Every successful law passed finite/nonnegative CRPS, finite mean, quantile
ordering, original rain support, and reconstructed quantile/mean/CRPS equality.
The original shared restoration function did not recognize a Bayesian mixture
leaf's `kind=bayesian_scalar`. The root has now added the Bayesian lazy decoder
to the shared `distribution_from_spec`, including nested mixtures. The owned
`alternative_classical_serialization.restore_distribution` is an explicit
re-export of that shared API, not a second recursive implementation or a
replacement posterior family.

The root subsequently reported a fresh actual all-ID run after the
residual-covariance release, source guard and censored-support corrections:
**exit 0**, **132.6136508 s**, again **120 records / 30 IDs / 28 successful
IDs / 82 OK / 34 domain exclusions / 4 physical-data gates**, with all **60
before/after hashes unchanged**. This is a root-provided receipt, not a second
execution claimed by this lane. The root also reported its actual
failure-boundary audit **PASS**, **0.669 s**. No additional production edit
was made for source freeze.

## Explicit actual BMA ancestry and serialization: completed

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/Scripts/python.exe -B -m analysis.alternative_classical_bma_actual_audit
```

**Exit 0**, **35.04284649999681 s**. EACH of the four actual cases has
**14 common prequential years (2003-2016)**, **14 ancestor receipts**, and
**zero fold failures**. Actual replay checks prove >=10 earlier source years,
`HIST_END < pseudo_init`, whole held-out source/valid-year exclusion, ancestor
hash equality, original case ID preservation, and the unchanged outer catalog
cutoff. The Bayesian component is fitted with its genuine known-input
conditioning, not substituted by a plug-in regression.

|Actual case|BMA weights: EMOS, restricted MOS, BJP|Original/restored mean|Original/restored CRPS|
|---|---|---:|---:|
|Weekly rain|0.26613152290501807, 0.35946206245424683, 0.3744064146407351|12.98545429997742|8.492965191856994|
|Weekly temperature|0.38488269240031064, 0.5111785364757736, 0.10393877112391563|7.2136629599901365|0.7538477378410089|
|Monthly rain|0.40677742898167324, 0.40924587547508134, 0.1839766955432453|108.02362829233971|28.142981712186014|
|Monthly temperature|0.5811844977849038, 0.3358737482746405, 0.0829417539404557|12.765640918213874|0.6595300315671501|

The original and JSON-restored numbers in each row were identical. Means were
also checked independently against the weighted sum of actual component
means. Rain zero atoms were 0.3095306160647682 (weekly) and
0.010322560349285852 (monthly); temperature has no zero atom. Actual fit times
were 0.6467964, 0.5790781, 0.8154072 and 0.5696977 seconds respectively.

## Full mixed-zero synthetic BMA audit: historical failures retained

The first mixture/BMA audit encountered a then-missing Bayesian helper.
The Bayesian helper subsequently arrived. A second integration issue was
identified: Bayesian fitted models hash the known-input original case ID;
prequential BMA must predict the exact ancestor pseudo-target rather than
substituting a validation row ID. The mixture helper owner was instructed
to preserve that identity. The corrected actual BMA and final real-data smoke
have now passed as shown above. The genuinely censored, mixed-zero synthetic
posterior/prequential run executed the prescribed folds and budgets, then
exited **1** at the unchanged required-success assertion:

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/Scripts/python.exe -B -m analysis.alternative_classical_mixture_audit --fits --rain-bma
```

```text
AssertionError: ('bma_component_pool', 'REQUIRE_EIGHT_COMMON_YEARS')
```

This is not an OK forecast and is not being hidden by the successful all-wet
actual-case receipts. The audit's failure message was expanded to include
the existing fold failures/diagnostics, without changing its predicate or
tolerance. A minimal first-fold diagnostic executed the same genuine Bayesian
API with ten past years:

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/Scripts/python.exe -B -m analysis.alternative_classical_bma_diagnostics
```

Diagnostic driver **exit 0**, **60.0452684999982 s** (it reports the failure,
not an OK forecast). Source years 1993-2002, pseudo-issue 2003:

```text
status = POSTERIOR_DIAGNOSTICS_FAILED
chains = 4; warmup_per_chain = 1024; retained_per_chain = 32768
rhat_max = 1.0000791214975324
ess_bulk_min = 102184.5402977528
ess_tail_min = 113070.83108769062
importance_effective_count = 127220.03288908766
maximum_weight = 1.3569018951720937e-05
mean_mcse = 0.046725143353949575 mm
probability_mcse = 0.00037434581565336857
crps_mcse = 0.009934836837120375 mm
crps_mcse_quadrature_difference = 0.00018583584305751304 mm
```

The sampler convergence/importance gates passed. Physical training SD is
**2.1007016360461663 mm**, so the frozen mean-MCSE bound is
**0.021007016360461664 mm**: the predictive mean-precision gate correctly
fails after the full budget. The other listed precision gates pass
(CRPS bound 0.010503508180230832 mm; quadrature-difference bound
0.001050350818023083 mm). No draw budget, precision threshold, asserted
success predicate, fixture scale, or failed status has been changed.

This was a Bayesian-component precision limit, not an identified defect in
the classical likelihood/ancestry/serialization code.

### Authorized residual-covariance release and unchanged retry

The root exclusively authorized Bayesian owner `st_01a11437` to implement
consultant `st_01a11472`'s distribution-level residual-covariance
Rao-Blackwellization. The classical owner did not edit Bayesian-prefixed files.
The sampler's Gibbs transitions, random draws, parameter monitors, checkpoints
(2048, 8192, 32768), warmup (1024), chain count (4), and diagnostic thresholds
remain unchanged. Emitted components remain a finite Normal mixture (`df=None`),
with analytically marginalized response regression/mean parameters and an
integrated Student predictor-density weight in the nonaugmented branch;
there is no mean-only control variate.

The owner reported the first strict ten-year fold still correctly returns
`POSTERIOR_DIAGNOSTICS_FAILED`: mean MCSE **0.0261082 mm** remains above
**0.02100701636 mm** despite the valid variance reduction and mathematical
equivalence checks. That failed fold is not relabeled OK.
The unchanged full `--fits --rain-bma` command was relaunched across all
14 eligible pseudo-issues. Its completed receipt below proves that at least
eight common component years succeed. The root explicitly permits honest
individual precision failures to remain reported rather than changing
assertions, fixtures or budgets.

### Final unchanged full mixture/BMA receipt: PASS

Monitor `mon_S4VT8VYQFA9W98B7` completed **exit 0**.
Command (no fixture, threshold, budget or assertion change):

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/Scripts/python.exe -B -m analysis.alternative_classical_mixture_audit --fits --rain-bma
elapsed_seconds = 742.4409330000017
atom_measure = PASS
dirichlet_closed_form = PASS
uniform_identical_components = PASS
unsupported_law = PASS
weight_stationarity_error = 2.772734020162204e-07
```

Both BMA fits returned **OK**, using actual strict folds and genuine
Bayesian API calls on the unchanged deterministic mixed-zero audit fixture:

| Variable | Common prequential years | Weights: EMOS, restricted MOS, BJP | Mean | CRPS at 5 | Fit seconds |
| --- | --- | --- | ---: | ---: | ---: |
| t15m | 2003-2016 (14) | 0.41276514948111603, 0.5152428632032529, 0.07199198731563122 | 5.257003359848725 | 0.18265818516411553 | 0.49220019999847864 |
| prcp | 2007, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016 (9) | 0.6157440985331603, 0.12581278884934763, 0.25844311261749214 | 8.848837004697819 | 0.6634137051479246 | 694.9942940000001 |

All eight fitted method/variable combinations passed JSON reconstruction of
predictive mean, CRPS, CDF and atom mass. Each physical-unit CRPS also passed
the independent CDF-integral oracle (`rtol=2e-5`, `atol=2e-5`, unchanged).
Both BMA common-year counts passed the unchanged `>=8` assertion.
The CDF-CV fits selected temperature weights `[1.0, 0.0]` and rain
`[0.6, 0.4]`, each on 2012-2016, with their strict-fold score replay passing.
The 17-year fixtures still returned genuine `INSUFFICIENT_INNER_FOLDS`
with no fitted model.

Temperature had no fold failures. Rain retained **five**, all with original
code **POSTERIOR_DIAGNOSTICS_FAILED**, method **bjp_sqrt_censored**:

| Pseudo-issue | Recorded reason | Mean MCSE (mm, rounded) |
| --- | --- | ---: |
| 2003 | POSTERIOR_DIAGNOSTICS_FAILED; predictive_mcse_passed=False | 0.026108154 |
| 2004 | POSTERIOR_DIAGNOSTICS_FAILED; predictive_mcse_passed=False | 0.030694503 |
| 2005 | POSTERIOR_DIAGNOSTICS_FAILED; predictive_mcse_passed=False | 0.022871983 |
| 2006 | POSTERIOR_DIAGNOSTICS_FAILED; predictive_mcse_passed=False | 0.021460541 |
| 2008 | POSTERIOR_DIAGNOSTICS_FAILED; predictive_mcse_passed=False | 0.036706372 |

Every rejected fold exhausted four chains with warmup 1024 and retained
32768 per chain. All five recorded sampler-convergence `passed=True` and
`importance_passed=True`, but failed the unchanged predictive precision
guard. They were not relabeled successful, assigned substitute forecasts,
or called scientific-data gates. Their full original diagnostic vectors
remain in the terminal monitor receipt. Nine genuinely successful common
rain years suffice for this fit under the frozen eight-year contract.
The terminal process exited normally; it is no longer a live watch or
background fit. No duplicate run or additional production edit was needed.

### Owned failure-status boundary correction

The classical wrapper now distinguishes insufficient DATA folds from failed
numerical component fits: if 14 eligible years exist but Bayesian inference
fails, it preserves `POSTERIOR_DIAGNOSTICS_FAILED` and
`PREQUENTIAL_COMPONENT_FAILED`, with all original fold diagnostics, rather
than presenting this as `INSUFFICIENT_INNER_FOLDS`.

```text
.venv/Scripts/python.exe -B -m analysis.alternative_classical_mixture_failure_audit
```

**Exit 0**, **1.0805734999994456 s**. The external numerical-failure boundary
was injected while actual strict inner-fold construction and classical
component fits ran: 14 eligible years/14 failed components propagate the
posterior failure with no fitted model. The original 17-year selected-CDF
fixture still yields the genuine `INSUFFICIENT_INNER_FOLDS` data status.
Success assertions and their tolerances were not changed.

A read-only independent review found no correctness defects in BMA's mixed
measure likelihood, Dirichlet(2) objective, frozen-catalog ancestry, known-input
Bayesian target identity, or exact serialization. It independently verified
all 14 synthetic fold target hashes/ancestries and fixed-F2 CDF/CRPS JSON
round trips. The mixed-zero branch was unverified at that review's time;
the final unchanged full receipt above now verifies it.

All owned `analysis/alternative_classical*.py` modules, including these new
audits and the exact serialization dispatcher, have native basedpyright
**0 errors, 0 warnings, 0 notes** and Ruff **All checks passed**.
Both native commands were rerun successfully while the final unchanged
mixed-zero retry was running:

```text
.venv/Scripts/python.exe -m basedpyright analysis/alternative_classical*.py
0 errors, 0 warnings, 0 notes
.venv/Scripts/python.exe -m ruff check analysis/alternative_classical*.py
All checks passed!
```

The serialization audit entry point now reexports the shared
`alternative_distributions.distribution_from_spec`, including its released
Bayesian scalar decoder, instead of duplicating the decoder. A fresh
`analysis.alternative_classical_mixture_audit --fixed-fits` run exited **0**
in **4.941479100001743 s**. Atom-measure likelihood, the Dirichlet closed form,
identical-component uniform weights and unsupported-law checks passed
(stationarity error 2.772734020162204e-7). Four fitted temperature/rain
fixed-50 and signal-shrink laws passed shared-decoder JSON checks of their
means, CRPS, CDF and zero atoms:

| Variable / method | Mean | CRPS |
| --- | ---: | ---: |
| t15m / cdf_mix_fixed50 | 5.556415812263868 | 0.3179848132177298 |
| t15m / anomaly_signal_shrink | 5.556415812263868 | 0.3315530236141335 |
| prcp / cdf_mix_fixed50 | 4.8958584453738085 | 0.3793868086783239 |
| prcp / anomaly_signal_shrink | 4.895858464996118 | 0.23154445265834148 |

Audit CLI `--help` exits 0; `--invalid` rejects the flag and exits 2 before
fitting. All owned modules remain below 250 nonblank/noncomment lines (the
largest is the local fitting module at 236).

No method is excluded for cost, no failed solver retains an initialization as
a fit, and no fallback is presented as the method. No existing/protected code,
data, observations, baseline outputs, research, environment, or git state was
modified. The classical lane's required mixture/BMA, actual all-ID,
preservation, native diagnostics and factual G3/G4 evidence is complete.
This is lane verification, not a claim that the root's full scientific
comparison across every source case has completed.
