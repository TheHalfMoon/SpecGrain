"""SpecGrain deterministic core primitives."""

from .lifecycle import (
    EXCEPTIONAL_STATES,
    TERMINAL_STATES,
    LifecycleStateError,
    LifecycleTransitionError,
    SpecState,
    allowed_transitions,
    is_transition_allowed,
    parse_spec_state,
    require_transition_allowed,
)
from .model import SPECNODE_SCHEMA_VERSION, SpecNode, SpecValidationError, is_spec_id

__all__ = [
    "EXCEPTIONAL_STATES",
    "SPECNODE_SCHEMA_VERSION",
    "TERMINAL_STATES",
    "LifecycleStateError",
    "LifecycleTransitionError",
    "SpecNode",
    "SpecState",
    "SpecValidationError",
    "allowed_transitions",
    "is_spec_id",
    "is_transition_allowed",
    "parse_spec_state",
    "require_transition_allowed",
]
