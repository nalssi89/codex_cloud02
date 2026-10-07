"""Original-law and category scoring, and dimension-matched weighted joint scores."""

from __future__ import annotations

from itertools import combinations

import numpy as np

from analysis.alternative_contracts import (
    CaseInput,
    CategoryPrediction,
    ContinuousPrediction,
    JointPrediction,
)
from analysis.alternative_experiment_types import JointTruth, ScoreTruth
from analysis.alternative_runner_io import Row, dumps
from analysis.scoring import probability_scores, score_prediction


def identity(target: CaseInput, method: str, fit_ref: str, n_train: int) -> Row:
    return {
        "case_id": target.case_id, "method_id": method, "variable": target.variable,
        "fit_ref": fit_ref, "CASE_ID": target.case_id, "METHOD": method,
        "VARIABLE": target.variable, "PRODUCT": target.product, "LEAD": target.lead,
        "INIT_DATE": target.init.isoformat(), "VALID_START": target.valid_start.isoformat(),
        "VALID_END": target.valid_end.isoformat(), "N_TRAIN": n_train,
        "YEAR": target.valid_start.year, "VALID_MONTH": target.valid_start.month,
        "SEASON": ("DJF", "MAM", "JJA", "SON")[(target.valid_start.month % 12) // 3],
        "N_MEMBERS": len(target.members),
    }


def score_continuous(prediction: ContinuousPrediction, truth: ScoreTruth) -> Row:
    law = prediction.distribution
    cumulative = law.cdf(truth.thresholds)
    probabilities = np.asarray([cumulative.item(0),
                                cumulative.item(1) - cumulative.item(0),
                                1 - cumulative.item(1)])
    mean, crps = law.mean(), law.crps(truth.observation)
    quantiles = law.quantile(np.array([0.05, 0.95]))
    if (not np.isfinite([mean, crps, *probabilities, *quantiles]).all()
            or crps < -1e-8 or np.any(probabilities < -1e-10)
            or abs(float(probabilities.sum()) - 1) > 1e-9):
        raise ValueError("Invalid original-unit predictive mean/CRPS/probability/interval")
    return dict(score_prediction(mean, crps, probabilities, quantiles, truth.observation,
                                 truth.historical_observations, truth.thresholds))


def score_categories(prediction: CategoryPrediction, truth: ScoreTruth) -> Row:
    probabilities = prediction.probabilities
    if (probabilities.shape != (3,) or not np.isfinite(probabilities).all()
            or np.any(probabilities < 0) or abs(float(probabilities.sum()) - 1) > 1e-9):
        raise ValueError("Invalid category predictive mass")
    if truth.thresholds.item(0) == truth.thresholds.item(1) and probabilities.item(1) != 0:
        raise ValueError("Coincident thresholds have nonzero middle mass")
    category = int(truth.observation > truth.thresholds.item(0)) + int(
        truth.observation > truth.thresholds.item(1))
    event = np.asarray([float(i == category) for i in range(3)])
    brier, rps = probability_scores(probabilities, event)
    return {
        "OBS": truth.observation, "Q33": truth.thresholds.item(0),
        "Q67": truth.thresholds.item(1), "P_BN": probabilities.item(0),
        "P_NN": probabilities.item(1), "P_AN": probabilities.item(2),
        "BRIER": brier, "RPS": rps,
        "EVENT_BN": event.item(0), "EVENT_NN": event.item(1), "EVENT_AN": event.item(2),
    }


def score_joint(prediction: JointPrediction, truth: JointTruth) -> Row:
    x = (prediction.samples - truth.centers) / truth.scales
    y = (truth.observations - truth.centers) / truth.scales
    w = prediction.weights
    if (x.ndim != 2 or x.shape[1:] != y.shape or len(w) != len(x)
            or not np.isfinite(x).all() or np.any(w < 0)
            or abs(float(w.sum()) - 1) > 1e-9):
        raise ValueError("Invalid weighted joint predictive law")
    energy = float(w @ np.linalg.norm(x - y, axis=1))
    # Row chunks avoid the N x N x dimension allocation for high-dimensional paths.
    pair_term = 0.0
    for start in range(0, len(x), 64):
        distances = np.linalg.norm(x[start:start + 64, None, :] - x[None, :, :], axis=2)
        pair_term += float(w[start:start + 64] @ distances @ w)
    pairs = tuple(combinations(range(int(np.size(x, axis=1))), 2))
    variogram = sum(
        (np.sqrt(abs(y.item(i) - y.item(j))) -
         float(w @ np.sqrt(np.abs(x[:, i] - x[:, j])))) ** 2
        for i, j in pairs
    ) / len(pairs)
    return {
        "ENERGY": energy - pair_term / 2, "VARIOGRAM": float(variogram),
        "observations": dumps(truth.observations), "centers": dumps(truth.centers),
        "scales": dumps(truth.scales), "thresholds": dumps(truth.thresholds),
        "HOT_DRY_P": None, "HOT_DRY_BRIER": None,
    }
