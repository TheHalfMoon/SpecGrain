# Plan 025 — Supported Pre-Grain Writer Serialization

## Objective

Close the reproduced supported pre-Grain lost-update race with the smallest cooperative coordination boundary: serialize only the existing `pregrain.py::_persist` transaction using a project-scoped non-blocking advisory lock while preserving all current exact-preimage and postimage defenses.

## Canonical shaping base

```text
101f018095868fc011c4ebea15dcac64f64d1061
```

Selection evidence is fixed to final observation head `58174dbc87e9c02ebbb3a19d38727e1f42149226`, fixture blob `b0852096a6f8916955a6a31b3a785ca8bb0d708d`, and successful permanent CI run `33431133156`.

Implementation MUST NOT begin until the shaping PR is merged with expected-head protection and the resulting canonical `main` passes the permanent five-cell CI matrix.

Planned implementation branch after that gate:

```text
feat/025-supported-pregrain-writer-serialization
```

## Change strategy

### 1. Keep serialization private to pre-Grain persistence

Add a private context-managed lock abstraction in `src/specgrain/pregrain.py` and acquire it only inside `_persist` around the persistence-critical section.

Do not add a new public API, CLI command, schema field, lifecycle state, or package dependency.

### 2. Create/open one inert lock anchor safely

Use:

```text
.specgrain/tmp/pregrain-mutation.lock
```

Resolve the existing project root/tmp boundary using current store helpers where possible rather than duplicating store-layout authority.

Open/create the anchor with standard-library filesystem primitives. Reject an existing symlink or non-regular anchor before treating it as a lock target. Where the platform exposes a no-follow open flag, use it as defense in depth and verify the opened descriptor refers to a regular file.

The file may remain after use. Its bytes and presence do not represent transaction state.

### 3. Implement one non-blocking cross-platform advisory lock helper

Use conditional standard-library imports only inside the platform branch:

```text
if os.name == "nt":
    msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
else:
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
```

For Windows, seek the descriptor to byte offset zero before lock/unlock. The platform primitive may lock one byte beyond EOF; no semantic lock-file payload is required.

Map active-lock contention to one stable `StoreValidationError` at:

```text
.specgrain/tmp/pregrain-mutation.lock
```

Do not retry or sleep.

Other filesystem/open/lock errors remain distinct fail-closed storage errors rather than being mislabeled as contention.

### 4. Hold the lock around the existing critical section

Inside `_persist`, acquire the advisory lock before `_validate_proposed` and hold it through:

- proposed project validation;
- target preimage read and `SpecNode` comparison;
- `_replace_spec_exact`;
- exact postimage check;
- `_validated_project` reload and expected-postimage confirmation.

This ensures a competing supported pre-Grain persistence call cannot commit between another writer's final preimage check and replacement.

Earlier pure computation in public APIs may remain concurrent. A caller that becomes stale before entering `_persist` must fail against the existing preimage comparison after it eventually acquires the lock.

### 5. Preserve current mutation implementation

Do not remove or weaken:

- `_replace_spec_exact` preimage checks;
- temporary-file fsync;
- `os.replace`;
- postimage confirmation;
- project revalidation;
- readiness/lifecycle/dependency checks.

### 6. Focused test proof

Extend focused pre-Grain tests with deterministic concurrency injection and lock-lifetime evidence.

Required focused cases:

- injected supported writer at writer A's final replace boundary now fails with active-lock contention instead of returning success;
- writer A succeeds and final state matches writer A;
- stale precomputed writer fails exact-preimage validation after lock release rather than overwriting;
- sequential shape/refine/grain operations still succeed with the persistent anchor present;
- lock is released after successful operation;
- lock is released after synthetic `_replace_spec_exact` failure;
- subprocess obtains the advisory lock and exits; subsequent mutation succeeds without deleting the anchor or waiting for a lease timeout;
- unsafe symlink/non-file anchor fails closed where platform capability permits deterministic construction;
- read-only load/check/next/packet behavior is unchanged;
- existing pre-Grain focused suite remains green.

The prior observation fixture stays on the observation branch and is not automatically merged into product history. Product tests should encode the corrected invariant rather than preserve a test whose expected behavior is the defect.

### 7. Cross-platform implementation proof

The permanent CI matrix is part of the feature acceptance boundary because the implementation deliberately uses separate standard-library Unix and Windows lock primitives.

No platform is considered covered merely because the corresponding Python documentation exists; the exact implementation head must pass the repository's Ubuntu, macOS, and Windows cells.

### 8. Documentation

Document only the supported-writer guarantee necessary for the feature. Do not advertise universal protection against manual editors or distributed filesystems.

Historical `v0.3.0` remains unchanged.

## Expected product implementation surface

```text
src/specgrain/pregrain.py
tests/test_pregrain.py
```

A focused new test module is allowed only when needed for subprocess/platform lock evidence.

Documentation-only closeout may later update:

```text
docs/adr/0020-supported-pregrain-writer-serialization.md
specs/025-supported-pregrain-writer-serialization/spec.md
specs/025-supported-pregrain-writer-serialization/tasks.md
specs/025-supported-pregrain-writer-serialization/verification.md
specs/025-supported-pregrain-writer-serialization/review.md
specs/025-supported-pregrain-writer-serialization/closeout.md
specs/CURRENT.md
docs/execution-master-plan.md
docs/roadmap.md
```

The selection evidence document remains immutable unless a factual correction is required.

## Verification order

1. focused pre-Grain serialization tests;
2. full pytest regression;
3. Ruff over `src`, `tests`, and `examples`;
4. tracked-tree cleanliness after tests;
5. compileall;
6. source CLI smoke;
7. package build;
8. built-wheel reinstall with `--no-deps`;
9. installed CLI smoke;
10. exact shaped-base-to-head diff review;
11. permanent five-cell CI on exact implementation head;
12. review comments/threads and review-system availability recheck without treating unavailable systems as PASS;
13. expected-head product merge;
14. canonical post-product CI;
15. historical `v0.3.0` preservation check;
16. documentation-only closeout;
17. exact-head closeout CI/review/expected-head merge;
18. canonical post-closeout CI and final governance re-read.

## Non-goals

No general project locking, child-authoring journal redesign, arbitrary external-writer coordination, distributed locking, timeout/lease/retry mechanism, dependency addition, READY/later lifecycle mutation, executor/provider orchestration, verification/evidence mutation, context automation, Spec Kit runtime adoption, release publication, hosted scope, or benchmark claim.
