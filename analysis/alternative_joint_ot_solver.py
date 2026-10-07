"""Balanced Kantorovich plans with exact mass constraints and true-cost receipts."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import linear_sum_assignment, linprog
from scipy.spatial.distance import cdist

from analysis.alternative_contracts import AlternativeError
from analysis.alternative_joint_coordinates import matrix_json, vector_json
from analysis.calibration import FloatArray
from analysis.data_io import Json


@dataclass(frozen=True, slots=True, kw_only=True)
class TransportPlan:
    mass: FloatArray
    source_mass: FloatArray
    target_mass: FloatArray
    cost: float
    row_error: float
    column_error: float
    solver: str
    perturbation_bound: float

    def to_spec(self) -> dict[str, Json]:
        return {
            "mass": matrix_json(self.mass), "source_mass": vector_json(self.source_mass),
            "target_mass": vector_json(self.target_mass), "true_squared_distance_cost": self.cost,
            "row_error": self.row_error, "column_error": self.column_error,
            "solver": self.solver, "tie_perturbation_cost_bound": self.perturbation_bound,
        }


def balanced_plan(
    x: FloatArray, y: FloatArray, a: FloatArray, b: FloatArray, tolerance: float = 1e-9,
) -> TransportPlan:
    """Assignment only for square uniform laws; otherwise full rectangular LP."""
    n, m = np.size(x, axis=0), np.size(y, axis=0)
    cost = cdist(x, y, metric="sqeuclidean")
    if min(n, m) == 0 or not np.isfinite(cost).all():
        raise AlternativeError("INVALID_TRANSPORT_SUPPORT", str((n, m)))
    if a.shape != (n,) or b.shape != (m,) or np.any(a < 0) or np.any(b < 0):
        raise AlternativeError("INVALID_TRANSPORT_MASS", "Nonnegative matching masses required.")
    if abs(float(np.sum(a)) - 1) > tolerance or abs(float(np.sum(b)) - 1) > tolerance:
        raise AlternativeError("UNNORMALIZED_TRANSPORT", "Each empirical law must have mass one.")
    assignment = n == m and np.array_equal(a, np.full(n, 1.0 / n)) and np.array_equal(b, np.full(m, 1.0 / m))
    perturbation = 0.0
    plan: FloatArray
    if assignment:
        rows, columns = linear_sum_assignment(cost)
        optimum = float(np.sum(cost[rows, columns])) / n
        perturbation = tolerance / 16.0
        priorities = np.power(float(n + 1), -np.arange(n, dtype=np.float64))
        tie_cost = priorities[:, None] * np.arange(n)[None, :] / max(1, n)
        _, initial = linear_sum_assignment(cost + perturbation * tie_cost)
        if float(np.sum(cost[np.arange(n), initial])) / n > optimum + tolerance / 8:
            raise AlternativeError("ASSIGNMENT_PERTURBATION_ERROR", "Tie perturbation changed true cost.")
        # Resolve equal-cost choices lexicographically even below floating perturbation resolution.
        available = list(range(n))
        chosen: list[int] = []
        accumulated = 0.0
        for i in range(n):
            accepted = False
            for j in available:
                remaining = [k for k in available if k != j]
                trial = accumulated + cost.item(i, j)
                if remaining:
                    block = cost[i + 1:, remaining]
                    rr, cc = linear_sum_assignment(block)
                    trial += float(np.sum(block[rr, cc]))
                if trial / n <= optimum + tolerance / 16:
                    chosen.append(j)
                    available.remove(j)
                    accumulated += cost.item(i, j)
                    accepted = True
                    break
            if not accepted:
                raise AlternativeError("LEX_ASSIGNMENT_FAILURE", str(i))
        plan = np.zeros((n, m))
        plan[np.arange(n), np.asarray(chosen)] = 1.0 / n
        solver = "linear_sum_assignment; bounded perturbation; lexicographic optimal-face replay"
    else:
        variable = np.arange(n * m)
        constraints = np.zeros((n + m, n * m))
        constraints[np.repeat(np.arange(n), m), variable] = 1.0
        constraints[n + np.tile(np.arange(m), n), variable] = 1.0
        result = linprog(
            cost.ravel(), A_eq=constraints, b_eq=np.concatenate((a, b)),
            bounds=(0, None), method="highs",
            options={"primal_feasibility_tolerance": 1e-10,
                     "dual_feasibility_tolerance": 1e-10},
        )
        if not result.success:
            raise AlternativeError("TRANSPORT_LP_FAILED", str(result.message))
        plan = np.asarray(result.x, dtype=np.float64).reshape(n, m)
        solver = "scipy.optimize.linprog(highs)"
    row_error = float(np.linalg.norm(np.sum(plan, axis=1) - a, ord=np.inf))
    column_error = float(np.linalg.norm(np.sum(plan, axis=0) - b, ord=np.inf))
    if row_error > tolerance or column_error > tolerance or np.any(plan < 0):
        raise AlternativeError("TRANSPORT_PRIMAL_FAILURE", f"{row_error},{column_error}")
    return TransportPlan(
        mass=plan, source_mass=a.copy(), target_mass=b.copy(),
        cost=float(np.sum(plan * cost)), row_error=row_error, column_error=column_error,
        solver=solver, perturbation_bound=perturbation,
    )
