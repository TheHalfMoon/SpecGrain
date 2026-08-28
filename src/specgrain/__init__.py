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
from .readiness import (
    GRAIN_READINESS_VERSION,
    GrainReadinessError,
    GrainReadinessReport,
    MinimalityChoice,
    ReadinessIssue,
    ReadinessIssueCode,
    SafetyStatus,
    evaluate_grain_readiness,
    require_grain_readiness,
)
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
    "GRAIN_READINESS_VERSION",
    "SPECNODE_SCHEMA_VERSION",
    "TERMINAL_STATES",
    "GrainReadinessError",
    "GrainReadinessReport",
    "LifecycleStateError",
    "LifecycleTransitionError",
    "MinimalityChoice",
    "ReadinessIssue",
    "ReadinessIssueCode",
    "RefinementIssue",
    "RefinementIssueCode",
    "RefinementValidationError",
    "SafetyStatus",
    "SpecNode",
    "SpecState",
    "SpecValidationError",
    "allowed_transitions",
    "evaluate_grain_readiness",
    "is_spec_id",
    "is_transition_allowed",
    "parse_spec_state",
    "refinement_roots",
    "require_grain_readiness",
    "require_transition_allowed",
    "require_valid_refinement",
    "validate_refinement",
]
