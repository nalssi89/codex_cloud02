# Primary literature recovery

Observer: primary-web-recovery; terminal completed. 21 queries; 10 distinct original URLs fetched. Retrieval boundaries documented below.

## Seasonal BJP
Schepen & Wang2013, MWR1414554–4563, DOI10.1175/MWR-D-12-00253.1.
https://journals.ametsoc.org/view/journals/mwre/141/12/mwr-d-12-00253.1.xml
Ensemble-mean predictor; Yeo–Johnson transformed bivariate normal; MCMC parameter uncertainty. Six GCMs,1980–2005 overlapping record (~26 annual events), one-month-lead Australian seasonal rain.
Quote: “Parameter uncertainty can be important when there is only a short data record to establish the model.”
Low correlation reverts toward predictand marginal, not identical to prior shrinkage.

Schepen/Wang/Robertson2014 DOI10.1175/MWR-D-13-00248.1.
https://journals.ametsoc.org/view/journals/mwre/142/5/mwr-d-13-00248.1.xml
Calibration uses local rain mean; bridging uses SST; one predictor/predictand per model. log–sinh; BMA combines calibrated/bridged predictions.
Quote: “the year to be forecast, the year before and the year after are omitted”.
Leave-three-years-out guards neighbors, but does not remove all future trend information.

## Multivariate seasonal comparison
Schepen/Everingham/Wang2020 DOI10.1175/MWR-D-19-0046.1.
https://journals.ametsoc.org/view/journals/mwre/148/1/mwr-d-19-0046.1.xml
1981–2016 System4 hindcast+archived forecasts, first15 raw members;36 available years and35 training pairs per LOYO fit. Three-month rainfall/Tmin/Tmax averages, one-month lead,12 overlapping seasons. MBJP vs UBJP+Schaake (window/block) vs transformed QM; not an ECC performance test.
UBJP+BSS strongest overall in that experiment; MBJP superior in-sample but overfits cross-validation.
Quote: “there is insufficient data to robustly infer the MBJP model parameters”.
Parameter formula excluding transform:2d+d(d−1)/2. DERIVED d6→27 joint vs3×5=15 separate. Not a universal sample threshold.
200 generated calibrated scenarios are not200 independent training years. Block SS is not bootstrap.

## Trend temperature
Shao et al.2021 DOI10.1175/MWR-D-20-0318.1.
https://journals.ametsoc.org/view/journals/mwre/149/8/MWR-D-20-0318.1.xml
SEAS5 1981–2016,25 raw members, Australian seasonal Tmin/Tmax. BJP-t separate transformed model/obs trends; BJP-ti zero-centered informative normal trend priors.
Quote: “in favor of no or weak trends in calibrated forecasts”.
LOYO caveat: trend skill can include future information. No transfer of Australian grid-derived prior scales to Korean single regional series.

## Trend precipitation
Shao et al.2022 DOI10.1175/JHM-D-21-0099.1.
https://journals.ametsoc.org/view/journals/hydr/23/1/JHM-D-21-0099.1.xml
SEAS5 seasonal rain, ensemble mean, log–sinh/left-censored zero, distinct trends and zero-centered prior.7×7 neighboring cells/three adjacent seasons used for local prior,75th percentile absolute scaled slope. This is sourced design, not recommendation to reproduce unavailable spatial pooling.
Overall comparable to ordinary BJP; gains only conditional.
Quote: “The cross-validated forecasts over the hindcast period may contain artificial skill”.
Changing-year latent censor threshold required after detrending.

## Access limits and EXPAND disposition
- Monthly catchment DOI10.1016/j.jhydrol.2014.03.017: original403/captcha; closed as access gap, not methodological confirmation.
- Earlier temperature DOI10.1002/joc.6788:403; newer readable2021 primary covers trend mechanism, duplicate lead closed.
- Daily extension https://hess.copernicus.org/articles/22/1615/2018/: extraction chiefly references; closed as nonessential daily-to-aggregate gap.
- Small-member signal/noise: assigned joint-gaussian owner wave2.
- Past-only operational validation: assigned validation owner, not an unperformed skill finding.
- 2025 spread paper DOI10.1002/qj.4925: source identity only; assigned joint-gaussian wave2, no asserted outcome.
- Counter-search no exact match for all project constraints: evidence gap, not proof of absence.

## Cleanup
No spawned process/browser/temp clone by this recovery lane; no cleanup required.
