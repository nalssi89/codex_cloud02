"""Read-only all-ID classical smoke on real archive and active observations."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from time import perf_counter

import numpy as np

from analysis.alternative_classical import CLASSICAL_IDS, fit_classical
from analysis.alternative_classical_audit import method
from analysis.alternative_classical_serialization import restore_distribution
from analysis.alternative_contracts import CaseInput, FitConfig, FitStatus
from analysis.alternative_data import load_experiment, training_for
from analysis.data_io import Json


def protected(root: Path, parse: Callable[[str], Json] = json.loads) -> int:
    """Check bytes and SHA256, never mutate any protected input."""
    receipt = parse(
        (root / ".omo/evidence/alternative-baseline-hashes.json").read_text(encoding="utf-8"))
    if not isinstance(receipt, dict):
        raise TypeError("Invalid baseline receipt")
    files = receipt["files"]
    if not isinstance(files, dict):
        raise TypeError("Invalid baseline file table")
    for name, expected in files.items():
        if not isinstance(expected, dict):
            raise TypeError("Invalid baseline file entry")
        path = root / name
        assert path.stat().st_size == expected["bytes"], name
        with path.open("rb") as handle:
            assert hashlib.file_digest(handle, "sha256").hexdigest() == expected["sha256"], name
    assert len(files) == 60
    return len(files)


def main() -> None:
    started = perf_counter()
    root = Path.cwd()
    before = protected(root)
    inputs = load_experiment(root)
    chosen: dict[tuple[str, str], CaseInput] = {}
    # Rain all-wet chooses a support-valid positive-Gamma/BJP-conjugate smoke,
    # not a skill-selected outcome. Mixed-zero behavior has separate checks.
    for target in inputs.cases:
        key = (target.product, target.variable)
        if key in chosen or target.case_id not in inputs.truths:
            continue
        training = training_for(target, inputs, "local")
        if target.variable == "prcp" and np.any(training.local_observations <= 0):
            continue
        chosen[key] = target
        if len(chosen) == 4:
            break
    assert len(chosen) == 4
    config = FitConfig(workers=1)
    records: list[dict[str, object]] = []
    successes: set[str] = set()
    for target in chosen.values():
        local = training_for(target, inputs, "local")
        pooled = training_for(target, inputs, "pooled")
        for name in CLASSICAL_IDS:
            training = pooled if name.startswith("pooled_") else local
            fitted = fit_classical(method(name), training, config)
            record: dict[str, object] = {
                "case_id": target.case_id, "product": target.product, "variable": target.variable,
                "id": name, "status": str(fitted.status), "reason": fitted.reason_code,
                "message": fitted.diagnostics.message, "seconds": fitted.diagnostics.elapsed_seconds,
                "rows": fitted.diagnostics.n_rows, "years": fitted.diagnostics.n_years,
                "train_hash": fitted.diagnostics.train_hash,
            }
            if fitted.status == FitStatus.OK:
                assert fitted.fitted_model is not None and fitted.diagnostics.convergence
                law = fitted.fitted_model.predict(target)
                restored = restore_distribution(law.to_spec())
                q = law.quantile(np.array([.05, .5, .95]))
                np.testing.assert_allclose(restored.quantile(np.array([.05, .5, .95])), q,
                                           atol=1e-8, rtol=1e-8)
                assert np.all(np.diff(q) >= 0) and np.isfinite(law.mean())
                assert target.variable != "prcp" or q.min() >= 0
                truth = inputs.truths[target.case_id]
                score = law.crps(truth.observation)
                assert np.isfinite(score) and score >= 0
                np.testing.assert_allclose(restored.mean(), law.mean(), atol=1e-8, rtol=1e-10)
                np.testing.assert_allclose(restored.crps(truth.observation), score,
                                           atol=1e-8, rtol=1e-9)
                record.update(mean=law.mean(), crps=score, atom=law.atom_mass(0),
                              log_density_at_truth=law.log_density(truth.observation))
                successes.add(name)
            else:
                assert fitted.fitted_model is None
            records.append(record)
            print(f"{target.case_id} {name} {fitted.status} " +
                  f"{fitted.diagnostics.elapsed_seconds:.3f}s {fitted.reason_code}", flush=True)
    after = protected(root)
    expected = set(CLASSICAL_IDS) - {"bma_group_normal", "bma_group_rain"}
    assert successes == expected, sorted(expected - successes)
    print(json.dumps({"scope": "SMOKE", "records": len(records),
                      "method_ids": len(CLASSICAL_IDS), "successful_ids": sorted(successes),
                      "status_counts": dict(Counter(str(record["status"]) for record in records)),
                      "cases": [target.case_id for target in chosen.values()],
                      "protected_before": before, "protected_after": after,
                      "seconds": perf_counter() - started}, indent=2), flush=True)


if __name__ == "__main__":
    main()
