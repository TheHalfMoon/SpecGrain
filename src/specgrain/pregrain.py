"""Bounded native preparation of authored candidates through Grain state."""

from __future__ import annotations

import os
import tempfile
from collections.abc import Sequence
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path

from .dependency import validate_dependencies
from .lifecycle import SpecState, require_transition_allowed
from .model import SpecNode, SpecValidationError, is_spec_id
from .readiness import (
    GRAIN_READINESS_VERSION,
    GrainReadinessReport,
    MinimalityChoice,
    SafetyStatus,
    evaluate_grain_readiness,
)
from .refinement import validate_refinement
from .store import (
    LocalProject,
    StoreError,
    StoreValidationError,
    _json_text,
    _parse_json_text,
    _read_text,
    load_project,
)

_RISK_LEVELS = frozenset({"low", "medium", "high", "critical"})


@dataclass(frozen=True, slots=True)
class PreGrainMutationResult:
    """One exact bounded pre-Grain mutation result."""

    node: SpecNode
    source_state: SpecState

    def to_dict(self) -> dict[str, str]:
        return {
            "file": f".specgrain/specs/{self.node.id}.json",
            "revision_digest": self.node.revision_digest,
            "source_state": self.source_state.value,
            "spec_id": self.node.id,
            "state": self.node.state,
        }


class GrainPromotionBlockedError(StoreValidationError):
    """Raised when the exact REFINING candidate does not pass Grain readiness."""

    def __init__(self, report: GrainReadinessReport) -> None:
        self.report = report
        codes = ", ".join(issue.code.value for issue in report.issues)
        super().__init__(
            f".specgrain/specs/{report.node_id}.json",
            f"Grain readiness blocked: {codes}",
        )


def _text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise StoreValidationError("pregrain", f"{field} must be non-empty text")
    return value.strip()


def _texts(
    values: Sequence[str],
    field: str,
    *,
    allow_empty: bool,
) -> tuple[str, ...]:
    if isinstance(values, str | bytes | bytearray):
        raise StoreValidationError("pregrain", f"{field} must be a sequence")
    normalized: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = _text(value, field)
        if item in seen:
            raise StoreValidationError("pregrain", f"{field} must not contain duplicates")
        seen.add(item)
        normalized.append(item)
    if not allow_empty and not normalized:
        raise StoreValidationError("pregrain", f"{field} must contain at least one value")
    return tuple(normalized)


def _validated_project(root: str | os.PathLike[str]) -> LocalProject:
    project = load_project(root)
    refinement_issues = validate_refinement(project.specs)
    if refinement_issues:
        first = refinement_issues[0]
        raise StoreValidationError(
            ".specgrain/specs",
            f"existing refinement is invalid: {first.code.value}: {first.message}",
        )
    dependency_issues = validate_dependencies(project.specs)
    if dependency_issues:
        first = dependency_issues[0]
        raise StoreValidationError(
            ".specgrain/specs",
            f"existing dependencies are invalid: {first.code.value}: {first.message}",
        )
    return project


def _target(
    root: str | os.PathLike[str],
    spec_id: str,
    source_state: SpecState,
) -> tuple[LocalProject, SpecNode]:
    if not is_spec_id(spec_id):
        raise StoreValidationError(
            ".specgrain/specs",
            "spec_id must match 'SG-' followed by exactly six decimal digits",
        )
    project = _validated_project(root)
    by_id = {node.id: node for node in project.specs}
    node = by_id.get(spec_id)
    if node is None:
        raise StoreValidationError(
            f".specgrain/specs/{spec_id}.json",
            "spec does not exist",
        )
    if node.state != source_state.value:
        raise StoreValidationError(
            f".specgrain/specs/{spec_id}.json",
            f"operation requires source state {source_state.value}; found {node.state}",
        )
    return project, node


def _validate_proposed(project: LocalProject, replacement: SpecNode) -> tuple[SpecNode, ...]:
    proposed = tuple(
        replacement if node.id == replacement.id else node for node in project.specs
    )
    refinement_issues = validate_refinement(proposed)
    if refinement_issues:
        first = refinement_issues[0]
        raise StoreValidationError(
            ".specgrain/specs",
            f"proposed refinement is invalid: {first.code.value}: {first.message}",
        )
    dependency_issues = validate_dependencies(proposed)
    if dependency_issues:
        first = dependency_issues[0]
        raise StoreValidationError(
            ".specgrain/specs",
            f"proposed dependencies are invalid: {first.code.value}: {first.message}",
        )
    return proposed


def _replace_spec_exact(path: Path, before_text: str, after: SpecNode, location: str) -> None:
    if _read_text(path, location) != before_text:
        raise StoreValidationError(location, "spec changed during pre-Grain mutation")

    descriptor: int | None = None
    temp_path: Path | None = None
    try:
        descriptor, raw_temp = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
        )
        temp_path = Path(raw_temp)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            descriptor = None
            handle.write(_json_text(after.to_dict()))
            handle.flush()
            os.fsync(handle.fileno())
        if _read_text(path, location) != before_text:
            raise StoreValidationError(location, "spec changed during pre-Grain mutation")
        os.replace(temp_path, path)
        temp_path = None
    except StoreError:
        raise
    except OSError as exc:
        raise StoreValidationError(location, f"cannot replace spec: {exc}") from exc
    finally:
        if descriptor is not None:
            with suppress(OSError):
                os.close(descriptor)
        if temp_path is not None:
            with suppress(OSError):
                temp_path.unlink(missing_ok=True)


def _persist(project: LocalProject, before: SpecNode, after: SpecNode) -> SpecNode:
    _validate_proposed(project, after)
    location = f".specgrain/specs/{before.id}.json"
    path = project.root / location
    before_text = _read_text(path, location)
    try:
        current = SpecNode.from_dict(_parse_json_text(before_text, location))
    except SpecValidationError as exc:
        raise StoreValidationError(location, f"invalid SpecNode: {exc}") from exc
    if current.to_dict() != before.to_dict():
        raise StoreValidationError(location, "spec changed before pre-Grain mutation")

    _replace_spec_exact(path, before_text, after, location)
    if _read_text(path, location) != _json_text(after.to_dict()):
        raise StoreValidationError(location, "spec postimage confirmation failed")

    confirmed = _validated_project(project.root)
    confirmed_by_id = {node.id: node for node in confirmed.specs}
    stored = confirmed_by_id.get(after.id)
    if stored is None or stored.to_dict() != after.to_dict():
        raise StoreValidationError(location, "stored spec does not match expected postimage")
    return stored


def _node_from_data(data: dict[str, object], location: str) -> SpecNode:
    try:
        return SpecNode.from_dict(data)
    except SpecValidationError as exc:
        raise StoreValidationError(location, f"invalid shaped SpecNode: {exc}") from exc


def shape_draft_spec(
    root: str | os.PathLike[str],
    *,
    spec_id: str,
    scope_in: Sequence[str],
    scope_out: Sequence[str] = (),
    acceptance: Sequence[str],
    dependencies: Sequence[str] = (),
    risk_level: str,
    recovery: str,
    context_budget: int,
    context_estimate: int,
    change_surface: Sequence[str] = (),
    change_surface_exception: str | None = None,
    evidence: Sequence[str],
    minimality_choice: str,
    minimality_rationale: str,
    safety_status: str,
    safety_requirements: Sequence[str] = (),
) -> PreGrainMutationResult:
    """Populate one DRAFT candidate explicitly and transition it to SHAPED."""

    project, node = _target(root, spec_id, SpecState.DRAFT)
    require_transition_allowed(node.state, SpecState.SHAPED)

    scope_in_values = _texts(scope_in, "scope_in", allow_empty=False)
    scope_out_values = _texts(scope_out, "scope_out", allow_empty=True)
    acceptance_values = _texts(acceptance, "acceptance", allow_empty=False)
    dependency_values = _texts(dependencies, "dependencies", allow_empty=True)
    for dependency_id in dependency_values:
        if not is_spec_id(dependency_id):
            raise StoreValidationError(
                "pregrain",
                f"dependency {dependency_id!r} is not a canonical SpecNode ID",
            )

    if risk_level not in _RISK_LEVELS:
        raise StoreValidationError(
            "pregrain",
            "risk_level must be one of: critical, high, low, medium",
        )
    recovery_value = _text(recovery, "recovery")
    if isinstance(context_budget, bool) or not isinstance(context_budget, int):
        raise StoreValidationError("pregrain", "context_budget must be an integer")
    if isinstance(context_estimate, bool) or not isinstance(context_estimate, int):
        raise StoreValidationError("pregrain", "context_estimate must be an integer")

    change_surface_values = _texts(
        change_surface,
        "change_surface",
        allow_empty=True,
    )
    exception_value = None
    if change_surface_exception is not None:
        exception_value = _text(change_surface_exception, "change_surface_exception")
    if not change_surface_values and exception_value is None:
        raise StoreValidationError(
            "pregrain",
            "change_surface or change_surface_exception is required",
        )

    evidence_values = _texts(evidence, "evidence", allow_empty=False)
    try:
        minimality = MinimalityChoice(minimality_choice)
    except ValueError as exc:
        raise StoreValidationError("pregrain", "minimality_choice is not canonical") from exc
    minimality_reason = _text(minimality_rationale, "minimality_rationale")
    try:
        safety = SafetyStatus(safety_status)
    except ValueError as exc:
        raise StoreValidationError("pregrain", "safety_status is not canonical") from exc
    safety_values = _texts(
        safety_requirements,
        "safety_requirements",
        allow_empty=True,
    )
    if safety is SafetyStatus.NONE_IDENTIFIED and safety_values:
        raise StoreValidationError(
            "pregrain",
            "safety_requirements must be empty when safety_status is none-identified",
        )
    if safety is SafetyStatus.REQUIREMENTS_DEFINED and not safety_values:
        raise StoreValidationError(
            "pregrain",
            "safety_requirements are required when safety_status is requirements-defined",
        )

    readiness: dict[str, object] = {
        "version": GRAIN_READINESS_VERSION,
        "unresolved_decisions": [],
        "minimality": {
            "choice": minimality.value,
            "rationale": minimality_reason,
        },
        "safety": {
            "status": safety.value,
            "requirements": list(safety_values),
        },
    }
    if exception_value is not None:
        readiness["change_surface_exception"] = exception_value

    data = node.to_dict()
    data["scope_in"] = list(scope_in_values)
    data["scope_out"] = list(scope_out_values)
    data["acceptance"] = list(acceptance_values)
    data["dependencies"] = list(dependency_values)
    data["risk"] = {"level": risk_level, "recovery": recovery_value}
    data["context"] = {
        "budget_tokens": context_budget,
        "estimated_tokens": context_estimate,
    }
    data["change_surface"] = list(change_surface_values)
    data["evidence"] = {"required": list(evidence_values)}
    metadata = dict(node.metadata)
    metadata["readiness"] = readiness
    data["metadata"] = metadata
    data["state"] = SpecState.SHAPED.value

    location = f".specgrain/specs/{node.id}.json"
    shaped = _node_from_data(data, location)
    proposed = _validate_proposed(project, shaped)

    probe_data = shaped.to_dict()
    probe_data["state"] = SpecState.REFINING.value
    probe = _node_from_data(probe_data, location)
    probe_forest = tuple(probe if item.id == probe.id else item for item in proposed)
    report = evaluate_grain_readiness(probe, probe_forest)
    if not report.is_ready:
        codes = ", ".join(issue.code.value for issue in report.issues)
        raise StoreValidationError(
            location,
            f"shaped candidate would remain Grain-readiness blocked: {codes}",
        )

    stored = _persist(project, node, shaped)
    return PreGrainMutationResult(stored, SpecState.DRAFT)


def _state_only_transition(
    root: str | os.PathLike[str],
    *,
    spec_id: str,
    source: SpecState,
    target: SpecState,
) -> PreGrainMutationResult:
    project, node = _target(root, spec_id, source)
    require_transition_allowed(node.state, target)
    data = node.to_dict()
    data["state"] = target.value
    after = _node_from_data(data, f".specgrain/specs/{node.id}.json")
    if after.revision_digest != node.revision_digest:
        raise StoreValidationError(
            f".specgrain/specs/{node.id}.json",
            "state-only transition changed semantic revision digest",
        )
    stored = _persist(project, node, after)
    return PreGrainMutationResult(stored, source)


def refine_shaped_spec(
    root: str | os.PathLike[str] = ".",
    *,
    spec_id: str,
) -> PreGrainMutationResult:
    """Authorize exactly SHAPED -> REFINING without semantic mutation."""

    return _state_only_transition(
        root,
        spec_id=spec_id,
        source=SpecState.SHAPED,
        target=SpecState.REFINING,
    )


def promote_refining_spec_to_grain(
    root: str | os.PathLike[str] = ".",
    *,
    spec_id: str,
) -> PreGrainMutationResult:
    """Authorize REFINING -> GRAIN only for the exact ready candidate revision."""

    project, node = _target(root, spec_id, SpecState.REFINING)
    report = evaluate_grain_readiness(node, project.specs)
    if not report.is_ready:
        raise GrainPromotionBlockedError(report)
    require_transition_allowed(node.state, SpecState.GRAIN)
    data = node.to_dict()
    data["state"] = SpecState.GRAIN.value
    grain = _node_from_data(data, f".specgrain/specs/{node.id}.json")
    if grain.revision_digest != node.revision_digest:
        raise StoreValidationError(
            f".specgrain/specs/{node.id}.json",
            "Grain promotion changed semantic revision digest",
        )
    stored = _persist(project, node, grain)
    return PreGrainMutationResult(stored, SpecState.REFINING)
