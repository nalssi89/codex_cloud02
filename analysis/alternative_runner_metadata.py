"""Explicit measured metadata, separate from fit-key and target-score inputs."""

from collections import Counter
from collections.abc import Sequence
from time import perf_counter

from analysis.alternative_experiment_types import ExperimentInputs
from analysis.alternative_runner_engine import Engine
from analysis.alternative_runner_io import digest, json_value
from analysis.alternative_runner_types import RunOptions
from analysis.data_io import Json


def case_statuses(inputs: ExperimentInputs, options: RunOptions) -> dict[str, Json]:
    return {
        case.case_id: {
            "target_available": case.case_id in inputs.truths,
            "observation_status": "OK" if case.case_id in inputs.truths else
            inputs.excluded_cases[case.case_id],
            "history_rows": len(inputs.historical.get(case.case_id, ())),
            "history_years": len({row.source_year for row in inputs.historical.get(case.case_id, ())}),
            "selected": not options.case_ids or case.case_id in options.case_ids,
        } for case in inputs.cases
    }


def complete_metadata(engine: Engine, results: Sequence[dict[str, Json]],
                      started: float) -> dict[str, Json]:
    receipts: dict[str, Json] = {}
    for result in results:
        status = result["status"]
        if not isinstance(status, dict):
            raise TypeError("Terminal result status must be an object")
        if "gate" in result:
            receipt: dict[str, Json] = {
                "case_id": status["case_id"], "method_id": status["method_id"],
                "surface": status["surface"], "training_hash": result.get(
                    "training_hash", result.get("joint_train_hash")),
                "evaluation": "EVALUATED", "gate": result["gate"],
            }
        else:
            receipt = {
                "case_id": status["case_id"], "method_id": status["method_id"],
                "surface": status["surface"], "evaluation": "NOT_EVALUATED",
                "skip_reason": status["reason_code"],
            }
        receipts[digest(receipt)] = receipt
    return {
        "gate_receipts": list(receipts.values()),
        "cache_counts": {
            "fit_reuse_hits": engine.fit_reuses,
            "resume_prediction_hits": engine.resume_hits,
            "local_training_sets": len(engine.cache.local),
            "pooled_training_sets": len(engine.cache.pooled),
            "required_fold_cache_entries": len(engine.fold_cache),
            "training_count_cache_entries": len(engine.count_cache),
        },
        "timings": {
            "elapsed_seconds_at_artifact_export": perf_counter() - started,
            "task_elapsed_seconds": sum(float(value) for result in results
                                       if isinstance(value := result.get("elapsed_seconds"), (int, float))),
        },
        "terminal_status_counts": json_value(Counter(
            str(result["status"].get("status")) for result in results
            if isinstance(result["status"], dict))),
    }
