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
- Specification 026 — Supported Mutation Cross-Writer Coordination: `PRODUCT_VERIFIED_CLOSEOUT_PENDING`.

The latest published release remains `v0.3.0` at exact historical source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## Closed frontier — Specification 025

Specification 025 remains `CLOSED_CANONICAL`. Its final normalized post-closeout state is anchored by:

```text
product_merge = 5e3966fb0db3d8971b5abe19106949001ed55ba9
post_product_ci = 33434910548
reconciliation_merge = 8a0da2908f6251100a0d7ab71178c2a7c3ed64bb
post_reconciliation_ci = 33437077692
post_normalization_merge = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
post_normalization_ci = 33440739066
```

Unavailable or skipped review systems were never treated as PASS.

## Specification 026 selection

Fresh reproducible evidence against exact canonical baseline `1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1` independently selected:

```text
observation_branch = obs/post-025-supported-cross-writer-fixture
observation_head = 3b557f91ec80c147b30f797198d736c2b6b42518
fixture_blob = ba8cea9510d09415a5bd4d2f123a72f5c8affee8
ci_run = 33441481985
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION
```

The fixture used only supported `shape_draft_spec` and `create_child_draft_spec` APIs. Native child authoring could complete after the pre-Grain writer's final exact parent preimage check but before `os.replace`; the pre-Grain writer could then overwrite the successful parent postimage and leave structurally invalid refinement before failing full-project revalidation.

The earlier observation head `975c47b288cddbfbde34fbbca06afa77ee86f9af` / CI `33441425481` remains harness-invalid for selection because Ruff stopped before the fixture ran.

Selection record: `docs/research/post-025-supported-cross-writer-reproduction-2026-09-01.md`  
Architectural decision: `docs/adr/0021-supported-mutation-cross-writer-coordination.md`

## Specification 026 canonical shaping proof

```text
shaping_base = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
shaping_head = 51079a25cdd0f90a9af1cc34ae7577c72ecdf2d6
shaping_push_ci = 33441902147
shaping_pr = 59
shaping_pr_ci = 33442057984
shaping_merge = d27e000728823e93d2fce9ecd669629a839bfdb3
post_shaping_ci = 33442261877
```

The shaping diff was documentation/governance/evidence only. Permanent push, PR, and canonical post-shaping CI all succeeded across Ubuntu/Python 3.11, Ubuntu/Python 3.12, Ubuntu/Python 3.13, macOS/Python 3.11, and Windows/Python 3.11 before implementation authority became live.

## Specification 026 canonical product proof

Final implementation head:

```text
24728cd52b2daef2c83c5b83f084421b8096a11f
```

Exact product diff changed only:

- `src/specgrain/store.py`;
- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

The implementation reuses the existing `.specgrain/tmp/pregrain-mutation.lock` project-scoped non-blocking advisory anchor for both supported pre-Grain persistence and native child authoring. The private lock implementation moved to lower-level `store.py`; `pregrain.py` reuses the identical callable. Child authoring acquires the lock before journal creation and holds it through normal completion or handled recovery. The existing journal remains the separate durable recovery mechanism.

Specification 025 preimage/postimage, unsafe-anchor, platform, descriptor/process lifetime, persistent-anchor, shape/refine/grain, and read-only guarantees remain required and covered. `AUTHORING_TRANSACTION_VERSION`, journal schema, recovery classifications, lifecycle rules, child-ID behavior, and runtime dependency count remain unchanged.

```text
first_final_logic_head = fd27a146b8c39c777b5fb3f1611b2689a1fad3d5
first_final_logic_ci = 33442865903
first_final_logic_result = Ruff failure before tests; not acceptance evidence

final_product_head = 24728cd52b2daef2c83c5b83f084421b8096a11f
push_ci = 33443061640
product_pr = 60
product_pr_ci = 33443161567
product_merge = 69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b
post_product_ci = 33485603844
```

Final push CI, PR CI, and canonical post-product CI completed `success` across all five permanent cells.

At the final PR #60 merge gate:

```text
base = d27e000728823e93d2fce9ecd669629a839bfdb3
head = 24728cd52b2daef2c83c5b83f084421b8096a11f
changed_files = 3
mergeable = true
submitted_reviews = 0
inline_review_threads = 0
```

Qodo was billing-blocked, automatic CodeRabbit review was skipped by repository-star policy, and Cubic was neutral because its monthly review line limit was reached. None was treated as PASS. PR #60 merged with expected-head protection.

## Specification 026 delivered boundary

Delivered authority is limited to cooperative mutual exclusion between:

1. pre-Grain persistence through `src/specgrain/pregrain.py::_persist`;
2. native child authoring through `src/specgrain/store.py::create_child_draft_spec`.

Explicit non-authority remains:

- arbitrary manual/non-SpecGrain writer coordination;
- universal project transaction management;
- child-authoring journal schema/version/recovery redesign;
- distributed/network/database locking;
- blocking waits, retries, sleeps, backoff, leases, heartbeats, or timeout ownership inference;
- runtime dependencies;
- lifecycle expansion;
- executor/provider/result/verification/evidence orchestration;
- automatic context/network/model behavior;
- Spec Kit runtime adoption;
- release publication;
- hosted scope;
- benchmark or superiority claims.

The invalidated `SGB-EXP-001` hidden scorer remains outside inspection/search/materialization/reproduction/use authority.

## Historical release preservation

Historical `v0.3.0` remains unchanged after the Specification 026 product merge:

- source `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release `378962445`;
- wheel asset `535129008`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset `535129009`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

Specification 026 does not authorize release work.

## Specification 026 closeout sequence

Product work is complete and no further Specification 026 product mutation is authorized. Remaining closeout is documentation/governance/evidence only:

1. record exact verification, review, and closeout evidence;
2. reconcile `spec.md`, `tasks.md`, `specs/CURRENT.md`, this master plan, and the roadmap without widening authority;
3. qualify the exact closeout head and documentation-only diff with permanent push CI;
4. open/update closeout PR and recheck exact head/base/scope/PR CI/reviews/comments/threads/mergeability and review-system availability;
5. merge only with expected-head protection;
6. require canonical post-closeout five-cell CI;
7. create one final evidence reconciliation recording exact closeout merge/CI facts and `CLOSED_CANONICAL` disposition;
8. qualify and merge that reconciliation with expected-head protection;
9. require canonical post-reconciliation five-cell CI;
10. reverify `v0.3.0`, re-read all canonical authority, and return to observation unless fresh reproducible evidence independently selects another bounded product gap.

## Cross-spec execution rules

1. Live GitHub/repository truth overrides chat handoffs.
2. No force-push, rebase, or destructive shared-history rewriting.
3. Use bounded feature branches and pull requests.
4. Verify exact PR head, checks, threads, comments, scope, and mergeability before merge.
5. Merge with expected-head protection where available.
6. Never claim PASS, VERIFIED, MERGED, COMPLETE, or `CLOSED_CANONICAL` without exact evidence.
7. Re-read canonical `main` after every merge.
8. Prefer smaller native implementations over dependencies without demonstrated need.
9. Do not execute untrusted repository commands merely to inspect a brownfield project.
10. Do not make AI reasoning transcripts repository authority.
11. Preserve residual risks and blockers.
12. External ideas/code require license-aware provenance.
13. Post-v0.1 product work requires a newly shaped specification derived from live evidence; deferred roadmap categories, audits, external reviewers, and upstream-tool comparisons are not implicit implementation authority.

## Program continuation rule

Complete only the exact Specification 026 closeout/reconciliation sequence. After canonical closure, return to observation/evidence gathering. Do not invent Specification 027 merely to continue activity; shape a successor only when fresh reproducible evidence against live canonical truth selects a bounded product gap.
