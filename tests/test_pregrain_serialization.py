from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import specgrain.pregrain as pregrain_module
from specgrain import (
    create_draft_spec,
    init_project,
    load_project,
    promote_refining_spec_to_grain,
    refine_shaped_spec,
    shape_draft_spec,
)
from specgrain.store import StoreValidationError


def _shape(root: Path, spec_id: str, marker: str = "writer_a"):
    return shape_draft_spec(
        root,
        spec_id=spec_id,
        scope_in=(f"Implement {marker}",),
        scope_out=("No provider integration",),
        acceptance=(f"{marker} acceptance passes",),
        dependencies=(),
        risk_level="low",
        recovery="Revert the bounded file change.",
        context_budget=2000,
        context_estimate=500,
        change_surface=(f"src/{marker}.py",),
        change_surface_exception=None,
        evidence=(f"{marker}-evidence",),
        minimality_choice="native",
        minimality_rationale="Use the existing native mutation path.",
        safety_status="none-identified",
        safety_requirements=(),
    )


def _draft(root: Path):
    init_project(root, project_id="spec-025-test")
    return create_draft_spec(root, title="Candidate", outcome="Bounded outcome")


def test_competing_supported_writer_fails_closed_while_first_writer_holds_lock(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    draft = _draft(tmp_path)
    real_replace = pregrain_module._replace_spec_exact
    injected = False
    competitor_error: StoreValidationError | None = None

    def replace_with_competitor(path, before_text, after, location):
        nonlocal injected, competitor_error
        if not injected:
            injected = True
            try:
                _shape(tmp_path, draft.id, "writer_b")
            except StoreValidationError as exc:
                competitor_error = exc
            else:  # pragma: no cover - the invariant under test
                raise AssertionError("competing supported writer unexpectedly succeeded")
        return real_replace(path, before_text, after, location)

    monkeypatch.setattr(pregrain_module, "_replace_spec_exact", replace_with_competitor)

    writer_a = _shape(tmp_path, draft.id, "writer_a")

    assert injected is True
    assert competitor_error is not None
    assert competitor_error.location == ".specgrain/tmp/pregrain-mutation.lock"
    assert "already in progress" in competitor_error.detail
    stored = load_project(tmp_path).specs[0]
    assert stored.revision_digest == writer_a.node.revision_digest
    assert stored.scope_in == ("Implement writer_a",)


def test_stale_precomputed_writer_fails_after_lock_owner_commits(tmp_path: Path) -> None:
    draft = _draft(tmp_path)
    stale_project, stale_before = pregrain_module._target(
        tmp_path,
        draft.id,
        pregrain_module.SpecState.DRAFT,
    )
    stale_data = stale_before.to_dict()
    stale_data["scope_in"] = ["Implement stale"]
    stale_data["scope_out"] = ["No provider integration"]
    stale_data["acceptance"] = ["stale acceptance passes"]
    stale_data["risk"] = {"level": "low", "recovery": "Revert stale."}
    stale_data["context"] = {"budget_tokens": 2000, "estimated_tokens": 500}
    stale_data["change_surface"] = ["src/stale.py"]
    stale_data["evidence"] = {"required": ["stale-evidence"]}
    stale_data["metadata"] = {
        **stale_before.metadata,
        "readiness": {
            "version": pregrain_module.GRAIN_READINESS_VERSION,
            "unresolved_decisions": [],
            "minimality": {"choice": "native", "rationale": "Use native."},
            "safety": {"status": "none-identified", "requirements": []},
        },
    }
    stale_data["state"] = "SHAPED"
    stale_after = pregrain_module._node_from_data(
        stale_data,
        f".specgrain/specs/{draft.id}.json",
    )

    winner = _shape(tmp_path, draft.id, "winner")

    with pytest.raises(StoreValidationError, match="spec changed before pre-Grain mutation"):
        pregrain_module._persist(stale_project, stale_before, stale_after)

    assert load_project(tmp_path).specs[0].revision_digest == winner.node.revision_digest


def test_lock_is_released_after_persistence_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    draft = _draft(tmp_path)
    real_replace = pregrain_module._replace_spec_exact

    def fail_replace(*args, **kwargs):
        raise StoreValidationError("pregrain", "synthetic persistence failure")

    monkeypatch.setattr(pregrain_module, "_replace_spec_exact", fail_replace)
    with pytest.raises(StoreValidationError, match="synthetic persistence failure"):
        _shape(tmp_path, draft.id)

    monkeypatch.setattr(pregrain_module, "_replace_spec_exact", real_replace)
    result = _shape(tmp_path, draft.id)
    assert result.node.state == "SHAPED"
    assert (tmp_path / ".specgrain" / "tmp" / "pregrain-mutation.lock").is_file()


def test_persistent_anchor_does_not_block_sequential_shape_refine_grain(tmp_path: Path) -> None:
    draft = _draft(tmp_path)
    shaped = _shape(tmp_path, draft.id)
    refined = refine_shaped_spec(tmp_path, spec_id=draft.id)
    grain = promote_refining_spec_to_grain(tmp_path, spec_id=draft.id)

    assert shaped.node.state == "SHAPED"
    assert refined.node.state == "REFINING"
    assert grain.node.state == "GRAIN"
    assert shaped.node.revision_digest == refined.node.revision_digest == grain.node.revision_digest
    assert (tmp_path / ".specgrain" / "tmp" / "pregrain-mutation.lock").is_file()


def test_refine_and_grain_share_the_same_contention_boundary(tmp_path: Path) -> None:
    draft = _draft(tmp_path)
    _shape(tmp_path, draft.id)

    with (
        pregrain_module._pregrain_mutation_lock(tmp_path),
        pytest.raises(StoreValidationError, match="already in progress"),
    ):
        refine_shaped_spec(tmp_path, spec_id=draft.id)

    refined = refine_shaped_spec(tmp_path, spec_id=draft.id)
    assert refined.node.state == "REFINING"

    with (
        pregrain_module._pregrain_mutation_lock(tmp_path),
        pytest.raises(StoreValidationError, match="already in progress"),
    ):
        promote_refining_spec_to_grain(tmp_path, spec_id=draft.id)

    grain = promote_refining_spec_to_grain(tmp_path, spec_id=draft.id)
    assert grain.node.state == "GRAIN"


def test_non_regular_lock_anchor_fails_closed_before_spec_mutation(tmp_path: Path) -> None:
    draft = _draft(tmp_path)
    lock_path = tmp_path / ".specgrain" / "tmp" / "pregrain-mutation.lock"
    lock_path.parent.mkdir()
    lock_path.mkdir()

    before = (tmp_path / ".specgrain" / "specs" / f"{draft.id}.json").read_bytes()
    with pytest.raises(StoreValidationError, match="regular non-symlink file"):
        _shape(tmp_path, draft.id)
    after = (tmp_path / ".specgrain" / "specs" / f"{draft.id}.json").read_bytes()

    assert after == before


def test_symlink_lock_anchor_fails_closed_without_following_target(tmp_path: Path) -> None:
    draft = _draft(tmp_path)
    lock_path = tmp_path / ".specgrain" / "tmp" / "pregrain-mutation.lock"
    lock_path.parent.mkdir()
    target = tmp_path / "lock-target"
    target.write_bytes(b"sentinel")
    try:
        lock_path.symlink_to(target)
    except OSError as exc:  # pragma: no cover - platform privilege dependent
        pytest.skip(f"symlink creation unavailable: {exc}")

    spec_path = tmp_path / ".specgrain" / "specs" / f"{draft.id}.json"
    spec_before = spec_path.read_bytes()
    target_before = target.read_bytes()

    with pytest.raises(StoreValidationError, match="regular non-symlink file"):
        _shape(tmp_path, draft.id)

    assert spec_path.read_bytes() == spec_before
    assert target.read_bytes() == target_before


def test_process_exit_releases_lock_ownership_and_reads_remain_unlocked(tmp_path: Path) -> None:
    draft = _draft(tmp_path)
    script = (
        "import sys,time; "
        "from specgrain.pregrain import _pregrain_mutation_lock; "
        "cm=_pregrain_mutation_lock(sys.argv[1]); cm.__enter__(); "
        "print('locked', flush=True); time.sleep(30)"
    )
    process = subprocess.Popen(
        [sys.executable, "-c", script, str(tmp_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        assert process.stdout is not None
        assert process.stdout.readline().strip() == "locked"

        # Read-only project loading is outside the serialization boundary.
        assert load_project(tmp_path).specs[0].id == draft.id

        process.terminate()
        process.wait(timeout=10)
        result = _shape(tmp_path, draft.id)
        assert result.node.state == "SHAPED"
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=10)
