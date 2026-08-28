from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from specgrain.context import (
    ContextBudgetPolicy,
    ContextRequirement,
    ContextSource,
    evaluate_context_budget,
)
from specgrain.model import SpecNode
from specgrain.packet import (
    EXECUTION_RESULT_VERSION,
    WORK_PACKET_VERSION,
    ExecutionResult,
    ExecutionStatus,
    PacketContextSource,
    PacketValidationError,
    WorkPacket,
    build_work_packet,
)


def source(source_id: str, *, required: bool = True, priority: int = 0) -> ContextSource:
    return ContextSource(
        source_id=source_id,
        provenance=f"repo:{source_id}",
        selection_reason=f"needed {source_id}",
        revision="sha256:" + "a" * 64,
        size_bytes=10,
        token_cost=5,
        requirement=ContextRequirement.REQUIRED if required else ContextRequirement.OPTIONAL,
        priority=priority,
    )


def node(**overrides: object) -> SpecNode:
    values: dict[str, object] = {
        "id": "SG-000009",
        "title": "Portable packet",
        "outcome": "A portable packet exists.",
        "scope_in": ["packet"],
        "scope_out": ["execution"],
        "acceptance": ["packet digest is stable", "result is structured"],
        "dependencies": ["SG-000008"],
        "risk": {"level": "low", "recovery": "discard packet"},
        "change_surface": ["src/specgrain/packet.py"],
        "evidence": {"required": ["tests", "diff"]},
        "method": "quick",
        "state": "GRAIN",
    }
    values.update(overrides)
    return SpecNode(**values)


def report(*sources: ContextSource):
    return evaluate_context_budget(sources, ContextBudgetPolicy(max_tokens=100))


def test_packet_context_source_snapshots_context() -> None:
    original = source("repo")
    snap = PacketContextSource.from_context_source(original)
    assert snap.source_id == "repo"
    assert snap.revision == original.revision
    assert "requirement" not in snap.to_dict()
    assert "priority" not in snap.to_dict()


def test_packet_context_source_is_frozen() -> None:
    snap = PacketContextSource.from_context_source(source("repo"))
    with pytest.raises(FrozenInstanceError):
        snap.source_id = "other"  # type: ignore[misc]


@pytest.mark.parametrize("field", ["source_id", "provenance", "selection_reason", "revision"])
def test_packet_context_source_requires_text(field: str) -> None:
    values = {
        "source_id": "id",
        "provenance": "prov",
        "selection_reason": "why",
        "revision": "rev",
        "size_bytes": 1,
        "token_cost": 1,
    }
    values[field] = ""
    with pytest.raises(PacketValidationError, match=field):
        PacketContextSource(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("field", "value"),
    [("size_bytes", -1), ("token_cost", -1), ("size_bytes", True)],
)
def test_packet_context_source_rejects_invalid_costs(field: str, value: object) -> None:
    values: dict[str, object] = {
        "source_id": "id",
        "provenance": "prov",
        "selection_reason": "why",
        "revision": "rev",
        "size_bytes": 1,
        "token_cost": 1,
    }
    values[field] = value
    with pytest.raises(PacketValidationError, match=field):
        PacketContextSource(**values)  # type: ignore[arg-type]


def test_build_work_packet_binds_exact_spec_and_context_revisions() -> None:
    n = node()
    sources = (source("a"), source("b", required=False))
    context_report = report(*sources)
    packet = build_work_packet(
        n,
        sources,
        context_report,
        decisions=["Use JSON"],
        assumptions=["Executor honors scope"],
        minimality_evidence=["No existing packet contract"],
    )
    assert packet.packet_version == WORK_PACKET_VERSION
    assert packet.spec_id == n.id
    assert packet.spec_revision == n.revision_digest
    assert packet.context_plan_digest == context_report.plan_digest
    assert tuple(item.source_id for item in packet.context_sources) == context_report.selected_ids
    assert packet.required_evidence == ("diff", "tests")


def test_build_packet_is_permutation_invariant() -> None:
    sources = (source("b", required=False, priority=1), source("a"))
    context_report = report(*sources)
    first = build_work_packet(node(), sources, context_report)
    second = build_work_packet(node(), tuple(reversed(sources)), context_report)
    assert first.to_dict() == second.to_dict()
    assert first.packet_digest == second.packet_digest


def test_packet_digest_changes_with_spec_revision() -> None:
    sources = (source("a"),)
    context_report = report(*sources)
    first = build_work_packet(node(outcome="One"), sources, context_report)
    second = build_work_packet(node(outcome="Two"), sources, context_report)
    assert first.packet_digest != second.packet_digest


def test_packet_digest_changes_with_context_revision() -> None:
    n = node()
    first_source = source("a")
    second_source = ContextSource(
        source_id="a",
        provenance="repo:a",
        selection_reason="needed a",
        revision="sha256:" + "b" * 64,
        size_bytes=10,
        token_cost=5,
    )
    first = build_work_packet(n, (first_source,), report(first_source))
    second = build_work_packet(n, (second_source,), report(second_source))
    assert first.packet_digest != second.packet_digest


def test_packet_digest_changes_with_decision() -> None:
    sources = (source("a"),)
    context_report = report(*sources)
    first = build_work_packet(node(), sources, context_report, decisions=["A"])
    second = build_work_packet(node(), sources, context_report, decisions=["B"])
    assert first.packet_digest != second.packet_digest


def test_packet_json_is_canonical_and_contains_digest() -> None:
    sources = (source("a"),)
    packet = build_work_packet(node(), sources, report(*sources))
    text = packet.to_json()
    assert '"packet_digest":"' in text
    assert '": ' not in text
    assert '", ' not in text
    assert text == packet.to_json()


def test_packet_to_dict_is_detached() -> None:
    sources = (source("a"),)
    packet = build_work_packet(node(), sources, report(*sources))
    payload = packet.to_dict()
    payload["acceptance"].append("mutate")  # type: ignore[union-attr]
    assert "mutate" not in packet.acceptance


def test_packet_is_frozen() -> None:
    sources = (source("a"),)
    packet = build_work_packet(node(), sources, report(*sources))
    with pytest.raises(FrozenInstanceError):
        packet.outcome = "other"  # type: ignore[misc]


def test_builder_rejects_non_specnode() -> None:
    sources = (source("a"),)
    with pytest.raises(PacketValidationError, match="SpecNode"):
        build_work_packet(object(), sources, report(*sources))  # type: ignore[arg-type]


def test_builder_rejects_non_report() -> None:
    with pytest.raises(PacketValidationError, match="ContextBudgetReport"):
        build_work_packet(node(), (), object())  # type: ignore[arg-type]


def test_builder_rejects_failing_context_report() -> None:
    required = source("a")
    failing = evaluate_context_budget((required,), ContextBudgetPolicy(max_tokens=1))
    with pytest.raises(PacketValidationError, match="must fit"):
        build_work_packet(node(), (required,), failing)


def test_builder_rejects_missing_selected_source() -> None:
    sources = (source("a"), source("b"))
    context_report = report(*sources)
    with pytest.raises(PacketValidationError, match="missing selected"):
        build_work_packet(node(), (sources[0],), context_report)


def test_builder_rejects_unselected_source() -> None:
    required = source("a")
    optional = ContextSource(
        source_id="b",
        provenance="repo:b",
        selection_reason="optional",
        revision="sha256:" + "a" * 64,
        size_bytes=10,
        token_cost=100,
        requirement=ContextRequirement.OPTIONAL,
    )
    context_report = evaluate_context_budget(
        (required, optional), ContextBudgetPolicy(max_tokens=10)
    )
    assert context_report.selected_ids == ("a",)
    with pytest.raises(PacketValidationError, match="unselected"):
        build_work_packet(node(), (required, optional), context_report)


def test_builder_rejects_invalid_required_evidence() -> None:
    sources = (source("a"),)
    with pytest.raises(PacketValidationError, match="node.evidence.required"):
        build_work_packet(node(evidence={"required": "tests"}), sources, report(*sources))


def test_work_packet_rejects_duplicate_context_sources() -> None:
    snap = PacketContextSource.from_context_source(source("a"))
    with pytest.raises(PacketValidationError, match="duplicate context"):
        WorkPacket(
            spec_id="SG-000009",
            spec_revision="sha256:" + "a" * 64,
            outcome="x",
            acceptance=("a",),
            scope_in=("x",),
            scope_out=(),
            dependencies=(),
            authorized_change_surface=("x",),
            method="quick",
            risk={},
            required_evidence=("tests",),
            context_plan_digest="sha256:" + "b" * 64,
            context_sources=(snap, snap),
        )


@pytest.mark.parametrize("digest", ["", "sha256:abc", "SHA256:" + "a" * 64, "sha256:" + "A" * 64])
def test_work_packet_rejects_invalid_digests(digest: str) -> None:
    with pytest.raises(PacketValidationError):
        WorkPacket(
            spec_id="SG-000009",
            spec_revision=digest,
            outcome="x",
            acceptance=("a",),
            scope_in=("x",),
            scope_out=(),
            dependencies=(),
            authorized_change_surface=("x",),
            method="quick",
            risk={},
            required_evidence=("tests",),
            context_plan_digest="sha256:" + "b" * 64,
            context_sources=(),
        )


def test_execution_result_success_contract_and_digest() -> None:
    result = ExecutionResult(
        packet_digest="sha256:" + "a" * 64,
        status="succeeded",
        summary="Implemented bounded change",
        changed_paths=("b.py", "a.py"),
        reported_evidence=("tests",),
    )
    assert result.status is ExecutionStatus.SUCCEEDED
    assert result.result_version == EXECUTION_RESULT_VERSION
    assert result.changed_paths == ("a.py", "b.py")
    assert result.result_digest.startswith("sha256:")
    assert result.to_dict()["result_digest"] == result.result_digest


@pytest.mark.parametrize("status", ["failed", "blocked"])
def test_execution_result_failure_requires_error_code(status: str) -> None:
    with pytest.raises(PacketValidationError, match="require error_code"):
        ExecutionResult(
            packet_digest="sha256:" + "a" * 64,
            status=status,
            summary="No",
        )


def test_execution_result_success_rejects_error_code() -> None:
    with pytest.raises(PacketValidationError, match="must not carry"):
        ExecutionResult(
            packet_digest="sha256:" + "a" * 64,
            status="succeeded",
            summary="Done",
            error_code="ERR",
        )


def test_execution_result_failure_can_bind_error_code() -> None:
    result = ExecutionResult(
        packet_digest="sha256:" + "a" * 64,
        status="failed",
        summary="Tests failed",
        error_code="TEST_FAILURE",
    )
    assert result.error_code == "TEST_FAILURE"


@pytest.mark.parametrize("status", ["", "done", 1, None])
def test_execution_result_rejects_unknown_status(status: object) -> None:
    with pytest.raises(PacketValidationError, match="status"):
        ExecutionResult(
            packet_digest="sha256:" + "a" * 64,
            status=status,  # type: ignore[arg-type]
            summary="No",
            error_code="ERR",
        )


def test_execution_result_is_frozen() -> None:
    result = ExecutionResult(
        packet_digest="sha256:" + "a" * 64,
        status="succeeded",
        summary="Done",
    )
    with pytest.raises(FrozenInstanceError):
        result.summary = "other"  # type: ignore[misc]


def test_execution_result_digest_changes_with_changed_paths() -> None:
    first = ExecutionResult(
        packet_digest="sha256:" + "a" * 64,
        status="succeeded",
        summary="Done",
        changed_paths=("a.py",),
    )
    second = ExecutionResult(
        packet_digest="sha256:" + "a" * 64,
        status="succeeded",
        summary="Done",
        changed_paths=("b.py",),
    )
    assert first.result_digest != second.result_digest


def test_execution_result_is_only_self_report() -> None:
    result = ExecutionResult(
        packet_digest="sha256:" + "a" * 64,
        status="succeeded",
        summary="Claims success",
        reported_evidence=("pytest",),
    )
    payload = result.to_dict()
    assert "verified" not in payload
    assert "verification" not in payload


def test_packet_contains_no_provider_or_prompt_field() -> None:
    sources = (source("a"),)
    payload = build_work_packet(node(), sources, report(*sources)).to_dict()
    assert "provider" not in payload
    assert "model" not in payload
    assert "prompt" not in payload


def test_packet_round_trip_verifies_digest() -> None:
    sources = (source("a"),)
    packet = build_work_packet(node(), sources, report(*sources))
    assert WorkPacket.from_dict(packet.to_dict()) == packet


def test_packet_round_trip_rejects_digest_tampering() -> None:
    sources = (source("a"),)
    packet = build_work_packet(node(), sources, report(*sources))
    payload = packet.to_dict()
    payload["outcome"] = "tampered"
    with pytest.raises(PacketValidationError, match="packet_digest does not match"):
        WorkPacket.from_dict(payload)


def test_packet_round_trip_rejects_unknown_field() -> None:
    sources = (source("a"),)
    packet = build_work_packet(node(), sources, report(*sources))
    payload = packet.to_dict()
    payload["provider"] = "vendor"
    with pytest.raises(PacketValidationError, match="unknown fields"):
        WorkPacket.from_dict(payload)


def test_execution_result_round_trip_verifies_digest() -> None:
    result = ExecutionResult(
        packet_digest="sha256:" + "a" * 64,
        status="succeeded",
        summary="Done",
        changed_paths=("a.py",),
    )
    assert ExecutionResult.from_dict(result.to_dict()) == result


def test_execution_result_round_trip_rejects_tampering() -> None:
    result = ExecutionResult(
        packet_digest="sha256:" + "a" * 64,
        status="succeeded",
        summary="Done",
    )
    payload = result.to_dict()
    payload["summary"] = "tampered"
    with pytest.raises(PacketValidationError, match="result_digest does not match"):
        ExecutionResult.from_dict(payload)


def test_packet_allows_finite_float_in_spec_risk() -> None:
    sources = (source("a"),)
    packet = build_work_packet(
        node(risk={"level": "low", "recovery": "revert", "score": 0.5}),
        sources,
        report(*sources),
    )
    assert packet.to_dict()["risk"]["score"] == 0.5  # type: ignore[index]


def test_work_packet_rejects_noncanonical_dependency_id() -> None:
    with pytest.raises(PacketValidationError, match="canonical SpecGrain IDs"):
        WorkPacket(
            spec_id="SG-000009",
            spec_revision="sha256:" + "a" * 64,
            outcome="x",
            acceptance=("a",),
            scope_in=("x",),
            scope_out=(),
            dependencies=("bad",),
            authorized_change_surface=("x",),
            method="quick",
            risk={},
            required_evidence=("tests",),
            context_plan_digest="sha256:" + "b" * 64,
            context_sources=(),
        )


def test_execution_result_json_is_canonical() -> None:
    result = ExecutionResult(
        packet_digest="sha256:" + "a" * 64,
        status="succeeded",
        summary="Done with spaces",
    )
    text = result.to_json()
    assert '": ' not in text
    assert '", ' not in text
    assert text == result.to_json()
