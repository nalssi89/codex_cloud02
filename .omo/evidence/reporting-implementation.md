# Fair comparison reporter implementation evidence

Date: 2026-10-07. Owner: reporter child st_01a11477.
Scope: code readiness and REPORTING_SMOKE only; not FULL experiment validation.

## Delivered API and ownership

`analysis.alternative_reporting.generate_reports(output: Path,
inputs: ExperimentInputs) -> dict[str, Json]` is executable and wired by the runner
through its lazy import. Only `analysis/alternative_reporting.py`,
`analysis/alternative_reporting_*.py`, and this evidence file were edited.
No runner, model, data, validator, root notepad, baseline, source, or PDF was
edited by this owner. No commit was created.

Outputs are confined to the requested new output child. Protected-file receipt
overlap and source overlap are rejected. Reports publish from a temporary
directory under that output into `reports/`; an existing report directory is
backed up only for the observed atomic rename transition, with rollback on
rename error. No temporary report directories remained after execution.

## Implemented behavior

- Actual catalog/status coverage precedes scores. Domain eligibility, scientific
  gates (including insufficient scientific training/folds), missing truths,
  fitting/posterior failures, numerical/scoring failures, input conflicts,
  missing score after OK, and unrecorded states are separate fields.
- Pairwise and prespecified registry-family common-success masks retain exact
  sorted case/vector IDs and compact UTF-8 JSON SHA256. Empty intersections are
  visible. No entire-experiment global intersection is substituted.
- Separately named `method+climatology_on_failure` uses the actual local annual
  empirical observations, including tied-threshold category probabilities.
  Unrecorded/unsupported cases are not silently substituted. Original method
  states and law records remain unchanged.
- Actual joint fallback is the empirical law on complete aligned annual response
  vectors, standardized in the same outer-training coordinates. It does not
  independently resample scalar coordinates or invent a scalar joint law.
- Nonnegative missing-loss bounds use successful loss sum divided by scientifically
  eligible N and textual `+inf`; no finite failure penalty is invented.
- Ordinary continuous `generate_summaries` is called unchanged; new reports retain
  separate continuous CRPS, category-only RPS/Brier, and actual saved joint
  ENERGY/VARIOGRAM/event Brier. Product/native-unit scopes never pool T/P or
  weekly/monthly quantities.
- Lead/month/season/year and exact-window-equal-weight summaries are present.
  Fixed-seed 999-draw year and connected-overlap block resampling retains repeated
  windows; year influence and leave-one-year-out differences are descriptive,
  not significance claims with the actual approximately five verification years.
- Public tagged-law decoder handles Bayesian scalar laws. Diagnostics use actual
  analytic/original laws, atom-aware randomized PIT, generalized-inverse intervals,
  common outer terciles, and upper rain above the fixed outer-training P90.
  Missing laws or decoding/numerical errors remain explicit.
- Fixed-bin category reliability and continuous reliability are saved separately.
- Joint NPZ sample/weight arrays are actually inspected for finite support,
  dimensions, nonnegative masses and total mass. Approximation metadata is
  retained. Analytic and scenario-projected marginal tables remain separate and
  are further stratified by the actual parent vector component/lead scope.
- Korean findings and figures are derived only from actual saved scores. Coverage
  appears first; actual EMOS common-mask differences are descriptive, not a
  superiority claim. Agg PNGs carry explicit scope and seed.
- FULL readiness requires all frozen artifacts, registry coverage, statuses, laws,
  common thresholds, valid joint arrays and complete operational policies.
  Reporter returns `REPORTS_GENERATED`, never independent-validation PASS.
  Missing artifacts or SMOKE scope returns `INCOMPLETE`.

## Runner coordination, based on inspected actual fields

Read the frozen plan sections 9–11, output schema, actual `scoring.py`,
ExperimentInputs/contracts/catalog/registry and the peer's actual runner source.
The runner API is accepted. Joint score fields are ENERGY, VARIOGRAM,
HOT_DRY_P, HOT_DRY_BRIER and any other actual saved `*_BRIER` fields.

The reporter does not parse method/case naming conventions to identify vectors.
It joins exact `(case_id,method_id)` in `joint_key_status.csv.gz` to
`fit_schedule.csv` to obtain `component_case_ids`; successful joint rows already
carry those IDs. Actual inputs derive product, ordered variable/lead schema,
all exact component windows and calendar strata. Coupling `__emos`/`__bjp`
inventory variants are accepted explicitly under their registry family.

`joint_component_coverage.csv` separately retains aggregated scalar component
statuses, including unavailable/incomplete components; these are not called
vector predictions. Genuine mixed-unit train hashes are preserved in
`joint_training_manifest.csv.gz`; joint residual ancestry belongs in
`joint_fold_ancestry.csv.gz`, not a fabricated scalar training hash. This
validator integration requirement was relayed to the root.

Runner source-hash guards intentionally reject runs whose source changes during
execution. Freeze writers, then resume/re-run as needed. A final reporter call
after the runner's finalized run summary captures final provenance; an earlier
manifest records exactly the run-summary state it actually read.

## Executed commands and evidence

All commands executed from `D:/WORK/Projects/omo/Glosea6`.

```text
.venv/Scripts/ruff.exe check analysis/alternative_reporting*.py
.venv/Scripts/basedpyright.exe analysis/alternative_reporting*.py
.venv/Scripts/python.exe -B analysis/alternative_reporting.py --help
.venv/Scripts/python.exe -B analysis/alternative_reporting.py --output outputs/reporter_invalid_input_should_not_exist --invalid
.venv/Scripts/python.exe -B -m analysis.alternative_reporting_audit --output outputs/alternative_reporting_smoke_verified_20261007
```

Final native Ruff: `All checks passed!`, exit 0.
Final native basedpyright: `0 errors, 0 warnings, 0 notes`, exit 0.
Direct-script help: actual CLI output, exit 0.
Invalid flag: `unrecognized arguments: --invalid`, exit 2; no requested output
directory created. The audit imports and invokes the public reporting API twice
on actual read-only baseline rows.

Final real fixture audit: exit 0, actual receipt:

```json
{
  "actual_cases": 244,
  "actual_years": [2022, 2023, 2024, 2025, 2026],
  "arithmetic": {
    "independent_arithmetic_assertions": 13,
    "status": "PASS"
  },
  "byte_deterministic_report_files": 41,
  "protected_files_unchanged": 60,
  "real_baseline_rows": 960,
  "report_status": "INCOMPLETE",
  "scope": "REPORTING_SMOKE_NOT_FULL",
  "status": "PASS"
}
```

The fixture copies only real protected RAW/QM/QDM/EMOS score rows, 60 available
cases plus one actual unavailable target per variable/product. It does not
fabricate any new-method skill. Its missing law/full artifacts are deliberately
reported INCOMPLETE. Artificial three-row losses are used only in isolated
machine arithmetic assertions, not the reported forecast fixture.

Independent assertions include O(n²) empirical CRPS, exact fallback sums/N,
successful-loss bounds, immutable failed status disclosure, independently
encoded mask hashes, an exact repeated-window weighted mean, tied-threshold
climate probabilities, and actual annual-vector fallback against the independently
implemented joint energy/variogram oracle.

Retained artifacts:

- `outputs/alternative_reporting_smoke_verified_20261007/reporting_smoke_receipt.json`
- `outputs/alternative_reporting_smoke_verified_20261007/reports/report_manifest.json`
- `outputs/alternative_reporting_smoke_verified_20261007/reports/REPORT_KO.md`
- All 41 deterministic report files in that `reports/` directory.

The audit checks all 60 protected byte counts and SHA256 values before and after,
compares all report bytes across two API calls, and removes its intermediate
CSV. Earlier own smoke iterations were cleaned up; only the verified fixture
is retained as evidence.

## Personal manual QA and remaining parent-owned work

Personally rendered and inspected actual Agg plots: weekly rain CRPS (mm),
monthly temperature CRPS (degC), and monthly temperature coverage. Labels,
alphabetical method display, seed 20261007, REPORTING_SMOKE title and explicit
success-only/restricted-N caveat matched the actual scores and counts. The
retained final weekly-rain PNG was inspected after final behavioral refinement:
`reports/score_1mon_f2971799b1_CRPS.png`. Earlier inspected monthly-temperature
and coverage figures are also retained in the final deterministic report set.

Read the generated Korean report: coverage precedes actual losses and
common-mask deltas; each product/variable has 61 supplied, one unavailable,
60 eligible/scored for every baseline method. It explicitly reports missing
law artifacts and INCOMPLETE rather than new-method success or FULL PASS.

LSP diagnostics were requested before validation but its session import resolver
reported unresolved project imports; native root-cwd basedpyright supplied the
successful full owned-module check without suppressions. No project config,
baseline tests or validator were weakened.

Parent owns complete all-method execution, independent full artifact validation,
and final full report/image QA. This evidence proves reporter readiness and its
actual baseline reporting surface, not fitted new-method superiority.

## Development-QA refinement: visible N and terminal-state gate

The root's development inspection requested clearer N disclosure and warned that
an interrupted runner must not be promoted by the presence of prediction files.
Score-chart method labels now show their actual `scored_N`; coverage-chart labels
show actual `scored_count/eligible_count`. Neither changes the underlying scores
or sorts methods by skill.

Full report readiness now additionally requires the actual runner summary status
to equal `COMPLETED`. `RUNNING`, `FAILED_SOURCE_CHANGED`, other failed/interrupted
states and an absent status cannot produce complete reports even when prediction
artifacts exist. The manifest and Korean report explicitly record `run_status`.
Since the runner's initial lazy reporting call precedes its final completion
transition, that preliminary report remains INCOMPLETE; refresh reporting only
after successful runner finalization.

Focused checks, without another model fit or data-catalog smoke:

```text
.venv/Scripts/ruff.exe check analysis/alternative_reporting*.py
.venv/Scripts/basedpyright.exe analysis/alternative_reporting*.py
.venv/Scripts/python.exe -B -m analysis.alternative_reporting_refinement_audit
```

All exited 0; native Ruff passed and basedpyright returned 0 errors/0 warnings.
The focused audit rejects six non-final/absent terminal states and verifies the
actual saved score-table N label. It renders 16 figures from the already
verified real baseline tables, with no synthetic new-method skill and no model
or data smoke rerun. Receipt:
`outputs/alternative_reporting_refinement_20261007/refinement_receipt.json`.

Personally opened and inspected the new weekly-rain score and coverage PNGs in
that output directory. Actual `N=60` and `N=60/60` labels were legible and matched
the saved real tables; mm, seed, SMOKE and success-only caveat remained visible.
This inspection covers those two development figures only, not all final
full-experiment surfaces. Parent still owns full stabilized-run plot/report QA.
