"""Deterministic annual fixtures with truth confined to historical TrainingRows."""

from __future__ import annotations

from datetime import date, timedelta
from types import MappingProxyType

import numpy as np

from analysis.alternative_contracts import (
    CaseInput,
    JointTrainingSet,
    MethodSpec,
    TrainingRow,
)


def fixture(dimension: int = 2, n: int = 24) -> JointTrainingSet:
    rng = np.random.default_rng(913)
    init = date(2022, 3, 1)
    years = tuple(range(1993, 1993 + n))
    targets: list[CaseInput] = []
    columns: list[list[TrainingRow]] = []
    latent = rng.normal(size=(n, dimension))
    latent[:, 1:] += 0.4 * latent[:, :1]
    for j in range(dimension):
        rain = j >= dimension // 2
        lead = str(j % (dimension // 2) + 1)
        offset = timedelta(days=7 * int(lead))
        variable = "prcp" if rain else "t15m"
        case_id = f"synthetic:{variable}:{lead}"
        issued = np.asarray([20.0, 15.0, 25.0]) if rain else np.asarray([10.0, 11.0, 12.0])
        targets.append(CaseInput(
            case_id=case_id, init=init, valid_start=init + offset,
            valid_end=init + offset + timedelta(days=6), product="1mon", lead=lead,
            variable=variable, members=issued, member_keys=("a", "b", "c"),
            provenance_hash="synthetic-known-inputs", archive_era="3members",
        ))
        rows: list[TrainingRow] = []
        for i, year in enumerate(years):
            historical_init = date(year, 3, 1)
            predictor = float(10.0 + 2.0 * latent.item(i, j))
            response = float(11.0 + latent.item(i, j) + rng.normal())
            if rain:
                predictor = float(20.0 + 4.0 * latent.item(i, j))
                response = 0.0 if i % 5 == 0 else float(30.0 + 6.0 * latent.item(i, j))
            rows.append(TrainingRow(
                row_id=f"{case_id}:{year}", source_case_id=case_id, source_case_init=init,
                source_year=year, source_init=historical_init,
                hist_start=historical_init + offset,
                hist_end=historical_init + offset + timedelta(days=6),
                product="1mon", lead=lead, variable=variable,
                ensemble=np.asarray([predictor - 1.0, predictor, predictor + 1.0]),
                observation=response, member_keys=("a", "b", "c"),
                provenance_hash="synthetic-original-catalog", archive_era="3members",
            ))
        columns.append(rows)
    by_year = {year: tuple(column[i] for column in columns) for i, year in enumerate(years)}
    return JointTrainingSet(
        targets=tuple(targets), component_keys=tuple(t.case_id for t in targets),
        rows_by_year=MappingProxyType(by_year), source_years=years,
        historical_initializations=tuple(by_year[y][0].source_init for y in years),
        historical_windows=tuple(
            tuple((r.hist_start, r.hist_end) for r in by_year[y]) for y in years
        ),
        forecast_means=np.asarray([[float(np.mean(r.ensemble)) for r in by_year[y]] for y in years]),
        observations=np.asarray([[r.observation for r in by_year[y]] for y in years]),
        cutoff=init, catalog_cutoff=init, held_out_years=(2022,), train_hash=f"fixture-{dimension}-{n}",
    )


def method(method_id: str, marginal_method: str = "emos") -> MethodSpec:
    return MethodSpec(
        id=method_id, family_no=15 if method_id in (
            "schaake_window", "schaake_block", "ecc_q", "decc_path_shrunk_error",
            "residual_gaussian_copula",
        ) else 16,
        subtype=method_id, domain="both", surface="joint", fit_scope="joint",
        algorithm_version="section8-v1", owner="joint",
        fixed_parameters={"marginal_method": marginal_method},
    )
