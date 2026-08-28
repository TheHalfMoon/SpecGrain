"""Run a complete deterministic SpecGrain Grain-to-proof example."""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path

from specgrain import (
    CheckEvidence,
    ContextBudgetPolicy,
    ContextSource,
    ExecutionResult,
    SpecNode,
    append_verification_report,
    build_work_packet,
    init_project,
    load_proof,
    require_context_budget,
    require_grain_readiness,
    verify_execution,
)


def _sha256(data: bytes) -> str:
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def run_demo(root: Path) -> tuple[str, ...]:
    """Execute the example in *root* and return stable human-readable proof lines."""

    root.mkdir(parents=True, exist_ok=True)
    init_project(root, project_id="zero-to-verified")

    node = SpecNode(
        id="SG-000001",
        title="Add a deterministic health helper",
        outcome="A local health helper returns a stable ok status.",
        scope_in=("Add one local health helper.",),
        scope_out=("Network calls", "Database changes"),
        acceptance=("health-response",),
        risk={"level": "low", "recovery": "Delete src/health.py."},
        context={"budget_tokens": 128, "estimated_tokens": 32},
        change_surface=("src/health.py",),
        evidence={"required": ["file-content"]},
        state="REFINING",
        metadata={
            "readiness": {
                "version": 1,
                "unresolved_decisions": [],
                "minimality": {
                    "choice": "new-code",
                    "rationale": "The isolated demo has no existing health helper.",
                },
                "safety": {"status": "none-identified", "requirements": []},
            }
        },
    )
    readiness = require_grain_readiness(node, (node,))

    context_source = ContextSource(
        source_id="health-requirement",
        provenance="example:zero-to-verified",
        selection_reason="Carries the exact bounded outcome used by the demo.",
        revision=node.revision_digest,
        size_bytes=len(node.outcome.encode("utf-8")),
        token_cost=16,
    )
    context_report = require_context_budget(
        (context_source,),
        ContextBudgetPolicy(max_tokens=64, max_bytes=512, max_sources=1),
    )
    packet = build_work_packet(
        node,
        (context_source,),
        context_report,
        minimality_evidence=("No reusable implementation exists in the isolated demo.",),
    )

    target = root / "src" / "health.py"
    target.parent.mkdir(parents=True, exist_ok=True)
    expected = 'def health() -> dict[str, str]:\n    return {"status": "ok"}\n'
    target.write_text(expected, encoding="utf-8", newline="\n")
    observed = target.read_text(encoding="utf-8")
    implementation_revision = _sha256(target.read_bytes())

    result = ExecutionResult(
        packet_digest=packet.packet_digest,
        status="succeeded",
        summary="Added the one authorized health helper.",
        changed_paths=("src/health.py",),
        reported_evidence=("file-content",),
    )
    report = verify_execution(
        current_node=node,
        packet=packet,
        result=result,
        implementation_revision=implementation_revision,
        observed_changed_paths=("src/health.py",),
        acceptance_checks=(
            CheckEvidence(
                "health-response",
                observed == expected,
                implementation_revision,
                "Independent content comparison matched the expected implementation.",
            ),
        ),
        evidence_checks=(
            CheckEvidence(
                "file-content",
                target.is_file() and target.read_bytes() == expected.encode("utf-8"),
                implementation_revision,
                "Independent file evidence matched the implementation revision.",
            ),
        ),
    )
    if not report.verified:
        raise RuntimeError("independent verification unexpectedly failed")

    record = append_verification_report(root, report)
    proof = load_proof(root, node.id)
    if not proof.verified or proof.latest is None:
        raise RuntimeError("evidence proof unexpectedly failed")

    return (
        f"Spec: {node.id}",
        f"Readiness: {'GRAIN' if readiness.is_ready else 'BLOCKED'}",
        f"Packet: {packet.packet_digest}",
        "Verification: VERIFIED",
        f"Evidence: {record.record_digest}",
        "Proof: VERIFIED",
    )


def main() -> int:
    """Run the isolated example and print its deterministic proof summary."""

    with tempfile.TemporaryDirectory(prefix="specgrain-zero-to-verified-") as temp_dir:
        for line in run_demo(Path(temp_dir)):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
