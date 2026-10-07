"""Loader/scorer-only truth types, never passed to fitted methods."""

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from analysis.alternative_contracts import CaseInput, TrainingRow
from analysis.calibration import FloatArray
from analysis.data_io import CsvCell, Json


@dataclass(frozen=True, slots=True, kw_only=True)
class ScoreTruth:
    """Held-out truth is confined to scoring, separate from CaseInput."""

    case_id: str
    observation: float
    historical_observations: FloatArray
    thresholds: FloatArray


@dataclass(frozen=True, slots=True, kw_only=True)
class JointTruth:
    """Observed joint vector and outer-training scoring coordinates."""

    observations: FloatArray
    centers: FloatArray
    scales: FloatArray
    thresholds: tuple[FloatArray, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class ExperimentInputs:
    """Catalog and truths are separated before fitting any method."""

    root: Path
    source: Path
    cases: tuple[CaseInput, ...]
    historical: Mapping[str, tuple[TrainingRow, ...]]
    truths: Mapping[str, ScoreTruth]
    excluded_cases: Mapping[str, str]
    provenance: Mapping[str, Json]
    baseline_rows: tuple[Mapping[str, CsvCell], ...] = ()
