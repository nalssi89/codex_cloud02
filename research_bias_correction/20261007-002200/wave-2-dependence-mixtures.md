# Dependence and mixtures final dossiers

Observers dependence (>10queries) and mixtures. Retrieved2026-10-06; primarysources inspected; no fileswritten.

## Dependence methods
Pure reorder preserves marginalvalues/mean/quantiles/tercileprobabilities/CRPS. Joint hot-dry events or trajectories are additionaltargets, not existingunivariategain.
SS: use same-yearcalendar-alignedobservedregionalvectors to reorder calibratedsamples. No rawIDsrequired; climatologicalratherthanflowdependent;24/30templateyearsnoise, widenedcalendarwindowscanharm. Repeatedtemplatesnotnewtraininginformation.
ECC-Q: quantilesj/(M+1), rawmatchedmemberrankcopula. Lowcost/flowdependent, preserves wrongrawdependence if biased. OriginalIDsneeded; missingcommonIDsexplicitselection; currentQDMoldindexnotECCduetorankcrossings. EMOSquantilemembersapproximateanalyticCDF, retainanalyticmarginalscores.
ResidualGaussiancopula: calibratedresidualz=Phi^-1(F_fitted(y)), shrunk2Dcorrelation, transformbackusingissuedmarginals. DoNOTuseunconditionalobservedrho. Zeroatom needscensoredlatentintervals or justifiedrandomizedPIT. Plug-inMöller2013notposteriorBJP.
dECC: erroreddependencecoloredcorrections to rawtemplates; for multi-leadtrajectories, notscalarforecast. Hourlywindprecedentnotseasonalproof; highdimensioncovariancesingularatdimension>=K withsamplecentering.
MBCp/r: QDM+Pearson/Spearmancovariance correction. MBCn: randomrotations+univariatemapping, multivariatePDFmatching; climateperiodcorrectionnotconditionalforecastreliability. No automatictemporalorderpreservation;2Dseasonallyconditionedpredictiveadaptationneedsnewtest.
OTC/dOTC: jointdistributiontransport, evolvedperiodmapping; empiricalsupport/cost/binning/dimensionrisks. Rainnonnegativesupportandscalingmustbeverified. Unconditionaltransport≠seasonalcalibration.

## Mixtures
ClimatologyCDFpool: F=lambdaFcal+(1−lambda)Fclim, one regularizedtrain-onlyweight, identity-free,validzeroatoms; broadens or weakenssignals and lambdaoverfit possible. LOYOsource recommendation refined bylead to past-onlyouter operationalvalidation.
EqualTkernel: F=mean_mPhi((y−(a+b*x_m))/sigma), common3parameters; permutationinvariant/variableM; rawmultimodality+dispersion, tails/rawlocationspotentiallywrong.
BMA: fittedweightedcomponentdensities,temperatureNormal/rainzero+positivegamma. Groupmassw_g/M_g onlywithin scientificallyverifiedexchangeablegroups. NofixedmemberIDweightsbasedonarrayorder. KnownBMAweightsnotfullposterioroverallparameters.
Rainmixturedressingrequiresnonnegativekernels+zeroatom, notuntruncatedGaussian.

## Primarysources
- ECCSchefzik2013 DOI10.1214/13-STS443, https://arxiv.org/html/1302.7149 : rawrankperfect-modelassumption,50memberECMWFshort/mediumrange.
- dECCBenBouallègue2016 DOI10.1175/MWR-D-15-0403.1, https://arxiv.org/html/1511.05877 : COSMO20membershourly100mwind<=21h,45daycalibration,7stations.
- Clark2004 DOI10.1175/1525-7541(2004)005<0243:TSSAMF>2.0.CO;2, https://pubs.usgs.gov/publication/70027101 : dailyNCEP14dayrain/T, not24annualregionalproof.
- Schepen2020 DOI10.1175/MWR-D-19-0046.1: MBJPvsUBJP+SS/TQM; noindependentECCtest.
- Möller2013 DOI10.1002/qj.2009, https://arxiv.org/html/1202.3956 :8memberUW,5dailyvars48h,plug-incorrelation.
- Cannon2016 DOI10.1175/JCLI-D-15-0679.1, https://journals.ametsoc.org/view/journals/clim/29/19/jcli-d-15-0679.1.xml : MBCp/r maymodify modeledsequences.
- Cannon2018 DOI10.1007/s00382-017-3580-6:3hourly7varCanRCM4fireweather/climateperiods, held-outearlystopping; notseasonalensemblebenchmark.
- Robin2019 DOI10.5194/hess-23-773-2019, https://hess.copernicus.org/articles/23/773/2019/ :24D2295dayperiodsillustratecovariance estimationlimits.
- Lerch2020 DOI10.5194/npg-27-349-2020, https://npg.copernicus.org/articles/27/349/2020/ : simulationcomparison, “There is no consistently best method”.
- Shrestha2020 DOI10.1016/j.jhydrol.2020.124991, https://agris.fao.org/search/en/providers/122535/records/65e00a5663b8185d9cb0d2e9 : abstractonlytemporalaccumulationreliabilitywarning.
- Raftery2005 DOI10.1175/MWR2906.1, https://journals.ametsoc.org/view/journals/mwre/133/5/mwr2906.1.xml : fittedBMAtemperaturemixture.
- Sloughter2007 DOI10.1175/MWR3441.1: zero+gammaonpositivecube-rootrain, dataset-specific.
- Fraley2010 DOI10.1175/2009MWR3046.1, https://journals.ametsoc.org/view/journals/mwre/138/1/2009mwr3046.1.xml : constrain equalwithinknownexchangeablegroups.
- Roulston/Smith2003 DOI10.1034/j.1600-0870.2003.201378.x ; Bröcker/Smith2008 DOI10.1111/j.1600-0870.2008.00333.x : kerneldressing.
- Kleiber2008 DOI10.1175/2008MWR2565.1, https://journals.ametsoc.org/view/journals/mwre/136/12/2008mwr2565.1.xml : BMA/dressingextremeprobabilitycounterevidence.
- Baran/Lerch2018 DOI10.1016/j.ijforecast.2018.01.005, https://arxiv.org/html/1607.08096v3 : predictiveCDFpools. WronginitialDOI10.1016/j.csda.2018.01.012 identifiesunrelatedAhonenmixture-regression, rejected.

## Software routes, not executed
https://cran.r-project.org/web/packages/MBC/refman/MBC.html : no automaticseasonconditioning.
https://github.com/slerch/multiv_pp : simulations.
https://github.com/yrobink/SBCK-python : MBCn/OTC/dOTC, separateTSMBC.
https://search.r-project.org/CRAN/refmans/ensembleBMA/html/ensembleBMA.html : Rgroup/missingmember. ensembleBMAgamma help windspeednotrain.

## EXPAND closed
Originalmembergeneration/pairedidentity, jointoutputdemand, residualcensor/priors, MBCpredictiveadaptation: futureimplementationgates not asserted facts.
Deadends: membercountsasindependentyears; wrongFamienMBCn citation; unconditionalcorrelationasresidualcorrelation; publishermirrorsasindependentsourcegroups.
Noresourcesopened; nofilescreated; primaryaccessgapsretained.
