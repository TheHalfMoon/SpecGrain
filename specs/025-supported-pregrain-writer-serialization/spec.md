# Specification 025 — Supported Pre-Grain Writer Serialization

## Status

`CLOSEOUT_CANDIDATE`. The bounded product implementation is canonical at merge `5e3966fb0db3d8971b5abe19106949001ed55ba9`, canonical post-product CI `33434910548` succeeded across all five permanent cells, and historical `v0.3.0` remains unchanged. `CLOSED_CANONICAL` is not claimed until the documentation-only closeout merge, permanent post-closeout CI, and final evidence reconciliation are proven.

## Outcome

Prevent one successful supported pre-Grain mutation from being silently overwritten by another supported pre-Grain mutation by serializing the existing persistence-critical section without widening lifecycle, authoring, execution, verification, provider, or release authority.

## Selection evidence

Specification 025 was selected from the deterministic post-024 reproduction recorded in:

`docs/research/post-024-supported-pregrain-multi-writer-reproduction-2026-08-31.md`

Exact final observation evidence:

```text
canonical_base = 101f018095868fc011c4ebea15dcac64f64d1061
observation_head = 58174dbc87e9c02ebbb3a19d38727e1f42149226
fixture_blob = b0852096a6f8916955a6a31b3a785ca8bb0d708d
ci_run = 33431133156
ci_result = completed/success across all five permanent cells
```

The fixture proves that two supported public `shape_draft_spec` calls can each return success with distinct semantic revisions while the later `os.replace` from writer A silently removes writer B's already-confirmed successful postimage.

The selected gap is:

```text
SUPPORTED_PRE_GRAIN_MULTI_WRITER_LOST_UPDATE
```

## Architectural decision

Implementation is governed by:

`docs/adr/0020-supported-pregrain-writer-serialization.md`

ADR-0020 selects a project-scoped, non-blocking advisory lock around the existing `pregrain.py::_persist` persistence-critical section. It does not authorize broad repository locking or coordination with arbitrary external writers.

## Canonical implementation evidence

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

The final product diff changed only `src/specgrain/pregrain.py` and `tests/test_pregrain_serialization.py`. Push, PR, and post-product CI all succeeded across the permanent Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11 matrix. No unavailable or skipped review system was treated as PASS.

## Required behavior

### 1. Serialize supported pre-Grain persistence only

Every mutation currently persisted through `src/specgrain/pregrain.py::_persist` MUST acquire the same project-scoped advisory lock before entering its persistence-critical section.

This includes the existing public paths:

```text
shape_draft_spec
refine_shaped_spec
promote_refining_spec_to_grain
```

The lock MUST cover validation/read/replace/postimage confirmation sufficiently to prevent two supported persistence transactions from both returning success after overwriting one another.

Read-only operations MUST NOT acquire this lock.

### 2. Use one inert runtime lock anchor

Use:

```text
.specgrain/tmp/pregrain-mutation.lock
```

The anchor MUST be treated as runtime coordination metadata only.

Its existence alone MUST NOT mean:

- a writer is active;
- recovery is required;
- the lock is stale;
- an operation previously failed.

Active ownership exists only while the platform advisory lock is held by an open descriptor/process.

### 3. Use standard-library non-blocking platform primitives

The implementation MUST remain runtime-dependency free.

Use a private conditional platform abstraction based on:

```text
Unix-family: fcntl.flock(fd, LOCK_EX | LOCK_NB)
Windows:     msvcrt.locking(fd, LK_NBLCK, 1)
```

Platform-specific imports MUST remain conditional so package import stays portable.

Lock acquisition MUST NOT wait or retry. Contention MUST fail immediately and deterministically with a `StoreValidationError` identifying the pre-Grain mutation lock boundary.

### 4. Release ownership deterministically

The implementation MUST release/close the advisory lock in `finally` on success and handled failure.

Process termination MUST NOT require stale-owner timeout inference or manual deletion of the persistent anchor before a future supported writer can acquire the lock.

### 5. Fail closed on unsafe lock anchors

The anchor MUST be a regular non-symlink file.

Symlink, directory, device, or other unsafe/non-regular anchor states MUST fail closed without mutating a SpecNode.

The implementation MUST NOT follow an unsafe lock-anchor symlink.

### 6. Preserve existing mutation defenses

Specification 025 MUST retain the current:

- exact loaded-node comparison;
- exact preimage text checks;
- temporary-file write and fsync;
- final exact preimage recheck;
- atomic `os.replace`;
- exact postimage confirmation;
- full project revalidation after persistence.

The advisory lock is additive defense for cooperating supported writers. It MUST NOT weaken or replace current drift detection.

### 7. Preserve lifecycle and semantic contracts

The public APIs and allowed lifecycle path remain exactly:

```text
DRAFT -> SHAPED -> REFINING -> GRAIN
```

Specification 025 MUST NOT add `GRAIN -> READY` or any later transition.

State-only transitions MUST preserve existing semantic revision-digest behavior. Shaping MUST preserve all existing field validation and readiness semantics.

### 8. Preserve child-authoring authority

Specification 025 MUST NOT redesign or silently merge the ADR-0018 child-authoring journal with the new pre-Grain persistence lock.

`create_draft_spec`, `create_child_draft_spec`, and `recover_authoring_transaction` remain outside the product mutation surface.

### 9. No hidden retry policy

Lock contention MUST surface to the caller immediately.

Specification 025 MUST NOT add:

- sleep/retry loops;
- timeout heuristics;
- leases or heartbeats;
- background cleanup;
- daemon processes;
- network coordination.

Caller-level retry policy remains outside the deterministic core.

## Acceptance proof

Canonical evidence proves:

1. the exact supported-writer observation topology can no longer produce two successful competing writes;
2. writer A can succeed while injected writer B fails closed on active advisory-lock contention;
3. final canonical state equals writer A's expected postimage and contains no silent successful competing revision;
4. a stale caller computed against an old preimage still fails existing exact-preimage checks after another writer commits;
5. `shape_draft_spec`, `refine_shaped_spec`, and `promote_refining_spec_to_grain` share the same lock boundary;
6. lock ownership is released after successful persistence;
7. lock ownership is released after representative persistence failure;
8. process exit releases advisory ownership and a later supported mutation can reuse the persistent anchor without timeout inference;
9. the persistent anchor's mere existence does not block mutation after ownership is released;
10. symlink/non-regular lock anchors fail closed before SpecNode mutation;
11. existing preimage-drift, postimage, readiness, dependency, and lifecycle tests remain green;
12. read-only project loading remains unaffected;
13. no runtime dependency was added;
14. the permanent five-cell CI matrix succeeded on the final implementation head, PR head, and canonical product merge;
15. historical `v0.3.0` release identity remains unchanged.

Detailed proof is recorded in `verification.md` and review conclusions in `review.md`.

## Product implementation surface

Canonical product implementation changed exactly:

```text
src/specgrain/pregrain.py
tests/test_pregrain_serialization.py
```

No CLI behavior, public schema, lifecycle module, child-authoring journal code, workflow, dependency, package metadata, or release metadata changed.

## Existing contracts retained

Specification 025 preserves:

- SpecNode schema/version and semantic digest;
- lifecycle legality and authorization boundaries;
- Grain readiness semantics;
- dependency validation and eligibility;
- WorkPacket/context/evidence contracts;
- ADR-0018 recovery behavior;
- existing CLI success/error conventions except where existing pre-Grain errors naturally surface the new `StoreValidationError`;
- zero runtime dependencies.

## Explicitly out of scope

Specification 025 does not authorize:

- coordination with arbitrary manual/non-SpecGrain file writers;
- general project-wide locking of unrelated mutations;
- child-authoring lock or journal redesign;
- distributed/network filesystem lock guarantees;
- blocking waits, automatic retries, leases, heartbeats, or stale-owner timeout heuristics;
- database/store replacement;
- new runtime dependencies;
- `GRAIN -> READY` or later lifecycle mutation;
- executor/provider invocation or result ingestion;
- verification execution or evidence mutation;
- automatic context discovery, network access, or LLM selection;
- Spec Kit runtime integration;
- package versioning or release publication;
- hosted/account/dashboard/enterprise scope;
- benchmark superiority claims.

## Residual boundaries

Manual/non-cooperating writers remain outside the supported coordination contract. The exact-preimage checks continue to detect many such drifts, but Specification 025 does not claim an atomic compare-and-swap guarantee against arbitrary filesystem writers.

Other deferred product areas remain separately shapeable only from future fresh evidence after Specification 025 is canonically closed.

## Closure gate

The product is merged and post-product evidence is proven. The specification remains `CLOSEOUT_CANDIDATE` until T020/T021 complete through documentation-only closeout, permanent post-closeout CI, final evidence reconciliation, and canonical governance re-read.