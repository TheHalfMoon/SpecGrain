# Specification 025 — Supported Pre-Grain Writer Serialization

## Status

`CLOSED_CANONICAL` when this final evidence reconciliation is canonical.

No successor specification is selected by this closure record.

## Outcome

Prevent one successful supported pre-Grain mutation from being silently overwritten by another supported pre-Grain mutation by serializing the existing `src/specgrain/pregrain.py::_persist` persistence-critical section without widening lifecycle, authoring, execution, verification, provider, or release authority.

## Selection evidence

```text
canonical_base = 101f018095868fc011c4ebea15dcac64f64d1061
observation_head = 58174dbc87e9c02ebbb3a19d38727e1f42149226
fixture_blob = b0852096a6f8916955a6a31b3a785ca8bb0d708d
ci_run = 33431133156
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_PRE_GRAIN_MULTI_WRITER_LOST_UPDATE
```

The reproduction used two supported public `shape_draft_spec` calls and proved both could report success while one confirmed semantic revision was silently overwritten in the final preimage-check / `os.replace` window.

ADR-0020 selected one project-scoped, non-blocking advisory lock around `_persist`.

## Canonical product evidence

```text
shaping_head = e12dc2996f663f5d4a98eb5af212deb73ead5eff
shaping_merge = e394ab0c7efabbfade91b64bcdf9a11c8146f469
post_shaping_ci = 33432447491
final_implementation_head = bb1fa1406ef9dab6a65c1721378025943ba3f6de
push_ci = 33434286534
product_pr = 55
product_pr_ci = 33434757539
product_merge = 5e3966fb0db3d8971b5abe19106949001ed55ba9
post_product_ci = 33434910548
```

The final product diff changed only:

- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

The implementation uses `.specgrain/tmp/pregrain-mutation.lock` as an inert persistent regular-file anchor, with conditional standard-library `fcntl` / `msvcrt` non-blocking advisory locking. Contention fails closed immediately. Lock ownership is released after success, failure, and process exit. Symlink and non-regular anchors fail closed. Read-only project loading stays outside the lock.

Existing loaded-node comparison, exact preimage checks, temporary-file fsync, final preimage recheck, `os.replace`, postimage confirmation, project validation, lifecycle, readiness, dependency, and semantic-revision behavior remain authoritative.

The lifecycle remains exactly:

```text
DRAFT -> SHAPED -> REFINING -> GRAIN
```

No later lifecycle transition was added. Child-authoring journal/recovery behavior remains separately governed.

## Acceptance evidence

Canonical tests and CI prove:

1. competing supported pre-Grain writers cannot both succeed through the reproduced lost-update topology;
2. a competing writer fails closed while the lock owner persists successfully;
3. stale callers still fail exact-preimage validation;
4. shape/refine/grain share one contention boundary;
5. sequential shape/refine/grain remains valid;
6. ownership releases after success, failure, and process exit;
7. the persistent anchor remains reusable after ownership release;
8. unsafe anchors fail closed;
9. read-only loading remains unaffected;
10. no runtime dependency was added;
11. all permanent Ubuntu, macOS, and Windows CI cells succeeded.

## Canonical closeout evidence

```text
closeout_head = 885823e0e56dfd3e7c7c8e63d8dacc41b14448f2
closeout_push_ci = 33435480927
closeout_pr = 56
closeout_pr_ci = 33435703680
closeout_merge = e05df4bd046590ee043115c1edbcd7b83163b4ad
post_closeout_ci = 33436130730
```

The closeout diff changed exactly eight documentation/governance/evidence paths. PR #56 stayed on exact base `5e3966fb0db3d8971b5abe19106949001ed55ba9`, was mergeable, had no submitted reviews or inline review threads, and merged with expected-head protection. Qodo was billing-blocked, automatic CodeRabbit review was skipped by repository-star policy, and Cubic was descriptive only; none was treated as PASS.

The closeout merge has exact parent `5e3966fb0db3d8971b5abe19106949001ed55ba9`. Post-closeout CI `33436130730` completed `success` across all five permanent cells.

## Historical release preservation

Historical `v0.3.0` remains unchanged:

- source `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release `378962445`;
- wheel `535129008` / `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source archive `535129009` / `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

Specification 025 did not publish or mutate a release.

## Explicit residual boundaries

Specification 025 does not claim or authorize arbitrary non-cooperating writer coordination, general project-wide or distributed locking, child-authoring redesign, blocking waits/retries/leases, new runtime dependencies, later lifecycle mutation, executor/provider orchestration, verification/evidence mutation, automatic context/network/model behavior, Spec Kit runtime adoption, release publication, hosted scope, or benchmark superiority claims.

## Final disposition

All shaped product, implementation, verification, review, merge, closeout, post-closeout, release-preservation, and canonical governance re-read gates are proven. When this final evidence reconciliation is canonical, Specification 025 is `CLOSED_CANONICAL`, there is no active product specification, and the program returns to post-025 observation/evidence gathering.
