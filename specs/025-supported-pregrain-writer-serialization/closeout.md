# Closeout — Specification 025 Supported Pre-Grain Writer Serialization

**Status:** `CLOSEOUT_CANDIDATE`

## Delivered outcome

Specification 025 closes the reproduced supported pre-Grain lost-update topology by serializing the existing `src/specgrain/pregrain.py::_persist` persistence-critical section with one project-scoped non-blocking advisory lock.

The delivered guarantee is limited to cooperating supported pre-Grain writers:

```text
one active supported pre-Grain persistence transaction per project
```

A competing supported shape/refine/grain persistence call fails closed immediately instead of racing through the final preimage-check / `os.replace` window.

## Canonical evidence through product

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

Every final push/PR/post-merge CI listed above completed `success` across all five permanent cells at its applicable gate.

## Product surface

Final product diff changed exactly:

- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

No public API shape was expanded. No CLI command, schema version, lifecycle state, dependency, workflow, package version, release artifact, child-authoring transaction contract, provider, network, hosted service, or benchmark claim was added.

## Behavioral result

The implementation now:

- serializes supported `shape_draft_spec`, `refine_shaped_spec`, and `promote_refining_spec_to_grain` persistence through the common `_persist` boundary;
- uses `.specgrain/tmp/pregrain-mutation.lock` only as an inert persistent anchor;
- uses non-blocking standard-library advisory lock primitives on Unix-family and Windows systems;
- preserves existing preimage, replacement, postimage, validation, lifecycle, readiness, dependency, and semantic-digest defenses;
- releases ownership after success, failure, and process exit;
- leaves read-only project loading unlocked;
- rejects unsafe lock anchors fail closed.

## Review disposition

PR #55 merged only after exact-head push CI and PR CI were green, exact head/base and changed paths were rechecked, mergeability was true, and no submitted reviews or inline review threads were present.

Qodo was billing-blocked. Automatic CodeRabbit review was skipped by repository-star policy. Cubic was descriptive only. None was treated as PASS.

## Historical release preservation

Historical `v0.3.0` remains unchanged:

- source `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release `378962445`;
- wheel `535129008` / `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source archive `535129009` / `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

## Explicit residuals

Still outside Specification 025 authority:

- arbitrary manual/non-cooperating writer coordination;
- general project-wide or distributed locking;
- child-authoring journal/recovery redesign;
- blocking waits, retries, leases, heartbeats, or timeout ownership inference;
- READY/later lifecycle mutation;
- executor/provider/result orchestration;
- verification/evidence mutation;
- automatic context/retrieval/network/LLM behavior;
- dependency or release publication changes;
- hosted/account/dashboard scope;
- benchmark superiority claims.

## Remaining closure gates

This closeout candidate does not make Specification 025 `CLOSED_CANONICAL`.

Remaining work is limited to:

1. exact-head documentation-only closeout CI and scope review;
2. closeout PR CI/reviews/threads/mergeability and expected-head merge;
3. canonical post-closeout CI and historical release recheck;
4. final evidence reconciliation that records the closeout merge/post-closeout CI and, only then, publishes `CLOSED_CANONICAL` and returns the program to observation.
