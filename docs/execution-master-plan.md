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
- Specification 025 — Supported Pre-Grain Writer Serialization: `CLOSED_CANONICAL` when this final evidence reconciliation is canonical.

The latest published release remains `v0.3.0` at exact historical source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## Previous closed frontier — Specification 024

Specification 024 remains `CLOSED_CANONICAL`. Its final post-024 normalization merge is `101f018095868fc011c4ebea15dcac64f64d1061`; canonical post-normalization CI `33427947122` succeeded across all five permanent cells.

The invalidated SGB-EXP-001 experiment remains methodology evidence only. It produced no valid comparative dataset, supports no superiority claim, and selects no product authority.

## Specification 025 selection and shaping proof

```text
canonical_base = 101f018095868fc011c4ebea15dcac64f64d1061
observation_head = 58174dbc87e9c02ebbb3a19d38727e1f42149226
fixture_blob = b0852096a6f8916955a6a31b3a785ca8bb0d708d
ci_run = 33431133156
reproduced_gap = SUPPORTED_PRE_GRAIN_MULTI_WRITER_LOST_UPDATE

shaping_head = e12dc2996f663f5d4a98eb5af212deb73ead5eff
shaping_push_ci = 33432149125
shaping_pr = 54
shaping_pr_ci = 33432301056
shaping_merge = e394ab0c7efabbfade91b64bcdf9a11c8146f469
post_shaping_ci = 33432447491
```

Fresh deterministic evidence proved two supported `shape_draft_spec` writers could both report success while one confirmed revision was silently overwritten. ADR-0020 and Specification 025 therefore selected only cooperative project-scoped non-blocking advisory serialization for `src/specgrain/pregrain.py::_persist`.

All shaping CI gates succeeded across the permanent five-cell matrix. Unavailable or skipped review systems were never treated as PASS.

## Specification 025 canonical product proof

Final implementation head:

`bb1fa1406ef9dab6a65c1721378025943ba3f6de`

Exact product diff changed only:

- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

The implementation uses `.specgrain/tmp/pregrain-mutation.lock` as an inert persistent anchor and standard-library Unix/Windows non-blocking advisory locks. It preserves existing exact-preimage, fsync, atomic replacement, postimage, validation, lifecycle, readiness, dependency, and semantic-revision contracts while leaving read-only loading outside the lock.

```text
push_ci = 33434286534
product_pr = 55
product_pr_ci = 33434757539
product_merge = 5e3966fb0db3d8971b5abe19106949001ed55ba9
post_product_ci = 33434910548
```

The final push, PR, and canonical post-product CI each completed `success` across all five permanent cells. PR #55 merged with expected-head protection after exact head/base, scope, mergeability, reviews, threads, and comments were rechecked.

## Specification 025 canonical closeout proof

```text
closeout_head = 885823e0e56dfd3e7c7c8e63d8dacc41b14448f2
closeout_push_ci = 33435480927
closeout_pr = 56
closeout_pr_ci = 33435703680
closeout_merge = e05df4bd046590ee043115c1edbcd7b83163b4ad
post_closeout_ci = 33436130730
```

The closeout diff changed exactly eight documentation/governance/evidence paths. It did not modify product code, tests, workflows, dependencies, package metadata, release assets, or benchmark state.

PR #56 remained on exact base `5e3966fb0db3d8971b5abe19106949001ed55ba9` and exact head `885823e0e56dfd3e7c7c8e63d8dacc41b14448f2`, was mergeable, had no submitted reviews or inline review threads, and merged with expected-head protection as `e05df4bd046590ee043115c1edbcd7b83163b4ad`. Its exact parent is the product merge. Post-closeout CI `33436130730` completed `success` across all five permanent cells.

Qodo was billing-blocked, automatic CodeRabbit review was skipped by repository-star policy, and Cubic was descriptive only where those systems appeared. None was treated as PASS.

## Historical release preservation

After Specification 025 closeout, historical `v0.3.0` remains unchanged:

- source `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release `378962445`;
- wheel digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

## Closed frontier — Specification 025

When this final evidence reconciliation is canonical, Specification 025 is `CLOSED_CANONICAL` and the program state is `POST_025_OBSERVATION`.

There is no active product specification. All currently shaped and authorized product work is complete.

Explicit residuals remain unselected: arbitrary non-cooperating writer coordination, general project-wide or distributed locking, child-authoring redesign, waits/retries/leases, later lifecycle mutation, executor/provider orchestration, verification/evidence mutation, automatic context/network/model behavior, new runtime dependencies, package publication, hosted scope, and benchmark superiority claims.

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

After this final reconciliation becomes canonical and its canonical post-merge CI succeeds, remain in observation/evidence gathering. Do not invent Specification 026 merely to continue activity. Shape another specification only when fresh reproducible evidence against the new live canonical truth selects a bounded product gap.
