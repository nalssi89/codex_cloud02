"""Truth-free target-conditioned Bayesian fit serialization and scenario laws."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass

import numpy as np
from scipy.special import ndtri
from scipy.stats import chi2, qmc

from analysis.alternative_bayes_distribution import BayesianScalar, inverse
from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FitConfig,
    JointPrediction,
    PredictiveDistribution,
)
from analysis.calibration import FloatArray
from analysis.data_io import Json


def target_key(targets: tuple[CaseInput, ...]) -> str:
    """Includes only known issued inputs, never a verified response."""
    digest = hashlib.sha256()
    for target in targets:
        digest.update(
            f"{target.case_id}:{target.valid_start}:{target.variable}:".encode()
        )
        digest.update(target.members.tobytes())
    return digest.hexdigest()


def array_json(value: FloatArray) -> Json:
    if value.ndim == 1:
        return [float(x) for x in value.flat]
    return [
        array_json(value[i:i + 1].reshape(value.shape[1:]))
        for i in range(np.size(value, axis=0))
    ]


@dataclass(frozen=True, slots=True, kw_only=True)
class ConditionalLaw:
    """Exact conditional Student or unthinned target-weighted Normal mixture."""

    method_id: str
    train_hash: str
    target_hash: str
    transforms: tuple[str, ...]
    locations: FloatArray
    matrices: FloatArray
    weights: FloatArray
    df: float | None
    posterior_metadata: Mapping[str, Json]

    def marginals(self) -> tuple[PredictiveDistribution, ...]:
        retained = self.posterior_metadata.get("retained_per_chain")
        training_scales = self.posterior_metadata.get("training_response_sd")
        chain_shape = (4, retained) if isinstance(retained, int) else None
        scales = training_scales if isinstance(training_scales, list) else []
        response_sd: list[float] = []
        for value in scales:
            if not isinstance(value, (float, int)):
                raise TypeError("Invalid serialized training response SD")
            response_sd.append(float(value))
        return tuple(
            BayesianScalar(
                locations=self.locations[:, j],
                scales=np.sqrt(self.matrices[:, j, j]), weights=self.weights,
                df=self.df, transform=transform,
                chain_shape=chain_shape,
                training_sd=response_sd[j] if chain_shape is not None else None,
            ) for j, transform in enumerate(self.transforms)
        )

    def check(self, targets: tuple[CaseInput, ...]) -> None:
        if target_key(targets) != self.target_hash:
            raise AlternativeError(
                "TARGET_CONDITION_MISMATCH",
                "This local fit stores p(Y|D,X_issue); refit for different inputs.",
            )

    def to_spec(self) -> dict[str, Json]:
        return {
            "tag": "bayes_conditional_fit", "version": 1,
            "method_id": self.method_id, "train_hash": self.train_hash,
            "target_hash": self.target_hash, "transforms": list(self.transforms),
            "locations": array_json(self.locations),
            "matrices": array_json(self.matrices),
            "weights": array_json(self.weights), "df": self.df,
            "posterior_metadata": dict(self.posterior_metadata),
        }


@dataclass(frozen=True, slots=True, kw_only=True)
class ScalarModel:
    law: ConditionalLaw

    def predict(self, target: CaseInput) -> PredictiveDistribution:
        self.law.check((target,))
        return self.law.marginals()[0]

    def to_spec(self) -> dict[str, Json]:
        return {**self.law.to_spec(), "surface": "continuous"}


@dataclass(frozen=True, slots=True, kw_only=True)
class MultivariateModel:
    law: ConditionalLaw

    def predict(
        self, targets: tuple[CaseInput, ...],
        marginals: tuple[PredictiveDistribution, ...], config: FitConfig,
    ) -> JointPrediction:
        """MBJP owns its marginals; passed coupling marginals are not substituted."""
        _ = marginals
        self.law.check(targets)
        dimension = len(targets)
        uniforms = qmc.Sobol(d=dimension + 2, scramble=True, seed=config.seed).random_base2(9)
        indices = np.searchsorted(np.cumsum(self.law.weights), uniforms[:, 0])
        indices = np.minimum(indices, self.law.weights.size - 1)
        roots = np.linalg.cholesky(self.law.matrices[indices])
        normal = ndtri(uniforms[:, 1:dimension + 1])
        latent = (roots @ normal[..., None])[..., 0]
        if self.law.df is not None:
            latent /= np.sqrt(chi2.ppf(uniforms[:, -1], self.law.df) / self.law.df)[:, None]
        latent += self.law.locations[indices]
        samples = np.column_stack([
            inverse(latent[:, j], transform)
            for j, transform in enumerate(self.law.transforms)
        ])
        metadata: dict[str, Json] = {
            "law": "conditional_student" if self.law.df is not None else "posterior_normal_mixture",
            "scenario_count": 256, "sensitivity_scenario_count": 512,
            "mean_difference_256_512": array_json(
                samples[:256].mean(axis=0) - samples.mean(axis=0)
            ),
            "exact_marginal_specs": [m.to_spec() for m in self.law.marginals()],
            "posterior": dict(self.law.posterior_metadata),
        }
        return JointPrediction(
            joint_id="|".join(t.case_id for t in targets), method_id=self.law.method_id,
            component_case_ids=tuple(t.case_id for t in targets), samples=samples[:256],
            weights=np.full(256, 1 / 256),
            marginal_refs=tuple(f"{self.law.method_id}:{t.case_id}" for t in targets),
            approximation_metadata=metadata, fit_ref=self.law.train_hash,
        )

    def to_spec(self) -> dict[str, Json]:
        return {**self.law.to_spec(), "surface": "joint"}


def model_from_spec(spec: Mapping[str, Json]) -> ScalarModel | MultivariateModel:
    """Restore full predictive laws, not a grid of surrogate quantiles."""
    if spec.get("tag") != "bayes_conditional_fit" or spec.get("version") != 1:
        raise ValueError("Unknown Bayesian fitted-model serialization")
    transforms = spec["transforms"]
    metadata = spec["posterior_metadata"]
    degrees = spec["df"]
    if not isinstance(transforms, list) or not all(isinstance(x, str) for x in transforms):
        raise ValueError("Invalid Bayesian transforms")
    if not isinstance(metadata, dict) or not (degrees is None or isinstance(degrees, (int, float))):
        raise ValueError("Invalid Bayesian posterior metadata/df")
    law = ConditionalLaw(
        method_id=str(spec["method_id"]), train_hash=str(spec["train_hash"]),
        target_hash=str(spec["target_hash"]), transforms=tuple(str(t) for t in transforms),
        locations=np.asarray(spec["locations"], dtype=float),
        matrices=np.asarray(spec["matrices"], dtype=float),
        weights=np.asarray(spec["weights"], dtype=float), df=degrees,
        posterior_metadata=metadata,
    )
    if spec["surface"] == "joint":
        return MultivariateModel(law=law)
    return ScalarModel(law=law)
