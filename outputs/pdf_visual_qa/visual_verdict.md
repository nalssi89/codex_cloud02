# Current actual-station GloSea6 PDF: visual and functional QA

Date: 2026-10-06. **PASS, HIGH confidence; 68/68 pages covered, no blockers.**
The prior strict62 verdict is historical and is not carried forward.

## Current artifacts and execution evidence

- Main: `outputs/GLOSEA6_verification_by_dimension_KO.pdf`.
- Final: `outputs/GLOSEA6_verification_by_dimension_KO_final.pdf`.
- Both files are byte-identical; SHA-256:
  `055c7deeea849afd64bdff86cbc1b78759942c2243bd7fe253f857083e0a7e1f`.
- Fresh captures: `outputs/pdf_qa/pages/page_001.png` through `page_068.png`.
- Fresh contact sheets: `outputs/pdf_qa/contact_sheets/contact_001.png` through
  `contact_017.png`, four consecutive pages each.
- `outputs/pdf_validation.json`: PASS, 78,401 checks, 10,640 numerical records,
  68 rendered pages, no errors. Embedded fonts, physical-page bounds,
  selectable CJK text, vector charts, source hashes and 22 bookmark destinations
  were checked. This is distinct from visual inspection.
- The lead personally opened all 17 sheets and inspected every page.
- Independent functional pass `st_01a110d6`: PASS/HIGH, all 17 sheets and
  full-resolution pages 2 and 61; all capture hashes/signatures and source
  freshness checked, no product/evidence blocker.
- Independent visual/CJK pass `st_01a110d7`: PASS/HIGH, all 17 sheets and
  full-resolution pages 1, 2, 3, 4, 29, 61 and 68; no product/evidence blocker.
- Both reviewers were read-only: no rerenders, source edits or audit reruns.

## Observation policy and corrected content

The current result uses source-QC-valid means over actual daily contributors,
including 61/60-station days. The supplied minimum is 50; there is no 62/n
rescaling or imputation of unavailable individual-station values.
Temperature averages the daily means; precipitation sums daily regional means.
The station list still has 62 sites, while actual contributors vary.

- 6,318 of 6,580 supplied cases verified.
- Weekly temperature/rainfall: 1,844 each.
- Monthly temperature/rainfall: 1,315 each.
- Monthly temperature: 53 distinct periods; BN=130, NN=100, AN=1,085.
- All-62 historical period-reference equality is retained. Partial-station
  reference differences are logged and distinguished from exact independent
  reconstruction of canonical daily-policy OBS.
- QDM sorted-quantile/climate-trend preservation is not guaranteed.
- The former 307-case/13-period/NN=0 claims are not current.

## Complete page-coverage ledger

Each row covers all four named page captures, not a sample.

| Sheet | Pages inspected | Verdict | Surface |
|---|---|---|---|
| contact_001.png | 1, 2, 3, 4 | PASS | Cover, guidance and complete 16-row summaries |
| contact_002.png | 5, 6, 7, 8 | PASS | Weekly-temperature lead charts |
| contact_003.png | 9, 10, 11, 12 | PASS | Weekly-rainfall lead charts |
| contact_004.png | 13, 14, 15, 16 | PASS | Monthly-temperature lead charts |
| contact_005.png | 17, 18, 19, 20 | PASS | Monthly-rainfall lead charts |
| contact_006.png | 21, 22, 23, 24 | PASS | Weekly-temperature month charts |
| contact_007.png | 25, 26, 27, 28 | PASS | Weekly-rainfall month charts |
| contact_008.png | 29, 30, 31, 32 | PASS | Monthly-temperature month charts |
| contact_009.png | 33, 34, 35, 36 | PASS | Monthly-rainfall month charts |
| contact_010.png | 37, 38, 39, 40 | PASS | Weekly-temperature season charts |
| contact_011.png | 41, 42, 43, 44 | PASS | Weekly-rainfall season charts |
| contact_012.png | 45, 46, 47, 48 | PASS | Monthly-temperature season charts |
| contact_013.png | 49, 50, 51, 52 | PASS | Monthly-rainfall season charts |
| contact_014.png | 53, 54, 55, 56 | PASS | Weekly-temperature year charts |
| contact_015.png | 57, 58, 59, 60 | PASS | Weekly-rainfall year charts |
| contact_016.png | 61, 62, 63, 64 | PASS | Monthly-temperature year charts |
| contact_017.png | 65, 66, 67, 68 | PASS | Monthly-rainfall year charts |

## Applicable print-surface checklist

| Items | Verdict | Evidence |
|---|---|---|
| A1, A3, A7, A8, A9 | PASS | Intentional grid/margins/grouping; no overlap or clipping on pages 1–68 |
| B3, B4, B5, B6 | PASS | Descriptive titles, hierarchy and consistent method encoding |
| C1, C2, C4, C5, C8 | PASS | Readable technical copy/CJK, complete clauses and selectable text |
| E2, E3, E4 | PASS | Visually legible contrast; named methods plus distinct markers/colors |
| F2, F3, F4 | PASS | Shared spacing/chart anatomy and retained document identity |
| G6, G7 | PASS | Fully composed, static readable pages |
| Remaining mobile/theme/control/motion/window items | N/A | Fixed print PDF, not a responsive application |

Contrast approval is visual, not a claimed numerical WCAG measurement.
Viewer-owned keyboard focus, shortcuts and interaction are outside this static
document. Bookmark navigation, fonts and text extraction are separately checked.

## Findings and completion

No `[product]` or `[evidence]` blockers. No source or capture changed after
the final approving passes. Preserve the complete charts, distinct method
markers, actual count/mean diagnostics, explicit units and statistical caveats.
This approves the current rendered report, not statistical flawlessness of QM,
QDM or EMOS. The strict floating-point alert remains in the method audit.
