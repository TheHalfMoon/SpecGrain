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
- Specification 024 — Native WorkPacket Export: `CLOSED_CANONICAL`; bounded read-only native export from one dependency-eligible stored `GRAIN`.
- Specification 025 — Supported Pre-Grain Writer Serialization: `CLOSEOUT_CANDIDATE`; product is canonical and post-product verified, while documentation-only closeout remains active.

The latest published release remains `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## Specification 024 closed frontier

Specification 024 remains `CLOSED_CANONICAL`. Its final post-024 normalization merge is `101f018095868fc011c4ebea15dcac64f64d1061`, and canonical post-normalization CI `33427947122` succeeded across all five permanent cells.

The invalidated SGB-EXP-001 experiment remains methodology evidence only. It produced no valid comparative dataset, supports no superiority claim, and selects no current product authority.

## Specification 025 selection proof

Fresh deterministic post-024 evidence independently selected the supported pre-Grain writer race:

```text
canonical_base = 101f018095868fc011c4ebea15dcac64f64d1061
observation_head = 58174dbc87e9c02ebbb3a19d38727e1f42149226
fixture_blob = b0852096a6f8916955a6a31b3a785ca8bb0d708d
ci_run = 33431133156
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_PRE_GRAIN_MULTI_WRITER_LOST_UPDATE
```

The final fixture uses two supported `shape_draft_spec` calls. Writer B commits and confirms a distinct SHAPED revision while writer A is paused after its final preimage check; writer A then resumes `os.replace`, silently removes writer B's successful revision, confirms its own postimage, and also returns success.

Selection evidence:

`docs/research/post-024-supported-pregrain-multi-writer-reproduction-2026-08-31.md`

Architectural decision:

`docs/adr/0020-supported-pregrain-writer-serialization.md`

## Specification 025 shaping proof

```text
shaping_head = e12dc2996f663f5d4a98eb5af212deb73ead5eff
push_ci = 33432149125
pr = 54
pr_ci = 33432301056
shaping_merge = e394ab0c7efabbfade91b64bcdf9a11c8146f469
post_shaping_ci = 33432447491
```

Every shaping CI gate succeeded across the permanent five-cell matrix. PR #54 had no submitted reviews or inline review threads at the merge gate; Qodo was billing-blocked, CodeRabbit automatic review was skipped by repository-star policy, and Cubic was descriptive only. None was treated as PASS.

The shaping merge authorized exactly:

```text
cooperative project-scoped non-blocking advisory serialization
for src/specgrain/pregrain.py::_persist
```

## Specification 025 canonical product proof

Final implementation head:

`bb1fa1406ef9dab6a65c1721378025943ba3f6de`

Exact product diff from the shaping merge changed only:

- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

The implementation uses `.specgrain/tmp/pregrain-mutation.lock` as an inert persistent anchor and conditional standard-library `fcntl` / `msvcrt` non-blocking advisory locks. It preserves existing exact-preimage checks, temporary-file fsync, atomic replacement, postimage confirmation, project validation, lifecycle, readiness, dependency, and semantic-digest contracts.

Product verification:

```text
push_ci = 33434286534
product_pr = 55
product_pr_ci = 33434757539
product_merge = 5e3966fb0db3d8971b5abe19106949001ed55ba9
post_product_ci = 33434910548
```

The final push CI, PR CI, and canonical post-product CI each completed `success` across all five permanent cells. macOS/Python 3.11 on the final push head recorded `600 passed` plus all configured static, cleanliness, package-build, install, and CLI smoke gates.

At the PR #55 merge gate, exact head/base and the two-file diff remained unchanged, mergeability was true, and no submitted reviews or inline review threads were present. Qodo was billing-blocked, automatic CodeRabbit review was skipped, and Cubic was descriptive only. No unavailable or skipped system was treated as PASS.

PR #55 merged with expected-head protection as `5e3966fb0db3d8971b5abe19106949001ed55ba9`, with parents `e394ab0c7efabbfade91b64bcdf9a11c8146f469` and `bb1fa1406ef9dab6a65c1721378025943ba3f6de`.

## Historical release preservation

After the Specification 025 product merge, historical `v0.3.0` remains unchanged:

- source `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release `378962445`;
- wheel digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

## Active closeout frontier — Specification 025

Product mutation is complete. The active authority is documentation-only closeout.

The closeout package may update only Specification 025 evidence/status/governance records and program-level status documents. It must not modify product code, tests, workflows, dependencies, package metadata, release assets, or benchmark state.

Remaining gates:

1. exact-head closeout CI succeeds across all five permanent cells;
2. closeout diff remains documentation/governance/evidence-only;
3. closeout PR exact head/base, reviews, inline threads, comments, and mergeability are rechecked without treating unavailable systems as PASS;
4. closeout PR merges with expected-head protection;
5. canonical post-closeout CI succeeds across all five permanent cells;
6. historical `v0.3.0` identity is reverified;
7. final evidence reconciliation records the exact closeout merge/post-closeout evidence;
8. only then may `CLOSED_CANONICAL` be published and the program return to observation.

## Explicitly unselected after Specification 025

Without separately shaped evidence, do not implement:

- coordination with arbitrary manual/non-SpecGrain writers;
- general project-wide locking or child-authoring journal redesign;
- distributed/network locking;
- blocking waits, retries, leases, heartbeats, or stale-owner timeout inference;
- `GRAIN -> READY` or later lifecycle mutation;
- executor/provider invocation or result orchestration;
- verification execution or evidence mutation;
- automatic context discovery, source-content packing, retrieval, network access, or LLM context selection;
- new runtime dependencies;
- PyPI publication or broader distribution changes;
- hosted SaaS, dashboard, account/enterprise, or provider runtime scope;
- Spec Kit preset/hook/extension/bundle/workflow execution or architectural adoption;
- arbitrary Markdown semantic inference;
- empirical benchmark superiority claims without a reproducible completed dataset.

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

Finish Specification 025 only through its bounded documentation closeout, canonical post-closeout verification, and final evidence reconciliation. After canonical closure, return to observation/evidence gathering. Do not invent a successor merely to continue activity; shape another specification only when fresh reproducible evidence against the new live canonical truth selects a bounded product gap.