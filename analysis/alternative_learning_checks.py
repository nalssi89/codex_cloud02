"""Executable mathematical and adversarial checks for learning entry points."""

from __future__ import annotations

from dataclasses import replace
from datetime import date

import numpy as np

from analysis.alternative_contracts import (
    CaseInput,
    CategoryFitResult,
    FitConfig,
    FitStatus,
    MethodSpec,
    TrainingRow,
    TrainingSet,
)
from analysis.alternative_learning import fit_learning, predict_categories
from analysis.alternative_learning_category import (
    historical_labels,
    ordinal_probabilities,
)
from analysis.calibration import FloatArray


def fixture(rain: bool = False, constant: bool = False) -> TrainingSet:
    target = CaseInput(
        case_id="audit-target", init=date(2024, 2, 1),
        valid_start=date(2024, 2, 1), valid_end=date(2024, 2, 7),
        product="1mon", lead="W1", variable="prcp" if rain else "t15m",
        members=np.array([4., 5., 6.]), member_keys=("a", "b", "c"),
        provenance_hash="learning-audit", archive_era="three_24",
    )
    rows: list[TrainingRow] = []
    for year in range(1993, 2023):
        for condition in range(2):
            value = 5. if constant else (
                0. if rain and year % 5 == 0
                else 4 + .3 * (year - 1993) + 2 * np.sin(year) + condition
            )
            rows.append(TrainingRow(
                row_id=f"{year}:{condition}", source_case_id=f"condition:{condition}",
                source_case_init=date(2022, 12, 1), source_year=year,
                source_init=date(year, 2, 1), hist_start=date(year, 2, 1),
                hist_end=date(year, 2, 7), product=target.product, lead=target.lead,
                variable=target.variable, ensemble=np.array([value - .3, value, value + .3]),
                observation=float(value), member_keys=target.member_keys,
                provenance_hash=target.provenance_hash, archive_era=target.archive_era,
            ))
    if rain:
        rows = [replace(row, ensemble=np.maximum(row.ensemble, 0)) for row in rows]
    local = np.array([row.observation for row in rows[::2]])
    return TrainingSet(
        target=target, rows=tuple(rows), year_weights=np.full(len(rows), .5),
        cutoff=target.init, catalog_cutoff=target.init, held_out_years=(2024,),
        train_hash=f"audit-{rain}-{constant}", local_observations=local,
        thresholds=np.quantile(local, [1 / 3, 2 / 3]),
    )


def method(identifier: str) -> MethodSpec:
    return MethodSpec(
        id=identifier, family_no=11, subtype=identifier, domain="both",
        surface="category" if identifier in ("ordinal_logit", "elr_threshold_logit") else "continuous",
        fit_scope="pooled", algorithm_version="frozen-section7", owner="learning",
    )


def check_ancestry() -> None:
    training = fixture()
    selected, _, _, ancestors = historical_labels(training)
    assert len(selected) == 40
    by_id = {row.row_id: row for row in training.rows}
    for index, ids in zip(selected, ancestors, strict=True):
        row = training.rows[int(index)]
        assert len(ids) >= 10
        assert row.row_id not in ids
        valid_years = tuple(range(row.hist_start.year, row.hist_end.year + 1))
        held_out_source = {row.source_year, *valid_years}
        for ancestor_id in ids:
            ancestor = by_id[ancestor_id]
            assert ancestor.hist_end < row.source_init
            assert ancestor.source_year not in held_out_source
            assert not any(ancestor.hist_start.year <= year <= ancestor.hist_end.year for year in valid_years)
            assert ancestor.source_case_init > row.source_init
            assert ancestor.source_case_init <= training.catalog_cutoff
    parameters = np.array([-.7, .5, 0., 1.])
    x = np.array([[0., -1.], [0., 0.], [0., 1.]])
    probabilities = ordinal_probabilities(parameters, x)
    assert np.all(probabilities >= 0)
    np.testing.assert_allclose(probabilities.sum(axis=1), 1, atol=1e-14)
    assert np.all(np.diff(probabilities[:, 0]) < 0)
    # Adversarial year metadata: date gating alone would admit this ancestor.
    validation = replace(
        training.rows[34], source_year=2009, source_init=date(2009, 12, 28),
        hist_start=date(2009, 12, 28), hist_end=date(2010, 1, 3),
        row_id="crossing-validation",
    )
    candidate = replace(
        training.rows[0], row_id="crossing-bad-year",
        source_year=2010, hist_start=date(2008, 2, 1), hist_end=date(2008, 2, 7),
    )
    adversary = replace(training, rows=(*training.rows, validation, candidate))
    selected_rows, _, _, cross_ancestors = historical_labels(adversary)
    position = selected_rows.index(len(training.rows))
    assert candidate.row_id not in cross_ancestors[position]


def check_year_crossing() -> None:
    from analysis.alternative_data import row_thresholds

    training = fixture()
    crossed = replace(training, rows=tuple(
        replace(
            row, lead="W2", source_init=date(row.source_year, 12, 28),
            hist_start=date(row.source_year + 1, 1, 4),
            hist_end=date(row.source_year + 1, 1, 10),
        ) for row in training.rows
    ))
    selected, _, thresholds, _ = historical_labels(crossed)
    assert len(selected) == 40
    for position, index in enumerate(selected):
        expected = row_thresholds(crossed, crossed.rows[index])
        assert expected is not None
        np.testing.assert_array_equal(expected, thresholds[position:position + 1].reshape(-1))


def check_categories() -> None:
    for constant in (False, True):
        training = fixture(constant=constant)
        for identifier in ("ordinal_logit", "elr_threshold_logit"):
            result = fit_learning(method(identifier), training, FitConfig())
            assert result.status == FitStatus.OK, result.reason_code
            assert result.fitted_model is not None
            model = result.fitted_model
            # This function is exercised only for the category IDs above.
            assert isinstance(result, CategoryFitResult)
            assert result.fitted_model is not None
            prediction = predict_categories(result.fitted_model, training.target, training.thresholds)
            assert np.all(np.isfinite(prediction.probabilities))
            np.testing.assert_allclose(prediction.probabilities.sum(), 1, atol=1e-14)
            assert np.all(prediction.probabilities >= 0)
            tied: FloatArray = np.array([5., 5.])
            collapsed = predict_categories(result.fitted_model, training.target, tied)
            assert collapsed.probabilities[1] == 0
            assert "label_ancestors" in model.to_spec()
            print(identifier, "constant=" + str(constant), result.diagnostics.objective)


def check_input_boundaries() -> None:
    training = fixture()
    too_short = replace(training, rows=training.rows[:18], year_weights=training.year_weights[:18])
    for identifier in ("ordinal_logit", "gamlss_ridge"):
        result = fit_learning(method(identifier), too_short, FitConfig())
        assert result.status == FitStatus.INSUFFICIENT_TRAINING
        assert result.fitted_model is None and not result.diagnostics.convergence
        assert result.diagnostics.n_years == 9
    try:
        _ = fit_learning(replace(method("ordinal_logit"), id="unknown-learning"), training, FitConfig())
    except ValueError:
        return
    else:
        raise AssertionError("Unknown learning ID accepted")


if __name__ == "__main__":
    check_ancestry()
    print("OWNPAST ANCESTRY AND ORDINAL MASS PASS")
    check_categories()
    print("CATEGORY FIT, TIED CUTS, EMPTY MIDDLE CATEGORY PASS")
    check_input_boundaries()
    print("INSUFFICIENT SUPPORT AND UNKNOWN ID REJECTION PASS")
    check_year_crossing()
    print("YEAR-CROSSING PAST LABELS MATCH DATA HELPER PASS")
