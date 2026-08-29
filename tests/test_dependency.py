from __future__ import annotations

import itertools

import pytest

from specgrain.dependency import (
    DEPENDENCY_BLOCKER_STATES,
    DEPENDENCY_SATISFIED_STATES,
    DependencyIssueCode,
    DependencyValidationError,
    dependency_waves,
    grain_dependency_report,
    ready_grains,
    require_valid_dependencies,
    validate_dependencies,
)
from specgrain.lifecycle import SpecState
from specgrain.model import SpecNode


def node(num: int, *, dependencies: tuple[int, ...] = (), state: str = "GRAIN") -> SpecNode:
    return SpecNode(
        id=f"SG-{num:06d}",
        title=f"Node {num}",
        outcome=f"Outcome {num}",
        dependencies=tuple(f"SG-{dependency:06d}" for dependency in dependencies),
        state=state,
    )


def test_empty_and_single_graph_are_valid() -> None:
    assert validate_dependencies([]) == ()
    assert validate_dependencies([node(1)]) == ()
    require_valid_dependencies([node(1)])


def test_non_specnode_member_is_rejected() -> None:
    with pytest.raises(TypeError, match=r"nodes\[1\] must be a SpecNode"):
        validate_dependencies([node(1), object()])  # type: ignore[list-item]


def test_duplicate_ids_are_identity_blocker_only() -> None:
    issues = validate_dependencies([node(1), node(1), node(2, dependencies=(99,))])
    assert len(issues) == 1
    assert issues[0].code is DependencyIssueCode.DUPLICATE_ID
    assert issues[0].node_id == "SG-000001"


def test_missing_dependency_is_deterministic() -> None:
    issues = validate_dependencies([node(2, dependencies=(9, 8)), node(1)])
    assert [issue.code for issue in issues] == [
        DependencyIssueCode.MISSING_DEPENDENCY,
        DependencyIssueCode.MISSING_DEPENDENCY,
    ]
    assert [issue.dependency_id for issue in issues] == ["SG-000008", "SG-000009"]


def test_self_dependency_is_rejected() -> None:
    issues = validate_dependencies([node(1, dependencies=(1,))])
    assert [issue.code for issue in issues] == [DependencyIssueCode.SELF_DEPENDENCY]


def test_two_node_cycle_is_canonical() -> None:
    nodes = [node(2, dependencies=(1,)), node(1, dependencies=(2,))]
    cycle = [
        issue
        for issue in validate_dependencies(nodes)
        if issue.code is DependencyIssueCode.CYCLE
    ]
    assert len(cycle) == 1
    assert cycle[0].message == "dependency cycle detected: SG-000001 -> SG-000002 -> SG-000001"


def test_three_node_cycle_is_input_order_invariant() -> None:
    nodes = [
        node(1, dependencies=(2,)),
        node(2, dependencies=(3,)),
        node(3, dependencies=(1,)),
    ]
    expected = validate_dependencies(nodes)
    assert [issue.code for issue in expected] == [DependencyIssueCode.CYCLE]
    for permutation in itertools.permutations(nodes):
        assert validate_dependencies(permutation) == expected


def test_aggregate_error_preserves_exact_issues() -> None:
    nodes = [node(1, dependencies=(9,))]
    issues = validate_dependencies(nodes)
    with pytest.raises(DependencyValidationError) as caught:
        require_valid_dependencies(nodes)
    assert caught.value.issues == issues


def test_state_classifications_are_disjoint_and_exact() -> None:
    assert frozenset({SpecState.VERIFIED, SpecState.CONTROLLED}) == DEPENDENCY_SATISFIED_STATES
    assert frozenset(
        {
            SpecState.BLOCKED,
            SpecState.FAILED,
            SpecState.STALE,
            SpecState.CANCELLED,
            SpecState.SUPERSEDED,
        }
    ) == DEPENDENCY_BLOCKER_STATES
    assert not (DEPENDENCY_SATISFIED_STATES & DEPENDENCY_BLOCKER_STATES)


@pytest.mark.parametrize("state", [SpecState.VERIFIED, SpecState.CONTROLLED])
def test_satisfied_dependency_makes_grain_eligible(state: SpecState) -> None:
    dependency = node(1, state=state.value)
    candidate = node(2, dependencies=(1,))
    report = grain_dependency_report(candidate.id, [candidate, dependency])
    assert report.eligible
    assert report.waiting_on == report.blocked_by == ()


@pytest.mark.parametrize(
    "state",
    [
        SpecState.DRAFT,
        SpecState.SHAPED,
        SpecState.REFINING,
        SpecState.GRAIN,
        SpecState.READY,
        SpecState.RUNNING,
        SpecState.VERIFYING,
    ],
)
def test_waiting_dependency_prevents_eligibility_without_hard_blocker(state: SpecState) -> None:
    dependency = node(1, state=state.value)
    candidate = node(2, dependencies=(1,))
    report = grain_dependency_report(candidate.id, [candidate, dependency])
    assert not report.eligible
    assert report.waiting_on == (dependency.id,)
    assert report.blocked_by == ()


@pytest.mark.parametrize("state", sorted(DEPENDENCY_BLOCKER_STATES, key=lambda item: item.value))
def test_direct_hard_blocker_is_reported(state: SpecState) -> None:
    dependency = node(1, state=state.value)
    candidate = node(2, dependencies=(1,))
    report = grain_dependency_report(candidate.id, [candidate, dependency])
    assert report.waiting_on == (dependency.id,)
    assert report.blocked_by == (dependency.id,)


def test_transitive_hard_blocker_propagates_through_waiting_chain() -> None:
    blocker = node(1, state="FAILED")
    middle = node(2, dependencies=(1,), state="READY")
    candidate = node(3, dependencies=(2,))
    report = grain_dependency_report(candidate.id, [candidate, blocker, middle])
    assert report.waiting_on == (middle.id,)
    assert report.blocked_by == (blocker.id,)


def test_satisfied_node_stops_historical_blocker_traversal() -> None:
    old_blocker = node(1, state="FAILED")
    verified = node(2, dependencies=(1,), state="VERIFIED")
    candidate = node(3, dependencies=(2,))
    report = grain_dependency_report(candidate.id, [candidate, old_blocker, verified])
    assert report.eligible
    assert report.blocked_by == ()


def test_waiting_and_blocker_lists_are_sorted() -> None:
    failed = node(1, state="FAILED")
    stale = node(2, state="STALE")
    middle = node(3, dependencies=(2, 1), state="READY")
    direct = node(4, state="RUNNING")
    candidate = node(5, dependencies=(4, 3))
    report = grain_dependency_report(candidate.id, [candidate, direct, middle, stale, failed])
    assert report.waiting_on == (middle.id, direct.id)
    assert report.blocked_by == (failed.id, stale.id)


def test_report_rejects_unknown_and_non_grain_candidate() -> None:
    with pytest.raises(ValueError, match="unknown"):
        grain_dependency_report("SG-000099", [node(1)])
    shaped = node(1, state="SHAPED")
    with pytest.raises(ValueError, match="must be in GRAIN"):
        grain_dependency_report(shaped.id, [shaped])


def test_ready_grains_are_sorted_and_only_grain_candidates() -> None:
    verified = node(1, state="VERIFIED")
    g3 = node(3, dependencies=(1,))
    g2 = node(2)
    ready_state = node(4, state="READY")
    assert [item.id for item in ready_grains([g3, ready_state, verified, g2])] == [
        "SG-000002",
        "SG-000003",
    ]


def test_ready_grains_fail_closed_on_invalid_graph() -> None:
    with pytest.raises(DependencyValidationError):
        ready_grains([node(1, dependencies=(9,))])


def test_dependency_waves_project_parallel_chain() -> None:
    verified = node(1, state="VERIFIED")
    a = node(2, dependencies=(1,))
    b = node(3, dependencies=(1,))
    c = node(4, dependencies=(2, 3))
    waves = dependency_waves([c, b, verified, a])
    assert [[node.id for node in wave] for wave in waves] == [
        ["SG-000002", "SG-000003"],
        ["SG-000004"],
    ]
    assert waves[0] == ready_grains([c, b, verified, a])


def test_unresolved_non_grain_dependency_excludes_wave_and_downstream() -> None:
    running = node(1, state="RUNNING")
    first = node(2, dependencies=(1,))
    second = node(3, dependencies=(2,))
    assert dependency_waves([second, first, running]) == ()


def test_hard_blocker_excludes_wave_and_downstream() -> None:
    failed = node(1, state="FAILED")
    first = node(2, dependencies=(1,))
    second = node(3, dependencies=(2,))
    assert dependency_waves([failed, first, second]) == ()


def test_independent_grain_can_project_when_another_chain_is_stuck() -> None:
    running = node(1, state="RUNNING")
    stuck = node(2, dependencies=(1,))
    free = node(3)
    waves = dependency_waves([stuck, free, running])
    assert [[item.id for item in wave] for wave in waves] == [[free.id]]


def test_dependency_analysis_does_not_mutate_nodes_or_input() -> None:
    verified = node(1, state="VERIFIED")
    candidate = node(2, dependencies=(1,))
    nodes = [candidate, verified]
    before = [item.to_dict() for item in nodes]
    grain_dependency_report(candidate.id, nodes)
    ready_grains(nodes)
    dependency_waves(nodes)
    assert [item.to_dict() for item in nodes] == before
