# Plan 027 — Execution Attempt Identity Contract

## Objective

Close only the reproduced occurrence-identity gap by adding a separate deterministic `ExecutionAttemptRecord` contract while preserving current packet/request/result content identities and all execution/verification authority boundaries.

## Canonical shaping base

```text
e4fb1bf5463c72f164ffb842088a07df4a63abb2
```

Selection evidence:

```text
observation_head = 67f8562c30f7e2adfa3d93a82ca3cf0091c6f4e6
fixture_blob = 4613b5cea6ee86a9a17bd459de70bee47e7dfe24
ci_run = 34163498855
ci_result = completed/success across all five permanent cells
```

Implementation MUST NOT begin until the shaping PR is merged with expected-head protection and the resulting canonical `main` passes the permanent five-cell CI matrix.

Planned implementation branch after that gate:

```text
feat/027-execution-attempt-identity
```

## Change strategy

### 1. Add a new isolated module

Prefer:

```text
src/specgrain/attempt.py
```

Keep existing v1 packet/adapter/result modules unchanged unless a compatibility-only import/export adjustment is necessary.

### 2. Validate attempt occurrence identity

Implement strict `EA-<lowercase canonical UUID>` validation with the standard library.

Do not generate IDs in core. Do not use timestamps, hostnames, process IDs, providers, models, or environment paths as identity.

### 3. Define portable attempt status

Add `ExecutionAttemptStatus` with exactly:

```text
STARTED
SUCCEEDED
FAILED
BLOCKED
INTERRUPTED
```

This enum is not `SpecState` and does not authorize lifecycle transitions.

### 4. Define frozen deterministic record

`ExecutionAttemptRecord` should be frozen/slotted and validate:

- version exactly 1;
- canonical attempt ID;
- exact SHA-256 packet/request/result digests where present;
- status/result/error invariants;
- non-empty error code when required.

Expose stable deterministic serialization and strict deserialization with digest recomputation.

### 5. Preserve v1 identities

Regression tests must snapshot or otherwise prove unchanged behavior for representative existing:

- WorkPacket digest;
- generic AgentRequest request digest;
- ExecutionResult result digest.

Do not add attempt identity into those content hashes.

### 6. Prove separate occurrence identity

Focused tests must prove two records with different `attempt_id` and identical packet/request/result bindings have different attempt digests and remain separately serializable.

### 7. Prove progressive binding without persistence

Construct a `STARTED` record for one attempt ID, then construct later terminal records with the same ID and additional request/result bindings.

This demonstrates contract-level continuity only. Do not persist or mutate an earlier record.

### 8. Preserve verification boundary

The attempt type must not expose `verified`, acceptance, evidence sufficiency, or implementation-verification authority.

Verification continues to own exact final verdicts.

### 9. Cross-platform proof

Exact implementation head must pass:

```text
ubuntu-latest / Python 3.11
ubuntu-latest / Python 3.12
ubuntu-latest / Python 3.13
macos-latest / Python 3.11
windows-latest / Python 3.11
```

### 10. Historical release preservation

Do not modify or republish `v0.3.0`.

## Expected product implementation surface

```text
src/specgrain/attempt.py
src/specgrain/__init__.py
tests/test_attempt.py
```

If a smaller surface is possible, prefer it. Any expansion requires explicit evidence and must remain within the shaped outcome.

## Verification order

1. re-read canonical governance and Specification 027 after shaping merge;
2. focused attempt-ID/status/serialization tests;
3. representative packet/adapter/result digest compatibility tests;
4. full pytest regression;
5. Ruff over source/tests/examples;
6. tracked-tree cleanliness;
7. compile;
8. CLI smoke;
9. package build;
10. built-wheel reinstall with `--no-deps`;
11. installed CLI smoke;
12. exact shaped-base-to-head diff review;
13. permanent five-cell CI on exact implementation head;
14. review comments/threads/availability recheck without treating skipped systems as PASS;
15. expected-head product merge;
16. canonical post-product CI;
17. historical `v0.3.0` preservation check;
18. documentation-only closeout/reconciliation if required by the active tasks;
19. final governance reread and return to observation.

## Non-goals

No attempt persistence, executor/provider invocation, orchestration, lifecycle mutation, retries/backoff/timeouts, verification/evidence mutation, hidden reasoning/eval access, fixed donor stage graph, networking, hosted scope, dependencies, or release publication.