# Frozen comparison output schema

This contract coordinates the independent validator and root runner. No fitted
skill result is asserted by writing this schema. The validator's recorded field
requirements are accepted, not weakened to accommodate whatever gets produced.

## Continuous and categorical rows

Lowercase identity/provenance:
`case_id,method_id,variable,fit_ref`.

Existing summary-compatible uppercase fields:
`CASE_ID,METHOD,VARIABLE,PRODUCT,INIT_DATE,VALID_START,VALID_END,LEAD,N_TRAIN`.
Uppercase and lowercase identity values must agree.

Continuous scores:
`OBS,Q33,Q67,PRED_MEAN,CRPS,P_BN,P_NN,P_AN,P05,P95,BRIER,RPS`.
Retain the existing baseline scoring fields needed by `generate_summaries`.

For original finite RAW/QM/QDM laws, keep published baseline linear-statistic
P05/P95 unchanged and additionally record actual inverse-CDF quantiles as
`CONTRACT_P05,CONTRACT_P95`. Do not call the old linear statistic the exact
inverse of a finite empirical CDF.

Category-only methods have their own probability/score table. They do not
receive invented PRED_MEAN, continuous CRPS, or intervals.

## Law records

JSONL: `case_id,method_id,fit_ref,distribution`.
The distribution is the complete tagged original-unit law; Bayesian scalar
`kind="bayesian_scalar"` routes to its own decoder. Numerical/posterior precision
failures while scoring remain explicit failures, not substituted method laws.

## Inventory / statuses / fit provenance

- Inventory: `method_id,family_no,surface`, plus subtype/domain/owner/scope/gates,
  algorithm version and fixed settings.
- Status: `case_id,method_id,status,reason_code,surface,fit_ref`.
- Fit: `method_id,status,train_hash`, plus fit_ref and actual diagnostics.
- Training: `row_id,train_hash,source_case_init,source_year,hist_start,hist_end,
  cutoff,catalog_cutoff,held_out_years,product,variable,year_weight`.
- Fold: `fold_id,training_row_ids,validation_row_ids,pseudo_init,held_out_years,
  ancestor_hash,outer_train_hash,catalog_cutoff`.

Lists are JSON arrays in CSV cells; held-out years are integer arrays. Catalog
cutoff is actual outer issuance; inner response cutoff is the historical
pseudo-issuance. Raw forecasts are never historical legacy probability samples.

## Failure and coverage policies

`method_id,policy,eligible_count,scored_count`, with scientific gates distinct
from numerical/fit failures. Retain same-domain paired/common-mask summaries.
Success-only statistics explicitly report their restricted N. Any
climatology-on-failure operational derivative is a separately labeled object;
it is not the failed method's forecast or a replacement in its law record.

## Joint records

`joint_id,method_id,scenario_key,units,approximation_metadata`, with the actual
2D finite array and weights in `joint_scenarios.npz`.

Keep original analytic marginal scores separate from scenario-projected
marginal scores. Score each issued joint law on its matching vector and disclose
joint events/energy/variogram, marginal reference and numerical approximations.

The 16 latest absent-history component IDs in
`.omo/evidence/alternative-latest-absent-history.json` remain in full status/
case coverage; partial-horizon construction must not silently erase them.

## Artifact coverage

The complete experiment accounts for all 6,580 supplied cases, current 6,432
eligible truths, 148 unavailable future targets and all 66 registered IDs
(61 researched subtypes plus 5 controls). No old input, observation, research
or baseline output is overwritten. Protected 60-file snapshot is the regression
receipt, not a substitute for numerical or actual-user-surface validation.
