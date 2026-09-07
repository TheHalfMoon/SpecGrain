# Current Specification

## Canonical program state

Specifications 000–027 are `CLOSED_CANONICAL`.

There is no active product specification. The program is in bounded post-027 observation and no successor specification is preselected.

```text
ACTIVE_PRODUCT_SPECIFICATION = none
LAST_CLOSED_PRODUCT_SPECIFICATION = 027-execution-attempt-identity
PROGRAM_STATE = POST_027_OBSERVATION
LIVE_TRUTH_SOURCE = canonical GitHub main plus exact verification evidence
PUBLISHED_RELEASE = v0.3.0
```

Live GitHub/repository truth overrides this file if branch, merge, CI, review, or release state changes after it was written. Current canonical commit and latest workflow identifiers are intentionally not embedded in this live-state header because committing such identifiers would make the header self-stale.

## Specification 027 — Execution Attempt Identity Contract

Specification 027 is `CLOSED_CANONICAL`.

Its delivered product boundary is a separate portable immutable execution occurrence identity contract through `ExecutionAttemptRecord`. Existing WorkPacket, AgentRequest, and ExecutionResult v1 schemas and content digests remain unchanged.

Specification 027 does not own attempt persistence, orchestration, executor/provider invocation, lifecycle mutation, retry scheduling, verification/evidence mutation, hidden reasoning/evaluation access, networking, hosted scope, runtime dependencies, or release publication.

Canonical product evidence includes:

```text
selection_observation_head = 67f8562c30f7e2adfa3d93a82ca3cf0091c6f4e6
selection_ci = 34163498855 = success 5/5
shaping_merge = c1853d5b547c1f1ec14b5042917e824f4ad3975e
post_shaping_ci = 34164197679 = success 5/5
product_merge = 08f3ca9e6bb46386e23a196339d7157362b2a9b6
post_product_ci = 34164674946 = success 5/5
closeout_merge = c778080105fca899a9837d9c832dddff7812e599
post_closeout_ci = 34165959588 = success 5/5
```

Detailed evidence is preserved in `specs/027-execution-attempt-identity/`.

## Post-027 repository reconciliation

The developer-facing README was reconciled with the already-canonical execution-attempt capability through merge `86ad90e97d9addfc0e7125a9753e1da6fb838005`. Canonical CI `34166425318` passed across all five permanent cells, and Release workflow `34166752932` completed successfully without changing the historical release.

This documentation reconciliation adds no product authority and selects no successor specification.

## Historical release preservation

```text
release_id = 378962445
tag = v0.3.0
source = 70dd66aba0e68ae710e6ef12605ed153d107bab4
wheel_asset = 535129008
wheel_sha256 = b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817
source_asset = 535129009
source_sha256 = e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835
```

## Continuation discipline

Do not invent Specification 028 merely to continue activity. Shape a successor only if fresh reproducible evidence against the then-live canonical repository independently selects another bounded gap.

The invalidated `SGB-EXP-001` hidden scorer remains outside inspection/search/materialization/reproduction/use authority.
