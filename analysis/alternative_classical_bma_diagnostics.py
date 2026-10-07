"""Single strict rain-BMA component fold diagnostic, retaining actual failures."""

from __future__ import annotations

import json
from dataclasses import replace
from time import perf_counter

from analysis.alternative_bayes import fit_bayes
from analysis.alternative_classical_audit import method
from analysis.alternative_classical_mixture_audit import synthetic_training
from analysis.alternative_contracts import FitConfig
from analysis.alternative_data import fold_training, inner_folds


def main() -> None:
    started = perf_counter()
    training = synthetic_training(True)
    folds = inner_folds(training, training.target, min_years=10, last_n=None)
    assert len(folds) == 14
    fold = folds[0]
    ancestor = fold_training(training, fold)
    spec = replace(method("bjp_sqrt_censored"), family_no=1, owner="bayes")
    fitted = fit_bayes(spec, ancestor, FitConfig(workers=1))
    print(json.dumps({"fold_id": fold.fold_id, "source_years": [row.source_year
                                                              for row in ancestor.rows],
                      "status": str(fitted.status), "reason": fitted.reason_code,
                      "message": fitted.diagnostics.message,
                      "posterior_diagnostics": dict(fitted.diagnostics.posterior_diagnostics),
                      "seconds": perf_counter()-started}, indent=2, allow_nan=False), flush=True)


if __name__ == "__main__":
    main()
