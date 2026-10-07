"""BMA component numerical failure remains a failure, not a data-fold gate."""

from __future__ import annotations

import json
from dataclasses import replace
from time import perf_counter
from unittest.mock import patch

from analysis.alternative_classical import fit_classical
from analysis.alternative_classical_audit import method
from analysis.alternative_classical_mixture_audit import synthetic_training
from analysis.alternative_contracts import (
    FitConfig,
    FitDiagnostics,
    FitResult,
    FitStatus,
    MethodSpec,
    TrainingSet,
)


def numerical_failure(spec: MethodSpec, training: TrainingSet,
                      config: FitConfig) -> FitResult:
    """Preserve the external component's actual typed failure boundary."""
    del config
    return FitResult(method_id=spec.id, status=FitStatus.POSTERIOR_DIAGNOSTICS_FAILED,
                     fitted_model=None, reason_code="POSTERIOR_DIAGNOSTICS_FAILED",
                     diagnostics=FitDiagnostics(
                         n_rows=len(training.rows),
                         n_years=len({row.source_year for row in training.rows}),
                         train_hash=training.train_hash,
                         message="mean_mcse=0.046725143353949575; bound=0.021007016360461664"))


def main() -> None:
    started = perf_counter()
    training = synthetic_training(True)
    spec = replace(method("bma_component_pool"), family_no=8)
    with patch("analysis.alternative_bayes.fit_bayes", side_effect=numerical_failure):
        fitted = fit_classical(spec, training, FitConfig(workers=1))
    assert fitted.status == FitStatus.POSTERIOR_DIAGNOSTICS_FAILED
    assert fitted.fitted_model is None and not fitted.diagnostics.convergence
    assert fitted.reason_code == "PREQUENTIAL_COMPONENT_FAILED"
    metadata = fitted.diagnostics.posterior_diagnostics
    available, failures, common = (metadata[name] for name in (
        "eligible_prequential_years", "fold_failures", "common_prequential_years"))
    assert isinstance(available, list) and len(available) == 14
    assert isinstance(failures, list) and len(failures) == 14
    assert common == []
    short = synthetic_training(True, 17)
    insufficient = fit_classical(method("cdf_mix_cv"), short, FitConfig(workers=1))
    assert insufficient.status == FitStatus.INSUFFICIENT_INNER_FOLDS
    assert insufficient.fitted_model is None
    print(json.dumps({"component_failure_status": str(fitted.status),
                      "eligible_years": len(available), "failed_folds": len(failures),
                      "data_insufficient_status": str(insufficient.status),
                      "seconds": perf_counter()-started}, indent=2))


if __name__ == "__main__":
    main()
