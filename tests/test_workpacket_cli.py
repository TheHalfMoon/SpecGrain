from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from specgrain import (
    ContextBudgetPolicy,
    ContextSource,
    WorkPacket,
    build_work_packet,
    load_project,
    require_context_budget,
)
from specgrain.cli import main

_CONTEXT_LIMIT = 1_048_576


def _clear(capsys: pytest.CaptureFixture[str]) -> None:
    capsys.readouterr()


def _init(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["init", str(root), "--project-id", "packet-cli-test"]) == 0
    _clear(capsys)


def _draft(
    root: Path,
    capsys: pytest.CaptureFixture[str],
    *,
    title: str,
    outcome: str,
) -> str:
    assert main(
        [
            "draft",
            str(root),
            "--title",
            title,
            "--outcome",
            outcome,
            "--json",
        ]
    ) == 0
    payload = json.loads(capsys.readouterr().out)
    return payload["spec_id"]


def _promote_to_grain(
    root: Path,
    capsys: pytest.CaptureFixture[str],
    spec_id: str,
    *,
    dependencies: tuple[str, ...] = (),
    budget: int = 128,
) -> None:
    args = [
        "shape",
        spec_id,
        str(root),
        "--scope-in",
        f"Export {spec_id} as one bounded packet.",
        "--scope-out",
        "Do not execute the packet.",
        "--acceptance",
        "The packet is deterministic and digest-bound.",
        "--risk-level",
        "low",
        "--recovery",
        "Delete the isolated test workspace.",
        "--context-budget",
        str(budget),
        "--context-estimate",
        "16",
        "--change-surface",
        "src/example.py",
        "--evidence",
        "packet-json",
        "--minimality-choice",
        "reuse-existing",
        "--minimality-rationale",
        "Reuse the existing WorkPacket and context contracts.",
        "--safety-status",
        "none-identified",
    ]
    for dependency in dependencies:
        args.extend(["--dependency", dependency])
    assert main(args) == 0
    _clear(capsys)
    assert main(["refine", spec_id, str(root)]) == 0
    _clear(capsys)
    assert main(["grain", spec_id, str(root)]) == 0
    _clear(capsys)


def _record(
    source_id: str = "source-a",
    *,
    token_cost: int = 8,
    requirement: str = "required",
    priority: int = 0,
) -> dict[str, object]:
    return {
        "source_id": source_id,
        "provenance": f"fixture:{source_id}",
        "selection_reason": "Bound one explicit context source to the packet.",
        "revision": f"fixture-revision:{source_id}",
        "size_bytes": 32,
        "token_cost": token_cost,
        "requirement": requirement,
        "priority": priority,
    }


def _write_sources(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text(json.dumps(records), encoding="utf-8")


def _store_snapshot(root: Path) -> dict[str, bytes]:
    store = root / ".specgrain"
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(store.rglob("*"))
        if path.is_file()
    }


def _packet_args(root: Path, spec_id: str, source_file: Path) -> list[str]:
    return [
        "packet",
        spec_id,
        str(root),
        "--context-sources",
        str(source_file),
        "--json",
    ]


def _eligible_grain(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    *,
    budget: int = 128,
) -> str:
    _init(tmp_path, capsys)
    spec_id = _draft(
        tmp_path,
        capsys,
        title="Packet export",
        outcome="One eligible Grain exports one portable WorkPacket.",
    )
    _promote_to_grain(tmp_path, capsys, spec_id, budget=budget)
    return spec_id


def test_packet_json_matches_existing_api_and_is_non_mutating(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _eligible_grain(tmp_path, capsys)
    source_file = tmp_path / "context.json"
    record = _record()
    _write_sources(source_file, [record])
    before = _store_snapshot(tmp_path)

    assert main(_packet_args(tmp_path, spec_id, source_file)) == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    cli_json = captured.out.rstrip("\n")
    parsed = json.loads(cli_json)
    packet = WorkPacket.from_dict(parsed)
    assert packet.packet_digest == parsed["packet_digest"]
    assert _store_snapshot(tmp_path) == before

    project = load_project(tmp_path)
    node = next(node for node in project.specs if node.id == spec_id)
    sources = (ContextSource(**record),)
    report = require_context_budget(
        sources,
        ContextBudgetPolicy(max_tokens=node.context["budget_tokens"]),
    )
    expected = build_work_packet(node, sources, report)
    assert cli_json == expected.to_json()

    assert main(_packet_args(tmp_path, spec_id, source_file)) == 0
    assert capsys.readouterr().out == cli_json + "\n"
    assert _store_snapshot(tmp_path) == before


def test_packet_is_deterministic_for_reordered_context_input(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _eligible_grain(tmp_path, capsys)
    first = _record("source-b", priority=1)
    second = _record("source-a", priority=0)
    source_file = tmp_path / "context.json"
    _write_sources(source_file, [first, second])

    assert main(_packet_args(tmp_path, spec_id, source_file)) == 0
    output_one = capsys.readouterr().out
    _write_sources(source_file, [second, first])
    assert main(_packet_args(tmp_path, spec_id, source_file)) == 0
    output_two = capsys.readouterr().out

    assert output_one == output_two
    payload = json.loads(output_one)
    assert [item["source_id"] for item in payload["context_sources"]] == [
        "source-a",
        "source-b",
    ]


def test_packet_text_output_is_stable_summary(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _eligible_grain(tmp_path, capsys)
    source_file = tmp_path / "context.json"
    _write_sources(source_file, [_record()])

    assert main(
        [
            "packet",
            spec_id,
            str(tmp_path),
            "--context-sources",
            str(source_file),
        ]
    ) == 0
    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    assert captured.err == ""
    assert lines[0] == "SpecGrain packet: EXPORTED"
    assert lines[1] == f"Spec: {spec_id}"
    assert lines[2].startswith("Revision: sha256:")
    assert lines[3].startswith("Context plan: sha256:")
    assert lines[4].startswith("Packet: sha256:")


def test_packet_fails_closed_for_wrong_state_and_missing_target(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _init(tmp_path, capsys)
    spec_id = _draft(
        tmp_path,
        capsys,
        title="Still draft",
        outcome="Remain outside the packet boundary.",
    )
    source_file = tmp_path / "context.json"
    _write_sources(source_file, [_record()])
    before = _store_snapshot(tmp_path)

    assert main(_packet_args(tmp_path, spec_id, source_file)) == 1
    error = json.loads(capsys.readouterr().err)
    assert error["valid"] is False
    assert "must be in GRAIN state" in error["error"]
    assert _store_snapshot(tmp_path) == before

    assert main(_packet_args(tmp_path, "SG-999999", source_file)) == 1
    error = json.loads(capsys.readouterr().err)
    assert "was not found" in error["error"]
    assert _store_snapshot(tmp_path) == before


def test_packet_rejects_noncanonical_spec_id(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _init(tmp_path, capsys)
    source_file = tmp_path / "context.json"
    _write_sources(source_file, [_record()])
    before = _store_snapshot(tmp_path)

    assert main(_packet_args(tmp_path, "not-a-spec", source_file)) == 1
    error = json.loads(capsys.readouterr().err)
    assert error == {
        "error": "spec_id must be a canonical SpecGrain ID",
        "valid": False,
    }
    assert _store_snapshot(tmp_path) == before


def test_packet_rejects_dependency_ineligible_grain(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _init(tmp_path, capsys)
    dependency = _draft(
        tmp_path,
        capsys,
        title="Dependency",
        outcome="Remain an unfinished dependency Grain.",
    )
    _promote_to_grain(tmp_path, capsys, dependency)
    target = _draft(
        tmp_path,
        capsys,
        title="Dependent",
        outcome="Wait until the dependency is independently complete.",
    )
    _promote_to_grain(tmp_path, capsys, target, dependencies=(dependency,))
    source_file = tmp_path / "context.json"
    _write_sources(source_file, [_record()])
    before = _store_snapshot(tmp_path)

    assert main(_packet_args(tmp_path, target, source_file)) == 1
    error = json.loads(capsys.readouterr().err)
    assert error["error"] == f"spec {target} is not dependency-eligible"
    assert _store_snapshot(tmp_path) == before


def test_packet_rejects_invalid_dependency_graph(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _init(tmp_path, capsys)
    target = _draft(
        tmp_path,
        capsys,
        title="Broken dependency graph",
        outcome="Fail closed when the dependency graph is invalid.",
    )
    _promote_to_grain(tmp_path, capsys, target, dependencies=("SG-999999",))
    source_file = tmp_path / "context.json"
    _write_sources(source_file, [_record()])
    before = _store_snapshot(tmp_path)

    assert main(_packet_args(tmp_path, target, source_file)) == 1
    error = json.loads(capsys.readouterr().err)
    assert "project dependency state is invalid" in error["error"]
    assert _store_snapshot(tmp_path) == before


def test_packet_rejects_required_context_over_grain_budget(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _eligible_grain(tmp_path, capsys, budget=32)
    source_file = tmp_path / "context.json"
    _write_sources(source_file, [_record(token_cost=33)])
    before = _store_snapshot(tmp_path)

    assert main(_packet_args(tmp_path, spec_id, source_file)) == 1
    error = json.loads(capsys.readouterr().err)
    assert "required context uses 33 tokens; policy allows 32" in error["error"]
    assert _store_snapshot(tmp_path) == before


def test_packet_omits_optional_context_using_existing_budget_semantics(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _eligible_grain(tmp_path, capsys, budget=12)
    source_file = tmp_path / "context.json"
    required = _record("required", token_cost=8, requirement="required")
    optional = _record("optional", token_cost=8, requirement="optional", priority=1)
    _write_sources(source_file, [optional, required])

    assert main(_packet_args(tmp_path, spec_id, source_file)) == 0
    payload = json.loads(capsys.readouterr().out)
    assert [item["source_id"] for item in payload["context_sources"]] == ["required"]


def test_packet_rejects_malformed_or_noncanonical_context_records(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _eligible_grain(tmp_path, capsys)
    source_file = tmp_path / "context.json"
    before = _store_snapshot(tmp_path)
    base = _record()

    missing = dict(base)
    del missing["priority"]
    unknown = dict(base)
    unknown["extra"] = True
    invalid = dict(base)
    invalid["source_id"] = ""

    cases = [
        ("{", "malformed JSON"),
        (json.dumps({"source_id": "not-an-array"}), "top-level value must be an array"),
        ("[1]", "context_sources[0] must be an object"),
        (json.dumps([missing]), "is missing fields: priority"),
        (json.dumps([unknown]), "has unknown fields: extra"),
        (json.dumps([invalid]), "source_id must be a non-empty string"),
        (
            "[{\"source_id\":\"a\",\"source_id\":\"b\","
            "\"provenance\":\"p\",\"selection_reason\":\"r\","
            "\"revision\":\"v\",\"size_bytes\":1,\"token_cost\":1,"
            "\"requirement\":\"required\",\"priority\":0}]",
            "duplicate object key 'source_id'",
        ),
        (
            "[{\"source_id\":\"a\",\"provenance\":\"p\","
            "\"selection_reason\":\"r\",\"revision\":\"v\","
            "\"size_bytes\":1,\"token_cost\":NaN,"
            "\"requirement\":\"required\",\"priority\":0}]",
            "non-finite numeric token 'NaN'",
        ),
    ]

    for raw, message in cases:
        source_file.write_text(raw, encoding="utf-8")
        assert main(_packet_args(tmp_path, spec_id, source_file)) == 1
        error = json.loads(capsys.readouterr().err)
        assert message in error["error"]
        assert _store_snapshot(tmp_path) == before


def test_packet_rejects_duplicate_source_ids(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _eligible_grain(tmp_path, capsys)
    source_file = tmp_path / "context.json"
    _write_sources(source_file, [_record("same"), _record("same")])
    before = _store_snapshot(tmp_path)

    assert main(_packet_args(tmp_path, spec_id, source_file)) == 1
    error = json.loads(capsys.readouterr().err)
    assert "duplicate source_id values: same" in error["error"]
    assert _store_snapshot(tmp_path) == before


def test_packet_rejects_non_file_oversized_and_invalid_utf8_input(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _eligible_grain(tmp_path, capsys)
    before = _store_snapshot(tmp_path)

    directory = tmp_path / "context-dir"
    directory.mkdir()
    assert main(_packet_args(tmp_path, spec_id, directory)) == 1
    error = json.loads(capsys.readouterr().err)
    assert "must be a regular file" in error["error"]

    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * (_CONTEXT_LIMIT + 1))
    assert main(_packet_args(tmp_path, spec_id, oversized)) == 1
    error = json.loads(capsys.readouterr().err)
    assert f"exceeds {_CONTEXT_LIMIT}-byte limit" in error["error"]

    invalid_utf8 = tmp_path / "invalid-utf8.json"
    invalid_utf8.write_bytes(b"[\xff]")
    assert main(_packet_args(tmp_path, spec_id, invalid_utf8)) == 1
    error = json.loads(capsys.readouterr().err)
    assert "not valid UTF-8" in error["error"]
    assert _store_snapshot(tmp_path) == before


def test_packet_rejects_symlink_context_input_when_supported(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _eligible_grain(tmp_path, capsys)
    target = tmp_path / "real-context.json"
    _write_sources(target, [_record()])
    link = tmp_path / "context-link.json"
    try:
        os.symlink(target, link)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"symlink creation unavailable: {exc}")
    before = _store_snapshot(tmp_path)

    assert main(_packet_args(tmp_path, spec_id, link)) == 1
    error = json.loads(capsys.readouterr().err)
    assert "must not be a symlink" in error["error"]
    assert _store_snapshot(tmp_path) == before


def test_packet_help_is_available_without_project_state(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["packet", "--help"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "--context-sources" in captured.out
    assert "portable WorkPacket" in captured.out
    assert captured.err == ""
