"""Portable immutable WorkPacket and execution-result contracts."""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Any

from .context import ContextBudgetReport, ContextSource, validate_context_sources
from .model import SpecNode, is_spec_id

WORK_PACKET_VERSION = 1
EXECUTION_RESULT_VERSION = 1


class PacketValidationError(ValueError):
    """Raised when a WorkPacket or execution result violates its contract."""


class ExecutionStatus(StrEnum):
    """Portable executor-reported completion state."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED = "blocked"


def _require_text(value: object, field_name: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise PacketValidationError(f"{field_name} must be a string")
    if not allow_empty and not value.strip():
        raise PacketValidationError(f"{field_name} must be a non-empty string")
    return value


def _normalize_strings(value: object, field_name: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise PacketValidationError(f"{field_name} must be a sequence of strings")
    result: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        text = _require_text(item, f"{field_name}[{index}]")
        if text in seen:
            raise PacketValidationError(f"{field_name} must not contain duplicate value {text!r}")
        seen.add(text)
        result.append(text)
    return tuple(sorted(result))


def _freeze_json(value: object, field_name: str) -> object:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise PacketValidationError(f"{field_name} contains a non-finite float")
        return value
    if isinstance(value, Mapping):
        frozen: dict[str, object] = {}
        for key, nested in value.items():
            if not isinstance(key, str):
                raise PacketValidationError(f"{field_name} contains a non-string object key")
            frozen[key] = _freeze_json(nested, f"{field_name}.{key}")
        return MappingProxyType(frozen)
    if isinstance(value, (list, tuple)):
        return tuple(
            _freeze_json(item, f"{field_name}[{index}]")
            for index, item in enumerate(value)
        )
    raise PacketValidationError(
        f"{field_name} contains unsupported JSON value type {type(value).__name__}"
    )


def _freeze_object(value: object, field_name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise PacketValidationError(f"{field_name} must be a JSON object")
    frozen = _freeze_json(value, field_name)
    assert isinstance(frozen, Mapping)
    return frozen


def _thaw_json(value: object) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_json(nested) for key, nested in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


def _digest(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _validate_digest(value: object, field_name: str) -> str:
    text = _require_text(value, field_name)
    if not text.startswith("sha256:") or len(text) != 71:
        raise PacketValidationError(f"{field_name} must be a sha256: digest")
    suffix = text[7:]
    if any(character not in "0123456789abcdef" for character in suffix):
        raise PacketValidationError(f"{field_name} must use lowercase hexadecimal")
    return text


@dataclass(frozen=True, slots=True)
class PacketContextSource:
    """Portable snapshot of one selected context source."""

    source_id: str
    provenance: str
    selection_reason: str
    revision: str
    size_bytes: int
    token_cost: int

    def __post_init__(self) -> None:
        for field_name in ("source_id", "provenance", "selection_reason", "revision"):
            object.__setattr__(
                self, field_name, _require_text(getattr(self, field_name), field_name)
            )
        for field_name in ("size_bytes", "token_cost"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise PacketValidationError(f"{field_name} must be a non-negative integer")

    def to_dict(self) -> dict[str, object]:
        """Return the portable JSON-compatible source snapshot."""

        return {
            "provenance": self.provenance,
            "revision": self.revision,
            "selection_reason": self.selection_reason,
            "size_bytes": self.size_bytes,
            "source_id": self.source_id,
            "token_cost": self.token_cost,
        }

    @classmethod
    def from_context_source(cls, source: ContextSource) -> PacketContextSource:
        """Snapshot a validated ContextSource without retaining policy-only fields."""

        if not isinstance(source, ContextSource):
            raise PacketValidationError("source must be a ContextSource")
        return cls(
            source_id=source.source_id,
            provenance=source.provenance,
            selection_reason=source.selection_reason,
            revision=source.revision,
            size_bytes=source.size_bytes,
            token_cost=source.token_cost,
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> PacketContextSource:
        """Parse a strict portable context-source snapshot."""

        if not isinstance(data, Mapping):
            raise PacketValidationError("packet context source must be an object")
        allowed = {
            "source_id",
            "provenance",
            "selection_reason",
            "revision",
            "size_bytes",
            "token_cost",
        }
        unknown = sorted(set(data) - allowed)
        missing = sorted(allowed - set(data))
        if unknown:
            raise PacketValidationError(
                f"packet context source has unknown fields: {', '.join(unknown)}"
            )
        if missing:
            raise PacketValidationError(
                f"packet context source is missing fields: {', '.join(missing)}"
            )
        return cls(**dict(data))  # type: ignore[arg-type]


@dataclass(frozen=True, slots=True)
class WorkPacket:
    """Immutable portable execution boundary bound to exact spec/context revisions."""

    spec_id: str
    spec_revision: str
    outcome: str
    acceptance: tuple[str, ...]
    scope_in: tuple[str, ...]
    scope_out: tuple[str, ...]
    dependencies: tuple[str, ...]
    authorized_change_surface: tuple[str, ...]
    method: str
    risk: Mapping[str, object]
    required_evidence: tuple[str, ...]
    context_plan_digest: str
    context_sources: tuple[PacketContextSource, ...]
    decisions: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    minimality_evidence: tuple[str, ...] = ()
    packet_version: int = WORK_PACKET_VERSION

    def __post_init__(self) -> None:
        if self.packet_version != WORK_PACKET_VERSION or isinstance(self.packet_version, bool):
            raise PacketValidationError(
                f"packet_version must equal integer {WORK_PACKET_VERSION}"
            )
        if not is_spec_id(self.spec_id):
            raise PacketValidationError("spec_id must be a canonical SpecGrain ID")
        object.__setattr__(
            self, "spec_revision", _validate_digest(self.spec_revision, "spec_revision")
        )
        object.__setattr__(self, "outcome", _require_text(self.outcome, "outcome"))
        object.__setattr__(self, "method", _require_text(self.method, "method"))
        object.__setattr__(
            self,
            "context_plan_digest",
            _validate_digest(self.context_plan_digest, "context_plan_digest"),
        )
        for field_name in (
            "acceptance",
            "scope_in",
            "scope_out",
            "dependencies",
            "authorized_change_surface",
            "required_evidence",
            "decisions",
            "assumptions",
            "minimality_evidence",
        ):
            object.__setattr__(
                self, field_name, _normalize_strings(getattr(self, field_name), field_name)
            )
        if any(not is_spec_id(dependency) for dependency in self.dependencies):
            raise PacketValidationError("dependencies must contain canonical SpecGrain IDs")
        object.__setattr__(self, "risk", _freeze_object(self.risk, "risk"))

        sources = tuple(self.context_sources)
        for index, source in enumerate(sources):
            if not isinstance(source, PacketContextSource):
                raise PacketValidationError(
                    f"context_sources[{index}] must be a PacketContextSource"
                )
        duplicates = sorted(
            source_id
            for source_id, count in Counter(source.source_id for source in sources).items()
            if count > 1
        )
        if duplicates:
            raise PacketValidationError(
                f"duplicate context source IDs: {', '.join(duplicates)}"
            )
        object.__setattr__(
            self, "context_sources", tuple(sorted(sources, key=lambda source: source.source_id))
        )

    def content_dict(self) -> dict[str, object]:
        """Return normalized packet content excluding the derived packet digest."""

        return {
            "acceptance": list(self.acceptance),
            "assumptions": list(self.assumptions),
            "authorized_change_surface": list(self.authorized_change_surface),
            "context_plan_digest": self.context_plan_digest,
            "context_sources": [source.to_dict() for source in self.context_sources],
            "decisions": list(self.decisions),
            "dependencies": list(self.dependencies),
            "method": self.method,
            "minimality_evidence": list(self.minimality_evidence),
            "outcome": self.outcome,
            "packet_version": self.packet_version,
            "required_evidence": list(self.required_evidence),
            "risk": _thaw_json(self.risk),
            "scope_in": list(self.scope_in),
            "scope_out": list(self.scope_out),
            "spec_id": self.spec_id,
            "spec_revision": self.spec_revision,
        }

    @property
    def packet_digest(self) -> str:
        """Return the stable digest over normalized packet content."""

        return _digest(self.content_dict())

    def to_dict(self) -> dict[str, object]:
        """Return a detached portable packet representation including its digest."""

        result = self.content_dict()
        result["packet_digest"] = self.packet_digest
        return result

    def to_json(self) -> str:
        """Return canonical compact JSON suitable for an adapter boundary."""

        return json.dumps(
            self.to_dict(),
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> WorkPacket:
        """Parse a strict packet representation and verify its declared digest."""

        if not isinstance(data, Mapping):
            raise PacketValidationError("WorkPacket input must be an object")
        payload = dict(data)
        declared_digest = payload.pop("packet_digest", None)
        allowed = {
            "acceptance", "assumptions", "authorized_change_surface", "context_plan_digest",
            "context_sources", "decisions", "dependencies", "method", "minimality_evidence",
            "outcome", "packet_version", "required_evidence", "risk", "scope_in", "scope_out",
            "spec_id", "spec_revision",
        }
        unknown = sorted(set(payload) - allowed)
        missing = sorted(allowed - set(payload))
        if unknown:
            raise PacketValidationError(
                f"WorkPacket input has unknown fields: {', '.join(unknown)}"
            )
        if missing:
            raise PacketValidationError(f"WorkPacket input is missing fields: {', '.join(missing)}")
        raw_sources = payload.get("context_sources")
        if isinstance(raw_sources, (str, bytes, bytearray)) or not isinstance(
            raw_sources, Sequence
        ):
            raise PacketValidationError("context_sources must be a sequence of objects")
        payload["context_sources"] = tuple(
            PacketContextSource.from_dict(item) for item in raw_sources
        )
        packet = cls(**payload)  # type: ignore[arg-type]
        if declared_digest is None:
            raise PacketValidationError("WorkPacket input is missing packet_digest")
        digest = _validate_digest(declared_digest, "packet_digest")
        if digest != packet.packet_digest:
            raise PacketValidationError("packet_digest does not match normalized packet content")
        return packet


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """Executor self-report bound to a WorkPacket but not verification authority."""

    packet_digest: str
    status: ExecutionStatus | str
    summary: str
    changed_paths: tuple[str, ...] = ()
    reported_evidence: tuple[str, ...] = ()
    error_code: str | None = None
    result_version: int = EXECUTION_RESULT_VERSION

    def __post_init__(self) -> None:
        if self.result_version != EXECUTION_RESULT_VERSION or isinstance(self.result_version, bool):
            raise PacketValidationError(
                f"result_version must equal integer {EXECUTION_RESULT_VERSION}"
            )
        object.__setattr__(
            self, "packet_digest", _validate_digest(self.packet_digest, "packet_digest")
        )
        try:
            status = ExecutionStatus(self.status)
        except (TypeError, ValueError) as exc:
            raise PacketValidationError(
                "status must be 'succeeded', 'failed', or 'blocked'"
            ) from exc
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "summary", _require_text(self.summary, "summary"))
        object.__setattr__(
            self, "changed_paths", _normalize_strings(self.changed_paths, "changed_paths")
        )
        object.__setattr__(
            self,
            "reported_evidence",
            _normalize_strings(self.reported_evidence, "reported_evidence"),
        )
        if self.error_code is not None:
            object.__setattr__(
                self, "error_code", _require_text(self.error_code, "error_code")
            )
        if status is ExecutionStatus.SUCCEEDED and self.error_code is not None:
            raise PacketValidationError("succeeded results must not carry error_code")
        if status is not ExecutionStatus.SUCCEEDED and self.error_code is None:
            raise PacketValidationError("failed or blocked results require error_code")

    def content_dict(self) -> dict[str, object]:
        """Return normalized result content excluding the derived result digest."""

        result: dict[str, object] = {
            "changed_paths": list(self.changed_paths),
            "packet_digest": self.packet_digest,
            "reported_evidence": list(self.reported_evidence),
            "result_version": self.result_version,
            "status": self.status.value,
            "summary": self.summary,
        }
        if self.error_code is not None:
            result["error_code"] = self.error_code
        return result

    @property
    def result_digest(self) -> str:
        """Return the stable digest over normalized executor-reported result content."""

        return _digest(self.content_dict())

    def to_dict(self) -> dict[str, object]:
        """Return a detached portable result representation including its digest."""

        result = self.content_dict()
        result["result_digest"] = self.result_digest
        return result

    def to_json(self) -> str:
        """Return canonical compact JSON suitable for an adapter boundary."""

        return json.dumps(
            self.to_dict(),
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ExecutionResult:
        """Parse a strict executor result and verify its declared digest."""

        if not isinstance(data, Mapping):
            raise PacketValidationError("ExecutionResult input must be an object")
        payload = dict(data)
        declared_digest = payload.pop("result_digest", None)
        allowed = {
            "packet_digest", "status", "summary", "changed_paths", "reported_evidence",
            "error_code", "result_version",
        }
        unknown = sorted(set(payload) - allowed)
        required = {
            "packet_digest",
            "status",
            "summary",
            "changed_paths",
            "reported_evidence",
            "result_version",
        }
        missing = sorted(required - set(payload))
        if unknown:
            raise PacketValidationError(
                f"ExecutionResult input has unknown fields: {', '.join(unknown)}"
            )
        if missing:
            raise PacketValidationError(
                f"ExecutionResult input is missing fields: {', '.join(missing)}"
            )
        result = cls(**payload)  # type: ignore[arg-type]
        if declared_digest is None:
            raise PacketValidationError("ExecutionResult input is missing result_digest")
        digest = _validate_digest(declared_digest, "result_digest")
        if digest != result.result_digest:
            raise PacketValidationError("result_digest does not match normalized result content")
        return result


def _required_evidence(node: SpecNode) -> tuple[str, ...]:
    value = node.evidence.get("required", ())
    try:
        return _normalize_strings(value, "node.evidence.required")
    except PacketValidationError as exc:
        raise PacketValidationError(str(exc)) from exc


def build_work_packet(
    node: SpecNode,
    context_sources: Iterable[ContextSource],
    context_report: ContextBudgetReport,
    *,
    decisions: Sequence[str] = (),
    assumptions: Sequence[str] = (),
    minimality_evidence: Sequence[str] = (),
) -> WorkPacket:
    """Build a portable packet from exact spec and selected context facts.

    This function does not authorize lifecycle transitions or execution. Callers must
    separately establish Grain readiness, dependency eligibility, and current baseline.
    """

    if not isinstance(node, SpecNode):
        raise PacketValidationError("node must be a SpecNode")
    if not isinstance(context_report, ContextBudgetReport):
        raise PacketValidationError("context_report must be a ContextBudgetReport")
    if not context_report.fits:
        raise PacketValidationError("context_report must fit policy before packet construction")

    canonical_sources = validate_context_sources(context_sources)
    by_id = {source.source_id: source for source in canonical_sources}
    missing = sorted(set(context_report.selected_ids) - set(by_id))
    extra = sorted(set(by_id) - set(context_report.selected_ids))
    if missing or extra:
        details: list[str] = []
        if missing:
            details.append(f"missing selected sources: {', '.join(missing)}")
        if extra:
            details.append(f"unselected sources supplied: {', '.join(extra)}")
        raise PacketValidationError("; ".join(details))

    packet_sources = tuple(
        PacketContextSource.from_context_source(by_id[source_id])
        for source_id in context_report.selected_ids
    )
    return WorkPacket(
        spec_id=node.id,
        spec_revision=node.revision_digest,
        outcome=node.outcome,
        acceptance=node.acceptance,
        scope_in=node.scope_in,
        scope_out=node.scope_out,
        dependencies=node.dependencies,
        authorized_change_surface=node.change_surface,
        method=node.method,
        risk=node.risk,
        required_evidence=_required_evidence(node),
        context_plan_digest=context_report.plan_digest,
        context_sources=packet_sources,
        decisions=tuple(decisions),
        assumptions=tuple(assumptions),
        minimality_evidence=tuple(minimality_evidence),
    )
