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
from .refinement import (
    RefinementIssue,
    RefinementIssueCode,
    RefinementValidationError,
    refinement_roots,
    require_valid_refinement,
    validate_refinement,
)

__all__ = [
    "EXCEPTIONAL_STATES",
    "SPECNODE_SCHEMA_VERSION",
    "TERMINAL_STATES",
    "LifecycleStateError",
    "LifecycleTransitionError",
    "RefinementIssue",
    "RefinementIssueCode",
    "RefinementValidationError",
    "SpecNode",
    "SpecState",
    "SpecValidationError",
    "allowed_transitions",
    "is_spec_id",
    "is_transition_allowed",
    "parse_spec_state",
    "refinement_roots",
    "require_transition_allowed",
    "require_valid_refinement",
    "validate_refinement",
]
