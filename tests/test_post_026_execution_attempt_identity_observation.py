from __future__ import annotations

from dataclasses import fields

from specgrain.adapter import AgentRequest, parse_agent_result, render_agent_request
from specgrain.context import ContextBudgetPolicy, ContextSource, evaluate_context_budget
from specgrain.model import SpecNode
from specgrain.packet import ExecutionResult, build_work_packet


def _packet():
    node = SpecNode(
        id="SG-000027",
        title="Observe execution attempt identity",
        outcome="A bounded execution attempt can be distinguished from another attempt.",
        scope_in=["execution attempt identity"],
        scope_out=["provider invocation"],
        acceptance=["repeated attempts remain distinguishable"],
        dependencies=[],
        risk={"level": "low", "recovery": "discard observation fixture"},
        change_surface=["tests/test_post_026_execution_attempt_identity_observation.py"],
        evidence={"required": ["tests"]},
        method="observation",
        state="GRAIN",
    )
    source = ContextSource(
        source_id="repo",
        provenance="repo:canonical-main",
        selection_reason="bind one deterministic context source",
        revision="sha256:" + "a" * 64,
        size_bytes=1,
        token_cost=1,
    )
    report = evaluate_context_budget((source,), ContextBudgetPolicy(max_tokens=10))
    return build_work_packet(node, (source,), report)


def test_repeated_same_packet_requests_have_no_attempt_identity() -> None:
    packet = _packet()

    first = render_agent_request(packet)
    second = render_agent_request(packet)

    assert first.request_digest == second.request_digest
    assert first.to_dict() == second.to_dict()
    assert "attempt_id" not in {field.name for field in fields(AgentRequest)}


def test_repeated_same_executor_reports_collapse_to_one_content_identity() -> None:
    packet = _packet()
    payload = {
        "status": "failed",
        "summary": "Executor stopped before completion.",
        "changed_paths": ["src/example.py"],
        "reported_evidence": [],
        "error_code": "EXECUTOR_INTERRUPTED",
    }

    first = parse_agent_result(packet, payload)
    second = parse_agent_result(packet, payload)

    assert first.result_digest == second.result_digest
    assert first.to_dict() == second.to_dict()
    assert "attempt_id" not in {field.name for field in fields(ExecutionResult)}
    assert "request_digest" not in {field.name for field in fields(ExecutionResult)}
