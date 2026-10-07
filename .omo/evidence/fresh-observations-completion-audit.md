# Fresh-observation goal completion audit

Objective: recollect actual observations under nalssi89/kmahub policy for the
fixed 62 ASOS stations, preserve original inputs, rerun all eligible GloSea6
temperature/precipitation calibration and verification, and publish traceable
updated reports with numerical and personally observed surface QA.

| Explicit requirement | Current-state completion evidence |
| --- | --- |
| Use the requested collection repository and actual station observations | `observations/kmahub_refresh/provenance.json` records `https://github.com/nalssi89/kmahub`, revision `e5c1e0cefbea07021aa294ea1a2789e39216b0e6`, KMA endpoints, retrieval timestamps, 450 retained response hashes and the station export. The gate independently reconciled every response with its exported measurements. |
| Fixed 62 IDs; no inference of particular missing stations from aggregate counts alone | The gate reproduced equality with original station metadata. `coverage_gaps.csv` identifies actual station/date absence and variable missingness from raw records: 24 absent rows, 258 missing returned temperature values, zero invalid returned precipitation values. |
| Daily/variable missingness, duplicates, QC and averaging | `coverage_audit.json`, `independent_audit.json`, and the gate's raw-chain/duplicate/sentinel/aggregation drivers establish 809,820 of 809,844 station/date rows, contributor distributions, actual-denominator averages, and explicit derived QC. No imputation or 62/n scaling; documented kmahub precipitation sentinel policy retained. |
| Historical calibration and current verification periods | Snapshot 1991-01-01–2026-10-05 has 13,062 calendar days. `training_audit.json` verifies 156,408 accepted annual pairs, historical-only boundaries and zero training-observation discrepancy. `case_audit.csv` accounts for all 6,580 supplied cases: 6,432 verified and 148 future/unavailable targets explicitly excluded as of the snapshot cutoff. |
| Separate fresh source; preserve original archive/model inputs | `observations/active_source.json` selects the new directory. Original-source absence-of-switch driver passed earlier. Independent source audit and gate each verify all 24 original manifest hashes. Original archive was not edited; seven unexpectedly absent CSVs were restored missing-only to their exact hashes. Their disappearance cause remains unknown; uninterrupted presence or an independently captured pre-task compressed-archive hash is not claimed. |
| Both temperature and precipitation, targets/training/all four methods | `run_summary.json`, `validation.json`, training ledger and predictions establish RAW/QM/QDM/EMOS 6,432 rows each, 25,728 total; weekly T/P 1,874 each and monthly T/P 1,342 each. EMOS fit failures: zero. Old period-reference differences are explicitly recorded rather than forced to equality with new observations. |
| Consistent metrics, Korean report and PDF provenance | Current metrics by lead/month/season/year and overall feed `REPORT_KO.md`, `method_review/REVIEW_KO.md` and `pdf_manifest.json`. The gate verified all 16 manifest source hashes and the authoritative PDF hash. |
| Type, related numerical checks and real entry-point use | Actual project-venv Ruff and basedpyright passed, repeated independently by the gate. Root completed 9,163,254 core checks, training/EMOS/scoring audits and the CLI happy path/help/bad-input surfaces. The gate independently exercised bounded parser, aggregation, QM/QDM and EMOS drivers; it does not claim its detached full-validator invocation returned a recovered PASS. |
| Actual numerical and visual PDF QA | `pdf_validation.json`: 78,431 checks, 10,640 compared records, 68 fresh 150dpi renders, errors empty. Root personally viewed all 17 contact sheets/all 68 pages; receipt `outputs/pdf_visual_qa/fresh_manual_qa_KO.md`. Gate additionally viewed representative sheets and full-size pages, and verified all 68 page-image hashes. |
| Secrets and authorized scope | Credential remained local, not saved in project artifacts or reports. No repository commit, formula rewrite, normals substitution, unrelated research-folder change, or forced viewer closure. |
| Final gate | `.omo/evidence/fresh-observations-gate-review.md`: **APPROVE**, blockers empty; completed task `st_01a113a9`. |

Authoritative deliverable:
`outputs/GLOSEA6_verification_by_dimension_KO_refreshed.pdf`.
SHA256: `e673c90839e09fe9bd97038b160a8db6d27a599c43faa922cac6eefdb2daa6a0`.
The old viewer-locked `_final.pdf` was preserved and is not the deliverable.

Explained retained numerical exception: QM/QDM strict oracle returns
`STRICT_TOLERANCE_ALERT`, exit 1, for one QDM member with accurate-sum error
`1.0345502232667059e-10` against `1e-10`. Operation-order failures are zero.
The gate independently reproduced this warning; it remains disclosed and
the tolerance was not weakened. No universal clean-PASS claim is made.

Todo reconciliation: 15 deliverables complete; 2 investigations dropped with
reasons (no aggregate-count bug requiring a fix; original CSV disappearance
unattributed but exact missing-only recovery verified). No task remains open.
All explicit requirements are covered by current evidence; goal complete.
