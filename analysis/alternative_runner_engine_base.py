"""Real dispatch, conservative fit sharing, and complete prediction checkpoints."""

from __future__ import annotations

import threading
from collections import OrderedDict, defaultdict
from collections.abc import Callable, Mapping
from dataclasses import replace
from pathlib import Path

import numpy as np

from analysis.alternative_bayes import fit_bayes
from analysis.alternative_classical import fit_classical
from analysis.alternative_contracts import (
    AlternativeError,
    CaseInput,
    CategoryFitResult,
    FitConfig,
    FitDiagnostics,
    FitResult,
    FoldSpec,
    JointTrainingSet,
    MethodSpec,
    PredictiveDistribution,
    TrainingSet,
)
from analysis.alternative_distributions import (
    normal,
    weighted_empirical,
)
from analysis.alternative_experiment_types import ExperimentInputs
from analysis.alternative_learning import fit_learning
from analysis.alternative_runner_ancestry import required_folds
from analysis.alternative_runner_io import (
    Row,
    digest,
    json_value,
    known_input,
    write_json,
)
from analysis.alternative_runner_training import TrainingCache
from analysis.data_io import Json, csv_rows

# These fits read only pooled rows/year weights/product/variable. Category
# center/scale and IDR strata DO depend on the target; they are deliberately absent.
SHARED_IDS = frozenset((
    "pooled_mos_ridge", "pooled_emos_ridge", "pooled_emos_cyclic",
    "gamlss_ridge", "componentwise_boost", "ngboost_small",
    "qrf_year_forest", "drn_small", "bqn_monotone",
))
COUPLING_IDS = frozenset((
    "schaake_window", "schaake_block", "ecc_q",
    "decc_path_shrunk_error", "residual_gaussian_copula",
))
type ScalarResult = FitResult | CategoryFitResult


class EngineBase:
    """Every cache key is truth-free; saved scores are NEVER used as fit keys."""

    def __init__(self, inputs: ExperimentInputs, output: Path, config: FitConfig,
                 sources: Mapping[str, Json], protected: Mapping[str, Json],
                 resume: bool) -> None:
        self.inputs: ExperimentInputs = inputs
        self.output: Path = output
        self.config: FitConfig = config
        self.resume: bool = resume
        self.cache: TrainingCache = TrainingCache(inputs)
        self.source_identity: str = digest({"code": sources, "protected": protected,
                                           "provenance": inputs.provenance})
        self.fits: OrderedDict[str, ScalarResult] = OrderedDict()
        self.fit_locks: dict[str, threading.Lock] = {}
        self.lock: threading.Lock = threading.Lock()
        self.neural_lock: threading.Lock = threading.Lock()
        self.fit_reuses: int = 0
        self.resume_hits: int = 0
        self.fold_cache: dict[tuple[str, str, str], tuple[FoldSpec, ...]] = {}
        self.count_cache: dict[str, tuple[int, int, int]] = {}
        self.fit_metadata: dict[str, dict[str, Json]] = {}
        self.baseline: dict[tuple[str, str], Row] = {
            (str(row["CASE_ID"]), str(row["METHOD"])): dict(row)
            for row in inputs.baseline_rows
        }
        self.members: dict[tuple[str, str], list[float]] = defaultdict(list)
        self.baseline_history: dict[str, dict[int, tuple[float, str, str]]] = defaultdict(dict)

    def prepare_baseline(self, case_ids: set[str]) -> None:
        for row in csv_rows(self.inputs.root / "outputs/calibrated_members.csv.gz"):
            if row["CASE_ID"] in case_ids:
                self.members[(row["CASE_ID"], row["METHOD"])].append(float(row["VALUE"]))
        for row in csv_rows(self.inputs.root / "outputs/training_ledger.csv.gz"):
            if row["CASE_ID"] in case_ids and row["STATUS"] == "OK":
                self.baseline_history[row["CASE_ID"]][int(row["SOURCE_YEAR"])] = (
                    float(row["OBS"]), row["HIST_START"], row["HIST_END"],
                )

    def fit_key(self, spec: MethodSpec, training: TrainingSet | JointTrainingSet,
                targets: tuple[CaseInput, ...], marginal: str = "") -> str:
        settings: dict[str, Json] = {
            "method": json_value(spec), "source_identity": self.source_identity,
            "train_hash": training.train_hash, "seed": self.config.seed,
            "numerical_tolerance": self.config.numerical_tolerance,
            "cutoff": training.cutoff.isoformat(),
            "catalog_cutoff": training.catalog_cutoff.isoformat(),
            "held_out_years": list(training.held_out_years),
            "weight_rule": "total annual source-year weight 1",
            "threshold_definition": "outer local historical linear terciles",
            "marginal": marginal,
        }
        if spec.id not in SHARED_IDS or isinstance(training, JointTrainingSet):
            settings["known_inputs"] = [known_input(target) for target in targets]
            if isinstance(training, TrainingSet):
                settings["local_training_observations"] = json_value(training.local_observations)
                settings["local_thresholds"] = json_value(training.thresholds)
        return digest(settings)

    def fit_config(self, spec: MethodSpec, training_hash: str) -> FitConfig:
        # Deliberately independent of executor order, worker count and target truth.
        seed = int(digest([self.config.seed, spec.id, training_hash, "fit"])[:8], 16)
        return replace(self.config, seed=seed,
                       fixed_registry_parameters=spec.fixed_parameters)

    def schedule_folds(self, spec: MethodSpec, training: TrainingSet) -> tuple[FoldSpec, ...]:
        role = "BMA_all_min10" if spec.id == "bma_component_pool" else "selection_latest5_min15"
        if spec.id not in {"bma_component_pool", "cdf_mix_cv", "tweedie_selected_p"}:
            return ()
        key = (training.train_hash, digest(known_input(training.target)), role)
        if key not in self.fold_cache:
            self.fold_cache[key] = required_folds(spec, training)
        return self.fold_cache[key]

    def training_counts(self, training: TrainingSet) -> tuple[int, int, int]:
        if training.train_hash not in self.count_cache:
            self.count_cache[training.train_hash] = (
                len(training.rows), len({row.source_year for row in training.rows}),
                sum(row.observation == 0 or float(row.ensemble.mean()) == 0
                    for row in training.rows),
            )
        return self.count_cache[training.train_hash]

    def record_fit(self, method_id: str, key: str, status: str, train_hash: str,
                   diagnostics: FitDiagnostics,
                   serialize: Callable[[], dict[str, Json]] | None, *,
                   spec: MethodSpec) -> dict[str, Json]:
        """Store a shared forest/posterior ONCE; keep only small metadata in RAM."""
        with self.lock:
            if key in self.fit_metadata:
                return self.fit_metadata[key]
            record: dict[str, Json] = {
                "method_id": method_id, "fit_ref": key, "status": status,
                "train_hash": train_hash, "diagnostics": json_value(diagnostics),
                "model": serialize() if serialize is not None else None,
                "fit_hash": key, "algorithm_version": spec.algorithm_version,
                "fixed_parameters": dict(spec.fixed_parameters),
                "seed": None if spec.owner == "baseline" else self.fit_config(spec, train_hash).seed,
                "global_seed": self.config.seed,
            }
            path = self.output / "cache" / "fits" / f"{key}.json"
            write_json(path, record)
            metadata = {name: value for name, value in record.items() if name != "model"}
            metadata["model_ref"] = path.relative_to(self.output).as_posix()
            self.fit_metadata[key] = metadata
            return metadata

    def fit_scalar(self, spec: MethodSpec, training: TrainingSet, key: str) -> ScalarResult:
        with self.lock:
            lock = self.fit_locks.setdefault(key, threading.Lock())
        with lock:
            with self.lock:
                if key in self.fits:
                    self.fit_reuses += 1
                    self.fits.move_to_end(key)
                    return self.fits[key]
            config = self.fit_config(spec, training.train_hash)
            match spec.owner:
                case "classical":
                    fitted = fit_classical(spec, training, config)
                case "bayes":
                    fitted = fit_bayes(spec, training, config)
                case "learning":
                    if spec.id in {"drn_small", "bqn_monotone"}:
                        # Torch initialization uses its process-global generator.
                        # Hold the whole deterministic fit, not just manual_seed.
                        with self.neural_lock:
                            fitted = fit_learning(spec, training, config)
                    else:
                        fitted = fit_learning(spec, training, config)
                case _:
                    raise ValueError(f"Non-scalar owner: {spec.owner}")
            with self.lock:
                self.fits[key] = fitted
                if len(self.fits) > 64:
                    _ = self.fits.popitem(last=False)
            return fitted

    def baseline_law(self, target: CaseInput, spec: MethodSpec,
                     training: TrainingSet) -> PredictiveDistribution:
        if spec.id == "climatology_empirical":
            values = training.local_observations
            return weighted_empirical(values, np.full(len(values), 1 / len(values)))
        original = self.baseline_history[target.case_id]
        accepted = {
            row.source_year: (row.observation, row.hist_start.isoformat(), row.hist_end.isoformat())
            for row in training.rows
        }
        if original != accepted:
            raise AlternativeError("BASELINE_TRAINING_CHANGED", target.case_id)
        saved = self.baseline[(target.case_id, spec.id)]
        if spec.id == "EMOS":
            return normal(float(str(saved["EMOS_MU"])), float(str(saved["EMOS_SIGMA"])),
                          censor_zero=target.variable == "prcp")
        values = np.asarray(self.members[(target.case_id, spec.id)], dtype=np.float64)
        if not len(values):
            raise AlternativeError("BASELINE_LAW_MISSING", target.case_id + "/" + spec.id)
        if spec.id == "RAW" and not np.array_equal(np.sort(values), np.sort(target.members)):
            raise AlternativeError("BASELINE_ISSUED_MEMBERS_CHANGED", target.case_id)
        return weighted_empirical(values, np.full(len(values), 1 / len(values)))
