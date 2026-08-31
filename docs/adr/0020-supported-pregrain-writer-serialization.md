# ADR-0020 — Supported Pre-Grain Writer Serialization

## Status

Accepted for Specification 025 shaping. Product implementation remains blocked until the shaping package is merged canonically and the resulting `main` passes the permanent CI matrix.

## Context

ADR-0018 deliberately avoided broad cross-process locking for recoverable child authoring and does not promise coordination with arbitrary non-cooperating file edits.

Post-024 observation now provides a narrower and materially different fact: two supported public `shape_draft_spec` calls can both return success while one successful semantic revision is silently lost.

Exact selection evidence:

```text
canonical_base = 101f018095868fc011c4ebea15dcac64f64d1061
observation_head = 58174dbc87e9c02ebbb3a19d38727e1f42149226
fixture_blob = b0852096a6f8916955a6a31b3a785ca8bb0d708d
ci_run = 33431133156
ci_result = completed/success across all five permanent cells
```

The race exists because `_replace_spec_exact` performs a final preimage check and then a separate unconditional `os.replace`. A supported competing writer can commit between those operations.

SpecGrain needs a cooperative boundary for its own supported pre-Grain persistence operations without claiming universal filesystem coordination.

## Decision

Specification 025 will serialize supported pre-Grain persistence transactions cooperatively at the project level.

The implementation will introduce one private non-blocking advisory lock abstraction used by `src/specgrain/pregrain.py::_persist`.

### Lock scope

The lock is held around the complete persistence-critical section:

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

The lock is acquired before this section and released after success or failure.

The public shaping/refining/grain APIs and their lifecycle semantics remain unchanged.

### Lock anchor

Use one project-scoped regular-file anchor under:

```text
.specgrain/tmp/pregrain-mutation.lock
```

The anchor is runtime coordination metadata only. Its existence does not mean a transaction is active and MUST NOT be interpreted as ownership or stale state.

The anchor may persist after operations. Active ownership exists only while the operating system holds the advisory lock for an open file descriptor.

### Platform primitives

Use only Python standard-library platform primitives:

- Unix-family supported runners: `fcntl.flock(fd, LOCK_EX | LOCK_NB)`;
- Windows: `msvcrt.locking(fd, LK_NBLCK, 1)` from byte offset zero.

The implementation must keep platform-specific imports private and conditional so importing SpecGrain remains portable.

The lock acquisition is non-blocking. If another supported pre-Grain persistence transaction holds the lock, the second mutation fails immediately with a deterministic `StoreValidationError` rather than waiting, retrying, or racing.

### Lifetime and crash behavior

The lock is tied to the open descriptor/process, not to lock-file presence. Normal `finally` cleanup releases/closes the descriptor. Process termination must not leave a logically owned stale lock that requires timeout inference.

The implementation must include subprocess evidence that a lock held by a process is acquirable again after that process exits.

### Existing defenses remain

The exact-preimage checks, temp-file fsync, `os.replace`, exact postimage check, and full project revalidation remain in place. Serialization is an additional supported-writer guarantee, not a replacement for current validation.

## Why advisory serialization instead of a transaction marker

A create-if-absent transaction marker could serialize writers, but marker presence survives process death and therefore requires durable ownership/recovery semantics, stale-owner decisions, or explicit recovery state. That is unnecessary for the reproduced single-file pre-Grain race.

Operating-system advisory locks provide the narrower property required by the evidence: cooperative supported writers exclude one another while a descriptor is alive, and ownership is not inferred from persistent metadata.

## Why non-blocking

SpecGrain is fail-closed and deterministic. A bounded CLI/library mutation should not hide contention behind scheduler-dependent waits or timeouts. Immediate contention failure is observable, testable, and retryable by the caller without introducing implicit retry policy into the core.

## Compatibility

This decision:

- does not change SpecNode schema or revision-digest semantics;
- does not change lifecycle legality;
- does not change Grain readiness;
- does not change child-authoring journal semantics;
- does not add a runtime dependency;
- does not coordinate arbitrary non-SpecGrain writers;
- does not change read-only commands;
- does not publish a release.

Existing initialized projects need no migration. The lock anchor is lazily created under existing runtime `.specgrain/tmp/` storage and is not canonical product data.

## Security and filesystem boundary

The lock anchor must be a regular non-symlink file. The implementation must fail closed on an unsafe anchor rather than follow a symlink or treat a directory/device as a lock.

No claim is made for distributed filesystems whose advisory-lock semantics do not match the supported local filesystem contract.

## Verification requirements

Implementation must prove at minimum:

1. the exact supported-writer lost-update fixture no longer permits two successful competing writes;
2. one writer succeeds while the injected competitor fails closed on lock contention;
3. the successful writer's canonical postimage is preserved;
4. the existing exact-preimage drift checks still reject non-lock-mediated drift detected before replacement;
5. lock release occurs after success and every handled failure;
6. a subprocess/process exit releases ownership so a later mutation can acquire the same persistent anchor;
7. unsafe lock-anchor types fail closed;
8. all three supported pre-Grain persistence paths (`shape`, `refine`, `grain`) use the same serialization boundary;
9. read-only operations do not acquire the lock;
10. permanent Ubuntu, macOS, and Windows CI remains green;
11. runtime dependency count remains zero;
12. historical `v0.3.0` identity remains unchanged.

## Consequences

Supported pre-Grain writers become mutually exclusive only during persistence. Concurrent callers may still perform earlier pure computation concurrently, but stale callers fail before mutation once they enter the serialized persistence section.

A caller encountering active contention receives an immediate error and may choose its own retry policy outside the deterministic core.

The persistent anchor is expected runtime metadata and may remain present after successful operations without representing pending recovery work.

## Explicit non-goals

This ADR does not authorize:

- general project-wide writer serialization;
- child-authoring lock redesign;
- coordination with manual edits or other applications;
- distributed locks;
- lease expiry or stale-owner heuristics;
- blocking waits or automatic retries;
- database migration;
- lifecycle expansion;
- execution/provider/verification/evidence orchestration;
- release publication.
