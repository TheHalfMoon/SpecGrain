from __future__ import annotations

from pathlib import Path

import pytest

import specgrain.pregrain as pregrain_module
from specgrain import create_child_draft_spec, create_draft_spec, init_project, load_project
from specgrain.refinement import validate_refinement
from specgrain.store import StoreValidationError


def _shape(root: Path, spec_id: str):
    return pregrain_module.shape_draft_spec(
        root,
        spec_id=spec_id,
        scope_in=("Implement observed mutation",),
        scope_out=("No provider integration",),
        acceptance=("Observed mutation acceptance passes",),
        dependencies=(),
        risk_level="low",
        recovery="Revert the bounded file change.",
        context_budget=2000,
        context_estimate=500,
        change_surface=("src/observed.py",),
        change_surface_exception=None,
        evidence=("observation-evidence",),
        minimality_choice="native",
        minimality_rationale="Use the existing native mutation path.",
        safety_status="none-identified",
        safety_requirements=(),
    )


def test_supported_child_authoring_can_be_overwritten_by_failed_pregrain_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    init_project(tmp_path, project_id="post-025-observation")
    parent = create_draft_spec(
        tmp_path,
        title="Parent candidate",
        outcome="Bounded parent outcome",
    )
    parent_path = tmp_path / ".specgrain" / "specs" / f"{parent.id}.json"

    real_replace = pregrain_module.os.replace
    injected = False
    child_result = None

    def replace_with_supported_child_writer(source, destination):
        nonlocal injected, child_result
        if not injected and Path(destination) == parent_path:
            injected = True
            child_result = create_child_draft_spec(
                tmp_path,
                parent_id=parent.id,
                title="Supported child",
                outcome="Supported child outcome",
            )
            child_committed = load_project(tmp_path)
            parent_after_child = next(
                node for node in child_committed.specs if node.id == parent.id
            )
            assert parent_after_child.children == (child_result.child.id,)
            assert child_result.child.parent_id == parent.id
        return real_replace(source, destination)

    monkeypatch.setattr(pregrain_module.os, "replace", replace_with_supported_child_writer)

    with pytest.raises(StoreValidationError, match="existing refinement is invalid"):
        _shape(tmp_path, parent.id)

    assert injected is True
    assert child_result is not None

    stored = load_project(tmp_path)
    by_id = {node.id: node for node in stored.specs}
    stored_parent = by_id[parent.id]
    stored_child = by_id[child_result.child.id]

    assert stored_parent.state == "SHAPED"
    assert stored_parent.children == ()
    assert stored_child.state == "DRAFT"
    assert stored_child.parent_id == parent.id
    assert validate_refinement(stored.specs)
