"""Independent balanced-transport oracles, including odd blocks and full composition."""

from __future__ import annotations

import itertools

import numpy as np

from analysis.alternative_joint_audit_data import fixture
from analysis.alternative_joint_coordinates import forward
from analysis.alternative_joint_ot import fit_ot, transport_from_spec
from analysis.alternative_joint_ot_solver import balanced_plan
from analysis.data_io import Json


def run() -> dict[str, Json]:
    masses = np.full(2, 0.5)
    simple = balanced_plan(np.asarray([[0.0], [1.0]]), np.asarray([[1.0], [3.0]]), masses, masses)
    assert simple.cost == 2.5, "True unperturbed assignment cost is wrong."
    assert np.array_equal(simple.mass, np.diag(masses))
    tied = balanced_plan(np.zeros((4, 2)), np.zeros((4, 2)), np.full(4, 0.25), np.full(4, 0.25))
    assert np.array_equal(tied.mass, np.eye(4) / 4), "Exact ties are not lexicographic."
    rng = np.random.default_rng(723)
    x, y = rng.normal(size=(5, 2)), rng.normal(size=(5, 2))
    known_cost = min(float(np.mean(np.sum((x - y[list(p)]) ** 2, axis=1)))
                     for p in itertools.permutations(range(5)))
    optimum = balanced_plan(x, y, np.full(5, 0.2), np.full(5, 0.2))
    assert abs(optimum.cost - known_cost) < 1e-10
    rectangular = balanced_plan(x[:2], y[:3], np.asarray([0.3, 0.7]), np.asarray([0.2, 0.5, 0.3]))
    assert np.max(np.abs(np.sum(rectangular.mass, axis=1) - [0.3, 0.7])) < 1e-12
    assert np.max(np.abs(np.sum(rectangular.mass, axis=0) - [0.2, 0.5, 0.3])) < 1e-12
    source = np.arange(5.0)[:, None]
    nearest = fit_ot("otc_annual", source, source + 10, tuple(range(2000, 2005)), ())
    support, weights = nearest.predict(np.asarray([0.0]))
    assert np.array_equal(support[:, 0], np.asarray([10.0, 11.0, 12.0]))
    assert np.allclose(weights, 1.0 / 3.0, atol=0, rtol=0), "Exact match must still mix nearest three."
    blind = fit_ot("otc_annual", source, source[::-1], tuple(range(2000, 2005)), ())
    matched = fit_ot("otc_annual", source, source, tuple(range(2000, 2005)), ())
    bs, bw = blind.predict(np.asarray([0.0]))
    ms, mw = matched.predict(np.asarray([0.0]))
    assert np.array_equal(np.sort(bs[:, 0]), np.sort(ms[:, 0])) and np.array_equal(bw, mw)
    block_receipts: list[Json] = []
    for n in (24, 25):
        training = fixture(n=n)
        x = forward(training.forecast_means, (1,))
        y = forward(training.observations, (1,))
        dynamic = fit_ot("dotc_annual", x, y, training.source_years, (1,))
        altered = y.copy()
        altered[n // 2:] += 1e6
        no_recent = fit_ot("dotc_annual", x, altered, training.source_years, (1,))
        assert np.array_equal(dynamic.plan, no_recent.plan), "Recent observations leaked into dOTC."
        assert np.array_equal(dynamic.support, no_recent.support)
        replay = transport_from_spec(dynamic.to_spec())
        ds, dw = dynamic.predict(np.asarray([10.2, 0.35]))
        rs, rw = replay.predict(np.asarray([10.2, 0.35]))
        assert np.array_equal(ds, rs) and np.array_equal(dw, rw)
        assert abs(float(np.sum(dynamic.target_mass)) - 1) < 1e-12
        assert np.max(np.abs(np.sum(dynamic.plan, axis=0) - dynamic.target_mass)) < 1e-9
        assert np.max(np.abs(np.sum(dynamic.plan, axis=1) - dynamic.source_mass)) < 1e-9
        assert np.all(dynamic.support[:, 1] >= 0)
        block_receipts.append({
            "years": n, "support_atoms": np.size(dynamic.support, axis=0),
            "mass": float(np.sum(dynamic.target_mass)),
            "final_row_error": float(np.linalg.norm(np.sum(dynamic.plan, axis=1) - dynamic.source_mass, np.inf)),
            "final_column_error": float(np.linalg.norm(np.sum(dynamic.plan, axis=0) - dynamic.target_mass, np.inf)),
            "recent_observation_sentinel": "IDENTICAL",
        })
    collapse_x = np.zeros((24, 2))
    collapse_x[:12, 1] = 3.0
    projected = fit_ot("dotc_annual", collapse_x, np.zeros((24, 2)), tuple(range(1993, 2017)), (1,))
    assert projected.receipts["projected_rain_probability_mass"] == 1.0
    assert np.size(projected.support, axis=0) == 1, "Duplicate projected atoms were not merged."
    assert abs(projected.target_mass.item(0) - 1) < 1e-12
    return {
        "known_assignment_cost": simple.cost, "permutation_oracle_cost": known_cost,
        "rectangular_nonuniform_constraints": "PASS", "exact_tie_lexicographic": "PASS",
        "nearest_three_at_exact_match": "PASS", "pairing_blind_counterexample": "PASS",
        "historical_block_compositions": block_receipts,
        "projection_and_duplicate_mass": "PASS", "frozen_transport_replay": "PASS",
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2))
