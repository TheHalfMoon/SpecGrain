"""Portable deterministic execution-attempt identity contracts."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

EXECUTION_ATTEMPT_VERSION = 1


class ExecutionAttemptValidationError(ValueError):
    """Raised when execution-attempt content is malformed or inconsistent."""


class ExecutionAttemptStatus(StrEnum):
    """Portable attempt status independent from SpecNode lifecycle authority."""

    STARTED = "started"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED = "blocked"
    INTERRUPTED = "interrupted"


def _require_text(value: object, field_name: str) -> str:
    if not isinstance(value, str):
        raise ExecutionAttemptValidationError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ExecutionAttemptValidationError(f"{field_name} must be non-empty")
    return normalized


def _validate_digest(value: object, field_name: str) -> str:
    digest = _require_text(value, field_name)
    if len(digest) != 71 or not digest.startswith("sha256:"):
        raise ExecutionAttemptValidationError(
            f"{field_name} must be lowercase sha256:<64 hex>"
        )
    suffix = digest[7:]
    if any(character not in "0123456789abcdef" for character in suffix):
        raise ExecutionAttemptValidationError(
            f"{field_name} must be lowercase sha256:<64 hex>"
        )
    return digest


def _validate_attempt_id(value: object) -> str:
    attempt_id = _require_text(value, "attempt_id")
    if not attempt_id.startswith("EA-"):
        raise ExecutionAttemptValidationError(
            "attempt_id must use canonical EA-<lowercase UUID> form"
        )
    uuid_text = attempt_id[3:]
    try:
        parsed = UUID(uuid_text)
    except (AttributeError, ValueError) as exc:
        raise ExecutionAttemptValidationError(
            "attempt_id must use canonical EA-<lowercase UUID> form"
        ) from exc
    if parsed.int == 0 or str(parsed) != uuid_text:
        raise ExecutionAttemptValidationError(
            "attempt_id must use canonical EA-<lowercase UUID> form"
        )
    return attempt_id


def _digest(content: Mapping[str, object]) -> str:
    encoded = json.dumps(
        dict(content),
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


@dataclass(frozen=True, slots=True)
class ExecutionAttemptRecord:
    """Describe one execution occurrence without granting verification authority."""

    attempt_id: str
    packet_digest: str
    status: ExecutionAttemptStatus
    request_digest: str | None = None
    result_digest: str | None = None
    error_code: str | None = None
    attempt_version: int = EXECUTION_ATTEMPT_VERSION

    def __post_init__(self) -> None:
        if (
            self.attempt_version != EXECUTION_ATTEMPT_VERSION
            or isinstance(self.attempt_version, bool)
        ):
            raise ExecutionAttemptValidationError(
                f"attempt_version must equal integer {EXECUTION_ATTEMPT_VERSION}"
            )

        object.__setattr__(self, "attempt_id", _validate_attempt_id(self.attempt_id))
        object.__setattr__(
            self,
            "packet_digest",
            _validate_digest(self.packet_digest, "packet_digest"),
        )

        if self.request_digest is not None:
            object.__setattr__(
                self,
                "request_digest",
                _validate_digest(self.request_digest, "request_digest"),
            )
        if self.result_digest is not None:
            object.__setattr__(
                self,
                "result_digest",
                _validate_digest(self.result_digest, "result_digest"),
            )
        if self.error_code is not None:
            object.__setattr__(
                self,
                "error_code",
                _require_text(self.error_code, "error_code"),
            )

        try:
            status = ExecutionAttemptStatus(self.status)
        except (TypeError, ValueError) as exc:
            allowed = ", ".join(status.value for status in ExecutionAttemptStatus)
            raise ExecutionAttemptValidationError(
                f"status must be one of: {allowed}"
            ) from exc
        object.__setattr__(self, "status", status)

        if status is ExecutionAttemptStatus.STARTED:
            if self.result_digest is not None or self.error_code is not None:
                raise ExecutionAttemptValidationError(
                    "started attempts must not carry result_digest or error_code"
                )
        elif status is ExecutionAttemptStatus.SUCCEEDED:
            if self.result_digest is None:
                raise ExecutionAttemptValidationError(
                    "succeeded attempts require result_digest"
                )
            if self.error_code is not None:
                raise ExecutionAttemptValidationError(
                    "succeeded attempts must not carry error_code"
                )
        elif self.error_code is None:
            raise ExecutionAttemptValidationError(
                "failed, blocked, or interrupted attempts require error_code"
            )

    def content_dict(self) -> dict[str, object]:
        """Return normalized attempt content excluding the derived attempt digest."""

        result: dict[str, object] = {
            "attempt_id": self.attempt_id,
            "attempt_version": self.attempt_version,
            "packet_digest": self.packet_digest,
            "status": self.status.value,
        }
        if self.request_digest is not None:
            result["request_digest"] = self.request_digest
        if self.result_digest is not None:
            result["result_digest"] = self.result_digest
        if self.error_code is not None:
            result["error_code"] = self.error_code
        return result

    @property
    def attempt_digest(self) -> str:
        """Return the stable digest over normalized attempt content."""

        return _digest(self.content_dict())

    def to_dict(self) -> dict[str, object]:
        """Return a detached portable representation including its digest."""

        result = self.content_dict()
        result["attempt_digest"] = self.attempt_digest
        return result

    def to_json(self) -> str:
        """Return canonical compact JSON for portable interchange."""

        return json.dumps(
            self.to_dict(),
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ExecutionAttemptRecord:
        """Parse a strict attempt record and verify its declared digest."""

        if not isinstance(data, Mapping):
            raise ExecutionAttemptValidationError(
                "ExecutionAttemptRecord input must be an object"
            )
        payload = dict(data)
        declared_digest = payload.pop("attempt_digest", None)
        allowed = {
            "attempt_id",
            "attempt_version",
            "packet_digest",
            "request_digest",
            "result_digest",
            "status",
            "error_code",
        }
        required = {
            "attempt_id",
            "attempt_version",
            "packet_digest",
            "status",
        }
        unknown = sorted(set(payload) - allowed)
        missing = sorted(required - set(payload))
        if unknown:
            raise ExecutionAttemptValidationError(
                "ExecutionAttemptRecord input has unknown fields: "
                + ", ".join(unknown)
            )
        if missing:
            raise ExecutionAttemptValidationError(
                "ExecutionAttemptRecord input is missing fields: "
                + ", ".join(missing)
            )
        if declared_digest is None:
            raise ExecutionAttemptValidationError(
                "ExecutionAttemptRecord input is missing attempt_digest"
            )

        record = cls(**payload)  # type: ignore[arg-type]
        digest = _validate_digest(declared_digest, "attempt_digest")
        if digest != record.attempt_digest:
            raise ExecutionAttemptValidationError(
                "attempt_digest does not match normalized attempt content"
            )
        return record
