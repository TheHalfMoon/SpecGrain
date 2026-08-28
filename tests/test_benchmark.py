from __future__ import annotations

from dataclasses import replace

import pytest

from specgrain.benchmark import (
    ArmConfiguration,
    BenchmarkArm,
    BenchmarkCase,
    BenchmarkIssueCode,
    BenchmarkPlan,
    BenchmarkRun,
    BenchmarkRunStatus,
    BenchmarkValidationError,
    benchmark_preflight,
    build_benchmark_report,
)

D_A = "sha256:" + "a" * 64
D_B = "sha256:" + "b" * 64
D_C = "sha256:" + "c" * 64
D_D = "sha256:" + "d" * 64
D_E = "sha256:" + "e" * 64
D_F = "sha256:" + "f" * 64
D_1 = "sha256:" + "1" * 64
D_2 = "sha256:" + "2" * 64
D_3 = "sha256:" + "3" * 64


def plan(*, repetitions: int = 2) -> BenchmarkPlan:
    case = BenchmarkCase(
        case_id="localized-bugfix-001",
        repository_revision="git:0123456789abcdef",
        task_digest=D_A,
        acceptance_oracle_digest=D_B,
        environment_digest=D_C,
        scorer_revision="scorer-v1",
        repetitions=repetitions,
        model_config_digest=D_D,
        scorer_hidden=True,
    )
    return BenchmarkPlan(
        case=case,
        arms=(
            ArmConfiguration(BenchmarkArm.PROMPT_ONLY, D_1),
            ArmConfiguration(BenchmarkArm.SPEC_KIT, D_2),
            ArmConfiguration(BenchmarkArm.SPEC_GRAIN, D_3),
        ),
    )


def run(
    arm: BenchmarkArm,
    repetition: int,
    *,
    status: BenchmarkRunStatus = BenchmarkRunStatus.COMPLETED,
) -> BenchmarkRun:
    configs = {
        BenchmarkArm.PROMPT_ONLY: D_1,
        BenchmarkArm.SPEC_KIT: D_2,
        BenchmarkArm.SPEC_GRAIN: D_3,
    }
    return BenchmarkRun(
        run_id=f"{arm.value}-{repetition}",
        case_id="localized-bugfix-001",
        arm=arm,
        repetition=repetition,
        workspace_id=f"workspace-{arm.value}-{repetition}",
        context_id=f"context-{arm.value}-{repetition}",
        repository_revision="git:0123456789abcdef",
        scorer_revision="scorer-v1",
        method_config_digest=configs[arm],
        model_config_digest=D_D,
        status=status,
        acceptance_pass=status is BenchmarkRunStatus.COMPLETED,
        regression_pass=status is BenchmarkRunStatus.COMPLETED,
        scope_pass=status is BenchmarkRunStatus.COMPLETED,
        safety_pass=None,
        first_pass_verified=status is BenchmarkRunStatus.COMPLETED,
        scorer_visible=False,
        input_tokens=100 * repetition,
        output_tokens=20 * repetition,
        duration_ms=1000 * repetition,
        retries=0,
        human_interventions=0,
        changed_files=1,
        changed_lines=3,
        rework_units=0,
        failure_code=None if status is BenchmarkRunStatus.COMPLETED else "EXECUTION_FAILURE",
    )


def full_runs() -> tuple[BenchmarkRun, ...]:
    return tuple(run(arm, repetition) for arm in BenchmarkArm for repetition in (1, 2))


def codes(result) -> set[BenchmarkIssueCode]:
    return {issue.code for issue in result.issues}


def test_plan_requires_exact_three_initial_arms() -> None:
    case = plan().case
    with pytest.raises(BenchmarkValidationError, match="exactly once"):
        BenchmarkPlan(
            case=case,
            arms=(
                ArmConfiguration(BenchmarkArm.PROMPT_ONLY, D_1),
                ArmConfiguration(BenchmarkArm.SPEC_KIT, D_2),
            ),
        )


def test_plan_digest_and_json_are_deterministic_across_arm_input_order() -> None:
    first = plan()
    second = BenchmarkPlan(case=first.case, arms=tuple(reversed(first.arms)))
    assert first.plan_digest == second.plan_digest
    assert first.to_json() == second.to_json()
    assert len(first.expected_cells()) == 6


def test_completed_and_failed_run_contracts_are_strict() -> None:
    assert run(BenchmarkArm.PROMPT_ONLY, 1).status is BenchmarkRunStatus.COMPLETED
    failed = run(BenchmarkArm.PROMPT_ONLY, 1, status=BenchmarkRunStatus.FAILED)
    assert failed.failure_code == "EXECUTION_FAILURE"
    with pytest.raises(BenchmarkValidationError, match="failure_code"):
        replace(failed, failure_code=None)
    with pytest.raises(BenchmarkValidationError, match="must not carry"):
        replace(run(BenchmarkArm.PROMPT_ONLY, 1), failure_code="SHOULD_NOT_EXIST")


def test_valid_preflight_requires_every_cell_once_with_fresh_isolation() -> None:
    result = benchmark_preflight(plan(), full_runs())
    assert result.valid
    assert result.issues == ()


def test_missing_and_duplicate_cells_fail_closed() -> None:
    benchmark = plan()
    observations = list(full_runs())
    observations.pop()
    missing = benchmark_preflight(benchmark, observations)
    assert BenchmarkIssueCode.MISSING_CELL in codes(missing)

    observations = list(full_runs())
    duplicate = replace(
        observations[0],
        run_id="duplicate-cell-run",
        workspace_id="duplicate-cell-workspace",
        context_id="duplicate-cell-context",
    )
    duplicated = benchmark_preflight(benchmark, (*observations, duplicate))
    assert BenchmarkIssueCode.DUPLICATE_CELL in codes(duplicated)


def test_workspace_context_and_run_id_reuse_are_contamination() -> None:
    observations = list(full_runs())
    observations[1] = replace(
        observations[1],
        run_id=observations[0].run_id,
        workspace_id=observations[0].workspace_id,
        context_id=observations[0].context_id,
    )
    result = benchmark_preflight(plan(), observations)
    assert {
        BenchmarkIssueCode.DUPLICATE_RUN_ID,
        BenchmarkIssueCode.WORKSPACE_REUSED,
        BenchmarkIssueCode.CONTEXT_REUSED,
    } <= codes(result)


@pytest.mark.parametrize(
    ("changes", "expected"),
    [
        ({"case_id": "other-case"}, BenchmarkIssueCode.CASE_MISMATCH),
        ({"repetition": 3}, BenchmarkIssueCode.REPETITION_INVALID),
        ({"repository_revision": "git:other"}, BenchmarkIssueCode.REPOSITORY_MISMATCH),
        ({"scorer_revision": "scorer-v2"}, BenchmarkIssueCode.SCORER_MISMATCH),
        ({"method_config_digest": D_E}, BenchmarkIssueCode.METHOD_CONFIG_MISMATCH),
        ({"model_config_digest": D_F}, BenchmarkIssueCode.MODEL_CONFIG_MISMATCH),
        ({"scorer_visible": True}, BenchmarkIssueCode.SCORER_LEAK),
    ],
)
def test_preflight_rejects_control_mismatches(changes, expected) -> None:
    observations = list(full_runs())
    observations[0] = replace(observations[0], **changes)
    result = benchmark_preflight(plan(), observations)
    assert expected in codes(result)


def test_report_retains_failed_and_blocked_runs_and_does_not_rank() -> None:
    observations = list(full_runs())
    observations[0] = run(
        BenchmarkArm.PROMPT_ONLY,
        1,
        status=BenchmarkRunStatus.FAILED,
    )
    observations[3] = run(
        BenchmarkArm.SPEC_KIT,
        2,
        status=BenchmarkRunStatus.BLOCKED,
    )
    report = build_benchmark_report(plan(), observations)
    assert report.valid_comparison
    mapping = {summary.arm: summary for summary in report.summaries}
    assert mapping[BenchmarkArm.PROMPT_ONLY].failed_runs == 1
    assert mapping[BenchmarkArm.SPEC_KIT].blocked_runs == 1
    assert report.to_dict()["automatic_winner"] is None
    assert "Automatic winner: none" in report.to_markdown()


def test_report_metrics_use_all_observations_and_are_deterministic() -> None:
    benchmark = plan()
    observations = full_runs()
    first = build_benchmark_report(benchmark, observations)
    second = build_benchmark_report(benchmark, tuple(reversed(observations)))
    assert first.report_digest == second.report_digest
    assert first.to_json() == second.to_json()
    prompt = next(item for item in first.summaries if item.arm is BenchmarkArm.PROMPT_ONLY)
    assert prompt.total_runs == 2
    assert prompt.total_input_tokens == 300
    assert prompt.total_output_tokens == 60
    assert prompt.total_duration_ms == 3000
    assert prompt.total_changed_files == 2
    assert prompt.total_changed_lines == 6


def test_invalid_comparison_still_reports_runs_without_hiding_them() -> None:
    observations = full_runs()[:-1]
    report = build_benchmark_report(plan(), observations)
    assert not report.valid_comparison
    assert BenchmarkIssueCode.MISSING_CELL in {issue.code for issue in report.issues}
    assert sum(summary.total_runs for summary in report.summaries) == len(observations)
