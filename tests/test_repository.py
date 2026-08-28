from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src" / "specgrain"))

from repository import RepositoryScanError, ScanLimits, scan_repository  # noqa: E402


def write(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_scan_limits_reject_bool_and_non_positive() -> None:
    with pytest.raises(ValueError):
        ScanLimits(max_files=True)
    with pytest.raises(ValueError):
        ScanLimits(max_depth=0)
    with pytest.raises(ValueError):
        ScanLimits(max_manifest_bytes=-1)


def test_root_must_be_existing_directory_and_not_symlink(tmp_path: Path) -> None:
    missing = tmp_path / "missing"
    with pytest.raises(RepositoryScanError, match="ROOT_INVALID"):
        scan_repository(missing)
    file_path = tmp_path / "file"
    write(file_path)
    with pytest.raises(RepositoryScanError, match="ROOT_INVALID"):
        scan_repository(file_path)
    if hasattr(os, "symlink"):
        target = tmp_path / "target"
        target.mkdir()
        link = tmp_path / "link"
        link.symlink_to(target, target_is_directory=True)
        with pytest.raises(RepositoryScanError, match="ROOT_INVALID"):
            scan_repository(link)


def test_scan_deterministic_and_digest_changes_with_facts(tmp_path: Path) -> None:
    write(tmp_path / "src" / "a.py", "print('a')\n")
    first = scan_repository(tmp_path)
    second = scan_repository(tmp_path)
    assert first.to_dict() == second.to_dict()
    write(tmp_path / "src" / "b.py", "print('b')\n")
    third = scan_repository(tmp_path)
    assert third.content_digest != first.content_digest


def test_scan_skips_control_vendor_and_generated_directories(tmp_path: Path) -> None:
    for directory in (
        ".git",
        ".specgrain",
        "node_modules",
        ".venv",
        "target",
        "dist",
        "build",
        ".next",
        ".cache",
        "coverage",
        "__pycache__",
    ):
        write(tmp_path / directory / "ignored.py", "x=1\n")
    write(tmp_path / "src" / "kept.py", "x=1\n")
    result = scan_repository(tmp_path)
    assert result.file_count == 1
    assert [item.language for item in result.languages] == ["Python"]
    assert result.languages[0].file_count == 1


def test_symlink_file_and_directory_are_counted_and_not_followed(tmp_path: Path) -> None:
    if not hasattr(os, "symlink"):
        pytest.skip("symlink unavailable")
    outside = tmp_path / "outside"
    outside.mkdir()
    write(outside / "secret.py", "secret=1\n")
    root = tmp_path / "repo"
    root.mkdir()
    write(root / "real.py", "x=1\n")
    (root / "linked-file.py").symlink_to(outside / "secret.py")
    (root / "linked-dir").symlink_to(outside, target_is_directory=True)
    result = scan_repository(root)
    assert result.file_count == 1
    assert result.skipped_symlink_count == 2


def test_file_limit_fails_closed_with_relative_location(tmp_path: Path) -> None:
    write(tmp_path / "a.py")
    write(tmp_path / "b.py")
    with pytest.raises(RepositoryScanError) as caught:
        scan_repository(tmp_path, limits=ScanLimits(max_files=1))
    assert caught.value.code == "SCAN_FILE_LIMIT"
    assert caught.value.location == "b.py"


def test_depth_limit_fails_closed(tmp_path: Path) -> None:
    write(tmp_path / "a" / "b" / "c.py")
    with pytest.raises(RepositoryScanError) as caught:
        scan_repository(tmp_path, limits=ScanLimits(max_depth=2))
    assert caught.value.code == "SCAN_DEPTH_LIMIT"
    assert not caught.value.location.startswith(str(tmp_path))


def test_manifest_detection_is_broad_and_sorted(tmp_path: Path) -> None:
    write(tmp_path / "requirements-dev.txt", "pytest\n")
    write(tmp_path / "x.csproj", "<Project />\n")
    write(tmp_path / "package-lock.json", "{}\n")
    result = scan_repository(tmp_path)
    assert [(item.path, item.kind) for item in result.manifests] == [
        ("package-lock.json", "node"),
        ("requirements-dev.txt", "python"),
        ("x.csproj", "dotnet"),
    ]


def test_pyproject_dependency_extraction(tmp_path: Path) -> None:
    write(
        tmp_path / "pyproject.toml",
        """
[project]
dependencies = ["requests>=2", "rich[ansi]>=13"]
[project.optional-dependencies]
dev = ["pytest>=8"]
[tool.poetry.dependencies]
python = "^3.11"
httpx = "^0.27"
""".strip(),
    )
    result = scan_repository(tmp_path)
    assert [(item.ecosystem, item.name) for item in result.dependencies] == [
        ("python", "httpx"),
        ("python", "pytest"),
        ("python", "requests"),
        ("python", "rich"),
    ]


def test_package_json_dependency_extraction(tmp_path: Path) -> None:
    write(
        tmp_path / "package.json",
        json.dumps(
            {
                "dependencies": {"react": "19"},
                "devDependencies": {"vite": "7"},
                "peerDependencies": {"react-dom": "19"},
                "optionalDependencies": {"fsevents": "2"},
            }
        ),
    )
    result = scan_repository(tmp_path)
    assert [item.name for item in result.dependencies] == [
        "fsevents",
        "react",
        "react-dom",
        "vite",
    ]


def test_package_json_rejects_duplicate_keys(tmp_path: Path) -> None:
    write(tmp_path / "package.json", '{"dependencies": {}, "dependencies": {}}')
    with pytest.raises(RepositoryScanError) as caught:
        scan_repository(tmp_path)
    assert caught.value.code == "MANIFEST_INVALID"


def test_cargo_dependency_extraction(tmp_path: Path) -> None:
    write(
        tmp_path / "Cargo.toml",
        """
[dependencies]
serde = "1"
[dev-dependencies]
proptest = "1"
[build-dependencies]
cc = "1"
""".strip(),
    )
    result = scan_repository(tmp_path)
    assert [item.name for item in result.dependencies] == ["cc", "proptest", "serde"]


def test_go_mod_dependency_extraction(tmp_path: Path) -> None:
    write(
        tmp_path / "go.mod",
        """
module example.com/demo

go 1.23

require example.com/one v1.0.0
require (
    example.com/two v2.0.0
    example.com/three v3.0.0 // indirect
)
""".strip(),
    )
    result = scan_repository(tmp_path)
    assert [item.name for item in result.dependencies] == [
        "example.com/one",
        "example.com/three",
        "example.com/two",
    ]


def test_semantic_manifest_size_limit_fails(tmp_path: Path) -> None:
    write(tmp_path / "package.json", json.dumps({"dependencies": {"x": "1"}}))
    with pytest.raises(RepositoryScanError) as caught:
        scan_repository(tmp_path, limits=ScanLimits(max_manifest_bytes=5))
    assert caught.value.code == "MANIFEST_TOO_LARGE"
    assert caught.value.location == "package.json"


def test_unparsed_manifest_size_does_not_trigger_semantic_limit(tmp_path: Path) -> None:
    write(tmp_path / "requirements.txt", "x" * 100)
    result = scan_repository(tmp_path, limits=ScanLimits(max_manifest_bytes=5))
    assert result.manifests[0].path == "requirements.txt"


def test_language_signals_are_explicit_and_unknown_files_still_count(tmp_path: Path) -> None:
    write(tmp_path / "a.py")
    write(tmp_path / "b.ts")
    write(tmp_path / "c.rs")
    write(tmp_path / "d.unknown")
    result = scan_repository(tmp_path)
    assert result.file_count == 4
    assert [(item.language, item.file_count) for item in result.languages] == [
        ("Python", 1),
        ("Rust", 1),
        ("TypeScript", 1),
    ]


def test_test_and_config_signals_are_relative(tmp_path: Path) -> None:
    write(tmp_path / "tests" / "test_a.py")
    write(tmp_path / "src" / "thing.spec.ts")
    write(tmp_path / ".github" / "workflows" / "ci.yml")
    write(tmp_path / "Dockerfile")
    write(tmp_path / "ruff.toml")
    result = scan_repository(tmp_path)
    assert result.test_paths == ("src/thing.spec.ts", "tests", "tests/test_a.py")
    assert result.config_paths == (".github/workflows", "Dockerfile", "ruff.toml")


def test_component_signals_are_path_based_only(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "src" / "alpha").mkdir(parents=True)
    (tmp_path / "packages" / "pkg").mkdir(parents=True)
    (tmp_path / "apps" / "web").mkdir(parents=True)
    result = scan_repository(tmp_path)
    assert ("top-level", "docs", "docs") in [
        (item.kind, item.name, item.path) for item in result.components
    ]
    assert ("src-module", "alpha", "src/alpha") in [
        (item.kind, item.name, item.path) for item in result.components
    ]
    assert ("package", "pkg", "packages/pkg") in [
        (item.kind, item.name, item.path) for item in result.components
    ]
    assert ("app", "web", "apps/web") in [
        (item.kind, item.name, item.path) for item in result.components
    ]


def test_git_absent_layout(tmp_path: Path) -> None:
    assert scan_repository(tmp_path).git.to_dict() == {"layout": "none", "present": False}


def test_git_indirect_file_is_not_followed(tmp_path: Path) -> None:
    write(tmp_path / ".git", "gitdir: /outside/secret\n")
    result = scan_repository(tmp_path)
    assert result.git.present is True
    assert result.git.layout == "indirect"
    assert result.git.head_commit is None


def test_git_ordinary_symbolic_head_resolves_loose_ref(tmp_path: Path) -> None:
    commit = "a" * 40
    write(tmp_path / ".git" / "HEAD", "ref: refs/heads/main\n")
    write(tmp_path / ".git" / "refs" / "heads" / "main", commit + "\n")
    result = scan_repository(tmp_path)
    assert result.git.layout == "ordinary"
    assert result.git.head_ref == "refs/heads/main"
    assert result.git.head_commit == commit
    assert result.file_count == 0


def test_git_ordinary_symbolic_head_resolves_packed_ref(tmp_path: Path) -> None:
    commit = "b" * 40
    write(tmp_path / ".git" / "HEAD", "ref: refs/heads/main\n")
    write(tmp_path / ".git" / "packed-refs", f"# pack-refs\n{commit} refs/heads/main\n")
    result = scan_repository(tmp_path)
    assert result.git.head_commit == commit


def test_git_detached_head(tmp_path: Path) -> None:
    commit = "c" * 40
    write(tmp_path / ".git" / "HEAD", commit + "\n")
    assert scan_repository(tmp_path).git.head_commit == commit


def test_output_contains_no_absolute_root_or_timestamps(tmp_path: Path) -> None:
    write(tmp_path / "src" / "a.py")
    payload = json.dumps(scan_repository(tmp_path).to_dict(), sort_keys=True)
    assert str(tmp_path) not in payload
    assert "timestamp" not in payload.lower()
    assert "mtime" not in payload.lower()


def test_scan_does_not_mutate_repository(tmp_path: Path) -> None:
    write(tmp_path / "a.py", "x=1\n")
    before = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*"))
    scan_repository(tmp_path)
    after = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*"))
    assert before == after
