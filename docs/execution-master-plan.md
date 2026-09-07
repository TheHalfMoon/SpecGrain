# SpecGrain Execution Master Plan

## Mission

Build SpecGrain as a deterministic, agent-neutral delivery control plane that turns software work into small, bounded, independently verifiable changes.

The canonical high-level flow remains:

```text
Intent / Import
  -> SpecNode refinement
  -> Grain readiness
  -> WorkPacket
  -> execution outside or around the deterministic core
  -> ExecutionResult
  -> independent VerificationReport
  -> EvidenceRecord
```

Specification 027 adds only a missing occurrence-identity contract around one execution attempt. It does not turn the core into an executor or orchestration engine.

## Governance order

For every unit:

1. read `AGENTS.md`;
2. read `specs/CURRENT.md`;
3. read `.specify/memory/constitution.md`;
4. read this master plan;
5. read the active specification, plan, tasks, review, and referenced evidence;
6. reverify live GitHub/repository truth before trusting cached state.

Live repository truth overrides stale prose, remembered hashes, old reviews, old CI state, and previous completion claims.

## Permanent acceptance discipline

Configured permanent CI matrix:

```text
ubuntu-latest / Python 3.11
ubuntu-latest / Python 3.12
ubuntu-latest / Python 3.13
macos-latest / Python 3.11
windows-latest / Python 3.11
```

Green CI is necessary where configured but is not alone sufficient. Exact head/base/scope, canonical authority, review state, evidence origin, release preservation, and explicit completion conditions must also be satisfied.

Unavailable, skipped, neutral, descriptive, or billing-blocked review systems are not PASS.

## Completed program frontier

Specifications 000–026 are `CLOSED_CANONICAL` under their recorded closure conditions.

Specification 026 terminal reconciliation became canonical before the program returned to `POST_026_OBSERVATION`. Later repository-presentation and donor-reference documentation changes did not reopen product authority.

Historical release remains:

```text
tag = v0.3.0
source = 70dd66aba0e68ae710e6ef12605ed153d107bab4
release_id = 378962445
wheel_sha256 = b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817
source_sha256 = e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835
```

No current work may silently mutate or republish that release.

## Active unit — Specification 027 shaping

Fresh post-026 evidence:

```text
canonical_base = e4fb1bf5463c72f164ffb842088a07df4a63abb2
observation_branch = obs/post-026-execution-attempt-identity
observation_head = 67f8562c30f7e2adfa3d93a82ca3cf0091c6f4e6
fixture_blob = 4613b5cea6ee86a9a17bd459de70bee47e7dfe24
observation_ci = 34163498855
observation_result = completed/success across all five permanent cells
reproduced_gap = REPEATED_PACKET_EXECUTION_ATTEMPT_IDENTITY_COLLAPSE
```

The evidence demonstrates that repeated executions of identical content cannot be represented as separate occurrences by the existing deterministic request/result contracts.

### Selected bounded product shape

Specification 027 will add a separate `ExecutionAttemptRecord` identity contract no broader than:

```text
attempt_version
attempt_id
packet_digest
request_digest?
status
result_digest?
error_code?
attempt_digest
```

Attempt status is descriptive and separate from SpecNode lifecycle state.

Current v1 WorkPacket/AgentRequest/ExecutionResult schemas and digests remain stable.

### Why persistence is not included

The observation proves an identity-contract gap. It does not prove failure of a native attempt store because no such store is currently owned by the product.

Therefore the first product unit does not add `.specgrain` attempt persistence, append logs, transaction recovery, or writer coordination. Those require separate evidence if needed later.

### Why orchestration is not included

SpecGrain remains agent/vendor neutral. The deterministic core must not require Claude, Cursor, Codex, model providers, hosted services, or a particular runtime.

Specification 027 does not invoke executors, models, providers, subprocesses, or external tools.

## Specification 027 shaping gate

Current authority:

```text
SHAPING_JUSTIFIED = true
SHAPED_CANDIDATE = true
IMPLEMENTATION_AUTHORIZED = false
```

Required order before product work:

1. finish exact documentation/governance/evidence shaping package;
2. verify shaping diff contains no source/tests/workflows/dependencies/release mutation;
3. require exact-head push CI success across all five permanent cells;
4. open shaping PR against exact canonical base;
5. require exact-head PR CI success across all five permanent cells;
6. recheck reviews, issue comments, review threads, mergeability, and review-system availability;
7. resolve genuine findings without broadening scope;
8. merge with expected-head protection;
9. require canonical post-shaping CI success across all five permanent cells;
10. re-read canonical authority and historical-release identity.

Only after step 10 does bounded product implementation become authorized.

## Planned Specification 027 product unit

Preferred implementation branch:

```text
feat/027-execution-attempt-identity
```

Preferred product surface:

```text
src/specgrain/attempt.py
src/specgrain/__init__.py
tests/test_attempt.py
```

Implementation requirements:

- standard-library only;
- strict `EA-<lowercase canonical UUID>` validation;
- portable attempt status `STARTED | SUCCEEDED | FAILED | BLOCKED | INTERRUPTED`;
- strict lowercase SHA-256 binding validation;
- deterministic serialization and digest recomputation;
- strict status/result/error invariants;
- no `verified` field or verification authority;
- unchanged existing packet/request/result v1 serialized identity;
- focused and full regression proof;
- permanent five-cell exact-head CI;
- expected-head merge and canonical post-product CI;
- historical release preservation.

## Product verification order

After shaping authority becomes live:

1. branch from exact canonical post-shaping main;
2. implement only shaped attempt contract;
3. run focused attempt tests;
4. run packet/adapter/result compatibility tests;
5. run full regression;
6. run Ruff source/tests/examples;
7. verify tracked-tree cleanliness;
8. compile;
9. source CLI smoke;
10. build package;
11. reinstall built wheel with no dependencies;
12. installed CLI smoke;
13. inspect exact base-to-head diff;
14. require exact product-head five-cell CI;
15. open/update PR and recheck all review/merge gates;
16. expected-head merge;
17. canonical post-product five-cell CI;
18. reverify `v0.3.0` unchanged;
19. perform documentation-only closeout/reconciliation if required by the active tasks;
20. re-read canonical authority and return to observation when closure conditions hold.

## Explicit non-goals for Specification 027

No attempt persistence, automatic attempt-ID generation, executor/provider/model invocation, agent orchestration, lifecycle mutation, automatic retries, sleeps/backoff/timeouts/leases/heartbeats, verification/evidence mutation, hidden reasoning storage, hidden benchmark/evaluation access, fixed donor stage taxonomy, networking, hosted/account/dashboard scope, runtime dependencies, or release publication.

## Benchmark boundary

The invalidated `SGB-EXP-001` experiment remains `INVALIDATED_ORACLE_REVEALED_PRE_FREEZE`. Its hidden scorer remains outside inspection/search/materialization/reproduction/use authority. No current product decision or comparative claim may use it.

## Continuation rule

Do not create work merely to keep the project busy.

After the active unit closes, perform bounded observation against live canonical truth. Shape a successor only if fresh reproducible evidence independently selects another concrete bounded product gap.