from __future__ import annotations

import json
from pathlib import Path

import pytest

from specgrain import load_project
from specgrain.cli import main


def _shape_args(root: Path, spec_id: str, *, as_json: bool = False) -> list[str]:
    args = [
        "shape",
        spec_id,
        str(root),
        "--scope-in",
        "Implement bounded validation",
        "--scope-out",
        "No provider integration",
        "--acceptance",
        "Focused tests pass",
        "--risk-level",
        "low",
        "--recovery",
        "Revert the bounded file change.",
        "--context-budget",
        "2000",
        "--context-estimate",
        "500",
        "--change-surface",
        "src/example.py",
        "--change-surface",
        "tests/test_example.py",
        "--evidence",
        "focused-tests",
        "--minimality-choice",
        "native",
        "--minimality-rationale",
        "The repository has no existing equivalent primitive.",
        "--safety-status",
        "none-identified",
    ]
    if as_json:
        args.append("--json")
    return args


def _draft(root: Path, capsys: pytest.CaptureFixture[str]) -> str:
    assert main(["init", str(root), "--project-id", "demo"]) == 0
    capsys.readouterr()
    assert main(
        [
            "draft",
            str(root),
            "--title",
            "Validate config",
            "--outcome",
            "Reject invalid config",
        ]
    ) == 0
    output = capsys.readouterr().out
    assert "Spec: SG-000001" in output
    return "SG-000001"


def test_cli_closes_draft_to_grain_preparation_loop(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _draft(tmp_path, capsys)

    assert main(_shape_args(tmp_path, spec_id)) == 0
    shape = capsys.readouterr().out
    assert "SpecGrain shape: UPDATED" in shape
    assert "Source state: DRAFT" in shape
    assert "State: SHAPED" in shape
    assert "Revision: sha256:" in shape

    assert main(["refine", spec_id, str(tmp_path)]) == 0
    refine = capsys.readouterr().out
    assert "SpecGrain refine: UPDATED" in refine
    assert "Source state: SHAPED" in refine
    assert "State: REFINING" in refine

    assert main(["check", str(tmp_path)]) == 0
    check = capsys.readouterr().out
    assert "REFINING leaves: 1" in check
    assert "Grain-ready: 1" in check
    assert "Readiness-blocked: 0" in check

    assert main(["grain", spec_id, str(tmp_path)]) == 0
    grain = capsys.readouterr().out
    assert "SpecGrain grain: UPDATED" in grain
    assert "Source state: REFINING" in grain
    assert "State: GRAIN" in grain

    assert main(["next", str(tmp_path)]) == 0
    next_output = capsys.readouterr().out
    assert "Eligible: 1" in next_output
    assert f"- {spec_id}" in next_output


def test_cli_json_payloads_preserve_semantic_revision_across_state_only_edges(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _draft(tmp_path, capsys)

    assert main(_shape_args(tmp_path, spec_id, as_json=True)) == 0
    shaped = json.loads(capsys.readouterr().out)
    assert shaped["spec_id"] == spec_id
    assert shaped["source_state"] == "DRAFT"
    assert shaped["state"] == "SHAPED"
    revision = shaped["revision_digest"]
    assert revision.startswith("sha256:")

    assert main(["refine", spec_id, str(tmp_path), "--json"]) == 0
    refining = json.loads(capsys.readouterr().out)
    assert refining["source_state"] == "SHAPED"
    assert refining["state"] == "REFINING"
    assert refining["revision_digest"] == revision

    assert main(["grain", spec_id, str(tmp_path), "--json"]) == 0
    grain = json.loads(capsys.readouterr().out)
    assert grain["source_state"] == "REFINING"
    assert grain["state"] == "GRAIN"
    assert grain["revision_digest"] == revision


def test_cli_grain_blocked_json_is_exact_and_non_mutating(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _draft(tmp_path, capsys)
    assert main(_shape_args(tmp_path, spec_id)) == 0
    capsys.readouterr()
    assert main(["refine", spec_id, str(tmp_path)]) == 0
    capsys.readouterr()

    path = tmp_path / ".specgrain" / "specs" / f"{spec_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["acceptance"] = []
    path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    before = path.read_bytes()

    assert main(["grain", spec_id, str(tmp_path), "--json"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    payload = json.loads(captured.err)
    assert payload["valid"] is False
    assert payload["spec_id"] == spec_id
    assert payload["source_state"] == "REFINING"
    assert payload["state"] == "REFINING"
    assert payload["issues"] == [
        {
            "code": "ACCEPTANCE_REQUIRED",
            "field": "acceptance",
            "message": "at least one acceptance condition is required",
        }
    ]
    assert path.read_bytes() == before
    assert load_project(tmp_path).specs[0].state == "REFINING"


def test_cli_wrong_source_state_returns_stable_failure(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _draft(tmp_path, capsys)

    assert main(["refine", spec_id, str(tmp_path), "--json"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    payload = json.loads(captured.err)
    assert payload["valid"] is False
    assert "requires source state SHAPED" in payload["error"]


def test_cli_shape_rejects_invalid_context_bounds(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _draft(tmp_path, capsys)

    budget_args = _shape_args(tmp_path, spec_id, as_json=True)
    budget_args[budget_args.index("--context-budget") + 1] = "0"
    assert main(budget_args) == 1
    budget_payload = json.loads(capsys.readouterr().err)
    assert "context_budget must be a positive integer" in budget_payload["error"]

    estimate_args = _shape_args(tmp_path, spec_id, as_json=True)
    estimate_args[estimate_args.index("--context-estimate") + 1] = "-1"
    assert main(estimate_args) == 1
    estimate_payload = json.loads(capsys.readouterr().err)
    assert "context_estimate must be a non-negative integer" in estimate_payload["error"]
    assert load_project(tmp_path).specs[0].state == "DRAFT"


def test_cli_shape_requires_explicit_safety_requirements(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec_id = _draft(tmp_path, capsys)
    args = _shape_args(tmp_path, spec_id, as_json=True)
    status_index = args.index("none-identified")
    args[status_index] = "requirements-defined"

    assert main(args) == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.err)
    assert payload["valid"] is False
    assert "safety_requirements are required" in payload["error"]
