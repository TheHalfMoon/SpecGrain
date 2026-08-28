from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_release_metadata_is_versioned_and_runtime_dependency_free() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["version"] == "0.1.0"
    assert data["project"]["dependencies"] == []
    assert data["project"]["requires-python"] == ">=3.11"


def test_permanent_ci_covers_supported_launch_platforms() -> None:
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    for runner in ("ubuntu-latest", "macos-latest", "windows-latest"):
        assert runner in workflow
    for version in ('python: "3.11"', 'python: "3.12"', 'python: "3.13"'):
        assert version in workflow
    assert "python -m pytest" in workflow
    assert "python -m ruff check src tests examples" in workflow
    assert "python -m build" in workflow
    assert "--force-reinstall" in workflow


def test_readme_uses_only_current_cli_commands() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for command in (
        "specgrain init",
        "specgrain check",
        "specgrain next",
        "specgrain scan",
        "specgrain prove",
        "specgrain import-spec-kit",
    ):
        assert command in readme
    for unsupported in ("specgrain ask ", "specgrain packet ", "specgrain verify "):
        assert unsupported not in readme


def test_zero_to_verified_example_executes() -> None:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "examples" / "zero_to_verified.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "Readiness: GRAIN" in completed.stdout
    assert "Verification: VERIFIED" in completed.stdout
    assert "Proof: VERIFIED" in completed.stdout
