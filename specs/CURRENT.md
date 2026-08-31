# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Canonical Specification 025 shaping merge:** `e394ab0c7efabbfade91b64bcdf9a11c8146f469`  
**Canonical Specification 025 product merge:** `5e3966fb0db3d8971b5abe19106949001ed55ba9`  
**Canonical Specification 025 closeout merge:** `e05df4bd046590ee043115c1edbcd7b83163b4ad`  
**Canonical post-closeout CI:** `33436130730` — `completed/success` across all five permanent cells  
**Program status:** `POST_025_OBSERVATION` when this final evidence reconciliation is canonical  
**Last closed specification:** `specs/025-supported-pregrain-writer-serialization/` — `CLOSED_CANONICAL` when this reconciliation is canonical  
**Active product specification:** none when this reconciliation is canonical  
**Product implementation:** canonical, post-product verified, closeout verified  
**Published release:** `v0.3.0`  
**Published release source:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Published release ID:** `378962445`

## Previous canonical frontier

Specification 024 — Native WorkPacket Export — remains `CLOSED_CANONICAL`. Its final post-024 normalization merge is `101f018095868fc011c4ebea15dcac64f64d1061`, with canonical post-normalization CI `33427947122` succeeding across all five permanent cells.

The SGB-EXP-001 comparative experiment remains `INVALIDATED_ORACLE_REVEALED_PRE_FREEZE`; it produced no valid comparative result, supports no superiority claim, and selected no product work.

## Specification 025 selection proof

```text
canonical_base = 101f018095868fc011c4ebea15dcac64f64d1061
observation_head = 58174dbc87e9c02ebbb3a19d38727e1f42149226
fixture_blob = b0852096a6f8916955a6a31b3a785ca8bb0d708d
ci_run = 33431133156
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_PRE_GRAIN_MULTI_WRITER_LOST_UPDATE
```

The supported-writer fixture proved that two public `shape_draft_spec` calls could both report success while one confirmed semantic revision was silently overwritten in the final preimage-check / `os.replace` window.

Selection record: `docs/research/post-024-supported-pregrain-multi-writer-reproduction-2026-08-31.md`  
Architectural decision: `docs/adr/0020-supported-pregrain-writer-serialization.md`

## Specification 025 shaping proof

```text
shaping_head = e12dc2996f663f5d4a98eb5af212deb73ead5eff
shaping_push_ci = 33432149125
shaping_pr = 54
shaping_pr_ci = 33432301056
shaping_merge = e394ab0c7efabbfade91b64bcdf9a11c8146f469
post_shaping_ci = 33432447491
```

All shaping CI gates succeeded across the permanent five-cell matrix. PR #54 had no submitted reviews or inline review threads; Qodo was billing-blocked, automatic CodeRabbit review was skipped, and Cubic was descriptive only. None was treated as PASS.

## Specification 025 product proof

Final implementation head:

`bb1fa1406ef9dab6a65c1721378025943ba3f6de`

Exact product diff changed only:

- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

The delivered implementation serializes supported shape/refine/grain persistence with one project-scoped non-blocking advisory lock, uses `.specgrain/tmp/pregrain-mutation.lock` as an inert persistent regular-file anchor, uses conditional standard-library Unix/Windows lock primitives, fails closed on contention and unsafe anchors, releases ownership after success/failure/process exit, preserves all prior preimage/postimage/lifecycle/readiness/dependency/semantic-revision defenses, and leaves read-only project loading outside the serialization boundary.

```text
final_product_head = bb1fa1406ef9dab6a65c1721378025943ba3f6de
push_ci = 33434286534
product_pr = 55
product_pr_ci = 33434757539
product_merge = 5e3966fb0db3d8971b5abe19106949001ed55ba9
post_product_ci = 33434910548
```

Push CI, PR CI, and canonical post-product CI all completed `success` across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11. macOS/Python 3.11 on the final push head recorded `600 passed` plus all configured static, cleanliness, build, install, and CLI smoke gates.

At the PR #55 merge gate exact head/base and two-file scope remained unchanged, mergeability was true, and no submitted reviews or inline review threads were present. Qodo was billing-blocked, CodeRabbit automatic review was skipped, and Cubic was descriptive only. None was treated as PASS.

## Specification 025 closeout proof

```text
closeout_head = 885823e0e56dfd3e7c7c8e63d8dacc41b14448f2
closeout_push_ci = 33435480927
closeout_pr = 56
closeout_pr_ci = 33435703680
closeout_merge = e05df4bd046590ee043115c1edbcd7b83163b4ad
post_closeout_ci = 33436130730
```

The closeout diff changed exactly eight documentation/governance/evidence paths and no product/test/workflow/dependency/package/release path. PR #56 remained on exact product-merge base `5e3966fb0db3d8971b5abe19106949001ed55ba9`, was mergeable, had no submitted reviews or inline review threads, and merged with expected-head protection. Qodo was billing-blocked, CodeRabbit automatic review was skipped, and Cubic was descriptive only. None was treated as PASS.

Canonical closeout merge `e05df4bd046590ee043115c1edbcd7b83163b4ad` has exact parent `5e3966fb0db3d8971b5abe19106949001ed55ba9`. Post-closeout CI `33436130730` completed `success` across all five permanent cells.

## Historical release preservation

Live GitHub truth after closeout remains:

- tag `v0.3.0` -> `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release ID `378962445`, target `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- wheel asset `535129008` / digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset `535129009` / digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

Specification 025 did not publish or mutate a release.

## Explicitly unselected after Specification 025

No current authority exists for arbitrary non-cooperating writer coordination, general project-wide or distributed locking, child-authoring journal redesign, blocking waits/retries/leases, new runtime dependencies, `GRAIN -> READY` or later lifecycle mutation, executor/provider orchestration, verification/evidence mutation, automatic context/network/model behavior, contract-version redesign, Spec Kit runtime adoption, broader package publication, hosted/account/dashboard scope, or benchmark superiority claims.

## Current execution gate

When this final evidence reconciliation is canonical:

1. Specification 025 is `CLOSED_CANONICAL`;
2. there is no active product specification;
3. all currently shaped and authorized product work is complete;
4. the program is in `POST_025_OBSERVATION`;
5. future product work requires fresh reproducible evidence against the new live canonical baseline.

Do not shape a successor merely because deferred work or residual risk exists. Observation/evidence gathering is the correct canonical frontier until new evidence independently selects a bounded product gap.
