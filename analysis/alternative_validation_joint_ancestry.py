"""Independent genuine annual-vector hash and scalar-source linkage replay."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from datetime import date
from pathlib import Path

import numpy as np

from analysis.alternative_validation_io import csv_records, decode, require_columns
from analysis.alternative_validation_reference import vector
from analysis.alternative_validation_training_wire import (
    row_ids,
    training_digest,
    year_block,
    years,
)
from analysis.data_io import Json


def joint_ancestry_checks(output: Path) -> dict[str, Json]:
    components = csv_records(output / "joint_component_manifest.csv")
    if not components:
        return {"status": "PASS", "joint_training_hashes": 0, "joint_fold_records": 0}
    require_columns(components, ("joint_train_hash", "component_case_ids", "source_years",
                                 "dimension", "component_training_hashes"), "joint components")
    scalar: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in csv_records(output / "training_ledger.csv.gz"):
        scalar[row["train_hash"]][row["row_id"]] = row
    for digest, records in scalar.items():
        first = next(iter(records.values()))
        if training_digest(list(records.values()), first["cutoff"], first["catalog_cutoff"],
                           first["held_out_years"]) != digest:
            raise AssertionError("joint scalar-source content hash mismatch")
    manifest = csv_records(output / "joint_training_manifest.csv.gz")
    require_columns(manifest, ("joint_train_hash", "source_year", "component_case_ids", "row_ids",
                              "forecast_means", "observations", "cutoff", "catalog_cutoff",
                              "held_out_years", "historical_initialization"), "joint training manifest")
    aligned: dict[str, dict[int, dict[str, str]]] = defaultdict(dict)
    for row in manifest:
        year = int(row["source_year"])
        group = aligned[row["joint_train_hash"]]
        if year in group:
            raise AssertionError("duplicate joint annual vector")
        group[year] = row
    known: set[str] = set()
    for component in components:
        digest = component["joint_train_hash"]
        if digest in known:
            raise AssertionError("duplicate joint component manifest")
        known.add(digest)
        ids = row_ids(component["component_case_ids"])
        hashes = row_ids(component["component_training_hashes"])
        source_years = tuple(sorted(years(component["source_years"])))
        if len(ids) != int(component["dimension"]) or len(ids) != len(hashes):
            raise AssertionError("joint component dimension/hash count mismatch")
        replay = hashlib.sha256()
        pools: list[dict[int, dict[str, str]]] = []
        for case_id, content_hash in zip(ids, hashes, strict=True):
            records = scalar[content_hash]
            if not records or any(r["source_case_id"] != case_id for r in records.values()):
                raise AssertionError("joint component hash lacks genuine scalar source link")
            pool = {int(r["source_year"]): r for r in records.values()}
            if len(pool) != len(records):
                raise AssertionError("joint component has duplicate source years")
            pools.append(pool)
            replay.update(content_hash.encode())
        replay.update(repr(source_years).encode())
        if replay.hexdigest() != digest:
            raise AssertionError("joint vector training content hash mismatch")
        if set(aligned[digest]) != set(source_years):
            raise AssertionError("joint manifest source years differ")
        common = set(pools[0])
        for pool in pools[1:]:
            common.intersection_update(pool)
        first = aligned[digest][source_years[0]]
        heldout = years(first["held_out_years"])
        common = {y for y in common if y not in heldout and not any(
            year_block(date.fromisoformat(p[y]["hist_start"]), date.fromisoformat(p[y]["hist_end"]),
                       heldout) for p in pools)}
        if common != set(source_years):
            raise AssertionError("joint annual complete-case intersection differs")
        for year in source_years:
            row = aligned[digest][year]
            originals = [p[year] for p in pools]
            if row_ids(row["row_ids"]) != [r["row_id"] for r in originals] or row_ids(
                row["component_case_ids"]) != ids:
                raise AssertionError("joint annual vector source/order linkage differs")
            if not np.array_equal(vector(decode(row["observations"])),
                                  np.array([float(r["observation"]) for r in originals])):
                raise AssertionError("joint observations differ from source rows")
            means = np.array([float(np.mean(vector(decode(r["ensemble"])))) for r in originals])
            if not np.array_equal(vector(decode(row["forecast_means"])), means):
                raise AssertionError("joint forecast means differ from source ensembles")
            if {r["source_init"] for r in originals} != {row["historical_initialization"]}:
                raise AssertionError("joint historical initialization alignment differs")
            for field in ("cutoff", "catalog_cutoff", "held_out_years"):
                if any(r[field] != row[field] for r in originals):
                    raise AssertionError(f"joint/scalar {field} differs")
    if known != aligned.keys():
        raise AssertionError("orphan joint annual manifest")
    folds = csv_records(output / "joint_fold_ancestry.csv.gz")
    for fold in folds:
        outer_hash = fold["outer_joint_train_hash"]
        annual = aligned[outer_hash]
        originals = {r["row_id"]: r for records in scalar.values() for r in records.values()}
        train = row_ids(fold["training_row_ids"])
        validation = row_ids(fold["validation_row_ids"])
        cutoff, heldout = date.fromisoformat(fold["pseudo_init"]), years(fold["held_out_years"])
        outer_ids = {key for r in annual.values() for key in row_ids(r["row_ids"])}
        if set(train) & set(validation) or not set(train + validation) <= outer_ids:
            raise AssertionError("joint fold overlap or foreign source")
        if not {int(originals[k]["source_year"]) for k in validation} <= heldout:
            raise AssertionError("joint validation source year not held out")
        expected = [key for y, r in sorted(annual.items()) if y not in heldout and all(
            date.fromisoformat(originals[k]["hist_end"]) < cutoff and not year_block(
                date.fromisoformat(originals[k]["hist_start"]),
                date.fromisoformat(originals[k]["hist_end"]), heldout)
            for k in row_ids(r["row_ids"])) for key in row_ids(r["row_ids"])]
        if train != expected:
            raise AssertionError("joint prequential whole-year ancestors differ")
        actual = hashlib.sha256("|".join((outer_hash, fold["pseudo_init"], *train)).encode()).hexdigest()
        if actual != fold["ancestor_hash"]:
            raise AssertionError("joint fold genuine ancestor hash mismatch")
    return {"status": "PASS", "joint_training_hashes": len(known),
            "joint_fold_records": len(folds)}
