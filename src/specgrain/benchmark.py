"""Deterministic SpecGrainBench experiment ledger and reporting primitives."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

BENCHMARK_VERSION = 1


class BenchmarkValidationError(ValueError):
    """Raised when benchmark input violates the v1 ledger contract."""


class BenchmarkArm(StrEnum):
    """Canonical initial comparison arms."""

    PROMPT_ONLY = "prompt-only"
    SPEC_KIT = "spec-kit"
    SPEC_GRAIN = "specgrain"


class BenchmarkRunStatus(StrEnum):
    """Observed external benchmark-run status."""

    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class BenchmarkIssueCode(StrEnum):
    """Stable contamination/comparability issue codes."""

    CASE_MISMATCH = "CASE_MISMATCH"
    CONTEXT_REUSED = "CONTEXT_REUSED"
    DUPLICATE_CELL = "DUPLICATE_CELL"
    DUPLICATE_RUN_ID = "DUPLICATE_RUN_ID"
    METHOD_CONFIG_MISMATCH = "METHOD_CONFIG_MISMATCH"
    MISSING_CELL = "MISSING_CELL"
    MODEL_CONFIG_MISMATCH = "MODEL_CONFIG_MISMATCH"
    REPETITION_INVALID = "REPETITION_INVALID"
    REPOSITORY_MISMATCH = "REPOSITORY_MISMATCH"
    SCORER_LEAK = "SCORER_LEAK"
    SCORER_MISMATCH = "SCORER_MISMATCH"
    WORKSPACE_REUSED = "WORKSPACE_REUSED"


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BenchmarkValidationError(f"{field} must be non-empty text")
    return value


def _digest_value(value: object, field: str) -> str:
    text = _text(value, field)
    if not text.startswith("sha256:") or len(text) != 71:
        raise BenchmarkValidationError(f"{field} must be a sha256: digest")
    if any(character not in "0123456789abcdef" for character in text[7:]):
        raise BenchmarkValidationError(f"{field} must use lowercase hexadecimal")
    return text


def _non_negative(value: object, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise BenchmarkValidationError(f"{field} must be a non-negative integer")
    return value


def _positive(value: object, field: str) -> int:
    result = _non_negative(value, field)
    if result == 0:
        raise BenchmarkValidationError(f"{field} must be a positive integer")
    return result


def _optional_non_negative(value: object, field: str) -> int | None:
    if value is None:
        return None
    return _non_negative(value, field)


def _canonical_json(value: dict[str, object]) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    )


def _content_digest(value: dict[str, object]) -> str:
    encoded = _canonical_json(value).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


@dataclass(frozen=True, slots=True, order=True)
class ArmConfiguration:
    """Exact method configuration bound to one benchmark arm."""

    arm: BenchmarkArm | str
    method_config_digest: str

    def __post_init__(self) -> None:
        try:
            arm = BenchmarkArm(self.arm)
        except (TypeError, ValueError) as exc:
            raise BenchmarkValidationError("arm is not canonical") from exc
        object.__setattr__(self, "arm", arm)
        object.__setattr__(
            self,
            "method_config_digest",
            _digest_value(self.method_config_digest, "method_config_digest"),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "arm": self.arm.value,
            "method_config_digest": self.method_config_digest,
        }


@dataclass(frozen=True, slots=True)
class BenchmarkCase:
    """Immutable common baseline and scoring controls for one benchmark task."""

    case_id: str
    repository_revision: str
    task_digest: str
    acceptance_oracle_digest: str
    environment_digest: str
    scorer_revision: str
    repetitions: int
    model_config_digest: str | None = None
    scorer_hidden: bool = True
    benchmark_version: int = BENCHMARK_VERSION

    def __post_init__(self) -> None:
        if isinstance(self.benchmark_version, bool) or self.benchmark_version != BENCHMARK_VERSION:
            raise BenchmarkValidationError(
                f"benchmark_version must equal integer {BENCHMARK_VERSION}"
            )
        for field in ("case_id", "repository_revision", "scorer_revision"):
            object.__setattr__(self, field, _text(getattr(self, field), field))
        for field in ("task_digest", "acceptance_oracle_digest", "environment_digest"):
            object.__setattr__(self, field, _digest_value(getattr(self, field), field))
        object.__setattr__(self, "repetitions", _positive(self.repetitions, "repetitions"))
        if self.model_config_digest is not None:
            object.__setattr__(
                self,
                "model_config_digest",
                _digest_value(self.model_config_digest, "model_config_digest"),
            )
        if not isinstance(self.scorer_hidden, bool):
            raise BenchmarkValidationError("scorer_hidden must be boolean")

    def to_dict(self) -> dict[str, object]:
        return {
            "acceptance_oracle_digest": self.acceptance_oracle_digest,
            "benchmark_version": self.benchmark_version,
            "case_id": self.case_id,
            "environment_digest": self.environment_digest,
            "model_config_digest": self.model_config_digest,
            "repetitions": self.repetitions,
            "repository_revision": self.repository_revision,
            "scorer_hidden": self.scorer_hidden,
            "scorer_revision": self.scorer_revision,
            "task_digest": self.task_digest,
        }


@dataclass(frozen=True, slots=True)
class BenchmarkPlan:
    """Canonical three-arm v1 benchmark plan."""

    case: BenchmarkCase
    arms: tuple[ArmConfiguration, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.case, BenchmarkCase):
            raise BenchmarkValidationError("case must be a BenchmarkCase")
        arms = tuple(self.arms)
        if any(not isinstance(item, ArmConfiguration) for item in arms):
            raise BenchmarkValidationError("arms must contain ArmConfiguration values")
        counts = Counter(item.arm for item in arms)
        expected = set(BenchmarkArm)
        if set(counts) != expected or any(count != 1 for count in counts.values()):
            raise BenchmarkValidationError(
                "v1 benchmark plan must contain prompt-only, spec-kit, and specgrain exactly once"
            )
        object.__setattr__(self, "arms", tuple(sorted(arms, key=lambda item: item.arm.value)))

    @property
    def plan_digest(self) -> str:
        return _content_digest(self.content_dict())

    def content_dict(self) -> dict[str, object]:
        return {
            "arms": [item.to_dict() for item in self.arms],
            "case": self.case.to_dict(),
        }

    def to_dict(self) -> dict[str, object]:
        result = self.content_dict()
        result["plan_digest"] = self.plan_digest
        return result

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())

    def expected_cells(self) -> tuple[tuple[BenchmarkArm, int], ...]:
        return tuple(
            (arm, repetition)
            for arm in BenchmarkArm
            for repetition in range(1, self.case.repetitions + 1)
        )

    def configuration_for(self, arm: BenchmarkArm) -> ArmConfiguration:
        return next(item for item in self.arms if item.arm is arm)


@dataclass(frozen=True, slots=True)
class BenchmarkRun:
    """One externally observed benchmark cell; failed and blocked cells are retained."""

    run_id: str
    case_id: str
    arm: BenchmarkArm | str
    repetition: int
    workspace_id: str
    context_id: str
    repository_revision: str
    scorer_revision: str
    method_config_digest: str
    status: BenchmarkRunStatus | str
    acceptance_pass: bool
    regression_pass: bool
    scope_pass: bool
    first_pass_verified: bool
    scorer_visible: bool
    model_config_digest: str | None = None
    safety_pass: bool | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    duration_ms: int | None = None
    retries: int = 0
    human_interventions: int = 0
    changed_files: int = 0
    changed_lines: int = 0
    rework_units: int = 0
    failure_code: str | None = None

    def __post_init__(self) -> None:
        for field in (
            "run_id",
            "case_id",
            "workspace_id",
            "context_id",
            "repository_revision",
            "scorer_revision",
        ):
            object.__setattr__(self, field, _text(getattr(self, field), field))
        try:
            arm = BenchmarkArm(self.arm)
        except (TypeError, ValueError) as exc:
            raise BenchmarkValidationError("arm is not canonical") from exc
        object.__setattr__(self, "arm", arm)
        try:
            status = BenchmarkRunStatus(self.status)
        except (TypeError, ValueError) as exc:
            raise BenchmarkValidationError("status is not canonical") from exc
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "repetition", _positive(self.repetition, "repetition"))
        object.__setattr__(
            self,
            "method_config_digest",
            _digest_value(self.method_config_digest, "method_config_digest"),
        )
        if self.model_config_digest is not None:
            object.__setattr__(
                self,
                "model_config_digest",
                _digest_value(self.model_config_digest, "model_config_digest"),
            )
        for field in (
            "acceptance_pass",
            "regression_pass",
            "scope_pass",
            "first_pass_verified",
            "scorer_visible",
        ):
            if not isinstance(getattr(self, field), bool):
                raise BenchmarkValidationError(f"{field} must be boolean")
        if self.safety_pass is not None and not isinstance(self.safety_pass, bool):
            raise BenchmarkValidationError("safety_pass must be boolean or null")
        for field in ("input_tokens", "output_tokens", "duration_ms"):
            object.__setattr__(
                self,
                field,
                _optional_non_negative(getattr(self, field), field),
            )
        for field in (
            "retries",
            "human_interventions",
            "changed_files",
            "changed_lines",
            "rework_units",
        ):
            object.__setattr__(self, field, _non_negative(getattr(self, field), field))
        if status is BenchmarkRunStatus.COMPLETED and self.failure_code is not None:
            raise BenchmarkValidationError("completed runs must not carry failure_code")
        if status is not BenchmarkRunStatus.COMPLETED:
            object.__setattr__(self, "failure_code", _text(self.failure_code, "failure_code"))

    @property
    def run_digest(self) -> str:
        return _content_digest(self.to_dict())

    def to_dict(self) -> dict[str, object]:
        return {
            "acceptance_pass": self.acceptance_pass,
            "arm": self.arm.value,
            "case_id": self.case_id,
            "changed_files": self.changed_files,
            "changed_lines": self.changed_lines,
            "context_id": self.context_id,
            "duration_ms": self.duration_ms,
            "failure_code": self.failure_code,
            "first_pass_verified": self.first_pass_verified,
            "human_interventions": self.human_interventions,
            "input_tokens": self.input_tokens,
            "method_config_digest": self.method_config_digest,
            "model_config_digest": self.model_config_digest,
            "output_tokens": self.output_tokens,
            "regression_pass": self.regression_pass,
            "repetition": self.repetition,
            "repository_revision": self.repository_revision,
            "retries": self.retries,
            "rework_units": self.rework_units,
            "run_id": self.run_id,
            "safety_pass": self.safety_pass,
            "scope_pass": self.scope_pass,
            "scorer_revision": self.scorer_revision,
            "scorer_visible": self.scorer_visible,
            "status": self.status.value,
            "workspace_id": self.workspace_id,
        }


@dataclass(frozen=True, slots=True, order=True)
class BenchmarkIssue:
    code: BenchmarkIssueCode
    location: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "code": self.code.value,
            "location": self.location,
            "message": self.message,
        }


@dataclass(frozen=True, slots=True)
class BenchmarkPreflight:
    plan_digest: str
    issues: tuple[BenchmarkIssue, ...]

    @property
    def valid(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict[str, object]:
        return {
            "issues": [issue.to_dict() for issue in self.issues],
            "plan_digest": self.plan_digest,
            "valid": self.valid,
        }


def _issue(
    issues: list[BenchmarkIssue],
    code: BenchmarkIssueCode,
    location: str,
    message: str,
) -> None:
    issues.append(BenchmarkIssue(code, location, message))


def benchmark_preflight(
    plan: BenchmarkPlan,
    runs: Iterable[BenchmarkRun],
) -> BenchmarkPreflight:
    """Validate isolation and comparability before a dataset may support comparison."""

    if not isinstance(plan, BenchmarkPlan):
        raise BenchmarkValidationError("plan must be a BenchmarkPlan")
    materialized = tuple(runs)
    if any(not isinstance(run, BenchmarkRun) for run in materialized):
        raise BenchmarkValidationError("runs must contain BenchmarkRun values")

    issues: list[BenchmarkIssue] = []
    run_ids = Counter(run.run_id for run in materialized)
    for run_id, count in sorted(run_ids.items()):
        if count > 1:
            _issue(
                issues,
                BenchmarkIssueCode.DUPLICATE_RUN_ID,
                f"run.{run_id}",
                f"run_id appears {count} times",
            )

    workspaces = Counter(run.workspace_id for run in materialized)
    contexts = Counter(run.context_id for run in materialized)
    for value, count in sorted(workspaces.items()):
        if count > 1:
            _issue(
                issues,
                BenchmarkIssueCode.WORKSPACE_REUSED,
                f"workspace.{value}",
                f"workspace_id is shared by {count} benchmark cells",
            )
    for value, count in sorted(contexts.items()):
        if count > 1:
            _issue(
                issues,
                BenchmarkIssueCode.CONTEXT_REUSED,
                f"context.{value}",
                f"context_id is shared by {count} benchmark cells",
            )

    cells = Counter((run.arm, run.repetition) for run in materialized)
    for arm, repetition in plan.expected_cells():
        count = cells.get((arm, repetition), 0)
        location = f"cell.{arm.value}.{repetition}"
        if count == 0:
            _issue(issues, BenchmarkIssueCode.MISSING_CELL, location, "expected cell is missing")
        elif count > 1:
            _issue(
                issues,
                BenchmarkIssueCode.DUPLICATE_CELL,
                location,
                f"expected cell has {count} observations",
            )

    for index, run in enumerate(materialized):
        location = f"runs[{index}]"
        if run.case_id != plan.case.case_id:
            _issue(
                issues,
                BenchmarkIssueCode.CASE_MISMATCH,
                location,
                "run case_id does not match the benchmark case",
            )
        if run.repetition > plan.case.repetitions:
            _issue(
                issues,
                BenchmarkIssueCode.REPETITION_INVALID,
                location,
                "run repetition exceeds the planned repetition count",
            )
        if run.repository_revision != plan.case.repository_revision:
            _issue(
                issues,
                BenchmarkIssueCode.REPOSITORY_MISMATCH,
                location,
                "run repository revision does not match the pinned baseline",
            )
        if run.scorer_revision != plan.case.scorer_revision:
            _issue(
                issues,
                BenchmarkIssueCode.SCORER_MISMATCH,
                location,
                "run scorer revision does not match the benchmark case",
            )
        expected_config = plan.configuration_for(run.arm).method_config_digest
        if run.method_config_digest != expected_config:
            _issue(
                issues,
                BenchmarkIssueCode.METHOD_CONFIG_MISMATCH,
                location,
                "run method configuration does not match the planned arm",
            )
        if run.model_config_digest != plan.case.model_config_digest:
            _issue(
                issues,
                BenchmarkIssueCode.MODEL_CONFIG_MISMATCH,
                location,
                "run model/provider configuration does not match the benchmark case",
            )
        if plan.case.scorer_hidden and run.scorer_visible:
            _issue(
                issues,
                BenchmarkIssueCode.SCORER_LEAK,
                location,
                "hidden scorer fixtures were visible to the implementation run",
            )

    ordered = tuple(sorted(set(issues)))
    return BenchmarkPreflight(plan_digest=plan.plan_digest, issues=ordered)


@dataclass(frozen=True, slots=True)
class ArmSummary:
    arm: BenchmarkArm
    total_runs: int
    completed_runs: int
    failed_runs: int
    blocked_runs: int
    acceptance_passes: int
    regression_passes: int
    scope_passes: int
    safety_applicable_runs: int
    safety_passes: int
    first_pass_verified_runs: int
    input_token_observations: int
    total_input_tokens: int
    output_token_observations: int
    total_output_tokens: int
    duration_observations: int
    total_duration_ms: int
    total_retries: int
    total_human_interventions: int
    total_changed_files: int
    total_changed_lines: int
    total_rework_units: int

    def to_dict(self) -> dict[str, object]:
        values = {
            field: getattr(self, field)
            for field in self.__dataclass_fields__
            if field != "arm"
        }
        values["arm"] = self.arm.value
        return values


def _summary(arm: BenchmarkArm, runs: tuple[BenchmarkRun, ...]) -> ArmSummary:
    selected = tuple(run for run in runs if run.arm is arm)
    safety = tuple(run for run in selected if run.safety_pass is not None)
    input_values = tuple(run.input_tokens for run in selected if run.input_tokens is not None)
    output_values = tuple(run.output_tokens for run in selected if run.output_tokens is not None)
    duration_values = tuple(run.duration_ms for run in selected if run.duration_ms is not None)
    return ArmSummary(
        arm=arm,
        total_runs=len(selected),
        completed_runs=sum(run.status is BenchmarkRunStatus.COMPLETED for run in selected),
        failed_runs=sum(run.status is BenchmarkRunStatus.FAILED for run in selected),
        blocked_runs=sum(run.status is BenchmarkRunStatus.BLOCKED for run in selected),
        acceptance_passes=sum(run.acceptance_pass for run in selected),
        regression_passes=sum(run.regression_pass for run in selected),
        scope_passes=sum(run.scope_pass for run in selected),
        safety_applicable_runs=len(safety),
        safety_passes=sum(run.safety_pass is True for run in safety),
        first_pass_verified_runs=sum(run.first_pass_verified for run in selected),
        input_token_observations=len(input_values),
        total_input_tokens=sum(input_values),
        output_token_observations=len(output_values),
        total_output_tokens=sum(output_values),
        duration_observations=len(duration_values),
        total_duration_ms=sum(duration_values),
        total_retries=sum(run.retries for run in selected),
        total_human_interventions=sum(run.human_interventions for run in selected),
        total_changed_files=sum(run.changed_files for run in selected),
        total_changed_lines=sum(run.changed_lines for run in selected),
        total_rework_units=sum(run.rework_units for run in selected),
    )


@dataclass(frozen=True, slots=True)
class BenchmarkReport:
    plan_digest: str
    valid_comparison: bool
    issues: tuple[BenchmarkIssue, ...]
    run_digests: tuple[str, ...]
    summaries: tuple[ArmSummary, ...]

    def content_dict(self) -> dict[str, object]:
        return {
            "automatic_winner": None,
            "issues": [issue.to_dict() for issue in self.issues],
            "plan_digest": self.plan_digest,
            "run_digests": list(self.run_digests),
            "summaries": [summary.to_dict() for summary in self.summaries],
            "valid_comparison": self.valid_comparison,
        }

    @property
    def report_digest(self) -> str:
        return _content_digest(self.content_dict())

    def to_dict(self) -> dict[str, object]:
        result = self.content_dict()
        result["report_digest"] = self.report_digest
        return result

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())

    def to_markdown(self) -> str:
        lines = [
            "# SpecGrainBench Report",
            "",
            f"Valid comparison: {'yes' if self.valid_comparison else 'no'}",
            "Automatic winner: none (the deterministic core does not rank methods).",
            "",
        ]
        if self.issues:
            lines.append("## Preflight issues")
            lines.extend(
                f"- `{issue.code.value}` {issue.location}: {issue.message}"
                for issue in self.issues
            )
            lines.append("")
        lines.append("## Arm summaries")
        for summary in self.summaries:
            lines.append(
                f"- {summary.arm.value}: runs={summary.total_runs}, "
                f"completed={summary.completed_runs}, failed={summary.failed_runs}, "
                f"blocked={summary.blocked_runs}, acceptance={summary.acceptance_passes}, "
                f"regression={summary.regression_passes}, scope={summary.scope_passes}"
            )
        lines.extend(("", f"Report digest: `{self.report_digest}`"))
        return "\n".join(lines)


def build_benchmark_report(
    plan: BenchmarkPlan,
    runs: Iterable[BenchmarkRun],
) -> BenchmarkReport:
    """Build a deterministic no-winner report while retaining failed/blocked runs."""

    materialized = tuple(runs)
    preflight = benchmark_preflight(plan, materialized)
    summaries = tuple(_summary(arm, materialized) for arm in BenchmarkArm)
    run_digests = tuple(sorted(run.run_digest for run in materialized))
    return BenchmarkReport(
        plan_digest=plan.plan_digest,
        valid_comparison=preflight.valid,
        issues=preflight.issues,
        run_digests=run_digests,
        summaries=summaries,
    )


__all__ = [
    "BENCHMARK_VERSION",
    "ArmConfiguration",
    "ArmSummary",
    "BenchmarkArm",
    "BenchmarkCase",
    "BenchmarkIssue",
    "BenchmarkIssueCode",
    "BenchmarkPlan",
    "BenchmarkPreflight",
    "BenchmarkReport",
    "BenchmarkRun",
    "BenchmarkRunStatus",
    "BenchmarkValidationError",
    "benchmark_preflight",
    "build_benchmark_report",
]
