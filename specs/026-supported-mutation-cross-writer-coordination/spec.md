# Specification 026 — Supported Mutation Cross-Writer Coordination

## Status

`PRODUCT_VERIFIED_CLOSEOUT_PENDING`.

The shaped product authority was satisfied by canonical shaping merge `d27e000728823e93d2fce9ecd669629a839bfdb3` and post-shaping CI `33442261877`. The bounded product implementation merged as `69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b`, and canonical post-product CI `33485603844` completed `success` across all five permanent cells.

Specification 026 is not `CLOSED_CANONICAL` until its documentation/evidence closeout and final reconciliation are merged and their canonical post-merge CI gates succeed.

## Outcome

Prevent supported native child authoring and supported pre-Grain persistence from corrupting one another when they overlap on the same local project by making both writer families participate in one existing project-scoped, non-blocking advisory mutation lock, while preserving child-authoring journal recovery, pre-Grain exact-preimage/postimage defenses, lifecycle semantics, dependency-free runtime behavior, and the historical `v0.3.0` release.

## Selection evidence

```text
canonical_base = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
canonical_tree = ffe4dbff9658524eedf359451578a9d0446fed4c
observation_branch = obs/post-025-supported-cross-writer-fixture
observation_head = 3b557f91ec80c147b30f797198d736c2b6b42518
fixture = tests/test_post_025_supported_cross_writer_observation.py
fixture_blob = ba8cea9510d09415a5bd4d2f123a72f5c8affee8
ci_run = 33441481985
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION
```

The observation used only supported public mutation APIs and is independent of the invalidated `SGB-EXP-001` experiment. The earlier observation head `975c47b288cddbfbde34fbbca06afa77ee86f9af` / CI `33441425481` is non-selection evidence because Ruff stopped the harness before test execution.

## Problem statement

Specification 025 serialized concurrent supported pre-Grain writers, but native child authoring used its recoverable journal without participating in that advisory lock. Both writer families could mutate the same DRAFT parent. A supported child authoring call could complete after the pre-Grain writer's final exact preimage check but before `os.replace`; the pre-Grain writer could then overwrite the successful parent postimage and fail only during later full-project validation, leaving structurally invalid stored refinement.

A journal-presence check alone cannot close this race because checking for a journal and replacing the parent are separate operations. The selected gap therefore required one shared operating-system advisory exclusion primitive across the two supported writer families.

## Scope in

- Reuse one project-scoped non-blocking advisory lock for supported pre-Grain persistence and supported native child authoring.
- Preserve the lock anchor `.specgrain/tmp/pregrain-mutation.lock`.
- Place the private lock abstraction so `store.py` and `pregrain.py` can use it without circular imports.
- Acquire the shared lock before native child authoring creates its transaction journal and hold it through completion or handled recovery of that authoring attempt.
- Keep the existing pre-Grain `_persist` critical section under the same shared lock.
- Preserve exact-preimage, temp-file fsync, `os.replace`, exact postimage, full project revalidation, authoring journal, and recovery defenses.
- Add deterministic tests for both contention directions and the corrected reproduced topology.
- Preserve cross-platform standard-library behavior on Ubuntu, macOS, and Windows.
- Preserve runtime dependency count at zero.
- Preserve historical `v0.3.0` identity and assets.

## Scope out

- Coordination with arbitrary manual editors, direct filesystem writes, or non-SpecGrain applications.
- A universal project-wide transaction manager.
- Child-authoring journal schema/version/recovery redesign or automatic hidden recovery.
- Blocking lock acquisition, retries, sleeps, backoff, timeouts, leases, heartbeats, or stale-owner inference.
- Distributed/network/database locking.
- SpecNode schema or semantic revision changes.
- Lifecycle expansion.
- Execution/provider/result/verification/evidence orchestration.
- Automatic context discovery, network access, or model selection.
- Spec Kit runtime integration.
- Release publication or mutation of `v0.3.0`.
- Hosted scope.
- Benchmark or superiority claims.
- Any inspection, search, materialization, reproduction, or use of the invalidated `SGB-EXP-001` hidden scorer.

## Functional requirements

### FR-001 — One shared advisory ownership boundary

Supported pre-Grain persistence and `create_child_draft_spec` MUST acquire the same project-scoped operating-system advisory lock before entering their mutation-critical sections. The lock MUST remain non-blocking and active contention MUST fail immediately with deterministic `StoreValidationError` semantics.

### FR-002 — Child authoring must acquire before transaction state

`create_child_draft_spec` MUST acquire the shared advisory lock before creating `.specgrain/tmp/authoring-transaction.json`. If contention prevents acquisition, the losing call MUST NOT create a journal, child file, or parent mutation.

### FR-003 — Pre-Grain persistence remains fully serialized

The Specification 025 `_persist` boundary MUST remain serialized from proposed-state validation through exact stored-postimage confirmation and full project revalidation. No existing defense may be weakened.

### FR-004 — Journal recovery remains separate and authoritative

The existing authoring journal MUST continue to define recoverable child-authoring interruption states after journal creation. The advisory lock MUST NOT encode transaction state, owner identity, recovery status, or stale-state inference in lock-file contents or presence.

### FR-005 — Safe dependency direction

The shared private lock abstraction MUST be placed so `store.py` and `pregrain.py` can use it without circular imports. No public locking API is authorized.

### FR-006 — Cross-platform standard-library only

The implementation MUST preserve standard-library primitives:

```text
Unix-family = fcntl.flock(fd, LOCK_EX | LOCK_NB)
Windows = msvcrt.locking(fd, LK_NBLCK, 1)
```

### FR-007 — Lock anchor safety and lifetime

The lock anchor MUST remain a regular non-symlink file. Ownership MUST remain tied to the live file descriptor/process, not file presence. Existing process-exit release, handled-failure release, persistent-anchor reuse, and unsafe-anchor fail-closed behavior remain required.

### FR-008 — Read-only behavior remains unlocked

Read-only project loading/checking/selection/packet behavior remains outside the mutation lock unless separately evidenced and authorized.

### FR-009 — No hidden contention policy

The core MUST NOT wait, retry, sleep, back off, or infer timeout ownership. Callers remain responsible for any explicit retry policy outside the deterministic core.

## Acceptance criteria and disposition

1. Corrected-invariant test prevents the reproduced topology from leaving invalid parent/child refinement — **PASS**.
2. Pre-Grain lock ownership makes competing child authoring fail before journal/child/parent side effects — **PASS**.
3. Child-authoring ownership makes competing `shape_draft_spec` fail before target mutation — **PASS**.
4. Refine/grain continue through the same shared `_persist` contention boundary — **PASS** via common lock path and retained Specification 025 coverage.
5. Losing writer does not alter canonical bytes in contention coverage — **PASS**.
6. Successful sequential child authoring remains valid under existing journal semantics — **PASS** through regression.
7. Existing child-authoring recovery fixtures remain green with no journal version/schema change — **PASS**.
8. Specification 025 serialization/lifetime/unsafe-anchor/read-only tests remain green — **PASS**.
9. Ruff, full regression, cleanliness, compileall, source CLI smoke, build, wheel install, and installed CLI smoke pass on exact product head — **PASS**.
10. Permanent five-cell CI succeeds on exact product head and canonical merge — **PASS**.
11. Final product diff contains only the minimum three source/test paths — **PASS**.
12. No runtime dependency added — **PASS**.
13. Historical `v0.3.0` source/release/assets remain unchanged — **PASS**.
14. PR head/base/scope/CI/reviews/comments/threads/mergeability and review-system availability were rechecked without treating unavailable/skipped systems as PASS — **PASS**.
15. Product merge used expected-head protection and canonical post-product CI succeeded — **PASS**.

## Delivered product evidence

```text
shaping_head = 51079a25cdd0f90a9af1cc34ae7577c72ecdf2d6
shaping_push_ci = 33441902147
shaping_pr = 59
shaping_pr_ci = 33442057984
shaping_merge = d27e000728823e93d2fce9ecd669629a839bfdb3
post_shaping_ci = 33442261877

final_product_head = 24728cd52b2daef2c83c5b83f084421b8096a11f
push_ci = 33443061640
product_pr = 60
product_pr_ci = 33443161567
product_merge = 69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b
post_product_ci = 33485603844
```

The first final-logic head `fd27a146b8c39c777b5fb3f1611b2689a1fad3d5` / CI `33442865903` is explicitly not acceptance evidence because Ruff source stopped the run before tests. The subsequent change normalized imports only.

## Risk

`medium`

The selected boundary touched two persistence paths and cross-platform locking. The delivered implementation keeps the lock helper private, leaves durable recovery in the journal, adds no schema migration, and preserves rollback by reverting the bounded implementation commits.

## Recovery

Revert the bounded Specification 026 product merge/implementation to restore exact Specification 025 behavior. No schema or journal migration is required.

## Context

```text
budget_tokens = 8000
estimated_tokens = 5500
```

## Product change surface

Delivered product surface:

```text
src/specgrain/store.py
src/specgrain/pregrain.py
tests/test_pregrain_serialization.py
```

No new private module was required.

## Historical release preservation

```text
tag = v0.3.0
source = 70dd66aba0e68ae710e6ef12605ed153d107bab4
release_id = 378962445
wheel_asset = 535129008
wheel_sha256 = b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817
source_asset = 535129009
source_sha256 = e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835
```

## Minimality choice

`native`

The delivered solution extends the advisory serialization primitive already proven by Specification 025 to exactly one additional supported mutation family selected by fresh evidence. No broader transaction framework was introduced.

## Safety status

`requirements-defined`

Safety requirements remain satisfied at the product gate: fail closed before mutation on contention; preserve explicit journal recovery; preserve exact-preimage/postimage validation; reject unsafe anchors; release advisory ownership on handled paths/process exit; no hidden waiting/retry/timeout policy; no runtime dependency; no historical release mutation; no use of invalidated hidden-scorer material.

## Closeout authority gate

```text
SHAPING_JUSTIFIED = true
IMPLEMENTATION_AUTHORIZED = true
PRODUCT_MERGED = true
POST_PRODUCT_VERIFIED = true
CLOSED_CANONICAL = false
```

Only documentation/evidence closeout and final reconciliation remain. No further Specification 026 product implementation is authorized.