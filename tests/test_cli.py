from __future__ import annotations

import json
from pathlib import Path

import pytest

import specgrain.cli as cli_module
import specgrain.store as store_module
from specgrain import SpecNode, SpecValidationError, StoreExistsError, create_draft_spec
from specgrain.cli import main


def write_json(path: Path, value: object) -> None:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")


def blocked_spec() -> SpecNode:
    return SpecNode(
        id="SG-000001",
        title="Blocked",
        outcome="Blocked outcome",
        scope_in=["bounded"],
        acceptance=[],
        risk={"level": "low", "recovery": "revert"},
        context={"budget_tokens": 1000, "estimated_tokens": 500},
        change_surface=["src/x.py"],
        evidence={"required": ["tests"]},
        metadata={
            "readiness": {
                "version": 1,
                "unresolved_decisions": [],
                "minimality": {"choice": "new-code", "rationale": "bounded"},
                "safety": {"status": "none-identified", "requirements": []},
            }
        },
        state="REFINING",
    )


def test_cli_init_and_check_text(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    init_out = capsys.readouterr().out
    assert "SpecGrain init: PASS" in init_out
    assert "Project: demo" in init_out

    assert main(["check", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "SpecGrain check: PASS" in out
    assert "Specs: 0" in out
    assert "Policy: default (readiness=report)" in out


def test_cli_init_refusal_returns_one_and_stderr(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 1
    captured = capsys.readouterr()
    assert "SpecGrain init: FAIL" in captured.err
    assert "refusing overwrite" in captured.err


def test_cli_check_json_is_deterministic(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()
    assert main(["check", str(tmp_path), "--json"]) == 0
    first = capsys.readouterr().out
    assert main(["check", str(tmp_path), "--json"]) == 0
    second = capsys.readouterr().out
    assert first == second
    payload = json.loads(first)
    assert payload["valid"] is True
    assert payload["project_id"] == "demo"
    assert payload["policy"] == "default"
    assert "root" not in payload


def test_create_draft_api_creates_safe_root_and_allocates_ids(tmp_path: Path) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    first = create_draft_spec(
        tmp_path,
        title="First capability",
        outcome="A bounded capability exists",
        rationale="Start with one root DRAFT.",
    )
    second = create_draft_spec(
        tmp_path,
        title="Second capability",
        outcome="Another bounded capability exists",
    )

    assert first.id == "SG-000001"
    assert second.id == "SG-000002"
    assert first.state == second.state == "DRAFT"
    assert first.parent_id is None
    assert first.children == first.dependencies == first.acceptance == first.change_surface == ()
    assert first.metadata == {}

    stored = json.loads(
        (tmp_path / ".specgrain" / "specs" / "SG-000001.json").read_text(encoding="utf-8")
    )
    assert stored == first.to_dict()


def test_create_draft_api_uses_lowest_unused_positive_id(tmp_path: Path) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    cap = tmp_path / ".specgrain" / "specs"
    one = SpecNode(id="SG-000001", title="One", outcome="One outcome")
    three = SpecNode(id="SG-000003", title="Three", outcome="Three outcome")
    write_json(cap / "SG-000001.json", one.to_dict())
    write_json(cap / "SG-000003.json", three.to_dict())

    node = create_draft_spec(tmp_path, title="Two", outcome="Fill deterministic gap")
    assert node.id == "SG-000002"


def test_create_draft_api_refuses_collision_without_overwrite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    first = create_draft_spec(tmp_path, title="First", outcome="Keep this content")
    path = tmp_path / ".specgrain" / "specs" / f"{first.id}.json"
    before = path.read_bytes()

    monkeypatch.setattr(store_module, "_next_draft_id", lambda specs: first.id)
    with pytest.raises(StoreExistsError, match="refusing overwrite"):
        create_draft_spec(tmp_path, title="Collision", outcome="Must not replace")
    assert path.read_bytes() == before


def test_create_draft_api_rejects_invalid_input_without_artifact(tmp_path: Path) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    with pytest.raises(SpecValidationError, match="title"):
        create_draft_spec(tmp_path, title="   ", outcome="Valid outcome")
    assert list((tmp_path / ".specgrain" / "specs").glob("*.json")) == []


def test_cli_draft_text_creates_draft_then_check_counts_it(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()

    assert main(
        [
            "draft",
            str(tmp_path),
            "--title",
            "Add health check",
            "--outcome",
            "Service exposes one bounded health endpoint",
            "--rationale",
            "Make the first native specification tangible.",
        ]
    ) == 0
    out = capsys.readouterr().out
    assert "SpecGrain draft: CREATED" in out
    assert "Spec: SG-000001" in out
    assert "State: DRAFT" in out
    assert "File: .specgrain/specs/SG-000001.json" in out
    assert "Revision: sha256:" in out
    assert "PASS" not in out

    assert main(["check", str(tmp_path)]) == 0
    check_out = capsys.readouterr().out
    assert "Specs: 1" in check_out
    assert "Roots: 1" in check_out
    assert "Grain-ready: 0" in check_out


def test_cli_draft_json_is_machine_readable_and_stable(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()
    assert main(
        [
            "draft",
            str(tmp_path),
            "--title",
            "First",
            "--outcome",
            "First outcome",
            "--json",
        ]
    ) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "file": ".specgrain/specs/SG-000001.json",
        "revision_digest": create_draft_spec.__module__ and payload["revision_digest"],
        "spec_id": "SG-000001",
        "state": "DRAFT",
    }
    assert payload["revision_digest"].startswith("sha256:")


def test_cli_draft_invalid_store_fails_without_artifact(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(
        ["draft", str(tmp_path), "--title", "First", "--outcome", "First outcome"]
    ) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "SpecGrain draft: FAIL" in captured.err
    assert not (tmp_path / ".specgrain").exists()


def test_cli_draft_json_validation_error_is_structured(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()
    assert main(
        [
            "draft",
            str(tmp_path),
            "--title",
            " ",
            "--outcome",
            "First outcome",
            "--json",
        ]
    ) == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.err)
    assert payload["valid"] is False
    assert "title must not be empty" in payload["error"]
    assert list((tmp_path / ".specgrain" / "specs").glob("*.json")) == []


def test_cli_report_mode_blocker_still_exits_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()
    node = blocked_spec()
    write_json(tmp_path / ".specgrain" / "specs" / f"{node.id}.json", node.to_dict())
    assert main(["check", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "Readiness-blocked: 1" in out
    assert "ACCEPTANCE_REQUIRED" in out


def test_cli_enforce_mode_blocker_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()
    write_json(
        tmp_path / ".specgrain" / "policies" / "default.json",
        {"policy_version": 1, "readiness_mode": "enforce"},
    )
    node = blocked_spec()
    write_json(tmp_path / ".specgrain" / "specs" / f"{node.id}.json", node.to_dict())
    assert main(["check", str(tmp_path), "--json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["valid"] is False
    assert payload["readiness_mode"] == "enforce"


def test_cli_missing_store_check_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["check", str(tmp_path)]) == 1
    out = capsys.readouterr().out
    assert "SpecGrain check: FAIL" in out
    assert "STORE_INVALID" in out


def test_argparse_usage_error_is_two() -> None:
    with pytest.raises(SystemExit) as caught:
        main([])
    assert caught.value.code == 2


def test_module_entrypoint_imports_same_main() -> None:
    import specgrain.__main__ as module_entry
    import specgrain.cli as cli

    assert module_entry.main is cli.main


def test_cli_init_unexpected_internal_error_fails_closed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(*args: object, **kwargs: object) -> object:
        raise RuntimeError("secret detail")

    monkeypatch.setattr(cli_module, "init_project", fail)
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "SpecGrain init: FAIL\n- internal error\n"
    assert "secret detail" not in captured.err


def test_cli_draft_unexpected_internal_error_fails_closed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(*args: object, **kwargs: object) -> object:
        raise RuntimeError("secret detail")

    monkeypatch.setattr(cli_module, "create_draft_spec", fail)
    assert main(
        ["draft", str(tmp_path), "--title", "First", "--outcome", "First outcome"]
    ) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "SpecGrain draft: FAIL\n- internal error\n"
    assert "secret detail" not in captured.err


def test_cli_check_unexpected_internal_error_fails_closed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(*args: object, **kwargs: object) -> object:
        raise RuntimeError("secret detail")

    monkeypatch.setattr(cli_module, "check_project", fail)
    assert main(["check", str(tmp_path), "--json"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "SpecGrain check: FAIL\n- internal error\n"
    assert "secret detail" not in captured.err
