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
    for command in (
        "python -m ruff check src",
        "python -m ruff check tests --exclude test_launch.py",
        "python -m ruff check tests/test_launch.py",
        "python -m ruff check examples/zero_to_verified.py",
        "python -m pytest",
        "git diff --exit-code",
        "python -m build",
        "--force-reinstall",
    ):
        assert command in workflow


def test_release_workflow_is_post_ci_and_immutable() -> None:
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    assert "workflow_run" in workflow
    assert "head_branch == 'main'" in workflow
    assert "workflow_run.conclusion == 'success'" in workflow
    assert "RELEASE_SHA: ${{ github.event.workflow_run.head_sha }}" in workflow
    assert "git tag v0.1.0 \"$RELEASE_SHA\"" in workflow
    assert "git push origin refs/tags/v0.1.0" in workflow
    assert "gh release create v0.1.0" in workflow
    assert "--verify-tag" in workflow


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


def test_public_launch_surface_is_present() -> None:
    required = (
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        "CHANGELOG.md",
        "examples/brownfield/README.md",
        "docs/migration-from-spec-kit.md",
        "docs/benchmark-report-v0.1.0.md",
        "docs/trust-model.md",
        "docs/releases/v0.1.0.md",
        "docs/assets/terminal-demo.svg",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/feature_request.md",
        ".github/pull_request_template.md",
    )
    for relative in required:
        assert (ROOT / relative).is_file(), relative


def test_brownfield_examples_are_pinned_without_fake_output() -> None:
    text = (ROOT / "examples" / "brownfield" / "README.md").read_text(encoding="utf-8")
    for revision in (
        "672971d66a2ef9f85151e53283113f33d642dabd",
        "22dda61ea29037ba85af25e84bc5efba77e62f44",
        "5a82625fae462e8ba64cec8146b24a372b4d75c6",
    ):
        assert revision in text
    assert "does not publish precomputed scan output" in text


def test_benchmark_report_declares_no_empirical_winner() -> None:
    report = (ROOT / "docs" / "benchmark-report-v0.1.0.md").read_text(encoding="utf-8")
    assert "Empirical comparative dataset:** not yet published" in report
    assert "Declared winner:** none" in report
    assert "no fabricated" in report


def test_spec_kit_guide_keeps_legacy_tasks_out_of_core() -> None:
    guide = (ROOT / "docs" / "migration-from-spec-kit.md").read_text(encoding="utf-8")
    assert "tasks_promoted_to_core` value is always false" in guide
    assert "does not write `.specgrain/` state" in guide
