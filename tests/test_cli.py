from __future__ import annotations

import json
from pathlib import Path

import pytest

from specgrain import SpecNode
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
