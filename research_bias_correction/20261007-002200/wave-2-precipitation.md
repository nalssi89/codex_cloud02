# Precipitation final dossier

Observer precipitation,2026-10-06;13 varied English queries; primary text including85k-character NERC monthly-aggregate PDF. No files written.

## Candidate distributions
CSG EMOS: Y=max(0,G−delta), G~Gamma(k,theta), delta>=0. P0=F_G(delta), F_Y(y)=F_G(y+delta) y>=0. Positive skew + atom0, analytic CRPS. Reduced mean/variance/shift5parameter example is new candidate specification, not universal canonicalCSG. Normalize predictor sums for changing member count. Main risks: shift/tail/occurrence coupling, small sample parameter burden. First currentEMOS extension.
Positive Gamma regression: parsimonious mean/variance links, positive support/skew; cannot model exact-zero mass. Compare if historical zero outcomes rare; absence in24/30 does not prove true zero probability.
Fixed-power censored Gaussian: Y=[max(0,Z)]^(1/r), r fixed small menu. F_Y(y)=Phi((y^r−mu)/sigma). Reuses current structure, but original-mm CRPS differs from transformed loss, inverse-transform(mu) is not mean. No unverified analyticCRPS claim; validated integration needed.
Hurdle: logistic occurrence + conditional-positive Gamma/lognormal. More flexible separate processes, but sample splitting/separation/rarezero uncertainty. All-wet unpenalized intercept divergence; priors/pooling needed. Hurdle factorization not same as BMA.
Censored GEV: flexible tail/atom0; shape unstable, endpoint/numerics; original paper constrains xi∈(−0.278,1) for positive skew/finite mean. Finite variance needs xi<0.5 (mathematical consequence). Total-precipGEV not block-maxima theorem application.
Tweedie1<p<2: compoundPoissonGamma, Var=phi*mu^p, P0=exp(−lambda), lambda=mu^(2−p)/(phi(2−p)). Conditional positive amount NOT oneGamma. Coherent skew/zero, but shape/dispersion and CDF costs. Monthly climatology fit precedent NOT forecast calibration evidence. Quasi-likelihood alone not full predictive CDF.

## Region/aggregation caveat
Nonnegative positive-weight region mean/time sum equals0 only if every component0. Does not establish observed Korean zero frequency or independence. Count true-zero/nearzero/positive outcomes per training product/lead/season first. Do not transfer daily0.1mm wet-day threshold to weekly/monthly region total.

## Primary references and source settings
1. Scheuerer/Hamill2015 DOI10.1175/MWR-D-15-0061.1; https://journals.ametsoc.org/view/journals/mwre/143/11/mwr-d-15-0061.1.xml : GEFS11member,12h totals2002–2013;3stage neighborhood design, not n30regional.
2. Baran/Nemoda2016 DOI10.1002/env.2391; https://arxiv.org/html/1512.04068 : UWME24h83stations70training days; ALADIN10cities55days. Exchangeable group equality only if scientifically justified. Daily pooled sample windows not universal yearly threshold.
3. Scheuerer2014 DOI10.1002/qj.2183; https://arxiv.org/html/1302.0893 : COSMO-DE6h totals18hlead, rolling30days pooled gauges +early stopping; GEV.
4. Sloughter etal2007 DOI10.1175/MWR3441.1; https://journals.ametsoc.org/view/journals/mwre/135/9/mwr3441.1.xml : zero+Gamma cube-root positive components in BMA;9distinguishable members,PacificNW24h48hlead,30daypooled training. Dataset-specific.
5. Messner/Mayr/Zeileis2016 DOI10.32614/RJ-2016-012; https://journal.r-project.org/articles/RJ-2016-012/ : crch censored/truncated regression; example is square-root censored LOGISTIC3day rain, not Gaussian. Excludeszero spread, so currentM1/spread0 support not copied.
6. Svensson/Hannaford/Prosdocimi2017 DOI10.1002/2016WR019276; https://nora.nerc.ac.uk/515472/1/N515472JA.pdf :121UKcatchments,1/3/6/12month mean-area totals,calendar month fit,minimum30record years; all positive in study; Tweedie climatological distribution not forecast skill.
7. Hasan/Dunn2010 DOI10.1016/j.agrformet.2010.06.002; https://researchportalplus.anu.edu.au/en/publications/a-simple-poisson-gamma-model-for-modelling-rainfall-occurrence-an/ : institutional abstract only; monthly stations, not ensemble regression.
8. https://www.psl.noaa.gov/forecasts/s2s_NNprecip/info.html : NOAA7/14day experimentalCSGD baseline,2000–2019 GEFSv12/PRISM0.5°; no Korea transfer.
9. https://search.r-project.org/CRAN/refmans/ensembleMOS/html/ensembleMOScsg0.html : R ensembleMOS0.8.2 reference, mean/member links and variance/mean,CRPS. API not executed.
10. https://scoringrules.readthedocs.io/en/latest/generated/scoringrules.crps_csg0.html : located PythonCRPS candidate, not executed; sign/shift convention needs verification.
11. https://journals.ametsoc.org/view/journals/mwre/145/5/mwr-d-16-0251.1.xml : BMA vsHCLR comparisons vary by training/metric/lead/season/threshold; HCLR logistic not Gaussian.
12. https://arxiv.org/html/1804.09233 : Courbariaux2018 hierarchical transformed precision/posteriorStudent-t+Tobit preprint. EmpiricalBayes hyperparameter fit not full posterior over all coefficients.

## Recommendation
Compare currentcensoredGaussian,leanGamma/CSG,fixedpower first, same original-mmCDF/CRPS and held-out targets. Hurdle only identifiable occurrence; GEV/Tweedie lower priority with fixed/shrunk shape. No measured improvement asserted.

## EXPAND and cleanup
NOAAweekly and NERCmonthly-aggregate leads verified/closed. Zero-frequency audit is future implementation question. Dunn2004PDF403 and HasanfullPDFunverified remain explicit gaps; relevant NERCfullprimary obtained. Streams closed; no process/browser/temp artifact spawned.
