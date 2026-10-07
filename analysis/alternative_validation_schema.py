"""In-memory wire-schema roundtrips and adversarial score-field checks."""

from __future__ import annotations

import csv
import io
import json
from collections.abc import Callable
from dataclasses import replace
from datetime import date
from pathlib import Path

import numpy as np

from analysis.alternative_validation_ancestry import training_digest
from analysis.alternative_validation_io import decode, mapping, number, require_columns
from analysis.alternative_validation_learning import fixture
from analysis.alternative_validation_oracles import close
from analysis.alternative_validation_scores import category_score
from analysis.data_io import Json


def schema_checks() -> dict[str, Json]:
    from analysis.alternative_data import training_for
    from analysis.alternative_experiment_types import ExperimentInputs

    category = {"case_id": "prototype", "method_id": "ordinal_logit", "OBS": "2",
                "Q33": "2", "Q67": "2", "P_BN": ".75", "P_NN": "0", "P_AN": ".25",
                "BRIER": ".125", "RPS": ".125"}
    category_score(category)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(category))
    header_writers: list[Callable[[], object]] = [writer.writeheader]
    row_writers: list[Callable[[dict[str, str]], object]] = [writer.writerow]
    _ = header_writers[0]()
    _ = row_writers[0](category)
    _ = buffer.seek(0)
    restored = list(csv.DictReader(buffer))
    if restored != [category]:
        raise AssertionError("lowercase IDs / uppercase score CSV schema failed roundtrip")
    category_score(restored[0])
    failures = 0
    for corrupted in ({**category, "P_NN": ".1"}, {**category, "BRIER": "0"},
                      {**category, "Q33": "3", "Q67": "2"}):
        try:
            category_score(corrupted)
        except AssertionError:
            failures += 1
        else:
            raise AssertionError("adversarial category schema/score mutation was accepted")
    try:
        require_columns([{"CASE_ID": "wrong_case"}], ("case_id",), "case-sensitive wire ID")
    except AssertionError:
        failures += 1
    else:
        raise AssertionError("uppercase-only identity silently passed lowercase wire schema")
    for invalid in (True, float("nan"), float("inf")):
        try:
            _ = number(invalid)
        except (TypeError, ValueError):
            failures += 1
        else:
            raise AssertionError("invalid numeric metadata accepted")
    wire: dict[str, Json] = {"case_id": "prototype", "method_id": "raw", "fit_ref": "h",
                             "distribution": {"tag": "weighted_empirical", "values": [0., 2.],
                                              "weights": [.5, .5]}}
    if mapping(decode(json.dumps(wire))) != wire:
        raise AssertionError("tagged JSON law failed roundtrip")
    base = fixture()
    inputs = ExperimentInputs(root=Path("."),
                              source=Path("synthetic"), cases=(base.target,),
                              historical={base.target.case_id: base.rows}, truths={},
                              excluded_cases={}, provenance={})
    training = training_for(base.target, inputs, "local")
    rows = [{
        "row_id": r.row_id, "source_case_id": r.source_case_id,
        "source_case_init": r.source_case_init.isoformat(), "source_year": str(r.source_year),
        "source_init": r.source_init.isoformat(), "hist_start": r.hist_start.isoformat(),
        "hist_end": r.hist_end.isoformat(), "product": r.product, "variable": r.variable,
        "lead": r.lead, "observation": str(r.observation),
        "member_keys": json.dumps(r.member_keys), "source_files": json.dumps(r.source_files),
        "provenance_hash": r.provenance_hash, "archive_era": r.archive_era,
        "ensemble": json.dumps(r.ensemble.tolist()),
    } for r in training.rows]
    digest = training_digest(rows, training.cutoff.isoformat(), training.catalog_cutoff.isoformat(),
                             json.dumps(training.held_out_years))
    if digest != training.train_hash:
        raise AssertionError("saved training wire schema does not replay actual adapter hash")
    # Accepted calendars remain explicit and dates are not serialized as timestamps.
    if replace(base.target, init=date(2026, 2, 1)).init.isoformat() != "2026-02-01":
        raise AssertionError("date-only wire format changed")
    close(float(np.sum(training.year_weights)), 20., "prototype annual mass")
    return {"status": "PASS", "adversarial_rejections": failures,
            "CSV_JSON_roundtrips": 2, "training_hash_replayed": digest,
            "scope": "SYNTHETIC_SCHEMA_ONLY_NOT_FULL_EXPERIMENT"}
