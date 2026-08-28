"""Deterministic structural validation for recursive SpecNode refinement forests."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

from .model import SpecNode


class RefinementIssueCode(StrEnum):
    """Stable machine-readable refinement validation issue codes."""

    DUPLICATE_ID = "DUPLICATE_ID"
    MISSING_PARENT = "MISSING_PARENT"
    MISSING_CHILD = "MISSING_CHILD"
    SELF_PARENT = "SELF_PARENT"
    SELF_CHILD = "SELF_CHILD"
    PARENT_CHILD_MISMATCH = "PARENT_CHILD_MISMATCH"
    CHILD_PARENT_MISMATCH = "CHILD_PARENT_MISMATCH"
    CYCLE = "CYCLE"


@dataclass(frozen=True, slots=True)
class RefinementIssue:
    """One deterministic structural refinement problem."""

    code: RefinementIssueCode
    node_id: str
    related_id: str | None
    message: str


class RefinementValidationError(ValueError):
    """Raised when a refinement collection is not a structurally valid forest."""

    def __init__(self, issues: tuple[RefinementIssue, ...]) -> None:
        self.issues = issues
        summary = "; ".join(issue.message for issue in issues)
        super().__init__(summary or "refinement validation failed")


def _materialize(nodes: Iterable[SpecNode]) -> tuple[SpecNode, ...]:
    materialized = tuple(nodes)
    for index, node in enumerate(materialized):
        if not isinstance(node, SpecNode):
            raise TypeError(f"nodes[{index}] must be a SpecNode")
    return materialized


def _issue_key(issue: RefinementIssue) -> tuple[str, str, str, str]:
    return (issue.code.value, issue.node_id, issue.related_id or "", issue.message)


def _canonical_cycle(cycle: list[str]) -> tuple[str, ...]:
    """Rotate a directed cycle ring so its smallest canonical ID is first."""

    smallest = min(cycle)
    index = cycle.index(smallest)
    return tuple(cycle[index:] + cycle[:index])


def _find_parent_cycles(by_id: dict[str, SpecNode]) -> set[tuple[str, ...]]:
    cycles: set[tuple[str, ...]] = set()

    for start in sorted(by_id):
        positions: dict[str, int] = {}
        path: list[str] = []
        current = start

        while current in by_id and current not in positions:
            positions[current] = len(path)
            path.append(current)
            parent_id = by_id[current].parent_id
            if parent_id is None or parent_id == current or parent_id not in by_id:
                current = ""
                break
            current = parent_id

        if current and current in positions:
            ring = path[positions[current] :]
            if len(ring) > 1:
                cycles.add(_canonical_cycle(ring))

    return cycles


def validate_refinement(nodes: Iterable[SpecNode]) -> tuple[RefinementIssue, ...]:
    """Return deterministic structural issues for a proposed refinement forest."""

    materialized = _materialize(nodes)
    counts = Counter(node.id for node in materialized)
    duplicates = sorted(node_id for node_id, count in counts.items() if count > 1)
    if duplicates:
        return tuple(
            RefinementIssue(
                RefinementIssueCode.DUPLICATE_ID,
                node_id,
                None,
                f"duplicate SpecNode id {node_id}",
            )
            for node_id in duplicates
        )

    by_id = {node.id: node for node in materialized}
    issues: list[RefinementIssue] = []

    for node_id in sorted(by_id):
        node = by_id[node_id]

        if node.parent_id == node.id:
            issues.append(
                RefinementIssue(
                    RefinementIssueCode.SELF_PARENT,
                    node.id,
                    node.id,
                    f"SpecNode {node.id} cannot be its own parent",
                )
            )
        elif node.parent_id is not None and node.parent_id not in by_id:
            issues.append(
                RefinementIssue(
                    RefinementIssueCode.MISSING_PARENT,
                    node.id,
                    node.parent_id,
                    f"SpecNode {node.id} references missing parent {node.parent_id}",
                )
            )

        for child_id in sorted(node.children):
            if child_id == node.id:
                issues.append(
                    RefinementIssue(
                        RefinementIssueCode.SELF_CHILD,
                        node.id,
                        child_id,
                        f"SpecNode {node.id} cannot include itself as a child",
                    )
                )
            elif child_id not in by_id:
                issues.append(
                    RefinementIssue(
                        RefinementIssueCode.MISSING_CHILD,
                        node.id,
                        child_id,
                        f"SpecNode {node.id} references missing child {child_id}",
                    )
                )

    for node_id in sorted(by_id):
        child = by_id[node_id]
        parent_id = child.parent_id
        if parent_id is not None and parent_id != child.id and parent_id in by_id:
            parent = by_id[parent_id]
            if child.id not in parent.children:
                issues.append(
                    RefinementIssue(
                        RefinementIssueCode.PARENT_CHILD_MISMATCH,
                        child.id,
                        parent.id,
                        f"SpecNode {child.id} declares parent {parent.id}, "
                        f"but {parent.id} does not list {child.id} as a child",
                    )
                )

        for child_id in sorted(child.children):
            if child_id == child.id or child_id not in by_id:
                continue
            declared_child = by_id[child_id]
            if declared_child.parent_id != child.id:
                actual_parent = declared_child.parent_id or "none"
                issues.append(
                    RefinementIssue(
                        RefinementIssueCode.CHILD_PARENT_MISMATCH,
                        child.id,
                        child_id,
                        f"SpecNode {child.id} lists child {child_id}, "
                        f"but {child_id} declares parent {actual_parent}",
                    )
                )

    for cycle in sorted(_find_parent_cycles(by_id)):
        path = " -> ".join((*cycle, cycle[0]))
        issues.append(
            RefinementIssue(
                RefinementIssueCode.CYCLE,
                cycle[0],
                cycle[1],
                f"refinement cycle detected: {path}",
            )
        )

    return tuple(sorted(issues, key=_issue_key))


def require_valid_refinement(nodes: Iterable[SpecNode]) -> None:
    """Require a structurally valid refinement forest."""

    issues = validate_refinement(nodes)
    if issues:
        raise RefinementValidationError(issues)


def refinement_roots(nodes: Iterable[SpecNode]) -> tuple[SpecNode, ...]:
    """Return deterministic roots for a valid refinement forest."""

    materialized = _materialize(nodes)
    issues = validate_refinement(materialized)
    if issues:
        raise RefinementValidationError(issues)
    return tuple(
        sorted((node for node in materialized if node.parent_id is None), key=lambda node: node.id)
    )
