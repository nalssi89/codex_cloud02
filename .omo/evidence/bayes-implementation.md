# Bayesian implementation: delivered, with explicit finite-budget failure

Scope: only `analysis/alternative_bayes.py`, `alternative_bayes_*` and this
evidence file. No protected input/baseline modifications or full-project rerun.

Implemented fixed physical NIW/MNIW/NIG algebra, conditional Student-scale
calculation, proper Bartlett inverse-Wishart sampling, strict coordinate Gibbs,
positive-X importance conditioning and target-augmentation branch, four-chain
rank/split diagnostics, predictive MCSE gates, local and multivariate fit DTOs,
and explicit evidence-backed G5 exclusions.

Fitted-model serialization stores the actual **target-conditioned** law and
known-input fingerprint. A different issued predictor requires refitting;
there is no stale reuse of p(Y|D,X) for a different X. No observed truth enters
the fingerprint, fitting functions or posterior MCSE probes.

## Executed mathematical checks

```
.venv/Scripts/python.exe -B -m analysis.alternative_bayes_algebra_audit
{
  "status": "PASS",
  "conditional_density_max_relative_error": 6.661338147750939e-15,
  "inverse_wishart_moment_max_error": 0.0037682413369410916,
  "zero_rectangle_max_error": 5.551115123125783e-17,
  "elapsed_seconds": 2.206921599999987
}
```

The conditional-density oracle divides SciPy's joint Student density by its
predictor marginal; predictive variance is integrated independently; IW moments
use 20,000 Bartlett draws; zero rectangles compare with the analytic arcsine
orthant law and a revealed-coordinate conditional counterexample.

This receipt records focused mathematical and actual-source verification, not
a full alternative experiment or a claim of comparative forecast skill.

## Public interface and inventory

`fit_bayes(spec: MethodSpec, training: TrainingSet, config: FitConfig) -> FitResult`
and `fit_mbjp(spec: MethodSpec, training: JointTrainingSet, config: FitConfig)
-> JointFitResult` are executable. `bayesian_method_specs()` supplies these 12
IDs (the root remains the owner of the complete registry):

```
joint_gaussian_plugin bjp_niw bjp_sqrt_censored bayesian_anomaly_ridge
bjp_yj_fixed bjp_logsinh_fixed bjp_t bjp_ti
mbjp_niw mbjp_sqrt_censored
finite_member_iid_signal_noise finite_member_known_covariance
```

`spec.id` is authoritative; `subtype` is not dispatched. Unknown IDs raise
typed `AlternativeError` codes `UNKNOWN_BAYES_METHOD`/`UNKNOWN_MBJP_METHOD`.
Both finite-member IDs return `GATED_DATA/G5_MEMBER_ERROR_LAW_UNPROVEN`.
No iid member replication, array-position identity, or 1/M variance claim is made.

`model_from_spec()` restores `ScalarModel`/`MultivariateModel` from
`tag=bayes_conditional_fit, version=1`. Scalar laws serialize as
`kind=bayesian_scalar`, restored by
`alternative_bayes_distribution.distribution_from_spec`. Every unthinned
posterior component/weight and physical transform is retained, not a quantile
surrogate. Joint models issue 256 fixed-seed Sobol scenarios and carry a
512-scenario mean sensitivity plus exact marginal specifications.

NIW: kappa0=1, nu0=d+8, Psi0=7I. MNIW row variances are (1,4) for BJP-t,
(1,.04) for BJP-ti. NIG regression uses V0=diag(4,1), IG(4,3); its one-dimensional
IW representation uses df=8, scale=6. The plug-in control has no Bayesian prior.

## Additional independent numerical receipts

```
.venv/Scripts/python.exe -B -m analysis.alternative_bayes_sampler_audit
status PASS
joint_zero_probability 0.060143481756345596
collapsed_student_latent_mean -0.46390480390592154
gibbs_latent_mean -0.46305523100845425
mean_mcse 0.005043169995754045
standard_errors_from_oracle 0.16846009517477337
rhat_max 1.0001177406442343
ess_bulk_min 6292.8200798839225
ess_tail_min 6869.625579001035
elapsed_seconds 3.797134800001004

.venv/Scripts/python.exe -B -m analysis.alternative_bayes_diagnostics_audit
PASS: independent rank/R-hat/ESS formulas, AR(1), tails, batches, input gates

.venv/Scripts/python.exe -B -m analysis.alternative_bayes_distribution_audit
oracle_crps_checks 24
maximum_absolute_crps_error 2.8200020096846856e-09
actual_observation_precision_gate PASS
8192_draw_cdf_ppf_seconds 0.5181500999988202
elapsed_seconds 3.8970293999991554
status PASS
```

The sampler oracle analytically integrates the bivariate Student predictive
over a **joint** zero rectangle, then compares its latent mean with the Gibbs
latent draws. It therefore checks more than a formula copied from the sampler.
The distribution audit uses independent original-unit CRPS integrals.

## Synthetic posterior conditioning receipts

The ordinary analytic driver
`.venv/Scripts/python.exe -B -m analysis.alternative_bayes_audit` passed all
11 scalar algorithm/domain combinations, 2/12/16-response-dimensional
temperature paths, finite-member G5 gates and fitted-model/scenario restoration.

For censored synthetic rain, square-root/YJ/log-sinh/NIG all passed four
chains with 1,024 warmup and 2,048 retained draws each. No thinning was used.
The following separate driver exercised the remaining weak-trend and zero
issued-predictor branches:

```python
import json
import numpy as np
from dataclasses import replace
from analysis.alternative_bayes_audit import synthetic, scalar_check
t = synthetic(True, True)
print(json.dumps(scalar_check(t, "bjp_ti"), indent=2))
z = replace(t, target=replace(t.target, members=np.zeros(3), case_id="zero_target"))
print(json.dumps(scalar_check(z, "bjp_sqrt_censored"), indent=2))
```

Executed with `.venv/Scripts/python.exe -B -c '<driver>'`:

|Case/method|Seconds|R-hat max|Bulk ESS min|Tail ESS min|Mean MCSE|Probability MCSE|CRPS MCSE|
|---|---:|---:|---:|---:|---:|---:|---:|
|synthetic BJP-ti|5.5333843|1.000473806|7249.587|7521.751|.429363738|.001684394|.177996459|
|zero issued mean, sqrt BJP|5.0202153|1.000942646|6118.836|7357.606|.268553016|.001909888|.108991146|

Both passed every threshold at 2,048 retained draws/chain. The zero-target
record reports `conditioning=augmented_target`, not conditioning on X=0:
its predictor is sampled on X<=0 along with an unobserved target response.
The positive-X weak-trend record reports density importance conditioning,
effective importance count 7758.8234, maximum weight .000216836.

### Intentionally retained numerical failure

The comprehensive `--censored` synthetic driver returned exit 1 at the strongly
trending/extrapolative BJP-t fixture. Four streams were extended through
2,048, 8,192 and 32,768 retained draws/chain. Final diagnostics:

```
status POSTERIOR_DIAGNOSTICS_FAILED
fitted_model None
rhat_max 1.000044041996734
ess_bulk_min 114806.03917305754
ess_tail_min 118687.56691089096
importance_effective_count 68333.86028364582
maximum_weight 4.7442689546561476e-05
mean_mcse .41050900584172767
probability_mcse .0009433586356879883
crps_mcse .312082563390517
crps_mcse_quadrature_difference .006204155586041076
predictive_mcse_passed false
```

This failure is not relabeled as convergence or a data gate, and the audit
expectation was not weakened to make it green. No Normal substitution occurs.
The chain diagnostics are retained in failed `FitDiagnostics`, not just prose.

Fit-time CRPS precision probes are training terciles/median, with no truth.
The scalar law additionally checks posterior CRPS MCSE at the **actual scoring
observation**, only inside `.crps(observation)`; it raises the typed posterior
diagnostic error if the .005*training-SD limit is exceeded. Chain shape and
training SD survive distribution serialization. This avoids claiming that
training probes alone certify every unseen score.

## Preservation and static/size checks

The complete lane native commands:

```
.venv/Scripts/python.exe -m basedpyright analysis/alternative_bayes*.py
.venv/Scripts/python.exe -m ruff check analysis/alternative_bayes*.py
```

Final native all-lane checking reported **0 errors/0 warnings** and Ruff
**All checks passed!**. LSP was run
before execution and exposes the known false `analysis.*` namespace import
failures; none were masked with a path hack or ignored diagnostic.

Every Bayesian module is <=250 nonblank/noncomment lines (maximum 212).
All 60 protected byte counts
and SHA256 values matched:

```
PROTECTED 60 UNCHANGED 60 FAILED []
```

Receipt driver used standard-library `hashlib.file_digest(..., "sha256")` and
compared `stat().st_size` and hashes with
`.omo/evidence/alternative-baseline-hashes.json`. No environment install,
baseline output write, git operation, or whole-project production rerun occurred.

## Final actual-source execution

```
.venv/Scripts/python.exe -B -m analysis.alternative_bayes_audit --real
status PASS
exit_code 0
elapsed_seconds 193.34814779999942
```

Ten scalar fits and two full-path fits were exercised:

* Weekly temperature `20220307_1MON_W01_t15m`: NIW, analytic.
* Weekly all-wet rain `20220307_1MON_W01_prcp`: sqrt BJP, analytic.
* Weekly dry stratum `20220307_1MON_W03_prcp`: sqrt BJP, fixed YJ,
  fixed log-sinh, NIG anomaly ridge, BJP-t and BJP-ti, genuine censored Gibbs.
  **Both trend variants succeeded on this real dry sample**; the synthetic
  stress failure above is not a blanket trend-method veto.
* Monthly first-lead T/P: NIW temperature and sqrt rain, analytic.
* The first complete weekly issuance: 16 response components / 32 joint
  coordinates, censored MBJP with four chains, 2,048 retained draws each.
* The first complete monthly issuance: 12 response components / 24 joint
  coordinates, exact conjugate MBJP.

The scalar run evaluated the **verified target observations only after fitting**
inside distribution scoring. It checked ordered PPFs, finite original-unit means
and CRPS, rain support/atom behavior, fitted-model restoration, and exact scenario
restoration. The target's observed truth never enters the fit/model DTO.

Selected real dry-stratum posterior diagnostics saved from this final run:

|Method|Fit seconds|Retained/chain|R-hat max|Bulk ESS min|Tail ESS min|Mean MCSE|Probability MCSE|CRPS MCSE|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|sqrt BJP|4.5701241|2048|1.0005452643|7318.8574|7671.4327|.101716071|.001523752|.036470490|
|YJ BJP|13.8566215|8192|1.0000824488|30876.4547|31410.7887|.043744661|.000594433|.020185979|
|log-sinh BJP|4.3419993|2048|1.0002243141|7304.1604|6608.7239|.061604789|.000886635|.026785136|
|NIG ridge|10.8494733|8192|1.0001714852|28656.4259|29158.5766|.052329249|.000468870|.016782750|

For the real dry sqrt fit, training SD is 10.530765518539507 mm, the correctly
target-conditioned mixture mean is 28.25343067713825 mm, and actual-observation
CRPS is 16.867395758213032 mm. Importance effective count is
8059.950692485515, maximum weight .0001871966315573696, and the CRPS MCSE
quadrature difference is .0001401039513257981.

Its complete per-monitor convergence lists (means, log SD, correlation,
eigenvalues, latent zero and predictive zero probability) are:

```json
{
  "rhat": [1.0002166910526624,1.0001203676058037,1.0005035044929647,
    1.000324383018006,1.0001220894925618,1.00035459704408,
    1.0001209551820849,0.9999977029646103,1.0005452642534902],
  "ess_bulk": [8285.219183036172,7737.246714255362,8269.097373181976,
    7318.857396531663,8325.157208704275,8259.309632269786,
    7689.15705362357,7776.17469082816,7676.279486890032],
  "ess_tail": [8021.620155974271,7671.432717959891,8247.033730931591,
    7739.039544198464,7967.37159419485,7760.198336794469,
    7979.531858887525,7936.250506139831,7854.246809222444],
  "passed": true,
  "predictive_mcse_passed": true,
  "conditioning": "importance_density"
}
```

The 16-component weekly path also passed every component's precision gate.
Importance effective count was 6333.285312799254, maximum weight
.0008216002599033634. Largest mean MCSE across components was .17128010082252906
in native component units, largest probability MCSE .0017410372054242988,
and largest training-probe CRPS MCSE .07486629530732207.
The monthly joint analytic fit took .0009375999998155748 seconds.
The IW prior-df fractions are explicitly reported (.625 weekly, .57142857
monthly); large paths are not falsely described as data-dominated estimates.

The final analytic/API run exited 0 in **2.1056432999994286 seconds**. Its added
adversarial checks show that mismatching `subtype` does not alter the authoritative
NIW ID's fitted law, an unknown ID raises a typed error, fewer than ten annual
years reports `INSUFFICIENT_TRAINING`, repeated annual vectors report
`INPUT_CONFLICT`, and finite-member variants retain their G5 gates.
Audit `--help` exited 0; `--unknown` exited 2 with an explicit unrecognized
argument message. Independent mathematical audits retain their own executable
entry points listed above.

## Residual limitations and operational contract

* No known algorithm stub or unresolved data/distribution dependency remains.
* The fixed maximum-budget synthetic BJP-t precision failure is deliberately
  retained and returned honestly. A full run must keep such numerical failures
  in its ledger; it must not replace them with a fitted Normal or omit them.
* Actual-observation CRPS precision can fail at scoring even when training
  probes pass. This is an explicit typed posterior-diagnostic failure, not a
  hidden fit fallback.
* Models are local **known-input-conditioned** laws; a new predictor needs a
  new fit/cache key. No real-time historical release claim is made.
* CRPS influence quadrature uses 128/256-node refinement; Gaussian log-sinh
  posterior component means used for MCSE use fixed survival quadrature.
  Issued means/CRPS use the independently audited adaptive integrals.
* Full Bayesian posterior diagnostics and mixtures are serializable and can be
  large for path fits. Joint scenarios are disclosed finite approximations,
  not replacements for the exact/posterior-mixture marginal distributions.
* No full experiment, comparative skill conclusion, or projected full-run
  completion claim is made. All owned audit processes finished; no live
  posterior workers or service resources were left behind.

Final native small driver, executed with `.venv/Scripts/python.exe -B -c`:

```python
import json
from dataclasses import replace
import numpy as np
from analysis.alternative_bayes import (
    bayesian_method_specs, fit_bayes, fit_mbjp, model_from_spec,
)
from analysis.alternative_bayes_audit import synthetic, synthetic_joint
from analysis.alternative_contracts import AlternativeError, FitConfig
specs = {s.id: s for s in bayesian_method_specs()}
t = synthetic(False)
r = fit_bayes(replace(specs["bjp_niw"], subtype="bjp_t"), t, FitConfig())
assert r.fitted_model is not None
m = model_from_spec(json.loads(json.dumps(r.fitted_model.to_spec(), allow_nan=False)))
np.testing.assert_array_equal(
    m.predict(t.target).quantile(np.array([.1, .5, .9])),
    r.fitted_model.predict(t.target).quantile(np.array([.1, .5, .9])),
)
j = synthetic_joint(2)
jr = fit_mbjp(specs["mbjp_niw"], j, FitConfig())
assert jr.fitted_model is not None
jm = model_from_spec(json.loads(json.dumps(jr.fitted_model.to_spec(), allow_nan=False)))
np.testing.assert_array_equal(
    jm.predict(j.targets, (), FitConfig()).samples,
    jr.fitted_model.predict(j.targets, (), FitConfig()).samples,
)
try:
    fit_mbjp(replace(specs["mbjp_niw"], id="unknown"), j, FitConfig())
except AlternativeError as e:
    assert e.code == "UNKNOWN_MBJP_METHOD"
else:
    raise AssertionError("missing typed MBJP error")
print("PASS authoritative IDs; JSON scalar/joint law roundtrips; UNKNOWN_MBJP_METHOD")
```

Observed exit 0:
`PASS authoritative IDs; JSON scalar/joint law roundtrips; UNKNOWN_MBJP_METHOD`.

## Authorized residual-covariance Rao--Blackwell revision: verified, first fold still fails

Root granted exclusive Bayesian ownership for the exact recommendation of
`st_01a11472`. This revision changes only:

* `analysis/alternative_bayes_algebra.py`: distribution-level collapsed component.
* `analysis/alternative_bayes_sampler.py`: emitted components/weights, not transitions.
* `analysis/alternative_bayes_engine.py`: estimator metadata on success and failure.
* `analysis/alternative_bayes_rao_audit.py`: independent law and transition checks.
* This evidence file.

No classical, shared-contract, registry, precision-threshold, distribution,
observation, baseline, or other-lane file is modified.

For each completed-data posterior `(Bn,Vn,nu,Psi)` and the already drawn Sigma:
`m=h*Bn`, `c=1+h*Vn*h'`, `a=x-mx`, `ell=my+Psi_yx*solve(Psi_xx,a)`,
`k=c+a'*solve(Psi_xx,a)`, and `Omega=Sigma_yy.x`. The emitted component is
**Normal(ell,k*Omega)**. Nonaugmented predictor log weights use the integrated
Student predictor density with `df=nu-d+1`, location `mx`, scale `c/df*Psi_xx`.
Augmented prediction uses its current augmented posterior and sampled latent
predictor with unit weight. Predictor-free NIG is `Normal(h*Bn,c*Sigma)`.

This marginalizes regression/cross-regression nuisance parameters across the
entire law. It does not correct only the mean, and it does not replace the
finite Normal mixture with Student components. `df=None`, component count,
component/chain order and serialization interfaces are unchanged. Parameter
draws, Gibbs coordinate updates, seed streams, monitors, warmup, retained
budgets and precision thresholds remain unchanged. Saved metadata names
`predictive_estimator=residual_covariance_rao_blackwell_v1`.

Pre-change state/RNG SHA256 receipts at iterations 1,10,100, seed 1917:

```
augmented  16e8816aee15e53affff950cc0a6474ceb787ad23c86a4f68082e810500d23b8
importance 51cb418b9b822b3f1fb20dcb25c43a9e0a7fca36d1e6d43bd6f5dde4ba4754b1
nig        9e68391a2192358f7a7cf9fe6da6d6f03fcd7d0c9139800517d22dd6a2673312
```

The audit hashes latent values, sampled coefficients, sampled covariances and
the RNG state, not the intentionally changed emitted predictive components.
All three post-change fingerprints match **exactly**. It also verifies that
augmentation retains exactly one extra row, uses its actual sampled latent
predictor in the conditional location, and emits log weight zero.

### Independent law proof and regressions

All commands below were executed with
`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1`:

```
.venv/Scripts/python.exe -B -m analysis.alternative_bayes_rao_audit
PASS, exit 0, 0.6215876999995089 seconds
largest zero-atom discrepancy       2.7755575615628914e-16
largest density discrepancy         1.7763568394002505e-15
largest physical rain mean error    7.389644451905042e-13 mm
multivariate covariance discrepancy 2.220446049250313e-16
all three transition fingerprints   UNCHANGED

.venv/Scripts/python.exe -B -m analysis.alternative_bayes_sampler_audit
PASS, exit 0, 4.589385200000834 seconds
latent mean vs collapsed-Student oracle 0.16846009517477337 MC standard errors

.venv/Scripts/python.exe -B -m analysis.alternative_bayes_algebra_audit
PASS, exit 0, 2.1435089000005974 seconds
```

The new oracle independently integrates the inverse-Wishart residual-scale
Normal mixture and compares it with the **joint Student density divided by
its predictor marginal**. Predictor dimensions 0, 1 and 3 cover NIG and
multivariate/trend algebra. It checks the zero atom, positive density and
physical square-root-rain mean, not merely an adjusted mean. Changing discarded
nuisance covariance blocks while holding Omega fixed leaves the emitted law
unchanged. A separate multivariate predictive covariance check catches Student
scale/covariance or residual-IW degrees-of-freedom mistakes.

### Exact unchanged first-fold diagnostic

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  .venv/Scripts/python.exe -B -m analysis.alternative_classical_bma_diagnostics
```

The existing classical driver was **read and executed, never edited**.
Its fixture is `synthetic_training(True)`, first `inner_folds(..., min_years=10,
last_n=None)` fold, source years 1993-2002, pseudo-issue 2003.
Driver exit 0 reports the following **failed fit**, not an OK forecast:

```json
{
  "fold_id": "mixture-audit-prcp/prequential/2003",
  "status": "POSTERIOR_DIAGNOSTICS_FAILED",
  "reason": "POSTERIOR_DIAGNOSTICS_FAILED",
  "rhat_max": 1.0000791214975324,
  "ess_bulk_min": 88909.17643897035,
  "ess_tail_min": 109352.28926521062,
  "importance_effective_count": 131071.99999999997,
  "maximum_weight": 7.629394531250002e-06,
  "mean_mcse": [0.026108153917616103],
  "probability_mcse": [0.00011439668268417066],
  "crps_mcse": [0.004033780183836599],
  "crps_mcse_quadrature_difference": [0.00004283476736122881],
  "passed": true,
  "importance_passed": true,
  "predictive_mcse_passed": false,
  "chains": 4,
  "warmup_per_chain": 1024,
  "retained_per_chain": 32768,
  "predictive_estimator": "residual_covariance_rao_blackwell_v1",
  "predictor_weight": "integrated_student_density",
  "seconds": 75.02395759999854
}
```

Mean MCSE decreased from **.046725143353949575** to
**.026108153917616103 mm**, but remains above the unchanged
**.021007016360461664 mm** bound. The failure is retained with no fitted model.
All other precision/convergence/importance gates passed. Original parameter/
latent monitor streams are unchanged; the predictive-zero monitor appropriately
describes the new emitted mixture, so its ESS can differ.

Here all historical predictors are revealed. Their analytically integrated
predictor density is constant across completed latent-response draws, explaining
the exactly uniform importance weights; this is the proven factorization, not
an unweighted-cut substitution.

### Actual-source dry and full-path QA after this revision

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  .venv/Scripts/python.exe -B -m analysis.alternative_bayes_audit --real
PASS, exit 0, elapsed_seconds 105.13468030000149
```

The same ten scalar/two joint actual-source checks passed. All six rain methods
on dry stratum `20220307_1MON_W03_prcp` passed at **4 x 2,048 retained draws**:

|Method|Fit seconds|Mean MCSE (mm)|CRPS MCSE (mm)|
|---|---:|---:|---:|
|sqrt BJP|6.0158752|.08784102138|.01824466496|
|fixed YJ|6.5585177|.05030074944|.01392380234|
|fixed log-sinh|5.7402066|.02707887331|.00811858855|
|NIG ridge|5.1628914|.05078633125|.01084977135|
|BJP-t|6.9331258|.06280370559|.01481402056|
|BJP-ti|7.2794776|.05168173072|.01081715904|

Actual-observation CRPS precision, rain support/atoms, means/quantiles and
fitted-law restoration passed, using the **same emitted mixture throughout**.
The 16-response weekly censored MBJP passed in 21.22636489999786 seconds,
R-hat max 1.0011877178935298, bulk ESS min 7071.77817808031, tail ESS min
7000.626730220443. Its 4 x 2,048 components retained exact chain ordering.
The 12-response monthly analytic path also passed and was not changed.

Final native whole-Bayes checks: basedpyright **0 errors, 0 warnings, 0 notes**;
Ruff **All checks passed!**. All sixty byte counts/SHA256 hashes again matched:
`PROTECTED 60 UNCHANGED 60 FAILED []`. No LSP namespace masking, environment
change, numerical threshold relaxation, fixture change or out-of-scope edit.
All owned verification processes exited.

**Owner release:** this exact estimator revision is ready for the classical
owner's unchanged `--fits --rain-bma` retry. That collective 14-fold audit remains
with its owner; this lane does not claim it passed. It must retain diagnosed
early failures and require the unchanged >=8 successful common years.
