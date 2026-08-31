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

SpecGrain is an independent, agent-neutral delivery system built around recursively refined specifications. Probabilistic systems may propose work; deterministic validation owns correctness-sensitive state transitions.

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
- Specification 020 — v0.3.0 Recursive Authoring Release: `CLOSED_CANONICAL`; release source `70dd66aba0e68ae710e6ef12605ed153d107bab4`; Release `378962445`.
- Specification 021 — Public Launch Readiness Hardening: `CLOSED_CANONICAL`.
- Specification 022 — Native Grain Preparation: `CLOSED_CANONICAL`.
- Specification 023 — Spec Kit Preset-Compatible Import: `CLOSED_CANONICAL`.
- Specification 024 — Native WorkPacket Export: `CLOSED_CANONICAL`.
- Specification 025 — Supported Pre-Grain Writer Serialization: `CLOSED_CANONICAL`.
- Specification 026 — Supported Mutation Cross-Writer Coordination: `SHAPED_CANDIDATE`; implementation blocked until canonical shaping merge and post-shaping CI.

The latest published release remains `v0.3.0` at exact historical source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## Closed frontier — Specification 025

Specification 025 remains `CLOSED_CANONICAL`. Its product implementation introduced one project-scoped non-blocking advisory lock around supported pre-Grain persistence and preserved exact-preimage/postimage, lifecycle, readiness, dependency, and runtime-dependency-free behavior.

Canonical evidence remains:

```text
product_merge = 5e3966fb0db3d8971b5abe19106949001ed55ba9
post_product_ci = 33434910548
closeout_merge = e05df4bd046590ee043115c1edbcd7b83163b4ad
post_closeout_ci = 33436130730
reconciliation_merge = 8a0da2908f6251100a0d7ab71178c2a7c3ed64bb
post_reconciliation_ci = 33437077692
post_normalization_merge = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
post_normalization_ci = 33440739066
```

All permanent post-product/closeout/reconciliation/normalization CI gates succeeded across Ubuntu/Python 3.11, Ubuntu/Python 3.12, Ubuntu/Python 3.13, macOS/Python 3.11, and Windows/Python 3.11. Unavailable or skipped review systems were never treated as PASS.

## Post-025 observation and Specification 026 selection

Fresh reproducible evidence against exact canonical baseline `1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1` independently selected a new bounded gap:

```text
observation_branch = obs/post-025-supported-cross-writer-fixture
observation_head = 3b557f91ec80c147b30f797198d736c2b6b42518
fixture_blob = ba8cea9510d09415a5bd4d2f123a72f5c8affee8
ci_run = 33441481985
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION
```

The fixture uses only supported `shape_draft_spec` and `create_child_draft_spec` APIs. A child writer can successfully create and confirm a child plus parent reference after the pre-Grain writer's final exact preimage check but before `os.replace`. The pre-Grain writer then overwrites that successful parent postimage, fails project revalidation after mutation, and leaves a structurally invalid stored refinement.

The first observation head `975c47b288cddbfbde34fbbca06afa77ee86f9af` / CI `33441425481` is harness-invalid for selection because Ruff stopped execution before the fixture ran. No product inference is taken from it.

Selection record:

```text
docs/research/post-025-supported-cross-writer-reproduction-2026-09-01.md
```

Architectural decision:

```text
docs/adr/0021-supported-mutation-cross-writer-coordination.md
```

## Specification 026 shaped boundary

Specification 026 selects only cooperative mutual exclusion between two already-supported mutation families that can touch the same canonical DRAFT parent:

1. pre-Grain persistence through `src/specgrain/pregrain.py::_persist`;
2. native child authoring through `src/specgrain/store.py::create_child_draft_spec`.

The candidate reuses the existing project-scoped non-blocking advisory anchor:

```text
.specgrain/tmp/pregrain-mutation.lock
```

The private lock abstraction may be moved to a dependency-neutral module so both `store.py` and `pregrain.py` can use it without a circular import. Child authoring must acquire the shared lock before journal creation and hold it through completion or handled recovery of that authoring attempt. The journal remains the separate durable recovery mechanism.

### Explicit non-authority

Specification 026 does not authorize arbitrary external-writer coordination, universal project transaction management, journal schema/version/recovery redesign, distributed locking, blocking waits/retries/timeouts/leases, runtime dependencies, lifecycle expansion, executor/provider/result/verification/evidence orchestration, automatic context/network/model behavior, Spec Kit runtime integration, release publication, hosted scope, or benchmark claims.

The invalidated SGB-EXP-001 hidden scorer remains outside all inspection/search/materialization/use authority.

## Specification 026 authority gate

Current shaping state:

```text
SHAPING_JUSTIFIED = true
SHAPED_CANDIDATE = true
IMPLEMENTATION_AUTHORIZED = false
```

Product implementation MUST NOT begin until:

1. the documentation/governance-only shaping branch is verified against exact canonical base;
2. shaping push CI succeeds across all five permanent cells on the exact final head;
3. the shaping PR exact head/base/scope, CI, mergeability, reviews, comments, and inline threads are rechecked;
4. unavailable/skipped review systems are recorded accurately and not treated as PASS;
5. the shaping PR is merged with expected-head protection;
6. canonical `main` is re-read;
7. permanent post-shaping CI succeeds across all five permanent cells on the exact shaping merge;
8. no new live repository truth supersedes the authority.

Only then may implementation proceed on:

```text
feat/026-supported-mutation-cross-writer-coordination
```

## Specification 026 implementation sequence after authority

1. place/refactor the existing private advisory-lock helper into a dependency-safe location only if required;
2. keep `pregrain.py::_persist` under the existing complete critical section;
3. make `create_child_draft_spec` acquire the same advisory lock before authoring journal creation;
4. preserve `AUTHORING_TRANSACTION_VERSION`, journal schema, recovery classifications, child-ID behavior, and explicit recovery semantics;
5. add deterministic tests for both contention directions and the corrected post-025 race invariant;
6. keep all Specification 025 lock regression and child-authoring recovery tests green;
7. run full regression/static/build/install/CLI verification;
8. prove exact-head permanent five-cell CI;
9. verify exact product diff and runtime dependency count;
10. open/update product PR and recheck exact head/base/scope/CI/reviews/threads/comments/mergeability;
11. merge only with expected-head protection;
12. require canonical post-product CI;
13. reverify historical `v0.3.0` unchanged;
14. complete documentation/evidence closeout and reconciliation if canonically required;
15. re-read live canonical truth and return to observation unless fresh independent evidence selects another bounded unit.

## Historical release preservation

Historical `v0.3.0` remains unchanged:

- source `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release `378962445`;
- wheel digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

Specification 026 shaping does not authorize release work.

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
13. Post-v0.1 product work requires a newly shaped specification derived from live evidence; roadmap deferrals, audits, external reviewers, and upstream-tool comparisons are not implicit implementation authority.

## Program continuation rule

Proceed only through the exact Specification 026 shaping gate. Do not begin product implementation from the candidate branch itself. After any completed canonical unit, re-read live `main` and the full active authority chain before continuing.
