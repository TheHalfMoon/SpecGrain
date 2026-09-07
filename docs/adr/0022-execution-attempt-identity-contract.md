# ADR-0022 — Execution Attempt Identity Contract

## Status

Accepted for Specification 027 shaping. Product implementation remains blocked until the shaping package is merged canonically and the resulting `main` passes the permanent five-cell CI matrix.

## Context

`WorkPacket`, `AgentRequest`, and `ExecutionResult` intentionally use deterministic content digests. Repeating the same packet through the same generic adapter therefore produces the same request digest. Repeating the same executor report for that packet produces the same result digest.

Fresh post-026 observation proved across the permanent cross-platform matrix that current public contracts do not carry an occurrence identity capable of distinguishing those two executions:

```text
canonical_base = e4fb1bf5463c72f164ffb842088a07df4a63abb2
observation_head = 67f8562c30f7e2adfa3d93a82ca3cf0091c6f4e6
fixture_blob = 4613b5cea6ee86a9a17bd459de70bee47e7dfe24
ci_run = 34163498855
ci_result = completed/success across all five permanent cells
reproduced_gap = REPEATED_PACKET_EXECUTION_ATTEMPT_IDENTITY_COLLAPSE
```

Content identity and occurrence identity solve different problems. Existing digests must remain deterministic; adding random or temporal data to them would weaken reproducibility rather than solve the gap.

## Decision

Specification 027 will introduce a separate portable immutable execution-attempt identity contract without changing the v1 `WorkPacket`, `AgentRequest`, or `ExecutionResult` schemas.

### New primitive

The product will define a frozen/slotted, versioned `ExecutionAttemptRecord` (name may change only if an equivalently precise name is demonstrably clearer) with a contract no broader than:

- `attempt_version`;
- caller-supplied canonical `attempt_id`;
- exact `packet_digest`;
- optional exact `request_digest`;
- portable attempt status;
- optional exact `result_digest`;
- optional concise public `error_code`;
- derived deterministic `attempt_digest` over normalized record content.

The record is descriptive execution metadata. It does not confer readiness, execution authorization, verification, or evidence sufficiency.

### Attempt identity

`attempt_id` is occurrence identity, not a content digest. The deterministic core will validate it but will not infer an attempt from packet/result equality.

The first implementation should prefer caller-supplied identity over hidden randomness, clocks, hostnames, process IDs, model names, or environment-specific state. This keeps the core portable and allows an external orchestrator, human tool, or future native owner to allocate attempt identity explicitly.

The canonical validation format should be narrow and version-stable. A prefixed lowercase UUID form such as:

```text
EA-550e8400-e29b-41d4-a716-446655440000
```

is preferred because it provides portable uniqueness without requiring repository-global sequence allocation. The exact grammar is owned by Specification 027.

### Status vocabulary

Attempt status must remain separate from `SpecState` lifecycle authority.

A minimal portable vocabulary may include:

```text
STARTED
SUCCEEDED
FAILED
BLOCKED
INTERRUPTED
```

Status validation may constrain whether `result_digest` or `error_code` is present, but it must not mutate a `SpecNode` or assert `VERIFIED`.

### Existing v1 contracts remain stable

Specification 027 will not add `attempt_id` directly to `WorkPacket`, `AgentRequest`, or `ExecutionResult` v1. Doing so would create an avoidable serialized-schema compatibility break.

Instead, `ExecutionAttemptRecord` binds existing exact content identities externally:

```text
attempt_id
  -> packet_digest
  -> request_digest? 
  -> result_digest?
```

This preserves the meaning of all current digests while making repeated occurrences distinguishable.

### No persistence yet

The reproduced evidence proves an identity-contract gap. It does not prove a repository persistence failure because current product intentionally does not own execution-attempt storage.

Therefore Specification 027 does not yet authorize:

- `.specgrain` attempt files;
- append logs or hash-chained attempt ledgers;
- transaction/recovery semantics for attempt storage;
- concurrency rules for attempt writers.

Those may be selected later only by separate reproducible evidence.

## Compatibility

The decision must preserve:

- `WORK_PACKET_VERSION = 1`;
- `EXECUTION_RESULT_VERSION = 1`;
- `ADAPTER_PROTOCOL_VERSION = 1`;
- existing packet/request/result digests for identical current inputs;
- independent verification authority;
- zero runtime third-party dependencies;
- agent/vendor neutrality;
- no network or provider invocation.

No project migration is required because no persisted attempt schema is introduced.

## Verification requirements

Implementation must prove at minimum:

1. two distinct valid `attempt_id` values can bind the same exact packet/request/result digests while remaining distinguishable records;
2. identical attempt content including identical `attempt_id` has a stable deterministic `attempt_digest`;
3. changing only `attempt_id` changes `attempt_digest` without changing packet/request/result digests;
4. malformed attempt IDs and malformed digests fail closed;
5. strict deserialization rejects unknown/missing fields and digest tampering;
6. status/result/error invariants are deterministic;
7. an attempt record exposes no `verified` field and cannot grant verification authority;
8. existing v1 packet/result/adapter serialization and digests remain unchanged;
9. no lifecycle mutation or provider invocation is added;
10. no runtime dependency is added;
11. all permanent CI cells succeed;
12. historical `v0.3.0` remains unchanged.

## Explicit non-goals

This ADR does not authorize execution-attempt persistence, executor/provider invocation, process supervision, retry scheduling, sleeps/backoff/timeouts, leases/heartbeats, lifecycle mutation, verification/evidence mutation, hidden reasoning storage, benchmark-secret access, fixed donor workflow stages, networking, hosted scope, runtime dependencies, or release publication.