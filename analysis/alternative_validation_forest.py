"""Independent forest leaf-mixture and year-bootstrap membership reconstruction."""

from __future__ import annotations

from collections import Counter

import numpy as np

from analysis.alternative_validation_io import mapping, number, sequence
from analysis.alternative_validation_reference import vector
from analysis.calibration import FloatArray
from analysis.data_io import Json


def forest_weights(spec: dict[str, Json], features: FloatArray) -> FloatArray:
    years = [int(number(year)) for year in sequence(spec["source_years"])]
    observations = vector(spec["observations"])
    year_counts = Counter(years)
    trees = sequence(spec["trees"])
    if len(trees) != 64 or spec["bootstrap_unit"] != "source_year":
        raise AssertionError("forest is not the declared 64 year-block trees")
    weights = np.zeros(len(observations), dtype=np.float64)
    for item in trees:
        tree = mapping(item)
        bootstrap: dict[int, int] = {}
        for pair in sequence(tree["bootstrap_year_counts"]):
            year, count = sequence(pair)
            bootstrap[int(number(year))] = int(number(count))
        if (sum(bootstrap.values()) != len(year_counts) or min(bootstrap.values()) < 0
                or not bootstrap.keys() <= year_counts.keys()):
            raise AssertionError("tree bootstrap is not a sample of whole source years")
        def visit(node: dict[str, Json], depth: int, counts: dict[int, int] = bootstrap) -> None:
            if depth > 4:
                raise AssertionError("forest exceeded fixed depth")
            if "feature" in node:
                visit(mapping(node["left"]), depth+1, counts)
                visit(mapping(node["right"]), depth+1, counts)
                return
            indices = [int(number(i)) for i in sequence(node["indices"])]
            masses = vector(node["masses"])
            if len(indices) != len(set(indices)) or len(indices) != len(masses):
                raise AssertionError("leaf duplicates rows or mismatches response masses")
            if any(i < 0 or i >= len(years) or counts.get(years[i], 0) <= 0 for i in indices):
                raise AssertionError("leaf contains a row outside its year bootstrap")
            if depth and len({years[i] for i in indices}) < 5:
                raise AssertionError("leaf has fewer than five source-year blocks")
            expected: FloatArray = np.array(
                [counts[years[i]]/year_counts[years[i]] for i in indices], dtype=np.float64)
            expected = expected/float(np.sum(expected))
            np.testing.assert_allclose(masses, expected, atol=1e-12, rtol=1e-12)
        visit(tree, 0)
        node = tree
        while "feature" in node:
            column = int(number(node["feature"]))
            side = "left" if float(features.take(column)) <= number(node["threshold"]) else "right"
            node = mapping(node[side])
        indices = np.array([int(number(i)) for i in sequence(node["indices"])], dtype=np.int64)
        np.add.at(weights, indices, vector(node["masses"])/64)
    if abs(float(np.sum(weights))-1) > 1e-12:
        raise AssertionError("reconstructed forest mixture has missing mass")
    return weights
