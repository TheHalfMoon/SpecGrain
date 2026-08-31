from __future__ import annotations

import importlib
import json
import sys
import types
from pathlib import Path

import pytest


@pytest.fixture()
def cli_module(monkeypatch: pytest.MonkeyPatch):
    src = Path(__file__).parents[1] / "src" / "specgrain"
    package = types.ModuleType("specgrain")
    package.__path__ = [str(src)]
    monkeypatch.setitem(sys.modules, "specgrain", package)

    project = types.ModuleType("specgrain.project")
    project.NextResult = object
    project.check_project = lambda path: None
    project.next_project = lambda path: None
    monkeypatch.setitem(sys.modules, "specgrain.project", project)

    store = types.ModuleType("specgrain.store")
    store.AuthoringRecoveryResult = object
    store.ChildDraftResult = object
    store.ProjectCheckResult = object
    store.StoreError = type("StoreError", (Exception,), {})
    store.create_child_draft_spec = lambda path, parent_id, title, outcome, rationale="": None
    store.create_draft_spec = lambda path, title, outcome, rationale="": None
    store.init_project = lambda path, project_id=None: None
    store.load_project = lambda path: None
    store.recover_authoring_transaction = lambda path: None
    monkeypatch.setitem(sys.modules, "specgrain.store", store)

    for name in ("specgrain.repository", "specgrain.cli"):
        sys.modules.pop(name, None)
    return importlib.import_module("specgrain.cli")


def test_scan_cli_text_success(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    cli_module: types.ModuleType,
) -> None:
    (tmp_path / "a.py").write_text("x=1\n", encoding="utf-8")
    assert cli_module.main(["scan", str(tmp_path)]) == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    assert "SpecGrain scan: PASS" in captured.out
    assert "Files: 1" in captured.out
    assert "language Python: 1" in captured.out


def test_scan_cli_json_is_deterministic_and_environment_free(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    cli_module: types.ModuleType,
) -> None:
    (tmp_path / "a.py").write_text("x=1\n", encoding="utf-8")
    assert cli_module.main(["scan", str(tmp_path), "--json"]) == 0
    first = capsys.readouterr().out
    assert cli_module.main(["scan", str(tmp_path), "--json"]) == 0
    second = capsys.readouterr().out
    assert first == second
    payload = json.loads(first)
    assert payload["repository_name"] == tmp_path.name
    assert str(tmp_path) not in first
    assert len(payload["content_digest"]) == 64


def test_scan_cli_failure_is_stable_and_relative(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    cli_module: types.ModuleType,
) -> None:
    missing = tmp_path / "missing"
    assert cli_module.main(["scan", str(missing), "--json"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    payload = json.loads(captured.err)
    assert payload["valid"] is False
    assert payload["error"]["code"] == "ROOT_INVALID"
    assert str(missing) not in captured.err


def test_scan_cli_unexpected_error_fails_closed(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    cli_module: types.ModuleType,
) -> None:
    def fail(path: str) -> object:
        raise RuntimeError("secret detail")

    monkeypatch.setattr(cli_module, "scan_repository", fail)
    assert cli_module.main(["scan", str(tmp_path), "--json"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "SpecGrain scan: FAIL\n- internal error\n"
    assert "secret detail" not in captured.err