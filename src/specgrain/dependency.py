"""Deterministic dependency-graph validation and Grain eligibility analysis."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from enum import StrEnum

from .lifecycle import SpecState
from .model import SpecNode

DEPENDENCY_SATISFIED_STATES = frozenset({SpecState.VERIFIED, SpecState.CONTROLLED})
DEPENDENCY_BLOCKER_STATES = frozenset(
    {
        SpecState.BLOCKED,
        SpecState.FAILED,
        SpecState.STALE,
        SpecState.CANCELLED,
        SpecState.SUPERSEDED,
    }
)


class DependencyIssueCode(StrEnum):
    """Stable machine-readable dependency-graph issue codes."""

    DUPLICATE_ID = "DUPLICATE_ID"
    MISSING_DEPENDENCY = "MISSING_DEPENDENCY"
    SELF_DEPENDENCY = "SELF_DEPENDENCY"
    CYCLE = "CYCLE"


@dataclass(frozen=True, slots=True)
class DependencyIssue:
    """One deterministic dependency-graph structural problem."""

    code: DependencyIssueCode
    node_id: str
    dependency_id: str | None
    message: str


class DependencyValidationError(ValueError):
    """Raised when a dependency collection is structurally invalid."""

    def __init__(self, issues: tuple[DependencyIssue, ...]) -> None:
        self.issues = issues
        summary = "; ".join(issue.message for issue in issues)
        super().__init__(summary or "dependency validation failed")


@dataclass(frozen=True, slots=True)
class GrainDependencyReport:
    """Current dependency analysis for one Grain candidate."""

    node_id: str
    eligible: bool
    waiting_on: tuple[str, ...]
    blocked_by: tuple[str, ...]


def _materialize(nodes: Iterable[SpecNode]) -> tuple[SpecNode, ...]:
    materialized = tuple(nodes)
    for index, node in enumerate(materialized):
        if not isinstance(node, SpecNode):
            raise TypeError(f"nodes[{index}] must be a SpecNode")
    return materialized


def _issue_key(issue: DependencyIssue) -> tuple[str, str, str, str]:
    return (issue.code.value, issue.node_id, issue.dependency_id or "", issue.message)


def _canonical_cycle(cycle: list[str]) -> tuple[str, ...]:
    smallest = min(cycle)
    index = cycle.index(smallest)
    return tuple(cycle[index:] + cycle[:index])


def _adjacency(by_id: dict[str, SpecNode]) -> dict[str, tuple[str, ...]]:
    return {
        node_id: tuple(
            sorted(
                dependency_id
                for dependency_id in node.dependencies
                if dependency_id != node_id and dependency_id in by_id
            )
        )
        for node_id, node in sorted(by_id.items())
    }


def _find_cycles(by_id: dict[str, SpecNode]) -> set[tuple[str, ...]]:
    adjacency = _adjacency(by_id)
    state: dict[str, int] = {}
    cycles: set[tuple[str, ...]] = set()

    for start in sorted(adjacency):
        if state.get(start, 0) != 0:
            continue

        state[start] = 1
        path = [start]
        positions = {start: 0}
        stack: list[tuple[str, Iterator[str]]] = [(start, iter(adjacency[start]))]

        while stack:
            node_id, iterator = stack[-1]
            try:
                dependency_id = next(iterator)
            except StopIteration:
                state[node_id] = 2
                stack.pop()
                positions.pop(node_id, None)
                path.pop()
                continue

            dependency_state = state.get(dependency_id, 0)
            if dependency_state == 0:
                state[dependency_id] = 1
                positions[dependency_id] = len(path)
                path.append(dependency_id)
                stack.append((dependency_id, iter(adjacency[dependency_id])))
            elif dependency_state == 1:
                ring = path[positions[dependency_id] :]
                if len(ring) > 1:
                    cycles.add(_canonical_cycle(ring))

    return cycles


def validate_dependencies(nodes: Iterable[SpecNode]) -> tuple[DependencyIssue, ...]:
    """Return deterministic structural issues for SpecNode dependencies."""

    materialized = _materialize(nodes)
    counts = Counter(node.id for node in materialized)
    duplicates = sorted(node_id for node_id, count in counts.items() if count > 1)
    if duplicates:
        return tuple(
            DependencyIssue(
                DependencyIssueCode.DUPLICATE_ID,
                node_id,
                None,
                f"duplicate SpecNode id {node_id}",
            )
            for node_id in duplicates
        )

    by_id = {node.id: node for node in materialized}
    issues: list[DependencyIssue] = []

    for node_id in sorted(by_id):
        node = by_id[node_id]
        for dependency_id in sorted(node.dependencies):
            if dependency_id == node.id:
                issues.append(
                    DependencyIssue(
                        DependencyIssueCode.SELF_DEPENDENCY,
                        node.id,
                        dependency_id,
                        f"SpecNode {node.id} cannot depend on itself",
                    )
                )
            elif dependency_id not in by_id:
                issues.append(
                    DependencyIssue(
                        DependencyIssueCode.MISSING_DEPENDENCY,
                        node.id,
                        dependency_id,
                        f"SpecNode {node.id} references missing dependency {dependency_id}",
                    )
                )

    for cycle in sorted(_find_cycles(by_id)):
        path = " -> ".join((*cycle, cycle[0]))
        issues.append(
            DependencyIssue(
                DependencyIssueCode.CYCLE,
                cycle[0],
                cycle[1],
                f"dependency cycle detected: {path}",
            )
        )

    return tuple(sorted(issues, key=_issue_key))


def require_valid_dependencies(nodes: Iterable[SpecNode]) -> None:
    """Require a structurally valid dependency graph."""

    issues = validate_dependencies(nodes)
    if issues:
        raise DependencyValidationError(issues)


def _validated_by_id(nodes: Iterable[SpecNode]) -> dict[str, SpecNode]:
    materialized = _materialize(nodes)
    issues = validate_dependencies(materialized)
    if issues:
        raise DependencyValidationError(issues)
    return {node.id: node for node in materialized}


def grain_dependency_report(
    node_id: str, nodes: Iterable[SpecNode]
) -> GrainDependencyReport:
    """Return current waiting/blocker analysis for one Grain node."""

    by_id = _validated_by_id(nodes)
    if node_id not in by_id:
        raise ValueError(f"unknown SpecNode id {node_id}")
    node = by_id[node_id]
    if node.state != SpecState.GRAIN.value:
        raise ValueError(f"SpecNode {node_id} must be in GRAIN state for dependency eligibility")

    waiting_on = tuple(
        sorted(
            dependency_id
            for dependency_id in node.dependencies
            if SpecState(by_id[dependency_id].state) not in DEPENDENCY_SATISFIED_STATES
        )
    )

    blocked_by: set[str] = set()
    visited: set[str] = set()
    stack = list(reversed(waiting_on))
    while stack:
        current_id = stack.pop()
        if current_id in visited:
            continue
        visited.add(current_id)
        current = by_id[current_id]
        current_state = SpecState(current.state)
        if current_state in DEPENDENCY_SATISFIED_STATES:
            continue
        if current_state in DEPENDENCY_BLOCKER_STATES:
            blocked_by.add(current_id)
            continue
        for dependency_id in reversed(sorted(current.dependencies)):
            if dependency_id not in visited:
                stack.append(dependency_id)

    return GrainDependencyReport(
        node_id=node.id,
        eligible=not waiting_on,
        waiting_on=waiting_on,
        blocked_by=tuple(sorted(blocked_by)),
    )


def ready_grains(nodes: Iterable[SpecNode]) -> tuple[SpecNode, ...]:
    """Return current dependency-eligible Grain nodes in canonical ID order."""

    materialized = _materialize(nodes)
    require_valid_dependencies(materialized)
    grains = sorted(
        (node for node in materialized if node.state == SpecState.GRAIN.value),
        key=lambda node: node.id,
    )
    return tuple(
        node
        for node in grains
        if grain_dependency_report(node.id, materialized).eligible
    )


def dependency_waves(nodes: Iterable[SpecNode]) -> tuple[tuple[SpecNode, ...], ...]:
    """Project deterministic dependency-only waves for current Grain nodes."""

    materialized = _materialize(nodes)
    require_valid_dependencies(materialized)
    by_id = {node.id: node for node in materialized}
    completed = {
        node.id
        for node in materialized
        if SpecState(node.state) in DEPENDENCY_SATISFIED_STATES
    }
    pending = {
        node.id for node in materialized if node.state == SpecState.GRAIN.value
    }
    waves: list[tuple[SpecNode, ...]] = []

    while pending:
        wave_ids = tuple(
            node_id
            for node_id in sorted(pending)
            if all(dependency_id in completed for dependency_id in by_id[node_id].dependencies)
        )
        if not wave_ids:
            break
        waves.append(tuple(by_id[node_id] for node_id in wave_ids))
        pending.difference_update(wave_ids)
        completed.update(wave_ids)

    return tuple(waves)
