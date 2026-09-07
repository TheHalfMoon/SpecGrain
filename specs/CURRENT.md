# Current Specification

## Live program state

Specifications 000–026 are `CLOSED_CANONICAL` under their recorded closure conditions.

Fresh post-026 observation has selected **Specification 027 — Execution Attempt Identity Contract** as a `SHAPED_CANDIDATE`.

Product implementation is **not yet authorized**. Implementation authority becomes live only if the exact documentation/governance-only shaping package is merged canonically and the resulting canonical `main` succeeds across all five permanent CI cells.

```text
CANONICAL_BASE_BEFORE_027_SHAPING = e4fb1bf5463c72f164ffb842088a07df4a63abb2
PROGRAM_STATE = SPEC_027_SHAPING
ACTIVE_PRODUCT_SPECIFICATION = 027-execution-attempt-identity
SHAPING_JUSTIFIED = true
SHAPED_CANDIDATE = true
IMPLEMENTATION_AUTHORIZED = false
PUBLISHED_RELEASE = v0.3.0
```

Live GitHub/repository truth overrides this file if the branch, merge, CI, review, or release state changes after it was written.

## Specification 027 selection evidence

```text
observation_branch = obs/post-026-execution-attempt-identity
observation_head = 67f8562c30f7e2adfa3d93a82ca3cf0091c6f4e6
fixture = tests/test_post_026_execution_attempt_identity_observation.py
fixture_blob = 4613b5cea6ee86a9a17bd459de70bee47e7dfe24
observation_ci = 34163498855
observation_result = completed/success across all five permanent cells
reproduced_gap = REPEATED_PACKET_EXECUTION_ATTEMPT_IDENTITY_COLLAPSE
```

The observation proves that two separate executions of the same exact `WorkPacket` produce identical deterministic `AgentRequest` content/digest, and two identical executor reports for that packet produce identical `ExecutionResult` content/digest. Neither current public contract carries a separate `attempt_id` occurrence identity.

This is not a defect in content-addressing. Existing digests are intentionally deterministic. The selected gap is the absence of a separate portable occurrence-identity primitive for repeated attempts.

Selection record:

```text
docs/research/post-026-execution-attempt-identity-reproduction-2026-09-08.md
```

Architectural decision:

```text
docs/adr/0022-execution-attempt-identity-contract.md
```

## Specification 027 bounded candidate

The shaped product outcome is one new immutable/versioned `ExecutionAttemptRecord` contract with:

- caller-supplied canonical `attempt_id`;
- exact `packet_digest`;
- optional exact `request_digest`;
- portable attempt status independent from `SpecState`;
- optional exact `result_digest`;
- optional public `error_code`;
- deterministic `attempt_digest` and strict serialization/deserialization.

The preferred first implementation surface is:

```text
src/specgrain/attempt.py
src/specgrain/__init__.py
tests/test_attempt.py
```

Existing `WorkPacket`, `AgentRequest`, and `ExecutionResult` v1 serialized schemas and digests must remain unchanged.

## Explicit non-authority

Specification 027 shaping does not authorize:

- `.specgrain` attempt persistence or append ledgers;
- automatic attempt ID generation by the deterministic core;
- executor/subprocess/provider/model invocation;
- agent orchestration or fixed donor stage graphs;
- `READY -> RUNNING` or other lifecycle mutation;
- retry loops, sleeps, backoff, timeouts, leases, heartbeats, or stale-owner inference;
- verification or evidence mutation;
- hidden reasoning/chain-of-thought storage;
- hidden benchmark/evaluation access;
- networking, hosted scope, new runtime dependencies, or release publication.

The invalidated `SGB-EXP-001` hidden scorer remains outside inspection/search/materialization/reproduction/use authority.

## Shaping gate

Before any product implementation:

1. exact shaping diff must remain documentation/governance/evidence only;
2. exact shaping head must pass push CI across all five permanent cells;
3. shaping PR must preserve exact head/base/scope;
4. PR CI must pass across all five permanent cells;
5. reviews/comments/threads/mergeability and review-system availability must be rechecked;
6. unavailable/skipped/neutral review systems must not be treated as PASS;
7. shaping must merge with expected-head protection;
8. canonical post-shaping CI must pass across all five permanent cells;
9. canonical authority must be reread;
10. historical `v0.3.0` must remain unchanged.

Only then does `IMPLEMENTATION_AUTHORIZED=true` become true for the bounded Specification 027 product scope.

## Specification 026 closure truth

Specification 026 is `CLOSED_CANONICAL`.

Its terminal reconciliation merge is:

```text
e8872201087640b3e684e93609f694e89811be97
```

Canonical post-reconciliation CI succeeded across all five permanent cells before the program returned to `POST_026_OBSERVATION`.

Subsequent developer-first documentation merge `faddebccb4f4b1dd71bf06b1ce7e3d7b367178ed` and Tencent donor-qualification merge `e4fb1bf5463c72f164ffb842088a07df4a63abb2` did not reopen Specification 026 or alter product authority.

## Historical release preservation

The latest published release remains unchanged:

```text
tag = v0.3.0
source = 70dd66aba0e68ae710e6ef12605ed153d107bab4
release_id = 378962445
wheel_asset = 535129008
wheel_sha256 = b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817
source_asset = 535129009
source_sha256 = e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835
```

No Specification 027 shaping work authorizes a release.

## Continuation discipline

Follow `specs/027-execution-attempt-identity/tasks.md` in dependency order.

Do not begin product work while the shaping gate is incomplete. After eventual Specification 027 closure, return to bounded observation and do not invent Specification 028 without fresh reproducible evidence.