# Post-026 Execution Attempt Identity Reproduction — 2026-09-08

## Purpose

Determine whether live canonical SpecGrain can distinguish two separate execution attempts of the same exact `WorkPacket` through its current portable request/result contracts.

This is a bounded post-026 observation. It does not invoke an executor or provider, mutate lifecycle state, inspect hidden reasoning, access benchmark secrets, or use the invalidated `SGB-EXP-001` hidden scorer.

## Canonical baseline

```text
repository = TheHalfMoon/SpecGrain
canonical_main = e4fb1bf5463c72f164ffb842088a07df4a63abb2
program_state = POST_026_OBSERVATION
active_product_specification = none
published_release = v0.3.0
```

Canonical governance permits successor shaping only when fresh reproducible evidence against live canonical truth independently selects a bounded product gap.

## Existing boundary

Current source provides:

```text
WorkPacket
  -> AgentRequest
  -> external execution occurs outside SpecGrain
  -> ExecutionResult
  -> VerificationReport
  -> EvidenceRecord
```

`WorkPacket` and `AgentRequest` are deterministic content-addressed contracts. `ExecutionResult` is executor self-report bound to the packet digest. `VerificationReport` independently binds exact packet/result/implementation revisions.

These content identities work as designed. The observation asks a different question: can two separate retries of the same packet be represented as two separate attempts when their request/result content is identical?

## Observation fixture

```text
branch = obs/post-026-execution-attempt-identity
observation_head = 67f8562c30f7e2adfa3d93a82ca3cf0091c6f4e6
fixture = tests/test_post_026_execution_attempt_identity_observation.py
fixture_blob = 4613b5cea6ee86a9a17bd459de70bee47e7dfe24
```

The fixture exercises only supported deterministic APIs.

### Repeated request

For one exact packet:

```text
first = render_agent_request(packet)
second = render_agent_request(packet)
```

The fixture proves:

- `first.request_digest == second.request_digest`;
- `first.to_dict() == second.to_dict()`;
- public `AgentRequest` has no `attempt_id` field.

Therefore two separate executions of the exact same packet cannot be distinguished by request identity alone.

### Repeated executor report

For the same packet and identical failed executor payload, the fixture calls `parse_agent_result` twice.

The fixture proves:

- both normalized `ExecutionResult` values have the same `result_digest`;
- both serialized results are byte-for-byte semantically identical;
- public `ExecutionResult` has no `attempt_id`;
- public `ExecutionResult` has no `request_digest` binding.

Therefore two separate attempts that happen to report identical content collapse to one content identity.

## Machine-run evidence

```text
run_id = 34163498855
head = 67f8562c30f7e2adfa3d93a82ca3cf0091c6f4e6
workflow = CI
event = push
status = completed
conclusion = success
```

All permanent cells completed successfully:

```text
ubuntu-latest / Python 3.11 = success
ubuntu-latest / Python 3.12 = success
ubuntu-latest / Python 3.13 = success
macos-latest / Python 3.11 = success
windows-latest / Python 3.11 = success
```

The workflow also passed Ruff over source/tests/examples, editable installation, the full regression suite including the observation fixture, tracked-tree cleanliness, compile, source CLI smoke, package build, built-wheel installation, and installed CLI smoke.

## Reproduced gap

```text
REPEATED_PACKET_EXECUTION_ATTEMPT_IDENTITY_COLLAPSE
```

SpecGrain can content-address an execution request and an executor result, but it cannot represent that two otherwise identical request/result pairs came from separate execution attempts.

This matters for interruption, retry, attribution, diagnostics, and future recovery semantics because content identity is not occurrence identity.

The gap does **not** mean existing digests are defective. Their determinism is required. The missing primitive is a separate portable attempt identity that can bind one occurrence to the exact packet/request/result without changing content-address semantics.

## Smallest justified product boundary

Fresh evidence justifies shaping only an execution-attempt identity contract.

A minimal candidate is a new immutable/versioned `ExecutionAttemptRecord` that:

- carries a caller-supplied canonical `attempt_id`;
- binds the exact `packet_digest`;
- may bind an exact `request_digest` after rendering;
- records a small portable attempt status;
- may bind an exact `result_digest` when a result exists;
- may carry a concise public error/diagnostic code;
- serializes deterministically and has its own content digest;
- remains descriptive execution history, never verification authority.

The evidence does not independently justify repository persistence, automatic retries, executor invocation, lifecycle mutation, or a full orchestration engine.

## Donor relationship

The previously qualified LoopForge and SkillHone reviews informed where to look:

- LoopForge demonstrates explicit resumable attempt/workflow identity and state;
- SkillHone demonstrates bounded observation history and one-change attribution.

The selection itself comes from the local reproducible SpecGrain fixture above, not from donor feature presence.

No donor source code is copied by this observation or shaping decision.

## Explicit non-authority

This evidence does not justify:

- storing attempt ledgers under `.specgrain`;
- automatic provider/model/agent invocation;
- `READY -> RUNNING` or other lifecycle mutation authority;
- retry loops, backoff, sleeps, timeouts, leases, heartbeats, or stale-owner inference;
- fixed architect/developer/reviewer/test stage taxonomies;
- hidden reasoning or chain-of-thought storage;
- hidden benchmark/evaluation access;
- verification or evidence authority for attempt records;
- runtime dependencies;
- networking, hosted scope, or release publication.

## Selection conclusion

```text
BOUNDED_PRODUCT_GAP = REPEATED_PACKET_EXECUTION_ATTEMPT_IDENTITY_COLLAPSE
SUCCESSOR_SHAPING_JUSTIFIED = true
IMPLEMENTATION_AUTHORIZED = false
```

Specification 027 may be shaped around the smallest portable attempt-identity contract. Product implementation remains blocked until the shaping package is merged canonically and the resulting `main` passes the permanent five-cell CI matrix.