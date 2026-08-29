"""Repository-local SpecGrain store and deterministic project checks."""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
from collections.abc import Mapping
from contextlib import suppress
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from .lifecycle import SpecState
from .model import SpecNode, SpecValidationError, is_spec_id
from .readiness import GrainReadinessReport, evaluate_grain_readiness
from .refinement import refinement_roots, validate_refinement

STORE_VERSION = 1
POLICY_VERSION = 1
AUTHORING_TRANSACTION_VERSION = 1
_AUTHORING_OPERATION = "create_child_draft"
_AUTHORING_JOURNAL_LOCATION = ".specgrain/tmp/authoring-transaction.json"
_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


class ReadinessPolicyMode(StrEnum):
    """Project policy for readiness-blocked REFINING leaves."""

    REPORT = "report"
    ENFORCE = "enforce"


class AuthoringRecoveryStatus(StrEnum):
    """Deterministic outcome of explicit authoring-transaction recovery."""

    NONE = "none"
    CLEARED = "cleared"
    ROLLED_BACK = "rolled_back"
    FINALIZED = "finalized"


class StoreError(ValueError):
    """Base class for deterministic local-store errors."""

    def __init__(self, location: str, message: str) -> None:
        self.location = location
        self.detail = message
        super().__init__(f"{location}: {message}")


class StoreExistsError(StoreError):
    """Raised when initialization or creation would overwrite existing state."""


class StoreValidationError(StoreError):
    """Raised when repository-local state violates the store contract."""


@dataclass(frozen=True, slots=True)
class ProjectManifest:
    store_version: int
    project_id: str
    policy: str


@dataclass(frozen=True, slots=True)
class ProjectPolicy:
    policy_version: int
    readiness_mode: ReadinessPolicyMode


@dataclass(frozen=True, slots=True)
class LocalProject:
    root: Path
    store_path: Path
    manifest: ProjectManifest
    policy: ProjectPolicy
    specs: tuple[SpecNode, ...]


@dataclass(frozen=True, slots=True)
class ChildDraftResult:
    """One completed child-DRAFT authoring operation."""

    child: SpecNode
    parent_before_revision: str
    parent_after: SpecNode


@dataclass(frozen=True, slots=True)
class AuthoringRecoveryResult:
    """One explicit recovery outcome for the bounded authoring journal."""

    status: AuthoringRecoveryStatus
    parent_id: str | None
    child_id: str | None

    def to_dict(self) -> dict[str, str | None]:
        return {
            "child_id": self.child_id,
            "parent_id": self.parent_id,
            "status": self.status.value,
        }


@dataclass(frozen=True, slots=True)
class ProjectCheckIssue:
    code: str
    location: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code, "location": self.location, "message": self.message}


@dataclass(frozen=True, slots=True)
class ProjectCheckResult:
    valid: bool
    project_id: str | None
    policy_name: str | None
    readiness_mode: ReadinessPolicyMode | None
    spec_count: int
    root_count: int | None
    refining_leaf_count: int
    grain_ready_count: int
    readiness_blocked: tuple[GrainReadinessReport, ...]
    issues: tuple[ProjectCheckIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "project_id": self.project_id,
            "policy": self.policy_name,
            "readiness_mode": None if self.readiness_mode is None else self.readiness_mode.value,
            "spec_count": self.spec_count,
            "root_count": self.root_count,
            "refining_leaf_count": self.refining_leaf_count,
            "grain_ready_count": self.grain_ready_count,
            "readiness_blocked": [
                {
                    "node_id": report.node_id,
                    "revision_digest": report.revision_digest,
                    "issues": [
                        {
                            "code": issue.code.value,
                            "field": issue.field,
                            "message": issue.message,
                        }
                        for issue in report.issues
                    ],
                }
                for report in self.readiness_blocked
            ],
            "issues": [issue.to_dict() for issue in self.issues],
        }


@dataclass(frozen=True, slots=True)
class _AuthoringJournal:
    parent_id: str
    child_id: str
    parent_before_text: str
    parent_before: SpecNode
    parent_after: SpecNode
    child: SpecNode


class _DuplicateKeyError(ValueError):
    pass


def _object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKeyError(f"duplicate object key {key!r}")
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise ValueError(f"non-finite number token {value}")


def _safe_name(value: object, field: str, location: str) -> str:
    if not isinstance(value, str) or _NAME_RE.fullmatch(value) is None:
        raise StoreValidationError(
            location,
            f"{field} must match [A-Za-z0-9][A-Za-z0-9._-]{{0,63}}",
        )
    return value


def _require_version(value: object, expected: int, field: str, location: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value != expected:
        raise StoreValidationError(location, f"{field} must equal integer {expected}")
    return value


def _require_exact_fields(
    data: Mapping[str, object], required: set[str], location: str
) -> None:
    unknown = sorted(set(data) - required)
    missing = sorted(required - set(data))
    if unknown:
        raise StoreValidationError(location, f"unknown fields: {', '.join(unknown)}")
    if missing:
        raise StoreValidationError(location, f"missing fields: {', '.join(missing)}")


def _require_directory(path: Path, location: str) -> None:
    if path.is_symlink():
        raise StoreValidationError(location, "symlink is not allowed")
    if not path.is_dir():
        raise StoreValidationError(location, "required directory is missing")


def _require_file(path: Path, location: str) -> None:
    if path.is_symlink():
        raise StoreValidationError(location, "symlink is not allowed")
    if not path.is_file():
        raise StoreValidationError(location, "required file is missing")


def _parse_json_text(text: str, location: str) -> Mapping[str, object]:
    try:
        value = json.loads(
            text,
            object_pairs_hook=_object_pairs,
            parse_constant=_reject_constant,
        )
    except (json.JSONDecodeError, _DuplicateKeyError, ValueError) as exc:
        raise StoreValidationError(location, f"invalid JSON: {exc}") from exc
    if not isinstance(value, Mapping):
        raise StoreValidationError(location, "top-level JSON value must be an object")
    return value


def _read_text(path: Path, location: str) -> str:
    _require_file(path, location)
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise StoreValidationError(location, f"cannot read UTF-8 JSON: {exc}") from exc


def _strict_json(path: Path, location: str) -> Mapping[str, object]:
    return _parse_json_text(_read_text(path, location), location)


def _json_text(value: Mapping[str, object]) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def _write_json(path: Path, value: Mapping[str, object]) -> None:
    path.write_text(_json_text(value), encoding="utf-8", newline="\n")


def _write_new_json_with_detail(
    path: Path,
    value: Mapping[str, object],
    location: str,
    exists_detail: str,
) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    try:
        descriptor = os.open(path, flags, 0o644)
    except FileExistsError as exc:
        raise StoreExistsError(location, exists_detail) from exc
    except OSError as exc:
        raise StoreValidationError(location, f"cannot create JSON file: {exc}") from exc

    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(_json_text(value))
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        with suppress(OSError):
            path.unlink(missing_ok=True)
        raise


def _write_new_json(path: Path, value: Mapping[str, object], location: str) -> None:
    """Create one spec JSON file without ever replacing an existing path."""

    _write_new_json_with_detail(
        path,
        value,
        location,
        "spec already exists; refusing overwrite",
    )


def _repository_root(root: str | os.PathLike[str]) -> Path:
    path = Path(root).expanduser()
    if path.is_symlink():
        raise StoreValidationError(".", "repository root symlink is not allowed")
    if not path.is_dir():
        raise StoreValidationError(".", "repository root must be an existing directory")
    try:
        return path.resolve(strict=True)
    except OSError as exc:
        raise StoreValidationError(".", f"cannot resolve repository root: {exc}") from exc


def _parse_manifest(data: Mapping[str, object]) -> ProjectManifest:
    location = ".specgrain/project.json"
    required = {"store_version", "project_id", "policy"}
    _require_exact_fields(data, required, location)
    return ProjectManifest(
        store_version=_require_version(
            data["store_version"], STORE_VERSION, "store_version", location
        ),
        project_id=_safe_name(data["project_id"], "project_id", location),
        policy=_safe_name(data["policy"], "policy", location),
    )


def _parse_policy(data: Mapping[str, object], policy_name: str) -> ProjectPolicy:
    location = f".specgrain/policies/{policy_name}.json"
    required = {"policy_version", "readiness_mode"}
    _require_exact_fields(data, required, location)
    version = _require_version(data["policy_version"], POLICY_VERSION, "policy_version", location)
    try:
        mode = ReadinessPolicyMode(data["readiness_mode"])
    except (TypeError, ValueError) as exc:
        raise StoreValidationError(
            location, "readiness_mode must be 'report' or 'enforce'"
        ) from exc
    return ProjectPolicy(policy_version=version, readiness_mode=mode)


def _authoring_tmp_path(root_path: Path) -> Path:
    return root_path / ".specgrain" / "tmp"


def _authoring_journal_path(root_path: Path) -> Path:
    return root_path / _AUTHORING_JOURNAL_LOCATION


def _inspect_authoring_journal_path(root_path: Path) -> Path | None:
    tmp_path = _authoring_tmp_path(root_path)
    if tmp_path.is_symlink():
        raise StoreValidationError(".specgrain/tmp", "symlink is not allowed")
    if tmp_path.exists() and not tmp_path.is_dir():
        raise StoreValidationError(".specgrain/tmp", "runtime path must be a directory")
    journal_path = _authoring_journal_path(root_path)
    if journal_path.is_symlink():
        raise StoreValidationError(_AUTHORING_JOURNAL_LOCATION, "symlink is not allowed")
    if journal_path.exists() and not journal_path.is_file():
        raise StoreValidationError(
            _AUTHORING_JOURNAL_LOCATION,
            "authoring transaction journal must be a regular file",
        )
    return journal_path if journal_path.is_file() else None


def _reject_pending_authoring_transaction(root_path: Path) -> None:
    if _inspect_authoring_journal_path(root_path) is not None:
        raise StoreValidationError(
            _AUTHORING_JOURNAL_LOCATION,
            "pending authoring transaction requires explicit recovery",
        )


def _ensure_authoring_tmp(root_path: Path) -> Path:
    tmp_path = _authoring_tmp_path(root_path)
    if tmp_path.is_symlink():
        raise StoreValidationError(".specgrain/tmp", "symlink is not allowed")
    try:
        tmp_path.mkdir()
    except OSError as exc:
        if not isinstance(exc, FileExistsError):
            raise StoreValidationError(
                ".specgrain/tmp", f"cannot create runtime directory: {exc}"
            ) from exc
    if tmp_path.is_symlink() or not tmp_path.is_dir():
        raise StoreValidationError(".specgrain/tmp", "runtime path must be a real directory")
    return tmp_path


def init_project(
    root: str | os.PathLike[str] = ".", *, project_id: str | None = None
) -> LocalProject:
    """Create a new dependency-free store without overwriting existing state."""

    root_path = _repository_root(root)
    store_path = root_path / ".specgrain"
    if store_path.is_symlink() or store_path.exists():
        raise StoreExistsError(".specgrain", "store already exists; refusing overwrite")

    chosen_id = project_id if project_id is not None else root_path.name
    chosen_id = _safe_name(chosen_id, "project_id", ".specgrain/project.json")

    staging = Path(tempfile.mkdtemp(prefix=".specgrain-init-", dir=root_path))
    try:
        (staging / "specs").mkdir()
        (staging / "policies").mkdir()
        _write_json(
            staging / "project.json",
            {"store_version": STORE_VERSION, "project_id": chosen_id, "policy": "default"},
        )
        _write_json(
            staging / "policies" / "default.json",
            {"policy_version": POLICY_VERSION, "readiness_mode": ReadinessPolicyMode.REPORT.value},
        )
        if store_path.is_symlink() or store_path.exists():
            raise StoreExistsError(".specgrain", "store appeared during initialization")
        os.rename(staging, store_path)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        raise

    return load_project(root_path)


def _load_project_from_root(root_path: Path, *, reject_pending: bool) -> LocalProject:
    store_path = root_path / ".specgrain"
    specs_path = store_path / "specs"
    policies_path = store_path / "policies"

    _require_directory(store_path, ".specgrain")
    _require_directory(specs_path, ".specgrain/specs")
    _require_directory(policies_path, ".specgrain/policies")
    if reject_pending:
        _reject_pending_authoring_transaction(root_path)

    manifest = _parse_manifest(_strict_json(store_path / "project.json", ".specgrain/project.json"))
    policy_location = f".specgrain/policies/{manifest.policy}.json"
    policy = _parse_policy(
        _strict_json(policies_path / f"{manifest.policy}.json", policy_location),
        manifest.policy,
    )

    specs: list[SpecNode] = []
    try:
        entries = sorted(specs_path.iterdir(), key=lambda item: item.name)
    except OSError as exc:
        raise StoreValidationError(".specgrain/specs", f"cannot list specs: {exc}") from exc

    for path in entries:
        location = f".specgrain/specs/{path.name}"
        if path.is_symlink():
            raise StoreValidationError(location, "symlink is not allowed")
        if not path.is_file() or path.suffix != ".json":
            continue
        if not is_spec_id(path.stem):
            raise StoreValidationError(
                location, "spec filename must be <canonical SpecNode ID>.json"
            )
        data = _strict_json(path, location)
        try:
            node = SpecNode.from_dict(data)
        except SpecValidationError as exc:
            raise StoreValidationError(location, f"invalid SpecNode: {exc}") from exc
        if node.id != path.stem:
            raise StoreValidationError(
                location, f"filename ID {path.stem} does not match content ID {node.id}"
            )
        specs.append(node)

    return LocalProject(
        root=root_path,
        store_path=store_path,
        manifest=manifest,
        policy=policy,
        specs=tuple(sorted(specs, key=lambda node: node.id)),
    )


def load_project(root: str | os.PathLike[str] = ".") -> LocalProject:
    """Load canonical local state without running graph/readiness checks."""

    return _load_project_from_root(_repository_root(root), reject_pending=True)


def _next_draft_id(specs: tuple[SpecNode, ...]) -> str:
    used = {int(node.id.removeprefix("SG-")) for node in specs}
    for number in range(1, 1_000_000):
        if number not in used:
            return f"SG-{number:06d}"
    raise StoreValidationError(
        ".specgrain/specs", "no positive six-digit SpecNode identifiers remain"
    )


def _require_valid_existing_refinement(project: LocalProject) -> None:
    refinement_issues = validate_refinement(project.specs)
    if refinement_issues:
        first = refinement_issues[0]
        raise StoreValidationError(
            ".specgrain/specs",
            f"existing refinement is invalid: {first.code.value}: {first.message}",
        )


def create_draft_spec(
    root: str | os.PathLike[str] = ".",
    *,
    title: str,
    outcome: str,
    rationale: str = "",
) -> SpecNode:
    """Create one validated root DRAFT without overwriting repository-local state."""

    project = load_project(root)
    _require_valid_existing_refinement(project)

    node = SpecNode(
        id=_next_draft_id(project.specs),
        title=title,
        outcome=outcome,
        rationale=rationale,
        state=SpecState.DRAFT.value,
    )
    relative_path = f".specgrain/specs/{node.id}.json"
    _write_new_json(project.root / relative_path, node.to_dict(), relative_path)
    return node


def _spec_from_mapping(value: object, field: str, location: str) -> SpecNode:
    if not isinstance(value, Mapping):
        raise StoreValidationError(location, f"{field} must be an object")
    try:
        return SpecNode.from_dict(value)
    except SpecValidationError as exc:
        raise StoreValidationError(location, f"{field} is not a valid SpecNode: {exc}") from exc


def _parse_authoring_journal(path: Path) -> _AuthoringJournal:
    data = _strict_json(path, _AUTHORING_JOURNAL_LOCATION)
    required = {
        "transaction_version",
        "operation",
        "parent_id",
        "child_id",
        "parent_before_text",
        "parent_after",
        "child",
    }
    _require_exact_fields(data, required, _AUTHORING_JOURNAL_LOCATION)
    _require_version(
        data["transaction_version"],
        AUTHORING_TRANSACTION_VERSION,
        "transaction_version",
        _AUTHORING_JOURNAL_LOCATION,
    )
    if data["operation"] != _AUTHORING_OPERATION:
        raise StoreValidationError(
            _AUTHORING_JOURNAL_LOCATION,
            f"operation must equal {_AUTHORING_OPERATION!r}",
        )
    parent_id = data["parent_id"]
    child_id = data["child_id"]
    if not is_spec_id(parent_id):
        raise StoreValidationError(_AUTHORING_JOURNAL_LOCATION, "parent_id is not canonical")
    if not is_spec_id(child_id):
        raise StoreValidationError(_AUTHORING_JOURNAL_LOCATION, "child_id is not canonical")
    before_text = data["parent_before_text"]
    if not isinstance(before_text, str):
        raise StoreValidationError(
            _AUTHORING_JOURNAL_LOCATION,
            "parent_before_text must be a string",
        )
    before = _spec_from_mapping(
        _parse_json_text(before_text, _AUTHORING_JOURNAL_LOCATION),
        "parent_before_text",
        _AUTHORING_JOURNAL_LOCATION,
    )
    after = _spec_from_mapping(data["parent_after"], "parent_after", _AUTHORING_JOURNAL_LOCATION)
    child = _spec_from_mapping(data["child"], "child", _AUTHORING_JOURNAL_LOCATION)

    if before.id != parent_id or after.id != parent_id:
        raise StoreValidationError(
            _AUTHORING_JOURNAL_LOCATION,
            "parent journal identity does not match parent_id",
        )
    if child.id != child_id or child.parent_id != parent_id:
        raise StoreValidationError(
            _AUTHORING_JOURNAL_LOCATION,
            "child journal identity does not match parent/child IDs",
        )
    if before.state != SpecState.DRAFT.value or after.state != SpecState.DRAFT.value:
        raise StoreValidationError(
            _AUTHORING_JOURNAL_LOCATION,
            "journal parent must remain DRAFT",
        )
    if child.state != SpecState.DRAFT.value:
        raise StoreValidationError(_AUTHORING_JOURNAL_LOCATION, "journal child must be DRAFT")

    before_dict = before.to_dict()
    after_dict = after.to_dict()
    before_children = before_dict.pop("children")
    after_children = after_dict.pop("children")
    if before_dict != after_dict:
        raise StoreValidationError(
            _AUTHORING_JOURNAL_LOCATION,
            "journal parent postimage changes fields other than children",
        )
    expected_children = [*before.children, child_id]
    if after_children != expected_children or child_id in before_children:
        raise StoreValidationError(
            _AUTHORING_JOURNAL_LOCATION,
            "journal parent child mutation is not the expected single append",
        )

    proposed = (after, child)
    structural = validate_refinement(proposed)
    external_issues = [
        issue
        for issue in structural
        if issue.code.value not in {"MISSING_PARENT", "MISSING_CHILD"}
    ]
    if external_issues:
        raise StoreValidationError(
            _AUTHORING_JOURNAL_LOCATION,
            f"journal contains invalid parent/child structure: {external_issues[0].message}",
        )

    return _AuthoringJournal(parent_id, child_id, before_text, before, after, child)


def _authoring_journal_value(
    parent_before_text: str,
    parent_after: SpecNode,
    child: SpecNode,
) -> dict[str, object]:
    assert child.parent_id == parent_after.id
    return {
        "transaction_version": AUTHORING_TRANSACTION_VERSION,
        "operation": _AUTHORING_OPERATION,
        "parent_id": parent_after.id,
        "child_id": child.id,
        "parent_before_text": parent_before_text,
        "parent_after": parent_after.to_dict(),
        "child": child.to_dict(),
    }


def _write_authoring_journal(
    root_path: Path,
    parent_before_text: str,
    parent_after: SpecNode,
    child: SpecNode,
) -> Path:
    _ensure_authoring_tmp(root_path)
    path = _authoring_journal_path(root_path)
    _write_new_json_with_detail(
        path,
        _authoring_journal_value(parent_before_text, parent_after, child),
        _AUTHORING_JOURNAL_LOCATION,
        "authoring transaction already exists; explicit recovery required",
    )
    return path


def _replace_json_exact(
    path: Path,
    before_text: str,
    value: Mapping[str, object],
    location: str,
) -> None:
    if _read_text(path, location) != before_text:
        raise StoreValidationError(location, "parent changed during authoring transaction")

    descriptor: int | None = None
    temp_path: Path | None = None
    try:
        descriptor, raw_temp = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
        )
        temp_path = Path(raw_temp)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            descriptor = None
            handle.write(_json_text(value))
            handle.flush()
            os.fsync(handle.fileno())
        if _read_text(path, location) != before_text:
            raise StoreValidationError(location, "parent changed during authoring transaction")
        os.replace(temp_path, path)
        temp_path = None
    except StoreError:
        raise
    except OSError as exc:
        raise StoreValidationError(location, f"cannot replace parent spec: {exc}") from exc
    finally:
        if descriptor is not None:
            with suppress(OSError):
                os.close(descriptor)
        if temp_path is not None:
            with suppress(OSError):
                temp_path.unlink(missing_ok=True)


def _remove_journal(path: Path) -> None:
    try:
        path.unlink()
    except OSError as exc:
        raise StoreValidationError(
            _AUTHORING_JOURNAL_LOCATION,
            f"cannot remove authoring transaction journal: {exc}",
        ) from exc


def _optional_file_text(path: Path, location: str) -> str | None:
    if path.is_symlink():
        raise StoreValidationError(location, "symlink is not allowed")
    if not path.exists():
        return None
    if not path.is_file():
        raise StoreValidationError(location, "expected regular file")
    return _read_text(path, location)


def recover_authoring_transaction(
    root: str | os.PathLike[str] = ".",
) -> AuthoringRecoveryResult:
    """Explicitly recover one exact recognized child-authoring transaction state."""

    root_path = _repository_root(root)
    store_path = root_path / ".specgrain"
    _require_directory(store_path, ".specgrain")
    _require_directory(store_path / "specs", ".specgrain/specs")
    _require_directory(store_path / "policies", ".specgrain/policies")

    journal_path = _inspect_authoring_journal_path(root_path)
    if journal_path is None:
        _load_project_from_root(root_path, reject_pending=True)
        return AuthoringRecoveryResult(AuthoringRecoveryStatus.NONE, None, None)

    journal = _parse_authoring_journal(journal_path)
    parent_location = f".specgrain/specs/{journal.parent_id}.json"
    child_location = f".specgrain/specs/{journal.child_id}.json"
    parent_path = root_path / parent_location
    child_path = root_path / child_location

    parent_text = _optional_file_text(parent_path, parent_location)
    child_text = _optional_file_text(child_path, child_location)
    after_text = _json_text(journal.parent_after.to_dict())
    expected_child_text = _json_text(journal.child.to_dict())

    if parent_text == journal.parent_before_text and child_text is None:
        _remove_journal(journal_path)
        _load_project_from_root(root_path, reject_pending=True)
        return AuthoringRecoveryResult(
            AuthoringRecoveryStatus.CLEARED,
            journal.parent_id,
            journal.child_id,
        )

    if parent_text == journal.parent_before_text and child_text == expected_child_text:
        try:
            child_path.unlink()
        except OSError as exc:
            raise StoreValidationError(
                child_location,
                f"cannot roll back transaction-created child: {exc}",
            ) from exc
        _remove_journal(journal_path)
        _load_project_from_root(root_path, reject_pending=True)
        return AuthoringRecoveryResult(
            AuthoringRecoveryStatus.ROLLED_BACK,
            journal.parent_id,
            journal.child_id,
        )

    if parent_text == after_text and child_text == expected_child_text:
        _remove_journal(journal_path)
        _load_project_from_root(root_path, reject_pending=True)
        return AuthoringRecoveryResult(
            AuthoringRecoveryStatus.FINALIZED,
            journal.parent_id,
            journal.child_id,
        )

    raise StoreValidationError(
        _AUTHORING_JOURNAL_LOCATION,
        "authoring transaction state is ambiguous; canonical files were not changed",
    )


def create_child_draft_spec(
    root: str | os.PathLike[str] = ".",
    *,
    parent_id: str,
    title: str,
    outcome: str,
    rationale: str = "",
) -> ChildDraftResult:
    """Create one child DRAFT under an existing DRAFT parent with explicit recovery."""

    if not is_spec_id(parent_id):
        raise StoreValidationError(
            ".specgrain/specs",
            "parent_id must match 'SG-' followed by exactly six decimal digits",
        )

    project = load_project(root)
    _require_valid_existing_refinement(project)
    by_id = {node.id: node for node in project.specs}
    parent = by_id.get(parent_id)
    if parent is None:
        raise StoreValidationError(
            f".specgrain/specs/{parent_id}.json",
            "parent spec does not exist",
        )
    if parent.state != SpecState.DRAFT.value:
        raise StoreValidationError(
            f".specgrain/specs/{parent_id}.json",
            "child authoring requires parent state DRAFT",
        )

    child = SpecNode(
        id=_next_draft_id(project.specs),
        title=title,
        outcome=outcome,
        rationale=rationale,
        parent_id=parent.id,
        state=SpecState.DRAFT.value,
    )
    parent_data = parent.to_dict()
    parent_data["children"] = [*parent.children, child.id]
    parent_after = SpecNode.from_dict(parent_data)

    proposed = tuple(
        parent_after if node.id == parent.id else node for node in project.specs
    ) + (child,)
    refinement_issues = validate_refinement(proposed)
    if refinement_issues:
        first = refinement_issues[0]
        raise StoreValidationError(
            ".specgrain/specs",
            f"proposed refinement is invalid: {first.code.value}: {first.message}",
        )

    parent_location = f".specgrain/specs/{parent.id}.json"
    parent_path = project.root / parent_location
    parent_before_text = _read_text(parent_path, parent_location)
    try:
        current_parent = SpecNode.from_dict(_parse_json_text(parent_before_text, parent_location))
    except SpecValidationError as exc:
        raise StoreValidationError(parent_location, f"invalid SpecNode: {exc}") from exc
    if current_parent.to_dict() != parent.to_dict():
        raise StoreValidationError(parent_location, "parent changed before authoring transaction")

    journal_path = _write_authoring_journal(
        project.root,
        parent_before_text,
        parent_after,
        child,
    )
    child_location = f".specgrain/specs/{child.id}.json"
    child_path = project.root / child_location

    try:
        _write_new_json(child_path, child.to_dict(), child_location)
    except StoreExistsError as exc:
        if _read_text(parent_path, parent_location) != parent_before_text:
            raise StoreValidationError(
                _AUTHORING_JOURNAL_LOCATION,
                "child collision coincided with parent drift; explicit recovery required",
            ) from exc
        _remove_journal(journal_path)
        raise
    except Exception as exc:
        try:
            recover_authoring_transaction(project.root)
        except StoreError as recovery_exc:
            raise StoreValidationError(
                _AUTHORING_JOURNAL_LOCATION,
                f"authoring failed; explicit recovery required: {recovery_exc.detail}",
            ) from exc
        raise

    try:
        _replace_json_exact(
            parent_path,
            parent_before_text,
            parent_after.to_dict(),
            parent_location,
        )
        if _read_text(parent_path, parent_location) != _json_text(parent_after.to_dict()):
            raise StoreValidationError(parent_location, "parent postimage confirmation failed")
        if _read_text(child_path, child_location) != _json_text(child.to_dict()):
            raise StoreValidationError(child_location, "child postimage confirmation failed")
        _remove_journal(journal_path)
    except Exception as exc:
        try:
            recovery = recover_authoring_transaction(project.root)
        except StoreError as recovery_exc:
            raise StoreValidationError(
                _AUTHORING_JOURNAL_LOCATION,
                f"authoring failed; explicit recovery required: {recovery_exc.detail}",
            ) from exc
        if recovery.status is AuthoringRecoveryStatus.FINALIZED:
            return ChildDraftResult(child, parent.revision_digest, parent_after)
        raise

    return ChildDraftResult(child, parent.revision_digest, parent_after)


def check_project(root: str | os.PathLike[str] = ".") -> ProjectCheckResult:
    """Load and deterministically validate one local SpecGrain project."""

    try:
        project = load_project(root)
    except StoreError as exc:
        return ProjectCheckResult(
            valid=False,
            project_id=None,
            policy_name=None,
            readiness_mode=None,
            spec_count=0,
            root_count=None,
            refining_leaf_count=0,
            grain_ready_count=0,
            readiness_blocked=(),
            issues=(ProjectCheckIssue("STORE_INVALID", exc.location, exc.detail),),
        )

    structural = validate_refinement(project.specs)
    if structural:
        issues = tuple(
            ProjectCheckIssue(
                issue.code.value,
                f".specgrain/specs/{issue.node_id}.json",
                issue.message,
            )
            for issue in structural
        )
        return ProjectCheckResult(
            valid=False,
            project_id=project.manifest.project_id,
            policy_name=project.manifest.policy,
            readiness_mode=project.policy.readiness_mode,
            spec_count=len(project.specs),
            root_count=None,
            refining_leaf_count=0,
            grain_ready_count=0,
            readiness_blocked=(),
            issues=issues,
        )

    roots = refinement_roots(project.specs)
    refining_leaves = tuple(
        node
        for node in project.specs
        if node.state == SpecState.REFINING.value and not node.children
    )
    reports = tuple(evaluate_grain_readiness(node, project.specs) for node in refining_leaves)
    blocked = tuple(report for report in reports if not report.is_ready)
    ready_count = len(reports) - len(blocked)
    valid = not blocked or project.policy.readiness_mode is ReadinessPolicyMode.REPORT

    return ProjectCheckResult(
        valid=valid,
        project_id=project.manifest.project_id,
        policy_name=project.manifest.policy,
        readiness_mode=project.policy.readiness_mode,
        spec_count=len(project.specs),
        root_count=len(roots),
        refining_leaf_count=len(refining_leaves),
        grain_ready_count=ready_count,
        readiness_blocked=blocked,
        issues=(),
    )
