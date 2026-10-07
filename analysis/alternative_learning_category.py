"""Past-only ordinal and monotone threshold category regression."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log1p
from sys import float_info
from time import perf_counter

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    CategoryPrediction,
    FeatureSpec,
    FitDiagnostics,
    TrainingRow,
    TrainingSet,
)
from analysis.calibration import FloatArray
from analysis.data_io import Json


def _softplus(value: float) -> float:
    return max(value, 0.) + log1p(exp(-abs(value)))


def historical_labels(
    training: TrainingSet,
) -> tuple[tuple[int, ...], FloatArray, FloatArray, tuple[tuple[str, ...], ...]]:
    """One condition's annual climate is recomputed at each pseudo-issuance.

    The catalog remains frozen at the actual outer issuance. Its 2022-vintage
    reforecasts are not discarded at a historical pseudo-issuance.
    """
    indices: list[int] = []
    responses: list[float] = []
    cuts: list[list[float]] = []
    ancestry: list[tuple[str, ...]] = []
    conditions: dict[tuple[str, str], list[TrainingRow]] = {}
    for row in training.rows:
        conditions.setdefault((row.source_case_id, row.lead), []).append(row)
    for index, row in enumerate(training.rows):
        valid_years = tuple(range(row.hist_start.year, row.hist_end.year + 1))
        held_out_source = {row.source_year, *valid_years}
        history = tuple(
            candidate for candidate in conditions[(row.source_case_id, row.lead)]
            if candidate.hist_end < row.source_init
            and candidate.source_year not in held_out_source
            and not any(candidate.hist_start.year <= year <= candidate.hist_end.year for year in valid_years)
            and candidate.source_case_init <= training.catalog_cutoff
        )
        if len({item.source_year for item in history}) < 10:
            continue
        thresholds = np.quantile(
            np.array([item.observation for item in history]), [1 / 3, 2 / 3],
        )
        indices.append(index)
        responses.append(row.observation)
        cuts.append([thresholds.item(0), thresholds.item(1)])
        ancestry.append(tuple(item.row_id for item in history))
    return (
        tuple(indices), np.array(responses), np.array(cuts).reshape(-1, 2),
        tuple(ancestry),
    )


def ordinal_probabilities(parameters: FloatArray, x: FloatArray) -> FloatArray:
    eta = x @ parameters[2:]
    first = expit(parameters.item(0) - eta)
    second = expit(parameters.item(0) + _softplus(parameters.item(1)) - eta)
    return np.column_stack((first, second - first, 1 - second))


@dataclass(frozen=True, slots=True)
class CategoryRegression:
    method_id: str
    feature_spec: FeatureSpec
    coefficients: FloatArray
    binary_coefficients: FloatArray
    threshold_center: float
    threshold_scale: float
    train_hash: str
    label_row_ids: tuple[str, ...]
    label_ancestors: tuple[tuple[str, ...], ...]

    def predict(
        self, target: CaseInput, thresholds: FloatArray,
    ) -> CategoryPrediction:
        from analysis.alternative_data import features_for_case

        x = features_for_case(target, self.feature_spec).reshape(1, -1)
        if self.method_id == "elr_threshold_logit":
            t = (thresholds - self.threshold_center) / self.threshold_scale
            c = self.coefficients
            cumulative = expit(c.item(0) + _softplus(c.item(1)) * t + (x.ravel() @ c[2:]).item())
            probabilities = np.array(
                [cumulative.item(0), cumulative.item(1) - cumulative.item(0), 1 - cumulative.item(1)],
            )
        elif thresholds[0] == thresholds[1]:
            p = expit(self.binary_coefficients.item(0) - (x.ravel() @ self.binary_coefficients[1:]).item())
            probabilities = np.array([p, 0.0, 1 - p])
        else:
            probabilities = ordinal_probabilities(self.coefficients, x)[:1].reshape(-1)
        return CategoryPrediction(
            case_id=target.case_id, method_id=self.method_id,
            thresholds=thresholds.copy(), probabilities=probabilities,
            fit_ref=self.train_hash,
        )

    def to_spec(self) -> dict[str, Json]:
        return {
            "kind": self.method_id,
            "coefficients": self.coefficients.tolist(),
            "binary_coefficients": self.binary_coefficients.tolist(),
            "threshold_center": self.threshold_center,
            "threshold_scale": self.threshold_scale,
            "feature_names": list(self.feature_spec.names),
            "feature_center": self.feature_spec.center.tolist(),
            "feature_scale": self.feature_spec.scale.tolist(),
            "predictor_power": self.feature_spec.predictor_power,
            "train_hash": self.train_hash,
            "label_rows": list(self.label_row_ids),
            "label_ancestors": [list(ids) for ids in self.label_ancestors],
            "catalog_semantics": "outer-frozen reforecast catalog; past responses",
        }


def fit_category(
    method_id: str, training: TrainingSet,
) -> tuple[CategoryRegression, FitDiagnostics]:
    start = perf_counter()
    from analysis.alternative_data import features_for_training

    full_x, feature_spec = features_for_training(training)
    selected, y, thresholds, ancestors = historical_labels(training)
    if not len(selected):
        raise AlternativeError("INSUFFICIENT_TRAINING", "No row has ten own-past years")
    indices = selected
    x = np.take(full_x, np.array(indices, dtype=np.int64), axis=0)
    years = tuple(training.rows[i].source_year for i in indices)
    counts = {year: years.count(year) for year in set(years)}
    weights = np.array([1 / counts[year] for year in years], dtype=np.float64)
    labels = np.greater(y, thresholds[:, 0]).astype(np.int64) + np.greater(y, thresholds[:, 1]).astype(np.int64)
    tied = np.equal(thresholds[:, 0], thresholds[:, 1])
    center = float(np.mean(training.local_observations))
    scale = max(float(np.std(training.local_observations)), 1e-6)
    standardized = (thresholds - center) / scale

    def objective(parameters: FloatArray) -> float:
        if method_id == "elr_threshold_logit":
            logits = (
                parameters.item(0) + _softplus(parameters.item(1)) * standardized
                + (x @ parameters[2:])[:, None]
            )
            outcome = np.less_equal(y[:, None], thresholds).astype(np.float64)
            loss = np.logaddexp(0, logits) - outcome * logits
            penalty = (
                .5 * np.sum(parameters[2:] ** 2).item()
                + .125 * parameters.item(0) ** 2 + .5 * parameters.item(1) ** 2
            )
            return float(np.sum(weights[:, None] * loss) / 2 + penalty)
        probabilities = ordinal_probabilities(parameters, x)
        # Collapsed training strata use a binary cut, never a middle category.
        first = expit(parameters.item(0) - x @ parameters[2:])
        chosen = np.asarray(
            np.take_along_axis(probabilities, labels[:, None], axis=1).ravel(),
            dtype=np.float64,
        )
        chosen = np.asarray(
            np.where(tied, np.where(np.less_equal(y, thresholds[:, 0]), first, 1 - first), chosen),
            dtype=np.float64,
        )
        k2 = parameters.item(0) + _softplus(parameters.item(1))
        return float(
            -np.sum(weights * np.log(np.maximum(chosen, float_info.min))).item()
            + .5 * np.sum(parameters[2:] ** 2).item()
            + .125 * (parameters.item(0) ** 2 + k2 ** 2)
        )

    initial = np.zeros(np.size(x, 1) + 2)
    initial[0] = -.7 if method_id == "ordinal_logit" else 0
    solution = minimize(
        objective, initial, method="L-BFGS-B",
        options={"maxiter": 500, "ftol": 1e-10, "gtol": 1e-6},
    )
    if not solution.success or not np.isfinite(solution.fun):
        raise AlternativeError("FIT_FAILED", str(solution.message))
    binary = np.zeros(np.size(x, 1) + 1)
    if method_id == "ordinal_logit":
        def binary_loss(parameters: FloatArray) -> float:
            z = parameters.item(0) - x @ parameters[1:]
            outcome = np.less_equal(y, thresholds[:, 0]).astype(np.float64)
            return float(
                np.sum(weights * (np.logaddexp(0, z) - outcome * z)).item()
                + .5 * np.sum(parameters[1:] ** 2).item() + .125 * parameters.item(0) ** 2
            )
        binary_solution = minimize(
            binary_loss, binary, method="L-BFGS-B",
            options={"maxiter": 500, "ftol": 1e-10, "gtol": 1e-6},
        )
        if not binary_solution.success:
            raise AlternativeError("FIT_FAILED", str(binary_solution.message))
        binary = np.asarray(binary_solution.x, dtype=np.float64)
    model = CategoryRegression(
        method_id, feature_spec, np.asarray(solution.x, dtype=np.float64), binary,
        center, scale, training.train_hash,
        tuple(training.rows[i].row_id for i in indices), ancestors,
    )
    return model, FitDiagnostics(
        objective=float(solution.fun), convergence=True,
        n_rows=len(training.rows), n_years=len({r.source_year for r in training.rows}),
        train_hash=training.train_hash,
        parameter_count=len(initial) + (len(binary) if method_id == "ordinal_logit" else 0),
        elapsed_seconds=perf_counter() - start,
        message=f"Own-past labels={len(indices)} rows/{len(set(years))} years; early rows omitted; year-balanced loss",
    )
