from __future__ import annotations

import json
from pathlib import Path

from specgrain.cli import main

SPEC = """# Feature Specification: CLI Import

**Feature Branch**: `013-cli-import`

**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Inspect migration (Priority: P1)

**Independent Test**: Run the importer and inspect the deterministic report.

## Requirements

### Functional Requirements

- **FR-001**: System MUST produce a migration report without modifying source files.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Repeated imports of identical bytes produce the same digest.
"""


def feature(tmp_path: Path) -> Path:
    root = tmp_path / "feature"
    root.mkdir()
    (root / "spec.md").write_text(SPEC, encoding="utf-8")
    return root


def test_import_spec_kit_cli_json_is_deterministic_and_read_only(
    tmp_path: Path, capsys
) -> None:
    root = feature(tmp_path)
    before = (root / "spec.md").read_bytes()
    assert main(["import-spec-kit", str(root), "--source-revision", "rev-1", "--json"]) == 0
    first = capsys.readouterr()
    assert first.err == ""
    payload = json.loads(first.out)
    assert payload["feature_name"] == "CLI Import"
    assert payload["tasks_promoted_to_core"] is False
    assert payload["digest"].startswith("sha256:")
    assert main(["import-spec-kit", str(root), "--source-revision", "rev-1", "--json"]) == 0
    second = capsys.readouterr()
    assert second.out == first.out
    assert (root / "spec.md").read_bytes() == before
    assert not (tmp_path / ".specgrain").exists()


def test_import_spec_kit_cli_text_summary(tmp_path: Path, capsys) -> None:
    root = feature(tmp_path)
    assert main(["import-spec-kit", str(root), "--source-revision", "rev-1"]) == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    assert "SpecGrain import-spec-kit: PASS" in captured.out
    assert "Feature: CLI Import" in captured.out
    assert "Legacy tasks promoted to core: false" in captured.out


def test_import_spec_kit_cli_failure_is_stable(tmp_path: Path, capsys) -> None:
    root = tmp_path / "missing"
    assert main(["import-spec-kit", str(root), "--source-revision", "rev-1", "--json"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    payload = json.loads(captured.err)
    assert payload["valid"] is False
    assert "ordinary directory" in payload["error"]
