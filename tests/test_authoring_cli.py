from __future__ import annotations

import json
from pathlib import Path

import pytest

import specgrain.cli as cli_module
import specgrain.store as store_module
from specgrain import SpecNode, create_draft_spec
from specgrain.cli import main


def _pending_journal(root: Path) -> tuple[SpecNode, SpecNode]:
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
    parent_data = parent.to_dict()
    parent_data["children"] = [child.id]
    parent_after = SpecNode.from_dict(parent_data)
    store_module._write_authoring_journal(
        root,
        before_text,
        parent_after,
        child,
    )
    return parent, child


def test_cli_child_draft_text_preserves_draft_states(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()
    assert main(
        [
            "draft",
            str(tmp_path),
            "--title",
            "Parent",
            "--outcome",
            "Parent outcome",
        ]
    ) == 0
    capsys.readouterr()

    assert main(
        [
            "draft",
            str(tmp_path),
            "--parent",
            "SG-000001",
            "--title",
            "Child",
            "--outcome",
            "Child outcome",
        ]
    ) == 0
    out = capsys.readouterr().out
    assert "SpecGrain draft: CREATED" in out
    assert "Spec: SG-000002" in out
    assert "State: DRAFT" in out
    assert "Parent: SG-000001" in out
    assert "Parent revision before: sha256:" in out
    assert "Parent revision after: sha256:" in out
    assert "PASS" not in out

    assert main(["check", str(tmp_path)]) == 0
    check = capsys.readouterr().out
    assert "Specs: 2" in check
    assert "Roots: 1" in check
    assert "Grain-ready: 0" in check


def test_cli_child_draft_json_is_deterministic_shape(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()
    assert main(
        [
            "draft",
            str(tmp_path),
            "--title",
            "Parent",
            "--outcome",
            "Parent outcome",
        ]
    ) == 0
    capsys.readouterr()

    assert main(
        [
            "draft",
            str(tmp_path),
            "--parent",
            "SG-000001",
            "--title",
            "Child",
            "--outcome",
            "Child outcome",
            "--json",
        ]
    ) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["spec_id"] == "SG-000002"
    assert payload["state"] == "DRAFT"
    assert payload["parent_id"] == "SG-000001"
    assert payload["file"] == ".specgrain/specs/SG-000002.json"
    assert payload["parent_file"] == ".specgrain/specs/SG-000001.json"
    assert payload["revision_digest"].startswith("sha256:")
    assert payload["parent_revision_before"].startswith("sha256:")
    assert payload["parent_revision_after"].startswith("sha256:")
    assert payload["parent_revision_before"] != payload["parent_revision_after"]


def test_cli_child_draft_non_draft_parent_is_nonzero(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()
    parent = create_draft_spec(tmp_path, title="Parent", outcome="Parent outcome")
    path = tmp_path / ".specgrain" / "specs" / f"{parent.id}.json"
    data = parent.to_dict()
    data["state"] = "SHAPED"
    path.write_text(store_module._json_text(data), encoding="utf-8")

    assert main(
        [
            "draft",
            str(tmp_path),
            "--parent",
            parent.id,
            "--title",
            "Child",
            "--outcome",
            "Child outcome",
            "--json",
        ]
    ) == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.err)
    assert payload["valid"] is False
    assert "requires parent state DRAFT" in payload["error"]
    assert captured.out == ""


def test_cli_recover_none_text_and_json(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()

    assert main(["recover", str(tmp_path)]) == 0
    assert capsys.readouterr().out == "SpecGrain recover: NONE\n"

    assert main(["recover", str(tmp_path), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == {"child_id": None, "parent_id": None, "status": "none"}


def test_cli_recover_clears_pending_no_write_transaction(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()
    parent, child = _pending_journal(tmp_path)

    assert main(["check", str(tmp_path)]) == 1
    check = capsys.readouterr().out
    assert "STORE_INVALID" in check
    assert "explicit recovery" in check

    assert main(["recover", str(tmp_path), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "child_id": child.id,
        "parent_id": parent.id,
        "status": "cleared",
    }
    assert main(["check", str(tmp_path)]) == 0


def test_cli_child_draft_internal_error_is_redacted(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()

    def fail(*args: object, **kwargs: object) -> object:
        raise RuntimeError("secret detail")

    monkeypatch.setattr(cli_module, "create_child_draft_spec", fail)
    assert main(
        [
            "draft",
            str(tmp_path),
            "--parent",
            "SG-000001",
            "--title",
            "Child",
            "--outcome",
            "Child outcome",
        ]
    ) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "SpecGrain draft: FAIL\n- internal error\n"
    assert "secret detail" not in captured.err


def test_cli_recover_internal_error_is_redacted(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail(*args: object, **kwargs: object) -> object:
        raise RuntimeError("secret detail")

    monkeypatch.setattr(cli_module, "recover_authoring_transaction", fail)
    assert main(["recover", str(tmp_path), "--json"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "SpecGrain recover: FAIL\n- internal error\n"
    assert "secret detail" not in captured.err
