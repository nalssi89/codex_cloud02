"""Read the protected catalog without regenerating baseline outputs."""

import math
from collections import defaultdict
from collections.abc import Mapping
from datetime import date
from pathlib import Path
from types import MappingProxyType
from typing import NamedTuple

import numpy as np

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    Product,
    TrainingRow,
    Variable,
)
from analysis.alternative_experiment_types import ExperimentInputs, ScoreTruth
from analysis.data_io import (
    DATASET,
    Observation,
    aggregate_observation,
    check_manifest,
    csv_rows,
    expected_window,
    load_cases,
    load_daily,
    load_references,
    observation_provenance,
    parse_date,
)


class Member(NamedTuple):
    """Original stored identity is retained, not interpreted as physical iid."""

    key: str
    value: float
    source_init: date
    source_file: str


def _groups(path: Path, historical: bool) -> Mapping[tuple[str, int], tuple[Member, ...]]:
    """Parse each member CSV once and reject contradictory identity rows."""
    groups: dict[tuple[str, int], list[Member]] = defaultdict(list)
    seen: set[tuple[str, int, str]] = set()
    for row in csv_rows(path):
        year = int(row["SOURCE_YEAR"]) if historical else 0
        identity = (row["CASE_ID"], year, row["MEMBER"])
        if identity in seen:
            raise AlternativeError("INPUT_CONFLICT", f"Duplicate member: {identity}")
        seen.add(identity)
        if not row["VALUE"]:
            if historical:
                raise AlternativeError("INPUT_CONFLICT", f"Empty hindcast: {identity}")
            continue
        value = float(row["VALUE"])
        if not math.isfinite(value):
            if historical:
                raise AlternativeError("INPUT_CONFLICT", f"Nonfinite hindcast: {identity}")
            continue
        if row["VARIABLE"] == "prcp" and value < 0:
            raise AlternativeError("NEGATIVE_RAIN", str(identity))
        source_init = parse_date(row["SOURCE_DATE"] if historical else row["INIT_DATE"])
        if historical and source_init.year != year:
            raise AlternativeError("INPUT_CONFLICT", f"Source year/date: {identity}")
        groups[(row["CASE_ID"], year)].append(
            Member(row["MEMBER"], value, source_init, row["SOURCE_FILE"]),
        )
    return MappingProxyType({key: tuple(value) for key, value in groups.items()})


def _product(value: str) -> Product:
    """Parse the known archive product at the input boundary."""
    match value:
        case "1mon":
            return "1mon"
        case "3mon":
            return "3mon"
        case _:
            raise AlternativeError("UNKNOWN_PRODUCT", value)


def _variable(value: str) -> Variable:
    """Parse native temperature/rain units without mixing responses."""
    match value:
        case "t15m":
            return "t15m"
        case "prcp":
            return "prcp"
        case _:
            raise AlternativeError("UNKNOWN_VARIABLE", value)


def _era(ensembles: tuple[tuple[int, tuple[Member, ...]], ...]) -> str:
    """Name only measured archive counts, never their physical cause."""
    counts = {len(members) for _, members in ensembles}
    years = {year for year, _ in ensembles}
    if counts == {3} and len(years) == 24:
        return "three_24"
    if counts == {7} and len(years) == 24:
        return "seven_24"
    if counts == {7} and len(years) == 30:
        return "seven_30"
    raise AlternativeError("UNKNOWN_ARCHIVE_ERA", f"{sorted(counts)}/{sorted(years)}")


def load_experiment(root: Path) -> ExperimentInputs:
    """Load actual source forecasts/annual observations, truth kept separate."""
    root = root.resolve()
    source = root / DATASET
    checked = check_manifest(source)
    original_cases = load_cases(source)
    daily = load_daily(source)
    provenance = {**observation_provenance(source), "manifest_verified_files": len(checked)}
    observation_hash = str(provenance["source_daily_sha256"])
    references = load_references(source)
    baseline_audit = {row["CASE_ID"]: row for row in csv_rows(root / "outputs/case_audit.csv")}
    cases: list[CaseInput] = []
    histories: dict[str, tuple[TrainingRow, ...]] = {}
    truths: dict[str, ScoreTruth] = {}
    excluded: dict[str, str] = {}
    aggregates: dict[tuple[date, date, bool], Observation] = {}

    def observed(start: date, end: date, rain: bool) -> Observation:
        key = (start, end, rain)
        if key not in aggregates:
            aggregates[key] = aggregate_observation(daily, start, end, rain)
        return aggregates[key]

    for product in ("1mon", "3mon"):
        for variable in ("t15m", "prcp"):
            forecast = _groups(source / f"data/model/fcst_raw/{product}_{variable}.csv.gz", False)
            historical = _groups(source / f"data/model/hcst_mapping/{product}_{variable}.csv.gz", True)
            by_case: dict[str, list[tuple[int, tuple[Member, ...]]]] = defaultdict(list)
            for (case_id, year), members in historical.items():
                by_case[case_id].append((year, members))
            for case in original_cases:
                if (case.product, case.variable) != (product, variable):
                    continue
                members = forecast[(case.case_id, 0)]
                start, end = expected_window(case.init, product, case.lead)
                annual = tuple(sorted(by_case[case.case_id], key=lambda pair: pair[0]))
                era = _era(annual)
                values = np.asarray([member.value for member in members], dtype=np.float64)
                values.setflags(write=False)
                target = CaseInput(
                    case_id=case.case_id, init=case.init, valid_start=start, valid_end=end,
                    product=_product(product), lead=case.lead, variable=_variable(variable),
                    members=values, member_keys=tuple(member.key for member in members),
                    provenance_hash=observation_hash, archive_era=era,
                )
                cases.append(target)
                actual = observed(start, end, variable == "prcp")
                audit = baseline_audit[case.case_id]
                if actual.status != "OK" or actual.value is None:
                    if audit["STATUS"] == "VERIFIED":
                        raise AlternativeError("BASELINE_REGRESSION", case.case_id)
                    excluded[case.case_id] = actual.status
                    continue
                if audit["STATUS"] != "VERIFIED" or abs(float(audit["OBS"]) - actual.value) > 1e-12:
                    raise AlternativeError("BASELINE_REGRESSION", case.case_id)
                rows: list[TrainingRow] = []
                for year, sample in annual:
                    source_init = sample[0].source_init
                    if any(member.source_init != source_init for member in sample):
                        raise AlternativeError("INPUT_CONFLICT", f"{case.case_id}/{year}")
                    hist_start, hist_end = expected_window(source_init, product, case.lead)
                    reference = references[case.case_id][year]
                    if (hist_start, hist_end) != (reference.start, reference.end):
                        raise AlternativeError("INPUT_CONFLICT", f"Historical window: {case.case_id}/{year}")
                    held_out = set(range(start.year, end.year + 1))
                    if hist_end >= case.init or year == start.year or any(
                        hist_start.year <= held <= hist_end.year for held in held_out
                    ):
                        continue
                    response = observed(hist_start, hist_end, variable == "prcp")
                    if response.status != "OK" or response.value is None:
                        continue
                    ensemble = np.asarray([member.value for member in sample], dtype=np.float64)
                    ensemble.setflags(write=False)
                    rows.append(TrainingRow(
                        row_id=f"{case.case_id}/{year}", source_case_id=case.case_id,
                        source_case_init=case.init, source_year=year, source_init=source_init,
                        hist_start=hist_start, hist_end=hist_end, product=target.product,
                        lead=case.lead, variable=target.variable, ensemble=ensemble,
                        observation=response.value, member_keys=tuple(member.key for member in sample),
                        provenance_hash=observation_hash, archive_era=era,
                        source_files=tuple(member.source_file for member in sample),
                    ))
                histories[case.case_id] = tuple(rows)
                history = np.asarray([row.observation for row in rows], dtype=np.float64)
                history.setflags(write=False)
                thresholds = np.asarray(np.quantile(history, [1 / 3, 2 / 3]), dtype=np.float64)
                thresholds.setflags(write=False)
                truths[case.case_id] = ScoreTruth(
                    case_id=case.case_id, observation=actual.value,
                    historical_observations=history, thresholds=thresholds,
                )
            del forecast, historical
    return ExperimentInputs(
        root=root, source=source, cases=tuple(sorted(cases, key=lambda case: case.case_id)),
        historical=MappingProxyType(histories), truths=MappingProxyType(truths),
        excluded_cases=MappingProxyType(excluded), provenance=MappingProxyType(provenance),
        baseline_rows=tuple(csv_rows(root / "outputs/matched_predictions.csv.gz")),
    )
