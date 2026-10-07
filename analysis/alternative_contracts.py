"""Typed, truth-separated contracts for the alternative experiment."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum
from types import MappingProxyType
from typing import Literal, Protocol

from analysis.calibration import FloatArray
from analysis.data_io import Json

type Product = Literal["1mon", "3mon"]
type Variable = Literal["t15m", "prcp"]
type Surface = Literal["continuous", "category", "joint"]
type FitScope = Literal["local", "pooled", "joint"]


def empty_metadata() -> Mapping[str, Json]:
    """Supply immutable empty metadata to independently owned models."""
    return MappingProxyType({})


class FitStatus(StrEnum):
    """A failed or scientifically gated fit never becomes a forecast."""

    OK = "OK"
    NOT_APPLICABLE_DOMAIN = "NOT_APPLICABLE_DOMAIN"
    GATED_DATA = "GATED_DATA"
    INSUFFICIENT_TRAINING = "INSUFFICIENT_TRAINING"
    INSUFFICIENT_INNER_FOLDS = "INSUFFICIENT_INNER_FOLDS"
    INPUT_CONFLICT = "INPUT_CONFLICT"
    FIT_FAILED = "FIT_FAILED"
    POSTERIOR_DIAGNOSTICS_FAILED = "POSTERIOR_DIAGNOSTICS_FAILED"
    NUMERICAL_DISTRIBUTION_FAILED = "NUMERICAL_DISTRIBUTION_FAILED"
    TARGET_UNAVAILABLE = "TARGET_UNAVAILABLE"


class AlternativeError(RuntimeError):
    """A typed numerical/input failure retaining its reason."""

    code: str
    detail: str

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


class PredictiveDistribution(Protocol):
    """The issued original-unit law, including atoms and its likelihood."""

    def cdf(self, value: FloatArray) -> FloatArray: ...
    def cdf_left(self, value: FloatArray) -> FloatArray: ...
    def quantile(self, probability: FloatArray) -> FloatArray: ...
    def mean(self) -> float: ...
    def crps(self, observation: float) -> float: ...
    def log_density(self, value: float) -> float: ...
    def atom_mass(self, value: float) -> float: ...
    def to_spec(self) -> dict[str, Json]: ...


@dataclass(frozen=True, slots=True, kw_only=True)
class CaseInput:
    """Known issued inputs only: there is deliberately no observed truth."""

    case_id: str
    init: date
    valid_start: date
    valid_end: date
    product: Product
    lead: str
    variable: Variable
    members: FloatArray
    member_keys: tuple[str, ...]
    provenance_hash: str
    archive_era: str = ""


@dataclass(frozen=True, slots=True, kw_only=True)
class TrainingRow:
    """One annual paired response, never one response per ensemble member."""

    row_id: str
    source_case_id: str
    source_case_init: date
    source_year: int
    source_init: date
    hist_start: date
    hist_end: date
    product: Product
    lead: str
    variable: Variable
    ensemble: FloatArray
    observation: float
    member_keys: tuple[str, ...]
    provenance_hash: str
    archive_era: str
    source_files: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True)
class FeatureSpec:
    """Training-only standardization of the fixed eight known features."""

    names: tuple[str, ...]
    center: FloatArray
    scale: FloatArray
    predictor_power: float = 1.0


@dataclass(frozen=True, slots=True, kw_only=True)
class FoldSpec:
    """An ancestor fit's response-time gate and reproducible row identities."""

    fold_id: str
    validation_row_ids: tuple[str, ...]
    training_row_ids: tuple[str, ...]
    pseudo_init: date
    held_out_years: tuple[int, ...]
    ancestor_hash: str


@dataclass(frozen=True, slots=True, kw_only=True)
class TrainingSet:
    """Eligible data with an outer-frozen catalog and stricter fold cutoff."""

    target: CaseInput
    rows: tuple[TrainingRow, ...]
    year_weights: FloatArray
    cutoff: date
    catalog_cutoff: date
    held_out_years: tuple[int, ...]
    train_hash: str
    local_observations: FloatArray
    thresholds: FloatArray
    feature_spec: FeatureSpec | None = None
    fold_specs: tuple[FoldSpec, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True)
class GateResult:
    """A factual input gate with the evidence and measured counts."""

    allowed: bool
    reason_code: str
    evidence_refs: tuple[str, ...] = ()
    counts: Mapping[str, Json] = field(default_factory=empty_metadata)


@dataclass(frozen=True, slots=True, kw_only=True)
class JointTrainingSet:
    """Complete annual vectors with their component/calendar provenance."""

    targets: tuple[CaseInput, ...]
    component_keys: tuple[str, ...]
    rows_by_year: Mapping[int, tuple[TrainingRow, ...]]
    source_years: tuple[int, ...]
    historical_initializations: tuple[date, ...]
    historical_windows: tuple[tuple[tuple[date, date], ...], ...]
    forecast_means: FloatArray
    observations: FloatArray
    cutoff: date
    catalog_cutoff: date
    held_out_years: tuple[int, ...]
    train_hash: str
    gate_receipts: tuple[GateResult, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True)
class ResidualSet:
    """Whole annual residual/PIT vectors and their past-only fit ancestry."""

    component_keys: tuple[str, ...]
    years: tuple[int, ...]
    residual_matrix: FloatArray
    weights: FloatArray
    fold_refs: tuple[FoldSpec, ...]
    kind: Literal["latent_error", "pit_normal"] = "latent_error"


@dataclass(frozen=True, slots=True, kw_only=True)
class FitConfig:
    """Predeclared algorithm settings; never target-score-selected."""

    seed: int = 20261007
    numerical_tolerance: float = 1e-7
    fixed_registry_parameters: Mapping[str, Json] = field(default_factory=empty_metadata)
    workers: int = 4


@dataclass(frozen=True, slots=True, kw_only=True)
class MethodSpec:
    """One algorithm/subtype, not a display alias counted as a new fit."""

    id: str
    family_no: int
    subtype: str
    domain: Literal["temperature", "precipitation", "both"]
    surface: Surface
    fit_scope: FitScope
    algorithm_version: str
    owner: Literal["baseline", "classical", "bayes", "learning", "joint"]
    fixed_parameters: Mapping[str, Json] = field(default_factory=empty_metadata)
    gate_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True)
class FitDiagnostics:
    """Actual solver/support diagnostics; missing checks remain missing."""

    objective: float | None = None
    convergence: bool = False
    n_rows: int = 0
    n_years: int = 0
    train_hash: str = ""
    parameter_count: int = 0
    boundary_flags: tuple[str, ...] = ()
    numerical_error: float | None = None
    posterior_diagnostics: Mapping[str, Json] = field(default_factory=empty_metadata)
    elapsed_seconds: float = 0.0
    message: str = ""


class FittedModel(Protocol):
    """A continuous fit predicts without any held-out observation."""

    def predict(self, target: CaseInput) -> PredictiveDistribution: ...
    def to_spec(self) -> dict[str, Json]: ...


class CategoryModel(Protocol):
    """A category fit does not fabricate a continuous distribution."""

    def predict(self, target: CaseInput, thresholds: FloatArray) -> CategoryPrediction: ...
    def to_spec(self) -> dict[str, Json]: ...


class JointModel(Protocol):
    """A joint model declares the complete scenario law it issues."""

    def predict(
        self, targets: tuple[CaseInput, ...],
        marginals: tuple[PredictiveDistribution, ...], config: FitConfig,
    ) -> JointPrediction: ...
    def to_spec(self) -> dict[str, Json]: ...


@dataclass(frozen=True, slots=True, kw_only=True)
class FitResult:
    """Continuous fitting outcome, including explicit scientific failures."""

    method_id: str
    status: FitStatus
    fitted_model: FittedModel | None
    diagnostics: FitDiagnostics
    reason_code: str = ""


@dataclass(frozen=True, slots=True, kw_only=True)
class CategoryFitResult:
    """A separate category outcome prevents accidental continuous scoring."""

    method_id: str
    status: FitStatus
    fitted_model: CategoryModel | None
    diagnostics: FitDiagnostics
    reason_code: str = ""


@dataclass(frozen=True, slots=True, kw_only=True)
class JointFitResult:
    """Joint fitting outcome with its own prediction surface."""

    method_id: str
    status: FitStatus
    fitted_model: JointModel | None
    diagnostics: FitDiagnostics
    reason_code: str = ""


@dataclass(frozen=True, slots=True, kw_only=True)
class ContinuousPrediction:
    """An issued continuous law and the fit that created it."""

    case_id: str
    method_id: str
    distribution: PredictiveDistribution
    fit_ref: str


@dataclass(frozen=True, slots=True, kw_only=True)
class CategoryPrediction:
    """Only requested category probabilities, not a made-up continuous law."""

    case_id: str
    method_id: str
    thresholds: FloatArray
    probabilities: FloatArray
    fit_ref: str


@dataclass(frozen=True, slots=True, kw_only=True)
class JointPrediction:
    """An actual weighted scenario distribution, with approximation disclosed."""

    joint_id: str
    method_id: str
    component_case_ids: tuple[str, ...]
    samples: FloatArray
    weights: FloatArray
    marginal_refs: tuple[str, ...]
    approximation_metadata: Mapping[str, Json]
    fit_ref: str


@dataclass(frozen=True, slots=True, kw_only=True)
class NumericIntegral:
    """An integration result, not an unqualified numerical scalar."""

    value: float
    error: float
    converged: bool


