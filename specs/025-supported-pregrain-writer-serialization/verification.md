# Verification — Specification 025 Supported Pre-Grain Writer Serialization

**Status:** `CLOSED_CANONICAL`  
**Canonical shaping merge:** `e394ab0c7efabbfade91b64bcdf9a11c8146f469`  
**Final implementation head:** `bb1fa1406ef9dab6a65c1721378025943ba3f6de`  
**Canonical product merge:** `5e3966fb0db3d8971b5abe19106949001ed55ba9`  
**Canonical closeout merge:** `e05df4bd046590ee043115c1edbcd7b83163b4ad`  
**Canonical post-closeout CI:** `33436130730` — `completed/success` across all five permanent cells  
**Canonical reconciliation merge:** `8a0da2908f6251100a0d7ab71178c2a7c3ed64bb`  
**Canonical post-reconciliation CI:** `33437077692` — `completed/success` across all five permanent cells  
**Published release preserved:** `v0.3.0` / Release `378962445`

## Selection evidence

```text
canonical_base = 101f018095868fc011c4ebea15dcac64f64d1061
observation_head = 58174dbc87e9c02ebbb3a19d38727e1f42149226
fixture_blob = b0852096a6f8916955a6a31b3a785ca8bb0d708d
ci_run = 33431133156
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_PRE_GRAIN_MULTI_WRITER_LOST_UPDATE
```

The supported-writer observation proved two `shape_draft_spec` calls could both report success while one confirmed semantic revision was silently overwritten.

## Shaping evidence

- shaping head `e12dc2996f663f5d4a98eb5af212deb73ead5eff`;
- push CI `33432149125` — five-cell success;
- PR #54 CI `33432301056` — five-cell success;
- no submitted reviews or inline review threads at the merge gate;
- Qodo billing-blocked, automatic CodeRabbit review skipped by repository-star policy, Cubic descriptive only; none treated as PASS;
- expected-head merge `e394ab0c7efabbfade91b64bcdf9a11c8146f469`;
- post-shaping CI `33432447491` — five-cell success.

## Product evidence

Final implementation head `bb1fa1406ef9dab6a65c1721378025943ba3f6de` changed only:

- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

The implementation adds one project-scoped non-blocking advisory lock around the existing `_persist` transaction, uses `.specgrain/tmp/pregrain-mutation.lock` as an inert persistent anchor, uses standard-library Unix/Windows primitives, fails closed on contention and unsafe anchors, releases ownership after success/failure/process exit, preserves all existing preimage/postimage/lifecycle/readiness/dependency defenses, and leaves read-only loading outside the lock.

Focused proof covers competing supported writers, stale callers, shared shape/refine/grain contention, sequential lifecycle use, lock release, process-exit release, persistent-anchor reuse, read-only behavior, and unsafe anchors.

Superseded failures remain explicit:

- `9a465ba5add1db8952cba071075b0baae7e25569` / `33432725766` — focused test-fixture defects;
- `932eb916657c956b6aa68be833e83d89c5a69b93` / `33434076951` — test-only Ruff `SIM117`;
- both were corrected without weakening runtime invariants.

Final push evidence:

```text
head = bb1fa1406ef9dab6a65c1721378025943ba3f6de
run = 33434286534
status = completed
conclusion = success
```

All five permanent cells succeeded. macOS/Python 3.11 recorded `600 passed`; Ruff, full regression, tracked-tree cleanliness, compileall, source CLI smoke, package build, built-wheel installation, and installed CLI smoke all passed.

## Product review and merge evidence

PR #55:

- exact head `bb1fa1406ef9dab6a65c1721378025943ba3f6de`;
- exact base `e394ab0c7efabbfade91b64bcdf9a11c8146f469`;
- exactly two changed files;
- PR CI `33434757539` — five-cell success;
- `mergeable=true` at final gate;
- no submitted reviews or inline review threads;
- Qodo billing-blocked, CodeRabbit skipped, Cubic descriptive only.

PR #55 merged with expected-head protection as `5e3966fb0db3d8971b5abe19106949001ed55ba9`. Canonical post-product CI `33434910548` completed `success` across all five permanent cells.

## Closeout and reconciliation evidence

Exact closeout head:

`885823e0e56dfd3e7c7c8e63d8dacc41b14448f2`

The closeout diff changed exactly these eight documentation/governance/evidence paths:

- `docs/execution-master-plan.md`;
- `docs/roadmap.md`;
- `specs/025-supported-pregrain-writer-serialization/closeout.md`;
- `specs/025-supported-pregrain-writer-serialization/review.md`;
- `specs/025-supported-pregrain-writer-serialization/spec.md`;
- `specs/025-supported-pregrain-writer-serialization/tasks.md`;
- `specs/025-supported-pregrain-writer-serialization/verification.md`;
- `specs/CURRENT.md`.

Closeout gates:

- push CI `33435480927` — five-cell success;
- PR #56 CI `33435703680` — five-cell success;
- expected-head closeout merge `e05df4bd046590ee043115c1edbcd7b83163b4ad`;
- exact closeout parent `5e3966fb0db3d8971b5abe19106949001ed55ba9`;
- post-closeout CI `33436130730` — five-cell success.

Final reconciliation gates:

```text
head = c145578694100383d7292fc76b5995cee8a0e121
push_ci = 33436685449
pr = 57
pr_ci = 33436869583
merge = 8a0da2908f6251100a0d7ab71178c2a7c3ed64bb
post_merge_ci = 33437077692
```

PR #57 merged as the canonical final evidence reconciliation. Canonical post-reconciliation CI completed `success` across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11.

## Historical release preservation

After final reconciliation, live GitHub truth remains:

- `v0.3.0` source `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release ID `378962445`;
- wheel asset `535129008`, size `70463`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset `535129009`, size `104057`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

## Final governance reconciliation

Canonical `AGENTS.md`, `specs/CURRENT.md`, constitution, execution master plan, and Specification 025 authority chain were re-read after the final reconciliation and successful post-reconciliation CI. No governance conflict or additional product authority was found.

## Closure conclusion

All Specification 025 selection, shaping, product, review, merge, closeout, reconciliation, cross-platform CI, release-preservation, and governance gates are proven. Specification 025 is `CLOSED_CANONICAL`, there is no active product specification, and the program is in post-025 observation/evidence gathering.
