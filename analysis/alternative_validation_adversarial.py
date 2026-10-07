"""Actual adapter/fit perturbations: withheld truth, dates, catalog and hashes."""

from __future__ import annotations

from dataclasses import replace
from datetime import date
from pathlib import Path
from types import MappingProxyType

import numpy as np

from analysis.alternative_contracts import AlternativeError, FitConfig, TrainingRow
from analysis.alternative_experiment_types import ExperimentInputs, ScoreTruth
from analysis.alternative_validation_learning import fixture
from analysis.alternative_validation_oracles import close
from analysis.data_io import Json


def adversarial_checks() -> dict[str, Json]:
    from analysis.alternative_bayes_distribution import forward
    from analysis.alternative_data import (
        aligned_joint,
        fold_training,
        inner_folds,
        training_for,
    )
    from analysis.alternative_learning_order import fit_order

    base = fixture()
    truth = ScoreTruth(case_id=base.target.case_id, observation=3.,
                       historical_observations=base.local_observations,
                       thresholds=base.thresholds)
    inputs = ExperimentInputs(root=Path("."), source=Path("synthetic"),
                              cases=(base.target,), historical=MappingProxyType({
                                  base.target.case_id: base.rows}),
                              truths=MappingProxyType({base.target.case_id: truth}),
                              excluded_cases=MappingProxyType({}),
                              provenance=MappingProxyType({"daily_sha256": "synthetic"}))
    training = training_for(base.target, inputs, "local")
    changed_truth = replace(inputs, truths=MappingProxyType({
        base.target.case_id: replace(truth, observation=1e12)}))
    sentinel_training = training_for(base.target, changed_truth, "local")
    if training.train_hash != sentinel_training.train_hash:
        raise AssertionError("held-out truth changes training hash")
    model, _ = fit_order("qrf_year_forest", training, FitConfig(seed=42, workers=1))
    sentinel_model, _ = fit_order("qrf_year_forest", sentinel_training,
                                FitConfig(seed=42, workers=6))
    if model.to_spec() != sentinel_model.to_spec():
        raise AssertionError("held-out truth/worker count changed fitted parameters")
    issued = model.predict(base.target)
    if issued.to_spec() != sentinel_model.predict(base.target).to_spec():
        raise AssertionError("held-out truth changes prediction")
    if issued.crps(truth.observation) == issued.crps(1e12):
        raise AssertionError("held-out truth perturbation failed to change score")
    seed_row = base.rows[0]
    invalid_rows = (
        replace(seed_row, row_id="boundary", hist_end=base.cutoff),
        replace(seed_row, row_id="future_response", hist_start=date(2027, 1, 1),
                hist_end=date(2027, 1, 7)),
        replace(seed_row, row_id="heldout_source", source_year=2026),
        replace(seed_row, row_id="crossing", hist_start=date(2025, 12, 30),
                hist_end=date(2026, 1, 5)),
        replace(seed_row, row_id="future_case_copy", source_case_init=date(2027, 1, 1)),
    )
    augmented = replace(inputs, historical=MappingProxyType({
        base.target.case_id: (*base.rows, *invalid_rows)}))
    with_excluded = training_for(base.target, augmented, "pooled")
    if with_excluded.train_hash != training.train_hash:
        raise AssertionError("boundary/future/heldout/crossing/catalog row not excluded")
    excluded_model, _ = fit_order("qrf_year_forest", with_excluded, FitConfig(seed=42))
    if excluded_model.predict(base.target).to_spec() != issued.to_spec():
        raise AssertionError("excluded rows changed actual fitted forecast")
    perturbed_excluded = replace(augmented, historical=MappingProxyType({
        base.target.case_id: (*base.rows, *(replace(r, observation=1e12) for r in invalid_rows))}))
    if training_for(base.target, perturbed_excluded, "pooled").train_hash != training.train_hash:
        raise AssertionError("excluded-row truth changed fit key")
    excluded_changed_model, _ = fit_order("qrf_year_forest", training_for(
        base.target, perturbed_excluded, "pooled"), FitConfig(seed=42))
    if excluded_changed_model.to_spec() != model.to_spec():
        raise AssertionError("changing excluded truth changed actual fit parameters")
    shuffled = replace(inputs, historical=MappingProxyType({
        base.target.case_id: tuple(reversed(base.rows))}))
    shuffled_training = training_for(base.target, shuffled, "local")
    if shuffled_training.train_hash != training.train_hash:
        raise AssertionError("input-order changes ordered training hash")
    accepted_changed = replace(inputs, historical=MappingProxyType({
        base.target.case_id: (replace(seed_row, observation=seed_row.observation+1), *base.rows[1:])}))
    if training_for(base.target, accepted_changed, "local").train_hash == training.train_hash:
        raise AssertionError("accepted truth absent from training hash")
    provenance_changed = replace(inputs, historical=MappingProxyType({
        base.target.case_id: tuple(replace(r, provenance_hash="new-active-daily-hash")
                                   for r in base.rows)}))
    if training_for(base.target, provenance_changed, "local").train_hash == training.train_hash:
        raise AssertionError("active observation hash permits stale fit reuse")
    contradictory = replace(inputs, historical=MappingProxyType({
        base.target.case_id: (*base.rows, replace(seed_row, observation=1e12))}))
    try:
        _ = training_for(base.target, contradictory, "pooled")
    except AlternativeError as error:
        if error.code != "INPUT_CONFLICT":
            raise
    else:
        raise AssertionError("contradictory duplicate was not INPUT_CONFLICT")
    empty = replace(inputs, historical=MappingProxyType({base.target.case_id: ()}))
    try:
        _ = training_for(base.target, empty, "pooled")
    except AlternativeError as error:
        if error.code != "INSUFFICIENT_TRAINING":
            raise
    else:
        raise AssertionError("empty allowed pool did not fail explicitly")
    try:
        _ = forward(np.array([-1., 2.]), "sqrt")
    except ValueError:
        pass
    else:
        raise AssertionError("negative rain accepted by physical transform boundary")
    # Complete annual blocks are intersected; never imputed or independently paired.
    second = replace(base.target, case_id="second", variable="prcp", members=np.array([10.]))
    unique = tuple(r for r in base.rows if r.row_id.endswith(":0"))
    rain_rows = tuple(replace(r, row_id="rain:"+r.row_id, source_case_id=second.case_id,
                              variable="prcp", observation=r.observation+1,
                              ensemble=r.ensemble+1) for r in unique[1:])
    joint_inputs = replace(inputs, cases=(base.target, second), historical=MappingProxyType({
        base.target.case_id: unique, second.case_id: rain_rows}))
    joint = aligned_joint((base.target, second), joint_inputs)
    if joint.source_years != tuple(range(1991, 2010)) or joint.observations.shape != (19, 2):
        raise AssertionError("incomplete joint year was paired/imputed")
    folds = inner_folds(training, base.target, min_years=10, last_n=None)
    if not folds:
        raise AssertionError("outer-frozen 2022-vintage historical folds all discarded")
    for fold in folds:
        ancestor = fold_training(training, fold)
        if ancestor.catalog_cutoff != training.catalog_cutoff:
            raise AssertionError("fold tightened original catalog to historical pseudo-issue")
        if ancestor.cutoff != fold.pseudo_init or ancestor.train_hash != fold.ancestor_hash:
            raise AssertionError("fold response cutoff/hash replay mismatch")
        if any(row.hist_end >= ancestor.cutoff or row.source_year in ancestor.held_out_years
               for row in ancestor.rows):
            raise AssertionError("inner fold leaks validation block")
        close(float(np.sum(ancestor.year_weights)), float(len({
            row.source_year for row in ancestor.rows})), "fold balanced year count")
    return {"status": "PASS", "truth_sentinel": 1e12, "excluded_perturbations": 5,
            "worker_counts": [1, 6], "historical_folds": len(folds),
            "single_member_target": True, "contradictory_duplicate": "INPUT_CONFLICT",
            "catalog": "OUTER_FROZEN_2022_VINTAGES_RETAINED",
            "empty_pool": "INSUFFICIENT_TRAINING", "negative_rain": "REJECTED",
            "complete_joint_years": len(joint.source_years)}


def crossing_fold_checks() -> dict[str, Json]:
    """A December pseudo-issue must hold out SOURCE year as well as next valid year."""
    from analysis.alternative_data import inner_folds, training_for
    from analysis.alternative_validation_ancestry import calendar_window

    base = fixture()
    target = replace(base.target, case_id="cross", init=date(2026, 12, 15),
                     valid_start=date(2027, 1, 1), valid_end=date(2027, 1, 31),
                     product="3mon", lead="M1")
    cross_rows: list[TrainingRow] = []
    early_rows: list[TrainingRow] = []
    for row in base.rows:
        late = date(row.source_year, 12, 15)
        first, last = calendar_window(late, "3mon", "M1")
        cross_rows.append(replace(row, row_id="cross:"+row.row_id, source_case_id="cross",
                                  source_case_init=date(2022, 12, 15), source_init=late,
                                  hist_start=first, hist_end=last, product="3mon", lead="M1"))
        early = date(row.source_year, 1, 15)
        first, last = calendar_window(early, "3mon", "M1")
        early_rows.append(replace(row, row_id="early:"+row.row_id, source_case_id="early",
                                  source_case_init=date(2022, 1, 15), source_init=early,
                                  hist_start=first, hist_end=last, product="3mon", lead="M1"))
    inputs = ExperimentInputs(root=Path("."), source=Path("synthetic"),
                              cases=(target,), historical=MappingProxyType({
                                  "cross": tuple(cross_rows), "early": tuple(early_rows)}),
                              truths=MappingProxyType({}), excluded_cases=MappingProxyType({}),
                              provenance=MappingProxyType({"daily_sha256": "synthetic"}))
    training = training_for(target, inputs, "pooled")
    by_id = {row.row_id: row for row in training.rows}
    folds = inner_folds(training, target, min_years=10, last_n=5)
    if len(folds) < 3:
        raise AssertionError("crossing-fold synthetic case unexpectedly lacks inner folds")
    for fold in folds:
        source_year = by_id[fold.validation_row_ids[0]].source_year
        leaks = [key for key in fold.training_row_ids if by_id[key].source_year == source_year]
        if leaks:
            raise AssertionError(
                f"{fold.fold_id}: validation SOURCE_YEAR={source_year} retained " +
                f"pooled rows {leaks}; held_out_years={fold.held_out_years}")
    return {"status": "PASS", "crossing_folds": len(folds),
            "SOURCE_and_VALID_year_blocks": "EXCLUDED"}
