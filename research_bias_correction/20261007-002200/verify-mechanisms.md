# Executed mechanism verification

Invocation: functions.eval(language="js"), deterministic synthetic calculation on Node v24.14.1 / win32, 2026-10-06.
No new process, port, browser or file was created by the calculation. Cleanup: none required.
This is an algorithm mechanism proof, NOT an experiment proving GloSea6 forecast skill or Bayesian estimation correctness.

## Joint Gaussian
Inputs: mu_x=1, mu_y=10, sigma_x=2, sigma_y=3, rho=0.6, x=3.
Executed formulas:
```js
conditionalMean = muy + rho * sy / sx * (x - mux);
conditionalVariance = sy**2 * (1 - rho**2);
schur = sy**2 - (rho * sx * sy)**2 / sx**2;
```
Output: mean=11.8, variance=5.76, independent Schur complement=5.760000000000001.
PASS: mean equals 11.8 within 1e-12 and variance equals Schur complement within 1e-12.
Consequence limited to fixed Gaussian parameters: conditional prediction is linear regression with Gaussian residual. Bayesian posterior parameter averaging and transforms need separate fitting.

## Reordering and marginal scores
Inputs: T=[1,2,3,4], P=[40,30,20,10], reordered P=[10,20,30,40], observed precipitation=25.
```js
const crps = (a,y) =>
 a.reduce((s,v)=>s+Math.abs(v-y),0)/a.length -
 a.flatMap(v=>a.map(w=>Math.abs(v-w))).reduce((s,v)=>s+v,0)/(2*a.length*a.length);
```
Outputs: empirical CRPS original=3.75, reordered=3.75.
Joint event T>2 and P>25: original frequency=0, reordered=0.5.
PASS: marginal empirical CRPS invariant; joint event changes.
Not proof that chosen dependence template is correct. ECC/Schaake need aligned physical scenarios and held-out joint scores.

## Zero rainfall
Executed Math.log(0)=-Infinity, Number.isFinite false.
max(0,z) on latent [-3,-1,2,4] gives [0,0,2,4], all nonnegative.
PASS: naive log transform fails on zero, censoring creates a zero mass.
Not proof of an adequate rain tail. Transform-offset, hurdle, censoring and truncated distributions are distinct model designs.

## Mixture variance and member-error assumptions
Additional exact invocation functions.eval(js), same Node/win32,2026-10-06.
CDFmixtureweight0.5,componentmeans0/10,componentvariances1/1:
mean5; E[var]+Var(E)=0.5*(1+0²)+0.5*(1+10²)−5²=26.
Naivewithin-onlyvariance1 is wrong. PASS26 exact.
Finite-memberexample signalvariance4,membernoisevariance9,beta1:
independentmeanvarianceM3=7;M7=5.285714285714286.
Ifmembererrorpaircorrelation0.5,M7meanvariance=4+9*(0.5+0.5/7)=9.142857142857142.
PASS: correlatederrorsnotcapturedbyindependent1/Mlaw. This is a syntheticcovariancemodel, NOT archiveestimatedcorrelation or validatedsizecorrection.
Cleanup: no externalresources/file/processspawned.
