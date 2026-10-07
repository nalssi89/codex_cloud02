# Historical strict62 Korean GloSea6 PDF: superseded visual verdict

This record belongs to the earlier strict62-filtered PDF, not the current
source-QC rerun. See `visual_verdict.md` for the current 6,318-case publication.

**VERDICT: PASS. 68/68 pages inspected; 68 PASS, 0 FAIL.**

No visual/layout or CJK blockers. No source, PDF, CSV, capture, or validator was modified.

## Evidence and scope

- Final artifact: `outputs/GLOSEA6_verification_by_dimension_KO_final.pdf`.
- Artifact SHA-256 supplied by the assigning lead: `1ae09fef9d5cb6455148eae73a84c03ac17d313714b17f90e61ab9d92e8b3fdb`. This visual pass did not independently recompute the hash.
- Directly opened and visually inspected **every** full-size capture: `outputs/pdf_qa/pages/page_001.png` through `outputs/pdf_qa/pages/page_068.png`, inclusive. Each image was individually displayed, in batches of at most eight, rather than inferred from extracted text or contact sheets.
- Capture specification supplied by the lead: fresh final-PDF renders, 1754 x 1241 pixels, 150 dpi. All displayed captures were complete, composited page images, with no viewer chrome, black regions, or visibly defective frames.
- The stale unsuffixed PDF was not used.
- Loaded `C:/Users/user/AppData/Roaming/npm/node_modules/omo-ai/plugin/skills/visual-qa/SKILL.md`. Applied its paginated-surface, complete-coverage, visible-layout, and CJK criteria. This task is the independent visual reviewer lane; no additional children were spawned, as instructed.
- Numerical/functional audit results, font embedding, bookmarks, text selection, and physical bounding-box checks belong to the lead's separate audit. They were not retested or used as substitutes for visual inspection.

## Overall visual/CJK audit

- Korean cover, methods, panel titles, axis labels, warnings, tables, and footers render as actual readable Hangul: no tofu, missing glyphs, clipped baselines, unnatural syllable breaks, or orphaned particles observed.
- All chart pages have consistent two-column grids, separated panel titles, readable ticks, a clear header legend, amber notes, source footer, and page index. The previously reported footer/x-label overlap is absent on **all** chart pages, including page 29.
- Summary tables on pages 3 and 4 display all 16 rows, including final monthly-rain EMOS rows. Headers and values fit their cells; neither table crosses the footer.
- Method encoding is consistent throughout: RAW gray circles, QM blue squares, QDM green triangles, EMOS orange diamonds; gray dashed reference curves and dotted zero/coverage reference lines are distinguishable. Coincident method points can naturally overplot; visible legend shapes retain the decoding key.
- Temperature dimensional panels identify degrees Celsius; precipitation dimensional panels identify mm per target interval. Correlation, ACC, skill, Brier/RPS and coverage are presented without inappropriate physical units.
- Lead axes visibly use W01-W08 or M01-M06; month axes retain 1-12; season axes use DJF-MAM-JJA-SON; year axes use 2022-2026, in order.
- Missing monthly-temperature positions on pages 29-32 remain gaps and disconnected segments, not artificial zero-valued observations. Undefined correlation positions on pages 29, 45 and 61 are likewise left blank. Real zero-valued marks, such as coverage points on page 64, remain visibly marked and are distinct from absence.
- Shared diagnostic axes are visibly sensible: correlation/ACC use -1 to 1; coverage uses 0 to 1 with the 0.90 reference. Different score quantities use their own legible scales rather than a misleading common physical unit.
- Common N and observed-mean diagnostics appear once as gray bars on their respective pages, not four redundant method series.
- No accidental empty panel/page, clipped chart title, unreadable legend, overlapping tick text, or clipped table row was observed.
- Static PDF mobile reflow, dark mode, pointer targets, keyboard focus, animation, loading states, and live controls are not applicable. No web-design requirements were imposed on these fixed chart pages.

## All-page PASS/FAIL ledger

Capture paths below are relative to `outputs/pdf_qa/pages/`. Every PASS includes visual inspection of its header/body/footer and CJK rendering.

| PDF page | Actual capture | Verdict | Specific visual reason |
|---:|---|---|---|
| 1 | `page_001.png` | PASS | Cover hierarchy and Korean text clear; counts, exclusions and monthly-temperature caution fit; index clear. |
| 2 | `page_002.png` | PASS | Methods paragraphs and Korean clauses fit; W/M and season explanations readable; reproduction commands separated at footer. |
| 3 | `page_003.png` | PASS | Deterministic summary: all 16 rows and eight columns fit; units and amber caution do not collide. |
| 4 | `page_004.png` | PASS | Probabilistic summary: all 16 rows and nine columns fit; long metric headers readable; final row intact. |
| 5 | `page_005.png` | PASS | Lead weekly-temperature deterministic six-panel grid; W01-W08 and single labeled N bars clear. |
| 6 | `page_006.png` | PASS | Lead weekly-temperature probability six panels; dashed references and score/skill separation readable. |
| 7 | `page_007.png` | PASS | Lead weekly-temperature BN/NN/AN panels distinct; all lower labels clear of notes. |
| 8 | `page_008.png` | PASS | Lead weekly-temperature interval/mean four panels; 0.90 reference and Celsius widths clear. |
| 9 | `page_009.png` | PASS | Lead weekly-rain deterministic panels; mm/target-interval titles fit and N labels clear. |
| 10 | `page_010.png` | PASS | Lead weekly-rain probability panels; negative skills readable around zero references. |
| 11 | `page_011.png` | PASS | Lead weekly-rain tercile titles, marks and ticks legible; footer separated. |
| 12 | `page_012.png` | PASS | Lead weekly-rain intervals/means; precipitation units fit long titles; gray OBS bars once. |
| 13 | `page_013.png` | PASS | Lead monthly-temperature deterministic M01-M06; N bars and amber sample warning readable. |
| 14 | `page_014.png` | PASS | Lead monthly-temperature probability titles and six scales fit; lower axes above caution. |
| 15 | `page_015.png` | PASS | Lead monthly-temperature BN/NN/AN six panels; NN label readable, not a blank/missing panel. |
| 16 | `page_016.png` | PASS | Lead monthly-temperature interval/mean four panels; forecast/OBS reference distinct and caution intact. |
| 17 | `page_017.png` | PASS | Lead monthly-rain deterministic panels; M01-M06, units and N-bar annotations fit. |
| 18 | `page_018.png` | PASS | Lead monthly-rain probability six panels; reference and negative-skill curves clear. |
| 19 | `page_019.png` | PASS | Lead monthly-rain tercile panels; all six titles and ticks readable without collision. |
| 20 | `page_020.png` | PASS | Lead monthly-rain interval/mean panels; units and OBS reference readable; bottom margin clear. |
| 21 | `page_021.png` | PASS | Month weekly-temperature deterministic panels retain all 12 ticks and readable N labels. |
| 22 | `page_022.png` | PASS | Month weekly-temperature probability panels; 12-month labels and skill baselines legible. |
| 23 | `page_023.png` | PASS | Month weekly-temperature tercile panels; month 10-12 ticks do not collide. |
| 24 | `page_024.png` | PASS | Month weekly-temperature intervals/means; near-zero winter means still readable, no cutoff. |
| 25 | `page_025.png` | PASS | Month weekly-rain deterministic panels; full 1-12 axis and single N-bar panel legible. |
| 26 | `page_026.png` | PASS | Month weekly-rain probability panels; dense crossing curves preserve distinct markers and clear legends. |
| 27 | `page_027.png` | PASS | Month weekly-rain tercile panels; extremes stay in plots, ticks and footers separated. |
| 28 | `page_028.png` | PASS | Month weekly-rain interval/mean four panels; full month axes and long unit headings fit. |
| 29 | `page_029.png` | PASS | Month monthly-temperature deterministic panels retain missing-month gaps; N labels clear; corrected footer spacing confirmed. |
| 30 | `page_030.png` | PASS | Month monthly-temperature probability panels show disconnected segments and isolated markers, not zero fill. |
| 31 | `page_031.png` | PASS | Month monthly-temperature tercile panels preserve gaps; negative BN skills legible; caution separated. |
| 32 | `page_032.png` | PASS | Month monthly-temperature intervals/means preserve missing positions; real zero/negative values distinguishable. |
| 33 | `page_033.png` | PASS | Month monthly-rain deterministic panels; extremes and all 12 N annotations fit. |
| 34 | `page_034.png` | PASS | Month monthly-rain probability panels; zero references and negative skills clear, lower labels intact. |
| 35 | `page_035.png` | PASS | Month monthly-rain tercile panels; large negative AN skill remains inside readable plot range. |
| 36 | `page_036.png` | PASS | Month monthly-rain interval/mean four panels; wide mm ranges and long headings remain readable. |
| 37 | `page_037.png` | PASS | Season weekly-temperature deterministic panels use DJF-MAM-JJA-SON; N and season-note text fit. |
| 38 | `page_038.png` | PASS | Season weekly-temperature probability six-panel layout; dashed curves and skills legible. |
| 39 | `page_039.png` | PASS | Season weekly-temperature tercile titles and four season positions clear; no lower-label collision. |
| 40 | `page_040.png` | PASS | Season weekly-temperature interval/mean panels; near-zero DJF OBS bar visible and footer separated. |
| 41 | `page_041.png` | PASS | Season weekly-rain deterministic panels; mm units and four N labels readable. |
| 42 | `page_042.png` | PASS | Season weekly-rain probability panels; close-valued score curves fit axes and markers remain keyed. |
| 43 | `page_043.png` | PASS | Season weekly-rain tercile panels; season axes and six titles clear; notes not overlapped. |
| 44 | `page_044.png` | PASS | Season weekly-rain intervals/means; mm units and four-panel grouping clear. |
| 45 | `page_045.png` | PASS | Season monthly-temperature deterministic panels; undefined DJF correlations left blank, N and warning readable. |
| 46 | `page_046.png` | PASS | Season monthly-temperature probability panels; negative skills/zero references fit and remain legible. |
| 47 | `page_047.png` | PASS | Season monthly-temperature tercile panels; BN negative range readable and NN panels render normally. |
| 48 | `page_048.png` | PASS | Season monthly-temperature intervals/means; negative DJF OBS bar not clipped; caution separate. |
| 49 | `page_049.png` | PASS | Season monthly-rain deterministic six panels; dimensional headings and single N bars clear. |
| 50 | `page_050.png` | PASS | Season monthly-rain probability panels; score/skill distinction and reference lines readable. |
| 51 | `page_051.png` | PASS | Season monthly-rain tercile panels; all seasonal ticks and lower notes clear. |
| 52 | `page_052.png` | PASS | Season monthly-rain interval/mean four panels; high mm widths fit with clear method symbols. |
| 53 | `page_053.png` | PASS | Year weekly-temperature deterministic panels; 2022-2026 ticks and N annotations readable. |
| 54 | `page_054.png` | PASS | Year weekly-temperature probability panels; five-year labels and shared legend clear. |
| 55 | `page_055.png` | PASS | Year weekly-temperature tercile panels; small score differences still read from labeled axes. |
| 56 | `page_056.png` | PASS | Year weekly-temperature interval/mean panels; Celsius titles and OBS bars readable. |
| 57 | `page_057.png` | PASS | Year weekly-rain deterministic panels; dimensional headings, 2022-2026 ticks and single N bars fit. |
| 58 | `page_058.png` | PASS | Year weekly-rain probability panels; negative-skill points remain distinct from zero references. |
| 59 | `page_059.png` | PASS | Year weekly-rain tercile six panels; year labels and panel spacing consistent. |
| 60 | `page_060.png` | PASS | Year weekly-rain interval/mean panels; mm labels and reference/forecast means clear. |
| 61 | `page_061.png` | PASS | Year monthly-temperature deterministic panels; undefined 2025 correlations form a gap, not zero fill; warning clear. |
| 62 | `page_062.png` | PASS | Year monthly-temperature probability panels; skill scales and zero references readable. |
| 63 | `page_063.png` | PASS | Year monthly-temperature tercile panels; negative BN skill and near-zero NN score marks readable. |
| 64 | `page_064.png` | PASS | Year monthly-temperature intervals/means; actual zero QM coverage marks visible, no missing-data conflation. |
| 65 | `page_065.png` | PASS | Year monthly-rain deterministic panels; long mm headings and five N labels clear. |
| 66 | `page_066.png` | PASS | Year monthly-rain probability six panels; negative skills and reference curves unclipped. |
| 67 | `page_067.png` | PASS | Year monthly-rain tercile panels; all six titles, year ticks and method markers consistent. |
| 68 | `page_068.png` | PASS | Final year monthly-rain interval/mean panels complete; footer, units and final 68/68 index intact. |

## Skill checklist applicability

PASS here means visually observed on the named page captures, not a numerical WCAG or source-code claim. Static-document adaptations are stated explicitly.

| Item | Verdict | Capture/evidence and applicability |
|---|---|---|
| A1 | PASS | Pages 1-68: intentional cover/prose/table/chart anchors, no accidental stranded content. |
| A2 | N/A | Static white PDF page; no scrolling/full-bleed web background. |
| A3 | PASS | Pages 1-4: readable prose/table measures and page margins; chart grid consistent on 5-68. |
| A4 | N/A | No phone safe-area UI. |
| A5 | N/A | No page-owned scrollbars. |
| A6 | N/A | No interactive scroll regions. |
| A7 | PASS | Pages 3-68: shared table edges/panel grids and consistent gaps. |
| A8 | PASS | Pages 5-68: header legend, panel groups and footer notes separated. |
| A9 | PASS | Fixed-document clipping/overlap criterion: all 68 full-size renders clear; responsive web widths N/A. |
| A10 | N/A | Complete fixed pages, no hidden continuing viewport content. |
| A11 | N/A | No app window/sidebar. |
| B1 | N/A | No primary action controls. |
| B2 | N/A | No destructive actions. |
| B3 | PASS | Pages 1-68: titles identify document or dimension/product/family; toolbar length rule N/A. |
| B4 | PASS | Pages 1-68: title then content; secondary cautions remain below chart/table body. |
| B5 | N/A | Multi-method scientific palette is intentional, not decorative toolbar accent styling. |
| B6 | PASS | Pages 1-68: clear title/body/footer hierarchy; static single appearance, not paired themes. |
| C1 | PASS | Pages 1-68: text/ticks/legend readable in the supplied 150-dpi full-size page images; phone font thresholds N/A. |
| C2 | N/A | Scientific dates, metric identifiers and reproduction paths are purposeful technical content. |
| C3 | N/A | No action/tab labels. |
| C4 | PASS | Pages 1-68: no clipped glyphs, heading wraps, or label/footer overlap. |
| C5 | PASS | Pages 1-68: no tofu or unnatural Hangul clause/particle splitting observed. |
| C6 | PASS | Pages 2, 29-32, 45, 61: missing data explained and represented as gaps; interactive errors N/A. |
| C7 | N/A | No input fields. |
| C8 | N/A | Selection is a separate functional audit, not provable from PNGs. |
| D1 | N/A | No touch/pointer targets. |
| D2 | N/A | No tab bar. |
| D3 | N/A | No toolbar. |
| D4 | N/A | No bar buttons. |
| E1 | N/A | Fixed white-page PDF, no app theme variants. |
| E2 | PASS | Pages 1-68: visible text and chart marks legible on white; no claim of measured WCAG ratios or dual-theme testing. |
| E3 | PASS | Pages 5-68: method identity uses both named labels and distinct marker shapes, not color alone. |
| E4 | PASS | Pages 5-68: method colors/shapes and gray references consistent throughout. |
| E5 | N/A | No translucent surfaces. |
| E6 | N/A | No theme selector. |
| F1 | N/A | Chart symbols are method encodings, not UI action icons. |
| F2 | N/A | No component radii/token implementation audit in this read-only PDF task. |
| F3 | PASS | Pages 5-68: common chart layout, legend and corrected bottom spacing checked on every consumer page. |
| F4 | N/A | No supplied branding fidelity target; cover title is intentional document identity. |
| F5 | N/A | No selection/focus state. |
| F6 | N/A | No action glyphs. |
| F7 | N/A | No windows/sheets/popovers. |
| G1-G7 | N/A | Static PDF has no motion or interaction feedback. |
| H1-H11 | N/A | Static PDF has no live loading, controls, permissions, sign-in, search or settings states. |
| I1-I5 | N/A | No PDF-owned interactive controls or media; functional PDF accessibility is outside this visual lane. |
| J1-J2 | N/A | No desktop/phone application chrome. |

## Blockers and minimal fixes

**None.** No page-specific correction is required by this visual pass.

## Preserve

Keep the corrected bottom spacing, method marker/color mapping, once-only gray N/OBS bars, full canonical dimension axes, disconnected missing-data segments, explicit temperature/rain units, and monthly-temperature sample cautions.

## Completion

Independent visual reviewer inspection is complete on all 68 supplied fresh final-artifact page images. This is an unconditional **visual/CJK PASS** for the identified final PDF; numerical and functional sign-off remains the separately reported lead audit, not a claim from image review.
