# Observation manifest
|observation_id|source|layer|group|independence|observer|observed_at|valid_at|artifact|anchor|contamination|
|---|---|---|---|---|---|---|---|---|---|---|
|P1|outputs/REPORT_KO.md|local current report|project|current rerun not old memory|lead|2026-10-06|2026-10-06|project report|7-58|same upstream observations|
|P2|outputs/method_review/REVIEW_KO.md|independent audit report|audit|independent math audits same inputs|lead|2026-10-06|2026-10-06|audit report|79-158|not independent weather realization|
|W1|https://researchonline.jcu.edu.au/67563/|primary repository metadata|lead-web|separate observer, same underlying paper as team|lead|2026-10-06|2020 publication|journal.md|title/authors/148(1)437-456|abstract extraction partial; not full results proof|
|W2|https://www.psl.noaa.gov/forecasts/s2s_NNprecip/info.html|first-party operational documentation|lead-web|independent NOAA territory|lead|2026-10-06|page observed at access date|journal.md|Method/Source|US gridded pooled data, not GloSea6|
|W3|https://journals.ametsoc.org/view/journals/mwre/149/8/MWR-D-20-0318.1.xml|primary methods paper|lead-web|separate observer, same paper as joint-gaussian|lead|2026-10-06|2021 publication|journal.md|Methods3a/3b; Conclusions5|LOYO not forward-time operational proof|
|B1|https://researchonline.jcu.edu.au/67563/|live browser rendering|browser|render route independent from text fetch; same primary work|top-source-browser|2026-10-06T23:22:16Z|2020 publication|assets/provenance/seasonal-joint-calibration-jcu-full.png|abstract|landing page only|
|B2|https://arxiv.org/abs/1512.04068|live browser rendering|browser|author manuscript source|top-source-browser|2026-10-06T23:26:34Z|arxiv v3/2016 journal|assets/provenance/precipitation-csg-emos-arxiv-full.png|abstract/journal reference|not full-paper proof|
|D1|https://journals.ametsoc.org/view/journals/mwre/148/1/mwr-d-19-0046.1.xml|full primary text|dependence|independent researcher of same primary study|dependence|2026-10-06|2020 publication|journal.md|out-of-sample vs in-sample; conclusions|Australia seasonal, not Korea weekly/monthly|

## Source-index observations
Each S-id in sources-ledger.md is also an observation id O-S{id}; URL is that row's source, artifact is the matching wave dossier, observed_at2026-10-06, valid_at is paper publication year or undated live page at observed_at. Evidence layer/access boundary recorded in ledger/dossier. Observer groups below are independent researchers, NOT automatically independent datasets/authorship.

|observations|observer/group|independence basis|artifact|anchors|contamination|
|---|---|---|---|---|---|
|O-S6,S7,S8,S39|primary-web-recovery/recovery|separate source reader; sameCSIROpaper lineage|wave-1-primary-recovery.md|methods/results quoted|sameauthors/underlyingdata|
|O-S5,S6,S8,S14,S37,S38,S39|joint-gaussian/joint|CSIROmethods and independentExetermodel|wave-2-joint-gaussian.md|conditionaldistribution/censor/limitations|notKoreanperformance;abstract-onlyexceptions|
|O-S2,S4,S27-36|precipitation/rain|NOAA,Baran,NERC,Rstatsdifferentterritories|wave-2-precipitation.md|distributionformula/trainingexamples|aggregation/regiontransferunproved|
|O-S10-23|validation/validation|Exeter/NCAR/KMA/APCCoperationalgroups|wave-2-validation.md|validation/provenancemetadata|externalconfignotarchiveproof|
|O-S24,S25,S45-59|learning/learning|QRF/IDR/IRI/NNgroups;NNoverlappingauthors|wave-2-learning.md|trainingtarget/tail/quantileconstraints|nominalspatialrowsnotindependentcases|
|O-S9,S26,S66-72|dependence/dependence|ECC,USGS,Cannon,FrenchOTsources|wave-2-dependence-mixtures.md|reorder/matrix/conditionalscope|mirrorsnotindependentsourcegroups|
|O-S29,S60-65|mixtures/mixtures|BMAauthors/kernel/poolinglineages|wave-2-dependence-mixtures.md|mixture/group constraints|anonymousmemberweightsunjustified|
|O-S40-44,S73-78|parsimonious/parsimonious|seasonalMOS+uncertaintystatistics+projectionmethods|wave-2-parsimonious.md|restrictedmodels/metadata|projectionmechanicsnotforecastskill|

Temporal source notes:2025Alpineobservations valid_at2025publication;2024Tanzaniavalid_at2024publication; APCCPDFpublicationdateunknown, validity limited to observedPDFmetadata.2020seasonalstudy36availableyears and35fitLOYOevents not conflated.

|P1-current|outputs/REPORT_KO.md:5-21,126,155-173,406 andrun_summaryobservation_source|liveconcurrentlyupdatedprojectreport|lead-current|newreadnotoldmemo|lead|2026-10-06T23:52Z|observationretrieval2026-10-06T23:42:09.597Z|project-evidence.md|freshKMAactualcontributor/min50/derivedQC/24–30/cutoff|otherworkspaceactorupdatedoutputs;notournewmethodexperiment|
