# Specification 026 — Supported Mutation Cross-Writer Coordination

## Status

`SHAPED_CANDIDATE`.

Product implementation is not authorized until this documentation/governance-only shaping package is merged canonically and the resulting `main` passes the permanent five-cell CI matrix.

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

The observation uses only supported public mutation APIs and is independent of the invalidated `SGB-EXP-001` experiment.

The reproduced topology is:

```text
shape_draft_spec(parent)
  -> passes final exact preimage check inside pre-Grain persistence
  -> pauses before os.replace

create_child_draft_spec(parent)
  -> creates recoverable journal
  -> creates child DRAFT
  -> updates parent children
  -> confirms both postimages
  -> removes journal
  -> returns success

shape_draft_spec resumes
  -> os.replace overwrites the successful child-parent postimage
  -> stores a SHAPED parent with the stale children list
  -> project revalidation detects structural invalidity
  -> raises StoreValidationError after mutation already occurred
```

The final store contains the child file but the SHAPED parent no longer references it. The failed pre-Grain operation is therefore not mutation-free and has invalidated a supported writer's successfully confirmed result.

## Problem statement

Specification 025 correctly prevents concurrent supported pre-Grain writers from silently overwriting one another, but its advisory lock is private to `pregrain.py::_persist`. Native child authoring uses a separate journal transaction in `store.py` and does not acquire that lock.

Both writer families can mutate the same DRAFT parent file. Because neither mechanism excludes the other, they can interleave after exact preimage checks and before replacement.

A journal-presence check alone cannot close this race because checking for a journal and replacing the parent would still be separate operations. The selected gap therefore requires one shared operating-system advisory exclusion primitive across the two supported writer families.

## Scope in

- Reuse one project-scoped non-blocking advisory lock for supported pre-Grain persistence and supported native child authoring.
- Preserve the current lock anchor path `.specgrain/tmp/pregrain-mutation.lock` unless implementation evidence proves a migration-free equivalent is required.
- Move or refactor the current private lock abstraction only as needed to make it safely importable by both `store.py` and `pregrain.py` without a circular import.
- Acquire the shared lock before native child authoring creates its transaction journal and hold it through completion or handled recovery of that authoring attempt.
- Keep the existing pre-Grain `_persist` critical section under the same shared lock.
- Preserve all existing exact-preimage, temp-file fsync, `os.replace`, exact postimage, full project revalidation, authoring journal, and recovery defenses.
- Add deterministic focused tests for both contention directions and the exact reproduced cross-writer topology.
- Preserve cross-platform standard-library behavior on Ubuntu, macOS, and Windows.
- Preserve runtime dependency count at zero.
- Preserve historical `v0.3.0` identity and assets.

## Scope out

- Coordination with arbitrary manual editors, direct filesystem writes, or non-SpecGrain applications.
- A universal project-wide transaction manager for all future mutation families.
- Child-authoring journal schema changes, version changes, recovery-state redesign, or automatic hidden recovery.
- Blocking lock acquisition, retry loops, sleeps, backoff, timeouts, leases, heartbeats, or stale-owner inference.
- Distributed/network/database locking.
- SpecNode schema or semantic revision changes.
- New lifecycle states or later lifecycle transitions.
- Execution/provider/result/verification/evidence orchestration.
- Automatic context discovery, network access, or model selection.
- Spec Kit runtime integration.
- Release publication or mutation of `v0.3.0`.
- Hosted scope.
- Benchmark or superiority claims.
- Any inspection, search, materialization, reproduction, or use of the invalidated `SGB-EXP-001` hidden scorer.

## Functional requirements

### FR-001 — One shared advisory ownership boundary

Supported pre-Grain persistence and `create_child_draft_spec` MUST acquire the same project-scoped operating-system advisory lock before entering their mutation-critical sections.

The lock MUST remain non-blocking. Active contention MUST fail immediately with deterministic `StoreValidationError` semantics.

### FR-002 — Child authoring must acquire before transaction state

`create_child_draft_spec` MUST acquire the shared advisory lock before creating `.specgrain/tmp/authoring-transaction.json`.

If contention prevents acquisition, the losing call MUST NOT create a journal, child file, or parent mutation.

### FR-003 — Pre-Grain persistence remains fully serialized

The Specification 025 `_persist` boundary MUST remain serialized from proposed-state validation through exact stored-postimage confirmation and full project revalidation.

No existing defense may be weakened to accommodate the shared lock.

### FR-004 — Journal recovery remains separate and authoritative

The existing authoring journal MUST continue to define recoverable child-authoring interruption states after journal creation.

The advisory lock MUST NOT encode transaction state, owner identity, recovery status, or stale-state inference in lock-file contents or presence.

### FR-005 — Safe dependency direction

The shared private lock abstraction MUST be placed so `store.py` and `pregrain.py` can use it without circular imports.

No public locking API is required or authorized.

### FR-006 — Cross-platform standard-library only

The implementation MUST preserve the standard-library-only operating-system primitives selected by ADR-0021 / Specification 025 behavior:

```text
Unix-family = fcntl.flock(fd, LOCK_EX | LOCK_NB)
Windows = msvcrt.locking(fd, LK_NBLCK, 1)
```

The exact implementation head MUST pass the permanent CI matrix rather than relying on documentation claims.

### FR-007 — Lock anchor safety and lifetime

The lock anchor MUST remain a regular non-symlink file. Ownership MUST remain tied to the live file descriptor/process, not file presence.

Existing process-exit release, handled-failure release, persistent-anchor reuse, and unsafe-anchor fail-closed behavior MUST remain valid.

### FR-008 — Read-only behavior remains unlocked

Read-only project loading/checking/selection/packet behavior MUST remain outside the mutation lock unless independently evidenced and separately authorized.

### FR-009 — No hidden contention policy

The core MUST NOT wait, retry, sleep, back off, or infer timeout ownership. Callers remain responsible for any explicit retry policy outside the deterministic core.

## Acceptance criteria

1. The final product head includes a corrected-invariant test derived from the post-025 observation and proves that the reproduced topology cannot leave invalid parent/child refinement.
2. With pre-Grain persistence holding the shared lock, a competing `create_child_draft_spec` fails closed before journal creation, child creation, or parent mutation.
3. With child authoring holding the shared lock, competing `shape_draft_spec` fails closed before target mutation.
4. Equivalent contention behavior is covered for pre-Grain refine/grain persistence through their common `_persist` path.
5. The losing writer cannot alter canonical parent/child bytes in a contention test.
6. Successful sequential child authoring remains valid and recoverable under existing journal semantics.
7. Existing child-authoring recovery fixtures remain green without journal-version or schema changes.
8. Existing Specification 025 serialization, stale-writer, success/failure release, process-exit release, persistent-anchor, unsafe-anchor, shape/refine/grain, and read-only tests remain green.
9. Full regression, Ruff, compileall, source CLI smoke, package build, built-wheel install, and installed CLI smoke pass on the exact product head.
10. Permanent CI succeeds on Ubuntu/Python 3.11, Ubuntu/Python 3.12, Ubuntu/Python 3.13, macOS/Python 3.11, and Windows/Python 3.11.
11. The final product diff contains only the minimum source/test surface justified by this specification.
12. No runtime dependency is added.
13. `v0.3.0` still points to `70dd66aba0e68ae710e6ef12605ed153d107bab4`, Release `378962445`, with the historical wheel/source digests unchanged.
14. Review, comments, threads, mergeability, exact head/base, and CI are rechecked immediately before merge; unavailable/skipped review systems are recorded as unavailable/skipped, never PASS.
15. Product merge uses expected-head protection and canonical post-merge CI succeeds before closeout proceeds.

## Risk

`medium`

This change touches two persistence paths and a cross-platform lock abstraction. The boundary is intentionally small, but an incorrectly placed lock could interfere with child recovery or create a circular import. Verification therefore requires exact contention-direction tests, recovery regression, and the permanent cross-platform matrix.

## Recovery

Revert the bounded implementation commits to restore the exact Specification 025 behavior. No schema or journal migration is permitted, so rollback must not require data conversion.

## Context

```text
budget_tokens = 8000
estimated_tokens = 5500
```

## Change surface

Expected product surface:

```text
src/specgrain/pregrain.py
src/specgrain/store.py
src/specgrain/mutation_lock.py   # only if a dependency-neutral helper is required
tests/test_pregrain_serialization.py
tests/test_store_authoring.py    # or the existing canonical child-authoring focused module
```

A smaller equivalent surface is preferred. A new private module is authorized only to avoid circular import and centralize the already-selected advisory lock implementation.

Documentation/evidence closeout may later update only the Specification 026 authority chain and canonical program-state documents necessary to record verified truth.

## Evidence required

- Exact post-025 selection evidence above.
- Exact shaping head/base/diff and permanent shaping CI.
- Exact canonical post-shaping merge and five-cell CI before product work starts.
- Focused corrected-invariant and two-direction contention tests.
- Child-authoring recovery regression.
- Specification 025 lock regression.
- Full exact-head CI and package verification.
- Exact product PR head/base/scope, comments, threads, reviews, mergeability, and expected-head merge evidence.
- Canonical post-product CI.
- Historical release preservation evidence.
- Documentation-only closeout and reconciliation if required by canonical governance.

## Minimality choice

`native`

The smallest justified solution extends the advisory serialization primitive already selected and proven by Specification 025 to the one additional supported mutation family that fresh evidence shows can overlap the same canonical parent state. No broader transaction framework is selected.

## Safety status

`requirements-defined`

Safety requirements:

- fail closed before mutation on lock contention;
- preserve explicit journal recovery after journal creation;
- do not weaken exact-preimage/postimage validation;
- reject unsafe lock anchors;
- release advisory ownership on all handled paths and process exit;
- no hidden waiting/retry/timeout policy;
- no runtime dependency addition;
- no historical release mutation;
- no use of invalidated benchmark hidden-scorer material.

## Authority gate

```text
SHAPING_JUSTIFIED = true
IMPLEMENTATION_AUTHORIZED = false
```

Implementation becomes authorized only after:

1. this shaping package is reviewed as documentation/governance-only and merged with exact-head protection;
2. canonical `main` is re-read after that merge;
3. the permanent five-cell CI matrix completes `success` on the exact canonical shaping merge;
4. no new live repository fact supersedes this authority.
