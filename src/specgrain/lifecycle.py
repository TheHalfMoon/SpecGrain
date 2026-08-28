"""Deterministic lifecycle vocabulary and structural transition validation."""

from __future__ import annotations

from enum import StrEnum


class LifecycleStateError(ValueError):
    """Raised when a lifecycle state value is not canonical."""


class LifecycleTransitionError(ValueError):
    """Raised when a lifecycle edge is not structurally allowed."""


class SpecState(StrEnum):
    """Canonical SpecGrain lifecycle states."""

    DRAFT = "DRAFT"
    SHAPED = "SHAPED"
    REFINING = "REFINING"
    GRAIN = "GRAIN"
    READY = "READY"
    RUNNING = "RUNNING"
    VERIFYING = "VERIFYING"
    VERIFIED = "VERIFIED"
    CONTROLLED = "CONTROLLED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    STALE = "STALE"
    CANCELLED = "CANCELLED"
    SUPERSEDED = "SUPERSEDED"


TERMINAL_STATES = frozenset({SpecState.CANCELLED, SpecState.SUPERSEDED})
EXCEPTIONAL_STATES = frozenset({SpecState.BLOCKED, SpecState.FAILED, SpecState.STALE})

_TRANSITIONS: dict[SpecState, frozenset[SpecState]] = {
    SpecState.DRAFT: frozenset(
        {SpecState.SHAPED, SpecState.BLOCKED, SpecState.CANCELLED, SpecState.SUPERSEDED}
    ),
    SpecState.SHAPED: frozenset(
        {
            SpecState.REFINING,
            SpecState.BLOCKED,
            SpecState.STALE,
            SpecState.CANCELLED,
            SpecState.SUPERSEDED,
        }
    ),
    SpecState.REFINING: frozenset(
        {
            SpecState.GRAIN,
            SpecState.BLOCKED,
            SpecState.STALE,
            SpecState.CANCELLED,
            SpecState.SUPERSEDED,
        }
    ),
    SpecState.GRAIN: frozenset(
        {
            SpecState.READY,
            SpecState.SHAPED,
            SpecState.BLOCKED,
            SpecState.STALE,
            SpecState.CANCELLED,
            SpecState.SUPERSEDED,
        }
    ),
    SpecState.READY: frozenset(
        {
            SpecState.RUNNING,
            SpecState.SHAPED,
            SpecState.BLOCKED,
            SpecState.STALE,
            SpecState.CANCELLED,
            SpecState.SUPERSEDED,
        }
    ),
    SpecState.RUNNING: frozenset(
        {
            SpecState.VERIFYING,
            SpecState.BLOCKED,
            SpecState.FAILED,
            SpecState.STALE,
            SpecState.CANCELLED,
            SpecState.SUPERSEDED,
        }
    ),
    SpecState.VERIFYING: frozenset(
        {
            SpecState.VERIFIED,
            SpecState.BLOCKED,
            SpecState.FAILED,
            SpecState.STALE,
            SpecState.CANCELLED,
            SpecState.SUPERSEDED,
        }
    ),
    SpecState.VERIFIED: frozenset(
        {SpecState.CONTROLLED, SpecState.STALE, SpecState.SUPERSEDED}
    ),
    SpecState.CONTROLLED: frozenset({SpecState.STALE, SpecState.SUPERSEDED}),
    SpecState.BLOCKED: frozenset(
        {SpecState.SHAPED, SpecState.CANCELLED, SpecState.SUPERSEDED}
    ),
    SpecState.FAILED: frozenset(
        {SpecState.SHAPED, SpecState.CANCELLED, SpecState.SUPERSEDED}
    ),
    SpecState.STALE: frozenset(
        {SpecState.SHAPED, SpecState.CANCELLED, SpecState.SUPERSEDED}
    ),
    SpecState.CANCELLED: frozenset(),
    SpecState.SUPERSEDED: frozenset(),
}


def parse_spec_state(value: object) -> SpecState:
    """Return a canonical state or raise a stable validation error."""

    if isinstance(value, SpecState):
        return value
    if not isinstance(value, str):
        raise LifecycleStateError("state must be a canonical lifecycle string")
    try:
        return SpecState(value)
    except ValueError as exc:
        raise LifecycleStateError(f"unknown lifecycle state {value!r}") from exc


def allowed_transitions(state: object) -> frozenset[SpecState]:
    """Return immutable structurally allowed targets for *state*."""

    return _TRANSITIONS[parse_spec_state(state)]


def is_transition_allowed(current: object, target: object) -> bool:
    """Return whether an edge is structurally allowed, not authorized."""

    source = parse_spec_state(current)
    destination = parse_spec_state(target)
    return destination in _TRANSITIONS[source]


def require_transition_allowed(current: object, target: object) -> None:
    """Raise when an edge is not structurally allowed."""

    source = parse_spec_state(current)
    destination = parse_spec_state(target)
    allowed = _TRANSITIONS[source]
    if destination in allowed:
        return

    allowed_text = ", ".join(sorted(state.value for state in allowed)) or "none"
    raise LifecycleTransitionError(
        f"transition {source.value} -> {destination.value} is not structurally allowed; "
        f"allowed targets: {allowed_text}"
    )
