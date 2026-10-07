# User-requested interruption and resumption

Date: 2026-10-07.

The user requested stopping because the computer must be shut down.
Root terminated the only active comparison process, `bash_157`, via
`kill_bash`. Its monitor `mon_QHBCAR39M53DC1JE` delivered a killed event.
The terminal log records the Windows CLOSE interruption. Do not classify this
user-requested interruption as a numerical method failure.

## Actual state

- The repaired all-method small run was interrupted after its latest reported
  progress, `200/352`; exact additional completed cache objects must be counted
  on resumption.
- Output: `outputs/alternative_comparison_root_all_methods_smoke_v2`.
- Its saved `run_summary.json` still says `RUNNING` because termination occurred
  outside normal CLI finalization. That stale status is **not** a live process
  and **not** a completed experiment.
- Complete fit/prediction checkpoints already written by the runner remain
  available. The runner verifies their complete scientific/source identity
  before reuse.
- The first small run's failed report remains honestly preserved at
  `outputs/alternative_comparison_root_all_methods_smoke`. Its 586 saved laws,
  98 joint scores and scalar/joint ancestry independently passed; the CSV
  boundary was subsequently fixed and its report-generation CLI passed.
- The binding FULL comparison and final FULL independent validation have not run.
- Scientific-work ledger: 44/51 completed; seven remaining tasks are paused,
  not completed or abandoned.

## Resume only when the user requests continuing

```text
.venv/Scripts/python.exe -B analysis/run_alternative_comparison.py --output outputs/alternative_comparison_root_all_methods_smoke_v2 --case-id 20220307_1MON_W01_t15m --case-id 20220307_1MON_W01_prcp --case-id 20220307_3MON_M01_t15m --case-id 20220307_3MON_M01_prcp --workers 4 --resume
```

Inspect guarded completion, independent scores/provenance and real reports.
Then execute the binding FULL command and FULL validator; never present the
small-run checks as FULL completion. Preserve all original files and the known
strict QDM precision alert.

## Subsequent GitHub preservation request

The user explicitly authorized uploading the work to GitHub. This supersedes
the earlier no-project-commit condition **for that requested backup only**;
it does not authorize history rewriting or changing original scientific files.
Actual checks: this directory is not a Git repository (`git rev-parse` and
`git remote -v` exit 128); GitHub CLI is authenticated as `nalssi89`.
Destination and visibility await the user's choice. No remote repository,
commit or upload has yet been created. Never upload credentials, API keys,
virtual environments or large disposable fitting caches.

### Destination confirmed subsequently

The user supplied `https://github.com/nalssi89/codex_cloud02` and additionally
requested that continuation records be pushed. The repository is private,
default branch `main`, with original commit
`be551eb8d7809eabef16d63f2883f975ae061809` and its README preserved.
Local Git metadata was initialized and attached to that existing history.
`NEXT_SESSION_KO.md` is the next-session entry point. Upload is in preparation;
no experimental calculation was restarted.
