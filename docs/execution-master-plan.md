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
- Specification 023 — Spec Kit Preset-Compatible Import: product merged and verified; documentation closeout in progress.

The latest published release remains `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## Closed frontier — Specification 022

Specification 022 closed the native pre-execution preparation gap. Final status reconciliation is canonical at `ff9f640bf0e4de5bdd5bf2af0e11b98d86f6587b`; post-reconciliation CI `33262914956` completed `success` across the permanent five-cell matrix.

A bounded concurrent-writer race around exact-preimage validation and atomic replacement remains an explicit residual. Specification 023 does not select or alter that boundary.

## Closeout frontier — Specification 023

Post-022 observation produced a reproduced compatibility finding against exact current GitHub Spec Kit truth.

Reviewed upstream:

- `github/spec-kit` main `51e52be6c3b26fed3ff5424c671f4a559519a759`;
- latest observed release `v1.0.1` / `374643230`;
- standard spec-template blob `ceb28776215a098e977650ac090c785dcbf53651`;
- bundled Lean README blob `ab17257f96091590d2289699aaf2b114cc05bbbe`;
- bundled Lean specify blob `c15353557aa941b18e811c15aef605c41ff64133`;
- bundled Lean plan blob `9fbbe4c3713203a363169b9ca4d7f0dedbd0d1e0`;
- bundled Lean tasks blob `724a7b840074b8e34cf107f2ca37d211745d15be`.

Pre-023 SpecGrain required the canonical full-template `# Feature Specification:` heading to establish feature identity. The official bundled Lean preset intentionally does not require that boilerplate.

### Canonical shaping authority

Documentation-only shaping PR #41 merged exact head `e19484f292c7601036e1993e58203554d1267594` with expected-head protection as canonical shaped base `99d8ee5bc7ce49c00ae542f3c06f564d05641a70`.

Canonical post-shaping CI `33263898618` completed `success` across the permanent five-cell matrix before implementation began.

### Delivered bounded product behavior

Specification 023 implements only:

- canonical full-template imports remain behavior/report/digest-stable;
- when the canonical feature heading is absent, migration-report identity may come only from a concrete explicit feature-path parent;
- fallback identity is explicit through `FEATURE_NAME_DERIVED_FROM_PATH`;
- unrecognized prose is not inferred into structured semantics;
- source path/role/UTF-8/size/digest/revision safety remains unchanged;
- tasks remain non-core migration evidence;
- constitutions remain source-bound but non-authoritative;
- `SPECKIT_IMPORT_VERSION` remains `1`;
- no runtime dependency or upstream command execution is added.

The canonical pre-023 full-template report digest remains:

`sha256:678fcc87985902002a9d2bc852196fbffdc59b332740660f1deeaf0d4f58746a`.

### Product verification and merge

Initial checkpoint `0d18c523f57da007d946c3ad6ed99bcccaabe784` passed five-cell push CI `33264209823`; Ubuntu/Python 3.11 recorded `578 passed` plus all required static/package/CLI gates.

Final implementation head `83fcc6add4e982df523f6c606399f08c317d3ffe` passed exact push CI `33264389193` and exact PR CI `33264479954`, both `completed/success` across the permanent five-cell matrix.

PR #42 had no submitted reviews or inline review threads. Qodo was billing-blocked, automatic CodeRabbit review was skipped by repository-star policy, and Cubic provided descriptive summary text only; none was treated as independent approval.

PR #42 merged with expected-head protection as signature-verified canonical product merge `037f137cdd6e7a0fe224bd3fa3371d6da7460f22`, with parents:

1. `99d8ee5bc7ce49c00ae542f3c06f564d05641a70`;
2. `83fcc6add4e982df523f6c606399f08c317d3ffe`.

Canonical post-product CI `33265277105` completed `success` across all five permanent cells.

Historical `v0.3.0` remains unchanged at source `70dd66aba0e68ae710e6ef12605ed153d107bab4`, Release `378962445`, wheel digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`, and source digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

### Remaining closeout gates

Product work is complete. The remaining authorized work is documentation-only closeout and final evidence reconciliation:

1. exact closeout diff must remain governance/evidence only;
2. exact closeout head must pass permanent push and PR five-cell CI;
3. review comments/threads, review-system availability, and mergeability must be rechecked;
4. closeout PR must merge with expected-head protection;
5. canonical closeout parentage, post-closeout CI, and release preservation must be proven;
6. final evidence reconciliation must record exact closeout truth and only then declare 023 `CLOSED_CANONICAL`.

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

After Specification 023 closes canonically, re-read exact canonical `main` and return to observation/evidence gathering. Do not automatically continue into READY mutation, WorkPacket execution, executor/provider orchestration, verification execution, evidence mutation, stronger locking, release work, or broader Spec Kit integration.

No successor product scope is currently selected. No empirical benchmark winner is claimed without a reproducible completed dataset, and no aspirational CLI command is presented as shipped historical-release behavior.
