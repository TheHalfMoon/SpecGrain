from __future__ import annotations

import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_release_metadata_is_versioned_and_runtime_dependency_free() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["version"] == "0.3.0"
    assert data["project"]["dependencies"] == []
    assert data["project"]["requires-python"] == ">=3.11"
    assert data["project"]["license"] == "MIT"
    assert data["project"]["license-files"] == ["LICENSE"]
    assert data["build-system"]["requires"] == ["setuptools>=77"]
    assert "ruff==0.6.9" in data["project"]["optional-dependencies"]["dev"]


def test_permanent_ci_covers_supported_launch_platforms() -> None:
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    for runner in ("ubuntu-latest", "macos-latest", "windows-latest"):
        assert runner in workflow
    for version in ('python: "3.11"', 'python: "3.12"', 'python: "3.13"'):
        assert version in workflow
    for command in (
        'python -m pip install "pytest>=8.0" "ruff==0.6.9" build',
        "python -m ruff check src",
        "python -m ruff check tests",
        "python -m ruff check examples",
        "python -m pip install -e . --no-deps",
        "python -m pytest",
        "git diff --exit-code",
        "python -m build",
        "--force-reinstall",
    ):
        assert command in workflow
    assert "actions/checkout@v7" in workflow
    assert "actions/setup-python@v7" in workflow
    assert "actions/checkout@v4" not in workflow
    assert "actions/setup-python@v5" not in workflow
    assert workflow.index("python -m ruff check src") < workflow.index(
        "python -m pip install -e . --no-deps"
    )


def test_release_workflow_is_metadata_derived_monotonic_and_installable() -> None:
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    assert "workflow_run" in workflow
    assert "head_branch == 'main'" in workflow
    assert "workflow_run.conclusion == 'success'" in workflow
    assert "actions/checkout@v7" in workflow
    assert "actions/setup-python@v7" in workflow
    assert "actions/checkout@v4" not in workflow
    assert "actions/setup-python@v5" not in workflow
    assert "RELEASE_SHA: ${{ github.event.workflow_run.head_sha }}" in workflow
    assert 'version=data["project"]["version"]' in workflow
    assert 'tag="v${version}"' in workflow
    assert 'wheel="specgrain-${version}-py3-none-any.whl"' in workflow
    assert 'sdist="specgrain-${version}.tar.gz"' in workflow
    assert 'notes="docs/releases/${tag}.md"' in workflow
    assert 'title="SpecGrain ${tag}"' in workflow
    assert "python -m build" in workflow
    assert 'git tag "$RELEASE_TAG" "$RELEASE_SHA"' in workflow
    assert 'git push origin "refs/tags/$RELEASE_TAG"' in workflow
    assert 'gh release create "$RELEASE_TAG"' in workflow
    assert "--verify-tag" in workflow
    assert "--json tagName,name,isDraft,isPrerelease" in workflow
    assert "already published at historical tag target" in workflow
    assert "refusing ambiguous partial publication" in workflow
    assert "git fetch --tags --force" not in workflow
    assert "git tag -f" not in workflow
    assert "git push --force" not in workflow
    assert "gh release edit" not in workflow
    assert "gh release upload" not in workflow
    assert "v0.1.0" not in workflow
    assert "v0.2.0" not in workflow
    assert "v0.3.0" not in workflow


def test_readme_uses_only_current_cli_commands() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for command in (
        "specgrain init",
        "specgrain draft",
        "specgrain recover",
        "specgrain check",
        "specgrain next",
        "specgrain scan",
        "specgrain prove",
        "specgrain import-spec-kit",
    ):
        assert command in readme
    for unsupported in ("specgrain ask ", "specgrain packet ", "specgrain verify "):
        assert unsupported not in readme
    assert "refs/tags/v0.3.0.zip" in readme
    assert "v0.3.0 versioned release contains every command in the table" in readme
    assert "do not promote lifecycle state" in readme


def test_readme_first_screen_states_current_public_contract() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "agent-neutral delivery control plane" in readme
    assert "Current release:** `v0.3.0`" in readme
    assert "Python:** `3.11+`" in readme
    assert "License:** MIT" in readme
    assert "Runtime dependencies:** zero" in readme
    assert "actions/workflows/ci.yml/badge.svg" in readme


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
        "LICENSE",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        "CHANGELOG.md",
        "examples/brownfield/README.md",
        "docs/migration-from-spec-kit.md",
        "docs/benchmark-report-v0.1.0.md",
        "docs/trust-model.md",
        "docs/releases/v0.1.0.md",
        "docs/releases/v0.2.0.md",
        "docs/releases/v0.3.0.md",
        "docs/assets/terminal-demo.svg",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/feature_request.md",
        ".github/pull_request_template.md",
    )
    for relative in required:
        assert (ROOT / relative).is_file(), relative


def test_security_policy_tracks_current_release_line() -> None:
    policy = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    assert "| 0.3.x | Supported |" in policy
    assert "| < 0.3 | Not supported |" in policy
    assert "| 0.1.x | Supported |" not in policy
    assert "historical evidence anchors" in policy


def test_launch_strategy_tracks_current_release() -> None:
    strategy = (ROOT / "docs" / "launch-strategy.md").read_text(encoding="utf-8")
    assert "## Current v0.3.0 launch demo" in strategy
    assert "refs/tags/v0.3.0.zip" in strategy
    assert "v0.1.0 launch demo" not in strategy
    for command in ("specgrain init", "specgrain draft", "specgrain check"):
        assert command in strategy


def test_v020_release_notes_preserve_authoring_and_trust_boundaries() -> None:
    notes = (ROOT / "docs" / "releases" / "v0.2.0.md").read_text(encoding="utf-8")
    assert "specgrain draft" in notes
    assert "create_draft_spec" in notes
    assert "Recursive child refinement remains outside" in notes
    assert "No PyPI" in notes
    assert "no benchmark winner is claimed" in notes
    assert "Runtime third-party dependency count remains zero" in notes


def test_v030_release_notes_preserve_recursive_authoring_and_trust_boundaries() -> None:
    notes = (ROOT / "docs" / "releases" / "v0.3.0.md").read_text(encoding="utf-8")
    assert "create_child_draft_spec" in notes
    assert "specgrain recover" in notes
    assert "does not change `src/specgrain/` product behavior" in notes
    assert "No PyPI" in notes
    assert "no benchmark winner is claimed" in notes
    assert "Runtime third-party dependency count remains zero" in notes


def test_changelog_promotes_v030_and_restores_unreleased_boundary() -> None:
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [0.3.0] — 2026-08-29" in changelog
    assert "## [0.2.0] — 2026-08-29" in changelog
    assert changelog.index("## Unreleased") < changelog.index("## [0.3.0]")
    assert changelog.index("## [0.3.0]") < changelog.index("## [0.2.0]")
    assert "_No changes recorded yet._" in changelog
    assert "create_child_draft_spec" in changelog
    assert "specgrain recover" in changelog
    assert "Specification 020 changes no `src/specgrain/` product behavior" in changelog


def test_python_release_surface_respects_line_length() -> None:
    violations: list[str] = []
    for root_name in ("src", "tests", "examples"):
        for path in sorted((ROOT / root_name).rglob("*.py")):
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if len(line) > 100:
                    violations.append(f"{path.relative_to(ROOT)}:{line_number}:{len(line)}")
    assert violations == []


def test_public_launch_relative_markdown_links_resolve() -> None:
    docs = (
        ROOT / "README.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "SECURITY.md",
        ROOT / "docs" / "launch-strategy.md",
        ROOT / "docs" / "migration-from-spec-kit.md",
        ROOT / "docs" / "benchmark-report-v0.1.0.md",
        ROOT / "docs" / "trust-model.md",
        ROOT / "docs" / "releases" / "v0.1.0.md",
        ROOT / "docs" / "releases" / "v0.2.0.md",
        ROOT / "docs" / "releases" / "v0.3.0.md",
        ROOT / "examples" / "brownfield" / "README.md",
    )
    broken: list[str] = []
    for document in docs:
        text = document.read_text(encoding="utf-8")
        for raw_target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = raw_target.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            if not (document.parent / target).resolve().exists():
                broken.append(f"{document.relative_to(ROOT)} -> {raw_target}")
    assert broken == []


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
