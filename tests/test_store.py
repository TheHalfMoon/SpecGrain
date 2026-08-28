from __future__ import annotations

import json
from pathlib import Path

import pytest

import specgrain.store as store_module
from specgrain import (
    POLICY_VERSION,
    STORE_VERSION,
    ReadinessIssueCode,
    ReadinessPolicyMode,
    SpecNode,
    StoreExistsError,
    StoreValidationError,
    check_project,
    init_project,
    load_project,
)


def ready_metadata() -> dict[str, object]:
    return {
        "readiness": {
            "version": 1,
            "unresolved_decisions": [],
            "minimality": {"choice": "new-code", "rationale": "bounded new code"},
            "safety": {"status": "none-identified", "requirements": []},
        }
    }


def spec(num: int = 1, **overrides: object) -> SpecNode:
    values: dict[str, object] = {
        "id": f"SG-{num:06d}",
        "title": f"Node {num}",
        "outcome": f"Outcome {num}",
        "scope_in": ["bounded"],
        "acceptance": ["verified"],
        "risk": {"level": "low", "recovery": "revert"},
        "context": {"budget_tokens": 1000, "estimated_tokens": 500},
        "change_surface": ["src/x.py"],
        "evidence": {"required": ["tests"]},
        "metadata": ready_metadata(),
        "state": "REFINING",
    }
    values.update(overrides)
    return SpecNode(**values)


def write_json(path: Path, value: object) -> None:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")


def write_spec(root: Path, node: SpecNode, *, filename: str | None = None) -> Path:
    path = root / ".specgrain" / "specs" / (filename or f"{node.id}.json")
    write_json(path, node.to_dict())
    return path


def set_policy(root: Path, mode: str) -> None:
    write_json(
        root / ".specgrain" / "policies" / "default.json",
        {"policy_version": POLICY_VERSION, "readiness_mode": mode},
    )


def test_init_creates_exact_v1_surface(tmp_path: Path) -> None:
    project = init_project(tmp_path, project_id="demo")
    assert project.manifest.store_version == STORE_VERSION == 1
    assert project.manifest.project_id == "demo"
    assert project.manifest.policy == "default"
    assert project.policy.readiness_mode is ReadinessPolicyMode.REPORT
    assert project.specs == ()
    paths = sorted(
        path.relative_to(tmp_path).as_posix()
        for path in tmp_path.rglob("*")
        if ".specgrain-init-" not in path.name
    )
    assert paths == [
        ".specgrain",
        ".specgrain/policies",
        ".specgrain/policies/default.json",
        ".specgrain/project.json",
        ".specgrain/specs",
    ]
    assert (tmp_path / ".specgrain" / "project.json").read_text(encoding="utf-8").endswith("\n")


def test_init_uses_valid_root_basename_by_default(tmp_path: Path) -> None:
    root = tmp_path / "demo-project"
    root.mkdir()
    assert init_project(root).manifest.project_id == "demo-project"


def test_init_requires_explicit_id_for_invalid_root_basename(tmp_path: Path) -> None:
    root = tmp_path / "bad name"
    root.mkdir()
    with pytest.raises(StoreValidationError, match="project_id"):
        init_project(root)
    assert not (root / ".specgrain").exists()


@pytest.mark.parametrize("project_id", ["", " bad", "a/b", "a" * 65, "é"])
def test_init_rejects_unsafe_project_id(tmp_path: Path, project_id: str) -> None:
    with pytest.raises(StoreValidationError):
        init_project(tmp_path, project_id=project_id)


def test_init_refuses_existing_store_without_overwrite(tmp_path: Path) -> None:
    store = tmp_path / ".specgrain"
    store.mkdir()
    marker = store / "keep.txt"
    marker.write_text("keep", encoding="utf-8")
    with pytest.raises(StoreExistsError):
        init_project(tmp_path, project_id="demo")
    assert marker.read_text(encoding="utf-8") == "keep"


def test_init_cleans_staging_on_write_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(*args: object, **kwargs: object) -> None:
        raise OSError("synthetic")

    monkeypatch.setattr(store_module, "_write_json", fail)
    with pytest.raises(OSError, match="synthetic"):
        init_project(tmp_path, project_id="demo")
    assert not (tmp_path / ".specgrain").exists()
    assert not list(tmp_path.glob(".specgrain-init-*"))


def test_load_valid_project_and_specs_are_sorted(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    write_spec(tmp_path, spec(2))
    write_spec(tmp_path, spec(1))
    project = load_project(tmp_path)
    assert [node.id for node in project.specs] == ["SG-000001", "SG-000002"]


def test_spec_filename_must_be_canonical_id(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    write_spec(tmp_path, spec(1), filename="bad.json")
    with pytest.raises(StoreValidationError, match="filename"):
        load_project(tmp_path)


def test_spec_filename_must_match_content_id(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    write_spec(tmp_path, spec(2), filename="SG-000001.json")
    with pytest.raises(StoreValidationError, match="does not match"):
        load_project(tmp_path)


@pytest.mark.parametrize(
    "text, expected",
    [
        ('{"store_version":1,"store_version":1,"project_id":"x","policy":"default"}', "duplicate"),
        ('{"store_version":NaN,"project_id":"x","policy":"default"}', "non-finite"),
        ('[]', "top-level"),
        ('{', "invalid JSON"),
    ],
)
def test_manifest_strict_json_failures(tmp_path: Path, text: str, expected: str) -> None:
    init_project(tmp_path, project_id="demo")
    (tmp_path / ".specgrain" / "project.json").write_text(text, encoding="utf-8")
    with pytest.raises(StoreValidationError, match=expected):
        load_project(tmp_path)


def test_manifest_invalid_utf8_is_rejected(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    (tmp_path / ".specgrain" / "project.json").write_bytes(b"\xff")
    with pytest.raises(StoreValidationError, match="UTF-8"):
        load_project(tmp_path)


@pytest.mark.parametrize(
    "manifest, expected",
    [
        ({"store_version": True, "project_id": "demo", "policy": "default"}, "store_version"),
        ({"store_version": 2, "project_id": "demo", "policy": "default"}, "store_version"),
        ({"store_version": 1, "project_id": "demo", "policy": "../x"}, "policy"),
        ({"store_version": 1, "project_id": "demo", "policy": "default", "extra": 1}, "unknown"),
    ],
)
def test_manifest_contract_is_strict(
    tmp_path: Path, manifest: dict[str, object], expected: str
) -> None:
    init_project(tmp_path, project_id="demo")
    write_json(tmp_path / ".specgrain" / "project.json", manifest)
    with pytest.raises(StoreValidationError, match=expected):
        load_project(tmp_path)


@pytest.mark.parametrize(
    "policy, expected",
    [
        ({"policy_version": True, "readiness_mode": "report"}, "policy_version"),
        ({"policy_version": 2, "readiness_mode": "report"}, "policy_version"),
        ({"policy_version": 1, "readiness_mode": "magic"}, "readiness_mode"),
        ({"policy_version": 1, "readiness_mode": "report", "extra": 1}, "unknown"),
    ],
)
def test_policy_contract_is_strict(
    tmp_path: Path, policy: dict[str, object], expected: str
) -> None:
    init_project(tmp_path, project_id="demo")
    write_json(tmp_path / ".specgrain" / "policies" / "default.json", policy)
    with pytest.raises(StoreValidationError, match=expected):
        load_project(tmp_path)


def test_nested_duplicate_key_in_spec_is_rejected(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    text = json.dumps(spec().to_dict())
    text = text.replace('"risk": {', '"risk": {"level":"low",')
    (tmp_path / ".specgrain" / "specs" / "SG-000001.json").write_text(text, encoding="utf-8")
    with pytest.raises(StoreValidationError, match="duplicate object key 'level'"):
        load_project(tmp_path)


def test_model_validation_error_is_path_qualified(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    data = spec().to_dict()
    data["state"] = "UNKNOWN"
    write_json(tmp_path / ".specgrain" / "specs" / "SG-000001.json", data)
    with pytest.raises(StoreValidationError, match="invalid SpecNode"):
        load_project(tmp_path)


def test_check_empty_project_passes(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    result = check_project(tmp_path)
    assert result.valid
    assert result.spec_count == result.root_count == 0
    assert result.refining_leaf_count == result.grain_ready_count == 0
    assert result.readiness_blocked == result.issues == ()


def test_check_valid_multi_root_forest_is_deterministic(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    write_spec(tmp_path, spec(2))
    write_spec(tmp_path, spec(1))
    result = check_project(tmp_path)
    assert result.valid
    assert result.root_count == 2
    assert result.refining_leaf_count == result.grain_ready_count == 2
    assert result.to_dict() == check_project(tmp_path).to_dict()


def test_check_invalid_refinement_fails_with_structured_issue(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    write_spec(tmp_path, spec(1, children=["SG-000099"]))
    result = check_project(tmp_path)
    assert not result.valid
    assert result.root_count is None
    assert result.issues[0].code == "MISSING_CHILD"
    assert result.readiness_blocked == ()


def test_report_mode_reports_readiness_blocker_without_failing(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    write_spec(tmp_path, spec(1, acceptance=[]))
    result = check_project(tmp_path)
    assert result.valid
    assert result.refining_leaf_count == 1
    assert result.grain_ready_count == 0
    assert len(result.readiness_blocked) == 1
    assert ReadinessIssueCode.ACCEPTANCE_REQUIRED in {
        issue.code for issue in result.readiness_blocked[0].issues
    }


def test_enforce_mode_fails_on_readiness_blocker(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    set_policy(tmp_path, "enforce")
    write_spec(tmp_path, spec(1, acceptance=[]))
    result = check_project(tmp_path)
    assert not result.valid
    assert result.readiness_mode is ReadinessPolicyMode.ENFORCE
    assert len(result.readiness_blocked) == 1


def test_enforce_mode_passes_ready_refining_leaf(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    set_policy(tmp_path, "enforce")
    write_spec(tmp_path, spec())
    result = check_project(tmp_path)
    assert result.valid
    assert result.grain_ready_count == 1


def test_check_does_not_reauthorize_later_state_nodes(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    write_spec(tmp_path, spec(state="GRAIN", acceptance=[]))
    result = check_project(tmp_path)
    assert result.valid
    assert result.refining_leaf_count == 0
    assert result.readiness_blocked == ()


def test_check_invalid_store_returns_structured_failure(tmp_path: Path) -> None:
    result = check_project(tmp_path)
    assert not result.valid
    assert result.project_id is None
    assert result.issues[0].code == "STORE_INVALID"


def test_check_is_read_only(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    write_spec(tmp_path, spec())
    before = {
        path.relative_to(tmp_path).as_posix(): path.read_bytes()
        for path in (tmp_path / ".specgrain").rglob("*")
        if path.is_file()
    }
    check_project(tmp_path)
    after = {
        path.relative_to(tmp_path).as_posix(): path.read_bytes()
        for path in (tmp_path / ".specgrain").rglob("*")
        if path.is_file()
    }
    assert after == before


def test_non_json_non_symlink_entries_are_ignored(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    (tmp_path / ".specgrain" / "specs" / "README.txt").write_text("notes", encoding="utf-8")
    assert load_project(tmp_path).specs == ()


def test_symlinked_store_component_is_rejected(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    link = tmp_path / ".specgrain"
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises(StoreValidationError, match="symlink"):
        load_project(tmp_path)


def test_symlinked_spec_file_is_rejected(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    outside = tmp_path / "outside.json"
    write_json(outside, spec().to_dict())
    link = tmp_path / ".specgrain" / "specs" / "SG-000001.json"
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises(StoreValidationError, match="symlink"):
        load_project(tmp_path)


def test_repository_root_symlink_is_rejected(tmp_path: Path) -> None:
    target = tmp_path / "target-root"
    target.mkdir()
    link = tmp_path / "root-link"
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises(StoreValidationError, match="root symlink"):
        init_project(link, project_id="demo")


def test_symlinked_project_manifest_is_rejected(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    manifest = tmp_path / ".specgrain" / "project.json"
    outside = tmp_path / "outside-project.json"
    outside.write_bytes(manifest.read_bytes())
    manifest.unlink()
    try:
        manifest.symlink_to(outside)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises(StoreValidationError, match="symlink"):
        load_project(tmp_path)


def test_symlinked_active_policy_is_rejected(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    policy = tmp_path / ".specgrain" / "policies" / "default.json"
    outside = tmp_path / "outside-policy.json"
    outside.write_bytes(policy.read_bytes())
    policy.unlink()
    try:
        policy.symlink_to(outside)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises(StoreValidationError, match="symlink"):
        load_project(tmp_path)


def test_symlinked_specs_directory_is_rejected(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    specs = tmp_path / ".specgrain" / "specs"
    specs.rmdir()
    outside = tmp_path / "outside-specs"
    outside.mkdir()
    try:
        specs.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises(StoreValidationError, match="symlink"):
        load_project(tmp_path)
