# ADR-0021 — Supported Mutation Cross-Writer Coordination

## Status

Accepted for Specification 026 shaping. Product implementation remains blocked until the shaping package is merged canonically and the resulting `main` passes the permanent CI matrix.

## Context

Specification 025 introduced cooperative serialization for supported pre-Grain persistence operations flowing through `src/specgrain/pregrain.py::_persist`. Native child authoring in `src/specgrain/store.py::create_child_draft_spec` remains governed by its recoverable authoring journal and does not participate in that advisory lock.

Post-025 observation reproduces a cross-writer race using only supported public APIs:

```text
canonical_base = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
observation_head = 3b557f91ec80c147b30f797198d736c2b6b42518
fixture_blob = ba8cea9510d09415a5bd4d2f123a72f5c8affee8
ci_run = 33441481985
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION
```

A supported `create_child_draft_spec` call can complete successfully between a supported `shape_draft_spec` writer's final parent preimage check and `os.replace`. The child writer confirms a parent postimage that references the new child and returns success. The pre-Grain writer then overwrites that parent postimage, subsequently fails project revalidation, and leaves its own SHAPED parent mutation stored alongside an orphaned child relationship. The final project is structurally invalid even though the later-returning pre-Grain operation reported failure.

This is narrower than arbitrary filesystem concurrency and materially different from the pre-Grain/pre-Grain lost update closed by Specification 025.

## Decision

Specification 026 will coordinate the existing supported pre-Grain persistence transaction and the existing native child-authoring transaction through one shared project-scoped, non-blocking advisory mutation lock.

The implementation will preserve the existing advisory-lock semantics selected by Specification 025 while making the lock abstraction usable by both writer families without creating a circular import.

### Shared exclusion boundary

Both supported writer families will use one private project-scoped advisory lock anchor:

```text
.specgrain/tmp/pregrain-mutation.lock
```

The historical path is retained to avoid adding a second coordination object or migration requirement. Its meaning is widened only from "supported pre-Grain persistence ownership" to "supported bounded local mutation ownership" for the two explicitly selected writer families.

No public API contract will expose or require callers to manage the lock directly.

### Pre-Grain critical section

The existing pre-Grain `_persist` critical section remains protected exactly as in Specification 025:

```text
validate proposed project state
-> read exact target preimage
-> validate exact preimage against loaded SpecNode
-> create/fsync replacement temp file
-> final exact preimage recheck
-> atomic os.replace
-> exact postimage confirmation
-> reload/validate stored project postimage
```

Existing shape/refine/grain public behavior remains unchanged except that contention with active child authoring fails closed immediately.

### Child-authoring critical section

Native `create_child_draft_spec` will acquire the same advisory lock before it establishes transaction state and hold it through successful completion or recovery of the bounded mutation:

```text
revalidate loaded parent/preimage as required
-> create authoring journal
-> create child file
-> replace parent with child reference
-> confirm parent and child postimages
-> remove/recover authoring journal
```

The lock must be acquired before creating the journal so active pre-Grain persistence cannot coexist with a pending child-authoring transaction.

The existing authoring journal remains authoritative for crash/interruption recovery after journal creation. Advisory exclusion and durable recovery solve different problems and MUST remain separate concepts.

### Lock abstraction placement

The current advisory-lock implementation lives in `pregrain.py`, which imports store primitives. `store.py` therefore cannot safely import that helper without creating a circular dependency.

Implementation may move the private lock abstraction to a narrow dependency-neutral module such as:

```text
src/specgrain/mutation_lock.py
```

or an equivalently safe existing lower-level module.

The moved abstraction must preserve the Specification 025 behavior:

- standard-library only;
- Unix `fcntl.flock(... LOCK_EX | LOCK_NB)`;
- Windows `msvcrt.locking(... LK_NBLCK, 1)`;
- regular non-symlink lock anchor;
- non-blocking contention failure;
- ownership tied to the open descriptor/process rather than file presence;
- no retries, sleeps, timeouts, leases, heartbeats, or stale-owner inference.

### Error behavior

Active contention remains an immediate deterministic `StoreValidationError` located at:

```text
.specgrain/tmp/pregrain-mutation.lock
```

A competing child-authoring call that cannot acquire the lock MUST fail before creating its journal or child file or mutating the parent.

A competing pre-Grain persistence call that cannot acquire the lock MUST fail before target mutation.

### Journal compatibility

This decision does not change:

- `AUTHORING_TRANSACTION_VERSION`;
- authoring journal fields or parse rules;
- recovery state classifications;
- child creation ordering once the shared lock is held;
- exact parent replacement checks;
- child ID semantics;
- explicit recovery API behavior.

No journal migration is authorized.

## Why share one advisory lock

The reproduced race exists precisely because two supported mutation families use different coordination mechanisms over overlapping canonical state. A shared advisory exclusion boundary is the smallest mechanism that prevents either family from entering its mutation transaction while the other is already in a critical section.

Adding pre-Grain awareness of journal presence alone is insufficient because journal observation and `os.replace` would still be separate operations with a race between them. Adding journal awareness of the pre-Grain lock without actually acquiring the same operating-system lock would have the same check-then-act problem.

One shared advisory lock makes the exclusion decision atomic at the operating-system locking primitive while leaving the child journal responsible for recovery semantics.

## Compatibility

This decision:

- does not change SpecNode schema or semantic revision digests;
- does not change lifecycle legality or Grain readiness;
- does not change child-authoring journal schema;
- does not change explicit recovery classifications;
- adds no runtime dependency;
- does not coordinate arbitrary non-SpecGrain writers;
- does not serialize read-only operations;
- does not publish a release.

Existing initialized projects require no migration. The lock anchor already exists lazily for projects that used Specification 025 pre-Grain mutation and remains inert when no process owns its advisory lock.

## Verification requirements

Implementation must prove at minimum:

1. the exact post-025 cross-writer observation topology no longer permits a failed pre-Grain mutation to overwrite a successful child-authoring parent update;
2. when pre-Grain persistence owns the shared lock, a competing `create_child_draft_spec` fails before journal creation, child creation, or parent mutation;
3. when child authoring owns the shared lock, competing shape/refine/grain persistence fails before target mutation;
4. after contention failure, canonical parent/child state remains unchanged by the losing writer;
5. successful sequential child authoring followed by pre-Grain mutation remains valid where lifecycle permits;
6. successful sequential pre-Grain mutation and unrelated child authoring behavior remain compatible with existing lifecycle rules;
7. all existing authoring recovery tests continue to pass;
8. all Specification 025 lock-lifetime, stale-writer, unsafe-anchor, platform, and read-only guarantees remain green;
9. the lock is released after child-authoring success, handled failure, and recovery paths;
10. all permanent Ubuntu, macOS, and Windows CI cells succeed;
11. runtime dependency count remains zero;
12. historical `v0.3.0` remains unchanged.

## Explicit non-goals

This ADR does not authorize:

- coordination with arbitrary manual/non-SpecGrain writers;
- a universal project transaction manager;
- child-authoring journal redesign or version bump;
- distributed/network locking;
- blocking waits, retries, leases, heartbeats, or timeout ownership inference;
- database migration;
- lifecycle expansion;
- execution/provider/result/verification/evidence orchestration;
- automatic context/network/model behavior;
- Spec Kit runtime integration;
- release publication;
- hosted scope;
- benchmark or superiority claims.
