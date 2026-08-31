from __future__ import annotations

from pathlib import Path

import pytest

import specgrain.store as store_module
from specgrain import create_child_draft_spec, create_draft_spec, init_project, load_project


def test_parent_replace_can_overwrite_concurrent_edit_after_final_preimage_check(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reproduce the documented post-024 multi-writer race without fixing it."""

    init_project(tmp_path, project_id="post-024-observation")
    parent = create_draft_spec(tmp_path, title="Parent", outcome="Original outcome")
    parent_path = tmp_path / ".specgrain" / "specs" / f"{parent.id}.json"

    real_replace = store_module.os.replace
    injected = False

    def replace_with_concurrent_parent_edit(src: object, dst: object) -> None:
        nonlocal injected
        destination = Path(dst)
        if destination == parent_path and not injected:
            injected = True
            concurrent = parent.to_dict()
            concurrent["outcome"] = "Concurrent writer outcome"
            parent_path.write_text(
                store_module._json_text(concurrent),
                encoding="utf-8",
            )
        real_replace(src, dst)

    monkeypatch.setattr(store_module.os, "replace", replace_with_concurrent_parent_edit)

    result = create_child_draft_spec(
        tmp_path,
        parent_id=parent.id,
        title="Child",
        outcome="Child outcome",
    )

    assert injected is True
    stored = {node.id: node for node in load_project(tmp_path).specs}

    # The competing valid parent write occurred after _replace_json_exact's final
    # preimage check, but os.replace then overwrote it without detecting drift.
    assert stored[parent.id].outcome == "Original outcome"
    assert stored[parent.id].children == (result.child.id,)
    assert stored[parent.id].revision_digest == result.parent_after.revision_digest
    assert stored[result.child.id].parent_id == parent.id
    assert not (tmp_path / ".specgrain" / "tmp" / "authoring-transaction.json").exists()
