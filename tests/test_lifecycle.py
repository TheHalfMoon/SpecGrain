from __future__ import annotations

import pytest

from specgrain import (
    EXCEPTIONAL_STATES,
    TERMINAL_STATES,
    LifecycleStateError,
    LifecycleTransitionError,
    SpecNode,
    SpecState,
    SpecValidationError,
    allowed_transitions,
    is_transition_allowed,
    parse_spec_state,
    require_transition_allowed,
)

EXPECTED_TRANSITIONS = {
    SpecState.DRAFT: {
        SpecState.SHAPED,
        SpecState.BLOCKED,
        SpecState.CANCELLED,
        SpecState.SUPERSEDED,
    },
    SpecState.SHAPED: {
        SpecState.REFINING,
        SpecState.BLOCKED,
        SpecState.STALE,
        SpecState.CANCELLED,
        SpecState.SUPERSEDED,
    },
    SpecState.REFINING: {
        SpecState.GRAIN,
        SpecState.BLOCKED,
        SpecState.STALE,
        SpecState.CANCELLED,
        SpecState.SUPERSEDED,
    },
    SpecState.GRAIN: {
        SpecState.READY,
        SpecState.SHAPED,
        SpecState.BLOCKED,
        SpecState.STALE,
        SpecState.CANCELLED,
        SpecState.SUPERSEDED,
    },
    SpecState.READY: {
        SpecState.RUNNING,
        SpecState.SHAPED,
        SpecState.BLOCKED,
        SpecState.STALE,
        SpecState.CANCELLED,
        SpecState.SUPERSEDED,
    },
    SpecState.RUNNING: {
        SpecState.VERIFYING,
        SpecState.BLOCKED,
        SpecState.FAILED,
        SpecState.STALE,
        SpecState.CANCELLED,
        SpecState.SUPERSEDED,
    },
    SpecState.VERIFYING: {
        SpecState.VERIFIED,
        SpecState.BLOCKED,
        SpecState.FAILED,
        SpecState.STALE,
        SpecState.CANCELLED,
        SpecState.SUPERSEDED,
    },
    SpecState.VERIFIED: {SpecState.CONTROLLED, SpecState.STALE, SpecState.SUPERSEDED},
    SpecState.CONTROLLED: {SpecState.STALE, SpecState.SUPERSEDED},
    SpecState.BLOCKED: {SpecState.SHAPED, SpecState.CANCELLED, SpecState.SUPERSEDED},
    SpecState.FAILED: {SpecState.SHAPED, SpecState.CANCELLED, SpecState.SUPERSEDED},
    SpecState.STALE: {SpecState.SHAPED, SpecState.CANCELLED, SpecState.SUPERSEDED},
    SpecState.CANCELLED: set(),
    SpecState.SUPERSEDED: set(),
}


def test_enum_is_complete_and_unique() -> None:
    assert len(SpecState) == 14
    assert {state.value for state in SpecState} == {state.name for state in SpecState}


@pytest.mark.parametrize("state", list(SpecState))
def test_parse_accepts_canonical_states(state: SpecState) -> None:
    assert parse_spec_state(state) is state
    assert parse_spec_state(state.value) is state


@pytest.mark.parametrize("value", ["draft", " DRAFT", "DRAFT ", "", "UNKNOWN", 1, None])
def test_parse_rejects_noncanonical_states(value: object) -> None:
    with pytest.raises(LifecycleStateError):
        parse_spec_state(value)


def test_classifications_are_exact_and_immutable() -> None:
    assert TERMINAL_STATES == frozenset({SpecState.CANCELLED, SpecState.SUPERSEDED})
    assert EXCEPTIONAL_STATES == frozenset(
        {SpecState.BLOCKED, SpecState.FAILED, SpecState.STALE}
    )


@pytest.mark.parametrize("source", list(SpecState))
def test_full_transition_matrix(source: SpecState) -> None:
    assert allowed_transitions(source) == frozenset(EXPECTED_TRANSITIONS[source])
    for target in SpecState:
        assert is_transition_allowed(source, target) is (target in EXPECTED_TRANSITIONS[source])


def test_terminal_states_have_no_outgoing_edges() -> None:
    assert not allowed_transitions(SpecState.CANCELLED)
    assert not allowed_transitions(SpecState.SUPERSEDED)


@pytest.mark.parametrize("source", [SpecState.BLOCKED, SpecState.FAILED, SpecState.STALE])
@pytest.mark.parametrize(
    "target",
    [
        SpecState.REFINING,
        SpecState.GRAIN,
        SpecState.READY,
        SpecState.RUNNING,
        SpecState.VERIFYING,
        SpecState.VERIFIED,
    ],
)
def test_exceptional_states_cannot_resume_downstream(
    source: SpecState, target: SpecState
) -> None:
    assert not is_transition_allowed(source, target)


def test_require_transition_allowed_is_explainable() -> None:
    require_transition_allowed("DRAFT", "SHAPED")

    with pytest.raises(
        LifecycleTransitionError,
        match=r"transition DRAFT -> VERIFIED is not structurally allowed; allowed targets:",
    ):
        require_transition_allowed("DRAFT", "VERIFIED")


def test_terminal_rejection_reports_no_targets() -> None:
    with pytest.raises(LifecycleTransitionError, match=r"allowed targets: none"):
        require_transition_allowed("CANCELLED", "SHAPED")


def test_invalid_transition_inputs_raise_state_error() -> None:
    with pytest.raises(LifecycleStateError):
        is_transition_allowed("UNKNOWN", "DRAFT")
    with pytest.raises(LifecycleStateError):
        allowed_transitions(42)


@pytest.mark.parametrize("state", list(SpecState))
def test_specnode_accepts_all_canonical_states(state: SpecState) -> None:
    node = SpecNode(id="SG-000001", title="x", outcome="y", state=state)
    assert node.state == state.value


def test_specnode_rejects_unknown_state_as_model_error() -> None:
    with pytest.raises(SpecValidationError, match="unknown lifecycle state"):
        SpecNode(id="SG-000001", title="x", outcome="y", state="UNKNOWN")


def test_state_validation_does_not_change_content_digest() -> None:
    draft = SpecNode(id="SG-000001", title="x", outcome="y", state="DRAFT")
    ready = SpecNode(id="SG-000001", title="x", outcome="y", state="READY")
    assert draft.revision_digest == ready.revision_digest
