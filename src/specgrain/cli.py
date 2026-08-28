"""Command-line interface for the bounded local SpecGrain product surface."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from .project import NextResult, check_project, next_project
from .repository import RepositoryMap, RepositoryScanError, scan_repository
from .speckit import SpecKitImportError, SpecKitImportReport, load_spec_kit_feature
from .store import ProjectCheckResult, StoreError, init_project
from .verification import ProofResult, VerificationError, load_proof


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="specgrain")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="initialize repository-local SpecGrain state")
    init.add_argument("path", nargs="?", default=".")
    init.add_argument("--project-id")

    check = subparsers.add_parser("check", help="validate repository-local SpecGrain state")
    check.add_argument("path", nargs="?", default=".")
    check.add_argument("--json", action="store_true", dest="as_json")

    next_parser = subparsers.add_parser("next", help="show dependency-eligible Grains")
    next_parser.add_argument("path", nargs="?", default=".")
    next_parser.add_argument("--json", action="store_true", dest="as_json")

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
                print(
                    json.dumps(
                        {"error": str(exc), "valid": False},
                        sort_keys=True,
                        ensure_ascii=False,
                        separators=(",", ":"),
                    ),
                    file=sys.stderr,
                )
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
                print(
                    json.dumps(
                        {"error": str(exc), "valid": False},
                        sort_keys=True,
                        ensure_ascii=False,
                        separators=(",", ":"),
                    ),
                    file=sys.stderr,
                )
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
