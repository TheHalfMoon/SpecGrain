"""Repository-local SpecGrain store and deterministic project checks."""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
from collections.abc import Mapping
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
_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


class ReadinessPolicyMode(StrEnum):
    """Project policy for readiness-blocked REFINING leaves."""

    REPORT = "report"
    ENFORCE = "enforce"


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


def _strict_json(path: Path, location: str) -> Mapping[str, object]:
    _require_file(path, location)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise StoreValidationError(location, f"cannot read UTF-8 JSON: {exc}") from exc
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


def _json_text(value: Mapping[str, object]) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def _write_json(path: Path, value: Mapping[str, object]) -> None:
    path.write_text(_json_text(value), encoding="utf-8", newline="\n")


def _write_new_json(path: Path, value: Mapping[str, object], location: str) -> None:
    """Create one JSON file without ever replacing an existing path."""

    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    try:
        descriptor = os.open(path, flags, 0o644)
    except FileExistsError as exc:
        raise StoreExistsError(location, "spec already exists; refusing overwrite") from exc
    except OSError as exc:
        raise StoreValidationError(location, f"cannot create spec file: {exc}") from exc

    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(_json_text(value))
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass
        raise


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


def load_project(root: str | os.PathLike[str] = ".") -> LocalProject:
    """Load canonical local state without running graph/readiness checks."""

    root_path = _repository_root(root)
    store_path = root_path / ".specgrain"
    specs_path = store_path / "specs"
    policies_path = store_path / "policies"

    _require_directory(store_path, ".specgrain")
    _require_directory(specs_path, ".specgrain/specs")
    _require_directory(policies_path, ".specgrain/policies")

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


def _next_draft_id(specs: tuple[SpecNode, ...]) -> str:
    used = {int(node.id.removeprefix("SG-")) for node in specs}
    for number in range(1, 1_000_000):
        if number not in used:
            return f"SG-{number:06d}"
    raise StoreValidationError(
        ".specgrain/specs", "no positive six-digit SpecNode identifiers remain"
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
    refinement_issues = validate_refinement(project.specs)
    if refinement_issues:
        first = refinement_issues[0]
        raise StoreValidationError(
            ".specgrain/specs",
            f"existing refinement is invalid: {first.code.value}: {first.message}",
        )

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
