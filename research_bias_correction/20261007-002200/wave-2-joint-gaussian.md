# Joint Gaussian final dossier

Observer joint-gaussian,2026-10-06;14 varied English queries; primary full AMS text. All source leads closed; no files/resources created.

## Source-locked methods
Fixed transformed bivariate joint Gaussian: predictor raw historical ensemble mean and predictand annual same-window observation. Conditional mean mu_y+Sigma_yx Sigma_xx^-1(z_x−mu_x); Schur conditional variance. This is closely related to Gaussian MOS. Basic BJP adds posterior averaging of joint means/covariances and censoring/back-transformation. Predictive mixture generally not Gaussian. MAP transform parameters in2020/2022 are fixed later, not all uncertainty propagated.
Joint T/P additionally fits cross-variable predictive covariance; d4 would have14 joint-normal parameters versus two d2 models total10, excluding transforms (DERIVED from source formula; not minimum sample rule).
Mean-based BJP only needs annual mean/window pairing, not original member identity. Raw ECC template requires raw member identity/alignment.

## Advantages and limits
UBJP: explicitly models forecast-observation relation and Bayesian parameter uncertainty; weak signal can revert toward observation marginal. Basic mean-only version discards spread information. Transformation/tail/prior/MCMC diagnostics required.24/30years not proof of enough information.
MBJP/coplanar T/P: joint conditional events; greater covariance burden, dry transform/back-transform sensitivity.2020 Australian System4 36available/35fitLOYO annual seasonal T/P study: MBJP in-sample superiority did not survive CV. Paper not Korean weekly/monthly, not generic ECC benchmark.
Trend BJP-t/ti: observation/model separate transformed slopes; zero-centered priors moderate trend sampling. Priors derived from unavailable Australian spatial pools not portable. LOYO may use future observations, so operational skill must be past-only.
Rain trend censor after detrending: c_i(t)=g_i(0)−alpha_i(t−t_mid), not fixed threshold. Trend-rain benefit conditional, not universal.

## Finite-member candidate
Siegert2016 DOI10.1175/JCLI-D-15-0196.1: GloSea5 DJFNAO20year sample/24lagged members. Bayesian Gaussian signal-noise:
y=mu_y+s+epsilon; x_r=mu_x+beta*s+eta_r.
DERIVED under independent homogeneous member errors:
Var(mean x|M)=beta²sigma_s²+sigma_eta²/M;
Cov(y,mean x)=beta*sigma_s².
Conditional mean/variance use issued M. Can address mean noise from3/7 vs larger issuedM, but not by blindly multiplying current EMOS variance. Exchangeability alone does not imply independent errors or1/M law. Model adequacy/prior sensitivity/parameter identifiability and regime comparability pending. T first; paper's GaussianNAO does not directly validate rain.

## Other sources and implementation boundary
- DOI10.1175/JAMC-D-19-0093.1, https://journals.ametsoc.org/view/journals/apme/59/3/jamc-d-19-0093.1.xml : monthly station copula postprocessing, forecast-observation copulas then SS. Maximum-likelihood family selection, NOT Bayesian posterior.
- https://arxiv.org/abs/1607.04736 : Gaussian copula tail-independence mathematics, not climate performance. No compound-extreme transfer claims.
- https://researchdata.edu.au/bayesian-joint-probability-r-packages/1449950 : CSIRO2020 twoR packages metadata, DOI10.25919/5e83ec773ecd8. API/license/runtime not inspected or executed.
- https://www.cpc.ncep.noaa.gov/products/people/sstrazzo/cbam/about.php : operational CBaM existence only.

## EXPAND closed
Original streamflow Wiley2009/2011 body empty; newer seasonal2020/2022 directly supports adopted zero machinery. Gamma-Gaussian hydrology DOI10.1016/j.jhydrol.2021.126893 CAPTCHA: metadata-only optional, no formula/efficacy assertion.
Spread paper2025 DOI10.1002/qj.4925 empty: access gap, mean-only baseline limit unchanged.
Exchangeability/identity/provenance/priors: implementation prerequisites, not new proved claims.
No remaining actionable source lead; all recommendations conditional on new held-out GloSea6 experiments.
