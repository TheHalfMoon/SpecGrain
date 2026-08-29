# SpecGrain Execution Master Plan

This document is the durable continuation plan for SpecGrain. `specs/CURRENT.md` is authoritative for the active frontier, and live GitHub state overrides stale text when they disagree.

## Canonical reading order

Before changing the repository, read:

1. `AGENTS.md`;
2. `specs/CURRENT.md`;
3. `.specify/memory/constitution.md`;
4. this file;
5. the active `spec.md`, `plan.md`, and `tasks.md` when an active specification exists;
6. referenced ADRs, contracts, research, and implementation files.

## Product objective

> Make every software change small enough to understand, execute, verify, recover, measure, and prove.

SpecGrain is an independent, agent-neutral delivery system built around recursively refined specifications. A specification is refined until a leaf satisfies the deterministic Definition of Grain. Probabilistic systems may propose work; they are never the sole authority for correctness-sensitive state transitions.

## Canonical initial program sequence

```text
001 SpecNode schema
  -> 002 lifecycle state
  -> 003 refinement tree
  -> 004 Grain readiness
  -> 005 CLI/local store
  -> 006 dependency graph
  -> 007 repository scan
  -> 008 context budget
  -> 009 WorkPacket
  -> 010 verification/evidence
  -> 011 method profiles
  -> 012 diff/drift/metrics
  -> 013 Spec Kit import
  -> 014 agent adapters
  -> 015 SpecGrainBench
  -> 016 public launch
```

Specification 000 established the project foundation and constitution. Specifications 000 through 016 are `CLOSED_CANONICAL`.

## Versioned product history

- `v0.1.0` product source: `5eb46db0479cb8707afe070027dab4f3c558849a`; initial program closeout: `7c343841424ca48207f9c42eae725a53213d19e5`.
- Specification 017 — Native DRAFT CLI: `CLOSED_CANONICAL`; root DRAFT authoring.
- Specification 018 — v0.2.0 Authoring Release: `CLOSED_CANONICAL`; published root DRAFT authoring.
- Specification 019 — Native Child-DRAFT Authoring: `CLOSED_CANONICAL`; recoverable reciprocal child authoring under ADR-0018.
- Specification 020 — v0.3.0 Recursive Authoring Release: `CLOSED_CANONICAL`; product/release source `70dd66aba0e68ae710e6ef12605ed153d107bab4`; GitHub Release `378962445`.
- Specification 021 — Public Launch Readiness Hardening: `CLOSED_CANONICAL`; repository-side public launch hardening without product/release mutation.
- Specification 022 — Native Grain Preparation: `CLOSED_CANONICAL`; current source closes the bounded native `DRAFT -> SHAPED -> REFINING -> GRAIN` pre-execution gap without READY/execution/verification authority.

The latest published release remains `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## Closed frontier — Specification 022

Specification 022 was selected from reproduced native adoption friction and closed the exact bounded pre-execution preparation gap. Final evidence reconciliation is canonical at `ff9f640bf0e4de5bdd5bf2af0e11b98d86f6587b`; post-reconciliation CI `33262914956` completed `success` across the permanent five-cell matrix.

The historical `v0.3.0` tag, Release `378962445`, assets, digests, and historical command list remain unchanged. A bounded concurrent-writer race remains an explicit residual and requires separately shaped authority if future evidence selects stronger coordination.

## Active frontier — Specification 023

Post-022 observation produced a concrete compatibility finding against exact current GitHub Spec Kit truth.

Reviewed upstream:

- `github/spec-kit` main `51e52be6c3b26fed3ff5424c671f4a559519a759`;
- latest observed release `v1.0.1` / `374643230`;
- standard `templates/spec-template.md` blob `ceb28776215a098e977650ac090c785dcbf53651`;
- bundled Lean README blob `ab17257f96091590d2289699aaf2b114cc05bbbe`;
- bundled Lean specify blob `c15353557aa941b18e811c15aef605c41ff64133`;
- bundled Lean plan blob `9fbbe4c3713203a363169b9ca4d7f0dedbd0d1e0`;
- bundled Lean tasks blob `724a7b840074b8e34cf107f2ca37d211745d15be`.

Pre-023 SpecGrain importer blob `fe68ca91d9bca3b649a80bf7fc4d2942db6a18a0` established feature identity only from the canonical full-template `# Feature Specification:` heading. The official bundled Lean preset intentionally produces focused Markdown without requiring full-template boilerplate. Therefore an official current Spec Kit artifact could be rejected before the bounded migration report exists solely because of template shape.

The exact audit lives at:

`docs/research/post-022-spec-kit-1.0-compatibility-audit-2026-08-29.md`

### Canonical shaping authority

Documentation-only shaping PR #41 merged exact head `e19484f292c7601036e1993e58203554d1267594` with expected-head protection as canonical shaped base:

`99d8ee5bc7ce49c00ae542f3c06f564d05641a70`

Canonical post-shaping CI `33263898618` completed `success` across the permanent five-cell matrix, and historical `v0.3.0` remained unchanged. T007 is closed and 023 implementation authority is canonical.

### 023 bounded product behavior

Specification 023 authorizes only the smallest deterministic repair:

- canonical full-template imports remain behavior/report/digest-stable;
- when the canonical feature heading is absent, migration-report identity may come only from a concrete explicit feature-path parent;
- direct artifact mappings use the normalized `spec.md` parent path;
- filesystem loading uses the explicitly selected feature directory's final component solely as fallback identity while keeping legacy source-artifact report paths stable;
- path fallback is explicit through `FEATURE_NAME_DERIVED_FROM_PATH`;
- unrecognized prose is not inferred into structured semantics;
- existing source path/role/UTF-8/size/digest/revision safety remains unchanged;
- tasks remain non-core migration evidence;
- constitutions remain source-bound but non-authoritative;
- `SPECKIT_IMPORT_VERSION` remains `1`;
- no runtime dependency or upstream command execution is added.

ADR-0020 governs this path-bound identity rule.

### Verified implementation checkpoint

Checkpoint:

`0d18c523f57da007d946c3ad6ed99bcccaabe784`

changes only `src/specgrain/speckit.py`, `tests/test_speckit.py`, and `docs/migration-from-spec-kit.md` from canonical shaped base.

Push CI `33264209823` completed `success` across all five permanent cells. Ubuntu/Python 3.11 recorded `578 passed` plus Ruff over `src`, `tests`, and `examples`, editable installation with `--no-deps`, tracked-tree cleanliness, compileall, source CLI smoke, package build, built-wheel reinstall with `--no-deps`, and installed CLI smoke.

The pre-023 canonical full-template report digest remains locked at:

`sha256:678fcc87985902002a9d2bc852196fbffdc59b332740660f1deeaf0d4f58746a`

and the import report version remains `1`.

### Remaining 023 product gates

Before product merge:

1. reconcile exact evidence/status documents;
2. review the shaped-base-to-final-head diff for semantic inference, unsafe path acceptance, hidden upstream coupling, report/digest churn, task/constitution promotion, unrelated scope, and false historical release claims;
3. open the bounded implementation PR from exact shaped base;
4. prove permanent push/PR five-cell CI on exact PR head;
5. recheck review comments/threads/mergeability and unavailable review systems without false PASS claims;
6. merge only with expected-head protection;
7. prove canonical product merge parentage, post-product five-cell CI, and historical `v0.3.0` preservation;
8. complete documentation-only closeout and final canonical verification.

023 explicitly does not authorize arbitrary Markdown semantic inference, Spec Kit preset/hook/extension/bundle/workflow installation or execution, automatic SpecNode creation, constitution adoption, task promotion, READY/execution/verification authority, provider orchestration, concurrency expansion, or release publication.

An external architectural review, including a Fable review, may add evidence but cannot widen 023 authority without canonical reshaping.

## Cross-spec execution rules

1. Live GitHub/repository truth overrides chat handoffs.
2. No force-push, rebase, or destructive shared-history rewriting.
3. Use bounded feature branches and pull requests.
4. Verify exact PR head, checks, threads, and scope before merge.
5. Merge with expected-head protection where available.
6. Never claim PASS, VERIFIED, MERGED, COMPLETE, or `CLOSED_CANONICAL` without exact evidence.
7. Re-read canonical `main` after every merge.
8. Prefer smaller native implementations over dependencies without demonstrated need.
9. Do not execute untrusted repository commands merely to inspect a brownfield project.
10. Do not make AI reasoning transcripts repository authority.
11. Preserve residual risks and blockers.
12. External ideas/code require license-aware provenance.
13. Post-v0.1 work requires a newly shaped specification derived from live evidence; roadmap deferrals, audits, external reviewers, and upstream-tool comparisons are not implicit implementation authority.

## Program continuation rule

If Specification 023 closes canonically, re-read exact canonical `main` and return to observation/evidence gathering. Do not automatically continue into READY mutation, WorkPacket execution, executor/provider orchestration, verification execution, evidence mutation, stronger locking, release work, or broader Spec Kit integration.

No empirical benchmark winner is claimed without a reproducible completed dataset. No aspirational CLI command is presented as shipped historical-release behavior.
