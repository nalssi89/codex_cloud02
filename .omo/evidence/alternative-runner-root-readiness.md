# Root runner readiness receipt

The root read `.omo/evidence/runner-implementation.md` in full after its owner
declared runner sources frozen. FULL experiment completion is not asserted.

## Personally executed final surface checks

- `.venv/Scripts/python.exe -B analysis/run_alternative_comparison.py --help`:
  successful help output; `--methods` and repeatable `--case-id` explicitly
  identify SMOKE scope, worker choices 1 through 6 and content-matched resume.
- Same CLI with `--invalid`: rejected before fitting, exit **2**.
- `.venv/Scripts/ruff.exe check --no-cache analysis/alternative_runner*.py analysis/run_alternative_comparison.py`:
  **All checks passed!**
- `.venv/Scripts/basedpyright.exe --pythonpath .venv/Scripts/python.exe --level warning analysis/alternative_runner*.py analysis/run_alternative_comparison.py`:
  **0 errors, 0 warnings, 0 notes**.

## Personally executed genuine final metadata pilot checks

Root read-only driver imported `metadata_checks`, `summary_checks` and
`ancestry_checks` and applied them to
`outputs/alternative_runner_metadata_ready_smoke`.

Monitor `mon_SEFXEKBY2E1E1R27`, process `bash_138`, completed **exit 0**:

- Metadata: **PASS**, 6 genuine fit cache identities.
- Pairwise masks: **PASS**, 19,664 comparison rows, 105 nonempty masks.
- Summaries: **PASS**, all 5 tables, 30 groups.
- Ancestry: **PASS**, 24 actual annual training rows, 1 scalar training hash.
- Catalog policy remains `OUTER_FROZEN_NOT_REAL_TIME_RELEASE_PROOF`.

This confirms the newly delivered real metadata pilot, not the older
`alternative_runner_final_ready_smoke` which predates those additions.
All check processes terminated; no source or fixture edits occurred.

## Execution dependency

Runner source hashes intentionally cover all `analysis/*.py`, including
independent validator modules and audits. The current joint analytic-marginal
validator repair must finish and freeze before the root begins its stable
all-method four-case small run and binding FULL run. Starting while that owner
is editing would deliberately invalidate the run's source-consistency guard.
No guard or scientific check is weakened to avoid that dependency.
