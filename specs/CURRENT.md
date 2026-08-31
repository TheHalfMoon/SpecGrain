# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Canonical post-025 normalization baseline:** `1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1`  
**Canonical Specification 025 shaping merge:** `e394ab0c7efabbfade91b64bcdf9a11c8146f469`  
**Canonical Specification 025 product merge:** `5e3966fb0db3d8971b5abe19106949001ed55ba9`  
**Canonical Specification 025 closeout merge:** `e05df4bd046590ee043115c1edbcd7b83163b4ad`  
**Canonical Specification 025 reconciliation merge:** `8a0da2908f6251100a0d7ab71178c2a7c3ed64bb`  
**Program status:** `SPEC_026_SHAPING_CANDIDATE`  
**Last closed specification:** `specs/025-supported-pregrain-writer-serialization/` — `CLOSED_CANONICAL`  
**Selected successor candidate:** `specs/026-supported-mutation-cross-writer-coordination/` — `SHAPED_CANDIDATE`  
**Active product implementation:** blocked pending canonical shaping merge and post-shaping CI  
**Published release:** `v0.3.0`  
**Published release source:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Published release ID:** `378962445`

## Previous canonical frontier

Specification 025 — Supported Pre-Grain Writer Serialization — is `CLOSED_CANONICAL`. Its final reconciliation merge is `8a0da2908f6251100a0d7ab71178c2a7c3ed64bb`; the post-025 normalization baseline is `1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1`, with canonical post-normalization CI `33440739066` succeeding across all five permanent cells.

The SGB-EXP-001 comparative experiment remains `INVALIDATED_ORACLE_REVEALED_PRE_FREEZE`; it produced no valid comparative result, supports no superiority claim, selected no product work, and its hidden scorer is outside all current authority.

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

Push CI, PR CI, and canonical post-product CI all completed `success` across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11. At the PR #55 merge gate exact head/base and two-file scope remained unchanged, mergeability was true, and unavailable/skipped review systems were not treated as PASS.

## Specification 025 closeout and reconciliation proof

```text
closeout_head = 885823e0e56dfd3e7c7c8e63d8dacc41b14448f2
closeout_push_ci = 33435480927
closeout_pr = 56
closeout_pr_ci = 33435703680
closeout_merge = e05df4bd046590ee043115c1edbcd7b83163b4ad
post_closeout_ci = 33436130730
reconciliation_head = c145578694100383d7292fc76b5995cee8a0e121
reconciliation_push_ci = 33436685449
reconciliation_pr = 57
reconciliation_pr_ci = 33436869583
reconciliation_merge = 8a0da2908f6251100a0d7ab71178c2a7c3ed64bb
post_reconciliation_ci = 33437077692
post_normalization_merge = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
post_normalization_ci = 33440739066
```

The closeout, reconciliation, and normalization diffs were documentation/governance/evidence-only. Permanent CI remained successful across all five cells. Unavailable or skipped review systems were never treated as PASS.

## Post-025 observation and Specification 026 selection proof

Fresh observation against the exact post-025 canonical baseline independently reproduced a bounded gap between two supported mutation families:

```text
canonical_base = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
canonical_tree = ffe4dbff9658524eedf359451578a9d0446fed4c
observation_branch = obs/post-025-supported-cross-writer-fixture
observation_head = 3b557f91ec80c147b30f797198d736c2b6b42518
fixture = tests/test_post_025_supported_cross_writer_observation.py
fixture_blob = ba8cea9510d09415a5bd4d2f123a72f5c8affee8
ci_run = 33441481985
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION
```

The final fixture proves that supported `create_child_draft_spec` can complete successfully after a supported `shape_draft_spec` writer has passed its final parent preimage check but before that pre-Grain writer executes `os.replace`. The pre-Grain writer then overwrites the successful child-authoring parent postimage, fails during full-project postimage validation, and leaves a structurally invalid project with a stored child whose SHAPED parent no longer references it.

The earlier observation head `975c47b288cddbfbde34fbbca06afa77ee86f9af` and CI `33441425481` are not selection evidence because Ruff stopped the harness before test execution. Only formatting was corrected before the final qualifying head; no product inference is taken from the failed run.

Selection record: `docs/research/post-025-supported-cross-writer-reproduction-2026-09-01.md`  
Architectural decision: `docs/adr/0021-supported-mutation-cross-writer-coordination.md`

## Specification 026 selected boundary

Specification 026 is justified only for cooperative mutual exclusion between:

- existing supported pre-Grain persistence through `pregrain.py::_persist`;
- existing supported native child authoring through `store.py::create_child_draft_spec`.

The candidate reuses one project-scoped non-blocking advisory lock and preserves the child-authoring journal as the separate crash/recovery mechanism. The lock helper may be moved to a private dependency-neutral module only to avoid circular imports.

Explicitly not selected: arbitrary external-writer coordination, universal project transaction management, child-journal schema/recovery redesign, distributed locking, blocking waits/retries/timeouts/leases, runtime dependencies, lifecycle expansion, orchestration, release work, hosted scope, or benchmark claims.

## Historical release preservation

Live GitHub truth remains:

- tag `v0.3.0` -> `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release ID `378962445`, target `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- wheel asset `535129008` / digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset `535129009` / digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

Specification 026 shaping does not authorize release publication or mutation.

## Current execution gate

Current candidate state:

1. Specification 025 remains `CLOSED_CANONICAL`;
2. post-025 observation has independently selected the bounded Specification 026 candidate;
3. Specification 026 is `SHAPED_CANDIDATE` only;
4. product implementation remains blocked;
5. the shaping package must remain documentation/governance/evidence-only;
6. implementation becomes authorized only after the exact shaping PR is merged with expected-head protection and canonical post-shaping CI completes `success` across all five permanent cells;
7. any new live repository fact may supersede this candidate before implementation begins.

Do not widen Specification 026 beyond the reproduced supported cross-writer gap. Do not use the invalidated `SGB-EXP-001` experiment for product selection or benchmark claims.
