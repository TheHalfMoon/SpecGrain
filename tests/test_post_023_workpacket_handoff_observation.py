from __future__ import annotations

import json
from pathlib import Path

import pytest

from specgrain import (
    ContextBudgetPolicy,
    ContextSource,
    build_work_packet,
    load_project,
    require_context_budget,
    require_grain_readiness,
)
from specgrain.cli import main


def _shape_args(root: Path, spec_id: str) -> list[str]:
    return [
        "shape",
        spec_id,
        str(root),
        "--scope-in",
        "Export one portable execution handoff.",
        "--scope-out",
        "Do not invoke an executor.",
        "--acceptance",
        "The handoff is digest-bound and portable.",
        "--risk-level",
        "low",
        "--recovery",
        "Delete the isolated fixture workspace.",
        "--context-budget",
        "128",
        "--context-estimate",
        "16",
        "--change-surface",
        "src/example.py",
        "--evidence",
        "handoff-json",
        "--minimality-choice",
        "native",
        "--minimality-rationale",
        "Reuse the existing WorkPacket contract without executor scope.",
        "--safety-status",
        "none-identified",
    ]


def test_native_grain_handoff_requires_python_api_glue(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["init", str(tmp_path), "--project-id", "handoff-observation"]) == 0
    capsys.readouterr()

    assert main(
        [
            "draft",
            str(tmp_path),
            "--title",
            "Portable handoff fixture",
            "--outcome",
            "A ready Grain can be handed to an external executor without product mutation.",
        ]
    ) == 0
    capsys.readouterr()
    spec_id = "SG-000001"

    assert main(_shape_args(tmp_path, spec_id)) == 0
    capsys.readouterr()
    assert main(["refine", spec_id, str(tmp_path)]) == 0
    capsys.readouterr()
    assert main(["grain", spec_id, str(tmp_path)]) == 0
    capsys.readouterr()
    assert main(["next", str(tmp_path), "--json"]) == 0
    next_payload = json.loads(capsys.readouterr().out)
    assert next_payload["eligible_ids"] == [spec_id]

    with pytest.raises(SystemExit) as exc_info:
        main(["packet", spec_id, str(tmp_path), "--json"])
    assert exc_info.value.code == 2
    parser_failure = capsys.readouterr()
    assert parser_failure.out == ""
    assert "invalid choice" in parser_failure.err
    assert "packet" in parser_failure.err

    project = load_project(tmp_path)
    node = project.specs[0]
    readiness = require_grain_readiness(node, project.specs)
    assert readiness.is_ready

    outcome_bytes = node.outcome.encode("utf-8")
    source = ContextSource(
        source_id="grain-outcome",
        provenance=f"spec:{node.id}",
        selection_reason="Carry the exact bounded outcome into the external handoff.",
        revision=node.revision_digest,
        size_bytes=len(outcome_bytes),
        token_cost=8,
    )
    context_report = require_context_budget(
        (source,),
        ContextBudgetPolicy(max_tokens=128, max_bytes=4096, max_sources=1),
    )
    packet = build_work_packet(
        node,
        (source,),
        context_report,
        minimality_evidence=(
            "The fixture had to leave the native CLI and assemble public Python API objects.",
        ),
    )

    portable = json.loads(packet.to_json())
    assert portable["spec_id"] == spec_id
    assert portable["spec_revision"] == node.revision_digest
    assert portable["packet_digest"].startswith("sha256:")
    assert portable["context_sources"][0]["source_id"] == "grain-outcome"
