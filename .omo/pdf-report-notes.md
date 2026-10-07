# PDF report notepad - GloSea6 by lead, month, season and year
Started: 2026-10-06

## Goal and tier
HEAVY: new PDF reporting pipeline with exhaustive paginated visual QA.
Reuse all existing verified scores. Do not alter or refit model results.
Ideal state: Korean PDF plus every comparison figure, canonical categorical order,
all four methods, all four product/variable groups, all verification metrics,
audited numerical fidelity and personally inspected rendered pages.

## Plan
1. Read own verification memory, CSV schemas, existing artifacts, plotting/PDF tools.
2. Lock A4 landscape structure and complete dimension/group/metric coverage.
3. Build analysis/make_dimension_pdf.py; generate lead, month, season, year figures.
4. Four chart families per group: deterministic; overall probability; tercile;
   intervals/observed and predicted means. Four dimensions x four groups x four
   families = 64 chart pages; add four front-matter/summary pages = 68 pages.
5. Keep missing monthly bins as NaN gaps, not zeros or interpolated lines.
6. Save exact plot_data.csv, source hashes and numbered page manifest.
7. Assemble vector PDF with embedded Malgun Gothic and navigable bookmarks.
8. Independent numerical/functional QA compares every plot point and N to original
   CSV, confirms input hashes, PDF coverage/text and every page capture.
9. Render every actual PDF page at150dpi, inspect complete fresh captures personally.
10. Independent visual/CJK reviewer inspects all pages. Functional reviewer checks
    genuine generated charts, coverage and PDF text/accessibility; irrelevant web,
    keyboard, motion and dark-mode criteria are N/A for this static PDF.
11. Fix actual blockers, rerender affected source and full final capture set.
12. Keep final PDF, PNGs, source-data manifests and QA receipts; clean temporary state.
Topology: lead owns generation/assembly, deep-low child owns ONLY independent
analysis/validate_dimension_pdf.py plus functional audit; visual-engineering
read-only child owns all-page CJK/layout audit after fresh page renders.
No design-planner: known CSV-to-matplotlib/PDF procedure, no open domain decision.
Skills used: ultrawork/session evidence discipline; data-scientist + visualization
(numeric plots); programming/Python (typed scripts); visual-qa (all PDF pages,
independent numerical/functional and visual/CJK passes); verification-before-completion.

## Success scenarios
C1 `.venv/Scripts/python.exe analysis/make_dimension_pdf.py`: all four dimensions,
all methods, all groups, 64 PNG charts + complete Korean PDF. Source tables unchanged.
C2 `.venv/Scripts/python.exe analysis/validate_dimension_pdf.py`: all plotted values,
N, canonical bins, missingness, PDF page count/text/font and source hashes PASS.
C3 `tool.read` every rendered PDF page/contact sheet plus full-size captions:
labels, CJK, units and legends readable; no blank, clipped or overlapping page.
Both independent audit lanes terminal without an unresolved blocker.
Stop when PDF and PNGs are proven and delivered. No further analysis refitting.

## Findings
- Original verification PASS:6580 accounted,4644 accepted x4methods.
- Monthly temperature only307 cases /13 distinct target windows; BN26/NN0/AN281.
- Existing CSVs include all four dimension breakdowns and full deterministic,
  probabilistic, tercile and interval metrics. All month tables numeric bins,
  season canonical DJF/MAM/JJA/SON, year VALID_START year2022-2026.
- Monthly temperature absent months must remain visibly absent, never zero.
- Resident Python kernel unreliable; run isolated .venv CLI through monitors.
- Malgun Gothic fonts available C:/Windows/Fonts/malgun.ttf and malgunbd.ttf.
- Existing matplotlib/numpy/Pillow available. PyMuPDF and pypdf install monitor armed.
- No git repository; no commits or Git initialization.

## Now
Confirm chart coverage and implement generation plus independent validator.

## Todo
Live phased checklist has10 items; generation, numerical QA and every-page QA pending.

## Learnings
- Distinguish source-case counts from independent observation windows.
- Group month/season/year by VALID_START, not initialization date.
- Static PDF needs page renders, not extracted text alone, for layout proof.

## First render and caught regression
Generator CLI exit0:68pages,64PNGcharts,10640 exported data points.
Typechecker caught incomplete Matplotlib kwargs and narrow Literal/protocol
contracts; real typed interfaces fixed without warning suppression.
Lead `tool.read(outputs/dimension_figures/month_3mon_t15m_deterministic.png)`
caught warning footer overlapping the bottom axis labels on six-panel pages.
This is an actual visual QA failure, not a numerical error. Fix subplot bottom
margin .10->.15, regenerate every plotted page and PDF before next image check.
Independent validator worker told to treat first-build captures as superseded and
wait for FINAL_GENERATION_READY. Original numerical CSVs remain untouched.

## Corrected render and final front matter
Second generator exit0 produced all68pages/64charts/10640points.
Lead re-opened monthly-temperature deterministic PNG: warning/footer clear
of all bottom axis labels; PASS. Also inspected season/week/rain probability and
year/month/rain interval families: legible units, canonical order and methods.
Lead actual pypdf CLI verifies68 PDFpages, navigable outline and embedded Korean text.
Self-review found PDF needs exact reproducibility commands and explicit exclusions.
Added only two9pt commands to reading page and1674+262 exclusions to cover;
chart values/layout unchanged. Final full generation bash_64/mon_DSNSJ352Q8ZAE7BN
armed. Child instructed final captures require final PDFhash after generation.
Code scenarios: basedpyright new modules0errors0warnings, ruffPASS.
CLI `make_dimension_pdf.py --help` usageexit0; `--invalid-option` rejectexit1.
Now: final PDF generation; independent validator typing/functional work active.
Next: receive final68page renders, start separate visual/CJK audit and lead inspection.

## Observed Windows viewer lock and paired cleanup
Final frontmatter build bash_64 completed charts but final write raised
PermissionError on the existing PDF. Old PDF and all original sourceCSV retained.
Independent worker verified no owned validator/document lock remains and added
unconditional resource cleanup, including an injected-failure lifecycle check.
Do not close or kill user viewers. Write fully built PDF to an owned staging file,
then atomic replace; on this observed PermissionError only, preserve oldviewer copy
and deliver separate GLOSEA6_verification_by_dimension_KO_final.pdf, with exact
actual path in manifest. Filename is our implementation choice, not a user constraint.
Original goal's intended full PDF artifact remains binding; its actual path will
follow pdf_manifest.json, not an unverified stale viewer-locked copy.
Latest generation bash_66/mon_898C4ZGFWRYC3MPE armed.
Lead opened updated real PDF preview frontpages1-2 at150dpi: PASS; exact dates,
sample/exclusion totals, monthlytemperature13-window caveat and reproduction
commands readable, unclipped and separated from footer. PreviewCLI closed document.

## Final verified deliverable and STOP
Atomic generation bash_66 exit0 preserved the viewer-locked original and wrote
outputs/GLOSEA6_verification_by_dimension_KO_final.pdf,839358bytes.
pdf_manifest identifies correct final;SHA256:
1ae09fef9d5cb6455148eae73a84c03ac17d313714b17f90e61ab9d92e8b3fdb.
68pages=4frontmatter+64chartpages.10640audited plot records,475missing-bin records.
Original8sourcehashes unchanged. All4dimensions,4groups,4methods,4families covered.
Independent functional audit PASS65216checks,68fresh150dpi nativePDFrenders,
all bounds/fonts/selectable Korean,22bookmarks,exact summary/source values.
Lead personally reran validator (bash_68):PASSexit0; no scoring helpers imported.
Independent visual/CJK worker read ALL68full-size pages and unconditionallyPASS:
outputs/pdf_visual_qa/visual_verdict.md, no clipping/overlap/tofu/visual blockers.
Specialist route unavailable; capable deep-low substituted without configuration changes.
Lead personally inspected all68layouts through17fresh contact sheets, plus fullsize
pages1-8/29 and chart PNG examples. All families/chapters/data gaps/order/footers
readable; corrected bottom warning no longer intersects axis labels.
Final basedpyright entireanalysis0errors0warnings;ruffPASS;compileallPASSexit0.
Generatorhelp/badinputPASS; validatorhelpPASS/invalid--dpi149rejectedexit2 beforewrites.
No tests existed to skip or weaken. No Git repo/commits.
Cleanup receipts: all owned CLI/monitor processes finite exited, all child tasks
terminal; no user viewer touched. Removed ownedanalysis/__pycache__ and
supersededoutputs/pdf_front_preview. Staging .dimension_raw.pdf and
.dimension_completed.pdf absent (fs.statENOENT), no owneddocument/stream lock.
Final PDF/64PNGs, audit JSON, plot CSV, manifests and capture evidence retained as
intentional deliverables. Locked olduser-viewer copy intentionally preserved.
C1allcoveragePASS;C2source/PDFvalidationPASS;C3everypagevisualPASS.

## Now
DONE. Deliver final PDF and figure-directory links, then STOP.

## Todo
None.12/12 tasks completed. No further edits, renders or polish.
