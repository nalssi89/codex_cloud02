"""Complete annual-vector alignment and explicitly measured scientific gates."""

import hashlib
from types import MappingProxyType
from typing import assert_never

import numpy as np

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    GateResult,
    JointTrainingSet,
    MethodSpec,
    TrainingSet,
)
from analysis.alternative_experiment_types import ExperimentInputs
from analysis.alternative_training import training_for


def aligned_joint(component_cases: tuple[CaseInput, ...],
                  inputs: ExperimentInputs) -> JointTrainingSet:
    """Align source years and calendars, without asserting member identity."""
    if not component_cases or len({case.init for case in component_cases}) != 1:
        raise AlternativeError("JOINT_ALIGNMENT", "Empty/different issue dates")
    training = tuple(training_for(case, inputs, "local") for case in component_cases)
    by_component = tuple({row.source_year: row for row in item.rows} for item in training)
    common: set[int] = set(by_component[0])
    for rows in by_component[1:]:
        common.intersection_update(rows)
    years: tuple[int, ...] = tuple(sorted(common))
    held_out = tuple(sorted({year for item in training for year in item.held_out_years}))
    years = tuple(year for year in years if year not in held_out and not any(
        row.hist_start.year <= held <= row.hist_end.year
        for rows in by_component for row in (rows[year],) for held in held_out
    ))
    rows_by_year = {year: tuple(rows[year] for rows in by_component) for year in years}
    for year, rows in rows_by_year.items():
        if len({row.source_init for row in rows}) != 1:
            raise AlternativeError("JOINT_ALIGNMENT", f"Historical issues: {year}")
        for left in rows:
            for right in rows:
                if left.product == right.product and left.lead == right.lead and (
                    left.hist_start, left.hist_end
                ) != (right.hist_start, right.hist_end):
                    raise AlternativeError("JOINT_ALIGNMENT", f"T/P window: {year}")
    x = np.asarray([
        [float(np.mean(row.ensemble)) for row in rows_by_year[year]] for year in years
    ], dtype=np.float64)
    y = np.asarray([
        [row.observation for row in rows_by_year[year]] for year in years
    ], dtype=np.float64)
    for values in (x, y):
        values.setflags(write=False)
    digest = hashlib.sha256()
    for item in training:
        digest.update(item.train_hash.encode())
    digest.update(repr(years).encode())
    return JointTrainingSet(
        targets=component_cases, component_keys=tuple(case.case_id for case in component_cases),
        rows_by_year=MappingProxyType(rows_by_year), source_years=years,
        historical_initializations=tuple(rows_by_year[year][0].source_init for year in years),
        historical_windows=tuple(
            tuple((row.hist_start, row.hist_end) for row in rows_by_year[year]) for year in years
        ), forecast_means=x, observations=y, cutoff=component_cases[0].init,
        catalog_cutoff=component_cases[0].init, held_out_years=held_out,
        train_hash=digest.hexdigest(),
        gate_receipts=(GateResult(
            allowed=len(years) >= 10, reason_code="ALIGNED_ANNUAL_VECTORS",
            evidence_refs=(".omo/evidence/alternative-input-applicability.md",),
            counts={"years": len(years), "components": len(component_cases)},
        ),),
    )


def gate_report(spec: MethodSpec, training: TrainingSet | JointTrainingSet,
                inputs: ExperimentInputs) -> GateResult:
    """Unsupported physical/iid claims stay gates, not invented metadata."""
    evidence = (".omo/evidence/alternative-input-applicability.md",)
    closed = {"G3", "G4", "G5"}
    if closed.intersection(spec.gate_ids):
        return GateResult(
            allowed=False, reason_code="PHYSICAL_GROUP_OR_NOISE_METADATA_UNDOCUMENTED",
            evidence_refs=evidence,
        )
    match training:
        case TrainingSet():
            years = len({row.source_year for row in training.rows})
            if "G0" in spec.gate_ids and np.any(training.local_observations <= 0):
                return GateResult(
                    allowed=False, reason_code="POSITIVE_GAMMA_ZERO_TRAINING",
                    evidence_refs=evidence,
                )
        case JointTrainingSet():
            years = len(training.source_years)
            if "G6" in spec.gate_ids and years < 20:
                return GateResult(
                    allowed=False, reason_code="HISTORICAL_BLOCKS_BELOW_TEN_YEARS",
                    evidence_refs=evidence,
                )
            if "G6" in spec.gate_ids and any(
                len({rows[column].archive_era for rows in training.rows_by_year.values()}) != 1
                for column in range(len(training.targets))
            ):
                return GateResult(
                    allowed=False, reason_code="HISTORICAL_ARCHIVE_ERA_CONFLICT",
                    evidence_refs=evidence,
                )
        case _:
            assert_never(training)
    return GateResult(
        allowed=years >= 10, reason_code="INPUTS_AVAILABLE" if years >= 10 else "INSUFFICIENT_TRAINING",
        evidence_refs=evidence, counts={"years": years, "catalog_cases": len(inputs.cases)},
    )
