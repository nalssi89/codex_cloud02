"""Required schedule candidates and exported ancestry from actual fitted receipts."""

from __future__ import annotations

from collections.abc import Iterator

from analysis.alternative_contracts import FoldSpec, MethodSpec, TrainingSet
from analysis.alternative_data import inner_folds
from analysis.alternative_runner_io import Row, dumps
from analysis.alternative_training import training_hash
from analysis.data_io import Json


def required_folds(spec: MethodSpec, training: TrainingSet) -> tuple[FoldSpec, ...]:
    if spec.id == "bma_component_pool":
        return inner_folds(training, training.target, 10, None)
    if spec.id in {"cdf_mix_cv", "tweedie_selected_p"}:
        return inner_folds(training, training.target, 15, 5)
    return ()


def actual_fold_rows(fit: dict[str, Json], training: TrainingSet) -> Iterator[Row]:
    """Never label a generic target-global candidate as an executed model ancestor."""
    rows = {row.row_id: row for row in training.rows}
    diagnostics = fit.get("diagnostics")
    if isinstance(diagnostics, dict):
        posterior = diagnostics.get("posterior_diagnostics")
        if isinstance(posterior, dict):
            receipts = posterior.get("fold_receipts")
            if isinstance(receipts, list):
                candidates = {fold.fold_id: fold for fold in inner_folds(
                    training, training.target, 10, None)}
                for receipt in receipts:
                    if not isinstance(receipt, dict):
                        raise TypeError("Actual fold receipt must be an object")
                    train_ids, valid_ids = receipt["training_row_ids"], receipt["validation_row_ids"]
                    if not isinstance(train_ids, list) or not isinstance(valid_ids, list):
                        raise TypeError("Actual fold row IDs must be arrays")
                    accepted = tuple(sorted((rows[str(key)] for key in train_ids), key=lambda row: row.row_id))
                    validation = tuple(rows[str(key)] for key in valid_ids)
                    candidate = candidates[str(receipt["fold_id"])]
                    held_out = candidate.held_out_years
                    cutoff = validation[0].source_init
                    ancestor = training_hash(accepted, cutoff, training.catalog_cutoff, held_out)
                    supplied_hash = receipt.get("ancestor_hash", receipt.get("train_hash"))
                    if ancestor != supplied_hash or cutoff.isoformat() != receipt["pseudo_init"]:
                        raise ValueError("Actual component fold receipt failed content/calendar replay")
                    yield {
                        "fold_id": str(receipt["fold_id"]), "training_row_ids": dumps(train_ids),
                        "validation_row_ids": dumps(valid_ids), "pseudo_init": cutoff.isoformat(),
                        "held_out_years": dumps(held_out), "ancestor_hash": ancestor,
                        "outer_train_hash": training.train_hash,
                        "catalog_cutoff": training.catalog_cutoff.isoformat(),
                        "role": "executed_prequential_model",
                    }
    model = fit.get("model")
    if not isinstance(model, dict):
        return
    labels, ancestors = model.get("label_rows"), model.get("label_ancestors")
    if not isinstance(labels, list) or not isinstance(ancestors, list):
        return
    for label, ancestor_ids in zip(labels, ancestors, strict=True):
        if not isinstance(ancestor_ids, list):
            raise TypeError("Actual category label ancestry must be an array")
        validation = rows[str(label)]
        accepted = tuple(sorted((rows[str(key)] for key in ancestor_ids), key=lambda row: row.row_id))
        held_out = tuple(sorted({
            validation.source_year, *range(validation.hist_start.year, validation.hist_end.year + 1),
        }))
        ancestor = training_hash(accepted, validation.source_init, training.catalog_cutoff, held_out)
        yield {
            "fold_id": f"{validation.source_case_id}/label/{validation.source_year}",
            "training_row_ids": dumps(ancestor_ids), "validation_row_ids": dumps([label]),
            "pseudo_init": validation.source_init.isoformat(),
            "held_out_years": dumps(held_out), "ancestor_hash": ancestor,
            "outer_train_hash": training.train_hash,
            "catalog_cutoff": training.catalog_cutoff.isoformat(),
            "role": "actual_own_condition_category_label_climatology",
        }
