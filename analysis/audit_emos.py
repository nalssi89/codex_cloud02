"""Read-only EMOS numerical audit; run with .venv/Scripts/python.exe.

Run only after core outputs have been rebuilt from the selected observation source:
daily station count >=50, actual-n means (including 61/60), no 62/n scaling or
raw-station imputation. Case counts follow saved fits; observation-policy and
calendar validation belong to the separate training audit.

The numerical oracle integrates CDFs, not the production CRPS expression.
Sensitivity uses a separately expressed expectation identity and SLSQP without
the production gradient. Selection never reads held-out scores. No global
optimality or statistical identification claim follows from solver agreement.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from collections import Counter, defaultdict
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import TypeAlias

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import minimize
from scipy.special import ndtr, ndtri

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis import calibration
from analysis.calibration import FloatArray, calibrate, gaussian_crps
from analysis.data_io import (
    DATASET,
    csv_rows,
    load_forecasts,
    load_hindcasts,
    observation_daily_path,
    observation_provenance,
)
from analysis.scoring import distribution_summary
from analysis.validate_results import day, observation_summary, parse_daily

Json: TypeAlias = str | int | float | bool | None | list["Json"] | dict[str, "Json"]
SQRT_PI = math.sqrt(math.pi)
Objective: TypeAlias = Callable[
    [FloatArray, FloatArray, FloatArray, FloatArray, bool], tuple[float, FloatArray]
]


def objective(p: FloatArray, m: FloatArray, v: FloatArray,
              y: FloatArray, rain: bool) -> tuple[float, FloatArray]:
    """Typed collection of runtime diagnostic seams, not a production copy."""
    name = "_objective"
    seams: list[Objective] = [getattr(calibration, name)]
    return seams[0](p, m, v, y, rain)


def average(values: FloatArray) -> float:
    """Avoid imprecise inferred ndarray scalar types."""
    return math.fsum(float(v) for v in values.flat) / values.size


def positive_mean(mu: float, sigma: float) -> float:
    """Independent tail mean: integrate survival, retaining extreme tail mass."""
    t = mu / sigma
    low = max(0.0, t - 12.0)
    value, _ = quad(lambda x: 0.5 * math.erfc((x - t) / math.sqrt(2)),
                    low, max(12.0, t + 12.0),
                    epsabs=1e-300, epsrel=2e-12, limit=150)
    return sigma * (low + value)


def cdf_crps(mu: float, sigma: float, y: float, censored: bool) -> float:
    """CRPS/sigma integration in standardized coordinates, split at observation."""
    z = (y - mu) / sigma
    lower = -mu / sigma if censored else min(-12.0, z)
    upper = max(12.0, z + 12.0)

    def left(x: float) -> float:
        return (0.5 * math.erfc(-x / math.sqrt(2))) ** 2

    def right(x: float) -> float:
        return (0.5 * math.erfc(x / math.sqrt(2))) ** 2

    left_points = sorted({lower, z, *(x for x in (-12.0, 0.0, 12.0) if lower < x < z)})
    right_points = sorted({z, upper, *(x for x in (-12.0, 0.0, 12.0) if z < x < upper)})
    first = math.fsum(quad(left, a, b, epsabs=1e-14, epsrel=2e-12, limit=150)[0]
                      for a, b in pairwise(left_points))
    second = math.fsum(quad(right, a, b, epsabs=1e-14, epsrel=2e-12, limit=150)[0]
                       for a, b in pairwise(right_points))
    return sigma * (first + second)


def independent_loss(p: FloatArray, m: FloatArray, v: FloatArray,
                     y: FloatArray, rain: bool) -> float:
    """Expectation identity, independently implemented from gaussian_crps."""
    a, b, c, d = (float(x) for x in p.flat)
    mu = a + b * m
    sigma = np.sqrt(c + d * v)
    t = mu / sigma
    z = (mu - y) / sigma
    pdf_t = np.exp(-t * t / 2) / math.sqrt(2 * math.pi)
    pdf_z = np.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    if rain:
        mass = ndtr(t)
        mean = sigma * (t * mass + pdf_t)
        excess = sigma * (z * ndtr(z) + pdf_z)
        integral = sigma * (
            t * mass**2 + 2 * mass * pdf_t - ndtr(math.sqrt(2) * t) / SQRT_PI
        )
        score = y - 2 * mean + 2 * excess + integral
    else:
        score = sigma * (2 * pdf_z + z * (2 * ndtr(z) - 1) - 1 / SQRT_PI)
    return average(np.asarray(score, dtype=np.float64))


def hashes(root: Path) -> dict[str, str]:
    """Hash actual source bytes and existing prediction inputs, never git state."""
    paths = sorted((root / DATASET).rglob("*"))
    paths += [root / "analysis" / name for name in
              ("calibration.py", "scoring.py", "data_io.py", "run_verification.py")]
    paths += [root / "outputs" / name for name in
              ("calibration_fits.csv", "training_ledger.csv.gz",
               "matched_predictions.csv.gz", "calibrated_members.csv.gz")]
    result: dict[str, str] = {}
    for path in paths:
        if path.is_file():
            with path.open("rb") as handle:
                result[str(path.relative_to(root))] = hashlib.file_digest(handle, "sha256").hexdigest()
    return result


def numerical_checks() -> dict[str, Json]:
    """Stress scalar/vector broadcasting, censoring, gradients and tiny spread."""
    oracle: list[Json] = []
    for rain in (False, True):
        for mu, sigma, y in (
            (0.0, 1.0, 0.0), (-2.0, 1.0, 0.0), (-8.0, 1.0, 0.0),
            (-10.0, 1.0, 0.0), (-12.0, 1.0, 0.0), (-20.0, 1.0, 0.0),
            (-40.0, 1.0, 0.0), (-1e8, 1.0, 0.0),
            (3.0, 2.0, 7.0), (1.0, 1e-8, 1.0),
            (2e6, 1e5, 3e6), (-10.0, 0.001, 3.0),
        ):
            observed = np.asarray(y, dtype=np.float64)
            score = gaussian_crps(np.asarray(mu), np.asarray(sigma), observed, rain)
            actual = float(score)
            reference = cdf_crps(mu, sigma, y, rain)
            independent = independent_loss(
                np.array([mu, 0.0, sigma**2, 0.0], dtype=np.float64),
                np.zeros(1), np.zeros(1), np.array([y], dtype=np.float64), rain,
            )
            oracle.append({
                "rain": rain, "mu": mu, "sigma": sigma, "y": y,
                "production": actual, "cdf_integral": reference,
                "independent_expectation_loss": independent,
                "independent_oracle_error": abs(independent - reference),
                "absolute_error": abs(actual - reference),
                "negative": actual < 0, "scalar_shape": list(score.shape),
            })
    gradients: list[Json] = []
    m = np.array([0.2, 0.8, 1.2, 2.0], dtype=np.float64)
    v = np.array([0.0, 0.3, 0.8, 1.6], dtype=np.float64)
    y = np.array([0.0, 0.6, 1.7, 2.3], dtype=np.float64)
    for rain in (False, True):
        for name, p in (
            ("interior", np.array([-0.4, 0.8, 0.4, 0.6], dtype=np.float64)),
            ("boundary_near", np.array([-0.1, 1e-7, 1.01e-6, 1e-7], dtype=np.float64)),
            ("floor_transition", np.array([0.0, 0.0, 1e-6, 0.0], dtype=np.float64)),
        ):
            _, analytic = objective(p, m, v, y, rain)
            for index in range(4):
                step = 1e-5 * max(abs(float(p.flat[index])), 1.0)
                if index in (0, 1):
                    step = min(step, math.sqrt(float(p.flat[2])) * 1e-4 / float(m.max()))
                if index == 2:
                    step = min(step, float(p.flat[index]) * 1e-3)
                if index == 3:
                    step = min(step, float(p.flat[2]) * 1e-3 / float(v.max()))
                if index in (1, 3) and float(p.flat[index]) < step:
                    # Second-order forward derivative at/near active bounds.
                    q1, q2 = p.copy(), p.copy()
                    q1[index] += step
                    q2[index] += 2 * step
                    estimate = (-3 * independent_loss(p, m, v, y, rain)
                                + 4 * independent_loss(q1, m, v, y, rain)
                                - independent_loss(q2, m, v, y, rain)) / (2 * step)
                else:
                    q1, q2 = p.copy(), p.copy()
                    q1[index] += step
                    q2[index] -= step
                    estimate = (independent_loss(q1, m, v, y, rain)
                                - independent_loss(q2, m, v, y, rain)) / (2 * step)
                exact = float(analytic.flat[index])
                gradients.append({
                    "rain": rain, "setting": name, "parameter": "abcd"[index],
                    "analytic": exact, "finite_difference": estimate, "step": step,
                    "relative_error": abs(exact - estimate) / max(1.0, abs(exact)),
                })
    means: list[Json] = []
    for mu in (-5.0, -8.0, -9.0, -10.0, -12.0, -20.0, -40.0):
        mean, probs, quantiles = distribution_summary(mu, 1.0, np.array([0.0, 1.0]), True)
        oracle_mean = positive_mean(mu, 1.0)
        means.append({
            "mu": mu, "sigma": 1.0, "production_mean": mean,
            "survival_integral_mean": oracle_mean,
            "relative_error": abs(mean - oracle_mean) / max(oracle_mean, 1e-300),
            "absolute_error": abs(mean - oracle_mean),
            "probabilities": [float(x) for x in probs.flat],
            "quantiles": [float(x) for x in quantiles.flat],
        })
    vector = gaussian_crps(np.array([-2.0, 0.0]), np.array([1.0]),
                           np.array([0.0, 1.0]), True)
    cancellation: list[Json] = []
    for sigma in (1e-6, 1.0, 1e6):
        mus = sigma * np.linspace(-12.0, -2.0, 501)
        scores = gaussian_crps(mus, np.full(mus.size, sigma), np.zeros(mus.size), True)
        minimum = int(np.argmin(scores))
        mu = float(mus.flat[minimum])
        cancellation.append({
            "sigma": sigma, "mu_at_minimum": mu,
            "minimum_crps": float(scores.flat[minimum]),
            "negative_count": int(np.count_nonzero(scores < 0)),
            "cdf_integral_at_minimum": cdf_crps(mu, sigma, 0.0, True),
        })
    return {"crps_oracle": oracle, "gradient_checks": gradients,
            "negative_latent_mean_checks": means, "broadcast_shape": list(vector.shape),
            "cancellation_scan": cancellation}


@dataclass
class Training:
    """Only training predictors and observations enter sensitivity selection."""

    row: Mapping[str, str]
    means: FloatArray
    variances: FloatArray
    observed: FloatArray
    forecast: FloatArray
    scale: float
    shift: float
    parameters: FloatArray
    condition: float

    @property
    def rain(self) -> bool:
        return self.row["VARIABLE"] == "prcp"

    def scaled(self) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
        a, b, c, d = (float(x) for x in self.parameters.flat)
        p = np.array([(a - self.shift + b * self.shift) / self.scale,
                      b, c / self.scale**2, d], dtype=np.float64)
        return (p, (self.means - self.shift) / self.scale,
                self.variances / self.scale**2, (self.observed - self.shift) / self.scale)


def selection(cases: list[Training]) -> list[Training]:
    """Predeclared cap: eight per product/variable, selected without target OBS.

    Six training-only extremes (max b,d, min scaled c,b,d, max design
    condition), followed by two spread lead/year anchors; duplicate selectors
    are replaced with evenly spaced chronological/lead entries.
    """
    ordered = sorted(cases, key=lambda x: (x.row["CASE_ID"].split("_")[2], x.row["CASE_ID"]))
    selectors = [
        max(cases, key=lambda x: float(x.parameters.flat[1])),
        max(cases, key=lambda x: float(x.parameters.flat[3])),
        min(cases, key=lambda x: float(x.parameters.flat[2]) / x.scale**2),
        min(cases, key=lambda x: float(x.parameters.flat[1])),
        min(cases, key=lambda x: float(x.parameters.flat[3])),
        max(cases, key=lambda x: x.condition),
        ordered[len(ordered) // 4], ordered[3 * len(ordered) // 4],
    ]
    selectors += [ordered[int(i)] for i in np.linspace(0, len(ordered) - 1, 32)]
    picked: list[Training] = []
    keys: set[str] = set()
    for candidate in selectors:
        key = candidate.row["CASE_ID"]
        if key not in keys:
            picked.append(candidate)
            keys.add(key)
        if len(picked) == 8:
            break
    return picked


def sensitivity(case: Training) -> dict[str, Json]:
    """Three deterministic SLSQP starts; every unsuccessful solve is reported."""
    p, m, v, y = case.scaled()
    residual = y - m
    starts = [
        p,
        np.array([average(y), 0.0, max(float(y.var()), 1e-6), 0.0]),
        np.array([average(residual), 1.0, max(float(residual.var()), 1e-6), 1.0]),
    ]
    baseline = independent_loss(p, m, v, y, case.rain) * case.scale
    solutions: list[Json] = []
    for index, start in enumerate(starts):
        result = minimize(
            independent_loss, start, args=(m, v, y, case.rain), method="SLSQP",
            bounds=((None, None), (0, None), (1e-6, None), (0, None)),
            options={"maxiter": 600, "ftol": 1e-12},
        )
        fitted = np.asarray(result.x, dtype=np.float64)
        a, b, c, d = (float(x) for x in fitted.flat)
        physical = np.array([case.shift + case.scale * a - b * case.shift,
                             b, case.scale**2 * c, d], dtype=np.float64)
        target_mu = float(physical.flat[0]) + b * average(case.forecast)
        target_sigma = math.sqrt(float(physical.flat[2]) + d * float(case.forecast.var(ddof=1)))
        target_mean = distribution_summary(
            target_mu, target_sigma, np.quantile(case.observed, [1 / 3, 2 / 3]), case.rain,
        )[0]
        original_mean = distribution_summary(
            float(case.row["MU"]), float(case.row["SIGMA"]),
            np.quantile(case.observed, [1 / 3, 2 / 3]), case.rain,
        )[0]
        fit = independent_loss(fitted, m, v, y, case.rain) * case.scale
        solutions.append({
            "start": index, "success": bool(result.success), "status": int(result.status),
            "message": str(result.message), "iterations": int(result.nit),
            "physical_parameters": [float(x) for x in physical.flat],
            "training_crps": fit, "improvement": baseline - fit,
            "relative_improvement": (baseline - fit) / max(baseline, 1e-12),
            "target_mu": target_mu, "target_sigma": target_sigma, "target_mean": target_mean,
            "target_mu_difference": target_mu - float(case.row["MU"]),
            "target_sigma_difference": target_sigma - float(case.row["SIGMA"]),
            "target_mean_difference": target_mean - original_mean,
            "scaled_gradient": [float(x) for x in objective(fitted, m, v, y, case.rain)[1].flat],
        })
    # A local curvature estimate is diagnostic, not an identification test.
    hessian = np.zeros((4, 4))
    for column in range(4):
        h = 1e-5 * max(1.0, abs(float(p.flat[column])))
        if column == 2:
            h = min(h, float(p.flat[column]) * 0.1)
        plus, minus = p.copy(), p.copy()
        plus[column] += h
        minus[column] -= h
        lower = 1e-6 if column == 2 else 0.0
        if column > 0 and float(minus.flat[column]) < lower:
            hessian[:, column] = (objective(plus, m, v, y, case.rain)[1]
                                  - objective(p, m, v, y, case.rain)[1]) / h
        else:
            hessian[:, column] = (objective(plus, m, v, y, case.rain)[1]
                                  - objective(minus, m, v, y, case.rain)[1]) / (2 * h)
    eigenvalues = np.linalg.eigvalsh((hessian + hessian.T) / 2)
    return {
        "case_id": case.row["CASE_ID"], "product": case.row["PRODUCT"],
        "variable": case.row["VARIABLE"], "n_train": case.observed.size,
        "baseline_parameters": [float(x) for x in case.parameters.flat],
        "baseline_training_crps": baseline,
        "design_condition": case.condition,
        "scaled_unconstrained_hessian_eigenvalues": [float(x) for x in eigenvalues.flat],
        "hessian_note": "One-sided differences at active bounds; curvature only, not confidence intervals.",
        "solutions": solutions,
    }


def run(root: Path) -> None:
    """Reconstruct all saved fits, then audit up to 32 training-selected cases."""
    started = time.perf_counter()
    if (np.__version__, scipy.__version__) != ("2.5.3", "1.18.1"):
        raise RuntimeError("Required exact .venv versions: numpy 2.5.3 / scipy 1.18.1")
    before = hashes(root)
    source = root / DATASET
    provenance = observation_provenance(source)
    daily = {day(row["DATE"]): parse_daily(row)
             for row in csv_rows(observation_daily_path(source))}
    variables = {row["CASE_ID"]: row["VARIABLE"]
                 for row in csv_rows(source / "cases/verification_cases.csv")}
    fits = list(csv_rows(root / "outputs/calibration_fits.csv"))
    ledger: dict[str, dict[int, float]] = defaultdict(dict)
    for row in csv_rows(root / "outputs/training_ledger.csv.gz"):
        if row["STATUS"] == "OK":
            observed, stations = observation_summary(
                daily, day(row["HIST_START"]), day(row["HIST_END"]),
                variables[row["CASE_ID"]] == "prcp",
            )
            if observed is None or abs(observed - float(row["OBS"])) > 1e-10 \
                    or stations != int(row["N_STATION_MIN"]):
                raise RuntimeError(f"Selected-source training observation mismatch: {row['CASE_ID']}")
            ledger[row["CASE_ID"]][int(row["SOURCE_YEAR"])] = float(row["OBS"])
    predictions = {
        row["CASE_ID"]: row for row in csv_rows(root / "outputs/matched_predictions.csv.gz")
        if row["METHOD"] == "EMOS"
    }
    for key, row in predictions.items():
        observed, stations = observation_summary(
            daily, day(row["VALID_START"]), day(row["VALID_END"]), variables[key] == "prcp",
        )
        if observed is None or abs(observed - float(row["OBS"])) > 1e-10 \
                or stations != int(row["N_STATION"]):
            raise RuntimeError(f"Selected-source target observation mismatch: {key}")
    diagnostics: list[dict[str, Json]] = []
    visited: set[str] = set()
    selected: list[Training] = []
    group_stats: dict[str, Json] = {}
    maxima: dict[str, tuple[float, str]] = {}
    latent_minima: dict[str, tuple[float, str]] = {}
    for product in ("1mon", "3mon"):
        for variable in ("t15m", "prcp"):
            forecasts = load_forecasts(source, product, variable)
            hindcasts = load_hindcasts(source, product, variable)
            cases: list[Training] = []
            counts: Counter[str] = Counter()
            member_counts: Counter[int] = Counter()
            forecast_counts: Counter[int] = Counter()
            n_train: Counter[int] = Counter()
            for row in fits:
                if (row["PRODUCT"], row["VARIABLE"]) != (product, variable):
                    continue
                key = row["CASE_ID"]
                years = [int(x) for x in row["SOURCE_YEARS"].split(";")]
                if set(years) != set(ledger[key]):
                    raise RuntimeError(f"Accepted SOURCE_YEAR mismatch: {key}")
                if len(years) != int(row["N_TRAIN"]):
                    raise RuntimeError(f"N_TRAIN mismatch: {key}")
                ensembles = tuple(hindcasts[key][year] for year in years)
                actual = np.array([ledger[key][year] for year in years], dtype=np.float64)
                m = np.array([average(x) for x in ensembles], dtype=np.float64)
                v = np.array([float(x.var(ddof=1)) for x in ensembles], dtype=np.float64)
                scale = max(float(actual.std()), 0.1 if variable == "prcp" else 1.0)
                shift = 0.0 if variable == "prcp" else average(actual)
                parameters = np.array([float(row[x]) for x in ("A", "B", "C", "D")], dtype=np.float64)
                forecast = forecasts[key].members
                design = np.column_stack((np.ones(m.size), (m - shift) / scale,
                                          v / scale**2))
                singular = np.linalg.svd(design, compute_uv=False)
                condition = float(singular.flat[0]) / float(singular.flat[-1])
                case = Training(row, m, v, actual, forecast, scale, shift, parameters, condition)
                p, sm, sv, sy = case.scaled()
                fit, grad = objective(parameters, m, v, actual, case.rain)
                independent = independent_loss(parameters, m, v, actual, case.rain)
                scaled_score, scaled_gradient = objective(p, sm, sv, sy, case.rain)
                target_mu = float(parameters.flat[0]) + float(parameters.flat[1]) * average(forecast)
                target_sigma = math.sqrt(float(parameters.flat[2])
                                         + float(parameters.flat[3]) * float(forecast.var(ddof=1)))
                thresholds = np.quantile(actual, [1 / 3, 2 / 3])
                mean, probs, quantiles = distribution_summary(target_mu, target_sigma,
                                                               thresholds, case.rain)
                oracle_cdf = ndtr((thresholds - target_mu) / target_sigma)
                oracle_probs = np.array([float(oracle_cdf.flat[0]),
                                         float(oracle_cdf.flat[1] - oracle_cdf.flat[0]),
                                         float(1 - oracle_cdf.flat[1])], dtype=np.float64)
                oracle_quantiles = target_mu + target_sigma * ndtri(np.array([0.05, 0.95]))
                if case.rain:
                    oracle_quantiles = np.maximum(oracle_quantiles, 0.0)
                stable_mean = positive_mean(target_mu, target_sigma) if case.rain else mean
                prediction = predictions[key]
                errors = {
                    "fit_crps_error": abs(fit - float(row["FIT_CRPS"])),
                    "independent_fit_error": abs(independent - float(row["FIT_CRPS"])),
                    "physical_rescaling_error": abs(fit - scaled_score * scale),
                    "target_mu_error": abs(target_mu - float(row["MU"])),
                    "target_sigma_error": abs(target_sigma - float(row["SIGMA"])),
                    "prediction_mean_error": abs(mean - float(prediction["PRED_MEAN"])),
                    "prediction_quantile_error": max(abs(float(quantiles.flat[i]) - float(prediction[x]))
                                                     for i, x in enumerate(("P05", "P95"))),
                    "prediction_probability_error": max(abs(float(probs.flat[i]) - float(prediction[x]))
                                                        for i, x in enumerate(("P_BN", "P_NN", "P_AN"))),
                    "independent_cdf_probability_error": max(abs(float(x)) for x in (probs - oracle_probs).flat),
                    "independent_quantile_error": max(abs(float(x)) for x in (quantiles - oracle_quantiles).flat),
                }
                errors["target_mean_oracle_absolute_error"] = abs(mean - stable_mean)
                projected = scaled_gradient.copy()
                for i, lower in ((1, 0.0), (2, 1e-6), (3, 0.0)):
                    if float(p.flat[i]) <= lower + 1e-9 and float(projected.flat[i]) > 0:
                        projected[i] = 0
                errors["scaled_projected_gradient_max"] = max(abs(float(x)) for x in projected.flat)
                for label, magnitude in errors.items():
                    if label not in maxima or magnitude > maxima[label][0]:
                        maxima[label] = (magnitude, key)
                latent_z = target_mu / target_sigma
                if variable not in latent_minima or latent_z < latent_minima[variable][0]:
                    latent_minima[variable] = (latent_z, key)
                training_mu = float(parameters.flat[0]) + float(parameters.flat[1]) * m
                training_sigma = np.sqrt(float(parameters.flat[2]) + float(parameters.flat[3]) * v)
                training_scores = gaussian_crps(training_mu, training_sigma, actual, case.rain)
                counts["negative_individual_training_crps"] += int(np.count_nonzero(training_scores < 0))
                mean_extrapolation = average(forecast) < float(m.min()) or average(forecast) > float(m.max())
                spread_extrapolation = (float(forecast.var(ddof=1)) < float(v.min())
                                        or float(forecast.var(ddof=1)) > float(v.max()))
                for name, active in (
                    ("b_zero", float(parameters.flat[1]) <= 1e-9),
                    ("d_zero", float(parameters.flat[3]) <= 1e-9),
                    ("c_scaled_floor", float(p.flat[2]) <= 1.00001e-6),
                    ("target_mean_extrapolation", mean_extrapolation),
                    ("target_variance_extrapolation", spread_extrapolation),
                    ("negative_latent_target_mu", target_mu < 0),
                    ("negative_training_crps", fit < 0),
                    ("invalid_predictive_probabilities", bool(np.any(probs < 0)) or abs(average(probs) * 3 - 1) > 1e-12),
                    ("invalid_rain_support", case.rain and (mean < 0 or bool(np.any(quantiles < 0)))),
                    ("recorded_converged", row["CONVERGED"] == "1"),
                    ("fit_le_initial", fit <= float(row["INITIAL_CRPS"]) + 1e-10),
                ):
                    counts[name] += int(active)
                member_counts.update(x.size for x in ensembles)
                forecast_counts.update([forecast.size])
                n_train.update([actual.size])
                diagnostics.append({
                    "case_id": key, "product": product, "variable": variable,
                    "scale": scale, "scaled_c": float(p.flat[2]), "n_train": actual.size,
                    "n_forecast": forecast.size, "b": float(parameters.flat[1]), "d": float(parameters.flat[3]),
                    "target_latent_z": latent_z,
                    "training_min_latent_z": min(float(x) for x in (training_mu / training_sigma).flat),
                    "target_mean_stable_oracle": stable_mean,
                    "target_mean_oracle_absolute_error": abs(mean - stable_mean),
                    "design_condition": condition,
                    "scaled_projected_gradient_max": max(abs(float(x)) for x in projected.flat),
                    "physical_gradient": [float(x) for x in grad.flat],
                    "target_mean_extrapolation": mean_extrapolation,
                    "target_variance_extrapolation": spread_extrapolation,
                    **errors,
                })
                cases.append(case)
                visited.add(key)
            selected.extend(selection(cases))
            group_stats[f"{product}/{variable}"] = {
                "count": len(cases), "counts": dict(counts),
                "annual_hindcast_member_counts": {str(k): v for k, v in member_counts.items()},
                "forecast_member_counts": {str(k): v for k, v in forecast_counts.items()},
                "training_year_counts": {str(k): v for k, v in n_train.items()},
            }
            print(f"RECONSTRUCTED {product}/{variable}: {len(cases)}", flush=True)
    if len(diagnostics) != len(fits) or visited != {
        row["CASE_ID"] for row in fits
    }:
        raise RuntimeError("Audit did not visit every saved fit")
    checks = numerical_checks()
    comparisons: list[Json] = []
    for index, case in enumerate(selected, 1):
        comparison = sensitivity(case)
        comparisons.append(comparison)
        print(f"SENSITIVITY {index}/{len(selected)} {case.row['CASE_ID']}", flush=True)
    # Execute the actual fit surface once for each family and compare altered
    # forecast inputs: training parameters must not depend on target ensemble.
    independence: list[Json] = []
    for rain in (False, True):
        actual = np.array([0.0, 0.6, 1.7, 2.3, 1.1, 0.4]) if rain else np.arange(6.0)
        historical = tuple(np.array([x - 0.1, x + 0.1, x + 0.2]) for x in (actual + 0.2).flat)
        one = calibrate(np.array([1.0, 2.0, 3.0]), historical, actual, rain)
        two = calibrate(np.array([10.0, 20.0, 30.0]), historical, actual, rain)
        independence.append({
            "rain": rain, "parameter_max_difference": max(abs(a - b) for a, b in
                                                         zip(one.parameters, two.parameters, strict=True)),
            "fit_crps_difference": abs(one.fit_crps - two.fit_crps),
            "heldout_observation_argument": False,
            "note": "calibrate signature has no heldout observation; forecast alteration changes only issued distribution/QM/QDM.",
        })
    after = hashes(root)
    report: dict[str, Json] = {
        "observation_source": provenance,
        "fits_audited": len(diagnostics), "saved_fits": len(fits),
        "observation_policy_scope": "Selected-source outputs: daily station count >=50; " +
                                    "use actual-n daily means, including 61/60; " +
                                    "no 62/n scaling or raw-station imputation. " +
                                    "Policy/calendar validation is a separate training audit.",
        "versions": {"numpy": np.__version__, "scipy": scipy.__version__},
        "reproduce": ".venv/Scripts/python.exe analysis/audit_emos.py",
        "source_hashes_before": {k: v for k, v in before.items()},
        "source_hashes_after": {k: v for k, v in after.items()},
        "source_hashes_unchanged": before == after,
        "source_hash_scope": "All extracted package files; four original implementation modules; fit/ledger/member/prediction outputs.",
        "method_references": {
            "loss_and_gradient": "analysis/calibration.py:57-89,105-129",
            "annual_weights_and_ddof": "analysis/calibration.py:156-158,183-184",
            "scale_bounds_starts_and_units": "analysis/calibration.py:180-231",
            "predictive_summary": "analysis/scoring.py:73-92",
            "historical_only_eligibility": "analysis/run_verification.py:84-114",
            "raw_value_units": "analysis/data_io.py:195-243; use VALUE, not RAW_ANOM; observations Celsius means/rain totals at 163-166",
        },
        "rescaling_algebra": "A=shift+scale*a-b*shift; B=b; C=scale^2*c; D=d. CRPS scales linearly; c_floor physical=1e-6*scale^2. No rescaling defect.",
        "all_fit_maxima": {
            label: {"magnitude": magnitude, "case_id": key}
            for label, (magnitude, key) in maxima.items()
        },
        "minimum_predictive_latent_z": {
            variable: {"z": z, "case_id": key}
            for variable, (z, key) in latent_minima.items()
        },
        "groups": group_stats, "all_fit_diagnostics": [entry for entry in diagnostics],
        "numerical": checks, "independence": independence,
        "selection": {
            "cap": 32, "per_group": 8,
            "rule": selection.__doc__,
            "target_scores_read_for_selection": False,
            "case_ids": [case.row["CASE_ID"] for case in selected],
        },
        "sensitivity": comparisons,
        "interpretation": [
            "Recorded convergence and fit<=initial do not prove global optimum or identification.",
            "SLSQP is bounded local optimization with independent loss and numerical derivatives; every failure retained.",
            "Better training objective is not evidence of better heldout skill; any skill effect requires full historical-only rerun of predictions and metrics.",
            "Annual observations constrain four parameters; current training-year counts are reported per group. Bounds, weak curvature and extrapolation are statistical risks, not automatically coding defects.",
            "Historical and issued forecast member counts are reported per group. Small historical ensembles yield noisy sample variances; ddof=1 is unbiased but does not remove sampling/regime mismatch.",
            "Tail arithmetic defects should be assessed against real-case occurrence; synthetic extreme failures alone do not invalidate existing metrics.",
        ],
        "minimal_suggestions": [
            "Use erfc/ndtr rather than NormalDist.cdf for extreme negative latent rainfall means.",
            "Use positive-support stable CRPS or tail-aware formulas rather than subtracting nearly equal Gaussian terms.",
            "Record projected gradient/active bounds and compare additional deterministic starts; never assert global optimality.",
            "Assess temporal dependence, small-sample parameter uncertainty and historical/forecast variance transfer separately from optimizer convergence.",
        ],
        "elapsed_seconds": time.perf_counter() - started,
    }
    destination = root / "outputs/method_review/emos_audit.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    if before != after:
        raise RuntimeError("Original input hashes changed during audit")
    print(f"AUDIT_DONE fits={len(diagnostics)} sensitivity={len(comparisons)} output={destination}", flush=True)


def main() -> None:
    """Bounded reproducible default command; unknown flags are errors."""
    if sys.argv[1:] == ["--help"]:
        print("Usage: .venv/Scripts/python.exe analysis/audit_emos.py\n" +
              "Audit all saved EMOS fits and up to 32 training-selected SLSQP cases; " +
              "write outputs/method_review/emos_audit.json only.")
        return
    if sys.argv[1:]:
        raise SystemExit("Unexpected arguments; use --help")
    run(Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    main()
