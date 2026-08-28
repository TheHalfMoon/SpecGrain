from __future__ import annotations

import json

import pytest

from specgrain.adapter import (
    ADAPTER_PROTOCOL_VERSION,
    AgentAdapterError,
    AgentAdapterKind,
    AgentRequest,
    parse_agent_result,
    render_agent_request,
)
from specgrain.packet import ExecutionResult, ExecutionStatus, WorkPacket

DIGEST_A = "sha256:" + "a" * 64
DIGEST_B = "sha256:" + "b" * 64


def packet() -> WorkPacket:
    return WorkPacket(
        spec_id="SG-000014",
        spec_revision=DIGEST_A,
        outcome="Expose the portable packet through a thin agent adapter.",
        acceptance=("Adapter output is deterministic.",),
        scope_in=("generic adapter boundary",),
        scope_out=("agent execution",),
        dependencies=("SG-000009", "SG-000010"),
        authorized_change_surface=("src/specgrain/adapter.py",),
        method="quick",
        risk={"level": "low", "recovery": "remove the adapter"},
        required_evidence=("pytest",),
        context_plan_digest=DIGEST_B,
        context_sources=(),
    )


def test_json_request_is_canonical_packet_json_and_deterministic() -> None:
    work = packet()
    first = render_agent_request(work)
    second = render_agent_request(work, "generic-json")
    assert first == second
    assert first.adapter is AgentAdapterKind.GENERIC_JSON
    assert first.packet_digest == work.packet_digest
    assert first.payload == work.to_json()
    assert first.media_type == "application/vnd.specgrain.work-packet+json"
    assert first.request_digest == second.request_digest


def test_markdown_request_binds_same_packet_without_verification_authority() -> None:
    work = packet()
    request = render_agent_request(work, AgentAdapterKind.GENERIC_MARKDOWN)
    assert request.packet_digest == work.packet_digest
    assert request.media_type == "text/markdown"
    assert work.packet_digest in request.payload
    assert work.to_json() in request.payload
    assert "do not claim verification" in request.payload


def test_request_round_trip_verifies_digest() -> None:
    request = render_agent_request(packet(), "generic-markdown")
    parsed = AgentRequest.from_dict(request.to_dict())
    assert parsed == request
    assert parsed.to_json() == request.to_json()
    assert json.loads(parsed.to_json())["protocol_version"] == ADAPTER_PROTOCOL_VERSION


def test_request_round_trip_rejects_tampering_and_unknown_fields() -> None:
    request = render_agent_request(packet())
    tampered = request.to_dict()
    tampered["payload"] = "{}"
    with pytest.raises(AgentAdapterError, match="request_digest"):
        AgentRequest.from_dict(tampered)
    unknown = request.to_dict()
    unknown["session_id"] = "external-state"
    with pytest.raises(AgentAdapterError, match="unknown fields"):
        AgentRequest.from_dict(unknown)


def test_render_rejects_non_packet_and_unknown_adapter() -> None:
    with pytest.raises(AgentAdapterError, match="WorkPacket"):
        render_agent_request(object())  # type: ignore[arg-type]
    with pytest.raises(AgentAdapterError, match="supported"):
        render_agent_request(packet(), "vendor-magic")


def test_success_result_is_bound_by_adapter_to_packet() -> None:
    work = packet()
    result = parse_agent_result(
        work,
        {
            "status": "succeeded",
            "summary": "Implemented the bounded change.",
            "changed_paths": ["src/specgrain/adapter.py"],
            "reported_evidence": ["pytest"],
        },
    )
    assert isinstance(result, ExecutionResult)
    assert result.status is ExecutionStatus.SUCCEEDED
    assert result.packet_digest == work.packet_digest
    assert result.changed_paths == ("src/specgrain/adapter.py",)
    assert result.reported_evidence == ("pytest",)


def test_failed_result_requires_error_code_through_canonical_contract() -> None:
    with pytest.raises(AgentAdapterError, match="error_code"):
        parse_agent_result(
            packet(),
            {"status": "failed", "summary": "Tests failed."},
        )
    result = parse_agent_result(
        packet(),
        {"status": "failed", "summary": "Tests failed.", "error_code": "TEST_FAILURE"},
    )
    assert result.status is ExecutionStatus.FAILED
    assert result.error_code == "TEST_FAILURE"


def test_external_result_cannot_supply_packet_or_verification_authority() -> None:
    work = packet()
    for field in ("packet_digest", "result_digest", "verified", "evidence_record"):
        with pytest.raises(AgentAdapterError, match="unauthorized fields"):
            parse_agent_result(
                work,
                {
                    "status": "succeeded",
                    "summary": "Done.",
                    field: "forged",
                },
            )


def test_external_json_is_strict_and_deterministic() -> None:
    work = packet()
    text = json.dumps(
        {
            "status": "succeeded",
            "summary": "Done.",
            "changed_paths": ["b.py", "a.py"],
            "reported_evidence": ["z", "a"],
        }
    )
    result = parse_agent_result(work, text)
    assert result.changed_paths == ("a.py", "b.py")
    assert result.reported_evidence == ("a", "z")


def test_external_json_rejects_duplicate_fields() -> None:
    with pytest.raises(AgentAdapterError, match="duplicate field"):
        parse_agent_result(
            packet(),
            '{"status":"succeeded","status":"failed","summary":"Done."}',
        )


def test_external_json_rejects_non_finite_values() -> None:
    with pytest.raises(AgentAdapterError, match="non-finite"):
        parse_agent_result(
            packet(),
            '{"status":"succeeded","summary":"Done.","changed_paths":[NaN]}',
        )


def test_external_result_rejects_non_object_json_and_bad_sequences() -> None:
    with pytest.raises(AgentAdapterError, match="decode to an object"):
        parse_agent_result(packet(), "[]")
    with pytest.raises(AgentAdapterError, match="changed_paths must be a sequence"):
        parse_agent_result(
            packet(),
            {"status": "succeeded", "summary": "Done.", "changed_paths": "a.py"},
        )
    with pytest.raises(AgentAdapterError, match="reported_evidence must be a sequence"):
        parse_agent_result(
            packet(),
            {"status": "succeeded", "summary": "Done.", "reported_evidence": "pytest"},
        )


def test_external_result_rejects_missing_and_unknown_fields() -> None:
    with pytest.raises(AgentAdapterError, match="missing fields"):
        parse_agent_result(packet(), {"status": "succeeded"})
    with pytest.raises(AgentAdapterError, match="unauthorized fields"):
        parse_agent_result(
            packet(),
            {"status": "succeeded", "summary": "Done.", "provider": "example"},
        )
