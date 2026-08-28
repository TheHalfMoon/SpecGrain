"""Deterministic Grain-readiness evaluation for SpecNode revisions."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum

from .model import SpecNode
from .refinement import validate_refinement

GRAIN_READINESS_VERSION = 1
_RISK_LEVELS = frozenset({"low", "medium", "high", "critical"})


class MinimalityChoice(StrEnum):
    """Declared implementation rung used for Grain readiness."""

    REUSE_EXISTING = "reuse-existing"
    STDLIB = "stdlib"
    NATIVE = "native"
    INSTALLED_DEPENDENCY = "installed-dependency"
    NEW_CODE = "new-code"


class SafetyStatus(StrEnum):
    """Declared safety-planning status for a Grain candidate."""

    NONE_IDENTIFIED = "none-identified"
    REQUIREMENTS_DEFINED = "requirements-defined"


class ReadinessIssueCode(StrEnum):
    """Stable machine-readable Grain-readiness blocker codes."""

    ACCEPTANCE_REQUIRED = "ACCEPTANCE_REQUIRED"
    CANDIDATE_MISSING = "CANDIDATE_MISSING"
    CANDIDATE_REVISION_MISMATCH = "CANDIDATE_REVISION_MISMATCH"
    CHANGE_SURFACE_REQUIRED = "CHANGE_SURFACE_REQUIRED"
    CONTEXT_BUDGET_EXCEEDED = "CONTEXT_BUDGET_EXCEEDED"
    CONTEXT_BUDGET_INVALID = "CONTEXT_BUDGET_INVALID"
    CONTEXT_ESTIMATE_INVALID = "CONTEXT_ESTIMATE_INVALID"
    EVIDENCE_REQUIRED_INVALID = "EVIDENCE_REQUIRED_INVALID"
    MINIMALITY_CHOICE_INVALID = "MINIMALITY_CHOICE_INVALID"
    MINIMALITY_RATIONALE_REQUIRED = "MINIMALITY_RATIONALE_REQUIRED"
    NOT_LEAF = "NOT_LEAF"
    READINESS_DECLARATION_INVALID = "READINESS_DECLARATION_INVALID"
    READINESS_VERSION_INVALID = "READINESS_VERSION_INVALID"
    RECOVERY_REQUIRED = "RECOVERY_REQUIRED"
    REFINEMENT_INVALID = "REFINEMENT_INVALID"
    RISK_LEVEL_INVALID = "RISK_LEVEL_INVALID"
    SAFETY_REQUIREMENTS_INVALID = "SAFETY_REQUIREMENTS_INVALID"
    SAFETY_STATUS_INVALID = "SAFETY_STATUS_INVALID"
    SCOPE_REQUIRED = "SCOPE_REQUIRED"
    SOURCE_STATE_INVALID = "SOURCE_STATE_INVALID"
    UNRESOLVED_DECISIONS_INVALID = "UNRESOLVED_DECISIONS_INVALID"
    UNRESOLVED_DECISIONS_PRESENT = "UNRESOLVED_DECISIONS_PRESENT"


@dataclass(frozen=True, slots=True)
class ReadinessIssue:
    """One deterministic Grain-readiness blocker."""

    code: ReadinessIssueCode
    field: str
    message: str


@dataclass(frozen=True, slots=True)
class GrainReadinessReport:
    """Readiness result bound to one exact semantic SpecNode revision."""

    node_id: str
    revision_digest: str
    issues: tuple[ReadinessIssue, ...]

    @property
    def is_ready(self) -> bool:
        return not self.issues


class GrainReadinessError(ValueError):
    """Raised when a candidate does not satisfy Grain-readiness v1."""

    def __init__(self, report: GrainReadinessReport) -> None:
        self.report = report
        summary = "; ".join(issue.message for issue in report.issues)
        super().__init__(summary or "Grain readiness failed")


def _issue_key(issue: ReadinessIssue) -> tuple[str, str, str]:
    return (issue.code.value, issue.field, issue.message)


def _report(node: SpecNode, issues: list[ReadinessIssue]) -> GrainReadinessReport:
    return GrainReadinessReport(
        node_id=node.id,
        revision_digest=node.revision_digest,
        issues=tuple(sorted(issues, key=_issue_key)),
    )


def _is_non_empty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _string_sequence(value: object, *, allow_empty: bool) -> tuple[str, ...] | None:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        return None

    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        if not _is_non_empty_text(item) or item in seen:
            return None
        assert isinstance(item, str)
        seen.add(item)
        normalized.append(item)

    if not allow_empty and not normalized:
        return None
    return tuple(normalized)


def _valid_recovery(value: object) -> bool:
    if _is_non_empty_text(value):
        return True
    return isinstance(value, Mapping) and bool(value)


def _evaluate_risk(node: SpecNode, issues: list[ReadinessIssue]) -> None:
    level = node.risk.get("level")
    if not isinstance(level, str) or level not in _RISK_LEVELS:
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.RISK_LEVEL_INVALID,
                "risk.level",
                "risk.level must be one of: critical, high, low, medium",
            )
        )

    if not _valid_recovery(node.risk.get("recovery")):
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.RECOVERY_REQUIRED,
                "risk.recovery",
                "risk.recovery must be a non-empty string or non-empty object",
            )
        )


def _evaluate_context(node: SpecNode, issues: list[ReadinessIssue]) -> None:
    budget = node.context.get("budget_tokens")
    estimate = node.context.get("estimated_tokens")

    budget_valid = _is_integer(budget) and budget > 0
    estimate_valid = _is_integer(estimate) and estimate >= 0

    if not budget_valid:
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.CONTEXT_BUDGET_INVALID,
                "context.budget_tokens",
                "context.budget_tokens must be a positive integer",
            )
        )

    if not estimate_valid:
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.CONTEXT_ESTIMATE_INVALID,
                "context.estimated_tokens",
                "context.estimated_tokens must be a non-negative integer",
            )
        )

    if budget_valid and estimate_valid and estimate > budget:
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.CONTEXT_BUDGET_EXCEEDED,
                "context.estimated_tokens",
                f"context.estimated_tokens {estimate} exceeds budget_tokens {budget}",
            )
        )


def _evaluate_evidence(node: SpecNode, issues: list[ReadinessIssue]) -> None:
    if _string_sequence(node.evidence.get("required"), allow_empty=False) is None:
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.EVIDENCE_REQUIRED_INVALID,
                "evidence.required",
                "evidence.required must contain unique non-empty identifiers",
            )
        )


def _evaluate_minimality(
    readiness: Mapping[str, object], issues: list[ReadinessIssue]
) -> None:
    minimality = readiness.get("minimality")
    if not isinstance(minimality, Mapping):
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.MINIMALITY_CHOICE_INVALID,
                "metadata.readiness.minimality.choice",
                "readiness minimality must declare a canonical choice",
            )
        )
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.MINIMALITY_RATIONALE_REQUIRED,
                "metadata.readiness.minimality.rationale",
                "readiness minimality rationale must be non-empty",
            )
        )
        return

    choice = minimality.get("choice")
    try:
        MinimalityChoice(choice)
    except (TypeError, ValueError):
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.MINIMALITY_CHOICE_INVALID,
                "metadata.readiness.minimality.choice",
                "readiness minimality choice is not canonical",
            )
        )

    if not _is_non_empty_text(minimality.get("rationale")):
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.MINIMALITY_RATIONALE_REQUIRED,
                "metadata.readiness.minimality.rationale",
                "readiness minimality rationale must be non-empty",
            )
        )


def _evaluate_safety(readiness: Mapping[str, object], issues: list[ReadinessIssue]) -> None:
    safety = readiness.get("safety")
    if not isinstance(safety, Mapping):
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.SAFETY_STATUS_INVALID,
                "metadata.readiness.safety.status",
                "readiness safety status is not canonical",
            )
        )
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.SAFETY_REQUIREMENTS_INVALID,
                "metadata.readiness.safety.requirements",
                "readiness safety requirements are inconsistent with status",
            )
        )
        return

    status_value = safety.get("status")
    try:
        status = SafetyStatus(status_value)
    except (TypeError, ValueError):
        status = None
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.SAFETY_STATUS_INVALID,
                "metadata.readiness.safety.status",
                "readiness safety status is not canonical",
            )
        )

    requirements = _string_sequence(safety.get("requirements"), allow_empty=True)
    requirements_valid = requirements is not None
    if status is SafetyStatus.NONE_IDENTIFIED:
        requirements_valid = requirements_valid and not requirements
    elif status is SafetyStatus.REQUIREMENTS_DEFINED:
        requirements_valid = requirements_valid and bool(requirements)
    elif status is None:
        requirements_valid = False

    if not requirements_valid:
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.SAFETY_REQUIREMENTS_INVALID,
                "metadata.readiness.safety.requirements",
                "readiness safety requirements are inconsistent with status",
            )
        )


def _evaluate_readiness_metadata(node: SpecNode, issues: list[ReadinessIssue]) -> None:
    readiness = node.metadata.get("readiness")
    if not isinstance(readiness, Mapping):
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.READINESS_DECLARATION_INVALID,
                "metadata.readiness",
                "metadata.readiness must be an object",
            )
        )
        if not node.change_surface:
            issues.append(
                ReadinessIssue(
                    ReadinessIssueCode.CHANGE_SURFACE_REQUIRED,
                    "change_surface",
                    "change_surface must be non-empty or have a readiness exception",
                )
            )
        return

    version = readiness.get("version")
    if not _is_integer(version) or version != GRAIN_READINESS_VERSION:
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.READINESS_VERSION_INVALID,
                "metadata.readiness.version",
                f"metadata.readiness.version must equal {GRAIN_READINESS_VERSION}",
            )
        )

    decisions = _string_sequence(readiness.get("unresolved_decisions"), allow_empty=True)
    if decisions is None:
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.UNRESOLVED_DECISIONS_INVALID,
                "metadata.readiness.unresolved_decisions",
                "unresolved_decisions must be an explicit sequence of unique non-empty strings",
            )
        )
    elif decisions:
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.UNRESOLVED_DECISIONS_PRESENT,
                "metadata.readiness.unresolved_decisions",
                "unresolved_decisions must be empty before Grain readiness",
            )
        )

    if not node.change_surface:
        exception = readiness.get("change_surface_exception")
        if not _is_non_empty_text(exception):
            issues.append(
                ReadinessIssue(
                    ReadinessIssueCode.CHANGE_SURFACE_REQUIRED,
                    "change_surface",
                    "change_surface must be non-empty or have a readiness exception",
                )
            )
    elif "change_surface_exception" in readiness and not _is_non_empty_text(
        readiness.get("change_surface_exception")
    ):
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.CHANGE_SURFACE_REQUIRED,
                "metadata.readiness.change_surface_exception",
                "change_surface_exception must be non-empty when present",
            )
        )

    _evaluate_minimality(readiness, issues)
    _evaluate_safety(readiness, issues)


def _evaluate_intrinsic(node: SpecNode, issues: list[ReadinessIssue]) -> None:
    if node.state != "REFINING":
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.SOURCE_STATE_INVALID,
                "state",
                "Grain readiness requires candidate state REFINING",
            )
        )
    if node.children:
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.NOT_LEAF,
                "children",
                "Grain readiness requires a refinement leaf",
            )
        )
    if not node.acceptance:
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.ACCEPTANCE_REQUIRED,
                "acceptance",
                "at least one acceptance condition is required",
            )
        )
    if not node.scope_in:
        issues.append(
            ReadinessIssue(
                ReadinessIssueCode.SCOPE_REQUIRED,
                "scope_in",
                "scope_in must contain at least one authorized behavior or surface",
            )
        )

    _evaluate_risk(node, issues)
    _evaluate_context(node, issues)
    _evaluate_evidence(node, issues)
    _evaluate_readiness_metadata(node, issues)


def evaluate_grain_readiness(
    node: SpecNode, forest: Iterable[SpecNode]
) -> GrainReadinessReport:
    """Evaluate Grain-readiness v1 without mutating lifecycle state."""

    if not isinstance(node, SpecNode):
        raise TypeError("node must be a SpecNode")

    materialized = tuple(forest)
    refinement_issues = validate_refinement(materialized)
    if refinement_issues:
        issues = [
            ReadinessIssue(
                ReadinessIssueCode.REFINEMENT_INVALID,
                f"forest.{issue.node_id}",
                f"{issue.code.value}: {issue.message}",
            )
            for issue in refinement_issues
        ]
        return _report(node, issues)

    candidates = [candidate for candidate in materialized if candidate.id == node.id]
    if not candidates:
        return _report(
            node,
            [
                ReadinessIssue(
                    ReadinessIssueCode.CANDIDATE_MISSING,
                    "id",
                    f"candidate {node.id} is not present in the refinement forest",
                )
            ],
        )

    forest_node = candidates[0]
    if forest_node.revision_digest != node.revision_digest:
        return _report(
            node,
            [
                ReadinessIssue(
                    ReadinessIssueCode.CANDIDATE_REVISION_MISMATCH,
                    "revision_digest",
                    "candidate semantic revision does not match the refinement forest copy",
                )
            ],
        )

    issues: list[ReadinessIssue] = []
    _evaluate_intrinsic(node, issues)
    return _report(node, issues)


def require_grain_readiness(
    node: SpecNode, forest: Iterable[SpecNode]
) -> GrainReadinessReport:
    """Return a passing report or raise with the exact failed report."""

    report = evaluate_grain_readiness(node, forest)
    if not report.is_ready:
        raise GrainReadinessError(report)
    return report
