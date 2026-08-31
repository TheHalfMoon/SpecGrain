"""Command-line interface for the bounded local SpecGrain product surface."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from .context import (
    ContextBudgetError,
    ContextBudgetPolicy,
    ContextSource,
    ContextValidationError,
    require_context_budget,
    validate_context_sources,
)
from .lifecycle import SpecState
from .model import SpecValidationError, is_spec_id
from .packet import PacketValidationError, build_work_packet
from .pregrain import (
    GrainPromotionBlockedError,
    PreGrainMutationResult,
    promote_refining_spec_to_grain,
    refine_shaped_spec,
    shape_draft_spec,
)
from .project import NextResult, check_project, next_project
from .repository import RepositoryMap, RepositoryScanError, scan_repository
from .speckit import SpecKitImportError, SpecKitImportReport, load_spec_kit_feature
from .store import (
    AuthoringRecoveryResult,
    ChildDraftResult,
    ProjectCheckResult,
    StoreError,
    create_child_draft_spec,
    create_draft_spec,
    init_project,
    load_project,
    recover_authoring_transaction,
)
from .verification import ProofResult, VerificationError, load_proof

_PACKET_CONTEXT_SOURCE_MAX_BYTES = 1_048_576
_PACKET_CONTEXT_SOURCE_FIELDS = frozenset(
    {
        "source_id",
        "provenance",
        "selection_reason",
        "revision",
        "size_bytes",
        "token_cost",
        "requirement",
        "priority",
    }
)


class _PacketCliError(ValueError):
    """Expected fail-closed packet CLI input/state error."""


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="specgrain")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="initialize repository-local SpecGrain state")
    init.add_argument("path", nargs="?", default=".")
    init.add_argument("--project-id")

    draft = subparsers.add_parser("draft", help="create a native DRAFT SpecNode")
    draft.add_argument("path", nargs="?", default=".")
    draft.add_argument("--title", required=True)
    draft.add_argument("--outcome", required=True)
    draft.add_argument("--rationale", default="")
    draft.add_argument("--parent")
    draft.add_argument("--json", action="store_true", dest="as_json")

    shape = subparsers.add_parser(
        "shape",
        help="populate one DRAFT candidate and advance it to SHAPED",
    )
    shape.add_argument("spec_id")
    shape.add_argument("path", nargs="?", default=".")
    shape.add_argument("--scope-in", action="append", required=True)
    shape.add_argument("--scope-out", action="append", default=[])
    shape.add_argument("--acceptance", action="append", required=True)
    shape.add_argument("--dependency", action="append", default=[])
    shape.add_argument(
        "--risk-level",
        required=True,
        choices=("low", "medium", "high", "critical"),
    )
    shape.add_argument("--recovery", required=True)
    shape.add_argument("--context-budget", type=int, required=True)
    shape.add_argument("--context-estimate", type=int, required=True)
    shape.add_argument("--change-surface", action="append", default=[])
    shape.add_argument("--change-surface-exception")
    shape.add_argument("--evidence", action="append", required=True)
    shape.add_argument(
        "--minimality-choice",
        required=True,
        choices=(
            "reuse-existing",
            "stdlib",
            "native",
            "installed-dependency",
            "new-code",
        ),
    )
    shape.add_argument("--minimality-rationale", required=True)
    shape.add_argument(
        "--safety-status",
        required=True,
        choices=("none-identified", "requirements-defined"),
    )
    shape.add_argument("--safety-requirement", action="append", default=[])
    shape.add_argument("--json", action="store_true", dest="as_json")

    refine = subparsers.add_parser(
        "refine",
        help="advance one SHAPED candidate to REFINING",
    )
    refine.add_argument("spec_id")
    refine.add_argument("path", nargs="?", default=".")
    refine.add_argument("--json", action="store_true", dest="as_json")

    grain = subparsers.add_parser(
        "grain",
        help="promote one ready REFINING leaf to GRAIN",
    )
    grain.add_argument("spec_id")
    grain.add_argument("path", nargs="?", default=".")
    grain.add_argument("--json", action="store_true", dest="as_json")

    recover = subparsers.add_parser(
        "recover", help="recover a pending native authoring transaction"
    )
    recover.add_argument("path", nargs="?", default=".")
    recover.add_argument("--json", action="store_true", dest="as_json")

    check = subparsers.add_parser("check", help="validate repository-local SpecGrain state")
    check.add_argument("path", nargs="?", default=".")
    check.add_argument("--json", action="store_true", dest="as_json")

    next_parser = subparsers.add_parser("next", help="show dependency-eligible Grains")
    next_parser.add_argument("path", nargs="?", default=".")
    next_parser.add_argument("--json", action="store_true", dest="as_json")

    packet = subparsers.add_parser(
        "packet",
        help="export one dependency-eligible GRAIN as a portable WorkPacket",
    )
    packet.add_argument("spec_id")
    packet.add_argument("path", nargs="?", default=".")
    packet.add_argument(
        "--context-sources",
        required=True,
        help="UTF-8 ContextSource JSON array (maximum 1048576 bytes)",
    )
    packet.add_argument("--json", action="store_true", dest="as_json")

    scan = subparsers.add_parser("scan", help="scan deterministic brownfield repository facts")
    scan.add_argument("path", nargs="?", default=".")
    scan.add_argument("--json", action="store_true", dest="as_json")

    prove = subparsers.add_parser("prove", help="show independent evidence for a specification")
    prove.add_argument("spec_id")
    prove.add_argument("path", nargs="?", default=".")
    prove.add_argument("--json", action="store_true", dest="as_json")

    import_spec_kit = subparsers.add_parser(
        "import-spec-kit", help="inspect a bounded Spec Kit feature for migration"
    )
    import_spec_kit.add_argument("feature_dir")
    import_spec_kit.add_argument("--source-revision", required=True)
    import_spec_kit.add_argument("--constitution")
    import_spec_kit.add_argument("--json", action="store_true", dest="as_json")
    return parser


def _render_check_text(result: ProjectCheckResult) -> str:
    status = "PASS" if result.valid else "FAIL"
    lines = [f"SpecGrain check: {status}"]
    if result.project_id is not None:
        lines.append(f"Project: {result.project_id}")
        assert result.readiness_mode is not None
        mode = result.readiness_mode.value
        lines.append(f"Policy: {result.policy_name} (readiness={mode})")
        lines.append(f"Specs: {result.spec_count}")
        if result.root_count is not None:
            lines.append(f"Roots: {result.root_count}")
        lines.append(f"REFINING leaves: {result.refining_leaf_count}")
        lines.append(f"Grain-ready: {result.grain_ready_count}")
        lines.append(f"Readiness-blocked: {len(result.readiness_blocked)}")

    for issue in result.issues:
        lines.append(f"- [{issue.code}] {issue.location}: {issue.message}")
    for report in result.readiness_blocked:
        codes = ", ".join(issue.code.value for issue in report.issues)
        lines.append(f"- [{report.node_id}] readiness: {codes}")
    return "\n".join(lines)


def _render_next_text(result: NextResult) -> str:
    status = "PASS" if result.valid else "FAIL"
    lines = [f"SpecGrain next: {status}"]
    if result.project_id is not None:
        lines.append(f"Project: {result.project_id}")
        lines.append(f"Eligible: {len(result.eligible_ids)}")
        lines.extend(f"- {node_id}" for node_id in result.eligible_ids)
        for report in result.dependency_reports:
            if report.eligible:
                continue
            waiting = ", ".join(report.waiting_on) or "none"
            blockers = ", ".join(report.blocked_by) or "none"
            lines.append(
                f"- {report.node_id} waiting: {waiting}; blockers: {blockers}"
            )
        lines.append(f"Projected waves: {len(result.waves)}")
        for index, wave in enumerate(result.waves, start=1):
            lines.append(f"Wave {index}: {', '.join(wave)}")
    for issue in result.issues:
        lines.append(f"- [{issue.code}] {issue.location}: {issue.message}")
    return "\n".join(lines)


def _render_packet_text(packet) -> str:
    return "\n".join(
        [
            "SpecGrain packet: EXPORTED",
            f"Spec: {packet.spec_id}",
            f"Revision: {packet.spec_revision}",
            f"Context plan: {packet.context_plan_digest}",
            f"Packet: {packet.packet_digest}",
        ]
    )


def _render_scan_text(result: RepositoryMap) -> str:
    lines = [
        "SpecGrain scan: PASS",
        f"Repository: {result.repository_name}",
        f"Files: {result.file_count}",
        f"Skipped symlinks: {result.skipped_symlink_count}",
        f"Manifests: {len(result.manifests)}",
        f"Dependencies: {len(result.dependencies)}",
        f"Components: {len(result.components)}",
        f"Git: {result.git.layout}",
        f"Digest: {result.content_digest}",
    ]
    for manifest in result.manifests:
        lines.append(f"- manifest {manifest.kind}: {manifest.path}")
    for language in result.languages:
        lines.append(f"- language {language.language}: {language.file_count}")
    return "\n".join(lines)


def _render_proof_text(result: ProofResult) -> str:
    status = "PASS" if result.verified else "FAIL"
    lines = [
        f"SpecGrain prove: {status}",
        f"Spec: {result.spec_id}",
        f"Records: {len(result.records)}",
        f"Verified: {str(result.verified).lower()}",
    ]
    if result.latest is not None:
        lines.append(f"Latest: {result.latest.record_digest}")
        lines.append(f"Implementation: {result.latest.report.implementation_revision}")
        lines.extend(
            f"- [{issue.code.value}] {issue.subject}: {issue.message}"
            for issue in result.latest.report.issues
        )
    return "\n".join(lines)


def _render_spec_kit_import_text(result: SpecKitImportReport) -> str:
    lines = [
        "SpecGrain import-spec-kit: PASS",
        f"Feature: {result.feature_name}",
        f"Source revision: {result.source_revision}",
        f"Stories: {len(result.stories)}",
        f"Functional requirements: {len(result.functional_requirements)}",
        f"Success criteria: {len(result.success_criteria)}",
        f"Legacy tasks preserved: {len(result.legacy_tasks)}",
        "Legacy tasks promoted to core: false",
        f"Digest: {result.digest}",
    ]
    lines.extend(f"- [{notice.code}] {notice.message}" for notice in result.notices)
    return "\n".join(lines)


def _draft_payload(spec_id: str, state: str, revision_digest: str) -> dict[str, str]:
    return {
        "file": f".specgrain/specs/{spec_id}.json",
        "revision_digest": revision_digest,
        "spec_id": spec_id,
        "state": state,
    }


def _child_draft_payload(result: ChildDraftResult) -> dict[str, str]:
    payload = _draft_payload(
        result.child.id,
        result.child.state,
        result.child.revision_digest,
    )
    payload.update(
        {
            "parent_file": f".specgrain/specs/{result.parent_after.id}.json",
            "parent_id": result.parent_after.id,
            "parent_revision_after": result.parent_after.revision_digest,
            "parent_revision_before": result.parent_before_revision,
        }
    )
    return payload


def _render_recovery_text(result: AuthoringRecoveryResult) -> str:
    lines = [f"SpecGrain recover: {result.status.value.upper()}"]
    if result.parent_id is not None:
        lines.append(f"Parent: {result.parent_id}")
    if result.child_id is not None:
        lines.append(f"Child: {result.child_id}")
    return "\n".join(lines)


def _render_pregrain_text(command: str, result: PreGrainMutationResult) -> str:
    payload = result.to_dict()
    return "\n".join(
        [
            f"SpecGrain {command}: UPDATED",
            f"Spec: {payload['spec_id']}",
            f"Source state: {payload['source_state']}",
            f"State: {payload['state']}",
            f"File: {payload['file']}",
            f"Revision: {payload['revision_digest']}",
        ]
    )


def _json_error(message: str) -> str:
    return json.dumps(
        {"error": message, "valid": False},
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )


def _strict_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _PacketCliError(
                f"context source input contains duplicate object key {key!r}"
            )
        result[key] = value
    return result


def _reject_json_constant(token: str) -> object:
    raise _PacketCliError(
        f"context source input contains non-finite numeric token {token!r}"
    )


def _load_packet_context_sources(value: str) -> tuple[ContextSource, ...]:
    path = Path(value)
    try:
        if path.is_symlink():
            raise _PacketCliError("context source input must not be a symlink")
        if not path.is_file():
            raise _PacketCliError("context source input must be a regular file")
        size = path.stat().st_size
        if size > _PACKET_CONTEXT_SOURCE_MAX_BYTES:
            raise _PacketCliError(
                "context source input exceeds "
                f"{_PACKET_CONTEXT_SOURCE_MAX_BYTES}-byte limit"
            )
        raw = path.read_bytes()
    except _PacketCliError:
        raise
    except OSError as exc:
        raise _PacketCliError("context source input could not be read") from exc

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _PacketCliError("context source input is not valid UTF-8") from exc

    try:
        payload = json.loads(
            text,
            object_pairs_hook=_strict_json_object,
            parse_constant=_reject_json_constant,
        )
    except _PacketCliError:
        raise
    except json.JSONDecodeError as exc:
        raise _PacketCliError(
            f"context source input is malformed JSON: {exc.msg}"
        ) from exc

    if not isinstance(payload, list):
        raise _PacketCliError("context source input top-level value must be an array")

    sources: list[ContextSource] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise _PacketCliError(f"context_sources[{index}] must be an object")
        unknown = sorted(set(item) - _PACKET_CONTEXT_SOURCE_FIELDS)
        missing = sorted(_PACKET_CONTEXT_SOURCE_FIELDS - set(item))
        if unknown:
            raise _PacketCliError(
                f"context_sources[{index}] has unknown fields: {', '.join(unknown)}"
            )
        if missing:
            raise _PacketCliError(
                f"context_sources[{index}] is missing fields: {', '.join(missing)}"
            )
        try:
            source = ContextSource(**item)
        except (ContextValidationError, TypeError) as exc:
            raise _PacketCliError(
                f"context_sources[{index}] is invalid: {exc}"
            ) from exc
        sources.append(source)

    return validate_context_sources(sources)


def _render_grain_blocked_json(exc: GrainPromotionBlockedError) -> str:
    report = exc.report
    return json.dumps(
        {
            "issues": [
                {
                    "code": issue.code.value,
                    "field": issue.field,
                    "message": issue.message,
                }
                for issue in report.issues
            ],
            "revision_digest": report.revision_digest,
            "source_state": "REFINING",
            "spec_id": report.node_id,
            "state": "REFINING",
            "valid": False,
        },
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )


def _render_grain_blocked_text(exc: GrainPromotionBlockedError) -> str:
    report = exc.report
    lines = [
        "SpecGrain grain: BLOCKED",
        f"Spec: {report.node_id}",
        "Source state: REFINING",
        "State: REFINING",
        f"Revision: {report.revision_digest}",
    ]
    lines.extend(
        f"- [{issue.code.value}] {issue.field}: {issue.message}"
        for issue in report.issues
    )
    return "\n".join(lines)


def _run_pregrain_command(args: argparse.Namespace) -> int:
    command = args.command
    try:
        if command == "shape":
            result = shape_draft_spec(
                args.path,
                spec_id=args.spec_id,
                scope_in=tuple(args.scope_in),
                scope_out=tuple(args.scope_out),
                acceptance=tuple(args.acceptance),
                dependencies=tuple(args.dependency),
                risk_level=args.risk_level,
                recovery=args.recovery,
                context_budget=args.context_budget,
                context_estimate=args.context_estimate,
                change_surface=tuple(args.change_surface),
                change_surface_exception=args.change_surface_exception,
                evidence=tuple(args.evidence),
                minimality_choice=args.minimality_choice,
                minimality_rationale=args.minimality_rationale,
                safety_status=args.safety_status,
                safety_requirements=tuple(args.safety_requirement),
            )
        elif command == "refine":
            result = refine_shaped_spec(args.path, spec_id=args.spec_id)
        elif command == "grain":
            result = promote_refining_spec_to_grain(args.path, spec_id=args.spec_id)
        else:
            raise AssertionError(f"unhandled pre-Grain command {command!r}")
    except GrainPromotionBlockedError as exc:
        if args.as_json:
            print(_render_grain_blocked_json(exc), file=sys.stderr)
        else:
            print(_render_grain_blocked_text(exc), file=sys.stderr)
        return 1
    except (StoreError, SpecValidationError) as exc:
        if args.as_json:
            print(_json_error(str(exc)), file=sys.stderr)
        else:
            print(f"SpecGrain {command}: FAIL\n- {exc}", file=sys.stderr)
        return 1
    except Exception:
        print(f"SpecGrain {command}: FAIL\n- internal error", file=sys.stderr)
        return 1

    if args.as_json:
        print(
            json.dumps(
                result.to_dict(),
                sort_keys=True,
                ensure_ascii=False,
                separators=(",", ":"),
            )
        )
    else:
        print(_render_pregrain_text(command, result))
    return 0


def _run_packet_command(args: argparse.Namespace) -> int:
    try:
        if not is_spec_id(args.spec_id):
            raise _PacketCliError("spec_id must be a canonical SpecGrain ID")

        project = load_project(args.path)
        matches = tuple(node for node in project.specs if node.id == args.spec_id)
        if not matches:
            raise _PacketCliError(f"spec {args.spec_id} was not found")
        if len(matches) != 1:
            raise _PacketCliError(f"spec {args.spec_id} is not unique")
        node = matches[0]
        if node.state != SpecState.GRAIN.value:
            raise _PacketCliError(
                f"spec {args.spec_id} must be in GRAIN state for packet export"
            )

        next_result = next_project(args.path)
        if not next_result.valid:
            details = "; ".join(
                f"[{issue.code}] {issue.location}: {issue.message}"
                for issue in next_result.issues
            )
            raise _PacketCliError(
                "project dependency state is invalid"
                + (f": {details}" if details else "")
            )
        if args.spec_id not in next_result.eligible_ids:
            raise _PacketCliError(f"spec {args.spec_id} is not dependency-eligible")

        sources = _load_packet_context_sources(args.context_sources)
        policy = ContextBudgetPolicy(max_tokens=node.context.get("budget_tokens"))
        context_report = require_context_budget(sources, policy)
        by_id = {source.source_id: source for source in sources}
        selected_sources = tuple(
            by_id[source_id] for source_id in context_report.selected_ids
        )
        packet = build_work_packet(node, selected_sources, context_report)
    except (
        _PacketCliError,
        ContextBudgetError,
        ContextValidationError,
        PacketValidationError,
        SpecValidationError,
        StoreError,
    ) as exc:
        if args.as_json:
            print(_json_error(str(exc)), file=sys.stderr)
        else:
            print(f"SpecGrain packet: FAIL\n- {exc}", file=sys.stderr)
        return 1
    except Exception:
        if args.as_json:
            print(_json_error("internal error"), file=sys.stderr)
        else:
            print("SpecGrain packet: FAIL\n- internal error", file=sys.stderr)
        return 1

    if args.as_json:
        print(packet.to_json())
    else:
        print(_render_packet_text(packet))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the SpecGrain CLI and return a process-compatible exit code."""

    args = _parser().parse_args(argv)
    if args.command == "init":
        try:
            project = init_project(args.path, project_id=args.project_id)
        except StoreError as exc:
            print(f"SpecGrain init: FAIL\n- {exc}", file=sys.stderr)
            return 1
        except Exception:
            print("SpecGrain init: FAIL\n- internal error", file=sys.stderr)
            return 1
        print("SpecGrain init: PASS")
        print(f"Project: {project.manifest.project_id}")
        print("Store: .specgrain")
        return 0

    if args.command == "draft":
        try:
            if args.parent is None:
                node = create_draft_spec(
                    args.path,
                    title=args.title,
                    outcome=args.outcome,
                    rationale=args.rationale,
                )
                child_result = None
            else:
                child_result = create_child_draft_spec(
                    args.path,
                    parent_id=args.parent,
                    title=args.title,
                    outcome=args.outcome,
                    rationale=args.rationale,
                )
                node = child_result.child
        except (StoreError, SpecValidationError) as exc:
            if args.as_json:
                print(_json_error(str(exc)), file=sys.stderr)
            else:
                print(f"SpecGrain draft: FAIL\n- {exc}", file=sys.stderr)
            return 1
        except Exception:
            print("SpecGrain draft: FAIL\n- internal error", file=sys.stderr)
            return 1

        payload = (
            _draft_payload(node.id, node.state, node.revision_digest)
            if child_result is None
            else _child_draft_payload(child_result)
        )
        if args.as_json:
            print(
                json.dumps(
                    payload,
                    sort_keys=True,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            )
        else:
            print("SpecGrain draft: CREATED")
            print(f"Spec: {node.id}")
            print(f"State: {node.state}")
            print(f"File: {payload['file']}")
            print(f"Revision: {node.revision_digest}")
            if child_result is not None:
                print(f"Parent: {child_result.parent_after.id}")
                print(
                    "Parent revision before: "
                    f"{child_result.parent_before_revision}"
                )
                print(
                    "Parent revision after: "
                    f"{child_result.parent_after.revision_digest}"
                )
        return 0

    if args.command in {"shape", "refine", "grain"}:
        return _run_pregrain_command(args)

    if args.command == "recover":
        try:
            result = recover_authoring_transaction(args.path)
        except StoreError as exc:
            if args.as_json:
                print(_json_error(str(exc)), file=sys.stderr)
            else:
                print(f"SpecGrain recover: FAIL\n- {exc}", file=sys.stderr)
            return 1
        except Exception:
            print("SpecGrain recover: FAIL\n- internal error", file=sys.stderr)
            return 1
        if args.as_json:
            print(
                json.dumps(
                    result.to_dict(),
                    sort_keys=True,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            )
        else:
            print(_render_recovery_text(result))
        return 0

    if args.command == "check":
        try:
            result = check_project(args.path)
        except Exception:
            print("SpecGrain check: FAIL\n- internal error", file=sys.stderr)
            return 1
        if args.as_json:
            print(
                json.dumps(
                    result.to_dict(),
                    sort_keys=True,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            )
        else:
            print(_render_check_text(result))
        return 0 if result.valid else 1

    if args.command == "next":
        try:
            result = next_project(args.path)
        except Exception:
            print("SpecGrain next: FAIL\n- internal error", file=sys.stderr)
            return 1
        if args.as_json:
            print(
                json.dumps(
                    result.to_dict(),
                    sort_keys=True,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            )
        else:
            print(_render_next_text(result))
        return 0 if result.valid else 1

    if args.command == "packet":
        return _run_packet_command(args)

    if args.command == "scan":
        try:
            result = scan_repository(args.path)
        except RepositoryScanError as exc:
            if args.as_json:
                print(
                    json.dumps(
                        {"error": exc.to_dict(), "valid": False},
                        sort_keys=True,
                        ensure_ascii=False,
                        separators=(",", ":"),
                    ),
                    file=sys.stderr,
                )
            else:
                print(f"SpecGrain scan: FAIL\n- {exc}", file=sys.stderr)
            return 1
        except Exception:
            print("SpecGrain scan: FAIL\n- internal error", file=sys.stderr)
            return 1
        if args.as_json:
            print(
                json.dumps(
                    result.to_dict(),
                    sort_keys=True,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            )
        else:
            print(_render_scan_text(result))
        return 0

    if args.command == "prove":
        try:
            result = load_proof(args.path, args.spec_id)
        except VerificationError as exc:
            if args.as_json:
                print(_json_error(str(exc)), file=sys.stderr)
            else:
                print(f"SpecGrain prove: FAIL\n- {exc}", file=sys.stderr)
            return 1
        if args.as_json:
            print(
                json.dumps(
                    result.to_dict(),
                    sort_keys=True,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            )
        else:
            print(_render_proof_text(result))
        return 0 if result.verified else 1

    if args.command == "import-spec-kit":
        try:
            result = load_spec_kit_feature(
                args.feature_dir,
                source_revision=args.source_revision,
                constitution_path=args.constitution,
            )
        except SpecKitImportError as exc:
            if args.as_json:
                print(_json_error(str(exc)), file=sys.stderr)
            else:
                print(f"SpecGrain import-spec-kit: FAIL\n- {exc}", file=sys.stderr)
            return 1
        payload = result.to_dict()
        payload["digest"] = result.digest
        if args.as_json:
            print(
                json.dumps(
                    payload,
                    sort_keys=True,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            )
        else:
            print(_render_spec_kit_import_text(result))
        return 0

    raise AssertionError(f"unhandled command {args.command!r}")