from __future__ import annotations

import json
from pathlib import Path

from test_verification import verified_report

from specgrain import init_project
from specgrain.cli import main
from specgrain.verification import append_verification_report


def test_prove_empty_chain_fails_without_mutation(tmp_path: Path, capsys) -> None:
    init_project(tmp_path, project_id="demo")
    before = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*"))
    assert main(["prove", "SG-000010", str(tmp_path)]) == 1
    captured = capsys.readouterr()
    assert "SpecGrain prove: FAIL" in captured.out
    assert captured.err == ""
    after = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*"))
    assert before == after


def test_prove_verified_text_and_json(tmp_path: Path, capsys) -> None:
    init_project(tmp_path, project_id="demo")
    record = append_verification_report(tmp_path, verified_report())
    assert main(["prove", "SG-000010", str(tmp_path)]) == 0
    text = capsys.readouterr().out
    assert "SpecGrain prove: PASS" in text
    assert f"Latest: {record.record_digest}" in text
    assert "Verified: true" in text

    assert main(["prove", "SG-000010", str(tmp_path), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["verified"] is True
    assert payload["latest_record_digest"] == record.record_digest


def test_prove_json_is_deterministic(tmp_path: Path, capsys) -> None:
    init_project(tmp_path, project_id="demo")
    append_verification_report(tmp_path, verified_report())
    assert main(["prove", "SG-000010", str(tmp_path), "--json"]) == 0
    first = capsys.readouterr().out
    assert main(["prove", "SG-000010", str(tmp_path), "--json"]) == 0
    second = capsys.readouterr().out
    assert first == second


def test_prove_corrupt_chain_fails_closed(tmp_path: Path, capsys) -> None:
    init_project(tmp_path, project_id="demo")
    evidence = tmp_path / ".specgrain" / "evidence" / "SG-000010"
    evidence.mkdir(parents=True)
    (evidence / "bad.txt").write_text("bad", encoding="utf-8")
    assert main(["prove", "SG-000010", str(tmp_path), "--json"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    payload = json.loads(captured.err)
    assert payload["valid"] is False
    assert "unexpected evidence entry" in payload["error"]
