"""Exact replication/permutation invariance and conflicting-row boundary audit."""

from __future__ import annotations

import json
from dataclasses import replace
from time import perf_counter

import numpy as np

from analysis.alternative_classical_pooled import IDS, PooledModel, fit_pooled
from analysis.alternative_classical_pooled_audit_gradient import (
    synthetic_spec,
    synthetic_training,
)
from analysis.alternative_contracts import FitConfig, FitStatus


def main() -> None:
    started = perf_counter()
    records: list[dict[str, object]] = []
    config = FitConfig(workers=1)
    for rain in (False, True):
        original = synthetic_training(rain, True)
        duplicated = replace(original, rows=original.rows*2,
                             year_weights=np.tile(original.year_weights/2, 2))
        permuted = replace(duplicated, rows=duplicated.rows[::-1],
                           year_weights=duplicated.year_weights[::-1])
        for name in IDS:
            spec = synthetic_spec(name, True)
            fits = tuple(fit_pooled(spec, training, config)
                         for training in (original, duplicated, permuted))
            models = tuple(fit.fitted_model for fit in fits)
            assert all(fit.status == FitStatus.OK for fit in fits)
            assert all(isinstance(model, PooledModel) for model in models)
            arrays = [model.parameters for model in models if isinstance(model, PooledModel)]
            for parameters in arrays[1:]:
                np.testing.assert_array_equal(parameters, arrays[0])
            quantiles = [model.predict(original.target).quantile(np.array([.05, .5, .95]))
                         for model in models if model is not None]
            for q in quantiles[1:]:
                np.testing.assert_array_equal(q, quantiles[0])
            records.append({"method": name, "rain": rain,
                            "original_quantiles": quantiles[0].tolist(),
                            "replicated_quantiles": quantiles[1].tolist(),
                            "max_delta": max(abs(quantiles[0].item(i)-quantiles[1].item(i))
                                             for i in range(3))})
        inconsistent = replace(duplicated, rows=duplicated.rows[:-1] + (
            replace(duplicated.rows[-1], observation=duplicated.rows[-1].observation+1),))
        failure = fit_pooled(synthetic_spec(IDS[2], True), inconsistent, config)
        assert failure.status == FitStatus.INPUT_CONFLICT and failure.fitted_model is None
    print(json.dumps({"replication_and_permutation": records,
                      "contradictory_replica": "INPUT_CONFLICT",
                      "seconds": perf_counter() - started}, indent=2))


if __name__ == "__main__":
    main()
