# Specification 027 — Execution Attempt Identity Contract

## Status

`CLOSEOUT_CANDIDATE`

The bounded product is implemented on canonical `main` and post-product-qualified. Final `CLOSED_CANONICAL` status is conditional on the documentation-only closeout merge, canonical post-closeout five-cell CI success, historical-release preservation, and canonical authority reread.

## Selected problem

Fresh post-026 observation proved `REPEATED_PACKET_EXECUTION_ATTEMPT_IDENTITY_COLLAPSE`: two separate executions of identical WorkPacket/request/result content could not be represented as separate occurrences because existing public contracts intentionally content-address identical values identically.

## Delivered outcome

SpecGrain now exposes one separate portable occurrence-identity contract:

- `EXECUTION_ATTEMPT_VERSION = 1`;
- `ExecutionAttemptStatus` with STARTED/SUCCEEDED/FAILED/BLOCKED/INTERRUPTED;
- frozen/slotted `ExecutionAttemptRecord`;
- `ExecutionAttemptValidationError`;
- strict `EA-<lowercase canonical UUID>` caller-supplied attempt identity;
- exact packet/request/result digest bindings;
- deterministic `attempt_digest`;
- strict serialization/deserialization and status invariants.

The new record is descriptive execution metadata. It grants no readiness, lifecycle, verification, or evidence authority.

## Acceptance

All Specification 027 acceptance criteria are satisfied by exact product tests and the permanent cross-platform CI evidence recorded in `verification.md`.

## Compatibility

The product preserves:

```text
WORK_PACKET_VERSION = 1
EXECUTION_RESULT_VERSION = 1
ADAPTER_PROTOCOL_VERSION = 1
```

Existing AgentRequest and ExecutionResult public field sets remain unchanged. Attempt occurrence identity is external to existing content digests.

## Exact implementation surface

```text
src/specgrain/attempt.py
src/specgrain/__init__.py
tests/test_attempt.py
```

## Explicitly out of scope and still deferred

- attempt persistence or append ledgers;
- automatic attempt ID generation;
- executor/provider/model invocation;
- agent orchestration;
- lifecycle mutation;
- automatic retry/backoff/sleep/timeout/lease/heartbeat behavior;
- verification/evidence mutation;
- hidden reasoning or hidden evaluation access;
- fixed donor stage taxonomy;
- networking/hosted scope;
- runtime dependencies;
- release publication.

No successor is implied by these deferred boundaries.