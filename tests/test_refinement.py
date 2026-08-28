from __future__ import annotations

import itertools

import pytest

from specgrain import (
    RefinementIssueCode,
    RefinementValidationError,
    SpecNode,
    refinement_roots,
    require_valid_refinement,
    validate_refinement,
)


def node(num: int, *, parent: int | None = None, children: tuple[int, ...] = ()) -> SpecNode:
    return SpecNode(
        id=f"SG-{num:06d}",
        title=f"Node {num}",
        outcome=f"Outcome {num}",
        parent_id=None if parent is None else f"SG-{parent:06d}",
        children=tuple(f"SG-{child:06d}" for child in children),
    )


def codes(nodes: object) -> list[RefinementIssueCode]:
    return [issue.code for issue in validate_refinement(nodes)]  # type: ignore[arg-type]


def test_empty_and_single_root_are_valid() -> None:
    assert validate_refinement([]) == ()
    root = node(1)
    assert validate_refinement([root]) == ()
    assert refinement_roots([root]) == (root,)


def test_multiple_roots_are_sorted() -> None:
    one, two, three = node(1), node(2), node(3)
    assert [item.id for item in refinement_roots([three, one, two])] == [
        "SG-000001",
        "SG-000002",
        "SG-000003",
    ]


def test_deep_valid_tree() -> None:
    nodes = [node(1, children=(2,)), node(2, parent=1, children=(3,)), node(3, parent=2)]
    assert validate_refinement(nodes) == ()
    require_valid_refinement(nodes)


def test_duplicate_ids_are_identity_blocker_only() -> None:
    issues = validate_refinement([node(1), node(1), node(2, parent=99)])
    assert len(issues) == 1
    assert issues[0].code is RefinementIssueCode.DUPLICATE_ID
    assert issues[0].node_id == "SG-000001"


def test_non_specnode_member_is_rejected() -> None:
    with pytest.raises(TypeError, match=r"nodes\[1\] must be a SpecNode"):
        validate_refinement([node(1), object()])  # type: ignore[list-item]


def test_missing_parent_and_child() -> None:
    issues = validate_refinement([node(1, children=(9,)), node(2, parent=8)])
    assert {issue.code for issue in issues} == {
        RefinementIssueCode.MISSING_CHILD,
        RefinementIssueCode.MISSING_PARENT,
    }


def test_self_parent_and_self_child() -> None:
    issues = validate_refinement([node(1, parent=1, children=(1,))])
    issue_codes = {issue.code for issue in issues}
    assert issue_codes == {RefinementIssueCode.SELF_CHILD, RefinementIssueCode.SELF_PARENT}
    assert RefinementIssueCode.CYCLE not in issue_codes


def test_child_parent_pointer_missing_from_parent_children() -> None:
    issues = validate_refinement([node(1), node(2, parent=1)])
    assert [issue.code for issue in issues] == [RefinementIssueCode.PARENT_CHILD_MISMATCH]
    assert issues[0].node_id == "SG-000002"
    assert issues[0].related_id == "SG-000001"


def test_parent_child_declaration_disagrees_with_child_parent() -> None:
    nodes = [node(1, children=(3,)), node(2), node(3, parent=2)]
    found = validate_refinement(nodes)
    assert {issue.code for issue in found} == {
        RefinementIssueCode.CHILD_PARENT_MISMATCH,
        RefinementIssueCode.PARENT_CHILD_MISMATCH,
    }


def test_parent_lists_child_with_no_parent() -> None:
    issues = validate_refinement([node(1, children=(2,)), node(2)])
    assert [issue.code for issue in issues] == [RefinementIssueCode.CHILD_PARENT_MISMATCH]


def test_two_node_cycle_is_canonical() -> None:
    nodes = [node(2, parent=1, children=(1,)), node(1, parent=2, children=(2,))]
    cycle = [
        issue for issue in validate_refinement(nodes) if issue.code is RefinementIssueCode.CYCLE
    ]
    assert len(cycle) == 1
    assert cycle[0].message == (
        "refinement cycle detected: SG-000001 -> SG-000002 -> SG-000001"
    )


def test_three_node_cycle_is_canonical_independent_of_input_order() -> None:
    nodes = [
        node(1, parent=3, children=(2,)),
        node(2, parent=1, children=(3,)),
        node(3, parent=2, children=(1,)),
    ]
    expected = validate_refinement(nodes)
    assert [issue.code for issue in expected] == [RefinementIssueCode.CYCLE]
    assert expected[0].message == (
        "refinement cycle detected: SG-000001 -> SG-000003 -> SG-000002 -> SG-000001"
    )
    for permutation in itertools.permutations(nodes):
        assert validate_refinement(permutation) == expected


def test_issue_order_is_input_order_invariant() -> None:
    nodes = [node(3, parent=9), node(1, children=(8,)), node(2, children=(2,))]
    expected = validate_refinement(nodes)
    for permutation in itertools.permutations(nodes):
        assert validate_refinement(permutation) == expected


def test_aggregate_error_preserves_exact_issues() -> None:
    nodes = [node(1, children=(9,))]
    issues = validate_refinement(nodes)
    with pytest.raises(RefinementValidationError) as caught:
        require_valid_refinement(nodes)
    assert caught.value.issues == issues


def test_root_query_fails_closed_for_invalid_forest() -> None:
    with pytest.raises(RefinementValidationError):
        refinement_roots([node(1, children=(9,))])


def test_children_authored_order_is_structurally_irrelevant() -> None:
    first = [node(1, children=(3, 2)), node(2, parent=1), node(3, parent=1)]
    second = [node(1, children=(2, 3)), node(2, parent=1), node(3, parent=1)]
    assert validate_refinement(first) == validate_refinement(second) == ()
