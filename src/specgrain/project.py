"""Local project orchestration for dependency-aware checks and next-set reporting."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from .dependency import (
    GrainDependencyReport,
    dependency_waves,
    grain_dependency_report,
    ready_grains,
    validate_dependencies,
)
from .lifecycle import SpecState
from .refinement import refinement_roots, validate_refinement
from .store import (
    ProjectCheckIssue,
    ProjectCheckResult,
    StoreError,
    load_project,
)
from .store import (
    check_project as _store_check_project,
)


@dataclass(frozen=True, slots=True)
class NextResult:
    valid: bool
    project_id: str | None
    eligible_ids: tuple[str, ...]
    dependency_reports: tuple[GrainDependencyReport, ...]
    waves: tuple[tuple[str, ...], ...]
    issues: tuple[ProjectCheckIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "project_id": self.project_id,
            "eligible": list(self.eligible_ids),
            "candidates": [
                {
                    "node_id": report.node_id,
                    "eligible": report.eligible,
                    "waiting_on": list(report.waiting_on),
                    "blocked_by": list(report.blocked_by),
                }
                for report in self.dependency_reports
            ],
            "waves": [list(wave) for wave in self.waves],
            "issues": [issue.to_dict() for issue in self.issues],
        }


def _mapped_dependency_issues(project) -> tuple[ProjectCheckIssue, ...]:
    return tuple(
        ProjectCheckIssue(
            issue.code.value,
            f".specgrain/specs/{issue.node_id}.json",
            issue.message,
        )
        for issue in validate_dependencies(project.specs)
    )


def check_project(root: str | os.PathLike[str] = ".") -> ProjectCheckResult:
    """Run the 005 check plus 006 dependency-graph validation without mutation."""

    try:
        project = load_project(root)
    except StoreError:
        return _store_check_project(root)

    refinement_issues = validate_refinement(project.specs)
    if refinement_issues:
        return _store_check_project(root)

    dependency_issues = _mapped_dependency_issues(project)
    if dependency_issues:
        return ProjectCheckResult(
            valid=False,
            project_id=project.manifest.project_id,
            policy_name=project.manifest.policy,
            readiness_mode=project.policy.readiness_mode,
            spec_count=len(project.specs),
            root_count=len(refinement_roots(project.specs)),
            refining_leaf_count=0,
            grain_ready_count=0,
            readiness_blocked=(),
            issues=dependency_issues,
        )

    return _store_check_project(root)


def next_project(root: str | os.PathLike[str] = ".") -> NextResult:
    """Return current dependency-eligible Grains and advisory waves without mutation."""

    try:
        project = load_project(root)
    except StoreError as exc:
        return NextResult(
            valid=False,
            project_id=None,
            eligible_ids=(),
            dependency_reports=(),
            waves=(),
            issues=(ProjectCheckIssue("STORE_INVALID", exc.location, exc.detail),),
        )

    refinement_issues = validate_refinement(project.specs)
    if refinement_issues:
        return NextResult(
            valid=False,
            project_id=project.manifest.project_id,
            eligible_ids=(),
            dependency_reports=(),
            waves=(),
            issues=tuple(
                ProjectCheckIssue(
                    issue.code.value,
                    f".specgrain/specs/{issue.node_id}.json",
                    issue.message,
                )
                for issue in refinement_issues
            ),
        )

    dependency_issues = _mapped_dependency_issues(project)
    if dependency_issues:
        return NextResult(
            valid=False,
            project_id=project.manifest.project_id,
            eligible_ids=(),
            dependency_reports=(),
            waves=(),
            issues=dependency_issues,
        )

    grain_nodes = tuple(
        node for node in project.specs if node.state == SpecState.GRAIN.value
    )
    reports = tuple(
        grain_dependency_report(node.id, project.specs) for node in grain_nodes
    )
    eligible = ready_grains(project.specs)
    waves = dependency_waves(project.specs)
    return NextResult(
        valid=True,
        project_id=project.manifest.project_id,
        eligible_ids=tuple(node.id for node in eligible),
        dependency_reports=reports,
        waves=tuple(tuple(node.id for node in wave) for wave in waves),
        issues=(),
    )
