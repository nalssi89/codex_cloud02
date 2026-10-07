"""Library-surface QA on synthetic adversaries or the actual original catalog."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import replace
from pathlib import Path

import numpy as np
from scipy.stats import norm

from analysis.alternative_contracts import (
    CaseInput,
    FitConfig,
    FitStatus,
    GateResult,
    JointTrainingSet,
)
from analysis.alternative_data import aligned_joint, load_experiment
from analysis.alternative_joint import fit_joint, predict_joint
from analysis.alternative_joint_audit_data import fixture, method
from analysis.alternative_joint_coordinates import matrix_json, vector_json
from analysis.alternative_joint_folds import component_training
from analysis.alternative_joint_marginals import fit_bjp_marginal, fit_emos_marginal
from analysis.alternative_joint_model import AnnualJointModel
from analysis.data_io import Json


def exercise(training: JointTrainingSet, config: FitConfig) -> dict[str, Json]:
    """Use every actual entry point with original fixed analytic EMOS marginals."""
    marginals = tuple(
        fit_emos_marginal(component_training(training, j), config).predict(target)
        for j, target in enumerate(training.targets)
    )
    results: list[Json] = []
    for identifier in (
        "schaake_window", "schaake_block", "ecc_q", "decc_path_shrunk_error",
        "residual_gaussian_copula", "mbcp_annual", "mbcr_annual", "mbcn_annual",
        "otc_annual", "dotc_annual",
    ):
        started = time.perf_counter()
        fitted = fit_joint(method(identifier), training, None, config)
        if identifier in ("ecc_q", "decc_path_shrunk_error"):
            assert fitted.status == FitStatus.GATED_DATA and fitted.fitted_model is None
            results.append({"id": identifier, "status": fitted.status.value, "reason": fitted.reason_code})
            continue
        assert fitted.status == FitStatus.OK, f"{identifier}: {fitted.reason_code}: {fitted.diagnostics.message}"
        assert fitted.fitted_model is not None
        prediction = predict_joint(fitted.fitted_model, training.targets, marginals, config)
        assert prediction.samples.shape[1] == len(training.targets)
        assert abs(float(np.sum(prediction.weights)) - 1) < 1e-9
        for j, target in enumerate(training.targets):
            if target.variable == "prcp":
                assert np.all(prediction.samples[:, j] >= 0)
        repeated = predict_joint(fitted.fitted_model, training.targets, marginals, replace(config, workers=1))
        assert np.array_equal(prediction.samples, repeated.samples)
        assert np.array_equal(prediction.weights, repeated.weights)
        row: dict[str, Json] = {
            "id": prediction.method_id, "status": fitted.status.value,
            "scenario_count": np.size(prediction.samples, axis=0),
            "seconds": time.perf_counter() - started,
            "mean_first_two": vector_json((prediction.weights @ prediction.samples)[:2]),
            "qq_scenario_p05_p50_p95_first_two": matrix_json(
                np.quantile(prediction.samples[:, :2], [0.05, 0.5, 0.95], axis=0)
            ),
        }
        if identifier == "residual_gaussian_copula":
            assert isinstance(fitted.fitted_model, AnnualJointModel)
            residuals = fitted.fitted_model.residuals
            assert residuals is not None
            probabilities = np.asarray([0.05, 0.25, 0.5, 0.75, 0.95])
            row["qq_standard_normal"] = vector_json(norm.ppf(probabilities))
            row["qq_prequential_normal_scores_first_two"] = matrix_json(
                np.quantile(residuals.residual_matrix[:, :2], probabilities, axis=0)
            )
            row["prequential_years"] = list(residuals.years)
            row["sobol_512_mean_minus_256"] = prediction.approximation_metadata["sobol_512_mean_minus_256"]
        results.append(row)
    return {
        "component_cases": [target.case_id for target in training.targets],
        "dimension": len(training.targets), "years": len(training.source_years),
        "results": results,
    }


def actual_groups(root: Path) -> tuple[JointTrainingSet, ...]:
    inputs = load_experiment(root)
    groups: list[JointTrainingSet] = []
    for product in ("1mon", "3mon"):
        cases = tuple(case for case in inputs.cases if case.product == product)
        first = min(case.init for case in cases)
        latest = max(case.init for case in cases)

        def ordering(case: CaseInput) -> tuple[str, str]:
            return case.variable, case.lead

        full = tuple(sorted((case for case in cases if case.init == first), key=ordering))
        shortest = tuple(sorted(
            (case for case in cases if case.init == latest and inputs.historical.get(case.case_id)),
            key=ordering,
        ))
        unavailable = [
            case.case_id for case in cases if case.init == latest and not inputs.historical.get(case.case_id)
        ]
        print(json.dumps({"scope": "REPRESENTATIVE_KEY_SELECTION", "product": product,
                          "no_history_keys_requiring_root_ledger": unavailable}), flush=True)
        pair_lead = full[0].lead
        pair = tuple(case for case in full if case.lead == pair_lead)
        temperature = tuple(case for case in full if case.variable == "t15m")
        precipitation = tuple(case for case in full if case.variable == "prcp")
        groups.extend((aligned_joint(pair, inputs), aligned_joint(temperature, inputs),
                       aligned_joint(precipitation, inputs), aligned_joint(full, inputs),
                       aligned_joint(shortest, inputs)))
    return tuple(groups)


def main() -> int:
    class Options(argparse.Namespace):
        actual: bool = False

    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--actual", action="store_true", help="Exercise real pair/full/partial keys for both products.")
    options = Options()
    _ = parser.parse_args(namespace=options)
    started = time.perf_counter()
    print("WORKING: joint fit/predict manual QA", flush=True)
    config = FitConfig(workers=1)
    groups = actual_groups(Path.cwd()) if options.actual else (fixture(), fixture(4))
    results = [exercise(group, config) for group in groups]
    bjp_results: list[Json] = []
    if options.actual:
        paired_month = next(
            group for group in groups if len(group.targets) == 2 and group.targets[0].product == "3mon"
        )
        laws = tuple(
            fit_bjp_marginal(component_training(paired_month, j), config).predict(t)
            for j, t in enumerate(paired_month.targets)
        )
        for identifier in ("schaake_window", "schaake_block", "residual_gaussian_copula"):
            fitted = fit_joint(method(identifier, "bjp"), paired_month, None, config)
            assert fitted.fitted_model is not None, fitted.diagnostics.message
            issued = predict_joint(fitted.fitted_model, paired_month.targets, laws, config)
            assert issued.method_id.endswith("__bjp")
            bjp_results.append({"id": issued.method_id, "status": fitted.status.value,
                                "seconds": fitted.diagnostics.elapsed_seconds,
                                "mean": vector_json(issued.weights @ issued.samples)})
    if not options.actual:
        training = fixture(4)
        proof = GateResult(allowed=True, reason_code="G3_SYNTHETIC_AUDIT_ONLY",
                           evidence_refs=("synthetic physical-ID oracle, NOT source-data proof",))
        approved = replace(training, gate_receipts=(proof,))
        marginals = tuple(
            fit_emos_marginal(component_training(approved, j), config).predict(t)
            for j, t in enumerate(approved.targets)
        )
        for identifier in ("ecc_q", "decc_path_shrunk_error"):
            result = fit_joint(method(identifier), approved, None, config)
            assert result.status == FitStatus.OK and result.fitted_model is not None
            issued = predict_joint(result.fitted_model, approved.targets, marginals, config)
            assert np.size(issued.samples, axis=0) == 3
        assert not hasattr(training.targets[0], "observation")
    print(json.dumps({"scope": "ACTUAL_SMOKE" if options.actual else "SYNTHETIC_QA",
                      "groups": results, "bjp_coupling": bjp_results,
                      "elapsed_seconds": time.perf_counter() - started}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
