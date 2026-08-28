"""Deterministic lightweight method-profile requirements."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum

from .model import SpecNode

METHOD_PROFILE_VERSION = 1


class MethodProfileName(StrEnum):
    """Canonical adaptive delivery profiles."""

    QUICK = "quick"
    DMAIC_LITE = "dmaic-lite"
    DMADV_LITE = "dmadv-lite"
    EXPERIMENT = "experiment"
    CONTROLLED = "controlled"


@dataclass(frozen=True, slots=True)
class MethodProfile:
    """One bounded profile expressed as readiness and evidence requirements."""

    name: MethodProfileName
    required_metadata: tuple[str, ...]
    required_evidence: tuple[str, ...]


class MethodIssueCode(StrEnum):
    """Stable method-profile blocker codes."""

    PROFILE_INVALID = "PROFILE_INVALID"
    METADATA_INVALID = "METADATA_INVALID"
    METADATA_MISSING = "METADATA_MISSING"
    EVIDENCE_MISSING = "EVIDENCE_MISSING"


@dataclass(frozen=True, slots=True, order=True)
class MethodIssue:
    """One deterministic method-profile readiness blocker."""

    code: MethodIssueCode
    field: str
    message: str


@dataclass(frozen=True, slots=True)
class MethodReport:
    """Method-profile result bound to one exact SpecNode revision."""

    node_id: str
    revision_digest: str
    profile: MethodProfileName | None
    issues: tuple[MethodIssue, ...]

    @property
    def is_ready(self) -> bool:
        """Return whether all profile-specific requirements pass."""

        return not self.issues


_PROFILES = {
    MethodProfileName.QUICK: MethodProfile(MethodProfileName.QUICK, (), ()),
    MethodProfileName.DMAIC_LITE: MethodProfile(
        MethodProfileName.DMAIC_LITE,
        ("baseline", "cause", "control"),
        ("baseline", "regression"),
    ),
    MethodProfileName.DMADV_LITE: MethodProfile(
        MethodProfileName.DMADV_LITE,
        ("value", "baseline", "analysis", "design"),
        ("baseline", "verification"),
    ),
    MethodProfileName.EXPERIMENT: MethodProfile(
        MethodProfileName.EXPERIMENT,
        ("hypothesis", "resource_boundary", "decision_rule", "non_production"),
        ("experiment-result",),
    ),
    MethodProfileName.CONTROLLED: MethodProfile(
        MethodProfileName.CONTROLLED,
        ("rollback", "review_separation", "control"),
        ("rollback", "independent-review"),
    ),
}


def get_method_profile(name: MethodProfileName | str) -> MethodProfile:
    """Return one canonical immutable method profile."""

    try:
        canonical = MethodProfileName(name)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"unknown method profile: {name!r}") from exc
    return _PROFILES[canonical]


def _non_empty(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, Mapping):
        return bool(value)
    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        return bool(value)
    return value is True


def _required_evidence(node: SpecNode) -> tuple[str, ...]:
    raw = node.evidence.get("required")
    if (
        isinstance(raw, Sequence)
        and not isinstance(raw, str | bytes | bytearray)
        and all(isinstance(item, str) for item in raw)
    ):
        return tuple(raw)
    return ()


def evaluate_method_profile(node: SpecNode) -> MethodReport:
    """Evaluate only profile-specific requirements without mutating the node."""

    if not isinstance(node, SpecNode):
        raise TypeError("node must be a SpecNode")
    try:
        profile = get_method_profile(node.method)
    except ValueError:
        issue = MethodIssue(
            MethodIssueCode.PROFILE_INVALID,
            "method",
            "method must be one of: controlled, dmaic-lite, dmadv-lite, experiment, quick",
        )
        return MethodReport(node.id, node.revision_digest, None, (issue,))

    issues: list[MethodIssue] = []
    method_meta = node.metadata.get("method")
    if profile.required_metadata:
        if not isinstance(method_meta, Mapping):
            issues.append(
                MethodIssue(
                    MethodIssueCode.METADATA_INVALID,
                    "metadata.method",
                    f"{profile.name.value} requires metadata.method object",
                )
            )
            method_meta = {}
        for key in profile.required_metadata:
            if not _non_empty(method_meta.get(key)):
                issues.append(
                    MethodIssue(
                        MethodIssueCode.METADATA_MISSING,
                        f"metadata.method.{key}",
                        f"{profile.name.value} requires non-empty method metadata {key!r}",
                    )
                )

    declared_evidence = set(_required_evidence(node))
    for evidence_id in profile.required_evidence:
        if evidence_id not in declared_evidence:
            issues.append(
                MethodIssue(
                    MethodIssueCode.EVIDENCE_MISSING,
                    "evidence.required",
                    f"{profile.name.value} requires evidence identifier {evidence_id!r}",
                )
            )

    return MethodReport(
        node.id,
        node.revision_digest,
        profile.name,
        tuple(sorted(issues)),
    )

@dataclass(frozen=True, slots=True)
class MethodReadinessReport:
    """Composite core-Grain and profile-specific readiness result."""

    core: object
    method: MethodReport

    @property
    def is_ready(self) -> bool:
        """Return whether both core Grain and method-profile gates pass."""

        return bool(getattr(self.core, "is_ready", False)) and self.method.is_ready


class MethodReadinessError(ValueError):
    """Raised when core or method-specific readiness fails."""

    def __init__(self, report: MethodReadinessReport) -> None:
        self.report = report
        super().__init__("method-aware Grain readiness failed")


def evaluate_method_readiness(node: SpecNode, forest: object) -> MethodReadinessReport:
    """Compose existing Grain readiness with the selected method-profile gate."""

    from .readiness import evaluate_grain_readiness

    core = evaluate_grain_readiness(node, forest)  # type: ignore[arg-type]
    return MethodReadinessReport(core=core, method=evaluate_method_profile(node))


def require_method_readiness(node: SpecNode, forest: object) -> MethodReadinessReport:
    """Return the composite report or raise without mutating lifecycle state."""

    report = evaluate_method_readiness(node, forest)
    if not report.is_ready:
        raise MethodReadinessError(report)
    return report
