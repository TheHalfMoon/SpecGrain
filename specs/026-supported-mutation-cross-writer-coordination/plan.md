# Plan 026 — Supported Mutation Cross-Writer Coordination

## Objective

Close the reproduced supported child-authoring / pre-Grain cross-writer partial-mutation race with the smallest cooperative boundary: make the existing native child-authoring transaction and existing pre-Grain persistence transaction acquire one shared project-scoped non-blocking advisory lock, while preserving journal recovery and every Specification 025 persistence defense.

## Canonical shaping base

```text
1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
```

Selection evidence is fixed to:

```text
observation_head = 3b557f91ec80c147b30f797198d736c2b6b42518
fixture_blob = ba8cea9510d09415a5bd4d2f123a72f5c8affee8
ci_run = 33441481985
ci_result = completed/success across all five permanent cells
```

Implementation MUST NOT begin until the shaping PR is merged with expected-head protection and the resulting canonical `main` passes the permanent five-cell CI matrix.

Planned implementation branch after that gate:

```text
feat/026-supported-mutation-cross-writer-coordination
```

## Change strategy

### 1. Preserve the existing operating-system advisory contract

Reuse the Specification 025 lock semantics and anchor:

```text
.specgrain/tmp/pregrain-mutation.lock
```

Do not add a second lock, transaction marker, retry mechanism, lock-owner payload, or migration.

The anchor remains inert runtime metadata when no process holds its advisory lock.

### 2. Move the lock abstraction only if dependency direction requires it

`pregrain.py` currently owns the advisory-lock helper while importing store primitives. `store.py` cannot import from `pregrain.py` safely.

Prefer a narrow private dependency-neutral module, for example:

```text
src/specgrain/mutation_lock.py
```

Move only the lock-related constants/helpers/context manager required for shared use. Preserve current external behavior and error details where compatible.

Do not expose a new public API.

### 3. Keep pre-Grain persistence behavior unchanged under the shared helper

`pregrain.py::_persist` must still acquire the lock before `_validate_proposed` and hold it through exact postimage/project confirmation.

Preserve:

- exact loaded-node comparison;
- exact preimage reads;
- temp-file fsync;
- final exact preimage recheck;
- `os.replace`;
- exact postimage confirmation;
- full refinement/dependency revalidation.

### 4. Add the same exclusion boundary to child authoring

`create_child_draft_spec` must acquire the shared advisory lock before creating the authoring journal.

Hold ownership through the normal authoring transaction and any handled recovery invoked by that call.

The existing journal still provides durable recovery semantics after journal creation. Do not rewrite the journal format or recovery state machine.

### 5. Fail closed before child transaction side effects on contention

When the shared lock is already held, a competing child-authoring call must raise deterministic `StoreValidationError` before:

- `.specgrain/tmp/authoring-transaction.json` is created;
- a child file is created;
- the parent is changed.

Verify exact bytes/absence where practical.

### 6. Fail closed before pre-Grain mutation on child contention

When child authoring owns the shared lock, competing shape/refine/grain persistence must fail at lock acquisition before target replacement.

Do not rely on journal-presence checks as the concurrency primitive.

### 7. Preserve explicit recovery behavior

Keep `recover_authoring_transaction` semantics unchanged.

Focused tests must prove existing recognized states still produce the same recovery classifications and that adding advisory ownership around live child authoring does not make persisted journals dependent on a stale lock file.

Explicit recovery called later must remain able to operate after process ownership has ended.

### 8. Focused corrected-invariant proof

Convert the observation into product tests that encode the corrected invariant rather than preserving the defect expectation.

Required cases:

- pre-Grain owns lock -> injected supported child writer fails before side effects -> pre-Grain succeeds -> project valid;
- child authoring owns lock -> injected supported pre-Grain writer fails before side effects -> child authoring succeeds -> project valid;
- sequential child authoring remains valid;
- sequential eligible pre-Grain mutation remains valid;
- losing writer leaves parent/child bytes unchanged;
- all existing Specification 025 lock tests remain green;
- all existing authoring recovery tests remain green.

### 9. Cross-platform proof

The shared helper deliberately uses separate Unix and Windows primitives. The exact implementation head must pass:

```text
ubuntu-latest / Python 3.11
ubuntu-latest / Python 3.12
ubuntu-latest / Python 3.13
macos-latest / Python 3.11
windows-latest / Python 3.11
```

No platform is accepted based on documentation alone.

### 10. Historical release preservation

Do not modify or republish `v0.3.0`.

Verify after product merge that tag/release source and asset digests remain unchanged.

## Expected product implementation surface

Preferred bounded surface:

```text
src/specgrain/pregrain.py
src/specgrain/store.py
src/specgrain/mutation_lock.py
tests/test_pregrain_serialization.py
<existing child-authoring focused test module>
```

If the existing helper can be shared without a new module and without circular imports, use the smaller surface.

Do not touch unrelated CLI, model, lifecycle, readiness, dependency, execution, benchmark, or release code.

## Verification order

1. re-read canonical `main`, `AGENTS.md`, constitution, current authority, and Specification 026 after shaping merge;
2. focused shared-lock and corrected cross-writer tests;
3. focused child-authoring recovery tests;
4. focused Specification 025 serialization regression;
5. full pytest regression;
6. Ruff over `src`, `tests`, and `examples`;
7. tracked-tree cleanliness after tests;
8. compileall;
9. source CLI smoke;
10. package build;
11. built-wheel reinstall with `--no-deps`;
12. installed CLI smoke;
13. exact shaped-base-to-head diff review;
14. permanent five-cell CI on exact implementation head;
15. review comments/threads and review-system availability recheck without treating unavailable/skipped systems as PASS;
16. expected-head product merge;
17. canonical post-product CI;
18. historical `v0.3.0` preservation check;
19. documentation-only closeout/reconciliation as required;
20. final canonical governance re-read and observation decision.

## Non-goals

No arbitrary external-writer coordination, universal project transaction manager, authoring journal redesign/version bump, distributed locking, blocking waits/retries/timeouts/leases, new runtime dependencies, lifecycle expansion, executor/provider orchestration, verification/evidence mutation, context automation, Spec Kit runtime adoption, release publication, hosted scope, or benchmark claim.
