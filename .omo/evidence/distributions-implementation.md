# Original-unit predictive distributions: implementation and actual QA

Date: 2026-10-07. Scope: distribution laws, not model fitting or verified-target
skill. Native Python 3.13.13, existing NumPy/SciPy environment; no installations,
Git operations, baseline reruns, data edits or observation access for fitting.

## Delivered callable surface

`analysis.alternative_distributions` exports the frozen section-3 interfaces:

```python
weighted_empirical(values, weights)
normal(mu, sigma, censor_zero=False)
student_t(df, loc, scale)
logistic(loc, scale)
lognormal(log_mu, log_sigma)
affine(base, offset, scale)
gamma(shape, scale, shift=0.0, censor_zero=False)
power_censored(base, power, unit_scale)
hurdle(p_zero, positive)
mixture(parts, weights)
censored_gev(loc, scale, shape)
tweedie(mu, phi, power)
bernstein(coefficients, p_zero=0.0)
cdf_crps(distribution, observation, scale, tolerance=1e-7)
distribution_from_spec(spec)
```

Every law supplies `cdf`, `cdf_left`, `quantile`, `mean`, `crps`,
`log_density`, `atom_mass`, and `to_spec`. Arrays are float64; internal law DTOs
are frozen, keyword-only, slotted. Empirical/coefficient/weight storage is copied
and marked read-only. Degenerate constructors produce actual point laws.

Gamma shift is ADDITIVE: `gamma(k, theta, shift=-delta, censor_zero=True)`
implements the prescribed CSG. Power is the FORWARD physical-to-latent exponent:
`power_censored(base, .5, 100)` returns `100*max(0,Z)**2`, never `100*Z**2`.
Negative affine scales reflect both left/right CDFs and atom-aware quantiles.
Hurdle intensity must be strictly positive; zero likelihood uses atom mass,
not continuous density plus atom probability.

Tagged JSON uses `tag`, never pickle or stored-quantile replacement laws:
`weighted_empirical`, `normal`, `student_t`, `logistic`, `lognormal`, `gamma`,
`censored_gev`, `affine`, `power_censored`, `hurdle`, `mixture`, `tweedie`,
`bernstein`. Scientific-law parameters are explicit ordered `parameters`;
composites retain their nested complete law, weights, scales and censor flags.
Canonical reduction of a degenerate or all-empirical mixture to an exact
empirical law is deliberate, not a distribution approximation.

Example:

```json
{"tag":"power_censored","base":{"tag":"student_t","parameters":[9,0,1],"censor_zero":false},"power":0.5,"unit_scale":100}
```

## Numerical implementation

- Normal/censored-Normal CRPS calls the existing analytic `gaussian_crps`
  without changing it. Weighted empirical CRPS is exact after tie merging.
- Uncensored Normal mixtures use the analytic cross-component absolute-Normal
  formula. Other mixtures integrate the MIXED CDF, not average component CRPS.
- Continuous CDF/PPF/densities use the installed SciPy laws; GEV shape is
  converted to SciPy's opposite sign. CSG mean uses the exact Gamma survival
  expression. Power and censored GEV means use survival integration in original
  units, split around actual support and quantile landmarks.
- `cdf_crps` integrates survival functions in upper tails, splits at the
  observation, support landmarks and explicit atoms, and returns the frozen
  `NumericIntegral(value,error,converged)`. Quadrature uses limit 200 and one
  tenfold refinement if its bound is exceeded. A failed bound raises in `crps`,
  rather than returning an unqualified score.
- Tweedie is the exact compound-Poisson Gamma series. No single-Gamma,
  Normal, saddlepoint or sample approximation is substituted. Poisson omission
  mass and first-moment bounds are exposed as `cdf_mass_bound` and
  `cdf_first_moment_bound`, each controlled to 1e-12. Positive density finds its
  OWN term mode, retains the union with the CDF/moment range, and bounds both
  omitted density tails geometrically. `density_bounds(x)` returns
  `(log_density, log_absolute_remainder, relative_remainder)`, requiring
  absolute remainder <=1e-12 AND relative remainder <=1e-9. Direct Tweedie CRPS
  includes `2*(omitted_first_moment + max(0,y)*omitted_mass)` in its reported
  integration error; affine/hurdle/mixture propagation retains those bounds.
- Means are not inverse transforms of latent means. Student laws require df>1;
  directly powered Student laws additionally require df>inverse_power.

## Actual executable checks

The saved executable driver is `analysis/alternative_distribution_audit.py`.
It imports and executes the real public module, calls the independently owned
`alternative_validation_distributions.production_checks`, uses independent
SciPy/CDF quadrature and Poisson-Gamma sums, reads the saved numerical reference
oracles, and verifies the 60-file preservation receipt.

Exact final invocation, repository root:

```text
.venv/Scripts/python.exe -B -m analysis.alternative_distribution_audit
```

Actual final output, exit code **0**:

```json
{
  "independent_laws": 22,
  "independent_status": "PASS",
  "extra": {
    "roundtrip_laws": 27,
    "edge_checks": "PASS",
    "saved_reference_oracle": ".omo\\evidence\\alternative-reference-oracles.json",
    "sqrt_t9_mean": 64.28571428571416,
    "mixture_crps": 2.5
  },
  "tweedie_density": {
    "density_certificate": "PASS",
    "integrated_mass": 0.9999999999999699,
    "integrated_mean": 24.999999999999698,
    "integrated_variance": 249.99999999995987,
    "invalid_inputs_rejected": 9
  },
  "protected_hashes": 60,
  "elapsed_seconds": 30.22101289999955
}
```

Coverage includes Normal and censored-Normal, tied empirical distributions,
mixture cross terms, additive CSG shift, regular/all-wet/all-dry hurdles,
square/cube original-mm inverses, negative latent locations, Student-t9 rain
moment/quantile reference, Gumbel/positive/negative/near-zero GEV shapes and
finite endpoints, Tweedie p=1.2/1.5/1.8, mu=0, rare dry and high-count cases,
bounded/constant/rain Bernstein laws, positive/negative/zero affine scales,
finite/infinite CDF limits, generalized-inverse inequalities, atom/left-CDF
agreement, density/atom separation, JSON roundtrips and invalid constructors.

The independently saved reference used is
`.omo/evidence/alternative-reference-oracles.json`: mixture CRPS 2.5 (not 5),
negative-latent inverse 0, Student-t9 square-root rain mean
64.28571428571429 and P95 336.0303023871549. Independent CP-Gamma integration
for `(mu,phi,p)=(25,2,1.5)` checks atom+density total 1, mean 25, variance 250.

Two earlier driver defects were found and repaired: constant Bernstein
polynomial rounding could move a point quantile infinitesimally below its
atom; evaluation now returns the constant exactly. The specialized Tweedie
helper's initial discriminator was `type`; it was integrated into the shared
`tag` roundtrip contract. No independent oracle was edited to pass.

## Native/static checks and file-size gate

Exact native commands (each exited **0**):

```text
.venv/Scripts/basedpyright.exe analysis/alternative_distributions.py analysis/alternative_distribution_base.py analysis/alternative_distribution_integrals.py analysis/alternative_distribution_transforms.py analysis/alternative_distribution_mixture.py analysis/alternative_distribution_bernstein.py analysis/alternative_distribution_tweedie.py analysis/alternative_distribution_audit.py
.venv/Scripts/ruff.exe check analysis/alternative_distributions.py analysis/alternative_distribution_base.py analysis/alternative_distribution_integrals.py analysis/alternative_distribution_transforms.py analysis/alternative_distribution_mixture.py analysis/alternative_distribution_bernstein.py analysis/alternative_distribution_tweedie.py analysis/alternative_distribution_audit.py
```

Actual output: `0 errors, 0 warnings, 0 notes`; `All checks passed!`.
LSP was queried before execution. Its workspace namespace could not resolve
`analysis.*` and a later Tweedie refresh timed out; native project checks above
are decisive, rather than ignoring those LSP messages.

Final nonblank/noncomment source-line counts (docstrings included):

|Owned module|Lines|
|---|---:|
|alternative_distributions.py|181|
|alternative_distribution_base.py|162|
|alternative_distribution_integrals.py|72|
|alternative_distribution_transforms.py|129|
|alternative_distribution_mixture.py|108|
|alternative_distribution_bernstein.py|89|
|alternative_distribution_tweedie.py|182|
|alternative_distribution_audit.py|160|

All are <=250. No typecasts, suppressed warnings, pandas, decorative pytest
tree, fake dependency fallback or model-cost exclusion was introduced.

## Boundaries and cleanup

This receipt establishes the distribution layer, not success of unfinished
root/model/runner lanes. No training/target DTO or catalog vintage rule was
changed. The standalone audit's independent-validator dependency existed and
executed; there is no unavailable-module PASS fallback. Extremely large
compound-Poisson ranges still require actual series computation and may consume
resources; no expense-based scientific gate or alternate law is used.

All Python checks ended; audit monitors completed. A broad skill-path discovery
shell was explicitly killed. No persistent service, temporary fixture,
environment change or protected artifact remained.
