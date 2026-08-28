"""Deterministic, bounded, read-only brownfield repository facts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

_SCAN_VERSION = 1
_GIT_METADATA_MAX_BYTES = 65_536
_IGNORED_DIRECTORIES = frozenset(
    {
        ".git",
        ".specgrain",
        ".venv",
        ".next",
        ".cache",
        "__pycache__",
        "build",
        "coverage",
        "dist",
        "node_modules",
        "target",
        "venv",
    }
)
_TEST_DIRECTORIES = frozenset({"tests", "test", "__tests__"})
_CONFIG_FILENAMES = frozenset(
    {
        ".pre-commit-config.yaml",
        "Dockerfile",
        "Makefile",
        "compose.yaml",
        "compose.yml",
        "docker-compose.yaml",
        "docker-compose.yml",
        "justfile",
        "mypy.ini",
        "pytest.ini",
        "ruff.toml",
        "tox.ini",
        "tsconfig.json",
    }
)
_LANGUAGE_EXTENSIONS = {
    ".bash": "Shell",
    ".c": "C",
    ".cc": "C++",
    ".cpp": "C++",
    ".cs": "C#",
    ".cxx": "C++",
    ".go": "Go",
    ".h": "C",
    ".hh": "C++",
    ".hpp": "C++",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".markdown": "Markdown",
    ".md": "Markdown",
    ".php": "PHP",
    ".py": "Python",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".sh": "Shell",
    ".sql": "SQL",
    ".swift": "Swift",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".zsh": "Shell",
}
_PYTHON_DEPENDENCY_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*")
_HEX_COMMIT = re.compile(r"^[0-9a-fA-F]{40}$")


class RepositoryScanError(Exception):
    """A stable, bounded repository-scan failure."""

    def __init__(self, code: str, message: str, *, location: str | None = None) -> None:
        self.code = code
        self.location = location
        self.message = message
        super().__init__(self._format())

    def _format(self) -> str:
        prefix = f"[{self.code}]"
        if self.location is not None:
            return f"{prefix} {self.location}: {self.message}"
        return f"{prefix} {self.message}"

    def to_dict(self) -> dict[str, str]:
        result = {"code": self.code, "message": self.message}
        if self.location is not None:
            result["location"] = self.location
        return result


@dataclass(frozen=True, slots=True)
class ScanLimits:
    """Hard repository-scan budgets."""

    max_files: int = 20_000
    max_depth: int = 12
    max_manifest_bytes: int = 1_048_576

    def __post_init__(self) -> None:
        for name, value in (
            ("max_files", self.max_files),
            ("max_depth", self.max_depth),
            ("max_manifest_bytes", self.max_manifest_bytes),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")


@dataclass(frozen=True, slots=True, order=True)
class RepositoryManifest:
    path: str
    kind: str
    size_bytes: int

    def to_dict(self) -> dict[str, object]:
        return {"kind": self.kind, "path": self.path, "size_bytes": self.size_bytes}


@dataclass(frozen=True, slots=True, order=True)
class LanguageSignal:
    language: str
    file_count: int

    def to_dict(self) -> dict[str, object]:
        return {"file_count": self.file_count, "language": self.language}


@dataclass(frozen=True, slots=True, order=True)
class DependencySignal:
    ecosystem: str
    name: str
    source_path: str

    def to_dict(self) -> dict[str, str]:
        return {
            "ecosystem": self.ecosystem,
            "name": self.name,
            "source_path": self.source_path,
        }


@dataclass(frozen=True, slots=True, order=True)
class ComponentSignal:
    kind: str
    name: str
    path: str

    def to_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "name": self.name, "path": self.path}


@dataclass(frozen=True, slots=True)
class GitFacts:
    present: bool
    layout: str
    head_ref: str | None = None
    head_commit: str | None = None

    def __post_init__(self) -> None:
        if self.layout not in {"none", "ordinary", "indirect"}:
            raise ValueError("git layout must be none, ordinary, or indirect")
        if not self.present and self.layout != "none":
            raise ValueError("absent git metadata must use none layout")
        if self.present and self.layout == "none":
            raise ValueError("present git metadata cannot use none layout")

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {"layout": self.layout, "present": self.present}
        if self.head_ref is not None:
            result["head_ref"] = self.head_ref
        if self.head_commit is not None:
            result["head_commit"] = self.head_commit
        return result


@dataclass(frozen=True, slots=True)
class RepositoryMap:
    scan_version: int
    repository_name: str
    file_count: int
    skipped_symlink_count: int
    top_level_entries: tuple[str, ...]
    manifests: tuple[RepositoryManifest, ...]
    config_paths: tuple[str, ...]
    test_paths: tuple[str, ...]
    languages: tuple[LanguageSignal, ...]
    dependencies: tuple[DependencySignal, ...]
    components: tuple[ComponentSignal, ...]
    git: GitFacts
    content_digest: str

    def _content_dict(self) -> dict[str, object]:
        return {
            "components": [item.to_dict() for item in self.components],
            "config_paths": list(self.config_paths),
            "dependencies": [item.to_dict() for item in self.dependencies],
            "file_count": self.file_count,
            "git": self.git.to_dict(),
            "languages": [item.to_dict() for item in self.languages],
            "manifests": [item.to_dict() for item in self.manifests],
            "repository_name": self.repository_name,
            "scan_version": self.scan_version,
            "skipped_symlink_count": self.skipped_symlink_count,
            "test_paths": list(self.test_paths),
            "top_level_entries": list(self.top_level_entries),
        }

    def to_dict(self) -> dict[str, object]:
        result = self._content_dict()
        result["content_digest"] = self.content_digest
        return result


@dataclass(slots=True)
class _ScanState:
    root: Path
    limits: ScanLimits
    file_count: int = 0
    skipped_symlinks: int = 0
    top_level_entries: set[str] | None = None
    manifests: list[RepositoryManifest] | None = None
    config_paths: set[str] | None = None
    test_paths: set[str] | None = None
    language_counts: dict[str, int] | None = None
    dependencies: set[DependencySignal] | None = None
    components: set[ComponentSignal] | None = None

    def __post_init__(self) -> None:
        self.top_level_entries = set()
        self.manifests = []
        self.config_paths = set()
        self.test_paths = set()
        self.language_counts = {}
        self.dependencies = set()
        self.components = set()


def _relative(path: str | PurePosixPath) -> str:
    return PurePosixPath(path).as_posix()


def _manifest_kind(name: str) -> str | None:
    lower = name.lower()
    if lower == "pyproject.toml" or lower in {"setup.py", "setup.cfg"}:
        return "python"
    if lower.startswith("requirements") and lower.endswith(".txt"):
        return "python"
    if lower in {
        "package.json",
        "package-lock.json",
        "npm-shrinkwrap.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "bun.lock",
        "bun.lockb",
    }:
        return "node"
    if lower in {"cargo.toml", "cargo.lock"}:
        return "rust"
    if lower in {"go.mod", "go.sum"}:
        return "go"
    if lower in {"pom.xml", "build.gradle", "build.gradle.kts"}:
        return "java"
    if name == "Gemfile":
        return "ruby"
    if lower == "composer.json":
        return "php"
    if lower.endswith(".sln") or lower.endswith(".csproj"):
        return "dotnet"
    return None


def _is_test_file(name: str) -> bool:
    lower = name.lower()
    if lower.startswith("test_") and lower.endswith(".py"):
        return True
    if lower.endswith("_test.py") or lower.endswith("_test.go"):
        return True
    return ".test." in lower or ".spec." in lower


def _is_config_file(name: str) -> bool:
    return name in _CONFIG_FILENAMES


def _read_bounded_text(path: Path, size: int, limit: int, location: str) -> str:
    if size > limit:
        raise RepositoryScanError(
            "MANIFEST_TOO_LARGE",
            f"manifest exceeds {limit} bytes",
            location=location,
        )
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise RepositoryScanError(
            "MANIFEST_INVALID",
            "manifest is not readable UTF-8 text",
            location=location,
        ) from exc


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def _reject_non_finite(value: str) -> Any:
    raise ValueError(f"non-finite JSON number: {value}")


def _dependency_name(requirement: str, location: str) -> str:
    match = _PYTHON_DEPENDENCY_NAME.match(requirement.strip())
    if match is None:
        raise RepositoryScanError(
            "MANIFEST_INVALID",
            "invalid Python dependency declaration",
            location=location,
        )
    return match.group(0)


def _extract_pyproject(text: str, location: str) -> set[str]:
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise RepositoryScanError(
            "MANIFEST_INVALID", "invalid TOML", location=location
        ) from exc
    names: set[str] = set()
    project = data.get("project", {})
    if not isinstance(project, dict):
        raise RepositoryScanError(
            "MANIFEST_INVALID", "project table must be a table", location=location
        )
    dependencies = project.get("dependencies", [])
    if not isinstance(dependencies, list) or not all(
        isinstance(item, str) for item in dependencies
    ):
        raise RepositoryScanError(
            "MANIFEST_INVALID",
            "project.dependencies must be an array of strings",
            location=location,
        )
    names.update(_dependency_name(item, location) for item in dependencies)
    optional = project.get("optional-dependencies", {})
    if not isinstance(optional, dict):
        raise RepositoryScanError(
            "MANIFEST_INVALID",
            "project.optional-dependencies must be a table",
            location=location,
        )
    for values in optional.values():
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            raise RepositoryScanError(
                "MANIFEST_INVALID",
                "optional dependency groups must be arrays of strings",
                location=location,
            )
        names.update(_dependency_name(item, location) for item in values)
    tool = data.get("tool", {})
    if not isinstance(tool, dict):
        raise RepositoryScanError(
            "MANIFEST_INVALID", "tool must be a table", location=location
        )
    poetry = tool.get("poetry", {})
    if poetry is None:
        poetry = {}
    if not isinstance(poetry, dict):
        raise RepositoryScanError(
            "MANIFEST_INVALID", "tool.poetry must be a table", location=location
        )
    poetry_dependencies = poetry.get("dependencies", {})
    if not isinstance(poetry_dependencies, dict):
        raise RepositoryScanError(
            "MANIFEST_INVALID",
            "tool.poetry.dependencies must be a table",
            location=location,
        )
    names.update(str(name) for name in poetry_dependencies if str(name).lower() != "python")
    return names


def _extract_package_json(text: str, location: str) -> set[str]:
    try:
        data = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=_reject_non_finite,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise RepositoryScanError(
            "MANIFEST_INVALID", "invalid package.json", location=location
        ) from exc
    if not isinstance(data, dict):
        raise RepositoryScanError(
            "MANIFEST_INVALID", "package.json root must be an object", location=location
        )
    names: set[str] = set()
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        value = data.get(key, {})
        if not isinstance(value, dict):
            raise RepositoryScanError(
                "MANIFEST_INVALID", f"{key} must be an object", location=location
            )
        if not all(isinstance(name, str) for name in value):
            raise RepositoryScanError(
                "MANIFEST_INVALID", f"{key} names must be strings", location=location
            )
        names.update(value)
    return names


def _extract_cargo(text: str, location: str) -> set[str]:
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise RepositoryScanError(
            "MANIFEST_INVALID", "invalid TOML", location=location
        ) from exc
    names: set[str] = set()
    for key in ("dependencies", "dev-dependencies", "build-dependencies"):
        value = data.get(key, {})
        if not isinstance(value, dict):
            raise RepositoryScanError(
                "MANIFEST_INVALID", f"{key} must be a table", location=location
            )
        names.update(str(name) for name in value)
    return names


def _extract_go_mod(text: str, location: str) -> set[str]:
    names: set[str] = set()
    in_require_block = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("//"):
            continue
        if in_require_block:
            if line == ")":
                in_require_block = False
                continue
            declaration = line.split("//", 1)[0].strip()
            parts = declaration.split()
            if len(parts) < 2:
                raise RepositoryScanError(
                    "MANIFEST_INVALID", "invalid go.mod require entry", location=location
                )
            names.add(parts[0])
            continue
        if line == "require (":
            in_require_block = True
            continue
        if line.startswith("require "):
            declaration = line[len("require ") :].split("//", 1)[0].strip()
            parts = declaration.split()
            if len(parts) < 2:
                raise RepositoryScanError(
                    "MANIFEST_INVALID", "invalid go.mod require entry", location=location
                )
            names.add(parts[0])
    if in_require_block:
        raise RepositoryScanError(
            "MANIFEST_INVALID", "unterminated go.mod require block", location=location
        )
    return names


def _extract_dependencies(path: Path, relative: str, size: int, limits: ScanLimits) -> set[str]:
    lower = path.name.lower()
    if lower not in {"pyproject.toml", "package.json", "cargo.toml", "go.mod"}:
        return set()
    text = _read_bounded_text(path, size, limits.max_manifest_bytes, relative)
    if lower == "pyproject.toml":
        return _extract_pyproject(text, relative)
    if lower == "package.json":
        return _extract_package_json(text, relative)
    if lower == "cargo.toml":
        return _extract_cargo(text, relative)
    return _extract_go_mod(text, relative)


def _dependency_ecosystem(name: str) -> str:
    return {
        "cargo.toml": "cargo",
        "go.mod": "go",
        "package.json": "npm",
        "pyproject.toml": "python",
    }[name.lower()]


def _record_directory(state: _ScanState, relative: str, name: str, depth: int) -> None:
    assert state.test_paths is not None
    assert state.config_paths is not None
    assert state.components is not None
    if name in _TEST_DIRECTORIES:
        state.test_paths.add(relative)
    if relative == ".github/workflows":
        state.config_paths.add(relative)
    parts = PurePosixPath(relative).parts
    if depth == 1:
        state.components.add(ComponentSignal("top-level", name, relative))
    elif len(parts) == 2:
        parent, child = parts
        kinds = {
            "apps": "app",
            "crates": "crate",
            "packages": "package",
            "services": "service",
            "src": "src-module",
        }
        if parent in kinds:
            state.components.add(ComponentSignal(kinds[parent], child, relative))


def _record_file(state: _ScanState, path: Path, relative: str, size: int) -> None:
    assert state.manifests is not None
    assert state.config_paths is not None
    assert state.test_paths is not None
    assert state.language_counts is not None
    assert state.dependencies is not None
    name = path.name
    kind = _manifest_kind(name)
    if kind is not None:
        state.manifests.append(RepositoryManifest(relative, kind, size))
        ecosystem = _dependency_ecosystem(name) if name.lower() in {
            "pyproject.toml",
            "package.json",
            "cargo.toml",
            "go.mod",
        } else None
        if ecosystem is not None:
            for dependency in _extract_dependencies(path, relative, size, state.limits):
                state.dependencies.add(DependencySignal(ecosystem, dependency, relative))
    if _is_config_file(name):
        state.config_paths.add(relative)
    if _is_test_file(name):
        state.test_paths.add(relative)
    language = _LANGUAGE_EXTENSIONS.get(path.suffix.lower())
    if language is not None:
        state.language_counts[language] = state.language_counts.get(language, 0) + 1


def _walk(
    state: _ScanState,
    directory: Path,
    relative_dir: PurePosixPath,
    child_depth: int,
) -> None:
    try:
        entries = sorted(os.scandir(directory), key=lambda item: item.name)
    except OSError as exc:
        location = relative_dir.as_posix() if relative_dir.parts else "."
        raise RepositoryScanError(
            "ROOT_INVALID", "repository directory is not readable", location=location
        ) from exc
    for entry in entries:
        name = entry.name
        relative = PurePosixPath(*relative_dir.parts, name)
        relative_text = relative.as_posix()
        try:
            if entry.is_symlink():
                state.skipped_symlinks += 1
                continue
            if not relative_dir.parts and name in {".git", ".specgrain"}:
                continue
            if entry.is_dir(follow_symlinks=False):
                if name in _IGNORED_DIRECTORIES:
                    continue
                if not relative_dir.parts:
                    assert state.top_level_entries is not None
                    state.top_level_entries.add(name)
                if child_depth > state.limits.max_depth:
                    raise RepositoryScanError(
                        "SCAN_DEPTH_LIMIT",
                        f"scan exceeds depth limit {state.limits.max_depth}",
                        location=relative_text,
                    )
                _record_directory(state, relative_text, name, child_depth)
                _walk(state, Path(entry.path), relative, child_depth + 1)
                continue
            if not entry.is_file(follow_symlinks=False):
                continue
            if not relative_dir.parts:
                assert state.top_level_entries is not None
                state.top_level_entries.add(name)
            if child_depth > state.limits.max_depth:
                raise RepositoryScanError(
                    "SCAN_DEPTH_LIMIT",
                    f"scan exceeds depth limit {state.limits.max_depth}",
                    location=relative_text,
                )
            state.file_count += 1
            if state.file_count > state.limits.max_files:
                raise RepositoryScanError(
                    "SCAN_FILE_LIMIT",
                    f"scan exceeds file limit {state.limits.max_files}",
                    location=relative_text,
                )
            stat = entry.stat(follow_symlinks=False)
            _record_file(state, Path(entry.path), relative_text, stat.st_size)
        except RepositoryScanError:
            raise
        except OSError as exc:
            raise RepositoryScanError(
                "ROOT_INVALID", "repository entry is not readable", location=relative_text
            ) from exc


def _safe_git_text(path: Path) -> str | None:
    try:
        if path.is_symlink() or not path.is_file():
            return None
        size = path.stat(follow_symlinks=False).st_size
        if size > _GIT_METADATA_MAX_BYTES:
            return None
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None


def _valid_ref_path(ref: str) -> bool:
    path = PurePosixPath(ref)
    return (
        not path.is_absolute()
        and bool(path.parts)
        and path.parts[0] == "refs"
        and ".." not in path.parts
        and "\\" not in ref
    )


def _resolve_git_ref(git_dir: Path, ref: str) -> str | None:
    if not _valid_ref_path(ref):
        return None
    loose_text = _safe_git_text(git_dir.joinpath(*PurePosixPath(ref).parts))
    if loose_text is not None:
        candidate = loose_text.strip()
        if _HEX_COMMIT.fullmatch(candidate):
            return candidate.lower()
    packed = _safe_git_text(git_dir / "packed-refs")
    if packed is None:
        return None
    for raw_line in packed.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("^"):
            continue
        parts = line.split()
        if len(parts) == 2 and parts[1] == ref and _HEX_COMMIT.fullmatch(parts[0]):
            return parts[0].lower()
    return None


def _git_facts(root: Path) -> GitFacts:
    git_path = root / ".git"
    try:
        if git_path.is_symlink():
            return GitFacts(present=True, layout="indirect")
        if git_path.is_file():
            return GitFacts(present=True, layout="indirect")
        if not git_path.exists():
            return GitFacts(present=False, layout="none")
        if not git_path.is_dir():
            return GitFacts(present=False, layout="none")
    except OSError:
        return GitFacts(present=False, layout="none")

    head_text = _safe_git_text(git_path / "HEAD")
    if head_text is None:
        return GitFacts(present=True, layout="ordinary")
    head = head_text.strip()
    if _HEX_COMMIT.fullmatch(head):
        return GitFacts(present=True, layout="ordinary", head_commit=head.lower())
    if head.startswith("ref: "):
        ref = head[5:].strip()
        if _valid_ref_path(ref):
            return GitFacts(
                present=True,
                layout="ordinary",
                head_ref=ref,
                head_commit=_resolve_git_ref(git_path, ref),
            )
    return GitFacts(present=True, layout="ordinary")


def _digest_content(content: dict[str, object]) -> str:
    encoded = json.dumps(
        content,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def scan_repository(
    path: str | os.PathLike[str] = ".",
    *,
    limits: ScanLimits | None = None,
) -> RepositoryMap:
    """Collect deterministic bounded facts from a repository directory without mutation."""

    active_limits = limits if limits is not None else ScanLimits()
    root_input = Path(path)
    try:
        if root_input.is_symlink() or not root_input.exists() or not root_input.is_dir():
            raise RepositoryScanError("ROOT_INVALID", "scan root must be an ordinary directory")
    except OSError as exc:
        raise RepositoryScanError(
            "ROOT_INVALID", "scan root must be an ordinary directory"
        ) from exc
    root = Path(os.path.abspath(os.fspath(root_input)))
    state = _ScanState(root=root, limits=active_limits)
    _walk(state, root, PurePosixPath(), 1)

    assert state.top_level_entries is not None
    assert state.manifests is not None
    assert state.config_paths is not None
    assert state.test_paths is not None
    assert state.language_counts is not None
    assert state.dependencies is not None
    assert state.components is not None
    languages = tuple(
        LanguageSignal(language, count)
        for language, count in sorted(state.language_counts.items())
    )
    repository_name = root.name or "."
    provisional = RepositoryMap(
        scan_version=_SCAN_VERSION,
        repository_name=repository_name,
        file_count=state.file_count,
        skipped_symlink_count=state.skipped_symlinks,
        top_level_entries=tuple(sorted(state.top_level_entries)),
        manifests=tuple(sorted(state.manifests)),
        config_paths=tuple(sorted(state.config_paths)),
        test_paths=tuple(sorted(state.test_paths)),
        languages=languages,
        dependencies=tuple(sorted(state.dependencies)),
        components=tuple(sorted(state.components)),
        git=_git_facts(root),
        content_digest="",
    )
    digest = _digest_content(provisional._content_dict())
    return RepositoryMap(
        scan_version=provisional.scan_version,
        repository_name=provisional.repository_name,
        file_count=provisional.file_count,
        skipped_symlink_count=provisional.skipped_symlink_count,
        top_level_entries=provisional.top_level_entries,
        manifests=provisional.manifests,
        config_paths=provisional.config_paths,
        test_paths=provisional.test_paths,
        languages=provisional.languages,
        dependencies=provisional.dependencies,
        components=provisional.components,
        git=provisional.git,
        content_digest=digest,
    )
