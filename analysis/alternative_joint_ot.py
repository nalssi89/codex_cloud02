"""Conditional annual OTC and full historical-block dynamic OT composition."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

import numpy as np

from analysis.alternative_contracts import AlternativeError
from analysis.alternative_joint_coordinates import (
    matrix_json,
    parse_vector,
    parse_vectors,
    vector_json,
)
from analysis.alternative_joint_ot_solver import balanced_plan
from analysis.calibration import FloatArray
from analysis.data_io import Json


@dataclass(frozen=True, slots=True, kw_only=True)
class FrozenTransport:
    method_id: str
    source: FloatArray
    support: FloatArray
    plan: FloatArray
    source_mass: FloatArray
    target_mass: FloatArray
    source_years: tuple[int, ...]
    receipts: Mapping[str, Json]

    def predict(self, x: FloatArray) -> tuple[FloatArray, FloatArray]:
        distance = np.sum((self.source - x) ** 2, axis=1)
        selected = sorted(
            range(len(self.source_years)),
            key=lambda i: (distance.item(i), self.source_years[i]),
        )[:3]
        weights = np.mean(self.plan[selected] / self.source_mass[selected, None], axis=0)
        if np.any(weights < 0) or abs(float(np.sum(weights)) - 1) > 1e-9:
            raise AlternativeError("CONDITIONAL_OT_MASS_ERROR", self.method_id)
        keep = weights > 0
        return self.support[keep].copy(), weights[keep]

    def to_spec(self) -> dict[str, Json]:
        return {
            "type": "frozen_annual_transport", "method_id": self.method_id,
            "source": matrix_json(self.source), "support": matrix_json(self.support),
            "plan": matrix_json(self.plan), "source_mass": vector_json(self.source_mass),
            "target_mass": vector_json(self.target_mass), "source_years": list(self.source_years),
            "receipts": dict(self.receipts),
        }


def fit_ot(
    method_id: str, x: FloatArray, y: FloatArray, years: tuple[int, ...],
    rain_indices: tuple[int, ...], tolerance: float = 1e-9,
) -> FrozenTransport:
    """Full plans, including final evolved-source -> synthetic-target balancing."""
    if x.shape != y.shape or len(years) != np.size(x, axis=0) or len(set(years)) != len(years):
        raise AlternativeError("INVALID_OT_TRAINING", str(x.shape))
    if len(years) < 3:
        raise AlternativeError("INSUFFICIENT_OT_YEARS", str(len(years)))
    def year_key(i: int) -> int:
        return years[i]

    order = np.asarray(sorted(range(len(years)), key=year_key), dtype=np.int64)
    source: FloatArray = x[order]
    observed: FloatArray = y[order]
    ordered_years = tuple(sorted(years))
    masses: FloatArray = np.full(len(years), 1.0 / len(years), dtype=np.float64)
    match method_id:
        case "otc_annual":
            plan = balanced_plan(source, observed, masses, masses, tolerance)
            return FrozenTransport(
                method_id=method_id, source=source, support=observed, plan=plan.mass,
                source_mass=masses, target_mass=masses, source_years=ordered_years,
                receipts={"stationary_plan": plan.to_spec(), "pairing_blind": True},
            )
        case "dotc_annual":
            if len(years) < 20:
                raise AlternativeError("G6_INSUFFICIENT_BLOCK_YEARS", str(len(years)))
            n0 = len(years) // 2
            x0: FloatArray = source[:n0]
            x1: FloatArray = source[n0:]
            y0: FloatArray = observed[:n0]
            a: FloatArray = np.full(n0, 1.0 / n0, dtype=np.float64)
            b: FloatArray = np.full(len(years) - n0, 1.0 / (len(years) - n0), dtype=np.float64)
            correction = balanced_plan(y0, x0, a, a, tolerance)
            evolution = balanced_plan(x0, x1, a, b, tolerance)
            atoms: list[FloatArray] = []
            weights: list[float] = []
            paths: list[Json] = []
            projected_mass = 0.0
            for j in range(n0):
                for i in range(n0):
                    for k in range(len(years) - n0):
                        mass = correction.mass.item(j, i) * evolution.mass.item(i, k) / a.item(i)
                        if mass <= 0:
                            continue
                        value = (y0[j:j + 1] + x1[k:k + 1] - x0[i:i + 1]).ravel()
                        if rain_indices and np.any(value[list(rain_indices)] < 0):
                            projected_mass += mass
                        for column in rain_indices:
                            value[column] = max(0.0, value.item(column))
                        atoms.append(value)
                        weights.append(mass)
                        paths.append({
                            "observation_year": ordered_years[j],
                            "reference_source_year": ordered_years[i],
                            "evolved_source_year": ordered_years[n0 + k], "mass": mass,
                        })
            synthetic, inverse = np.unique(np.asarray(atoms), axis=0, return_inverse=True)
            omega = np.bincount(inverse, weights=np.asarray(weights), minlength=np.size(synthetic, axis=0))
            if abs(float(np.sum(omega)) - 1) > tolerance:
                raise AlternativeError("DOTC_COMPOSITION_MASS_ERROR", str(np.sum(omega)))
            final = balanced_plan(x1, synthetic, b, omega, tolerance)
            return FrozenTransport(
                method_id=method_id, source=x1, support=synthetic, plan=final.mass,
                source_mass=b, target_mass=omega, source_years=ordered_years[n0:],
                receipts={
                    "reference_years": list(ordered_years[:n0]),
                    "evolved_years": list(ordered_years[n0:]),
                    "correction_plan_P": correction.to_spec(),
                    "evolution_plan_R": evolution.to_spec(), "final_plan_S": final.to_spec(),
                    "full_composition_paths": paths, "composition_mass": float(np.sum(omega)),
                    "projected_rain_probability_mass": projected_mass,
                    "recent_observations_used": False, "pairing_blind": True,
                },
            )
        case _:
            raise AlternativeError("UNKNOWN_OT_METHOD", method_id)


def transport_from_spec(spec: Mapping[str, Json]) -> FrozenTransport:
    method, years, receipts = spec["method_id"], spec["source_years"], spec["receipts"]
    if not isinstance(method, str) or not isinstance(years, list) or not isinstance(receipts, dict):
        raise AlternativeError("INVALID_TRANSPORT_SPEC", "Method/years/receipts malformed.")
    parsed_years: list[int] = []
    for year in years:
        if not isinstance(year, int):
            raise AlternativeError("INVALID_TRANSPORT_SPEC", "Year must be an integer.")
        parsed_years.append(year)
    return FrozenTransport(
        method_id=method, source=np.asarray(parse_vectors(spec["source"])),
        support=np.asarray(parse_vectors(spec["support"])), plan=np.asarray(parse_vectors(spec["plan"])),
        source_mass=parse_vector(spec["source_mass"]), target_mass=parse_vector(spec["target_mass"]),
        source_years=tuple(parsed_years), receipts=receipts,
    )
