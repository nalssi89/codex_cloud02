"""Independent predictive-law equivalence and unchanged-transition receipts."""

from __future__ import annotations

import hashlib
import json
import math
from time import perf_counter

import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr
from scipy.stats import gamma, multivariate_t

from analysis.alternative_bayes_algebra import condition, residual_predictive, update
from analysis.alternative_bayes_sampler import Chain
from analysis.calibration import FloatArray


def transition_receipt() -> dict[str, str]:
    """Hash only Gibbs states/RNG, never the predictive output being improved."""
    result: dict[str, str] = {}
    joint = np.asarray([[0.2, 0.0], [0.4, 0.3], [0.0, 0.0], [0.6, 0.8]])
    for name in ("importance", "augmented", "nig"):
        nig = name == "nig"
        values = joint[:, 1:] if nig else joint
        design = np.column_stack((np.ones(4), joint[:, 0])) if nig else np.ones((4, 1))
        variances = np.asarray([4., 1.]) if nig else np.ones(1)
        target_design = np.asarray([1., 0.25]) if nig else np.ones(1)
        predictor = np.empty(0) if nig else np.asarray([0.0 if name == "augmented" else 0.25])
        chain = Chain(
            values, design, variances, target_design, predictor,
            np.asarray(np.equal(values, 0), dtype=float),
            np.asarray(np.equal(predictor, 0), dtype=float), 1917,
            nig=nig, augmented=name == "augmented",
        )
        digest = hashlib.sha256()
        for step in range(100):
            emitted_mean, _, emitted_weight, _ = chain.step()
            if name == "augmented":
                assert emitted_weight == 0.0
                assert np.size(chain.values, axis=0) == 5
                posterior = update(chain.values, chain.design, variances)
                df, mean, scale = posterior.predictive(target_design)
                _, exact_mean, _ = condition(mean, scale, chain.values[-1, :1], df)
                np.testing.assert_allclose(emitted_mean, exact_mean, atol=1e-13)
            if step in (0, 9, 99):
                for state in (chain.values, chain.coefficients, chain.covariance):
                    digest.update(state.tobytes())
                digest.update(json.dumps(chain.rng.bit_generator.state, sort_keys=True).encode())
        result[name] = digest.hexdigest()
    return result


def scalar_equivalence(nx: int, nig: bool) -> dict[str, float]:
    """Integrate the IW residual scale, independently divide Student densities."""
    rng = np.random.default_rng(710 + nx)
    values = rng.normal(size=(18, nx + 1)) + np.linspace(0.1, 0.7, nx + 1)
    design = np.column_stack((np.ones(18), np.linspace(-0.7, 1.1, 18)))
    variances = np.asarray([4., 1.]) if nig else np.asarray([1., 4.])
    posterior = update(values, design, variances, nig=nig)
    h = np.asarray([1., 1.6])
    x = np.linspace(0.2, 0.6, nx)
    mean = h @ posterior.coefficients
    c = 1 + float(h @ posterior.row_covariance @ h)
    v = posterior.iw_df - nx
    joint_scale = c / v * posterior.iw_scale
    predictor_density = float(multivariate_t.pdf(
        x, loc=mean[:nx], shape=joint_scale[:nx, :nx], df=int(v)
    )) if nx else 1.0
    psi = posterior.iw_scale
    psi_residual = psi.item(nx, nx)
    if nx:
        psi_residual -= (psi[nx:, :nx] @ np.linalg.solve(
            psi[:nx, :nx], psi[:nx, nx:]
        )).item(0, 0)
    unit_covariance = np.eye(nx + 1)
    component_mean, component_covariance, log_weight = residual_predictive(
        posterior, unit_covariance, h, x
    )
    np.testing.assert_allclose(log_weight, math.log(predictor_density), atol=1e-12)
    ell, k = component_mean.item(0), component_covariance.item(0, 0)

    def density_oracle(z: float) -> float:
        return float(multivariate_t.pdf(
            np.concatenate((x, np.asarray([z]))), loc=mean,
            shape=joint_scale, df=int(v),
        )) / predictor_density

    def integrated_component(g: float, moment: int) -> float:
        variance = k * psi_residual / (2 * g)
        sd = math.sqrt(variance)
        if moment == 0:
            value = float(ndtr(-ell / sd))
        elif moment == 1:
            value = math.exp(-0.5 * ((0.7 - ell) / sd) ** 2) / (
                sd * math.sqrt(2 * math.pi)
            )
        else:
            a = ell / sd
            value = 100 * ((ell * ell + variance) * float(ndtr(a))
                           + ell * sd * math.exp(-a * a / 2) / math.sqrt(2 * math.pi))
        return value * float(gamma.pdf(g, posterior.iw_df / 2))

    collapsed = [
        quad(lambda g, selected=moment: integrated_component(g, selected), 0, math.inf,
             epsabs=1e-10, epsrel=1e-10)[0]
        for moment in range(3)
    ]
    reference = [
        quad(density_oracle, -math.inf, 0, epsabs=1e-11)[0],
        density_oracle(0.7),
        quad(lambda z: 100 * z * z * density_oracle(z), 0, math.inf,
             epsabs=1e-9, epsrel=1e-10)[0],
    ]
    np.testing.assert_allclose(collapsed, reference, rtol=1e-10, atol=1e-9)
    # Changing discarded nuisance blocks while retaining Omega cannot change law.
    nuisance = np.linspace(0.3, 0.8, nx)
    unit_covariance[:nx, -1] = nuisance
    unit_covariance[-1, :nx] = nuisance
    unit_covariance[-1, -1] += float(nuisance @ nuisance)
    mean_again, covariance_again, weight_again = residual_predictive(
        posterior, unit_covariance, h, x
    )
    np.testing.assert_allclose(mean_again, component_mean, atol=1e-14)
    np.testing.assert_allclose(covariance_again, component_covariance, atol=1e-14)
    assert weight_again == log_weight
    return {
        "atom_error": abs(collapsed[0] - reference[0]),
        "density_error": abs(collapsed[1] - reference[1]),
        "physical_rain_mean_error": abs(collapsed[2] - reference[2]),
    }


def multivariate_moment_equivalence() -> float:
    rng = np.random.default_rng(821)
    values = rng.normal(size=(24, 4))
    design = np.ones((24, 1))
    posterior = update(values, design, np.ones(1))
    degrees, joint_mean, joint_scale = posterior.predictive(np.ones(1))
    x = np.asarray([0.8, -0.5])
    conditional_df, conditional_mean, student_scale = condition(
        joint_mean, joint_scale, x, degrees
    )
    assert conditional_df is not None
    psi = posterior.iw_scale
    residual = psi[2:, 2:] - psi[2:, :2] @ np.linalg.solve(psi[:2, :2], psi[:2, 2:])
    covariance = np.eye(4)
    covariance[2:, 2:] = residual / (posterior.iw_df - 2 - 1)
    rb_mean, rb_covariance, _ = residual_predictive(posterior, covariance, np.ones(1), x)
    exact_covariance = student_scale * conditional_df / (conditional_df - 2)
    np.testing.assert_allclose(rb_mean, conditional_mean, atol=1e-13)
    np.testing.assert_allclose(rb_covariance, exact_covariance, atol=1e-13)
    error: FloatArray = np.abs(rb_covariance - exact_covariance)
    return float(np.max(error))


def main() -> None:
    started = perf_counter()
    receipts = transition_receipt()
    assert receipts == {
        "augmented": "16e8816aee15e53affff950cc0a6474ceb787ad23c86a4f68082e810500d23b8",
        "importance": "51cb418b9b822b3f1fb20dcb25c43a9e0a7fca36d1e6d43bd6f5dde4ba4754b1",
        "nig": "9e68391a2192358f7a7cf9fe6da6d6f03fcd7d0c9139800517d22dd6a2673312",
    }, receipts
    results = {f"predictors_{nx}": scalar_equivalence(nx, nx == 0) for nx in (0, 1, 3)}
    print(json.dumps({
        "status": "PASS", "transition_fingerprints_unchanged": receipts,
        "equivalence": results,
        "multivariate_covariance_error": multivariate_moment_equivalence(),
        "elapsed_seconds": perf_counter() - started,
    }, indent=2))


if __name__ == "__main__":
    main()
