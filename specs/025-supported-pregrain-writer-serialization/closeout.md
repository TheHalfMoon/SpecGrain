# Closeout — Specification 025 Supported Pre-Grain Writer Serialization

**Status:** `CLOSED_CANONICAL` when this final evidence reconciliation is canonical

## Delivered outcome

Specification 025 closes the reproduced supported pre-Grain lost-update topology by serializing the existing `src/specgrain/pregrain.py::_persist` persistence-critical section with one project-scoped non-blocking advisory lock.

The delivered guarantee is limited to cooperating supported pre-Grain writers:

```text
one active supported pre-Grain persistence transaction per project
```

A competing supported shape/refine/grain persistence call fails closed immediately instead of racing through the final preimage-check / `os.replace` window.

## Canonical evidence

Selection:

```text
canonical_base = 101f018095868fc011c4ebea15dcac64f64d1061
observation_head = 58174dbc87e9c02ebbb3a19d38727e1f42149226
fixture_blob = b0852096a6f8916955a6a31b3a785ca8bb0d708d
ci_run = 33431133156
reproduced_gap = SUPPORTED_PRE_GRAIN_MULTI_WRITER_LOST_UPDATE
```

Shaping:

```text
shaping_head = e12dc2996f663f5d4a98eb5af212deb73ead5eff
push_ci = 33432149125
pr = 54
pr_ci = 33432301056
shaping_merge = e394ab0c7efabbfade91b64bcdf9a11c8146f469
post_shaping_ci = 33432447491
```

Product:

```text
final_head = bb1fa1406ef9dab6a65c1721378025943ba3f6de
push_ci = 33434286534
pr = 55
pr_ci = 33434757539
product_merge = 5e3966fb0db3d8971b5abe19106949001ed55ba9
post_product_ci = 33434910548
```

Closeout:

```text
closeout_head = 885823e0e56dfd3e7c7c8e63d8dacc41b14448f2
closeout_push_ci = 33435480927
closeout_pr = 56
closeout_pr_ci = 33435703680
closeout_merge = e05df4bd046590ee043115c1edbcd7b83163b4ad
post_closeout_ci = 33436130730
```

Every final push/PR/post-merge CI listed above completed `success` across all five permanent cells at its applicable gate.

## Product surface

Final product diff changed exactly:

- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

No public API shape, CLI command, schema version, lifecycle state, dependency, workflow, package version, release artifact, child-authoring transaction contract, provider, network, hosted service, or benchmark claim was added.

The implementation serializes supported shape/refine/grain persistence through the common `_persist` boundary, uses `.specgrain/tmp/pregrain-mutation.lock` only as an inert persistent anchor, uses non-blocking standard-library Unix/Windows advisory locks, preserves existing preimage/postimage/lifecycle/readiness/dependency/semantic-digest defenses, releases ownership after success/failure/process exit, leaves read-only loading unlocked, and rejects unsafe anchors fail closed.

## Product review disposition

PR #55 merged only after exact-head push and PR CI were green, exact head/base and changed paths were rechecked, mergeability was true, and no submitted reviews or inline review threads were present.

Qodo was billing-blocked. Automatic CodeRabbit review was skipped by repository-star policy. Cubic was descriptive only. None was treated as PASS.

## Closeout review disposition

The closeout diff changed exactly eight documentation/governance/evidence paths and no product/test/workflow/dependency/package/release path.

PR #56 remained on exact head `885823e0e56dfd3e7c7c8e63d8dacc41b14448f2` and exact base `5e3966fb0db3d8971b5abe19106949001ed55ba9`, was mergeable, had no submitted reviews or inline review threads, and merged with expected-head protection as `e05df4bd046590ee043115c1edbcd7b83163b4ad`.

Qodo was billing-blocked, automatic CodeRabbit review was skipped, and Cubic was descriptive only; none was treated as PASS.

The closeout merge has exact parent `5e3966fb0db3d8971b5abe19106949001ed55ba9`. Canonical post-closeout CI `33436130730` completed `success` across all five permanent cells.

## Historical release preservation

Historical `v0.3.0` remains unchanged after closeout:

- source `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release `378962445`;
- wheel `535129008` / `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source archive `535129009` / `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

## Explicit residuals

Still outside Specification 025 authority are arbitrary non-cooperating writer coordination, general project-wide or distributed locking, child-authoring journal/recovery redesign, blocking waits/retries/leases, later lifecycle mutation, executor/provider/result orchestration, verification/evidence mutation, automatic context/network/model behavior, new runtime dependencies, release publication, hosted scope, and benchmark superiority claims.

## Final disposition

Canonical governance was re-read after the closeout merge and successful post-closeout CI. No further Specification 025 product work is authorized or required. When this final evidence reconciliation is canonical, Specification 025 is `CLOSED_CANONICAL`, no active product specification remains, and the program returns to post-025 observation/evidence gathering. No successor is selected merely to continue activity.
