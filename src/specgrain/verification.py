"""Independent deterministic verification and append-oriented evidence records."""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path, PurePosixPath

from .model import SpecNode, is_spec_id
from .packet import ExecutionResult, ExecutionStatus, WorkPacket

VERIFICATION_VERSION = 1
EVIDENCE_RECORD_VERSION = 1
MAX_EVIDENCE_RECORD_BYTES = 1_048_576
MAX_EVIDENCE_RECORDS = 10_000
_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class VerificationError(ValueError):
    """Raised when verification inputs or evidence storage violate the contract."""


class VerificationIssueCode(StrEnum):
    """Stable independent-verification blocker codes."""

    ACCEPTANCE_FAILED = "ACCEPTANCE_FAILED"
    ACCEPTANCE_MISSING = "ACCEPTANCE_MISSING"
    EVIDENCE_FAILED = "EVIDENCE_FAILED"
    EVIDENCE_MISSING = "EVIDENCE_MISSING"
    EXECUTION_NOT_SUCCEEDED = "EXECUTION_NOT_SUCCEEDED"
    EXECUTOR_SCOPE_MISMATCH = "EXECUTOR_SCOPE_MISMATCH"
    INDEPENDENT_CHECK_MISSING = "INDEPENDENT_CHECK_MISSING"
    RESULT_PACKET_MISMATCH = "RESULT_PACKET_MISMATCH"
    SPEC_REVISION_MISMATCH = "SPEC_REVISION_MISMATCH"
    UNSCOPED_CHANGE = "UNSCOPED_CHANGE"


@dataclass(frozen=True, slots=True, order=True)
class CheckEvidence:
    """One independent check result with a stable evidence reference."""

    check_id: str
    passed: bool
    evidence_ref: str
    detail: str = ""

    def __post_init__(self) -> None:
        for name in ("check_id", "evidence_ref"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise VerificationError(f"{name} must be a non-empty string")
        if not isinstance(self.passed, bool):
            raise VerificationError("passed must be a bool")
        if not isinstance(self.detail, str):
            raise VerificationError("detail must be a string")

    def to_dict(self) -> dict[str, object]:
        """Return a detached JSON-compatible representation."""

        return {
            "check_id": self.check_id,
            "detail": self.detail,
            "evidence_ref": self.evidence_ref,
            "passed": self.passed,
        }


@dataclass(frozen=True, slots=True, order=True)
class VerificationIssue:
    """One deterministic verification blocker."""

    code: VerificationIssueCode
    subject: str
    message: str

    def __post_init__(self) -> None:
        if not isinstance(self.code, VerificationIssueCode):
            raise VerificationError("code must be a VerificationIssueCode")
        for name in ("subject", "message"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise VerificationError(f"{name} must be a non-empty string")

    def to_dict(self) -> dict[str, str]:
        """Return a detached JSON-compatible representation."""

        return {
            "code": self.code.value,
            "message": self.message,
            "subject": self.subject,
        }


@dataclass(frozen=True, slots=True)
class VerificationReport:
    """Independent verdict bound to exact spec, packet, result, and implementation revisions."""

    spec_id: str
    spec_revision: str
    packet_digest: str
    result_digest: str
    implementation_revision: str
    observed_changed_paths: tuple[str, ...]
    acceptance_checks: tuple[CheckEvidence, ...]
    evidence_checks: tuple[CheckEvidence, ...]
    issues: tuple[VerificationIssue, ...]
    verification_version: int = VERIFICATION_VERSION

    def __post_init__(self) -> None:
        if (
            isinstance(self.verification_version, bool)
            or self.verification_version != VERIFICATION_VERSION
        ):
            raise VerificationError(
                f"verification_version must equal integer {VERIFICATION_VERSION}"
            )
        if not is_spec_id(self.spec_id):
            raise VerificationError("spec_id must be a canonical SpecGrain ID")
        for name in ("spec_revision", "packet_digest", "result_digest"):
            _require_digest(getattr(self, name), name)
        if (
            not isinstance(self.implementation_revision, str)
            or not self.implementation_revision.strip()
        ):
            raise VerificationError("implementation_revision must be a non-empty string")
        object.__setattr__(
            self,
            "observed_changed_paths",
            _normalize_paths(self.observed_changed_paths, "observed_changed_paths"),
        )
        object.__setattr__(
            self,
            "acceptance_checks",
            _normalize_checks(self.acceptance_checks, "acceptance_checks"),
        )
        object.__setattr__(
            self,
            "evidence_checks",
            _normalize_checks(self.evidence_checks, "evidence_checks"),
        )
        issues = tuple(self.issues)
        if any(not isinstance(issue, VerificationIssue) for issue in issues):
            raise VerificationError("issues must contain VerificationIssue records")
        object.__setattr__(
            self,
            "issues",
            tuple(
                sorted(
                    issues,
                    key=lambda issue: (
                        issue.code.value,
                        issue.subject,
                        issue.message,
                    ),
                )
            ),
        )

    @property
    def verified(self) -> bool:
        """Return whether every independent verification gate passed."""

        return not self.issues

    def to_dict(self) -> dict[str, object]:
        """Return the deterministic report representation."""

        return {
            "acceptance_checks": [check.to_dict() for check in self.acceptance_checks],
            "evidence_checks": [check.to_dict() for check in self.evidence_checks],
            "implementation_revision": self.implementation_revision,
            "issues": [issue.to_dict() for issue in self.issues],
            "observed_changed_paths": list(self.observed_changed_paths),
            "packet_digest": self.packet_digest,
            "result_digest": self.result_digest,
            "spec_id": self.spec_id,
            "spec_revision": self.spec_revision,
            "verification_version": self.verification_version,
            "verified": self.verified,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> VerificationReport:
        """Parse a strict serialized report and re-derive the verified field."""

        return _report_from_dict(data)


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    """Immutable hash-chained wrapper around one exact VerificationReport."""

    report: VerificationReport
    previous_record_digest: str | None = None
    record_version: int = EVIDENCE_RECORD_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.report, VerificationReport):
            raise VerificationError("report must be a VerificationReport")
        if isinstance(self.record_version, bool) or self.record_version != EVIDENCE_RECORD_VERSION:
            raise VerificationError(
                f"record_version must equal integer {EVIDENCE_RECORD_VERSION}"
            )
        if self.previous_record_digest is not None:
            _require_digest(self.previous_record_digest, "previous_record_digest")

    def content_dict(self) -> dict[str, object]:
        """Return normalized record content excluding its derived digest."""

        return {
            "previous_record_digest": self.previous_record_digest,
            "record_version": self.record_version,
            "report": self.report.to_dict(),
        }

    @property
    def record_digest(self) -> str:
        """Return the stable digest over normalized evidence content."""

        return _digest(self.content_dict())

    def to_dict(self) -> dict[str, object]:
        """Return a detached representation including the derived record digest."""

        result = self.content_dict()
        result["record_digest"] = self.record_digest
        return result

    def to_json(self) -> str:
        """Return canonical compact JSON for transport or comparison."""

        return json.dumps(
            self.to_dict(),
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> EvidenceRecord:
        """Parse a strict evidence record and reject digest tampering."""

        if not isinstance(data, Mapping):
            raise VerificationError("EvidenceRecord input must be an object")
        payload = dict(data)
        declared_digest = payload.pop("record_digest", None)
        required = {"previous_record_digest", "record_version", "report"}
        unknown = sorted(set(payload) - required)
        missing = sorted(required - set(payload))
        if unknown:
            raise VerificationError(
                f"EvidenceRecord input has unknown fields: {', '.join(unknown)}"
            )
        if missing:
            raise VerificationError(
                f"EvidenceRecord input is missing fields: {', '.join(missing)}"
            )
        report_data = payload["report"]
        if not isinstance(report_data, Mapping):
            raise VerificationError("report must be an object")
        record = cls(
            report=VerificationReport.from_dict(report_data),
            previous_record_digest=payload["previous_record_digest"],
            record_version=payload["record_version"],
        )
        digest = _require_digest(declared_digest, "record_digest")
        if digest != record.record_digest:
            raise VerificationError("record_digest does not match normalized evidence content")
        return record


@dataclass(frozen=True, slots=True)
class ProofResult:
    """Deterministic repository-local proof-chain view for one specification."""

    spec_id: str
    records: tuple[EvidenceRecord, ...]

    def __post_init__(self) -> None:
        if not is_spec_id(self.spec_id):
            raise VerificationError("spec_id must be a canonical SpecGrain ID")
        records = tuple(self.records)
        if any(not isinstance(record, EvidenceRecord) for record in records):
            raise VerificationError("records must contain EvidenceRecord values")
        object.__setattr__(self, "records", records)

    @property
    def latest(self) -> EvidenceRecord | None:
        """Return the current evidence-chain head."""

        return self.records[-1] if self.records else None

    @property
    def verified(self) -> bool:
        """Return whether the current chain head is independently verified."""

        return self.latest is not None and self.latest.report.verified

    def to_dict(self) -> dict[str, object]:
        """Return the deterministic proof representation."""

        return {
            "latest_record_digest": (
                None if self.latest is None else self.latest.record_digest
            ),
            "record_count": len(self.records),
            "records": [record.to_dict() for record in self.records],
            "spec_id": self.spec_id,
            "verified": self.verified,
        }


def _require_digest(value: object, field_name: str) -> str:
    if not isinstance(value, str) or _DIGEST_RE.fullmatch(value) is None:
        raise VerificationError(f"{field_name} must be a lowercase sha256 digest")
    return value


def _digest(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _normalize_paths(value: object, field_name: str) -> tuple[str, ...]:
    if isinstance(value, str | bytes | bytearray) or not isinstance(value, Sequence):
        raise VerificationError(
            f"{field_name} must be a sequence of repository-relative paths"
        )
    result: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise VerificationError(f"{field_name}[{index}] must be a non-empty string")
        if "\\" in item:
            raise VerificationError(f"{field_name}[{index}] must use POSIX separators")
        path = PurePosixPath(item)
        if path.is_absolute() or ".." in path.parts or not path.parts:
            raise VerificationError(
                f"{field_name}[{index}] must be repository-relative"
            )
        normalized = path.as_posix().rstrip("/")
        if normalized in seen:
            raise VerificationError(
                f"{field_name} must not contain duplicate path {normalized!r}"
            )
        seen.add(normalized)
        result.append(normalized)
    return tuple(sorted(result))


def _normalize_checks(value: object, field_name: str) -> tuple[CheckEvidence, ...]:
    if isinstance(value, str | bytes | bytearray) or not isinstance(value, Sequence):
        raise VerificationError(f"{field_name} must be a sequence of CheckEvidence")
    checks = tuple(value)
    for index, check in enumerate(checks):
        if not isinstance(check, CheckEvidence):
            raise VerificationError(f"{field_name}[{index}] must be a CheckEvidence")
    duplicates = sorted(
        check_id
        for check_id, count in Counter(check.check_id for check in checks).items()
        if count > 1
    )
    if duplicates:
        raise VerificationError(
            f"{field_name} contains duplicate check IDs: {', '.join(duplicates)}"
        )
    return tuple(sorted(checks, key=lambda check: check.check_id))


def _path_authorized(path: str, surfaces: tuple[str, ...]) -> bool:
    return any(path == surface or path.startswith(surface + "/") for surface in surfaces)


def _check_required(
    required: tuple[str, ...],
    checks: tuple[CheckEvidence, ...],
    *,
    missing_code: VerificationIssueCode,
    failed_code: VerificationIssueCode,
) -> list[VerificationIssue]:
    by_id = {check.check_id: check for check in checks}
    issues: list[VerificationIssue] = []
    for check_id in required:
        check = by_id.get(check_id)
        if check is None:
            issues.append(
                VerificationIssue(
                    missing_code,
                    check_id,
                    f"required check {check_id!r} is missing",
                )
            )
        elif not check.passed:
            issues.append(
                VerificationIssue(
                    failed_code,
                    check_id,
                    f"required check {check_id!r} failed",
                )
            )
    return issues


def verify_execution(
    current_node: SpecNode,
    packet: WorkPacket,
    result: ExecutionResult,
    *,
    implementation_revision: str,
    observed_changed_paths: Sequence[str],
    acceptance_checks: Sequence[CheckEvidence],
    evidence_checks: Sequence[CheckEvidence],
) -> VerificationReport:
    """Evaluate independent evidence without trusting executor completion claims."""

    if not isinstance(current_node, SpecNode):
        raise VerificationError("current_node must be a SpecNode")
    if not isinstance(packet, WorkPacket):
        raise VerificationError("packet must be a WorkPacket")
    if not isinstance(result, ExecutionResult):
        raise VerificationError("result must be an ExecutionResult")
    if not isinstance(implementation_revision, str) or not implementation_revision.strip():
        raise VerificationError("implementation_revision must be a non-empty string")

    observed = _normalize_paths(observed_changed_paths, "observed_changed_paths")
    surfaces = _normalize_paths(
        packet.authorized_change_surface,
        "packet.authorized_change_surface",
    )
    acceptance = _normalize_checks(acceptance_checks, "acceptance_checks")
    evidence = _normalize_checks(evidence_checks, "evidence_checks")
    issues: list[VerificationIssue] = []

    if packet.spec_id != current_node.id or packet.spec_revision != current_node.revision_digest:
        issues.append(
            VerificationIssue(
                VerificationIssueCode.SPEC_REVISION_MISMATCH,
                current_node.id,
                "packet is not bound to the current SpecNode semantic revision",
            )
        )
    if result.packet_digest != packet.packet_digest:
        issues.append(
            VerificationIssue(
                VerificationIssueCode.RESULT_PACKET_MISMATCH,
                packet.packet_digest,
                "execution result is bound to a different WorkPacket",
            )
        )
    if result.status is not ExecutionStatus.SUCCEEDED:
        issues.append(
            VerificationIssue(
                VerificationIssueCode.EXECUTION_NOT_SUCCEEDED,
                result.status.value,
                "executor did not report successful completion",
            )
        )
    if tuple(result.changed_paths) != observed:
        issues.append(
            VerificationIssue(
                VerificationIssueCode.EXECUTOR_SCOPE_MISMATCH,
                "changed_paths",
                "executor-reported changed paths do not match independently observed paths",
            )
        )
    for path in observed:
        if not _path_authorized(path, surfaces):
            issues.append(
                VerificationIssue(
                    VerificationIssueCode.UNSCOPED_CHANGE,
                    path,
                    f"observed changed path {path!r} is outside the authorized change surface",
                )
            )

    issues.extend(
        _check_required(
            packet.acceptance,
            acceptance,
            missing_code=VerificationIssueCode.ACCEPTANCE_MISSING,
            failed_code=VerificationIssueCode.ACCEPTANCE_FAILED,
        )
    )
    issues.extend(
        _check_required(
            packet.required_evidence,
            evidence,
            missing_code=VerificationIssueCode.EVIDENCE_MISSING,
            failed_code=VerificationIssueCode.EVIDENCE_FAILED,
        )
    )
    if not acceptance and not evidence:
        issues.append(
            VerificationIssue(
                VerificationIssueCode.INDEPENDENT_CHECK_MISSING,
                "independent_checks",
                "at least one independent acceptance or evidence check is required",
            )
        )

    return VerificationReport(
        spec_id=packet.spec_id,
        spec_revision=packet.spec_revision,
        packet_digest=packet.packet_digest,
        result_digest=result.result_digest,
        implementation_revision=implementation_revision,
        observed_changed_paths=observed,
        acceptance_checks=acceptance,
        evidence_checks=evidence,
        issues=tuple(issues),
    )


def _check_from_dict(data: object) -> CheckEvidence:
    if not isinstance(data, Mapping):
        raise VerificationError("check evidence must be an object")
    allowed = {"check_id", "detail", "evidence_ref", "passed"}
    if set(data) != allowed:
        raise VerificationError(
            "check evidence must contain exactly check_id/detail/evidence_ref/passed"
        )
    return CheckEvidence(**dict(data))


def _issue_from_dict(data: object) -> VerificationIssue:
    if not isinstance(data, Mapping) or set(data) != {"code", "message", "subject"}:
        raise VerificationError("verification issue has invalid fields")
    try:
        code = VerificationIssueCode(data["code"])
    except (TypeError, ValueError) as exc:
        raise VerificationError("verification issue has unknown code") from exc
    subject = data["subject"]
    message = data["message"]
    if not isinstance(subject, str) or not isinstance(message, str):
        raise VerificationError("verification issue subject/message must be strings")
    return VerificationIssue(code, subject, message)


def _report_from_dict(data: Mapping[str, object]) -> VerificationReport:
    allowed = {
        "acceptance_checks",
        "evidence_checks",
        "implementation_revision",
        "issues",
        "observed_changed_paths",
        "packet_digest",
        "result_digest",
        "spec_id",
        "spec_revision",
        "verification_version",
        "verified",
    }
    if set(data) != allowed:
        raise VerificationError("VerificationReport input has invalid fields")
    raw_acceptance = data["acceptance_checks"]
    raw_evidence = data["evidence_checks"]
    raw_issues = data["issues"]
    for name, value in (
        ("acceptance_checks", raw_acceptance),
        ("evidence_checks", raw_evidence),
        ("issues", raw_issues),
    ):
        if isinstance(value, str | bytes | bytearray) or not isinstance(value, Sequence):
            raise VerificationError(f"{name} must be an array")
    report = VerificationReport(
        spec_id=data["spec_id"],
        spec_revision=data["spec_revision"],
        packet_digest=data["packet_digest"],
        result_digest=data["result_digest"],
        implementation_revision=data["implementation_revision"],
        observed_changed_paths=data["observed_changed_paths"],
        acceptance_checks=tuple(_check_from_dict(item) for item in raw_acceptance),
        evidence_checks=tuple(_check_from_dict(item) for item in raw_evidence),
        issues=tuple(_issue_from_dict(item) for item in raw_issues),
        verification_version=data["verification_version"],
    )
    if not isinstance(data["verified"], bool) or data["verified"] is not report.verified:
        raise VerificationError(
            "verified field does not match independent verification issues"
        )
    return report


def _evidence_root(root: str | os.PathLike[str]) -> Path:
    repo = Path(root).expanduser()
    if repo.is_symlink() or not repo.is_dir():
        raise VerificationError("repository root must be an ordinary directory")
    store = repo / ".specgrain"
    if store.is_symlink() or not store.is_dir():
        raise VerificationError(".specgrain store must exist and not be a symlink")
    evidence = store / "evidence"
    if evidence.is_symlink():
        raise VerificationError(".specgrain/evidence symlink is not allowed")
    return evidence


def _reject_duplicate_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_non_finite(value: str) -> object:
    raise VerificationError(f"non-finite JSON number: {value}")


def _read_record(path: Path) -> EvidenceRecord:
    try:
        size = path.stat(follow_symlinks=False).st_size
    except OSError as exc:
        raise VerificationError(f"cannot stat evidence record {path.name}: {exc}") from exc
    if size > MAX_EVIDENCE_RECORD_BYTES:
        raise VerificationError(
            f"evidence record {path.name} exceeds {MAX_EVIDENCE_RECORD_BYTES} bytes"
        )
    try:
        with path.open("rb") as handle:
            raw = handle.read(MAX_EVIDENCE_RECORD_BYTES + 1)
    except OSError as exc:
        raise VerificationError(f"cannot read evidence record {path.name}: {exc}") from exc
    if len(raw) > MAX_EVIDENCE_RECORD_BYTES:
        raise VerificationError(
            f"evidence record {path.name} exceeds {MAX_EVIDENCE_RECORD_BYTES} bytes"
        )
    try:
        text = raw.decode("utf-8")
        data = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=_reject_non_finite,
        )
    except (UnicodeError, json.JSONDecodeError, VerificationError) as exc:
        raise VerificationError(f"invalid evidence record {path.name}: {exc}") from exc
    if not isinstance(data, Mapping):
        raise VerificationError(f"invalid evidence record {path.name}: root must be an object")
    return EvidenceRecord.from_dict(data)


def load_proof(root: str | os.PathLike[str], spec_id: str) -> ProofResult:
    """Load and validate one append-oriented evidence chain without mutation."""

    if not is_spec_id(spec_id):
        raise VerificationError("spec_id must be a canonical SpecGrain ID")
    evidence_root = _evidence_root(root)
    spec_dir = evidence_root / spec_id
    if not evidence_root.exists() or not spec_dir.exists():
        return ProofResult(spec_id, ())
    if spec_dir.is_symlink() or not spec_dir.is_dir():
        raise VerificationError(
            f".specgrain/evidence/{spec_id} must be an ordinary directory"
        )
    try:
        entries = sorted(spec_dir.iterdir(), key=lambda path: path.name)
    except OSError as exc:
        raise VerificationError(f"cannot list evidence records: {exc}") from exc
    if len(entries) > MAX_EVIDENCE_RECORDS:
        raise VerificationError(
            f"evidence chain exceeds {MAX_EVIDENCE_RECORDS} record entries"
        )

    records: dict[str, EvidenceRecord] = {}
    for path in entries:
        if path.is_symlink():
            raise VerificationError(f"evidence record symlink is not allowed: {path.name}")
        if not path.is_file() or path.suffix != ".json":
            raise VerificationError(f"unexpected evidence entry: {path.name}")
        record = _read_record(path)
        expected_name = record.record_digest[7:] + ".json"
        if path.name != expected_name:
            raise VerificationError(
                f"evidence filename does not match record digest: {path.name}"
            )
        if record.report.spec_id != spec_id:
            raise VerificationError(f"evidence record {path.name} belongs to another spec")
        if record.record_digest in records:
            raise VerificationError("duplicate evidence record digest")
        records[record.record_digest] = record

    if not records:
        return ProofResult(spec_id, ())
    referenced = {
        record.previous_record_digest
        for record in records.values()
        if record.previous_record_digest is not None
    }
    heads = sorted(set(records) - referenced)
    if len(heads) != 1:
        raise VerificationError("evidence chain must have exactly one head")
    chain: list[EvidenceRecord] = []
    current: str | None = heads[0]
    seen: set[str] = set()
    while current is not None:
        if current in seen or current not in records:
            raise VerificationError(
                "evidence chain is cyclic or references a missing record"
            )
        seen.add(current)
        record = records[current]
        chain.append(record)
        current = record.previous_record_digest
    if seen != set(records):
        raise VerificationError(
            "evidence directory contains records outside the canonical chain"
        )
    chain.reverse()
    return ProofResult(spec_id, tuple(chain))


def append_verification_report(
    root: str | os.PathLike[str], report: VerificationReport
) -> EvidenceRecord:
    """Append one immutable report and fail closed on overwrite or concurrent fork."""

    if not isinstance(report, VerificationReport):
        raise VerificationError("report must be a VerificationReport")
    evidence_root = _evidence_root(root)
    current = load_proof(root, report.spec_id)
    previous = None if current.latest is None else current.latest.record_digest
    record = EvidenceRecord(report, previous)
    spec_dir = evidence_root / report.spec_id
    try:
        evidence_root.mkdir(exist_ok=True)
        spec_dir.mkdir(exist_ok=True)
    except OSError as exc:
        raise VerificationError(f"cannot create evidence directory: {exc}") from exc
    if evidence_root.is_symlink() or spec_dir.is_symlink():
        raise VerificationError("evidence directories must not be symlinks")

    target = spec_dir / (record.record_digest[7:] + ".json")
    created = False
    try:
        with target.open("x", encoding="utf-8", newline="\n") as handle:
            created = True
            json.dump(
                record.to_dict(),
                handle,
                sort_keys=True,
                ensure_ascii=False,
                allow_nan=False,
                indent=2,
            )
            handle.write("\n")
        proof = load_proof(root, report.spec_id)
        if proof.latest is None or proof.latest.record_digest != record.record_digest:
            raise VerificationError("evidence append did not become the canonical chain head")
    except FileExistsError as exc:
        raise VerificationError("refusing to overwrite an existing evidence record") from exc
    except Exception:
        if created:
            with contextlib.suppress(OSError):
                target.unlink(missing_ok=True)
        raise
    return record
