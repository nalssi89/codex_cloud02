"""Frozen predictive joint laws, keeping analytic marginals separate from scenarios."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from types import MappingProxyType

import numpy as np

from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FitConfig,
    JointPrediction,
    PredictiveDistribution,
    ResidualSet,
)
from analysis.alternative_joint_coordinates import (
    forward,
    inverse,
    matrix_json,
    vector_json,
)
from analysis.alternative_joint_coupling import (
    dual_ecc,
    gaussian_copula,
    physical_template,
    rank_couple,
)
from analysis.alternative_joint_mbc import FrozenMap
from analysis.alternative_joint_ot import FrozenTransport
from analysis.alternative_joint_residuals import residual_spec
from analysis.calibration import FloatArray
from analysis.data_io import Json


@dataclass(frozen=True, slots=True, kw_only=True)
class AnnualJointModel:
    """One entire-year scenario law; componentwise draws are never substituted."""

    method_id: str
    algorithm: str
    marginal_method: str
    train_hash: str
    signature: tuple[tuple[str, str, str], ...]
    source_years: tuple[int, ...]
    rain: tuple[int, ...]
    observed_template: FloatArray
    training_mean: FloatArray
    training_scale: FloatArray
    residuals: ResidualSet | None = None
    dependence: FloatArray | None = None
    mapping: FrozenMap | None = None
    transport: FrozenTransport | None = None

    def predict(
        self, targets: tuple[CaseInput, ...],
        marginals: tuple[PredictiveDistribution, ...], config: FitConfig,
    ) -> JointPrediction:
        if tuple((t.product, t.variable, t.lead) for t in targets) != self.signature:
            raise AlternativeError("PREDICTION_COMPONENT_MISMATCH", "Product/variable/lead order changed.")
        coupling = self.algorithm in (
            "schaake_window", "schaake_block", "ecc_q", "decc_path_shrunk_error",
            "residual_gaussian_copula",
        )
        if coupling and len(marginals) != len(targets):
            raise AlternativeError("MISSING_FIXED_MARGINALS", self.marginal_method)
        metadata: dict[str, Json] = {
            "algorithm": self.algorithm, "coordinate_system": "T_degC,sqrt(P_mm/100)",
            "score_training_mean": vector_json(self.training_mean),
            "score_training_scale": vector_json(self.training_scale),
            "source_years": list(self.source_years),
            "full_dimension": len(targets),
            "partial_horizons": "dimension-matched supplied components; no horizon discarded",
        }
        weights: FloatArray | None = None
        match self.algorithm:
            case "schaake_window" | "schaake_block":
                keys = tuple(str(year) for year in self.source_years)
                samples = rank_couple(self.observed_template, marginals, keys, config.seed)
                metadata["scenario_ancestry_years"] = list(self.source_years)
                metadata["alias"] = (
                    "schaake_window" if self.algorithm == "schaake_block"
                    and len({target.lead for target in targets}) == 1 else None
                )
                metadata["whole_year_template"] = True
            case "ecc_q" | "decc_path_shrunk_error":
                raw, keys, details = physical_template(targets)
                metadata.update(details)
                if self.algorithm == "ecc_q":
                    samples = rank_couple(raw, marginals, keys, config.seed)
                else:
                    if self.dependence is None:
                        raise AlternativeError("MISSING_DECC_CORRELATION", self.train_hash)
                    samples = dual_ecc(raw, marginals, keys, self.dependence,
                                       self.training_scale, config.seed)
            case "residual_gaussian_copula":
                if self.dependence is None:
                    raise AlternativeError("MISSING_COPULA_CORRELATION", self.train_hash)
                samples = gaussian_copula(self.dependence, marginals, config.seed)
                sensitivity = gaussian_copula(self.dependence, marginals, config.seed, 512)
                metadata["sobol_512_mean_minus_256"] = vector_json(
                    np.mean(sensitivity, axis=0) - np.mean(samples, axis=0)
                )
                metadata["sobol_512_quantile_minus_256"] = matrix_json(
                    np.quantile(sensitivity, [0.05, 0.5, 0.95], axis=0)
                    - np.quantile(samples, [0.05, 0.5, 0.95], axis=0)
                )
                metadata["scenario_count_sensitivity"] = 512
            case "mbcp_annual" | "mbcr_annual" | "mbcn_annual":
                if self.mapping is None or self.residuals is None:
                    raise AlternativeError("MISSING_DRESSED_MAP", self.train_hash)
                raw_mean = np.asarray([float(np.mean(t.members)) for t in targets])
                center = self.mapping.apply(forward(raw_mean, self.rain))
                latent = center + self.residuals.residual_matrix
                samples = inverse(latent, self.rain)
                weights = self.residuals.weights.copy()
                metadata["scenario_ancestry_years"] = list(self.residuals.years)
                metadata["residual_dressing"] = "entire past-only map; whole vector; no recentering"
                metadata["tail_support"] = "finite prequential residual support, not analytic EMOS"
                metadata["rain_projection_mass"] = float(np.mean(
                    np.any(latent[:, self.rain] < 0, axis=1)
                )) if self.rain else 0.0
            case "otc_annual" | "dotc_annual":
                if self.transport is None:
                    raise AlternativeError("MISSING_TRANSPORT", self.train_hash)
                raw_mean = np.asarray([float(np.mean(t.members)) for t in targets])
                support, weights = self.transport.predict(forward(raw_mean, self.rain))
                samples = inverse(support, self.rain)
                metadata["conditional_transport"] = "uniform nearest-three conditional plan rows"
                metadata["tail_support"] = (
                    "bounded observed vectors" if self.algorithm == "otc_annual"
                    else "finite synthetic evolved vectors; may exceed observed support"
                )
                metadata["climate_claim"] = "historical annual predictive adaptation, not future climate proof"
            case _:
                raise AlternativeError("UNKNOWN_JOINT_METHOD", self.algorithm)
        if weights is None:
            weights = np.full(np.size(samples, axis=0), 1.0 / np.size(samples, axis=0))
        if not np.isfinite(samples).all() or np.any(weights < 0) or abs(float(np.sum(weights)) - 1) > 1e-9:
            raise AlternativeError("INVALID_JOINT_SCENARIO_LAW", self.train_hash)
        ids = tuple(target.case_id for target in targets)
        marginal_refs: tuple[str, ...] = ()
        if coupling:
            metadata["marginal_method"] = self.marginal_method
            metadata["analytic_marginals_preserved"] = False
            metadata["finite_quantile_multisets_preserved"] = self.algorithm != "residual_gaussian_copula"
            metadata["continuous_marginal_scores"] = "use original analytic laws, not scenario CRPS"
            metadata["scenario_mean_minus_analytic"] = vector_json(
                np.sum(weights[:, None] * samples, axis=0)
                - np.asarray([m.mean() for m in marginals])
            )
            marginal_refs = tuple(f"{self.marginal_method}:{case_id}" for case_id in ids)
        joint_id = hashlib.sha256("|".join(ids).encode()).hexdigest()[:24]
        output_id = f"{self.method_id}__{self.marginal_method}" if coupling else self.method_id
        return JointPrediction(
            joint_id=joint_id, method_id=output_id, component_case_ids=ids,
            samples=samples, weights=weights, marginal_refs=marginal_refs,
            approximation_metadata=MappingProxyType(metadata), fit_ref=self.train_hash,
        )

    def to_spec(self) -> dict[str, Json]:
        return {
            "type": "annual_joint", "version": 1, "method_id": self.method_id,
            "algorithm": self.algorithm, "marginal_method": self.marginal_method,
            "train_hash": self.train_hash,
            "component_signature": [list(signature) for signature in self.signature],
            "source_years": list(self.source_years), "rain_columns": list(self.rain),
            "observed_template": matrix_json(self.observed_template),
            "training_mean": vector_json(self.training_mean),
            "training_scale": vector_json(self.training_scale),
            "dependence": matrix_json(self.dependence) if self.dependence is not None else None,
            "residuals": residual_spec(self.residuals) if self.residuals is not None else None,
            "mapping": self.mapping.to_spec() if self.mapping is not None else None,
            "transport": self.transport.to_spec() if self.transport is not None else None,
        }
