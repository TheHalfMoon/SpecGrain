from __future__ import annotations

import json
from dataclasses import FrozenInstanceError, fields

import pytest

from specgrain import (
    EXECUTION_ATTEMPT_VERSION,
    EXECUTION_RESULT_VERSION,
    WORK_PACKET_VERSION,
    ExecutionAttemptRecord,
    ExecutionAttemptStatus,
    ExecutionAttemptValidationError,
    ExecutionResult,
)
from specgrain.adapter import ADAPTER_PROTOCOL_VERSION, AgentRequest

ATTEMPT_A = "EA-550e8400-e29b-41d4-a716-446655440000"
ATTEMPT_B = "EA-123e4567-e89b-12d3-a456-426614174000"
PACKET_DIGEST = "sha256:" + "a" * 64
REQUEST_DIGEST = "sha256:" + "b" * 64
RESULT_DIGEST = "sha256:" + "c" * 64


def _succeeded(attempt_id: str = ATTEMPT_A) -> ExecutionAttemptRecord:
    return ExecutionAttemptRecord(
        attempt_id=attempt_id,
        packet_digest=PACKET_DIGEST,
        request_digest=REQUEST_DIGEST,
        status=ExecutionAttemptStatus.SUCCEEDED,
        result_digest=RESULT_DIGEST,
    )


def test_distinct_occurrences_bind_identical_content_identities() -> None:
    first = _succeeded(ATTEMPT_A)
    second = _succeeded(ATTEMPT_B)

    assert first.packet_digest == second.packet_digest == PACKET_DIGEST
    assert first.request_digest == second.request_digest == REQUEST_DIGEST
    assert first.result_digest == second.result_digest == RESULT_DIGEST
    assert first.attempt_id != second.attempt_id
    assert first.attempt_digest != second.attempt_digest


def test_identical_attempt_content_has_stable_digest_and_round_trip() -> None:
    first = _succeeded()
    second = _succeeded()

    assert first.attempt_digest == second.attempt_digest
    assert first.to_dict() == second.to_dict()
    assert first.to_json() == json.dumps(
        first.to_dict(),
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    )
    assert ExecutionAttemptRecord.from_dict(first.to_dict()) == first


def test_progressive_binding_uses_same_attempt_id_without_mutation() -> None:
    started = ExecutionAttemptRecord(
        attempt_id=ATTEMPT_A,
        packet_digest=PACKET_DIGEST,
        status=ExecutionAttemptStatus.STARTED,
    )
    completed = _succeeded(ATTEMPT_A)

    assert started.attempt_id == completed.attempt_id
    assert started.request_digest is None
    assert started.result_digest is None
    assert completed.request_digest == REQUEST_DIGEST
    assert completed.result_digest == RESULT_DIGEST
    assert started.attempt_digest != completed.attempt_digest
    with pytest.raises(FrozenInstanceError):
        started.status = ExecutionAttemptStatus.SUCCEEDED  # type: ignore[misc]


@pytest.mark.parametrize(
    "attempt_id",
    [
        "",
        "550e8400-e29b-41d4-a716-446655440000",
        "EA-550E8400-E29B-41D4-A716-446655440000",
        "EA-{550e8400-e29b-41d4-a716-446655440000}",
        "EA-550e8400e29b41d4a716446655440000",
        "EA-00000000-0000-0000-0000-000000000000",
        "EA-not-a-uuid",
    ],
)
def test_attempt_id_must_be_canonical_non_nil_prefixed_uuid(attempt_id: str) -> None:
    with pytest.raises(ExecutionAttemptValidationError):
        ExecutionAttemptRecord(
            attempt_id=attempt_id,
            packet_digest=PACKET_DIGEST,
            status=ExecutionAttemptStatus.STARTED,
        )


@pytest.mark.parametrize(
    "field_name,bad_digest",
    [
        ("packet_digest", "a" * 64),
        ("packet_digest", "sha256:" + "A" * 64),
        ("request_digest", "sha256:short"),
        ("result_digest", "sha256:" + "g" * 64),
    ],
)
def test_bound_digests_fail_closed(field_name: str, bad_digest: str) -> None:
    kwargs: dict[str, object] = {
        "attempt_id": ATTEMPT_A,
        "packet_digest": PACKET_DIGEST,
        "status": ExecutionAttemptStatus.SUCCEEDED,
        "request_digest": REQUEST_DIGEST,
        "result_digest": RESULT_DIGEST,
    }
    kwargs[field_name] = bad_digest
    with pytest.raises(ExecutionAttemptValidationError):
        ExecutionAttemptRecord(**kwargs)  # type: ignore[arg-type]


def test_status_invariants_are_exact() -> None:
    with pytest.raises(ExecutionAttemptValidationError, match="started"):
        ExecutionAttemptRecord(
            attempt_id=ATTEMPT_A,
            packet_digest=PACKET_DIGEST,
            status=ExecutionAttemptStatus.STARTED,
            result_digest=RESULT_DIGEST,
        )
    with pytest.raises(ExecutionAttemptValidationError, match="require result_digest"):
        ExecutionAttemptRecord(
            attempt_id=ATTEMPT_A,
            packet_digest=PACKET_DIGEST,
            status=ExecutionAttemptStatus.SUCCEEDED,
        )
    with pytest.raises(ExecutionAttemptValidationError, match="must not carry error_code"):
        ExecutionAttemptRecord(
            attempt_id=ATTEMPT_A,
            packet_digest=PACKET_DIGEST,
            status=ExecutionAttemptStatus.SUCCEEDED,
            result_digest=RESULT_DIGEST,
            error_code="UNEXPECTED",
        )

    for status in (
        ExecutionAttemptStatus.FAILED,
        ExecutionAttemptStatus.BLOCKED,
        ExecutionAttemptStatus.INTERRUPTED,
    ):
        with pytest.raises(ExecutionAttemptValidationError, match="require error_code"):
            ExecutionAttemptRecord(
                attempt_id=ATTEMPT_A,
                packet_digest=PACKET_DIGEST,
                status=status,
            )
        record = ExecutionAttemptRecord(
            attempt_id=ATTEMPT_A,
            packet_digest=PACKET_DIGEST,
            status=status,
            error_code="EXECUTION_STOPPED",
        )
        assert record.error_code == "EXECUTION_STOPPED"
        assert record.result_digest is None


def test_strict_deserialization_rejects_unknown_missing_and_tampered_fields() -> None:
    payload = _succeeded().to_dict()

    unknown = dict(payload)
    unknown["provider"] = "example"
    with pytest.raises(ExecutionAttemptValidationError, match="unknown fields"):
        ExecutionAttemptRecord.from_dict(unknown)

    missing = dict(payload)
    missing.pop("packet_digest")
    with pytest.raises(ExecutionAttemptValidationError, match="missing fields"):
        ExecutionAttemptRecord.from_dict(missing)

    no_digest = dict(payload)
    no_digest.pop("attempt_digest")
    with pytest.raises(ExecutionAttemptValidationError, match="missing attempt_digest"):
        ExecutionAttemptRecord.from_dict(no_digest)

    tampered = dict(payload)
    tampered["attempt_id"] = ATTEMPT_B
    with pytest.raises(ExecutionAttemptValidationError, match="does not match"):
        ExecutionAttemptRecord.from_dict(tampered)


def test_attempt_record_has_no_verification_or_lifecycle_authority() -> None:
    field_names = {field.name for field in fields(ExecutionAttemptRecord)}

    assert "verified" not in field_names
    assert "verification" not in field_names
    assert "spec_state" not in field_names
    assert "lifecycle" not in field_names


def test_existing_v1_public_contracts_remain_unchanged() -> None:
    assert EXECUTION_ATTEMPT_VERSION == 1
    assert WORK_PACKET_VERSION == 1
    assert EXECUTION_RESULT_VERSION == 1
    assert ADAPTER_PROTOCOL_VERSION == 1
    assert {field.name for field in fields(AgentRequest)} == {
        "adapter",
        "packet_digest",
        "media_type",
        "payload",
        "protocol_version",
    }
    assert {field.name for field in fields(ExecutionResult)} == {
        "packet_digest",
        "status",
        "summary",
        "changed_paths",
        "reported_evidence",
        "error_code",
        "result_version",
    }
