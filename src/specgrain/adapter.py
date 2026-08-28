"""Deterministic generic agent request and result adapters."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from .packet import ExecutionResult, PacketValidationError, WorkPacket

ADAPTER_PROTOCOL_VERSION = 1
_JSON_MEDIA_TYPE = "application/vnd.specgrain.work-packet+json"
_MARKDOWN_MEDIA_TYPE = "text/markdown"


class AgentAdapterError(ValueError):
    """Raised when an adapter request or external result violates the v1 contract."""


class AgentAdapterKind(StrEnum):
    """Supported generic deterministic request representations."""

    GENERIC_JSON = "generic-json"
    GENERIC_MARKDOWN = "generic-markdown"


def _require_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AgentAdapterError(f"{field_name} must be non-empty text")
    return value


def _require_digest(value: object, field_name: str) -> str:
    text = _require_text(value, field_name)
    if not text.startswith("sha256:") or len(text) != 71:
        raise AgentAdapterError(f"{field_name} must be a sha256: digest")
    if any(character not in "0123456789abcdef" for character in text[7:]):
        raise AgentAdapterError(f"{field_name} must use lowercase hexadecimal")
    return text


def _canonical_json(value: Mapping[str, object]) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    )


def _digest(value: Mapping[str, object]) -> str:
    encoded = _canonical_json(value).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _strict_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AgentAdapterError(f"external result contains duplicate field {key!r}")
        result[key] = value
    return result


def _reject_non_finite(value: str) -> None:
    raise AgentAdapterError(f"external result contains non-finite JSON value {value!r}")


@dataclass(frozen=True, slots=True)
class AgentRequest:
    """Immutable deterministic request envelope around one exact WorkPacket."""

    adapter: AgentAdapterKind | str
    packet_digest: str
    media_type: str
    payload: str
    protocol_version: int = ADAPTER_PROTOCOL_VERSION

    def __post_init__(self) -> None:
        if (
            isinstance(self.protocol_version, bool)
            or self.protocol_version != ADAPTER_PROTOCOL_VERSION
        ):
            raise AgentAdapterError(
                f"protocol_version must equal integer {ADAPTER_PROTOCOL_VERSION}"
            )
        try:
            adapter = AgentAdapterKind(self.adapter)
        except (TypeError, ValueError) as exc:
            raise AgentAdapterError("adapter is not a supported generic adapter kind") from exc
        object.__setattr__(self, "adapter", adapter)
        object.__setattr__(
            self,
            "packet_digest",
            _require_digest(self.packet_digest, "packet_digest"),
        )
        object.__setattr__(self, "media_type", _require_text(self.media_type, "media_type"))
        object.__setattr__(self, "payload", _require_text(self.payload, "payload"))

    def content_dict(self) -> dict[str, object]:
        """Return normalized request content excluding the derived request digest."""

        return {
            "adapter": self.adapter.value,
            "media_type": self.media_type,
            "packet_digest": self.packet_digest,
            "payload": self.payload,
            "protocol_version": self.protocol_version,
        }

    @property
    def request_digest(self) -> str:
        """Return the stable digest over normalized request content."""

        return _digest(self.content_dict())

    def to_dict(self) -> dict[str, object]:
        """Return a detached portable request representation including its digest."""

        result = self.content_dict()
        result["request_digest"] = self.request_digest
        return result

    def to_json(self) -> str:
        """Return canonical compact JSON for storage or transport."""

        return _canonical_json(self.to_dict())

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> AgentRequest:
        """Parse a strict request representation and verify the declared digest."""

        if not isinstance(data, Mapping):
            raise AgentAdapterError("AgentRequest input must be an object")
        payload = dict(data)
        declared = payload.pop("request_digest", None)
        allowed = {
            "adapter",
            "media_type",
            "packet_digest",
            "payload",
            "protocol_version",
        }
        unknown = sorted(set(payload) - allowed)
        missing = sorted(allowed - set(payload))
        if unknown:
            raise AgentAdapterError(
                f"AgentRequest input has unknown fields: {', '.join(unknown)}"
            )
        if missing:
            raise AgentAdapterError(
                f"AgentRequest input is missing fields: {', '.join(missing)}"
            )
        request = cls(**payload)  # type: ignore[arg-type]
        digest = _require_digest(declared, "request_digest")
        if digest != request.request_digest:
            raise AgentAdapterError(
                "request_digest does not match normalized request content"
            )
        return request


def _markdown_payload(packet: WorkPacket) -> str:
    packet_json = packet.to_json()
    return (
        "# SpecGrain Agent Request\n\n"
        f"Packet digest: `{packet.packet_digest}`\n\n"
        "Execute only the bounded WorkPacket below. Return an executor self-report; "
        "do not claim verification.\n\n"
        "```json\n"
        f"{packet_json}\n"
        "```\n"
    )


def render_agent_request(
    packet: WorkPacket,
    adapter: AgentAdapterKind | str = AgentAdapterKind.GENERIC_JSON,
) -> AgentRequest:
    """Render one canonical WorkPacket through a deterministic generic adapter."""

    if not isinstance(packet, WorkPacket):
        raise AgentAdapterError("packet must be a WorkPacket")
    try:
        kind = AgentAdapterKind(adapter)
    except (TypeError, ValueError) as exc:
        raise AgentAdapterError("adapter is not a supported generic adapter kind") from exc

    if kind is AgentAdapterKind.GENERIC_JSON:
        media_type = _JSON_MEDIA_TYPE
        payload = packet.to_json()
    else:
        media_type = _MARKDOWN_MEDIA_TYPE
        payload = _markdown_payload(packet)

    return AgentRequest(
        adapter=kind,
        packet_digest=packet.packet_digest,
        media_type=media_type,
        payload=payload,
    )


def _external_mapping(payload: Mapping[str, object] | str) -> dict[str, object]:
    if isinstance(payload, str):
        try:
            decoded = json.loads(
                payload,
                object_pairs_hook=_strict_object_pairs,
                parse_constant=_reject_non_finite,
            )
        except json.JSONDecodeError as exc:
            raise AgentAdapterError("external result must be valid JSON") from exc
        if not isinstance(decoded, dict):
            raise AgentAdapterError("external result JSON must decode to an object")
        return decoded
    if not isinstance(payload, Mapping):
        raise AgentAdapterError("external result must be an object or JSON object text")
    result: dict[str, object] = {}
    for key, value in payload.items():
        if not isinstance(key, str):
            raise AgentAdapterError("external result object keys must be strings")
        result[key] = value
    return result


def parse_agent_result(
    packet: WorkPacket,
    payload: Mapping[str, object] | str,
) -> ExecutionResult:
    """Normalize an external executor self-report into the canonical result contract."""

    if not isinstance(packet, WorkPacket):
        raise AgentAdapterError("packet must be a WorkPacket")
    data = _external_mapping(payload)
    allowed = {
        "changed_paths",
        "error_code",
        "reported_evidence",
        "status",
        "summary",
    }
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise AgentAdapterError(
            "external result contains unauthorized fields: " + ", ".join(unknown)
        )
    missing = sorted({"status", "summary"} - set(data))
    if missing:
        raise AgentAdapterError(
            f"external result is missing fields: {', '.join(missing)}"
        )

    changed_paths = data.get("changed_paths", ())
    reported_evidence = data.get("reported_evidence", ())
    if isinstance(changed_paths, str | bytes | bytearray) or not isinstance(
        changed_paths, Sequence
    ):
        raise AgentAdapterError("changed_paths must be a sequence")
    if isinstance(reported_evidence, str | bytes | bytearray) or not isinstance(
        reported_evidence, Sequence
    ):
        raise AgentAdapterError("reported_evidence must be a sequence")

    try:
        return ExecutionResult(
            packet_digest=packet.packet_digest,
            status=data["status"],  # type: ignore[arg-type]
            summary=data["summary"],  # type: ignore[arg-type]
            changed_paths=tuple(changed_paths),
            reported_evidence=tuple(reported_evidence),
            error_code=data.get("error_code"),  # type: ignore[arg-type]
        )
    except (PacketValidationError, TypeError, ValueError) as exc:
        raise AgentAdapterError(f"external result violates ExecutionResult: {exc}") from exc


__all__ = [
    "ADAPTER_PROTOCOL_VERSION",
    "AgentAdapterError",
    "AgentAdapterKind",
    "AgentRequest",
    "parse_agent_result",
    "render_agent_request",
]
