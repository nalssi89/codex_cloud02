"""Original-unit categorical loss and tied-threshold contract."""

import numpy as np

from analysis.alternative_validation_oracles import close
from analysis.calibration import FloatArray


def category_score(row: dict[str, str]) -> None:
    probabilities: FloatArray = np.array(
        [float(row[f"P_{label}"]) for label in ("BN", "NN", "AN")], dtype=np.float64)
    if not np.all(np.isfinite(probabilities)) or np.any(probabilities < 0) or np.any(probabilities > 1):
        raise AssertionError("invalid category probabilities")
    close(float(probabilities.sum()), 1, "category total mass", atol=1e-10)
    observation, low, high = float(row["OBS"]), float(row["Q33"]), float(row["Q67"])
    if low > high:
        raise AssertionError("crossed category thresholds")
    if low == high:
        close(float(probabilities.take(1)), 0, "tied thresholds empty middle", atol=1e-12)
    category = int(observation > low)+int(observation > high)
    event = np.array([float(i == category) for i in range(3)], dtype=np.float64)
    close(float(row["BRIER"]), float(np.sum((probabilities-event)**2)), "Brier sum")
    close(float(row["RPS"]), float(np.sum((
        np.cumsum(probabilities)[:2]-np.cumsum(event)[:2])**2)), "RPS")
