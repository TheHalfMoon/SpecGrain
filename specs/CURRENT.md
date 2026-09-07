# Current Specification

## Live program state represented by this closeout candidate

Specifications 000–026 are `CLOSED_CANONICAL`.

Specification 027 — Execution Attempt Identity Contract has completed product implementation and canonical post-product qualification. This branch contains its documentation-only closeout candidate.

```text
CANONICAL_PRODUCT_MAIN = 08f3ca9e6bb46386e23a196339d7157362b2a9b6
ACTIVE_PRODUCT_SPECIFICATION = 027-execution-attempt-identity
PRODUCT_COMPLETE = true
POST_PRODUCT_CI = 34164674946 = completed/success 5/5
PROGRAM_STATE = SPEC_027_CLOSEOUT
CLOSED_CANONICAL = false until live closeout conditions are realized
PUBLISHED_RELEASE = v0.3.0
```

Live GitHub/repository truth overrides this file if branch, merge, CI, review, or release state changes after it was written.

## Specification 027 exact evidence

```text
selection_observation_head = 67f8562c30f7e2adfa3d93a82ca3cf0091c6f4e6
selection_ci = 34163498855 = success 5/5
shaping_head = e43a6680808b155010d2a4adeb7839fc417fe086
shaping_push_ci = 34163943883 = success 5/5
shaping_pr = 65
shaping_pr_ci = 34164096581 = success 5/5
shaping_merge = c1853d5b547c1f1ec14b5042917e824f4ad3975e
post_shaping_ci = 34164197679 = success 5/5
product_head = a795ac0de30ff254ce1697c49690a5f741c75fbe
product_push_ci = 34164406219 = success 5/5
product_pr = 66
product_pr_ci = 34164578794 = success 5/5
product_merge = 08f3ca9e6bb46386e23a196339d7157362b2a9b6
post_product_ci = 34164674946 = success 5/5
```

Detailed evidence is in `specs/027-execution-attempt-identity/verification.md`.

## Delivered product boundary

SpecGrain now has a separate portable immutable execution occurrence identity contract through `ExecutionAttemptRecord`. Existing WorkPacket/AgentRequest/ExecutionResult v1 schemas and content digests remain unchanged.

Specification 027 does not own attempt persistence, orchestration, executor/provider invocation, lifecycle mutation, retry scheduling, verification/evidence mutation, hidden reasoning/evaluation access, networking, hosted scope, runtime dependencies, or release publication.

## Closeout realization rule

Specification 027 becomes `CLOSED_CANONICAL` and the program becomes `POST_027_OBSERVATION` iff all live conditions below hold:

1. this exact closeout package is merged with expected-head protection;
2. exact closeout diff remains documentation/governance/evidence only;
3. closeout push and PR CI succeed across all five permanent cells;
4. there are no unresolved genuine review findings/threads at the merge gate;
5. canonical post-closeout CI succeeds across all five permanent cells;
6. historical `v0.3.0` remains unchanged;
7. canonical governance/authority is reread after merge.

Once those conditions hold, no additional PR is required merely to replace this conditional state with historical merge/run identifiers.

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

After closeout conditions are realized:

```text
SPECIFICATION_027 = CLOSED_CANONICAL
ACTIVE_PRODUCT_SPECIFICATION = none
PROGRAM_STATE = POST_027_OBSERVATION
```

Do not invent Specification 028. Shape a successor only if fresh reproducible evidence against the then-live canonical repository independently selects another bounded gap.

The invalidated `SGB-EXP-001` hidden scorer remains outside inspection/search/materialization/reproduction/use authority.