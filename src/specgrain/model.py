"""Deterministic SpecNode data model and content revision hashing."""

from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from hashlib import sha256
from types import MappingProxyType
from typing import Any

from .lifecycle import LifecycleStateError, parse_spec_state

SPECNODE_SCHEMA_VERSION = 1
_SPEC_ID_RE = re.compile(r"^SG-\d{6}$")
_EMPTY_OBJECT = MappingProxyType({})
_SET_LIKE_FIELDS = (
    "scope_in",
    "scope_out",
    "acceptance",
    "dependencies",
    "change_surface",
    "children",
    "labels",
)


class SpecValidationError(ValueError):
    """Raised when data violates the public SpecNode schema contract."""


def is_spec_id(value: object) -> bool:
    """Return whether *value* is a canonical repository-local SpecGrain ID."""

    return isinstance(value, str) and _SPEC_ID_RE.fullmatch(value) is not None


def _require_spec_id(value: object, field_name: str) -> str:
    if not is_spec_id(value):
        raise SpecValidationError(
            f"{field_name} must match 'SG-' followed by exactly six decimal digits"
        )
    return value


def _require_text(value: object, field_name: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise SpecValidationError(f"{field_name} must be a string")
    if not allow_empty and not value.strip():
        raise SpecValidationError(f"{field_name} must not be empty")
    return value


def _normalize_string_sequence(
    value: object,
    field_name: str,
    *,
    ids: bool = False,
) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise SpecValidationError(f"{field_name} must be a sequence of strings")

    normalized: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        item_name = f"{field_name}[{index}]"
        text = _require_spec_id(item, item_name) if ids else _require_text(item, item_name)
        if text in seen:
            raise SpecValidationError(f"{field_name} must not contain duplicate value {text!r}")
        seen.add(text)
        normalized.append(text)
    return tuple(normalized)


def _freeze_json(value: object, path: str) -> object:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise SpecValidationError(f"{path} contains a non-finite float")
        return value
    if isinstance(value, Mapping):
        frozen: dict[str, object] = {}
        for key, nested in value.items():
            if not isinstance(key, str):
                raise SpecValidationError(f"{path} contains a non-string object key")
            frozen[key] = _freeze_json(nested, f"{path}.{key}")
        return MappingProxyType(frozen)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item, f"{path}[{index}]") for index, item in enumerate(value))
    raise SpecValidationError(f"{path} contains unsupported JSON value type {type(value).__name__}")


def _freeze_object(value: object, field_name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise SpecValidationError(f"{field_name} must be a JSON object")
    frozen = _freeze_json(value, field_name)
    assert isinstance(frozen, Mapping)
    return frozen


def _thaw_json(value: object) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_json(nested) for key, nested in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class SpecNode:
    """Immutable recursive specification primitive for SpecGrain.

    Lifecycle state names are validated by Specification 002. Transition authorization
    remains the responsibility of later gate-owning specifications.
    """

    id: str
    title: str
    outcome: str
    schema_version: int = SPECNODE_SCHEMA_VERSION
    rationale: str = ""
    parent_id: str | None = None
    scope_in: tuple[str, ...] = ()
    scope_out: tuple[str, ...] = ()
    acceptance: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    risk: Mapping[str, object] = field(default_factory=lambda: _EMPTY_OBJECT)
    context: Mapping[str, object] = field(default_factory=lambda: _EMPTY_OBJECT)
    change_surface: tuple[str, ...] = ()
    evidence: Mapping[str, object] = field(default_factory=lambda: _EMPTY_OBJECT)
    method: str = "quick"
    state: str = "DRAFT"
    children: tuple[str, ...] = ()
    labels: tuple[str, ...] = ()
    metadata: Mapping[str, object] = field(default_factory=lambda: _EMPTY_OBJECT)

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", _require_spec_id(self.id, "id"))
        object.__setattr__(self, "title", _require_text(self.title, "title"))
        object.__setattr__(self, "outcome", _require_text(self.outcome, "outcome"))

        if isinstance(self.schema_version, bool) or not isinstance(self.schema_version, int):
            raise SpecValidationError("schema_version must be an integer")
        if self.schema_version != SPECNODE_SCHEMA_VERSION:
            raise SpecValidationError(
                f"unsupported schema_version {self.schema_version}; "
                f"expected {SPECNODE_SCHEMA_VERSION}"
            )

        object.__setattr__(
            self, "rationale", _require_text(self.rationale, "rationale", allow_empty=True)
        )

        if self.parent_id is not None:
            object.__setattr__(self, "parent_id", _require_spec_id(self.parent_id, "parent_id"))

        object.__setattr__(self, "scope_in", _normalize_string_sequence(self.scope_in, "scope_in"))
        object.__setattr__(
            self, "scope_out", _normalize_string_sequence(self.scope_out, "scope_out")
        )
        object.__setattr__(
            self, "acceptance", _normalize_string_sequence(self.acceptance, "acceptance")
        )
        object.__setattr__(
            self,
            "dependencies",
            _normalize_string_sequence(self.dependencies, "dependencies", ids=True),
        )
        object.__setattr__(
            self,
            "change_surface",
            _normalize_string_sequence(self.change_surface, "change_surface"),
        )
        object.__setattr__(
            self, "children", _normalize_string_sequence(self.children, "children", ids=True)
        )
        object.__setattr__(self, "labels", _normalize_string_sequence(self.labels, "labels"))

        object.__setattr__(self, "risk", _freeze_object(self.risk, "risk"))
        object.__setattr__(self, "context", _freeze_object(self.context, "context"))
        object.__setattr__(self, "evidence", _freeze_object(self.evidence, "evidence"))
        object.__setattr__(self, "metadata", _freeze_object(self.metadata, "metadata"))

        object.__setattr__(self, "method", _require_text(self.method, "method"))
        state_text = _require_text(self.state, "state")
        try:
            state = parse_spec_state(state_text)
        except LifecycleStateError as exc:
            raise SpecValidationError(str(exc)) from exc
        object.__setattr__(self, "state", state.value)

    def to_dict(self) -> dict[str, Any]:
        """Return a detached JSON-compatible representation of this node."""

        return {
            "id": self.id,
            "title": self.title,
            "outcome": self.outcome,
            "schema_version": self.schema_version,
            "rationale": self.rationale,
            "parent_id": self.parent_id,
            "scope_in": list(self.scope_in),
            "scope_out": list(self.scope_out),
            "acceptance": list(self.acceptance),
            "dependencies": list(self.dependencies),
            "risk": _thaw_json(self.risk),
            "context": _thaw_json(self.context),
            "change_surface": list(self.change_surface),
            "evidence": _thaw_json(self.evidence),
            "method": self.method,
            "state": self.state,
            "children": list(self.children),
            "labels": list(self.labels),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> SpecNode:
        """Construct a node from the public dictionary representation."""

        if not isinstance(data, Mapping):
            raise SpecValidationError("SpecNode input must be an object")

        non_string_keys = [key for key in data if not isinstance(key, str)]
        if non_string_keys:
            raise SpecValidationError("SpecNode input contains a non-string object key")

        allowed = set(cls.__dataclass_fields__)
        unknown = sorted(set(data) - allowed)
        if unknown:
            raise SpecValidationError(
                f"SpecNode input contains unknown fields: {', '.join(unknown)}"
            )

        missing = [name for name in ("id", "title", "outcome") if name not in data]
        if missing:
            raise SpecValidationError(
                f"SpecNode input is missing required fields: {', '.join(missing)}"
            )

        try:
            return cls(**dict(data))
        except SpecValidationError:
            raise
        except (TypeError, ValueError) as exc:
            raise SpecValidationError(str(exc)) from exc

    def canonical_content_dict(self) -> dict[str, Any]:
        """Return normalized semantic content used for revision hashing.

        ``state`` is intentionally excluded because lifecycle movement is operational
        state, not a change to specification meaning. ``schema_version`` remains in
        the content to bind the digest to its canonicalization contract.
        """

        content = self.to_dict()
        content.pop("state")
        for field_name in _SET_LIKE_FIELDS:
            content[field_name] = sorted(content[field_name])
        return content

    def canonical_content_json(self) -> bytes:
        """Return deterministic UTF-8 JSON bytes for semantic content."""

        try:
            text = json.dumps(
                self.canonical_content_dict(),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            )
        except (TypeError, ValueError) as exc:
            raise SpecValidationError(f"SpecNode canonical serialization failed: {exc}") from exc
        return text.encode("utf-8")

    @property
    def revision_digest(self) -> str:
        """Return the SHA-256 digest of canonical semantic content."""

        return f"sha256:{sha256(self.canonical_content_json()).hexdigest()}"
