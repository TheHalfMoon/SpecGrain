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
- Specification 017 — Native DRAFT CLI: `CLOSED_CANONICAL`.
- Specification 018 — v0.2.0 Authoring Release: `CLOSED_CANONICAL`.
- Specification 019 — Native Child-DRAFT Authoring: `CLOSED_CANONICAL`.
- Specification 020 — v0.3.0 Recursive Authoring Release: `CLOSED_CANONICAL`; product/release source `70dd66aba0e68ae710e6ef12605ed153d107bab4`; GitHub Release `378962445`.
- Specification 021 — Public Launch Readiness Hardening: `CLOSED_CANONICAL`.
- Specification 022 — Native Grain Preparation: `CLOSED_CANONICAL`; bounded `DRAFT -> SHAPED -> REFINING -> GRAIN` preparation.
- Specification 023 — Spec Kit Preset-Compatible Import: `CLOSED_CANONICAL`; bounded path-bound identity fallback for template-light read-only imports.
- Specification 024 — Native WorkPacket Export: `SHAPED` candidate when the current shaping package is canonical; implementation blocked pending shaping merge and post-shaping CI.

The latest published release remains `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## Closed frontier — Specification 023

Specification 023 was selected from reproduced compatibility evidence against GitHub Spec Kit `main` `51e52be6c3b26fed3ff5424c671f4a559519a759` and its official bundled Lean preset.

The bounded outcome is complete:

- canonical full-template imports remain stable;
- template-light fallback identity comes only from a concrete explicit feature-path parent;
- fallback emits `FEATURE_NAME_DERIVED_FROM_PATH`;
- arbitrary prose is not inferred into structured semantics;
- source safety, read-only behavior, legacy-task non-promotion, and constitution non-adoption remain intact;
- `SPECKIT_IMPORT_VERSION == 1`;
- the canonical pre-023 report digest remains `sha256:678fcc87985902002a9d2bc852196fbffdc59b332740660f1deeaf0d4f58746a`;
- no Spec Kit runtime dependency or preset/hook/extension/bundle/workflow execution was added.

### Canonical proof

- shaping PR #41: exact head `e19484f292c7601036e1993e58203554d1267594`; shaping merge `99d8ee5bc7ce49c00ae542f3c06f564d05641a70`; post-shaping CI `33263898618` success across five cells;
- final implementation head `83fcc6add4e982df523f6c606399f08c317d3ffe`; push CI `33264389193` and PR CI `33264479954` success across five cells;
- implementation PR #42: expected-head merge `037f137cdd6e7a0fe224bd3fa3371d6da7460f22`; post-product CI `33265277105` success across five cells;
- documentation closeout head `fb23602a3aa234b88b0a223443c8c974ff8ed25a`; push CI `33265481647` and PR CI `33265501850` success across five cells;
- closeout PR #43: expected-head merge `5b3a8b906309de642a0b35dfa8e260b5fa6bedd1`; post-closeout CI `33265589133` success across five cells;
- historical `v0.3.0` tag, Release `378962445`, assets, digests, notes, and command surface remain unchanged.

The later SGB-EXP-001 experiment is preserved as `INVALIDATED_ORACLE_REVEALED_PRE_FREEZE`; it produced no valid comparative result, supports no superiority claim, and selects no product work.

The bounded multi-writer race retained after Specification 022 remains an explicit residual outside 024 authority.

## Active shaping frontier — Specification 024

Fresh deterministic interoperability evidence now selects one bounded successor candidate.

Evidence record:

`docs/research/post-023-workpacket-handoff-reproduction-2026-08-31.md`

Exact observation proof:

```text
canonical_base = f2e8378dcba0cfea2beedc6da61324b0c3fea95e
observation_head = 95e5358ed420cd2e6fbd0bc7c56690763cea1283
fixture_blob = 58cb3e355468f6bcd7de63b676dba52361ff0dd7
ci_run = 33416110142
ci_result = success across five permanent cells
```

The reproduced discontinuity is exact:

```text
native DRAFT -> SHAPED -> REFINING -> GRAIN
-> native next reports the Grain eligible
-> no native packet export command exists
-> existing public Python WorkPacket APIs succeed only after custom glue
```

Specification 024 therefore shapes only a read-only native export boundary:

```text
specgrain packet <spec_id> [path] --context-sources <json-file> [--json]
```

The command is constrained to:

- existing stored `GRAIN` state;
- current dependency eligibility;
- explicit bounded ContextSource records;
- the Grain's existing token budget;
- existing context-budget and WorkPacket primitives;
- deterministic stdout export without store mutation.

No new architectural authority is added. READY/later lifecycle mutation, executor/provider invocation, result ingestion, verification execution, evidence mutation, automatic context discovery, network access, LLM context selection, stronger locking, release publication, and hosted scope remain unselected.

## Current execution gate

Product implementation of Specification 024 is blocked until the documentation-only shaping package completes this gate:

1. exact shaping head contains only authorized research/governance/specification changes;
2. permanent five-cell CI succeeds on that exact head;
3. review comments, threads, mergeability, and review-system availability are rechecked without false PASS claims;
4. shaping PR merges with expected-head protection;
5. resulting canonical `main` passes permanent five-cell CI;
6. historical `v0.3.0` identity remains unchanged.

Only after that gate may `feat/024-native-workpacket-export` begin.

The implementation and closeout ordering is authoritative in `specs/024-native-workpacket-export/plan.md` and `tasks.md`.

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

At the Specification 024 shaping frontier, complete the shaping gate before product work. After Specification 024 closes, return to observation unless fresh reproducible evidence selects another bounded successor.