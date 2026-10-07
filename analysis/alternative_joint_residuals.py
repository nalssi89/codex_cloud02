"""Entire-map prequential errors and four fixed atom-randomized PIT collections."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from scipy.special import ndtri

from analysis.alternative_contracts import (
    AlternativeError,
    FitConfig,
    FittedModel,
    FoldSpec,
    JointTrainingSet,
    ResidualSet,
    TrainingSet,
)
from analysis.alternative_joint_coordinates import (
    correlation,
    fixed_seed,
    forward,
    matrix_json,
    rain_columns,
)
from analysis.alternative_joint_folds import component_training, prequential_folds
from analysis.alternative_joint_marginals import fit_emos_marginal
from analysis.alternative_joint_mbc import fit_map
from analysis.calibration import FloatArray
from analysis.data_io import Json

type MarginalFitter = Callable[[TrainingSet, FitConfig], FittedModel]


@dataclass(frozen=True, slots=True, kw_only=True)
class PITResidualSet(ResidualSet):
    """Uniforms and ALL four diagnostic repetitions survive into model serialization."""

    uniform_repeats: tuple[FloatArray, ...]
    normal_score_repeats: tuple[FloatArray, ...]
    clipping_counts: tuple[int, ...]
    chosen_randomization: int
    marginal_method: str

    def diagnostics(self) -> dict[str, Json]:
        return {
            "atom_uniforms_four": [matrix_json(a) for a in self.uniform_repeats],
            "normal_scores_four": [matrix_json(a) for a in self.normal_score_repeats],
            "correlation_four": [matrix_json(correlation(a)) for a in self.normal_score_repeats],
            "clip_counts_four": list(self.clipping_counts),
            "selected_randomization_fixed": self.chosen_randomization,
            "marginal_method": self.marginal_method,
        }


def generate_residuals(
    training: JointTrainingSet, config: FitConfig, *, method_id: str,
    marginal_fitter: MarginalFitter | None = None, randomization: int = 0,
    marginal_method: str = "emos",
) -> ResidualSet:
    """Fit every eligible >=10-year ancestor; NEVER reuse the full-sample model.

    A caller can pass a fixed BJP fitter to produce a separately named copula.
    MBC algorithms ignore marginal_fitter and refit the ENTIRE mapping in each fold.
    The known-input catalog cutoff stays at actual outer issuance in every fold.
    """
    if randomization not in range(4):
        raise AlternativeError("INVALID_PIT_RANDOMIZATION", "Expected fixed index 0..3.")
    years: list[int] = []
    refs: list[FoldSpec] = []
    errors: list[FloatArray] = []
    uniforms: list[list[FloatArray]] = [[], [], [], []]
    normal_scores: list[list[FloatArray]] = [[], [], [], []]
    clips = [0, 0, 0, 0]
    rain = rain_columns(training.targets)
    fitter = marginal_fitter or fit_emos_marginal
    for year, past, fold in prequential_folds(training):
        rows = training.rows_by_year[year]
        raw = np.asarray([float(np.mean(row.ensemble)) for row in rows])
        observed = np.asarray([row.observation for row in rows])
        match method_id:
            case "mbcp_annual" | "mbcr_annual" | "mbcn_annual":
                mapping = fit_map(method_id, forward(past.forecast_means, rain),
                                  forward(past.observations, rain), config.seed)
                errors.append(forward(observed, rain) - mapping.apply(forward(raw, rain)))
            case "decc_path_shrunk_error":
                errors.append(observed - raw)
            case "residual_gaussian_copula":
                bounds = np.empty((len(rows), 2), dtype=np.float64)
                for j, row in enumerate(rows):
                    scalar_training = component_training(past, j)
                    law = fitter(scalar_training, config).predict(scalar_training.target)
                    value = np.asarray([row.observation], dtype=np.float64)
                    bounds[j] = (law.cdf_left(value).item(0), law.cdf(value).item(0))
                if np.any(bounds < 0) or np.any(bounds > 1) or np.any(bounds[:, 1] < bounds[:, 0]):
                    raise AlternativeError("INVALID_PIT_BOUNDS", fold.fold_id)
                for repeat in range(4):
                    uniform = np.asarray([
                        np.random.default_rng(fixed_seed(
                            config.seed, "atom-PIT", str(repeat), row.row_id,
                            training.component_keys[j],
                        )).uniform() for j, row in enumerate(rows)
                    ])
                    pit = bounds[:, 0] + uniform * (bounds[:, 1] - bounds[:, 0])
                    clips[repeat] += int(np.count_nonzero((pit < 1e-12) | (pit > 1.0 - 1e-12)))
                    uniforms[repeat].append(uniform)
                    normal_scores[repeat].append(ndtri(np.clip(pit, 1e-12, 1.0 - 1e-12)))
            case _:
                raise AlternativeError("UNSUPPORTED_RESIDUAL_METHOD", method_id)
        years.append(year)
        refs.append(fold)
    if len(years) < 8:
        raise AlternativeError("INSUFFICIENT_RESIDUAL_YEARS", str(len(years)))
    weights = np.full(len(years), 1.0 / len(years))
    if method_id == "residual_gaussian_copula":
        matrices = tuple(np.asarray(values) for values in normal_scores)
        return PITResidualSet(
            component_keys=training.component_keys, years=tuple(years),
            residual_matrix=matrices[randomization], weights=weights, fold_refs=tuple(refs),
            kind="pit_normal", uniform_repeats=tuple(np.asarray(values) for values in uniforms),
            normal_score_repeats=matrices, clipping_counts=tuple(clips),
            chosen_randomization=randomization, marginal_method=marginal_method,
        )
    return ResidualSet(
        component_keys=training.component_keys, years=tuple(years),
        residual_matrix=np.asarray(errors), weights=weights, fold_refs=tuple(refs),
        kind="latent_error",
    )


def residual_spec(residuals: ResidualSet) -> dict[str, Json]:
    result: dict[str, Json] = {
        "kind": residuals.kind, "years": list(residuals.years),
        "matrix": matrix_json(residuals.residual_matrix),
        "folds": [{
            "fold_id": f.fold_id, "ancestor_hash": f.ancestor_hash,
            "pseudo_init": f.pseudo_init.isoformat(), "held_out_years": list(f.held_out_years),
            "training_row_ids": list(f.training_row_ids),
            "validation_row_ids": list(f.validation_row_ids),
        } for f in residuals.fold_refs],
    }
    if isinstance(residuals, PITResidualSet):
        result["pit_diagnostics"] = residuals.diagnostics()
    return result
