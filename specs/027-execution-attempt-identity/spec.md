# Specification 027 — Execution Attempt Identity Contract

## Status

`SHAPED_CANDIDATE`

Fresh reproducible post-026 evidence selects this bounded product gap. Product implementation is blocked until this documentation/governance-only shaping package is merged canonically and canonical post-shaping CI succeeds across all five permanent cells.

## Problem

SpecGrain content-addresses `WorkPacket`, generic `AgentRequest`, and `ExecutionResult` deterministically. That is correct for reproducibility, but it means two separate executions of the exact same packet cannot be represented as two separate occurrences when their request/result content is identical.

Fresh observation reproduced this gap using only supported deterministic APIs.

## Outcome

Add one portable deterministic `ExecutionAttemptRecord` contract that gives each execution occurrence an explicit caller-supplied identity while binding the existing exact packet/request/result content digests and preserving all current trust boundaries.

## Selection evidence

```text
canonical_base = e4fb1bf5463c72f164ffb842088a07df4a63abb2
observation_branch = obs/post-026-execution-attempt-identity
observation_head = 67f8562c30f7e2adfa3d93a82ca3cf0091c6f4e6
fixture = tests/test_post_026_execution_attempt_identity_observation.py
fixture_blob = 4613b5cea6ee86a9a17bd459de70bee47e7dfe24
observation_ci = 34163498855
observation_result = completed/success across all five permanent cells
reproduced_gap = REPEATED_PACKET_EXECUTION_ATTEMPT_IDENTITY_COLLAPSE
```

Selection record: `docs/research/post-026-execution-attempt-identity-reproduction-2026-09-08.md`  
Architectural decision: `docs/adr/0022-execution-attempt-identity-contract.md`

## Public contract

### `ExecutionAttemptStatus`

A small portable enum independent from `SpecState` lifecycle authority:

- `STARTED`;
- `SUCCEEDED`;
- `FAILED`;
- `BLOCKED`;
- `INTERRUPTED`.

### `ExecutionAttemptRecord`

Frozen/slotted v1 record containing:

- `attempt_version=1`;
- canonical `attempt_id`;
- exact `packet_digest`;
- optional exact `request_digest`;
- `status`;
- optional exact `result_digest`;
- optional concise public `error_code`.

`attempt_digest` is SHA-256 over canonical normalized attempt content excluding the digest itself.

Expose deterministic `content_dict()`, `to_dict()`, canonical compact `to_json()`, and strict `from_dict()` that rejects unknown/missing fields and mismatched declared digest.

## Attempt ID grammar

The first public grammar is:

```text
EA-<lowercase canonical UUID>
```

Example:

```text
EA-550e8400-e29b-41d4-a716-446655440000
```

Rules:

- prefix exactly `EA-`;
- UUID textual form exactly 8-4-4-4-12 lowercase hexadecimal;
- no braced, uppercase, compact, nil/empty, hostname, timestamp, PID, model, or provider-derived alternatives;
- caller supplies the ID; SpecGrain validates but does not generate or persist it in this specification.

A caller may use a standard UUID generator outside the deterministic contract. The record remains deterministic once inputs are supplied.

## Status invariants

- `STARTED`: no `result_digest`; no `error_code`.
- `SUCCEEDED`: requires `result_digest`; forbids `error_code`.
- `FAILED`: may carry a `result_digest`; requires `error_code`.
- `BLOCKED`: may carry a `result_digest`; requires `error_code`.
- `INTERRUPTED`: `result_digest` optional; requires `error_code`.

`request_digest` remains optional for compatibility with callers that track an attempt before rendering an adapter request.

No status implies `VERIFIED`.

## Compatibility requirements

Specification 027 MUST preserve exact existing behavior for:

```text
WORK_PACKET_VERSION = 1
EXECUTION_RESULT_VERSION = 1
ADAPTER_PROTOCOL_VERSION = 1
```

It must not change serialized fields or derived digests of existing `WorkPacket`, `AgentRequest`, or `ExecutionResult` values.

The new record binds those identities without modifying them.

## Functional requirements

- **FR-001 — Separate occurrence identity:** two distinct valid attempt IDs bound to the same packet/request/result content remain distinguishable.
- **FR-002 — Deterministic record digest:** identical normalized record content yields identical `attempt_digest`.
- **FR-003 — Strict validation:** malformed IDs/digests/status combinations and unknown/missing fields fail closed.
- **FR-004 — Optional progressive binding:** an attempt may exist at `STARTED` before a request/result digest exists, then callers may construct later records with the same `attempt_id` and additional exact bindings.
- **FR-005 — No verification authority:** the record contains no `verified` field and cannot satisfy acceptance/evidence gates.
- **FR-006 — Backward compatibility:** current packet/request/result v1 serialization and digests are unchanged.
- **FR-007 — Agent neutrality:** no provider/model/IDE-specific field is required.
- **FR-008 — Dependency-free core:** implementation uses only the Python standard library.

## Expected implementation surface

Preferred bounded surface:

```text
src/specgrain/attempt.py
src/specgrain/__init__.py
tests/test_attempt.py
```

Do not modify `packet.py`, `adapter.py`, lifecycle mutation, verification mutation, CLI execution orchestration, store persistence, workflows, dependencies, or release automation unless fresh implementation evidence proves a strictly necessary compatibility-only change and that change is separately justified in the PR.

## Explicit out of scope

- `.specgrain` attempt persistence or append ledgers;
- attempt writer concurrency/recovery;
- automatic attempt ID generation;
- executor/subprocess/provider/model invocation;
- agent orchestration;
- lifecycle mutation including `READY -> RUNNING`;
- automatic retry/backoff/sleep/timeout/lease/heartbeat behavior;
- verification or evidence mutation;
- hidden reasoning/chain-of-thought storage;
- hidden benchmark/evaluation access;
- fixed donor stage taxonomy;
- networking/hosted scope;
- runtime dependencies;
- release publication.

## Acceptance criteria

1. distinct valid attempt IDs can bind identical packet/request/result digests and remain distinguishable.
2. attempt serialization is deterministic and strict.
3. attempt digest changes when occurrence identity or any bound semantic field changes.
4. malformed attempt IDs and digest tampering fail closed.
5. status/result/error invariants are enforced exactly.
6. attempt records remain descriptive self-report metadata, not verification authority.
7. existing WorkPacket, ExecutionResult, and generic adapter v1 tests remain unchanged and green.
8. no provider/model/host dependency enters the core.
9. runtime dependency count remains zero.
10. permanent Ubuntu/macOS/Windows CI succeeds on exact implementation head.
11. historical `v0.3.0` remains unchanged.

## Authority gate

```text
SHAPING_JUSTIFIED = true
SHAPED_CANDIDATE = true
IMPLEMENTATION_AUTHORIZED = false
```

Implementation becomes authorized only after the exact shaping package is canonical and canonical post-shaping CI succeeds across all five permanent cells.