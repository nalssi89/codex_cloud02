"""Independent saved MBC composition replay and balanced-transport oracle."""

from __future__ import annotations

import itertools
import math
from bisect import bisect_right

import numpy as np

from analysis.alternative_validation_io import mapping, number, sequence
from analysis.alternative_validation_oracles import close, floats
from analysis.calibration import FloatArray
from analysis.data_io import Json


def replay(spec: dict[str, Json], point: FloatArray) -> FloatArray:
    """Scalar piecewise-linear replay, independent of all production map classes."""
    current = list(floats(point))
    for item in sequence(spec["steps"]):
        step = mapping(item)
        if step["kind"] == "affine":
            matrix = [[number(v) for v in sequence(row)] for row in sequence(step["matrix"])]
            offset = [number(v) for v in sequence(step["offset"])]
            current = [math.fsum(current[k]*matrix[k][j] for k in range(len(current)))+
                       offset[j] for j in range(len(current))]
        elif step["kind"] == "scalar":
            knots = [[number(v) for v in sequence(row)] for row in sequence(step["knots"])]
            values = [[number(v) for v in sequence(row)] for row in sequence(step["values"])]
            updated: list[float] = []
            for x, nodes, outputs in zip(current, knots, values, strict=True):
                if x <= nodes[0]:
                    updated.append(outputs[0])
                elif x >= nodes[-1]:
                    updated.append(outputs[-1])
                else:
                    right = bisect_right(nodes, x)
                    left = right-1
                    fraction = (x-nodes[left])/(nodes[right]-nodes[left])
                    updated.append(outputs[left]+fraction*(outputs[right]-outputs[left]))
            current = updated
        else:
            raise AssertionError("unknown saved MBC operation")
    return np.array(current, dtype=np.float64)


def mbc_checks() -> dict[str, Json]:
    from analysis.alternative_joint_mbc import fit_map, map_from_spec

    x = np.array([[i/5, (i % 5)/4] for i in range(24)], dtype=np.float64)
    y = np.column_stack((x[:, 0]*1.2+x[:, 1], np.sin(x[:, 0])+x[:, 1]*2))
    probes: FloatArray = np.array([[-1., .2], [1.4, .8], [6., 2.]], dtype=np.float64)
    results: dict[str, Json] = {"status": "PASS"}
    for method in ("mbcp_annual", "mbcr_annual", "mbcn_annual"):
        fitted = fit_map(method, x, y, 20261007)
        spec = fitted.to_spec()
        restored = map_from_spec(spec)
        independent = np.stack([replay(spec, probes[i:i+1].reshape(-1))
                                for i in range(len(probes))])
        np.testing.assert_allclose(fitted.apply(probes), independent, atol=2e-10, rtol=2e-10)
        np.testing.assert_allclose(restored.apply(probes), independent, atol=2e-10, rtol=2e-10)
        results[method] = {"status": "PASS", "saved_steps": len(sequence(spec["steps"])),
                           "out_of_sample_probes": 3}
    return results


def transport_matrix_checks(plan: FloatArray, x: FloatArray, y: FloatArray,
                            expected: float) -> None:
    n, m = np.size(plan, axis=0), np.size(plan, axis=1)
    if np.any(plan < -1e-12):
        raise AssertionError("negative balanced transport mass")
    np.testing.assert_allclose(plan.sum(axis=1), np.full(n, 1/n), atol=1e-9, rtol=0)
    np.testing.assert_allclose(plan.sum(axis=0), np.full(m, 1/m), atol=1e-9, rtol=0)
    cost = np.sum((x[:, None, :]-y[None, :, :])**2, axis=2)
    close(float(np.sum(cost*plan)), expected, "true squared-distance OT objective",
          atol=1e-9, rtol=1e-9)


def assignment_reference(x: FloatArray, y: FloatArray) -> float:
    """Exhaustive four-vector oracle, not the production assignment solver."""
    n = len(x)
    return min(math.fsum(float(np.sum((x[i:i+1]-y[j:j+1])**2)) for i, j in enumerate(order))/n
               for order in itertools.permutations(range(n)))


def ot_checks() -> dict[str, Json]:
    from analysis.alternative_joint_ot import fit_ot, transport_from_spec
    from analysis.alternative_joint_ot_solver import balanced_plan

    x = np.array([[0., 0.], [1., 2.], [3., 1.], [4., 4.]], dtype=np.float64)
    y = np.array([[2., 1.], [5., 3.], [0., 2.], [1., 0.]], dtype=np.float64)
    stationary = fit_ot("otc_annual", x, y, (1990, 1991, 1992, 1993), ())
    expected = assignment_reference(x, y)
    transport_matrix_checks(stationary.plan, x, y, expected)
    support, weights = stationary.predict(np.array([0., 0.]))
    close(float(np.sum(weights)), 1, "OT nearest-three mass", atol=1e-12)
    restored = transport_from_spec(stationary.to_spec())
    replay_support, replay_weights = restored.predict(np.array([0., 0.]))
    np.testing.assert_allclose(replay_support, support, atol=1e-12)
    np.testing.assert_allclose(replay_weights, weights, atol=1e-12)
    selected = sorted(range(4), key=lambda i: (
        float(np.sum((x[i:i+1]-np.array([[0., 0.]]))**2)), 1990+i))[:3]
    conditional = np.sum(stationary.plan[selected], axis=0)*(4/3)
    np.testing.assert_allclose(weights, conditional[conditional > 0], atol=1e-12)
    rectangular = balanced_plan(np.array([[0.], [2.]]), np.array([[0.], [1.], [3.]]),
                                np.array([.4, .6]), np.array([.2, .5, .3]))
    # Exact monotone one-dimensional coupling, independent of any LP solver.
    np.testing.assert_allclose(rectangular.mass, np.array([[.2, .2, 0.], [0., .3, .3]]),
                               atol=1e-10, rtol=0)
    close(rectangular.cost, .8, "rectangular true OT cost", atol=1e-10)
    historical_x = np.arange(21, dtype=np.float64).reshape(-1, 1)
    historical_y = historical_x+2
    historical_years = tuple(range(1990, 2011))
    dynamic = fit_ot("dotc_annual", historical_x, historical_y, historical_years, ())
    changed_recent_y = historical_y.copy()
    changed_recent_y[10:] = 1e12
    unchanged = fit_ot("dotc_annual", historical_x, changed_recent_y, historical_years, ())
    if dynamic.to_spec() != unchanged.to_spec():
        raise AssertionError("recent observations contaminated dynamic evolved-target construction")
    receipts = dynamic.to_spec()["receipts"]
    receipt = mapping(receipts)
    if receipt["recent_observations_used"] is not False:
        raise AssertionError("dynamic transfer does not disclose unused recent observations")
    if receipt["reference_years"] != list(range(1990, 2000)):
        raise AssertionError("dynamic reference block is not earliest historical half")
    if receipt["evolved_years"] != list(range(2000, 2011)):
        raise AssertionError("dynamic evolved block is not later historical half")
    close(number(receipt["composition_mass"]), 1, "dynamic full path mass")
    np.testing.assert_allclose(dynamic.support, historical_x[10:]+2, atol=1e-10)
    transport_matrix_checks(dynamic.plan, historical_x[10:], dynamic.support, 4.)
    # Pairing-blindness is observable even with a reversed conditional relationship.
    simple = np.arange(3, dtype=np.float64).reshape(-1, 1)
    reversed_pair = fit_ot("otc_annual", simple, simple[::-1], (1990, 1991, 1992), ())
    close(float(np.sum(reversed_pair.plan*np.square(
        simple[:, None, :]-simple[::-1][None, :, :]).sum(axis=2))), 0.,
        "pairing-blind identical marginal law")
    return {"status": "PASS", "brute_force_assignment_cost": expected,
            "rectangular_cost": rectangular.cost, "dynamic_final_cost": 4.,
            "dynamic_reference_years": receipt["reference_years"],
            "dynamic_evolved_years": receipt["evolved_years"],
            "recent_observation_perturbation": "BYTE_IDENTICAL",
            "pairing_blind_counterexample": "PASS"}
