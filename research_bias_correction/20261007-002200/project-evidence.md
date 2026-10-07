# Project applicability evidence

Observed at 2026-10-06, current working files; no project Git SHA exists (git log/status exit128).

|Constraint|Evidence|Implication|
|---|---|---|
|Regional calibration targets; paired station/grid forecasts not established|latest outputs/REPORT_KO.md:126; data_io contract|Fresh station observation rows alone do not establish spatial forecast calibration inputs|
|Weekly and individual calendar month, not 3-month accumulated target|latest outputs/REPORT_KO.md:126|Daily weather methods need aggregation-aware fitting|
|24–30 annual observation pairs; 3/7 historical members|latest REPORT_KO.md:155-173; prior REVIEW_KO.md:144-158|Member replication is not extra independent labels; shrinkage/pooling candidates|
|Member exchangeability/independence not established|analysis/audit_scoring_sensitivity.py:95-101, personally re-read|Exchangeable BMA and signal-noise assumptions conditional|
|Target-valid year excluded, historical end before init|analysis/run_verification.py:90-118, personally re-read|Transforms, trend, pooling and hyperparameters must fit within training|
|Current calibration API one variable at a time|analysis/calibration.py:132-161; explore/dependence observations|Joint calibration needs explicit aligned T/P/history/lead arrays|
|EMOS parameters only, QM/QDM indexed arrays|analysis/run_verification.py:123-164|ECC needs sampled calibrated quantiles and a joint output schema|
|Fresh KMA API Hub actual-contributor means supersede earlier originalQC baseline during research|latest REPORT_KO.md:5-21,126; run_summary observation_source|Minimum50 per variable; actual60/61/62 observed contributors; no 62/n scaling or imputation; QC derived, not instrument QC|
|Calendar cutoff does not prove model release availability|latest REPORT_KO.md:404-406|Operational claims also require issued-time model/version/observations availability|

Exploration limitation: cases/ directory currently empty; do not conclude all original data are missing. Existing pipeline artifacts and data files remain. Exact cross-variable member identity has not been established by marginal outputs; requires inspecting original source sampling provenance before joint scenario reconstruction.

## Concurrent update
Another workspace task modified collection/outputs during this research (observed mtimes23:35–23:50UTC). Lead re-read latest reports at23:52UTC; current run6432eligible, observationretrieval2026-10-06T23:42:09.597Z. No source file was edited or reverted by this literature research. Previous originalQC audit results are historical methodological evidence, not independent audit of new metrics.
