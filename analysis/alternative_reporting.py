"""Failure-honest fair comparison reports from saved real experiment artifacts."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile
from collections.abc import Mapping
from pathlib import Path

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.alternative_experiment_types import ExperimentInputs
from analysis.alternative_registry import method_registry
from analysis.alternative_reporting_common import (
    Row,
    decode,
    method,
    number,
    object_json,
    rows,
    save_json,
    save_rows,
    string_list,
    text,
)
from analysis.alternative_reporting_diagnostics import diagnostics, reliability
from analysis.alternative_reporting_fairness import (
    common_masks,
    coverage,
    indexed,
    policies,
)
from analysis.alternative_reporting_joint import inspect_scenarios, scalar_case_coverage
from analysis.alternative_reporting_joint import metadata as joint_metadata
from analysis.alternative_reporting_joint import policies as joint_policies
from analysis.alternative_reporting_plots import plots
from analysis.alternative_reporting_statistics import (
    SEED,
    enrich,
    sensitivity,
    summaries,
)
from analysis.data_io import Json
from analysis.scoring import generate_summaries

REQUIRED = (
    "run_summary.json", "method_inventory.csv", "case_method_status.csv.gz",
    "continuous_predictions.csv.gz", "category_predictions.csv.gz", "joint_predictions.csv.gz",
    "training_ledger.csv.gz", "fit_ledger.csv.gz", "fit_schedule.csv",
    "fold_ancestry.csv.gz", "distribution_specs.jsonl.gz", "joint_scenarios.npz",
    "joint_training_manifest.csv.gz", "joint_fold_ancestry.csv.gz",
    "joint_scenario_marginals.csv.gz", "joint_analytic_marginals.csv.gz",
    "joint_key_status.csv.gz", "joint_component_manifest.csv",
)


def run_completed(run: Mapping[str, Json]) -> bool:
    """A report cannot promote a running, interrupted or failed experiment."""
    return run.get("status") == "COMPLETED"


def _safe(output: Path, inputs: ExperimentInputs) -> Path:
    output = output.resolve()
    root = inputs.root.resolve()
    if output == root / "outputs" or not output.is_relative_to(root / "outputs"):
        raise ValueError("Reporting output must be a new child under outputs")
    receipt = root / ".omo/evidence/alternative-baseline-hashes.json"
    if receipt.exists():
        protected = object_json(receipt).get("files")
        if not isinstance(protected, dict):
            raise ValueError("Invalid protected file receipt")
        for relative in protected:
            path = (root / relative).resolve()
            if output.is_relative_to(path) or path.is_relative_to(output):
                raise ValueError(f"Output overlaps protected baseline: {relative}")
    if output.is_relative_to(inputs.source.resolve()):
        raise ValueError("Reporting cannot overwrite source")
    return output


def _korean(summary: dict[str, Json], counts: list[Row], metrics: list[Row],
            paired: list[Row], policy: list[Row], diagnostic: list[Row]) -> str:
    lines = [
        "# 통계 대안 공정 비교 보고서", "",
        f"- 실행 범위: `{summary['scope']}`; 보고 상태: `{summary['status']}`.",
        f"- 원실행 상태: `{summary['run_status']}`. 진행·중단·실패 실행은 완료 보고가 아니다.",
        f"- 고정 난수 시드: {SEED}. 이 문서는 저장된 실제 예측만 분석한다.",
        "- 전체 실험 완료 또는 통계적 유의성을 이 보고서만으로 주장하지 않는다.", "",
        "## 1. 성능 비교에 앞선 실제 적용·성공 범위",
        "|상품|변수/벡터|방법|계열|제공|도메인 적용|과학적 게이트|결측 정답|평가 가능|평가 성공|적합 실패|수치/점수 실패|미기록|",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in counts:
        keys = ("PRODUCT", "VARIABLE", "method_id", "family_no", "supplied_count", "domain_eligible_count",
                "scientific_gates", "missing_targets", "eligible_count", "scored_count",
                "fit_failures", "numerical_or_score_failures", "unrecorded_count")
        lines.append("|"+"|".join(str(row.get(k, "")) for k in keys)+"|")
    lines.extend(["", "## 2. 실제 원단위 및 범주·결합 점수",
                  "주간(1mon: 7일)과 월간(3mon: 개별 달), 기온(degC)과 강수(mm)는 합치지 않는다.",
                  "아래 값은 성공 사례 제한 평균이다. 서로 다른 N의 평균을 전체 우열로 해석하지 않는다.",
                  "|상품|변수/벡터|방법|점수|평가 N|평균 손실|", "|---|---|---|---|---:|---:|"])
    for row in metrics:
        if text(row, "group") == "overall":
            lines.append("|"+"|".join(str(row.get(k, "")) for k in
                                      ("PRODUCT", "VARIABLE", "method_id", "score", "scored_N", "mean_loss"))+"|")
    lines.extend(["", "## 3. 동일 성공 마스크의 비교",
                  "paired_comparison.csv는 동일 사례에서만 손실 차이를 계산한다. 음수는 첫 방법의 작은 손실을 뜻한다.",
                  "common_masks.csv에 모든 정확한 사례 ID, SHA256, 사전 지정 레지스트리 family_no 교집합을 보존한다.",
                  f"저장된 공통마스크 점수 행: {len(paired)}. 빈 교집합도 숨기지 않는다.",
                  "lead/month/season/year별 결과는 각 점수 표에 있으며 범주 전용은 RPS/Brier만 산출한다.",
                  "다음은 EMOS가 포함된 동일 사례 손실 차이의 실제 수치이며 우월성·유의성 판정이 아니다.",
                  "|상품|변수|첫 방법−둘째 방법|점수|공통 N|손실 차이|마스크 SHA256|",
                  "|---|---|---|---|---:|---:|---|"])
    for row in paired:
        if text(row, "mask_kind") != "pairwise":
            continue
        participants = string_list(decode(text(row, "methods")))
        if "EMOS" not in participants:
            continue
        if method(row) != participants[0]:
            continue
        lines.append("|"+"|".join(str(row.get(k, "")) for k in
                                  ("PRODUCT", "VARIABLE", "methods", "score", "N",
                                   "delta_first_minus_second", "mask_hash"))+"|")
    lines.extend(["",
                  "## 4. 실패를 포함한 운용 정책과 손실 한계",
                  "failure_inclusive_policy.csv의 method+climatology_on_failure는 별도 정책이다.",
                  "실패한 원방법 상태·분포를 변경하지 않으며, 같은 외부 훈련 경험 기후값으로 실패 사례를 평가한다.",
                  "미기록 또는 미실행 상태는 성공도 실패 대체도 아니다. 정책이 불완전하면 평균은 비운다.",
                  "비음수 점수의 미평가 손실 한계는 [성공 손실 합/N, +inf]이며 유한 벌점을 만들지 않는다.",
                  f"정책 행: {len(policy)}; 상세 대체 출처는 failure_policy_cases.csv에 있다.", "",
                  "## 5. 반복 관측창·연도 민감도",
                  "동일 변수/상품/정확한 VALID_START-END 창 총 가중치 1을 발행들에 나눈다.",
                  "year_overlap_sensitivity.csv는 같은 창을 묶은 연도 블록 및 연결된 중첩창 블록 재표본화(999회),",
                  "연도별 차이와 한 연도 제외 차이를 기록한다. 실제 약 5개 검증 연도로 강한 유의성·인과 주장을 하지 않는다.", "",
                  "## 6. 분포·강수 사건·결합 근사",
                  "원래 해석적 주변분포 점수와 유한 시나리오 투영 주변점수는 별도 산출물이다.",
                  "결합 ENERGY/VARIOGRAM 및 실제 저장된 사건 Brier는 벡터 범위별로만 비교한다.",
                  "PIT는 F(y-)와 F(y) 사이 원자 질량을 고정 시드로 무작위화한다.",
                  "상위 강수 사건은 외부 훈련 90% 분위수 초과로 고정되며 검증 정답으로 임계값을 고르지 않는다.",
                  f"원분포 진단 행: {len(diagnostic)}; 원분포가 없거나 복원 실패하면 MISSING/ERROR를 표시한다.", "",
                  "## 7. 완전성·근거 및 해석 한계",
                  f"필수 산출물 결측: {summary['missing_artifacts']}.",
                  "report_manifest.json은 범위·시드·필수 산출물·진단 결측·마스크 정의·그림 경로를 기록한다.",
                  "모든 방법 전체 실행, 독립 검증 및 최종 수동 QA는 별도 증거가 필요하다.",
                  "유리한 일부 사례나 성공만으로 최선·우월·실험 PASS라고 주장하지 않는다.",
                  "RAW/QM/QDM/EMOS 비교도 위와 동일한 적용범위·공통마스크·실패정책 규칙을 따른다.", ""])
    return "\n".join(lines)


def generate_reports(output: Path, inputs: ExperimentInputs) -> dict[str, Json]:
    """Read runner tables, atomically publish reports/, and return honest completeness."""
    output = _safe(output, inputs)
    output.mkdir(parents=True, exist_ok=True)
    run = object_json(output / "run_summary.json") if (output / "run_summary.json").exists() else {}
    run_scope = str(run.get("scope", "UNRECORDED"))
    inventory = rows(output / "method_inventory.csv")
    selected = {method(row) for row in inventory}
    unknown = {i for i in selected if i.split("__")[0] not in {spec.id for spec in method_registry()}}
    if unknown:
        raise ValueError(f"Unknown inventory methods: {sorted(unknown)}")
    statuses = rows(output / "case_method_status.csv.gz")
    scalar_statuses = [r for r in statuses if text(r, "surface") != "joint"]
    schedule = rows(output / "fit_schedule.csv")
    joint_statuses = joint_metadata(rows(output / "joint_key_status.csv.gz"), schedule, inputs)
    continuous = enrich(rows(output / "continuous_predictions.csv.gz"))
    category = enrich(rows(output / "category_predictions.csv.gz"))
    joint = joint_metadata(rows(output / "joint_predictions.csv.gz"), schedule, inputs)
    for table in (continuous, category, joint):
        _ = indexed(table)
    ledger = indexed([*scalar_statuses, *joint_statuses])
    # Success requires both a scored record and unchanged explicit OK status.
    continuous = [r for r in continuous if text(ledger.get(
        (text(r, "case_id", "CASE_ID"), method(r)), {}), "status") == "OK"]
    category = [r for r in category if text(ledger.get(
        (text(r, "case_id", "CASE_ID"), method(r)), {}), "status") == "OK"]
    joint = [r for r in joint if text(ledger.get(
        (text(r, "joint_id"), method(r)), {}), "status") == "OK"]
    counts = coverage(inputs, [*scalar_statuses, *joint_statuses],
                      [*continuous, *category, *joint], selected)
    policy, policy_details = policies(inputs, [*continuous, *category], scalar_statuses,
                                     [r for r in counts if text(r, "surface") != "joint"])
    joint_scores = tuple(sorted({"ENERGY", "VARIOGRAM"} |
                               {k for row in joint for k in row if k.endswith("_BRIER")}))
    joint_policy, joint_policy_details = joint_policies(inputs, joint, joint_statuses, counts, joint_scores)
    policy.extend(joint_policy)
    policy_details.extend(joint_policy_details)
    all_metrics: list[Row] = []
    weighted: list[Row] = []
    paired: list[Row] = []
    masks: list[Row] = []
    sensitivities: list[Row] = []
    surfaces = (("continuous", continuous, ("CRPS", "BRIER", "RPS")),
                ("category", category, ("BRIER", "RPS")),
                ("joint", joint, joint_scores))
    for surface, table, scores in surfaces:
        ordinary, equal = summaries(table, scores, surface)
        all_metrics.extend(ordinary)
        weighted.extend(equal)
        comparisons, exact_masks = common_masks(table, counts, scores, surface)
        paired.extend(comparisons)
        masks.extend(exact_masks)
        sensitivities.extend(sensitivity(table, scores, surface))
    marginal_metrics: dict[str, list[Row]] = {}
    parent_scopes = {text(r, "joint_id"): text(r, "VARIABLE") for r in joint}
    for representation in ("scenario", "analytic"):
        marginal_rows = enrich(rows(output / f"joint_{representation}_marginals.csv.gz"))
        for row in marginal_rows:
            parent = parent_scopes[text(row, "joint_id")]
            row["VARIABLE"] = f"{text(row, 'VARIABLE')}::joint_scope={parent}"
        marginal_metrics[representation], _ = summaries(
            marginal_rows, ("CRPS", "BRIER", "RPS"), f"joint_{representation}_marginal")
    diagnostic, threshold_checks = diagnostics(output, inputs, continuous)
    scenario_diagnostics = inspect_scenarios(output, joint)
    missing = [name for name in REQUIRED if not (output / name).is_file()]
    unrecorded = sum(number(r, "unrecorded_count") or 0 for r in counts)
    bad_laws = sum(text(r, "law_status") != "OK" for r in diagnostic)
    bad_thresholds = sum(text(r, "threshold_status") != "MATCH" for r in threshold_checks)
    bad_scenarios = sum(text(r, "status") != "OK" for r in scenario_diagnostics)
    incomplete_policies = sum(text(r, "policy_status") != "COMPLETE" for r in policy)
    expected_methods = {s.id for s in method_registry()}
    full_ready = (run_scope == "FULL" and run_completed(run)
                  and not missing and expected_methods <= selected
                  and not unrecorded and not bad_laws and not bad_thresholds
                  and not bad_scenarios and not incomplete_policies)
    artifact_hashes: dict[str, Json] = {}
    for name in REQUIRED:
        if (output / name).is_file():
            with (output / name).open("rb") as handle:
                artifact_hashes[name] = hashlib.file_digest(handle, "sha256").hexdigest()
    summary: dict[str, Json] = {
        "scope": run_scope, "status": "REPORTS_GENERATED" if full_ready else "INCOMPLETE",
        "run_status": str(run.get("status", "UNRECORDED")),
        "not_validation_pass": True, "seed": SEED, "missing_artifacts": [str(i) for i in missing],
        "selected_methods": [str(i) for i in sorted(selected)],
        "missing_registry_methods": [str(i) for i in sorted(expected_methods-selected)],
        "unrecorded_status_count": unrecorded, "missing_or_error_laws": bad_laws,
        "threshold_mismatches": bad_thresholds, "counts_precede_scores": True,
        "invalid_joint_scenarios": bad_scenarios, "incomplete_policy_rows": incomplete_policies,
        "read_artifact_sha256": artifact_hashes,
        "mask_definition": "sorted exact case/joint IDs encoded compact UTF-8 JSON SHA256",
        "family_definition": "registry family_no within product/variable/surface, prespecified",
        "bounds": "[sum(success losses)/eligible N, +inf]",
        "weight_rule": "each product/variable/exact valid window total 1",
        "sensitivity": "999 fixed-seed year/connected-overlap block draws; descriptive only",
        "joint_ancestry": "joint_training_manifest.csv.gz and joint_fold_ancestry.csv.gz, not scalar hashes",
    }
    destination = output / "reports"
    staging = Path(tempfile.mkdtemp(prefix=".report-staging-", dir=output))
    backup = output / ".reports-previous"
    try:
        save_rows(staging / "coverage_and_failures.csv", counts)
        save_rows(staging / "joint_component_coverage.csv", scalar_case_coverage(inputs, statuses))
        save_rows(staging / "paired_comparison.csv", paired)
        save_rows(staging / "common_masks.csv", masks)
        save_rows(staging / "failure_inclusive_policy.csv", policy)
        save_rows(staging / "failure_policy_cases.csv", policy_details)
        save_rows(staging / "equal_valid_window_metrics.csv", weighted)
        save_rows(staging / "year_overlap_sensitivity.csv", sensitivities)
        for surface, _, _ in surfaces:
            save_rows(staging / f"{surface}_metrics.csv",
                      [r for r in all_metrics if text(r, "surface") == surface])
        for representation, records in marginal_metrics.items():
            save_rows(staging / f"joint_{representation}_marginal_metrics.csv", records)
        save_rows(staging / "distribution_diagnostics.csv", diagnostic)
        save_rows(staging / "joint_law_diagnostics.csv", scenario_diagnostics)
        save_rows(staging / "category_reliability.csv", reliability(category, "category"))
        save_rows(staging / "continuous_reliability.csv", reliability(continuous, "continuous"))
        save_rows(staging / "common_threshold_checks.csv", threshold_checks)
        if continuous:
            generate_summaries(continuous, staging)
        summary["plots"] = [str(i) for i in plots(staging, counts, all_metrics, run_scope)]
        _ = (staging / "REPORT_KO.md").write_text(
            _korean(summary, counts, all_metrics, paired, policy, diagnostic), encoding="utf-8")
        save_json(staging / "report_manifest.json", summary)
        if backup.exists():
            raise RuntimeError("Previous interrupted reporting backup requires inspection")
        if destination.exists():
            os.replace(destination, backup)
        try:
            os.replace(staging, destination)
        except OSError:
            if backup.exists():
                os.replace(backup, destination)
            raise
        if backup.exists():
            shutil.rmtree(backup)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return summary


def main() -> None:
    class Arguments(argparse.Namespace):
        output: Path = Path()
        root: Path = Path()

    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--output", type=Path, required=True)
    _ = parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(namespace=Arguments())
    from analysis.alternative_catalog import load_experiment

    result = generate_reports(args.output, load_experiment(args.root))
    print(f"{result['status']} scope={result['scope']} reports={args.output / 'reports'}")


if __name__ == "__main__":
    main()
