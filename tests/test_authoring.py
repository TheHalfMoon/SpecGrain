from __future__ import annotations

import json
from pathlib import Path

import pytest

import specgrain.store as store_module
from specgrain import (
    AuthoringRecoveryStatus,
    SpecNode,
    StoreValidationError,
    create_child_draft_spec,
    create_draft_spec,
    init_project,
    load_project,
    recover_authoring_transaction,
)


def _journal_fixture(root: Path) -> tuple[SpecNode, SpecNode, SpecNode, str]:
    parent = create_draft_spec(root, title="Parent", outcome="Parent outcome")
    parent_path = root / ".specgrain" / "specs" / f"{parent.id}.json"
    before_text = parent_path.read_text(encoding="utf-8")
    child = SpecNode(
        id="SG-000002",
        title="Child",
        outcome="Child outcome",
        parent_id=parent.id,
        state="DRAFT",
    )
    data = parent.to_dict()
    data["children"] = [child.id]
    parent_after = SpecNode.from_dict(data)
    store_module._write_authoring_journal(
        root,
        before_text,
        parent_after,
        child,
    )
    return parent, parent_after, child, before_text


def _write_exact(path: Path, node: SpecNode) -> None:
    path.write_text(store_module._json_text(node.to_dict()), encoding="utf-8")


def test_child_draft_api_creates_reciprocal_structure(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    parent = create_draft_spec(tmp_path, title="Parent", outcome="Parent outcome")

    result = create_child_draft_spec(
        tmp_path,
        parent_id=parent.id,
        title="Child",
        outcome="Child outcome",
        rationale="Keep decomposition explicit.",
    )

    assert result.child.id == "SG-000002"
    assert result.child.parent_id == parent.id
    assert result.child.state == "DRAFT"
    assert result.parent_before_revision == parent.revision_digest
    assert result.parent_after.state == "DRAFT"
    assert result.parent_after.children == (result.child.id,)
    assert result.parent_after.revision_digest != parent.revision_digest

    project = load_project(tmp_path)
    stored = {node.id: node for node in project.specs}
    assert stored[parent.id].children == (result.child.id,)
    assert stored[result.child.id].parent_id == parent.id
    assert not (tmp_path / ".specgrain" / "tmp" / "authoring-transaction.json").exists()


def test_child_draft_api_supports_nested_draft_authoring(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    root = create_draft_spec(tmp_path, title="Root", outcome="Root outcome")
    child = create_child_draft_spec(
        tmp_path,
        parent_id=root.id,
        title="Child",
        outcome="Child outcome",
    ).child
    grandchild = create_child_draft_spec(
        tmp_path,
        parent_id=child.id,
        title="Grandchild",
        outcome="Grandchild outcome",
    ).child

    project = load_project(tmp_path)
    by_id = {node.id: node for node in project.specs}
    assert by_id[root.id].children == (child.id,)
    assert by_id[child.id].children == (grandchild.id,)
    assert by_id[grandchild.id].parent_id == child.id
    assert all(node.state == "DRAFT" for node in project.specs)


def test_child_draft_rejects_non_draft_parent_without_journal(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    parent = create_draft_spec(tmp_path, title="Parent", outcome="Parent outcome")
    path = tmp_path / ".specgrain" / "specs" / f"{parent.id}.json"
    data = parent.to_dict()
    data["state"] = "SHAPED"
    path.write_text(store_module._json_text(data), encoding="utf-8")

    with pytest.raises(StoreValidationError, match="requires parent state DRAFT"):
        create_child_draft_spec(
            tmp_path,
            parent_id=parent.id,
            title="Child",
            outcome="Child outcome",
        )

    assert not (tmp_path / ".specgrain" / "tmp" / "authoring-transaction.json").exists()
    assert not (tmp_path / ".specgrain" / "specs" / "SG-000002.json").exists()


def test_child_draft_rejects_missing_or_invalid_parent(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    with pytest.raises(StoreValidationError, match="parent_id must match"):
        create_child_draft_spec(
            tmp_path,
            parent_id="bad",
            title="Child",
            outcome="Child outcome",
        )
    with pytest.raises(StoreValidationError, match="does not exist"):
        create_child_draft_spec(
            tmp_path,
            parent_id="SG-000001",
            title="Child",
            outcome="Child outcome",
        )


def test_child_draft_rejects_invalid_existing_forest_before_journal(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    parent = SpecNode(
        id="SG-000001",
        title="Parent",
        outcome="Parent outcome",
        children=["SG-000099"],
        state="DRAFT",
    )
    _write_exact(
        tmp_path / ".specgrain" / "specs" / "SG-000001.json",
        parent,
    )

    with pytest.raises(StoreValidationError, match="existing refinement is invalid"):
        create_child_draft_spec(
            tmp_path,
            parent_id=parent.id,
            title="Child",
            outcome="Child outcome",
        )
    assert not (tmp_path / ".specgrain" / "tmp" / "authoring-transaction.json").exists()


def test_pending_journal_blocks_reads_and_root_writes(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    _journal_fixture(tmp_path)

    with pytest.raises(StoreValidationError, match="explicit recovery"):
        load_project(tmp_path)
    with pytest.raises(StoreValidationError, match="explicit recovery"):
        create_draft_spec(tmp_path, title="Other", outcome="Other outcome")


def test_recovery_clears_no_write_journal(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    parent, _, child, before_text = _journal_fixture(tmp_path)

    result = recover_authoring_transaction(tmp_path)

    assert result.status is AuthoringRecoveryStatus.CLEARED
    assert result.parent_id == parent.id
    assert result.child_id == child.id
    parent_path = tmp_path / ".specgrain" / "specs" / f"{parent.id}.json"
    assert parent_path.read_text(encoding="utf-8") == before_text
    assert load_project(tmp_path).specs == (parent,)


def test_recovery_rolls_back_exact_child_only_write(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    parent, _, child, _ = _journal_fixture(tmp_path)
    child_path = tmp_path / ".specgrain" / "specs" / f"{child.id}.json"
    _write_exact(child_path, child)

    result = recover_authoring_transaction(tmp_path)

    assert result.status is AuthoringRecoveryStatus.ROLLED_BACK
    assert not child_path.exists()
    assert load_project(tmp_path).specs == (parent,)


def test_recovery_finalizes_completed_write_with_stale_journal(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    _, parent_after, child, _ = _journal_fixture(tmp_path)
    parent_path = tmp_path / ".specgrain" / "specs" / f"{parent_after.id}.json"
    child_path = tmp_path / ".specgrain" / "specs" / f"{child.id}.json"
    _write_exact(child_path, child)
    _write_exact(parent_path, parent_after)

    result = recover_authoring_transaction(tmp_path)

    assert result.status is AuthoringRecoveryStatus.FINALIZED
    project = load_project(tmp_path)
    assert {node.id: node for node in project.specs} == {
        parent_after.id: parent_after,
        child.id: child,
    }


def test_recovery_is_idempotent_when_no_journal_exists(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    result = recover_authoring_transaction(tmp_path)
    assert result.status is AuthoringRecoveryStatus.NONE
    assert result.parent_id is None
    assert result.child_id is None


def test_recovery_refuses_ambiguous_parent_without_mutation(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    parent, _, child, _ = _journal_fixture(tmp_path)
    parent_path = tmp_path / ".specgrain" / "specs" / f"{parent.id}.json"
    changed = parent.to_dict()
    changed["title"] = "Concurrent manual edit"
    changed_text = store_module._json_text(changed)
    parent_path.write_text(changed_text, encoding="utf-8")
    journal_path = tmp_path / ".specgrain" / "tmp" / "authoring-transaction.json"
    journal_before = journal_path.read_bytes()

    with pytest.raises(StoreValidationError, match="ambiguous"):
        recover_authoring_transaction(tmp_path)

    assert parent_path.read_text(encoding="utf-8") == changed_text
    assert not (tmp_path / ".specgrain" / "specs" / f"{child.id}.json").exists()
    assert journal_path.read_bytes() == journal_before


def test_parent_replace_failure_rolls_back_child_and_journal(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    init_project(tmp_path, project_id="demo")
    parent = create_draft_spec(tmp_path, title="Parent", outcome="Parent outcome")
    parent_path = tmp_path / ".specgrain" / "specs" / f"{parent.id}.json"
    parent_before = parent_path.read_bytes()

    def fail(*args: object, **kwargs: object) -> None:
        raise StoreValidationError(".specgrain/specs/SG-000001.json", "synthetic replace failure")

    monkeypatch.setattr(store_module, "_replace_json_exact", fail)
    with pytest.raises(StoreValidationError, match="synthetic replace failure"):
        create_child_draft_spec(
            tmp_path,
            parent_id=parent.id,
            title="Child",
            outcome="Child outcome",
        )

    assert parent_path.read_bytes() == parent_before
    assert not (tmp_path / ".specgrain" / "specs" / "SG-000002.json").exists()
    assert not (tmp_path / ".specgrain" / "tmp" / "authoring-transaction.json").exists()


def test_child_authoring_accepts_valid_noncanonical_parent_formatting(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    parent = create_draft_spec(tmp_path, title="Parent", outcome="Parent outcome")
    parent_path = tmp_path / ".specgrain" / "specs" / f"{parent.id}.json"
    compact = json.dumps(parent.to_dict(), sort_keys=True, ensure_ascii=False) + "\n"
    parent_path.write_text(compact, encoding="utf-8")

    result = create_child_draft_spec(
        tmp_path,
        parent_id=parent.id,
        title="Child",
        outcome="Child outcome",
    )

    assert result.child.parent_id == parent.id
    assert load_project(tmp_path).specs[0].children == (result.child.id,)
