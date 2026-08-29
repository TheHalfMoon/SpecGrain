from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_v020_release_workflow_binds_new_publication_to_exact_ci_head() -> None:
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    assert "RELEASE_SHA: ${{ github.event.workflow_run.head_sha }}" in workflow
    assert 'git tag "$RELEASE_TAG" "$RELEASE_SHA"' in workflow
    assert '--target "$RELEASE_SHA"' in workflow
    assert '--title "$RELEASE_TITLE"' in workflow
    assert '--notes-file "$RELEASE_NOTES"' in workflow


def test_v020_release_workflow_is_metadata_derived_and_history_safe() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["version"] == "0.2.0"
    assert data["project"]["dependencies"] == []

    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    for derived in (
        'tag="v${version}"',
        'wheel="specgrain-${version}-py3-none-any.whl"',
        'sdist="specgrain-${version}.tar.gz"',
        'notes="docs/releases/${tag}.md"',
        'title="SpecGrain ${tag}"',
    ):
        assert derived in workflow

    for forbidden in (
        "git tag -f",
        "git push --force",
        "git fetch --tags --force",
        "gh release edit",
        "gh release upload",
        "v0.1.0",
    ):
        assert forbidden not in workflow

    assert "already published at historical tag target" in workflow
    assert "refusing ambiguous partial publication" in workflow
    assert "tag_target" in workflow
    assert 'tag_target" != "$RELEASE_SHA' not in workflow
