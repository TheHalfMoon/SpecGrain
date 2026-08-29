from __future__ import annotations

import json
from pathlib import Path

import pytest

import specgrain.pregrain as pregrain_module
from specgrain import (
    GrainPromotionBlockedError,
    SpecNode,
    StoreValidationError,
    check_project,
    create_draft_spec,
    init_project,
    load_project,
    next_project,
    promote_refining_spec_to_grain,
    refine_shaped_spec,
    shape_draft_spec,
)


def _shape(root: Path, spec_id: str, **overrides: object):
    values: dict[str, object] = {
        "spec_id": spec_id,
        "scope_in": ("Implement bounded validation",),
        "scope_out": ("No provider integration",),
        "acceptance": ("Focused tests pass",),
        "dependencies": (),
        "risk_level": "low",
        "recovery": "Revert the bounded file change.",
        "context_budget": 2000,
        "context_estimate": 500,
        "change_surface": ("src/example.py", "tests/test_example.py"),
        "change_surface_exception": None,
        "evidence": ("focused-tests",),
        "minimality_choice": "native",
        "minimality_rationale": "The repository has no existing equivalent primitive.",
        "safety_status": "none-identified",
        "safety_requirements": (),
    }
    values.update(overrides)
    return shape_draft_spec(root, **values)  # type: ignore[arg-type]


def test_api_closes_draft_to_grain_preparation_loop(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    draft = create_draft_spec(tmp_path, title="Validate config", outcome="Reject invalid config")

    shaped = _shape(tmp_path, draft.id)
    assert shaped.source_state.value == "DRAFT"
    assert shaped.node.state == "SHAPED"
    assert shaped.node.revision_digest != draft.revision_digest
    shaped_revision = shaped.node.revision_digest

    refining = refine_shaped_spec(tmp_path, spec_id=draft.id)
    assert refining.source_state.value == "SHAPED"
    assert refining.node.state == "REFINING"
    assert refining.node.revision_digest == shaped_revision

    check = check_project(tmp_path)
    assert check.valid is True
    assert check.refining_leaf_count == 1
    assert check.grain_ready_count == 1
    assert check.readiness_blocked == ()

    grain = promote_refining_spec_to_grain(tmp_path, spec_id=draft.id)
    assert grain.source_state.value == "REFINING"
    assert grain.node.state == "GRAIN"
    assert grain.node.revision_digest == shaped_revision

    next_result = next_project(tmp_path)
    assert next_result.valid is True
    assert next_result.eligible_ids == (draft.id,)


def test_shape_persists_only_authorized_semantic_fields(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    draft = create_draft_spec(
        tmp_path,
        title="Bounded candidate",
        outcome="One result",
        rationale="Original rationale",
    )

    result = _shape(tmp_path, draft.id)
    stored = result.node

    assert stored.id == draft.id
    assert stored.title == draft.title
    assert stored.outcome == draft.outcome
    assert stored.rationale == draft.rationale
    assert stored.parent_id == draft.parent_id
    assert stored.children == draft.children
    assert stored.labels == draft.labels
    assert stored.method == draft.method
    assert stored.schema_version == draft.schema_version
    assert stored.scope_in == ("Implement bounded validation",)
    assert stored.scope_out == ("No provider integration",)
    assert stored.acceptance == ("Focused tests pass",)
    assert stored.risk == {
        "level": "low",
        "recovery": "Revert the bounded file change.",
    }
    assert stored.context == {"budget_tokens": 2000, "estimated_tokens": 500}
    assert stored.change_surface == ("src/example.py", "tests/test_example.py")
    assert stored.evidence == {"required": ["focused-tests"]}
    assert stored.metadata["readiness"] == {
        "version": 1,
        "unresolved_decisions": [],
        "minimality": {
            "choice": "native",
            "rationale": "The repository has no existing equivalent primitive.",
        },
        "safety": {"status": "none-identified", "requirements": []},
    }


def test_shape_accepts_explicit_change_surface_exception(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    draft = create_draft_spec(tmp_path, title="Docs", outcome="Clarify contract")

    shaped = _shape(
        tmp_path,
        draft.id,
        change_surface=(),
        change_surface_exception="No repository file mutation is expected.",
    ).node

    assert shaped.change_surface == ()
    readiness = shaped.metadata["readiness"]
    assert isinstance(readiness, dict)
    assert readiness["change_surface_exception"] == "No repository file mutation is expected."


def test_shape_rejects_readiness_blocker_without_mutation(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    draft = create_draft_spec(tmp_path, title="Context", outcome="Bound context")
    path = tmp_path / ".specgrain" / "specs" / f"{draft.id}.json"
    before = path.read_bytes()

    with pytest.raises(StoreValidationError, match="CONTEXT_BUDGET_EXCEEDED"):
        _shape(tmp_path, draft.id, context_budget=100, context_estimate=101)

    assert path.read_bytes() == before
    assert load_project(tmp_path).specs[0].state == "DRAFT"


def test_shape_rejects_missing_dependency_without_mutation(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    draft = create_draft_spec(tmp_path, title="Dependency", outcome="Use dependency")
    path = tmp_path / ".specgrain" / "specs" / f"{draft.id}.json"
    before = path.read_bytes()

    with pytest.raises(StoreValidationError, match="MISSING_DEPENDENCY"):
        _shape(tmp_path, draft.id, dependencies=("SG-000099",))

    assert path.read_bytes() == before


def test_shape_refuses_pending_authoring_transaction(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    draft = create_draft_spec(tmp_path, title="Pending", outcome="Remain unchanged")
    tmp_dir = tmp_path / ".specgrain" / "tmp"
    tmp_dir.mkdir()
    journal = tmp_dir / "authoring-transaction.json"
    journal.write_text("{}\n", encoding="utf-8")

    with pytest.raises(StoreValidationError, match="explicit recovery"):
        _shape(tmp_path, draft.id)

    raw = json.loads(
        (tmp_path / ".specgrain" / "specs" / f"{draft.id}.json").read_text(
            encoding="utf-8"
        )
    )
    assert raw["state"] == "DRAFT"


def test_shape_detects_exact_preimage_drift(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    init_project(tmp_path, project_id="demo")
    draft = create_draft_spec(tmp_path, title="Concurrent", outcome="Detect drift")
    path = tmp_path / ".specgrain" / "specs" / f"{draft.id}.json"
    original_read = pregrain_module._read_text
    calls = 0

    def drift(target: Path, location: str) -> str:
        nonlocal calls
        text = original_read(target, location)
        if target == path:
            calls += 1
            if calls == 2:
                data = json.loads(text)
                data["title"] = "Concurrent manual edit"
                target.write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")
                return original_read(target, location)
        return text

    monkeypatch.setattr(pregrain_module, "_read_text", drift)
    with pytest.raises(StoreValidationError, match="changed during pre-Grain mutation"):
        _shape(tmp_path, draft.id)

    assert json.loads(path.read_text(encoding="utf-8"))["title"] == "Concurrent manual edit"


def test_state_transitions_reject_wrong_sources_without_mutation(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    draft = create_draft_spec(tmp_path, title="State", outcome="Stay legal")
    path = tmp_path / ".specgrain" / "specs" / f"{draft.id}.json"
    before = path.read_bytes()

    with pytest.raises(StoreValidationError, match="requires source state SHAPED"):
        refine_shaped_spec(tmp_path, spec_id=draft.id)
    with pytest.raises(StoreValidationError, match="requires source state REFINING"):
        promote_refining_spec_to_grain(tmp_path, spec_id=draft.id)

    assert path.read_bytes() == before


def test_grain_blocker_reports_exact_issues_and_does_not_mutate(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    draft = create_draft_spec(tmp_path, title="Blocked", outcome="Stay refining")
    _shape(tmp_path, draft.id)
    refining = refine_shaped_spec(tmp_path, spec_id=draft.id).node
    path = tmp_path / ".specgrain" / "specs" / f"{draft.id}.json"

    data = refining.to_dict()
    data["acceptance"] = []
    path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    before = path.read_bytes()

    with pytest.raises(GrainPromotionBlockedError) as captured:
        promote_refining_spec_to_grain(tmp_path, spec_id=draft.id)

    assert [issue.code.value for issue in captured.value.report.issues] == [
        "ACCEPTANCE_REQUIRED"
    ]
    assert path.read_bytes() == before
    assert load_project(tmp_path).specs[0].state == "REFINING"


def test_shape_rejects_noncanonical_id_and_invalid_safety_contract(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    draft = create_draft_spec(tmp_path, title="Safety", outcome="Declare safety")

    with pytest.raises(StoreValidationError, match="spec_id must match"):
        _shape(tmp_path, "bad")
    with pytest.raises(StoreValidationError, match="safety_requirements are required"):
        _shape(
            tmp_path,
            draft.id,
            safety_status="requirements-defined",
            safety_requirements=(),
        )
