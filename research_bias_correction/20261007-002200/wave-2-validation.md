# Validation axis final dossier

Observer validation,2026-10-06.16 varied English queries; primary text/PDF fetched. No production run/files written.

## Primary observations
- Sansom/Ferro/Stephenson/Goddard/Mason2016, DOI10.1175/JCLI-D-15-0868.1: simple recalibration may outperform complex with limited training; overlap requires excluding neighboring blocks. Annual CanCM4 grid T experiment, not weekly Korean rain; no universal30-year threshold.
- Ferro2014 DOI10.1002/qj.2270: fair scores only for some dependence forms. Exchangeability symmetry is not iid.
- Siegert2016 DOI10.1175/JCLI-D-15-0196.1 / arxiv1504.01933: GloSea5 winterNAO1992–2011,20 yearly outcomes, six-parameter signal-noise Bayesian model; posterior normal mixture generally not a normal or automatically t.
- Risbey2021 DOI10.1038/s41467-021-23771-z / PMC8285537: future-aware centered CV is unfair for real-time comparison.
- Manzanas2022 DOI10.1029/2021GL094662: SEAS5 T/rain1981–2016,51members,42regions. Longer hindcasts/ensembles affect reliability estimation. Regional point probability pooling is NOT distribution of regional average.
- Testing the Tests2018 DOI10.1175/MWR-D-17-0295.1: identical cases needed for model comparison; partially repeated observations narrow naiveCI. Author metadata not independently checked, cite title/DOI.
- Gilleland2020 DOI10.1175/JTECH-D-20-0069.1: iid bootstrap fails with dependence. No fixed block-size transfer to a short5year series.
- Sampling Errors in Seasonal Forecasting2009 DOI10.1175/2008MWR2560.1: temporal/spatial pooling reduces variance but mixes signals; temporal correlation unaccounted in particular experiment.
- Kim2022 DOI10.14191/Atmos.2022.32.4.367: trial7 vs operational3/date;24yrs1993–2016; dates1/9/17/25; weighted nearby hindcast starts. May already exist in archive mapping; do not double pool.
- MetOffice GloSea6 guide observed2026-10-06 is institution/configuration specific, not latest KMA row provenance.
- APCC model description p11: KMA GloSea6GC3.2,1993–2022 on-the-fly,84FC/28combinedHC; ocean reanalysis1993–2016 UKMO ODA versus2017–2022 GODAPS2-RA. Publication date not established. Potential archive break only; exact row mapping unverified.
- IRI methodology: ELR1991–2020 ensemble mean/terciles; operational feasibility not Korean proof.
- NOAA CPC CBaM: monthly-issued3month seasonal guidance; calibration+bridging+BMA, not individual-calendar-month product.
- Beverley/Newman/Hoell2024 DOI10.1038/s41612-024-00832-w: trend error diagnostics; no Korean skill implication.

## Recommended benchmark (design inference)
Annual outcomes not member counts. Keep per-year total weight1/N_years; each member within-year weight1/(N_years*M_year).
Primary outer test past-only issued2022–2026, exact HIST_END<INIT_DATE and target-valid year excluded. All transforms/terciles/trend/pooling/hyperparameters fit only inner training. December→January uses exact calendar windows.
Same accepted targets across RAW, climate, mean-bias/MOS/constant-variance, QM/currentQDM/currentEMOS/new candidates; report fit failures separately.
Report both all-issuance scores and equal-valid-window sensitivity. Repeat issues are real operational decisions but dependent evidence, not independently repeated observations.
Paired year-block score-loss sensitivity; only~5 operational years means exploratory uncertainty, not robust significance.
Pool only within product/variable, preserve lead and valid-season/drift effects; cycles/anomalies, penalties/bandwidth chosen inside folds. Weekly/monthly rain totals never indiscriminately mixed.
Common1993–2016 versus extended1993–2022 training on same recent targets; do not infer later6years alone supports extra-stratum fitting.
3-of7 subsampling only if original matching identity and scientific sampling design established; no universal variance transfer factor.
Keep issued empiricalCRPS primary. Fair iid score secondary conditional sensitivity, not correction of official result.
Calibrate region aggregates directly. Regional-event probability is not average grid-event probability; nonlinear correction and aggregation generally do not commute.
Bayesian regression/predictive mixture is a candidate; prior sensitivity/model checks and actual predictive distribution scoring required.

## EXPAND closure
Archive ocean provenance, original identity, already-applied init-date weighting: conditional implementation prerequisites, no assertion yet.
Station/grid pooling and spatial copulas: unavailable target granularity; current-scope dead end.
No remaining broad retrieval needed. Streams closed; QA-only REQUESTS_CA_BUNDLE removed; no processes/browser/files spawned.
