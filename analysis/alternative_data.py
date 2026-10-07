"""Stable adapter API; no target truth is passed into method fitting."""

from analysis.alternative_catalog import load_experiment
from analysis.alternative_features import features_for_case, features_for_training
from analysis.alternative_joint_data import aligned_joint, gate_report
from analysis.alternative_training import (
    fold_training,
    inner_folds,
    row_thresholds,
    training_for,
)

__all__ = [
    "aligned_joint",
    "features_for_case",
    "features_for_training",
    "fold_training",
    "gate_report",
    "inner_folds",
    "load_experiment",
    "row_thresholds",
    "training_for",
]
