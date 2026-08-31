# Verification — Specification 025 Supported Pre-Grain Writer Serialization

**Status:** `CLOSEOUT_CANDIDATE`  
**Canonical shaping merge:** `e394ab0c7efabbfade91b64bcdf9a11c8146f469`  
**Final implementation head:** `bb1fa1406ef9dab6a65c1721378025943ba3f6de`  
**Canonical product merge:** `5e3966fb0db3d8971b5abe19106949001ed55ba9`  
**Canonical post-product CI:** `33434910548` — `completed/success` across all five permanent cells  
**Published release preserved:** `v0.3.0` / Release `378962445`

This document records Specification 025 evidence proven from live GitHub truth through the post-product gate. It does not claim canonical closeout before the documentation-only closeout PR and post-closeout CI complete.

## Selection evidence

Specification 025 was selected by the deterministic post-024 reproduction recorded in `docs/research/post-024-supported-pregrain-multi-writer-reproduction-2026-08-31.md`:

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

The fixture used two supported public `shape_draft_spec` calls and proved that both could return success with distinct semantic revisions while one successful revision was silently overwritten in the final preimage-check / `os.replace` window.

## Shaping evidence

- exact shaping head: `e12dc2996f663f5d4a98eb5af212deb73ead5eff`;
- shaping push CI `33432149125`: `completed/success` across all five permanent cells;
- shaping PR #54 CI `33432301056`: `completed/success` across all five permanent cells;
- PR #54 had no submitted reviews and no inline review threads at the merge gate;
- Qodo was billing-blocked, automatic CodeRabbit review was skipped by repository-star policy, and Cubic was descriptive only; none was treated as PASS;
- PR #54 merged with expected-head protection as `e394ab0c7efabbfade91b64bcdf9a11c8146f469`;
- merge parents are `101f018095868fc011c4ebea15dcac64f64d1061` and `e12dc2996f663f5d4a98eb5af212deb73ead5eff`;
- canonical post-shaping CI `33432447491`: `completed/success` across all five permanent cells.

The canonical shaping merge authorized product implementation under ADR-0020 and the Specification 025 boundary.

## Product evidence

Final implementation head:

`bb1fa1406ef9dab6a65c1721378025943ba3f6de`

Exact final product diff from canonical shaping base changed only:

- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

The implementation:

- adds one private project-scoped non-blocking advisory lock around the existing `pregrain.py::_persist` persistence transaction;
- uses `.specgrain/tmp/pregrain-mutation.lock` as an inert persistent regular-file anchor;
- uses `fcntl.flock(..., LOCK_EX | LOCK_NB)` on Unix-family systems and `msvcrt.locking(..., LK_NBLCK, 1)` on Windows;
- maps active contention to deterministic fail-closed `StoreValidationError` behavior;
- rejects symlink and non-regular anchors before SpecNode mutation;
- releases lock ownership in `finally`, while process exit releases OS ownership without stale-owner inference;
- preserves existing loaded-node comparison, exact preimage checks, temporary-file fsync, final preimage recheck, `os.replace`, postimage confirmation, project revalidation, lifecycle, readiness, dependency, and semantic revision behavior;
- leaves read-only project loading outside the serialization boundary.

## Focused acceptance evidence

Focused tests prove:

1. an injected competing supported writer fails closed while the first writer owns the lock instead of also returning success;
2. the first writer's expected semantic revision remains canonical;
3. a stale precomputed writer still fails the preserved exact-preimage gate after another writer commits;
4. `shape_draft_spec`, `refine_shaped_spec`, and `promote_refining_spec_to_grain` share one contention boundary;
5. sequential `shape -> refine -> grain` remains valid with the persistent anchor present;
6. ownership releases after successful persistence;
7. ownership releases after representative persistence failure;
8. process termination releases ownership and a later supported writer can reuse the same persistent anchor;
9. read-only project loading is unaffected;
10. non-regular and symlink anchors fail closed without SpecNode mutation or symlink-target mutation.

## Exact implementation CI

Superseded runs remain explicit:

- implementation head `9a465ba5add1db8952cba071075b0baae7e25569`, run `33432725766`: failed because two focused test fixtures used the wrong error attribute and did not create `.specgrain/tmp` before a non-file anchor;
- head `932eb916657c956b6aa68be833e83d89c5a69b93`, run `33434076951`: failed Ruff `SIM117` in a focused test only;
- both were corrected without weakening runtime invariants.

Final exact-head push CI:

```text
head = bb1fa1406ef9dab6a65c1721378025943ba3f6de
run = 33434286534
status = completed
conclusion = success
```

All permanent cells succeeded:

- Ubuntu / Python 3.11;
- Ubuntu / Python 3.12;
- Ubuntu / Python 3.13;
- macOS / Python 3.11;
- Windows / Python 3.11.

The final matrix passed Ruff over source/tests/examples, full regression, tracked-tree cleanliness, compileall, source CLI smoke, package build, built-wheel installation, and installed CLI smoke. macOS/Python 3.11 recorded `600 passed`.

## Product review and merge evidence

Product PR #55:

- title: `feat(025): serialize supported pre-Grain writers`;
- exact head: `bb1fa1406ef9dab6a65c1721378025943ba3f6de`;
- exact base: `e394ab0c7efabbfade91b64bcdf9a11c8146f469`;
- changed files: exactly `src/specgrain/pregrain.py` and `tests/test_pregrain_serialization.py`;
- PR CI `33434757539`: `completed/success` across all five permanent cells;
- mergeability: true at the final gate;
- submitted reviews: none;
- inline review threads: none;
- Qodo: billing-blocked;
- automatic CodeRabbit review: skipped by repository-star policy;
- Cubic: descriptive summary only.

No unavailable or skipped review system was treated as PASS.

PR #55 merged with expected-head protection, producing canonical product merge:

`5e3966fb0db3d8971b5abe19106949001ed55ba9`

Its parents are exactly:

- canonical shaping merge `e394ab0c7efabbfade91b64bcdf9a11c8146f469`;
- final implementation head `bb1fa1406ef9dab6a65c1721378025943ba3f6de`.

## Canonical post-product evidence

Post-product CI:

```text
head = 5e3966fb0db3d8971b5abe19106949001ed55ba9
run = 33434910548
status = completed
conclusion = success
```

All five permanent cells completed `success`, including the Windows implementation path.

## Historical release preservation

Live GitHub release truth after the product merge remains:

- tag `v0.3.0` -> `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release ID `378962445`, target `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- wheel asset ID `535129008`, size `70463`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset ID `535129009`, size `104057`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

Specification 025 did not publish or mutate a release.

## Preserved residual boundaries

Specification 025 does not claim coordination with arbitrary manual/non-cooperating writers, a general project-wide lock, child-authoring journal redesign, distributed locking, blocking waits/retries, leases, heartbeats, timeout ownership inference, new runtime dependencies, READY/later lifecycle mutation, execution/provider authority, verification/evidence mutation, automatic context/network/LLM behavior, release publication, hosted scope, or benchmark superiority.

## Closeout gate

Product implementation and post-product verification are proven. Canonical closure is not yet claimed.

The remaining gates are:

1. documentation-only closeout exact-head CI and scope review;
2. closeout PR CI, reviews/threads/mergeability recheck, and expected-head merge;
3. permanent post-closeout CI on the exact canonical merge;
4. final canonical evidence reconciliation and governance re-read before `CLOSED_CANONICAL` is published.
