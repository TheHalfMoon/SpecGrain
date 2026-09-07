# SpecGrain Execution Master Plan

## Mission

Build SpecGrain as a deterministic, agent-neutral delivery control plane that turns software work into small, bounded, independently verifiable changes.

## Canonical governance order

1. `AGENTS.md`
2. `specs/CURRENT.md`
3. `.specify/memory/constitution.md`
4. this master plan
5. active specification/plan/tasks/review/evidence, when one exists
6. fresh live GitHub/repository verification

Live repository truth overrides stale prose, old CI/review state, remembered hashes, and previous completion claims.

## Permanent CI matrix

```text
ubuntu-latest / Python 3.11
ubuntu-latest / Python 3.12
ubuntu-latest / Python 3.13
macos-latest / Python 3.11
windows-latest / Python 3.11
```

Green CI is necessary where configured but not alone sufficient. Exact head/base/scope, authority, review state, evidence origin, release preservation, and explicit closure conditions also matter. Unavailable/skipped/neutral/descriptive/billing-blocked review systems are not PASS.

## Program frontier

Specifications 000–027 are `CLOSED_CANONICAL`.

```text
active_product_specification = none
last_closed_product_specification = 027-execution-attempt-identity
program_state = POST_027_OBSERVATION
live_truth_source = canonical GitHub main plus exact verification evidence
published_release = v0.3.0
```

Current canonical commit and latest workflow identifiers are deliberately resolved from live GitHub truth rather than embedded in this live-state header. Historical evidence identifiers remain recorded where they are stable evidence rather than a self-referential current-state claim.

Specification 027 selected and closed a reproducible occurrence-identity gap between deterministic execution content identity and separate execution occurrences. Its canonical product merge is `08f3ca9e6bb46386e23a196339d7157362b2a9b6`; canonical closeout merge is `c778080105fca899a9837d9c832dddff7812e599`.

## Current operating mode — bounded observation

There is no active implementation unit.

The only valid path to another product specification is:

1. reverify live canonical `main` and governance;
2. reproduce a concrete gap against that exact state;
3. preserve the smallest sufficient observation evidence;
4. select only a bounded successor justified by that evidence;
5. shape it before product implementation;
6. execute dependency-order tasks under exact-head verification and review gates;
7. close it canonically before returning to observation.

Do not convert attractive donor ideas, deferred features, or general product ambition into an active specification without fresh selection evidence.

## Specification 027 preserved boundaries

No attempt persistence, automatic attempt-ID generation, executor/provider/model invocation, orchestration, lifecycle mutation, automatic retries/backoff/timeouts/leases/heartbeats, verification/evidence mutation, hidden reasoning/evaluation access, fixed donor stage taxonomy, networking/hosted scope, runtime dependencies, or release publication is authorized by Specification 027.

## Historical release

```text
release_id = 378962445
tag = v0.3.0
source = 70dd66aba0e68ae710e6ef12605ed153d107bab4
wheel_sha256 = b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817
source_sha256 = e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835
```

Current-source capabilities ahead of `v0.3.0` do not imply a newer release. Any future release publication requires its own explicit canonical authority and evidence.

## Benchmark boundary

The invalidated `SGB-EXP-001` remains `INVALIDATED_ORACLE_REVEALED_PRE_FREEZE`; its hidden scorer remains outside inspection/search/materialization/reproduction/use authority.

## Continuation rule

Remain in `POST_027_OBSERVATION` until fresh reproducible evidence independently selects another bounded gap. Do not invent Specification 028 merely to continue work.
