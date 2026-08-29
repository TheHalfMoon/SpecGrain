from __future__ import annotations

import json
from pathlib import Path

import pytest

from specgrain.speckit import (
    SPECKIT_IMPORT_VERSION,
    SpecKitImportError,
    import_spec_kit_artifacts,
    load_spec_kit_feature,
)

SPEC = """# Feature Specification: Search Workspace

**Feature Branch**: `013-search-workspace`

**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Search saved work (Priority: P1)

**Independent Test**: Create two saved items and find one by exact title.

### User Story 2 - Filter results (Priority: P2)

**Independent Test**: Filter a mixed result set to one content type.

## Requirements

### Functional Requirements

- **FR-001**: System MUST search saved work.
- **FR-002**: System MUST filter results by type.

## Success Criteria

### Measurable Outcomes

- **SC-001**: A saved item can be found by exact title.

## Assumptions

- Existing local storage remains authoritative.
- No remote service is required.
"""

PLAN = """# Implementation Plan: Search Workspace

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: None
**Testing**: pytest
**Target Platform**: Local CLI
**Constraints**: Offline-capable

## Constitution Check

No governance exception is required.
"""

TASKS = """# Tasks: Search Workspace

- [x] T001 [P] [US1] Add search index fixture
- [ ] T002 [US1] Implement exact title search
- [ ] T003 [US2] Implement type filter
"""

CONSTITUTION = """# Demo Constitution

## Core Principles

### I. Local First
All feature behavior works offline.
"""


def bundle() -> dict[str, str]:
    return {
        ".specify/memory/constitution.md": CONSTITUTION,
        "specs/013-search/spec.md": SPEC,
        "specs/013-search/plan.md": PLAN,
        "specs/013-search/tasks.md": TASKS,
    }


def test_import_version_and_deterministic_digest() -> None:
    first = import_spec_kit_artifacts(bundle(), source_revision="abc123")
    second = import_spec_kit_artifacts(
        dict(reversed(list(bundle().items()))), source_revision="abc123"
    )
    assert SPECKIT_IMPORT_VERSION == 1
    assert first.to_dict() == second.to_dict()
    assert first.digest == second.digest


def test_import_extracts_independent_testability_and_requirements() -> None:
    report = import_spec_kit_artifacts(bundle(), source_revision="abc123")
    assert report.feature_name == "Search Workspace"
    assert report.feature_branch == "013-search-workspace"
    assert report.status == "Draft"
    assert [(story.title, story.priority) for story in report.stories] == [
        ("Search saved work", "P1"),
        ("Filter results", "P2"),
    ]
    assert report.stories[0].independent_test.startswith("Create two saved items")
    assert [item.item_id for item in report.functional_requirements] == ["FR-001", "FR-002"]
    assert [item.item_id for item in report.success_criteria] == ["SC-001"]


def test_import_preserves_technical_context_constitution_and_legacy_tasks() -> None:
    report = import_spec_kit_artifacts(bundle(), source_revision="abc123")
    assert ("Language/Version", "Python 3.11") in [
        (item.name, item.value) for item in report.technical_context
    ]
    assert report.constitution_checks == ("No governance exception is required.",)
    assert len(report.source_artifacts) == 4
    assert len(report.legacy_tasks) == 3
    assert report.legacy_tasks[0].parallel is True
    assert report.legacy_tasks[0].story_id == "US1"
    assert report.tasks_promoted_to_core is False
    assert {notice.code for notice in report.notices} >= {
        "CONSTITUTION_SOURCE_BOUND",
        "LEGACY_TASKS_PRESERVED_NOT_CORE",
    }


def test_import_report_is_json_serializable_without_source_text_copy() -> None:
    report = import_spec_kit_artifacts(bundle(), source_revision="abc123")
    encoded = json.dumps(report.to_dict(), sort_keys=True)
    assert "System MUST search saved work" in encoded
    assert "All feature behavior works offline" not in encoded
    assert all(item.content_digest.startswith("sha256:") for item in report.source_artifacts)


def test_missing_spec_and_ambiguous_roles_fail_closed() -> None:
    with pytest.raises(SpecKitImportError, match="spec.md is required"):
        import_spec_kit_artifacts({"plan.md": PLAN}, source_revision="abc")
    with pytest.raises(SpecKitImportError, match="multiple artifacts"):
        import_spec_kit_artifacts(
            {"a/spec.md": SPEC, "b/spec.md": SPEC}, source_revision="abc"
        )


def test_unknown_artifact_and_bad_paths_fail_closed() -> None:
    with pytest.raises(SpecKitImportError, match="unsupported"):
        import_spec_kit_artifacts({"spec.md": SPEC, "research.md": "x"}, source_revision="abc")
    with pytest.raises(SpecKitImportError, match="normalized"):
        import_spec_kit_artifacts({"../spec.md": SPEC}, source_revision="abc")


def test_unresolved_feature_and_independent_test_placeholders_fail() -> None:
    with pytest.raises(SpecKitImportError, match="feature-name placeholder"):
        import_spec_kit_artifacts(
            {"spec.md": SPEC.replace("Search Workspace", "[FEATURE NAME]", 1)},
            source_revision="abc",
        )
    with pytest.raises(SpecKitImportError, match="Independent Test"):
        import_spec_kit_artifacts(
            {
                "spec.md": SPEC.replace(
                    "Create two saved items and find one by exact title.", "[Describe test]"
                )
            },
            source_revision="abc",
        )


def test_template_comments_do_not_create_false_placeholder_failure() -> None:
    source = SPEC + "\n<!-- ACTION REQUIRED: [placeholder example] -->\n"
    report = import_spec_kit_artifacts({"spec.md": source}, source_revision="abc")
    assert report.feature_name == "Search Workspace"


def test_duplicate_requirement_and_task_ids_fail_closed() -> None:
    with pytest.raises(SpecKitImportError, match="duplicate FR-001"):
        import_spec_kit_artifacts(
            {"spec.md": SPEC.replace("- **FR-002**", "- **FR-001**")},
            source_revision="abc",
        )
    with pytest.raises(SpecKitImportError, match="duplicate legacy task"):
        import_spec_kit_artifacts(
            {"spec.md": SPEC, "tasks.md": TASKS.replace("T002", "T001")},
            source_revision="abc",
        )


def test_direct_import_enforces_artifact_size_limit() -> None:
    with pytest.raises(SpecKitImportError, match="exceeds"):
        import_spec_kit_artifacts(
            {"spec.md": SPEC},
            source_revision="abc",
            max_artifact_bytes=10,
        )


def test_load_feature_reads_only_known_regular_bounded_files(tmp_path: Path) -> None:
    feature = tmp_path / "specs" / "013-search"
    feature.mkdir(parents=True)
    (feature / "spec.md").write_text(SPEC, encoding="utf-8")
    (feature / "plan.md").write_text(PLAN, encoding="utf-8")
    (feature / "tasks.md").write_text(TASKS, encoding="utf-8")
    constitution = tmp_path / "constitution.md"
    constitution.write_text(CONSTITUTION, encoding="utf-8")
    report = load_spec_kit_feature(
        feature,
        source_revision="rev-1",
        constitution_path=constitution,
    )
    assert report.source_revision == "rev-1"
    assert {item.role for item in report.source_artifacts} == {
        "constitution", "plan", "spec", "tasks"
    }


def test_loader_rejects_symlink_and_oversize(tmp_path: Path) -> None:
    feature = tmp_path / "feature"
    feature.mkdir()
    outside = tmp_path / "outside.md"
    outside.write_text(SPEC, encoding="utf-8")
    try:
        (feature / "spec.md").symlink_to(outside)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises(SpecKitImportError, match="ordinary file"):
        load_spec_kit_feature(feature, source_revision="rev")

    (feature / "spec.md").unlink()
    (feature / "spec.md").write_text(SPEC, encoding="utf-8")
    with pytest.raises(SpecKitImportError, match="exceeds"):
        load_spec_kit_feature(feature, source_revision="rev", max_artifact_bytes=10)


def test_loader_rejects_non_utf8_and_invalid_limit(tmp_path: Path) -> None:
    feature = tmp_path / "feature"
    feature.mkdir()
    (feature / "spec.md").write_bytes(b"\xff\xfe")
    with pytest.raises(SpecKitImportError, match="UTF-8"):
        load_spec_kit_feature(feature, source_revision="rev")
    with pytest.raises(SpecKitImportError, match="positive integer"):
        load_spec_kit_feature(feature, source_revision="rev", max_artifact_bytes=0)
