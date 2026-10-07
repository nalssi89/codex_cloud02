# Learning and independent benchmark dossier

Observers learning and benchmark-web-recovery.2026-10-06,20+ queries each; important primary methods/settings inspected. No files/resources spawned.

## Method claims and applicability
Ordinal logistic: coherent ordered cutpoints yield BN/NN/AN probabilities. One mean predictor/two cutpoints has3parameters; not a continuous-value/CRPS replacement. ELR uses physical thresholds and is related but not identical. Independent binary fits can cross. Empty/rare category implies separation/uncertainty, regularization/pooling conditional.
Componentwise distributional boosting/GAMLSS: separate location/scale/shape predictors, shrinkage/early stopping; tiny seasonal/lead/mean/spread design conditional on safe pooling. Response-family constraints remain; ZAGA/hurdle differs fromCSG. NGBoost natural gradient is not same algorithm as componentwiseEMOSboosting; defaultNormal not rain support solution.
QRF: Fhat(y|x)=sum_i w_i(x)1(y_i<=y); flexible/no family assumption, zeros included. Vanilla support bounded by historical outcomes. Leaves need distinct-year support, many trees do not add observed years. Conditional pooled experiment, NOT universal rejection for n30.
IDR: stochastic-order CDF fitting, interpretable nonparametric; chosen order must be scientifically valid, many incomparables/high dimension, bounded empiricaltails, explicitly data-hungry vsEMOS/BMA. No tuning≠n30adequacy.
DRN: nonlinear links to fixed predictivefamily, not Bayesposterior or universal remedy. BQN outputs Bernsteinquantile coefficients; original2020 didNOTenforce ordering, cannot claim guaranteed monotonic. Orderedincrement design is a new safeguard; polynomial tails bounded, zero atom needs separate handling.
SVR: one genuine30annualcase nonlinear success refutes blanket“MLimpossible”; deterministic index results doNOTproveQRF/DRNregionalrain distribution adequacy.

## Primary sources
- Vannitsem2021 review DOI10.1175/BAMS-D-19-0308.1: broad weatherreview, not seasonally validated ranking.
- Messner2014 DOI10.1175/MWR-D-13-00355.1: categorical ordered/logistic,10stations,~900days; reduceddata loses skill.
- Robertson2023 DOI10.1175/WAF-D-22-0160.1: SubXweekly/biweeklyterciles,17years×3neighborwindows=51rows, not51years; training-fold thresholds; gridded rather than regionaltotal.
- Wilks2009 DOI10.1002/met.134: ELR foundation.
- Messner2017 DOI10.1175/MWR-D-16-0088.1: dailyT,5stations,~1700days,~1550perCV; seasonalstandardizedanomalies.
- Duan2020 https://proceedings.mlr.press/v119/duan20a.html : NGBoost.
- Benáček2023 DOI10.1175/WAF-D-22-0006.1: dailyCzech36stations,1y12919vs4y49902pooled rows; EMOS resisted reducedtraining, not genericMLsuperiority.
- Meinshausen2006 https://www.jmlr.org/papers/volume7/meinshausen06a/meinshausen06a.pdf : QRFfundamental17ppfull.
- Taillardat2016 DOI10.1175/MWR-D-15-0260.1: T/wind87Frenchstations,4ydaily3–54hleads; maximumobservedbound.
- Taillardat2019 DOI10.1175/WAF-D-18-0149.1: rain86stations6h51hlead; EGPhybridtail is separate extension.
- Sansonnet2024 DOI10.1175/JAMC-D-24-0014.1: TanzaniamonthlyT/P,cluster/grid hybridlaggedpredictors,ERA51983–2023.30×12monthly situations not360independentyears. Originalnormalizationnottrain-only, do not copy.
- Henzi2021 DOI10.1111/rssb.12450: IDR31ppfull; airportdaily24hrain,1500–3000days; largertrainingneedthanEMOS/BMA.
- Rasp/Lerch2018 DOI10.1175/MWR-D-18-0187.1: daily48hT537stations;180849pooledrows2015vs1626724rows2007–2015,2016test.
- Uttarwar2025 DOI10.1016/j.advwatres.2025.105061: SEAS5dailygridT/P at1monthlead, notmonthlytarget.13289grids×10957days=145607573nominaltrain+validation,27205/27231parameters. ComparatorE-QMnotcurrentEMOS. FullKITPDFobserved.
- Bremnes2020 DOI10.1175/MWR-D-19-0227.1: BQNwind125stations,51members,+60h;49883train/45477test;7217weights. Originalquantilecrossings up to0.22%, averaging removed empirically, no guarantee.
- Schulz/Lerch2022 DOI10.1175/MWR-D-21-0150.1: gust175Germanstations,0–21h,2010–2015fit/2016test. Source benchmark rankings NOT seasonaltransfer.
- Horat/Lerch2024 DOI10.1175/MWR-D-23-0150.1: globalbiweekly3–4/5–6terciles,20reforecastyears,11HC/51FC,globalpatchpool; notQRFvsDRNcontrolledranking.
- Kharin2017 DOI10.1175/MWR-D-16-0337.1: CanSIPS1981–2010/20members; temporal/spatialsmoothedstatistics, samplingerror~30annualoutcomes, heterogeneousspatialsmoothingcanharm.
- Zhao2017 DOI10.1175/JCLI-D-16-0652.1: POAMAmonthlyrain1981–2011,QMvsBJP; biasremovalnotprobabilisticcalibration.
- Finnis2012 DOI10.1080/07055900.2012.667388:1972–2001annualindices,SVR5predictors,nestedyearCVexcludingneighbors; nonlinearcase-specificsuccessnotlocalrainproof.

## Implementation metadata only, not executed
QRF https://github.com/zillow/quantile-forest / DOI10.21105/joss.05976.
IDR https://github.com/AlexanderHenzi/isodistrreg ; Python https://github.com/evwalz/isodisreg .
NGBoost https://github.com/stanfordmlgroup/ngboost .
DRN https://github.com/slerch/ppnn ; Alpine https://github.com/Sam-Uttarwar/NN_arch .
BQN https://github.com/benediktschulz/paper_pp_wind_gusts .
SubseasonalCNN https://github.com/HoratN/pp-s2s .
RgamboostLSS/crch possible routes; family/gradient must be checked. PythonOrderedModel not claimed penalized bydefault.

## Convergence/cleanup
All bibliographic leads resolved or source-access gaps disclosed. Compatiblewithin-archivepooling is futureimplementationdecision, not unanswered literatureclaim. No benchmark provesQRFvsboostingvsDRNordering for exact24/30unpooledannualpairs. No new files/process/browser; in-memoryPDFhandlesclosed.
