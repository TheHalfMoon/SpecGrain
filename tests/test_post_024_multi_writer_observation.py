from __future__ import annotations

from pathlib import Path

import pytest

import specgrain.pregrain as pregrain_module
from specgrain import create_draft_spec, init_project, load_project, shape_draft_spec


def _shape(root: Path, spec_id: str, marker: str):
    return shape_draft_spec(
        root,
        spec_id=spec_id,
        scope_in=(f"Implement {marker}",),
        scope_out=("No provider integration",),
        acceptance=(f"{marker} acceptance passes",),
        dependencies=(),
        risk_level="low",
        recovery="Revert the bounded file change.",
        context_budget=2000,
        context_estimate=500,
        change_surface=(f"src/{marker}.py",),
        change_surface_exception=None,
        evidence=(f"{marker}-evidence",),
        minimality_choice="native",
        minimality_rationale="Use the existing native mutation path.",
        safety_status="none-identified",
        safety_requirements=(),
    )


def test_supported_pregrain_writer_can_lose_successful_competing_write(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reproduce the documented post-024 supported multi-writer race without fixing it."""

    init_project(tmp_path, project_id="post-024-observation")
    draft = create_draft_spec(tmp_path, title="Candidate", outcome="Bounded outcome")
    spec_path = tmp_path / ".specgrain" / "specs" / f"{draft.id}.json"

    real_replace = pregrain_module.os.replace
    competing_result = None
    injecting_competing_writer = False

    def replace_with_supported_competing_shape(src: Path, dst: Path) -> None:
        nonlocal competing_result, injecting_competing_writer
        destination = Path(dst)
        if (
            destination == spec_path
            and competing_result is None
            and not injecting_competing_writer
        ):
            # Writer B uses the same supported public mutation API. It loads the
            # still-DRAFT preimage, commits a distinct SHAPED value, confirms it,
            # and returns success while writer A is paused immediately before its
            # own unconditional os.replace. Nested replacement by writer B uses
            # the real primitive so this fixture injects exactly one competitor.
            injecting_competing_writer = True
            try:
                competing_result = _shape(tmp_path, draft.id, "writer_b")
            finally:
                injecting_competing_writer = False
        real_replace(src, dst)

    monkeypatch.setattr(
        pregrain_module.os,
        "replace",
        replace_with_supported_competing_shape,
    )

    writer_a = _shape(tmp_path, draft.id, "writer_a")

    assert competing_result is not None
    writer_b = competing_result
    assert writer_b.node.scope_in == ("Implement writer_b",)
    assert writer_a.node.scope_in == ("Implement writer_a",)
    assert writer_b.node.revision_digest != writer_a.node.revision_digest

    stored = load_project(tmp_path).specs[0]

    # Both supported calls returned success, but writer A's later os.replace
    # silently overwrote writer B after A's final preimage check had already run.
    assert stored.revision_digest == writer_a.node.revision_digest
    assert stored.scope_in == ("Implement writer_a",)
    assert stored.revision_digest != writer_b.node.revision_digest
