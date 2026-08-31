# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Canonical Specification 025 shaping merge:** `e394ab0c7efabbfade91b64bcdf9a11c8146f469`  
**Canonical Specification 025 product merge:** `5e3966fb0db3d8971b5abe19106949001ed55ba9`  
**Canonical Specification 025 post-product CI:** `33434910548` — `completed/success` across all five permanent cells  
**Program status:** `SPEC_025_CLOSEOUT`  
**Last closed specification:** `specs/024-native-workpacket-export/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/025-supported-pregrain-writer-serialization/` — `CLOSEOUT_CANDIDATE`  
**Product implementation:** canonical and post-product verified; product mutation complete  
**Published release:** `v0.3.0`  
**Published release source:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Published release ID:** `378962445`

## Previous canonical frontier

Specification 024 — Native WorkPacket Export — remains `CLOSED_CANONICAL`.

Its final post-024 normalization merge is `101f018095868fc011c4ebea15dcac64f64d1061`, with canonical post-normalization CI `33427947122` succeeding across all five permanent cells.

The SGB-EXP-001 comparative experiment remains preserved as `INVALIDATED_ORACLE_REVEALED_PRE_FREEZE`; it produced no valid comparative result, supports no superiority claim, and selected no product work.

## Specification 025 selection evidence

Fresh post-024 evidence reproduced the previously retained supported-writer residual using only supported public pre-Grain APIs:

```text
canonical_base = 101f018095868fc011c4ebea15dcac64f64d1061
observation_branch = obs/025-multi-writer-parent-replace-fixture
observation_head = 58174dbc87e9c02ebbb3a19d38727e1f42149226
fixture = tests/test_post_024_multi_writer_observation.py
fixture_blob = b0852096a6f8916955a6a31b3a785ca8bb0d708d
ci_run = 33431133156
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_PRE_GRAIN_MULTI_WRITER_LOST_UPDATE
```

The fixture proved that writer A and writer B could both call `shape_draft_spec`, both return success with distinct semantic revisions, and writer A could then silently overwrite writer B's already-confirmed successful postimage because writer A's final exact-preimage check and `os.replace` were separate operations.

Selection record:

`docs/research/post-024-supported-pregrain-multi-writer-reproduction-2026-08-31.md`

Architectural decision:

`docs/adr/0020-supported-pregrain-writer-serialization.md`

## Specification 025 shaping proof

```text
shaping_head = e12dc2996f663f5d4a98eb5af212deb73ead5eff
shaping_push_ci = 33432149125
shaping_pr = 54
shaping_pr_ci = 33432301056
shaping_merge = e394ab0c7efabbfade91b64bcdf9a11c8146f469
post_shaping_ci = 33432447491
```

The shaping push, PR, and canonical post-shaping CI gates all succeeded across the permanent five-cell matrix.

At the PR #54 merge gate there were no submitted reviews or inline review threads. Qodo was billing-blocked, automatic CodeRabbit review was skipped by repository-star policy, and Cubic was descriptive only. None was treated as PASS.

The shaping merge authorized only cooperative non-blocking serialization of the existing `src/specgrain/pregrain.py::_persist` critical section.

## Specification 025 product proof

Final implementation head:

`bb1fa1406ef9dab6a65c1721378025943ba3f6de`

Exact product diff from canonical shaping merge changed only:

- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

The delivered implementation:

- serializes supported shape/refine/grain persistence with one project-scoped advisory lock;
- uses `.specgrain/tmp/pregrain-mutation.lock` as an inert persistent regular-file anchor;
- uses conditional standard-library `fcntl` / `msvcrt` non-blocking lock primitives;
- fails closed immediately on supported-writer contention;
- rejects symlink/non-regular anchors;
- releases ownership after success, failure, and process exit;
- preserves loaded-node comparison, exact preimage checks, temporary-file fsync, final preimage recheck, `os.replace`, postimage confirmation, project revalidation, lifecycle, readiness, dependency, and semantic-revision behavior;
- leaves read-only project loading outside the serialization boundary.

Exact verification:

```text
final_product_head = bb1fa1406ef9dab6a65c1721378025943ba3f6de
push_ci = 33434286534
product_pr = 55
product_pr_ci = 33434757539
product_merge = 5e3966fb0db3d8971b5abe19106949001ed55ba9
post_product_ci = 33434910548
```

Push CI, PR CI, and canonical post-product CI all completed `success` across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11. macOS/Python 3.11 on the final push head recorded `600 passed` plus all configured static, cleanliness, build, install, and CLI smoke gates.

At the PR #55 merge gate:

- exact head/base remained unchanged;
- changed paths remained exactly the two authorized product/test paths;
- mergeability was true;
- no submitted reviews or inline review threads were present;
- Qodo was billing-blocked;
- automatic CodeRabbit review was skipped by repository-star policy;
- Cubic supplied descriptive summary text only.

No unavailable or skipped review system was treated as PASS.

PR #55 merged with expected-head protection as `5e3966fb0db3d8971b5abe19106949001ed55ba9`, with parents `e394ab0c7efabbfade91b64bcdf9a11c8146f469` and `bb1fa1406ef9dab6a65c1721378025943ba3f6de`.

## Historical release preservation

Live GitHub truth after the Specification 025 product merge remains:

- tag `v0.3.0` -> `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release ID `378962445`, target `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- wheel asset `535129008` / digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset `535129009` / digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

Specification 025 did not publish or mutate a release.

## Explicitly unselected under Specification 025

No authority exists under Specification 025 for:

- coordination with arbitrary manual/non-SpecGrain writers;
- general project-wide locking of unrelated mutations;
- child-authoring journal/recovery redesign;
- distributed/network locking;
- blocking waits, retry loops, leases, heartbeats, or timeout ownership inference;
- new runtime dependencies;
- `GRAIN -> READY` or later lifecycle mutation;
- executor/provider invocation or result orchestration;
- verification execution or evidence mutation;
- automatic source discovery, source-content packing, retrieval, network access, or LLM context selection;
- SpecNode, WorkPacket, or ContextSource contract version redesign;
- Spec Kit runtime integration or architectural adoption;
- PyPI publication or broader distribution changes;
- hosted/account/dashboard/enterprise scope;
- empirical benchmark superiority claims.

## Current execution gate

Specification 025 product implementation is canonical and post-product verification is complete.

The active branch is documentation-only closeout. Product code must not change during closeout.

The remaining authorized sequence is:

1. exact-head closeout CI and scope review;
2. closeout PR CI/review/thread/mergeability gate;
3. expected-head closeout merge;
4. permanent post-closeout CI and historical release recheck;
5. final evidence reconciliation and canonical governance re-read;
6. publish `CLOSED_CANONICAL` only after every preceding gate is proven.

## Next frontier discipline

Do not widen Specification 025 merely because adjacent concurrency work is visible. After canonical closure, return to observation/evidence gathering and shape any successor only from fresh reproducible evidence against the new canonical truth.