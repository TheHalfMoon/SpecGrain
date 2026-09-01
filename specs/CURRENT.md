# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Canonical post-025 normalization baseline:** `1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1`  
**Canonical Specification 026 shaping merge:** `d27e000728823e93d2fce9ecd669629a839bfdb3`  
**Canonical Specification 026 post-shaping CI:** `33442261877` — `completed/success` across all five permanent cells  
**Canonical Specification 026 product merge:** `69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b`  
**Canonical Specification 026 post-product CI:** `33485603844` — `completed/success` across all five permanent cells  
**Canonical Specification 026 closeout merge:** `2c9b18afb74e2254beb254bb84d9c07feec68aa0`  
**Canonical Specification 026 post-closeout CI:** `33486523094` — `completed/success` across all five permanent cells  
**Program status:** `SPEC_026_FINAL_RECONCILIATION_CANDIDATE`  
**Specification 026 disposition:** `CLOSED_CANONICAL` if and only if this exact final reconciliation becomes canonical and canonical post-reconciliation CI succeeds across all five permanent cells; otherwise final reconciliation remains pending  
**Active product implementation:** none  
**Published release:** `v0.3.0`  
**Published release source:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Published release ID:** `378962445`

## Canonical program history

Specifications 000 through 025 are `CLOSED_CANONICAL`.

Specification 026 — Supported Mutation Cross-Writer Coordination — was independently selected by fresh reproducible post-025 evidence, shaped canonically, implemented within a three-path source/test boundary, post-product verified, and documentation-only closeout verified canonically. No further Specification 026 product work is authorized.

The invalidated `SGB-EXP-001` experiment remains `INVALIDATED_ORACLE_REVEALED_PRE_FREEZE`; it produced no valid comparative result, supports no superiority claim, selected no Specification 026 authority, and its hidden scorer remains outside inspection/search/materialization/reproduction/use authority.

## Specification 026 selection proof

```text
canonical_base = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
canonical_tree = ffe4dbff9658524eedf359451578a9d0446fed4c
observation_head = 3b557f91ec80c147b30f797198d736c2b6b42518
fixture_blob = ba8cea9510d09415a5bd4d2f123a72f5c8affee8
observation_ci = 33441481985
reproduced_gap = SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION
```

The qualifying fixture used only supported public `shape_draft_spec` and `create_child_draft_spec` APIs. The earlier observation head `975c47b288cddbfbde34fbbca06afa77ee86f9af` / CI `33441425481` remains non-selection evidence because Ruff stopped before the fixture executed.

Selection record: `docs/research/post-025-supported-cross-writer-reproduction-2026-09-01.md`  
Architectural decision: `docs/adr/0021-supported-mutation-cross-writer-coordination.md`

## Specification 026 shaping and product proof

```text
shaping_head = 51079a25cdd0f90a9af1cc34ae7577c72ecdf2d6
shaping_push_ci = 33441902147
shaping_pr = 59
shaping_pr_ci = 33442057984
shaping_merge = d27e000728823e93d2fce9ecd669629a839bfdb3
post_shaping_ci = 33442261877

final_product_head = 24728cd52b2daef2c83c5b83f084421b8096a11f
product_push_ci = 33443061640
product_pr = 60
product_pr_ci = 33443161567
product_merge = 69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b
post_product_ci = 33485603844
```

Exact product diff changed only `src/specgrain/store.py`, `src/specgrain/pregrain.py`, and `tests/test_pregrain_serialization.py`. The implementation shares one project-scoped non-blocking advisory lock between supported pre-Grain persistence and native child authoring while preserving the lock anchor, standard-library platform primitives, fail-closed contention/unsafe-anchor behavior, descriptor/process ownership, exact-preimage/postimage defenses, separate authoring journal/recovery contract, lifecycle rules, read-only behavior, and zero runtime dependencies.

The superseded final-logic head `fd27a146b8c39c777b5fb3f1611b2689a1fad3d5` / CI `33442865903` is not acceptance evidence because Ruff stopped before tests. PR #60 was merged with expected-head protection after exact-head qualification; canonical post-product CI `33485603844` succeeded across all five permanent cells.

## Specification 026 canonical closeout proof

```text
closeout_base = 69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b
closeout_head = 9b6cd1769c24688172ca435b2a77118fa6f4228c
closeout_push_ci = 33486149999
closeout_pr = 61
closeout_pr_ci = 33486307568
closeout_merge = 2c9b18afb74e2254beb254bb84d9c07feec68aa0
post_closeout_ci = 33486523094
```

The closeout changed exactly eight documentation/governance/evidence paths. Push CI, PR CI, and canonical post-closeout CI completed `success` across all five permanent cells. At the final PR #61 merge gate, exact base/head/eight-path scope remained unchanged, `mergeable=true`, submitted reviews and inline review threads were `0`, Qodo was billing-blocked, CodeRabbit automatic review was skipped by repository-star policy, and Cubic produced no submitted approval. None was treated as PASS.

PR #61 was merged by concurrent activity as GitHub-signature-verified merge `2c9b18afb74e2254beb254bb84d9c07feec68aa0`, with exact parents `69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b` and `9b6cd1769c24688172ca435b2a77118fa6f4228c`. GitHub REST confirms the exact qualified closeout head was merged but does not expose whether the concurrent caller supplied `expected_head_sha`; no claim is made about that unobservable parameter.

## Historical release preservation

Live GitHub truth after canonical closeout remains:

- tag `v0.3.0` -> `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release ID `378962445`, target `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- wheel asset `535129008`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset `535129009`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

Specification 026 did not publish or mutate a release.

## Explicitly unselected

No Specification 026 authority exists for arbitrary non-cooperating writer coordination, universal project transaction management, child-authoring journal redesign, distributed locking, blocking waits/retries/timeouts/leases, runtime dependencies, lifecycle expansion, executor/provider/result/verification/evidence orchestration, automatic context/network/model behavior, Spec Kit runtime adoption, release publication, hosted scope, benchmark superiority claims, or use of the invalidated SGB-EXP-001 hidden scorer.

## Current execution gate

The only remaining Specification 026 gate is this exact final reconciliation. Required live conditions:

1. exact reconciliation diff is documentation/governance/evidence only and contains exactly eight paths;
2. permanent push CI succeeds on the exact reconciliation head across all five cells;
3. reconciliation PR exact head/base/scope, PR CI, reviews, comments, inline threads, mergeability, and review-system availability are rechecked without treating unavailable/skipped systems as PASS;
4. reconciliation merges with expected-head protection;
5. canonical post-reconciliation CI succeeds across all five permanent cells;
6. historical `v0.3.0` remains unchanged; and
7. canonical authority is re-read.

When all seven live conditions are satisfied, Specification 026 is `CLOSED_CANONICAL`, there is no active product specification, and the program state is `POST_026_OBSERVATION`. No additional documentation-only PR should be created solely to record the reconciliation merge SHA, post-reconciliation CI run ID, or to flip a stale checkbox.

After closure, do not invent a successor. Shape another specification only when fresh reproducible evidence against live canonical truth independently selects a bounded product gap.
