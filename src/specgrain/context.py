"""Deterministic revision-bound context budget accounting."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

from .repository import RepositoryMap


class ContextRequirement(StrEnum):
    """Whether a context source is mandatory or may be omitted to fit policy."""

    REQUIRED = "required"
    OPTIONAL = "optional"


class ContextValidationError(ValueError):
    """Raised when context records or collections violate the public contract."""


class ContextBudgetIssueCode(StrEnum):
    """Stable machine-readable required-context budget blocker codes."""

    REQUIRED_BYTES_EXCEEDED = "REQUIRED_BYTES_EXCEEDED"
    REQUIRED_SOURCE_COUNT_EXCEEDED = "REQUIRED_SOURCE_COUNT_EXCEEDED"
    REQUIRED_TOKENS_EXCEEDED = "REQUIRED_TOKENS_EXCEEDED"


@dataclass(frozen=True, slots=True)
class ContextSource:
    """One immutable revision-bound context accounting source."""

    source_id: str
    provenance: str
    selection_reason: str
    revision: str
    size_bytes: int
    token_cost: int
    requirement: ContextRequirement | str = ContextRequirement.REQUIRED
    priority: int = 0

    def __post_init__(self) -> None:
        for field_name in ("source_id", "provenance", "selection_reason", "revision"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ContextValidationError(f"{field_name} must be a non-empty string")

        for field_name in ("size_bytes", "token_cost", "priority"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ContextValidationError(f"{field_name} must be a non-negative integer")

        try:
            requirement = ContextRequirement(self.requirement)
        except (TypeError, ValueError) as exc:
            raise ContextValidationError(
                "requirement must be 'required' or 'optional'"
            ) from exc
        object.__setattr__(self, "requirement", requirement)

    def to_dict(self) -> dict[str, object]:
        return {
            "priority": self.priority,
            "provenance": self.provenance,
            "requirement": self.requirement.value,
            "revision": self.revision,
            "selection_reason": self.selection_reason,
            "size_bytes": self.size_bytes,
            "source_id": self.source_id,
            "token_cost": self.token_cost,
        }


@dataclass(frozen=True, slots=True)
class ContextBudgetPolicy:
    """Configured context ceilings for one deterministic plan."""

    max_tokens: int
    max_bytes: int | None = None
    max_sources: int | None = None

    def __post_init__(self) -> None:
        if (
            isinstance(self.max_tokens, bool)
            or not isinstance(self.max_tokens, int)
            or self.max_tokens <= 0
        ):
            raise ContextValidationError("max_tokens must be a positive integer")
        for field_name in ("max_bytes", "max_sources"):
            value = getattr(self, field_name)
            if value is None:
                continue
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ContextValidationError(f"{field_name} must be a positive integer or None")

    def to_dict(self) -> dict[str, int | None]:
        return {
            "max_bytes": self.max_bytes,
            "max_sources": self.max_sources,
            "max_tokens": self.max_tokens,
        }


@dataclass(frozen=True, slots=True, order=True)
class ContextBudgetIssue:
    """One deterministic required-context budget blocker."""

    code: ContextBudgetIssueCode
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code.value, "message": self.message}


@dataclass(frozen=True, slots=True)
class ContextBudgetReport:
    """Deterministic selected context plan and budget result."""

    fits: bool
    required_ids: tuple[str, ...]
    selected_ids: tuple[str, ...]
    omitted_optional_ids: tuple[str, ...]
    required_bytes: int
    required_tokens: int
    required_source_count: int
    selected_bytes: int
    selected_tokens: int
    selected_source_count: int
    issues: tuple[ContextBudgetIssue, ...]
    plan_digest: str

    def to_dict(self) -> dict[str, object]:
        return {
            "fits": self.fits,
            "issues": [issue.to_dict() for issue in self.issues],
            "omitted_optional_ids": list(self.omitted_optional_ids),
            "plan_digest": self.plan_digest,
            "required_bytes": self.required_bytes,
            "required_ids": list(self.required_ids),
            "required_source_count": self.required_source_count,
            "required_tokens": self.required_tokens,
            "selected_bytes": self.selected_bytes,
            "selected_ids": list(self.selected_ids),
            "selected_source_count": self.selected_source_count,
            "selected_tokens": self.selected_tokens,
        }


class ContextBudgetError(ValueError):
    """Raised when required context cannot fit the configured policy."""

    def __init__(self, report: ContextBudgetReport) -> None:
        self.report = report
        summary = "; ".join(issue.message for issue in report.issues)
        super().__init__(summary or "context budget failed")


def _materialize_sources(sources: Iterable[ContextSource]) -> tuple[ContextSource, ...]:
    materialized = tuple(sources)
    for index, source in enumerate(materialized):
        if not isinstance(source, ContextSource):
            raise ContextValidationError(f"sources[{index}] must be a ContextSource")

    duplicates = sorted(
        source_id
        for source_id, count in Counter(source.source_id for source in materialized).items()
        if count > 1
    )
    if duplicates:
        joined = ", ".join(duplicates)
        raise ContextValidationError(f"duplicate source_id values: {joined}")
    return tuple(sorted(materialized, key=lambda source: source.source_id))


def validate_context_sources(sources: Iterable[ContextSource]) -> tuple[ContextSource, ...]:
    """Validate and return sources in canonical source-ID order."""

    return _materialize_sources(sources)


def _within_policy(
    *, bytes_used: int, tokens_used: int, source_count: int, policy: ContextBudgetPolicy
) -> bool:
    if tokens_used > policy.max_tokens:
        return False
    if policy.max_bytes is not None and bytes_used > policy.max_bytes:
        return False
    return policy.max_sources is None or source_count <= policy.max_sources


def _required_issues(
    *, bytes_used: int, tokens_used: int, source_count: int, policy: ContextBudgetPolicy
) -> tuple[ContextBudgetIssue, ...]:
    issues: list[ContextBudgetIssue] = []
    if policy.max_bytes is not None and bytes_used > policy.max_bytes:
        issues.append(
            ContextBudgetIssue(
                ContextBudgetIssueCode.REQUIRED_BYTES_EXCEEDED,
                f"required context uses {bytes_used} bytes; policy allows {policy.max_bytes}",
            )
        )
    if policy.max_sources is not None and source_count > policy.max_sources:
        issues.append(
            ContextBudgetIssue(
                ContextBudgetIssueCode.REQUIRED_SOURCE_COUNT_EXCEEDED,
                f"required context uses {source_count} sources; policy allows {policy.max_sources}",
            )
        )
    if tokens_used > policy.max_tokens:
        issues.append(
            ContextBudgetIssue(
                ContextBudgetIssueCode.REQUIRED_TOKENS_EXCEEDED,
                f"required context uses {tokens_used} tokens; policy allows {policy.max_tokens}",
            )
        )
    return tuple(sorted(issues, key=lambda issue: issue.code.value))


def _digest_plan(
    *,
    policy: ContextBudgetPolicy,
    sources: tuple[ContextSource, ...],
    required_ids: tuple[str, ...],
    selected_ids: tuple[str, ...],
    omitted_optional_ids: tuple[str, ...],
    required_bytes: int,
    required_tokens: int,
    selected_bytes: int,
    selected_tokens: int,
    issues: tuple[ContextBudgetIssue, ...],
) -> str:
    payload = {
        "issues": [issue.to_dict() for issue in issues],
        "omitted_optional_ids": list(omitted_optional_ids),
        "policy": policy.to_dict(),
        "required": {
            "bytes": required_bytes,
            "ids": list(required_ids),
            "source_count": len(required_ids),
            "tokens": required_tokens,
        },
        "selected": {
            "bytes": selected_bytes,
            "ids": list(selected_ids),
            "source_count": len(selected_ids),
            "tokens": selected_tokens,
        },
        "sources": [source.to_dict() for source in sources],
    }
    encoded = json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def evaluate_context_budget(
    sources: Iterable[ContextSource], policy: ContextBudgetPolicy
) -> ContextBudgetReport:
    """Return a deterministic context plan without reading or mutating source content."""

    if not isinstance(policy, ContextBudgetPolicy):
        raise ContextValidationError("policy must be a ContextBudgetPolicy")
    canonical = validate_context_sources(sources)
    required = tuple(
        source for source in canonical if source.requirement is ContextRequirement.REQUIRED
    )
    optional = tuple(
        sorted(
            (source for source in canonical if source.requirement is ContextRequirement.OPTIONAL),
            key=lambda source: (source.priority, source.source_id),
        )
    )

    required_ids = tuple(source.source_id for source in required)
    required_bytes = sum(source.size_bytes for source in required)
    required_tokens = sum(source.token_cost for source in required)
    issues = _required_issues(
        bytes_used=required_bytes,
        tokens_used=required_tokens,
        source_count=len(required),
        policy=policy,
    )

    selected: list[ContextSource] = list(required)
    omitted: list[ContextSource] = []
    if not issues:
        selected_bytes = required_bytes
        selected_tokens = required_tokens
        for source in optional:
            candidate_bytes = selected_bytes + source.size_bytes
            candidate_tokens = selected_tokens + source.token_cost
            candidate_count = len(selected) + 1
            if _within_policy(
                bytes_used=candidate_bytes,
                tokens_used=candidate_tokens,
                source_count=candidate_count,
                policy=policy,
            ):
                selected.append(source)
                selected_bytes = candidate_bytes
                selected_tokens = candidate_tokens
            else:
                omitted.append(source)
    else:
        omitted.extend(optional)

    selected_ids = tuple(sorted(source.source_id for source in selected))
    omitted_ids = tuple(sorted(source.source_id for source in omitted))
    selected_bytes = sum(source.size_bytes for source in selected)
    selected_tokens = sum(source.token_cost for source in selected)
    digest = _digest_plan(
        policy=policy,
        sources=canonical,
        required_ids=required_ids,
        selected_ids=selected_ids,
        omitted_optional_ids=omitted_ids,
        required_bytes=required_bytes,
        required_tokens=required_tokens,
        selected_bytes=selected_bytes,
        selected_tokens=selected_tokens,
        issues=issues,
    )
    return ContextBudgetReport(
        fits=not issues,
        required_ids=required_ids,
        selected_ids=selected_ids,
        omitted_optional_ids=omitted_ids,
        required_bytes=required_bytes,
        required_tokens=required_tokens,
        required_source_count=len(required),
        selected_bytes=selected_bytes,
        selected_tokens=selected_tokens,
        selected_source_count=len(selected),
        issues=issues,
        plan_digest=digest,
    )


def require_context_budget(
    sources: Iterable[ContextSource], policy: ContextBudgetPolicy
) -> ContextBudgetReport:
    """Return the passing report or raise with the exact deterministic failure."""

    report = evaluate_context_budget(sources, policy)
    if not report.fits:
        raise ContextBudgetError(report)
    return report


def repository_map_context_source(
    repository_map: RepositoryMap,
    *,
    token_cost: int,
    selection_reason: str,
    source_id: str = "repository-map",
    requirement: ContextRequirement | str = ContextRequirement.REQUIRED,
    priority: int = 0,
) -> ContextSource:
    """Bind normalized Repository Scan facts into one context accounting source."""

    if not isinstance(repository_map, RepositoryMap):
        raise ContextValidationError("repository_map must be a RepositoryMap")
    encoded = json.dumps(
        repository_map.to_dict(),
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return ContextSource(
        source_id=source_id,
        provenance=f"repository-map:{repository_map.repository_name}",
        selection_reason=selection_reason,
        revision=f"sha256:{repository_map.content_digest}",
        size_bytes=len(encoded),
        token_cost=token_cost,
        requirement=requirement,
        priority=priority,
    )
