"""F2 climate mixtures/signal shrinkage and prequential model-component BMA."""

from __future__ import annotations

from dataclasses import dataclass, replace
from time import perf_counter
from types import MappingProxyType

import numpy as np

from analysis.alternative_classical_mixture_weights import (
    component_log_likelihood,
    fit_weights,
)
from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    FitConfig,
    FitDiagnostics,
    FitResult,
    FitStatus,
    FittedModel,
    MethodSpec,
    PredictiveDistribution,
    TrainingRow,
    TrainingSet,
)
from analysis.calibration import FloatArray
from analysis.data_io import Json


@dataclass(frozen=True, slots=True, kw_only=True)
class MixtureModel:
    """Store fitted component models, never frozen target-specific predictions."""

    components: tuple[FittedModel, ...]
    weights: tuple[float, ...]
    climate: PredictiveDistribution | None = None
    shrink: bool = False

    def predict(self, target: CaseInput) -> PredictiveDistribution:
        from analysis.alternative_distribution_base import ScientificLaw
        from analysis.alternative_distributions import mixture, normal
        parts = tuple(model.predict(target) for model in self.components)
        if self.shrink:
            law = parts[0]
            if not isinstance(law, ScientificLaw) or law.tag != "normal" or self.climate is None:
                raise AlternativeError("INVALID_EMOS_LAW", "Signal shrink requires latent Normal")
            mu = self.climate.mean() + .5 * (law.parameters[0] - self.climate.mean())
            return normal(mu, law.parameters[1], censor_zero=target.variable == "prcp")
        if self.climate is not None:
            parts += (self.climate,)
        return mixture(parts, np.asarray(self.weights))

    def to_spec(self) -> dict[str, Json]:
        return {"type": "classical_predictive_mixture",
                "components": [model.to_spec() for model in self.components],
                "weights": list(self.weights), "signal_shrink": self.shrink,
                "climate": None if self.climate is None else self.climate.to_spec()}


def validation_case(row: TrainingRow) -> CaseInput:
    """Historical pseudo-target contains only the validation row's known inputs."""
    return CaseInput(case_id=row.source_case_id, init=row.source_init,
                     valid_start=row.hist_start, valid_end=row.hist_end,
                     product=row.product, lead=row.lead, variable=row.variable,
                     members=row.ensemble, member_keys=row.member_keys,
                     provenance_hash=row.provenance_hash, archive_era=row.archive_era)


def _components(spec: MethodSpec, training: TrainingSet, config: FitConfig,
                bma: bool) -> tuple[FittedModel, ...]:
    from analysis.alternative_classical_local import fit_local
    kinds = ["emos", "emos_constant_variance"] if bma else ["emos"]
    results = [fit_local(replace(spec, id=kind, family_no=3, subtype=kind,
                                owner="classical", fixed_parameters=MappingProxyType({})),
                         training, config) for kind in kinds]
    if bma:
        from analysis.alternative_bayes import fit_bayes
        kind = "bjp_niw" if training.target.variable == "t15m" else "bjp_sqrt_censored"
        results.append(fit_bayes(replace(spec, id=kind, family_no=1, subtype=kind,
                                        owner="bayes", fixed_parameters=MappingProxyType({})),
                                 training, config))
    for result in results:
        if result.status != FitStatus.OK or result.fitted_model is None:
            message = f"{result.method_id}: {result.reason_code}; {result.diagnostics.message}"
            raise AlternativeError(str(result.status), message)
    return tuple(result.fitted_model for result in results if result.fitted_model is not None)


def _climate(training: TrainingSet) -> PredictiveDistribution:
    from analysis.alternative_distributions import weighted_empirical
    values = training.local_observations
    return weighted_empirical(values, np.full(len(values), 1 / len(values)))


def _prequential(spec: MethodSpec, training: TrainingSet, config: FitConfig,
                 bma: bool) -> tuple[list[tuple[int, float, tuple[PredictiveDistribution, ...]]],
                                     list[dict[str, Json]], list[AlternativeError], tuple[int, ...]]:
    from analysis.alternative_data import fold_training, inner_folds
    rows = {row.row_id: row for row in training.rows}
    records: list[tuple[int, float, tuple[PredictiveDistribution, ...]]] = []
    receipts: list[dict[str, Json]] = []
    failures: list[AlternativeError] = []
    folds = inner_folds(training, training.target, min_years=10 if bma else 15,
                        last_n=None if bma else 5)
    eligible_years = tuple(sorted({rows[row_id].source_year for fold in folds
                                  for row_id in fold.validation_row_ids}))
    for fold in folds:
        try:
            ancestor = fold_training(training, fold)
            if ancestor.catalog_cutoff != training.catalog_cutoff:
                raise AlternativeError("CATALOG_CUTOFF_CHANGED", fold.fold_id)
            models = _components(spec, ancestor, config, bma)
            climate = None if bma else _climate(ancestor)
            fold_records: list[tuple[int, float, tuple[PredictiveDistribution, ...]]] = []
            for row_id in fold.validation_row_ids:
                row = rows[row_id]
                pseudo = replace(validation_case(row), case_id=ancestor.target.case_id)
                parts = tuple(model.predict(pseudo) for model in models)
                if climate is not None:
                    parts += (climate,)
                fold_records.append((row.source_year, row.observation, parts))
            records.extend(fold_records)
            receipts.append({"fold_id": fold.fold_id,
                             "train_hash": ancestor.train_hash,
                             "training_row_ids": list(fold.training_row_ids),
                             "validation_row_ids": list(fold.validation_row_ids),
                             "pseudo_init": fold.pseudo_init.isoformat()})
        except AlternativeError as error:
            failures.append(AlternativeError(error.code, f"{fold.fold_id}: {error.detail}"))
    return records, receipts, failures, eligible_years


def fit_mixture(spec: MethodSpec, training: TrainingSet, config: FitConfig) -> FitResult:
    """Fit only the prescribed F2 subtypes and F8 named predictive-component pool."""
    from analysis.alternative_distributions import mixture
    start = perf_counter()
    kind = spec.id
    bma = kind == "bma_component_pool"
    allowed = {"cdf_mix_fixed50", "cdf_mix_cv", "anomaly_signal_shrink", "bma_component_pool"}
    if kind not in allowed:
        raise ValueError(f"Unsupported mixture method ID: {kind}")
    metadata: dict[str, Json] = {}
    objective: float | None = None
    error: float | None = None
    n_years = len({row.source_year for row in training.rows})

    def finish(status: FitStatus, model: MixtureModel | None, reason: str = "",
               message: str = "") -> FitResult:
        return FitResult(method_id=spec.id, status=status, fitted_model=model,
                         reason_code=reason, diagnostics=FitDiagnostics(
                             objective=objective, convergence=status == FitStatus.OK,
                             n_rows=len(training.rows), n_years=n_years,
                             train_hash=training.train_hash,
                             parameter_count=2 if bma else int(kind == "cdf_mix_cv"),
                             posterior_diagnostics=MappingProxyType(metadata),
                             numerical_error=error, elapsed_seconds=perf_counter()-start,
                             message=message or reason))

    if n_years < 10 or len(training.local_observations) == 0:
        return finish(FitStatus.INSUFFICIENT_TRAINING, None, "REQUIRE_TEN_TRAINING_YEARS")
    try:
        weights = (.5, .5)
        if bma or kind == "cdf_mix_cv":
            records, receipts, failures, eligible_years = _prequential(spec, training, config, bma)
            years = sorted({year for year, _, _ in records})
            metadata["fold_receipts"] = [receipt for receipt in receipts]
            metadata["fold_failures"] = [str(failure) for failure in failures]
            metadata["eligible_prequential_years"] = list(eligible_years)
            metadata["common_prequential_years"] = [year for year in years]
            required = 8 if bma else 3
            if len(years) < required:
                if len(eligible_years) >= required and failures:
                    codes = {failure.code for failure in failures}
                    status = next((status for status in (
                        FitStatus.INPUT_CONFLICT, FitStatus.POSTERIOR_DIAGNOSTICS_FAILED,
                        FitStatus.NUMERICAL_DISTRIBUTION_FAILED, FitStatus.FIT_FAILED,
                    ) if str(status) in codes), FitStatus.FIT_FAILED)
                    return finish(status, None, "PREQUENTIAL_COMPONENT_FAILED",
                                  "; ".join(str(failure) for failure in failures))
                return finish(FitStatus.INSUFFICIENT_INNER_FOLDS, None,
                              "REQUIRE_EIGHT_COMMON_YEARS" if bma else "REQUIRE_THREE_FOLDS")
            counts = {year: sum(record[0] == year for record in records) for year in years}
            if bma:
                log_likelihood: FloatArray = np.vstack([component_log_likelihood(parts, y)
                                                        for _, y, parts in records])
                row_weights: FloatArray = np.asarray([1 / counts[year] for year, _, _ in records])
                fitted_weights, objective, error = fit_weights(log_likelihood, row_weights)
                weights = tuple(fitted_weights.item(i) for i in range(fitted_weights.size))
                metadata["dirichlet_alpha"] = 2
            else:
                scores: list[float] = []
                for i in range(11):
                    lam = i / 10
                    score = sum(mixture(parts, np.asarray([lam, 1-lam])).crps(y)
                                / counts[year] for year, y, parts in records) / len(years)
                    if not np.isfinite(score):
                        raise AlternativeError("NONFINITE_CV_CRPS", str(lam))
                    scores.append(float(score))
                best = min(scores)
                index = next(i for i, score in enumerate(scores) if score <= best + 1e-10)
                weights, objective = (index / 10, 1 - index / 10), scores[index]
                metadata["cv_grid_crps"] = [score for score in scores]
        models = _components(spec, training, config, bma)
        model = MixtureModel(components=models, weights=weights,
                             climate=None if bma else _climate(training),
                             shrink=kind == "anomaly_signal_shrink")
        law = model.predict(training.target)
        if not np.isfinite(law.mean()):
            raise AlternativeError("NONFINITE_MIXTURE_MEAN", spec.id)
        metadata["mixture_weights"] = list(weights)
        return finish(FitStatus.OK, model)
    except AlternativeError as failure:
        code = failure.code
        status = FitStatus(code) if code in FitStatus._value2member_map_ else FitStatus.FIT_FAILED
        return finish(status, None, str(failure))
