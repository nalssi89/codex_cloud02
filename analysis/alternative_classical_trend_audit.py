"""Standalone trend regression audit, independent of the pooled duplicate-fit check."""

from __future__ import annotations

import json
from time import perf_counter

import numpy as np

from analysis.alternative_classical_pooled_audit_gradient import (
    synthetic_spec,
    synthetic_training,
)
from analysis.alternative_classical_trend import IDS, TrendModel, fit_trend
from analysis.alternative_classical_trend_audit_math import (
    audit_mapping,
    audit_restoration,
)
from analysis.alternative_contracts import FitConfig, FitStatus


def main() -> None:
    """Exercise temperature/rain trends, boundaries, future years and original maps."""
    started = perf_counter()
    evidence: list[dict[str, object]] = []
    for rain in (False, True):
        training = synthetic_training(rain, pooled=False)
        for method_id in IDS:
            result = fit_trend(synthetic_spec(method_id, pooled=False), training, FitConfig(workers=1))
            assert result.status == FitStatus.OK, result.diagnostics
            model = result.fitted_model
            assert isinstance(model, TrendModel) and result.diagnostics.convergence
            audit_restoration(model, training, result.diagnostics.objective)
            audit_mapping(model, training)
            law = model.predict(training.target)
            assert np.isfinite(law.mean()) and np.isfinite(law.crps(5.))
            _ = json.dumps(model.to_spec(), allow_nan=False)
            _ = json.dumps(law.to_spec(), allow_nan=False)
            evidence.append({"method": method_id, "rain": rain, "status": str(result.status),
                             "mean": law.mean(), "crps": law.crps(5.)})
    print(json.dumps({"fits": evidence, "checks": "variable censor boundaries, future trend "
                     + "restoration and original QM/QDM mapping parity",
                     "elapsed_seconds": perf_counter()-started}, indent=2))


if __name__ == "__main__":
    main()
