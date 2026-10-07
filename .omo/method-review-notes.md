# Rigorous QM/QDM/EMOS review notepad
Started: 2026-10-06

## Goal and tier
HEAVY: user explicitly requests careful review of existing statistical calculations.
Answer with findings and proposals, not unrequested production corrections.
Preserve calibration.py, prior scores, figures and both PDF versions byte-for-byte.
Ideal state: independent executed mathematical and real-case evidence, classification
of implementation errors versus method limitations, quantified actual impact,
one evidence-gate reviewer and concise Korean verdict.

## Plan
1. Read full calibration implementation, source-year assembly and old validation.
2. Two independent diagnostic lanes: empirical QM/QDM mathematics and real-case
   ranking/dry-tail behavior (deep-high); EMOS analytic loss/gradient/physical scaling
   plus independent optimizer sensitivity (deep-low). Disjoint new audit files only.
3. Lead independently audits historical/source calendars and observation availability,
   saved training count/target exclusion, ensemble-size domain shift and source hashes.
4. Root personally reproduces a constructed QDM rank-crossing example and existing
   live forecast scoring through audit CLIs. Do not infer correction quality from success.
5. Compare every eligible real case's saved QM/QDM outputs with independent weighted
   empirical computations; investigate quantile/order crossings and zero denominators.
6. EMOS analytic CRPS versus independent integrals and finite-difference gradients,
   including zeros/negative latent means/tiny scales; real-case parameter/forecast
   sensitivity using genuinely different solver/starts, not two identical reruns.
7. Integrate both lanes; personally run audit drivers in production .venv.
8. Write findings-first Korean report with file:line refs, reproduction commands,
   counts/magnitudes and proposed action, limitations and unresolved questions explicit.
9. Launch exactly one evidence gate reviewer after actual QA; verify its concerns.
10. Record source/result hashes unchanged and cleanup finite processes/caches;
    deliver review, no production reimplementation or PDF regeneration.
Topology: independent diagnostics, not a review panel. Lead owns temporal audit/
integration/report; each worker owns its own new script and output subpath. Gate
reviewer is read-only and once; no ulw-plan reviewer/consultant workflow.
Skills: review-work (explicit completed-work review and one gate);
data-scientist (resident/CLI numeric audit, bounded data); programming/Python
(typed audit code); systematic-debugging (counterexamples before classification);
verification-before-completion (actual evidence); dispatching-parallel-agents.

## Success scenarios
C1 `.venv/Scripts/python.exe analysis/audit_qm_qdm.py`: independent comparisons on
all4644eligible cases, weighting/tie tests, endpoint sensitivity, QDM quantile
crossing/dry-denominator/negative-rainfall/tie behavior counts and concrete examples.
C2 `.venv/Scripts/python.exe analysis/audit_emos.py`: analytic loss/gradient versus
independent numerical oracle; units/censoring/fit constraints; real-case objective
and prediction sensitivity under independently initialized/solved fits.
C3 `.venv/Scripts/python.exe analysis/audit_training.py`: all joins/calendars and
strict62 means/training-known-before-init verified, source drift quantified.
C4 outputs/method_review/REVIEW_KO.md: findings supported by all evidence; one final
gate audit concerns resolved or explicitly inconclusive. No claim of global optimum
or perfect method from solver convergence alone.
Stop when full review is delivered. Missing evidence is labeled unresolved, never PASS.

## Findings at bootstrap
- Existing implementation: weighted tied midpoint empirical distributions, linear
  interpolation/endpoint clipping, equal weight per source year.
- QDM uses forecast-ensemble midranks, additiveT / ratioP, drydenom<.1mm usesQO,
  precipitation floor0. Normal/marginal forecasts may not preserve rank after QDM;
  must check actual crossings and implications, not label this automatically a coding bug.
- EMOS four parameters, positive scaled variance floor, two L-BFGS-B starts,
  annualmean exact Gaussian/censoredGaussian CRPS, physical-unit rescaling.
- Previous validator matches formulas/scores and held-out input independence, but
  does not by itself establish QDM rank preservation or optimizer global uniqueness.
- Historical models are retrospective, mostly1993-2016, later1993-2022; annual paired
  samples19-30 afterstrict62 checks; forecast and hindcastmembercounts differ.
- MonthlyT307cases/13uniqueperiods,BN26/NN0/AN281 remains a distinct sampling limitation.
- Pythonresidentkernel unreliable; monitored .venv CLI only.

## Now
Review complete; final artifact is outputs/method_review/REVIEW_KO.md.
Existing calibration, score, PNG and PDF files were not modified.

## Todo
Live11item checklist; independent review gate approved and own bytecode cleaned.

## Learnings
Separate formula implementation correctness, statistical assumptions, numerical
stability, parameter identifiability and observed out-of-sample skill.

## Root executed diagnostics
Actual `calibrate` counterexample:
H annual[0,0],[100,100],[200,200],O[0,1,2],F[10,11,12]:
QM[.10,.11,.12],QDM[10,-88,-186],successfully reproduces rank reversal.
Synthetic case is intentionally extreme; not evidence of actual forecast frequency.
QM/QDM lane must quantify all4644 real cases and distinguish assigned-rank algebra
from issued-distribution quantile interpretation.
Actual scoring.distribution_summary(mu=-10,sigma=1,rain=True) mean7.6946e-23
versus stable ndtr7.47456e-25: relative ratio102.94 but absolute7.61985e-23.
This is a reproduced extreme-tail numerical weakness, not a demonstrated
material real-data error. EMOS lane tasked with actual minimum mu/sigma.
Lead independent training CLI (bash_78) PASSexit0:
4644targets,109764accepted source-year pairs,all source-relative calendars,
observations known beforeinit,strictdaily62 values agree exactly(maxdelta0).
No use of production window/observation helper; protected originalfiles unchanged.
Actual source member sizes3/7 vs forecast24-84 must be judged as domain/sampling
shift, not automatically leakage or formula error.
Canonical QDM primary source fetched:
https://dspace.library.uvic.ca/items/12633e33-35f3-4352-8942-f80920523979
Cannon,Sobie,Murdock2015,doi10.1175/JCLI-D-14-00754.1 (GCM future precipitation
quantile changes). Current single-forecast-ensemble F is explicitly an adaptation;
do not equate algebra to a proven climate-trend conservation theorem.
Do not propose sorting correctedmembers as a score fix: rearrangement alone leaves
ensemble multiset/scores unchanged and cannot restore conflicting original-rank deltas.
## Final evidence and decisions
- All four audit CLIs personally executed by root; QM/QDM retained strict exit1
  for one accurate-sum difference1.03455e-10mm, not weakened or hidden.
- Real QDM rank crossings4553/4644(98.0%), QM0; assigned-rank algebra agrees,
  issued sorted quantile preservation is not established. Scores remain valid
  for the issued multiset; sorting alone is not a repair.
- QDM dry replacements493members/218cases; rawzero->positive309/130.
- EMOS full4644 fits reproduced; independent integration/gradient/physical units
  verified. Training-selected32cases,96alternativeSLSQP solves all converged,
  no lower training objective found; no global-optimality/identifiability claim.
- Source109764 acceptedpairs; no temporal/observation mismatch. Forecast usable
  size includes18 aftermissingness, beyond usual24-84; HCST3/7 differs.
- iid fair CRPS is sensitivityonly: weeklyP ordering changes; exchangeability
  unproven, do not replace empirical score or equate good skill to QDM conservation.
- One finalgate st_01a11097 APPROVE/HIGH;109protected hashcomparisons match.
- Root final four-fileLSP clean,basedpyright0errors/0warnings/0notes,Ruffpass.
  Reviewer-sessionLSP lacked localimports/SciPystubs; runtime probes passed;
  different-sessionLSP claim not fully reproduced and explicitly reported.
- FourCLI help/error paths checked; publicnegative rainfall rejected.
- All owned numeric monitors and review tasks terminal; only generated
  audit_emos.cpython-313.pyc removed, not unrelated caches or sessions.
- Results apply only current4644-case analysis/run_verification.py pipeline,
  not older mapping/evaluation settings or operational availability claims.
- Proposal only: clarify QDM variant/conservation/zero policies first; if true
  monotone distribution preservation is needed, decide a new method and validate
  anew. No production method/score/report alteration without the next user decision.
