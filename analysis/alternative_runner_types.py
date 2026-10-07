"""Frozen runner options and exactly identified work items."""

from dataclasses import dataclass

from analysis.alternative_contracts import CaseInput, JointTrainingSet, MethodSpec


@dataclass(frozen=True, slots=True, kw_only=True)
class RunOptions:
    methods: tuple[str, ...] = ()
    case_ids: tuple[str, ...] = ()
    workers: int = 4
    seed: int = 20261007
    resume: bool = False


@dataclass(frozen=True, slots=True, kw_only=True)
class Work:
    spec: MethodSpec
    target: CaseInput | None = None
    joint_training: JointTrainingSet | None = None
    marginal: str = ""
