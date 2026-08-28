from __future__ import annotations

import json
from pathlib import Path

import pytest

import specgrain.cli as cli_module
from specgrain import SpecNode, check_project, init_project, next_project
from specgrain.cli import main


def metadata() -> dict[str, object]:
    return {
        "readiness": {
            "version": 1,
            "unresolved_decisions": [],
            "minimality": {"choice": "new-code", "rationale": "bounded"},
            "safety": {"status": "none-identified", "requirements": []},
        }
    }


def node(
    num: int,
    *,
    state: str = "GRAIN",
    dependencies: tuple[int, ...] = (),
    acceptance: tuple[str, ...] = ("done",),
) -> SpecNode:
    return SpecNode(
        id=f"SG-{num:06d}",
        title=f"Node {num}",
        outcome=f"Outcome {num}",
        scope_in=("bounded",),
        acceptance=acceptance,
        risk={"level": "low", "recovery": "revert"},
        context={"budget_tokens": 1000, "estimated_tokens": 500},
        change_surface=("src/x.py",),
        evidence={"required": ("tests",)},
        metadata=metadata(),
        dependencies=tuple(f"SG-{value:06d}" for value in dependencies),
        state=state,
    )


def write_node(root: Path, item: SpecNode) -> None:
    path = root / ".specgrain" / "specs" / f"{item.id}.json"
    path.write_text(json.dumps(item.to_dict(), sort_keys=True) + "\n", encoding="utf-8")


def test_check_rejects_dependency_invalid_before_readiness(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    bad = node(1, state="REFINING", dependencies=(99,), acceptance=())
    write_node(tmp_path, bad)
    result = check_project(tmp_path)
    assert not result.valid
    assert result.issues[0].code == "MISSING_DEPENDENCY"
    assert result.readiness_blocked == ()


def test_next_reports_eligible_waves_and_is_read_only(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    verified = node(1, state="VERIFIED")
    first = node(2, dependencies=(1,))
    parallel = node(3, dependencies=(1,))
    second = node(4, dependencies=(2, 3))
    for item in (second, parallel, verified, first):
        write_node(tmp_path, item)
    before = {p.name: p.read_bytes() for p in (tmp_path / ".specgrain" / "specs").iterdir()}
    result = next_project(tmp_path)
    after = {p.name: p.read_bytes() for p in (tmp_path / ".specgrain" / "specs").iterdir()}
    assert result.valid
    assert result.eligible_ids == (first.id, parallel.id)
    assert result.waves == ((first.id, parallel.id), (second.id,))
    assert after == before


def test_next_exposes_transitive_blocker(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    failed = node(1, state="FAILED")
    middle = node(2, state="READY", dependencies=(1,))
    candidate = node(3, dependencies=(2,))
    for item in (failed, middle, candidate):
        write_node(tmp_path, item)
    report = next_project(tmp_path).dependency_reports[0]
    assert report.waiting_on == (middle.id,)
    assert report.blocked_by == (failed.id,)


def test_cli_next_json_and_text(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()
    verified = node(1, state="VERIFIED")
    first = node(2, dependencies=(1,))
    second = node(3, dependencies=(2,))
    for item in (verified, first, second):
        write_node(tmp_path, item)
    assert main(["next", str(tmp_path), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["eligible"] == [first.id]
    assert payload["waves"] == [[first.id], [second.id]]
    assert main(["next", str(tmp_path)]) == 0
    assert "Projected waves: 2" in capsys.readouterr().out


def test_cli_next_invalid_graph_and_internal_error_fail_closed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "demo"]) == 0
    capsys.readouterr()
    write_node(tmp_path, node(1, dependencies=(99,)))
    assert main(["next", str(tmp_path), "--json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["issues"][0]["code"] == "MISSING_DEPENDENCY"

    def fail(*args: object, **kwargs: object) -> object:
        raise RuntimeError("secret")

    monkeypatch.setattr(cli_module, "next_project", fail)
    assert main(["next", str(tmp_path), "--json"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "SpecGrain next: FAIL\n- internal error\n"
    assert "secret" not in captured.err
