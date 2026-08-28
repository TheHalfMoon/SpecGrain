from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

import specgrain.verification as verification_module
from specgrain import init_project
from specgrain.context import ContextBudgetPolicy, ContextSource, evaluate_context_budget
from specgrain.model import SpecNode
from specgrain.packet import ExecutionResult, WorkPacket, build_work_packet
from specgrain.verification import (
    EVIDENCE_RECORD_VERSION,
    MAX_EVIDENCE_RECORD_BYTES,
    VERIFICATION_VERSION,
    CheckEvidence,
    EvidenceRecord,
    ProofResult,
    VerificationError,
    VerificationIssueCode,
    VerificationReport,
    append_verification_report,
    load_proof,
    verify_execution,
)


def node(**overrides: object) -> SpecNode:
    values: dict[str, object] = {
        "id": "SG-000010",
        "title": "Verification",
        "outcome": "Independent evidence can prove a change.",
        "scope_in": ["verification"],
        "scope_out": ["executor authority"],
        "acceptance": ["acceptance-a", "acceptance-b"],
        "dependencies": ["SG-000009"],
        "risk": {"level": "medium", "recovery": "discard evidence candidate"},
        "change_surface": ["src/specgrain/verification.py", "tests"],
        "evidence": {"required": ["tests", "diff"]},
        "method": "quick",
        "state": "GRAIN",
    }
    values.update(overrides)
    return SpecNode(**values)


def context_source() -> ContextSource:
    return ContextSource(
        source_id="repo",
        provenance="repository-map:demo",
        selection_reason="verification context",
        revision="sha256:" + "a" * 64,
        size_bytes=10,
        token_cost=5,
    )


def packet(n: SpecNode | None = None) -> WorkPacket:
    active = n or node()
    source = context_source()
    report = evaluate_context_budget((source,), ContextBudgetPolicy(max_tokens=100))
    return build_work_packet(active, (source,), report)


def result(p: WorkPacket, **overrides: object) -> ExecutionResult:
    values: dict[str, object] = {
        "packet_digest": p.packet_digest,
        "status": "succeeded",
        "summary": "implemented",
        "changed_paths": ["src/specgrain/verification.py"],
        "reported_evidence": ["self-report:tests"],
    }
    values.update(overrides)
    return ExecutionResult(**values)


def passing_checks() -> tuple[list[CheckEvidence], list[CheckEvidence]]:
    acceptance = [
        CheckEvidence("acceptance-a", True, "test:acceptance-a"),
        CheckEvidence("acceptance-b", True, "test:acceptance-b"),
    ]
    evidence = [
        CheckEvidence("tests", True, "pytest:403"),
        CheckEvidence("diff", True, "git:diff"),
    ]
    return acceptance, evidence


def verified_report() -> VerificationReport:
    n = node()
    p = packet(n)
    r = result(p)
    acceptance, evidence = passing_checks()
    return verify_execution(
        n,
        p,
        r,
        implementation_revision="git:abc123",
        observed_changed_paths=["src/specgrain/verification.py"],
        acceptance_checks=acceptance,
        evidence_checks=evidence,
    )


def write_record(path: Path, record: EvidenceRecord, *, filename: str | None = None) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    target = path / (filename or record.record_digest[7:] + ".json")
    target.write_text(json.dumps(record.to_dict()), encoding="utf-8")
    return target


def test_check_evidence_is_frozen_and_validated() -> None:
    check = CheckEvidence("tests", True, "pytest:1")
    with pytest.raises(FrozenInstanceError):
        check.check_id = "other"  # type: ignore[misc]
    with pytest.raises(VerificationError, match="check_id"):
        CheckEvidence("", True, "pytest:1")
    with pytest.raises(VerificationError, match="passed"):
        CheckEvidence("tests", 1, "pytest:1")  # type: ignore[arg-type]


def test_verified_report_binds_exact_revisions_and_digests() -> None:
    report = verified_report()
    assert report.verification_version == VERIFICATION_VERSION
    assert report.verified is True
    assert report.spec_id == "SG-000010"
    assert report.spec_revision.startswith("sha256:")
    assert report.packet_digest.startswith("sha256:")
    assert report.result_digest.startswith("sha256:")
    assert report.implementation_revision == "git:abc123"


def test_executor_success_alone_cannot_verify() -> None:
    n = node(acceptance=[], evidence={"required": []})
    p = packet(n)
    report = verify_execution(
        n,
        p,
        result(p),
        implementation_revision="git:a",
        observed_changed_paths=["src/specgrain/verification.py"],
        acceptance_checks=[],
        evidence_checks=[],
    )
    assert report.verified is False
    assert [issue.code for issue in report.issues] == [
        VerificationIssueCode.INDEPENDENT_CHECK_MISSING
    ]


def test_spec_revision_mismatch_blocks() -> None:
    original = node(outcome="original")
    current = node(outcome="changed")
    p = packet(original)
    acceptance, evidence = passing_checks()
    report = verify_execution(
        current,
        p,
        result(p),
        implementation_revision="git:a",
        observed_changed_paths=["src/specgrain/verification.py"],
        acceptance_checks=acceptance,
        evidence_checks=evidence,
    )
    assert VerificationIssueCode.SPEC_REVISION_MISMATCH in {
        issue.code for issue in report.issues
    }


def test_result_packet_mismatch_blocks() -> None:
    n = node()
    p = packet(n)
    r = result(p, packet_digest="sha256:" + "f" * 64)
    acceptance, evidence = passing_checks()
    report = verify_execution(
        n,
        p,
        r,
        implementation_revision="git:a",
        observed_changed_paths=["src/specgrain/verification.py"],
        acceptance_checks=acceptance,
        evidence_checks=evidence,
    )
    assert VerificationIssueCode.RESULT_PACKET_MISMATCH in {
        issue.code for issue in report.issues
    }


@pytest.mark.parametrize("status", ["failed", "blocked"])
def test_non_success_executor_status_blocks(status: str) -> None:
    n = node()
    p = packet(n)
    acceptance, evidence = passing_checks()
    report = verify_execution(
        n,
        p,
        result(p, status=status, error_code="EXECUTOR_STOPPED"),
        implementation_revision="git:a",
        observed_changed_paths=["src/specgrain/verification.py"],
        acceptance_checks=acceptance,
        evidence_checks=evidence,
    )
    assert VerificationIssueCode.EXECUTION_NOT_SUCCEEDED in {
        issue.code for issue in report.issues
    }


def test_executor_changed_paths_must_match_independent_observation() -> None:
    n = node()
    p = packet(n)
    acceptance, evidence = passing_checks()
    report = verify_execution(
        n,
        p,
        result(p, changed_paths=["tests/test_verification.py"]),
        implementation_revision="git:a",
        observed_changed_paths=["src/specgrain/verification.py"],
        acceptance_checks=acceptance,
        evidence_checks=evidence,
    )
    assert VerificationIssueCode.EXECUTOR_SCOPE_MISMATCH in {
        issue.code for issue in report.issues
    }


def test_unscoped_drive_by_change_blocks() -> None:
    n = node()
    p = packet(n)
    r = result(
        p,
        changed_paths=["src/specgrain/verification.py", "README.md"],
    )
    acceptance, evidence = passing_checks()
    report = verify_execution(
        n,
        p,
        r,
        implementation_revision="git:a",
        observed_changed_paths=["README.md", "src/specgrain/verification.py"],
        acceptance_checks=acceptance,
        evidence_checks=evidence,
    )
    assert [(issue.code, issue.subject) for issue in report.issues] == [
        (VerificationIssueCode.UNSCOPED_CHANGE, "README.md")
    ]


def test_authorized_directory_prefix_allows_child() -> None:
    n = node(change_surface=["src/specgrain"])
    p = packet(n)
    r = result(p)
    acceptance, evidence = passing_checks()
    report = verify_execution(
        n,
        p,
        r,
        implementation_revision="git:a",
        observed_changed_paths=["src/specgrain/verification.py"],
        acceptance_checks=acceptance,
        evidence_checks=evidence,
    )
    assert report.verified is True


@pytest.mark.parametrize(
    ("acceptance", "evidence", "expected"),
    [
        ([], passing_checks()[1], VerificationIssueCode.ACCEPTANCE_MISSING),
        (
            [
                CheckEvidence("acceptance-a", False, "test:a"),
                CheckEvidence("acceptance-b", True, "test:b"),
            ],
            passing_checks()[1],
            VerificationIssueCode.ACCEPTANCE_FAILED,
        ),
        (passing_checks()[0], [], VerificationIssueCode.EVIDENCE_MISSING),
        (
            passing_checks()[0],
            [CheckEvidence("tests", False, "pytest"), CheckEvidence("diff", True, "diff")],
            VerificationIssueCode.EVIDENCE_FAILED,
        ),
    ],
)
def test_required_independent_checks_block_when_missing_or_failed(
    acceptance: list[CheckEvidence],
    evidence: list[CheckEvidence],
    expected: VerificationIssueCode,
) -> None:
    n = node()
    p = packet(n)
    report = verify_execution(
        n,
        p,
        result(p),
        implementation_revision="git:a",
        observed_changed_paths=["src/specgrain/verification.py"],
        acceptance_checks=acceptance,
        evidence_checks=evidence,
    )
    assert expected in {issue.code for issue in report.issues}


def test_extra_independent_checks_are_preserved_but_do_not_block() -> None:
    n = node()
    p = packet(n)
    acceptance, evidence = passing_checks()
    evidence.append(CheckEvidence("security-review", True, "review:1"))
    report = verify_execution(
        n,
        p,
        result(p),
        implementation_revision="git:a",
        observed_changed_paths=["src/specgrain/verification.py"],
        acceptance_checks=acceptance,
        evidence_checks=evidence,
    )
    assert report.verified is True
    assert [check.check_id for check in report.evidence_checks] == [
        "diff",
        "security-review",
        "tests",
    ]


def test_verification_is_permutation_invariant() -> None:
    n = node()
    p = packet(n)
    acceptance, evidence = passing_checks()
    first = verify_execution(
        n,
        p,
        result(p, changed_paths=["tests/test_verification.py", "src/specgrain/verification.py"]),
        implementation_revision="git:a",
        observed_changed_paths=["tests/test_verification.py", "src/specgrain/verification.py"],
        acceptance_checks=acceptance,
        evidence_checks=evidence,
    )
    second = verify_execution(
        n,
        p,
        result(p, changed_paths=["src/specgrain/verification.py", "tests/test_verification.py"]),
        implementation_revision="git:a",
        observed_changed_paths=["src/specgrain/verification.py", "tests/test_verification.py"],
        acceptance_checks=list(reversed(acceptance)),
        evidence_checks=list(reversed(evidence)),
    )
    assert first.to_dict() == second.to_dict()


def test_invalid_changed_or_authorized_paths_fail_closed() -> None:
    n = node(change_surface=["../escape"])
    p = packet(n)
    with pytest.raises(VerificationError, match="repository-relative"):
        verify_execution(
            n,
            p,
            result(p),
            implementation_revision="git:a",
            observed_changed_paths=["src/specgrain/verification.py"],
            acceptance_checks=passing_checks()[0],
            evidence_checks=passing_checks()[1],
        )


def test_report_round_trip_rederives_verified() -> None:
    report = verified_report()
    loaded = VerificationReport.from_dict(report.to_dict())
    assert loaded == report
    payload = report.to_dict()
    payload["verified"] = False
    with pytest.raises(VerificationError, match="verified field"):
        VerificationReport.from_dict(payload)


def test_evidence_record_digest_round_trip_and_tamper_rejection() -> None:
    record = EvidenceRecord(verified_report())
    assert record.record_version == EVIDENCE_RECORD_VERSION
    assert EvidenceRecord.from_dict(record.to_dict()) == record
    payload = record.to_dict()
    payload["previous_record_digest"] = "sha256:" + "1" * 64
    with pytest.raises(VerificationError, match="record_digest"):
        EvidenceRecord.from_dict(payload)


def test_empty_proof_requires_initialized_store(tmp_path: Path) -> None:
    with pytest.raises(VerificationError, match=".specgrain store"):
        load_proof(tmp_path, "SG-000010")
    init_project(tmp_path, project_id="demo")
    proof = load_proof(tmp_path, "SG-000010")
    assert proof == ProofResult("SG-000010", ())
    assert proof.verified is False


def test_append_and_load_hash_chained_records(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    first = append_verification_report(tmp_path, verified_report())
    second = append_verification_report(tmp_path, verified_report())
    assert first.previous_record_digest is None
    assert second.previous_record_digest == first.record_digest
    proof = load_proof(tmp_path, "SG-000010")
    assert [record.record_digest for record in proof.records] == [
        first.record_digest,
        second.record_digest,
    ]
    assert proof.verified is True
    evidence_dir = tmp_path / ".specgrain" / "evidence" / "SG-000010"
    assert sorted(path.name for path in evidence_dir.iterdir()) == sorted(
        [first.record_digest[7:] + ".json", second.record_digest[7:] + ".json"]
    )


def test_latest_failed_reverification_controls_proof_status(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    append_verification_report(tmp_path, verified_report())
    report = verified_report()
    failed = VerificationReport(
        spec_id=report.spec_id,
        spec_revision=report.spec_revision,
        packet_digest=report.packet_digest,
        result_digest=report.result_digest,
        implementation_revision="git:new",
        observed_changed_paths=report.observed_changed_paths,
        acceptance_checks=report.acceptance_checks,
        evidence_checks=report.evidence_checks,
        issues=(
            verification_module.VerificationIssue(
                VerificationIssueCode.UNSCOPED_CHANGE,
                "README.md",
                "drive-by change",
            ),
        ),
    )
    append_verification_report(tmp_path, failed)
    assert load_proof(tmp_path, "SG-000010").verified is False


def test_load_rejects_filename_mismatch(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    record = EvidenceRecord(verified_report())
    write_record(
        tmp_path / ".specgrain" / "evidence" / "SG-000010",
        record,
        filename="0" * 64 + ".json",
    )
    with pytest.raises(VerificationError, match="filename"):
        load_proof(tmp_path, "SG-000010")


def test_load_rejects_forked_chain(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    evidence_dir = tmp_path / ".specgrain" / "evidence" / "SG-000010"
    first = EvidenceRecord(verified_report())
    other_report = verified_report()
    other = EvidenceRecord(
        VerificationReport(
            spec_id=other_report.spec_id,
            spec_revision=other_report.spec_revision,
            packet_digest=other_report.packet_digest,
            result_digest=other_report.result_digest,
            implementation_revision="git:other",
            observed_changed_paths=other_report.observed_changed_paths,
            acceptance_checks=other_report.acceptance_checks,
            evidence_checks=other_report.evidence_checks,
            issues=(),
        )
    )
    write_record(evidence_dir, first)
    write_record(evidence_dir, other)
    with pytest.raises(VerificationError, match="exactly one head"):
        load_proof(tmp_path, "SG-000010")


def test_load_rejects_missing_previous_record(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    record = EvidenceRecord(verified_report(), "sha256:" + "1" * 64)
    write_record(tmp_path / ".specgrain" / "evidence" / "SG-000010", record)
    with pytest.raises(VerificationError, match="missing record"):
        load_proof(tmp_path, "SG-000010")


def test_load_rejects_duplicate_json_keys_and_non_finite_numbers(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    evidence_dir = tmp_path / ".specgrain" / "evidence" / "SG-000010"
    evidence_dir.mkdir(parents=True)
    target = evidence_dir / ("0" * 64 + ".json")
    target.write_text('{"record_digest":"x","record_digest":"y"}', encoding="utf-8")
    with pytest.raises(VerificationError, match="duplicate JSON key"):
        load_proof(tmp_path, "SG-000010")
    target.write_text('{"value":NaN}', encoding="utf-8")
    with pytest.raises(VerificationError, match="non-finite"):
        load_proof(tmp_path, "SG-000010")


def test_load_rejects_oversized_record(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    evidence_dir = tmp_path / ".specgrain" / "evidence" / "SG-000010"
    evidence_dir.mkdir(parents=True)
    target = evidence_dir / ("0" * 64 + ".json")
    target.write_bytes(b"x" * (MAX_EVIDENCE_RECORD_BYTES + 1))
    with pytest.raises(VerificationError, match="exceeds"):
        load_proof(tmp_path, "SG-000010")


def test_load_rejects_unexpected_entry(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    evidence_dir = tmp_path / ".specgrain" / "evidence" / "SG-000010"
    evidence_dir.mkdir(parents=True)
    (evidence_dir / "notes.txt").write_text("not evidence", encoding="utf-8")
    with pytest.raises(VerificationError, match="unexpected evidence entry"):
        load_proof(tmp_path, "SG-000010")


def test_load_rejects_evidence_symlink(tmp_path: Path) -> None:
    if not hasattr(Path, "symlink_to"):
        pytest.skip("symlink unavailable")
    init_project(tmp_path, project_id="demo")
    outside = tmp_path / "outside"
    outside.mkdir()
    evidence = tmp_path / ".specgrain" / "evidence"
    evidence.symlink_to(outside, target_is_directory=True)
    with pytest.raises(VerificationError, match="symlink"):
        load_proof(tmp_path, "SG-000010")


def test_append_rolls_back_own_record_if_post_write_chain_check_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    init_project(tmp_path, project_id="demo")
    calls = 0
    real_load = verification_module.load_proof

    def synthetic(root: object, spec_id: str) -> ProofResult:
        nonlocal calls
        calls += 1
        if calls == 1:
            return real_load(root, spec_id)  # type: ignore[arg-type]
        raise VerificationError("synthetic concurrent fork")

    monkeypatch.setattr(verification_module, "load_proof", synthetic)
    with pytest.raises(VerificationError, match="concurrent fork"):
        append_verification_report(tmp_path, verified_report())
    evidence_dir = tmp_path / ".specgrain" / "evidence" / "SG-000010"
    assert list(evidence_dir.glob("*.json")) == []


def test_append_does_not_mutate_existing_store_files(tmp_path: Path) -> None:
    init_project(tmp_path, project_id="demo")
    manifest = tmp_path / ".specgrain" / "project.json"
    before = manifest.read_bytes()
    append_verification_report(tmp_path, verified_report())
    assert manifest.read_bytes() == before
