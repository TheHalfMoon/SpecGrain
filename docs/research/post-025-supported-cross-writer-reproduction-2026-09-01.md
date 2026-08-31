# Post-025 Supported Cross-Writer Reproduction — 2026-09-01

## Purpose

Determine whether the post-025 canonical product can preserve fail-closed local mutation semantics when two different supported SpecGrain writer families overlap on the same DRAFT parent:

- supported pre-Grain mutation through `shape_draft_spec`;
- supported native child authoring through `create_child_draft_spec`.

This observation is independent of the invalidated `SGB-EXP-001` experiment. It does not inspect, search for, materialize, reproduce, or use the hidden scorer, and it makes no benchmark claim.

## Canonical baseline

```text
repository = TheHalfMoon/SpecGrain
canonical_main = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
canonical_tree = ffe4dbff9658524eedf359451578a9d0446fed4c
program_state = POST_025_OBSERVATION
active_product_specification = none
published_release = v0.3.0
```

Canonical governance permits successor shaping only when fresh reproducible evidence against live canonical truth independently selects a bounded product gap.

## Supported writer boundaries on the baseline

Specification 025 serializes supported pre-Grain persistence inside `src/specgrain/pregrain.py::_persist` with the project-scoped non-blocking advisory anchor:

```text
.specgrain/tmp/pregrain-mutation.lock
```

Native child authoring in `src/specgrain/store.py::create_child_draft_spec` uses a separate recoverable transaction journal:

```text
.specgrain/tmp/authoring-transaction.json
```

The two writer families do not acquire one shared mutual-exclusion boundary.

Child authoring commits in this order:

```text
load/validate parent
-> write authoring journal
-> create child file
-> replace parent with child reference
-> confirm parent and child postimages
-> remove journal
```

Pre-Grain persistence commits in this order while holding only the pre-Grain advisory lock:

```text
validate proposed project
-> read/validate target preimage
-> write/fsync replacement temp file
-> final target preimage recheck
-> os.replace target
-> confirm target postimage
-> reload/validate project
```

The final target preimage recheck and `os.replace` remain separate filesystem operations. A supported child-authoring transaction does not participate in the pre-Grain lock and can therefore commit between those two operations.

## Observation fixture

A test-only observation branch was created directly from the exact canonical baseline:

```text
branch = obs/post-025-supported-cross-writer-fixture
final_observation_head = 3b557f91ec80c147b30f797198d736c2b6b42518
fixture = tests/test_post_025_supported_cross_writer_observation.py
fixture_blob = ba8cea9510d09415a5bd4d2f123a72f5c8affee8
```

The fixture injects exactly one supported child writer at the pre-Grain writer's final `os.replace` boundary:

```text
writer A: shape_draft_spec(parent)
  -> loads the original DRAFT parent
  -> shapes a SHAPED replacement that retains the original empty children list
  -> enters the Specification 025 pre-Grain advisory lock
  -> passes the final exact parent preimage check
  -> pauses immediately before os.replace

writer B: create_child_draft_spec(parent)
  -> uses the same still-DRAFT parent through the supported public API
  -> writes its recoverable journal
  -> creates the child DRAFT
  -> replaces the parent with the child reference
  -> confirms both postimages
  -> removes the journal
  -> returns success

writer A resumes
  -> os.replace overwrites writer B's successful parent postimage
  -> confirms writer A's target postimage
  -> reloads the whole project
  -> detects invalid refinement and raises StoreValidationError
```

The fixture proves all of the following simultaneously:

- writer A uses supported public `shape_draft_spec`;
- writer B uses supported public `create_child_draft_spec`;
- writer B completes successfully and its child is canonically referenced by the parent before writer A resumes;
- writer A subsequently overwrites that parent reference;
- writer A then fails during postimage project validation;
- despite writer A reporting failure, writer A's SHAPED parent mutation remains stored;
- the child file created by the successful writer B remains stored;
- the final stored parent does not reference that child;
- `validate_refinement` reports the final project as structurally invalid.

This is not an arbitrary external edit, manual filesystem mutation, distributed-filesystem scenario, or benchmark artifact. Both competing mutations are supported SpecGrain APIs.

## Machine-run evidence

The first observation head was harness-invalid for selection purposes:

```text
head = 975c47b288cddbfbde34fbbca06afa77ee86f9af
run_id = 33441425481
result = failure before test execution
reason = Ruff E501 in the observation fixture
product_inference = none
```

Only fixture formatting was corrected. The product hypothesis and injection topology were unchanged.

Final GitHub Actions evidence:

```text
run_id = 33441481985
head = 3b557f91ec80c147b30f797198d736c2b6b42518
workflow = CI
status = completed
conclusion = success
```

All permanent cells completed successfully:

```text
ubuntu-latest / Python 3.11 = success
ubuntu-latest / Python 3.12 = success
ubuntu-latest / Python 3.13 = success
macos-latest / Python 3.11 = success
windows-latest / Python 3.11 = success
```

The workflow also passed Ruff over source/tests/examples, the full regression suite including the observation fixture, tracked-tree cleanliness, compileall, source CLI smoke, package build, built-wheel installation, and installed CLI smoke.

## Reproduced gap

The reproduced product gap is:

```text
SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION
```

A supported pre-Grain mutation can report failure after overwriting a successful supported child-authoring parent update, leaving the local project structurally invalid while both writer families have used their documented persistence paths.

This violates SpecGrain's fail-closed mutation boundary more narrowly than general filesystem concurrency: failure is not mutation-free, and one supported writer can invalidate another supported writer's successfully confirmed result.

## Smallest justified product boundary

Fresh evidence justifies shaping only cooperative mutual exclusion between the existing supported pre-Grain persistence transaction and the existing native child-authoring transaction.

The smallest candidate design is to reuse one project-scoped non-blocking advisory lock abstraction across both writer families, with child authoring holding that boundary around its journal/create-parent-update/confirmation transaction and pre-Grain persistence holding the same boundary around its existing `_persist` critical section.

The implementation must preserve child-authoring journal recovery as a separate durability/recovery mechanism. Sharing an advisory exclusion boundary does not authorize redesigning the journal format, recovery state machine, child ID allocation policy, or lifecycle semantics.

A candidate may relocate the existing private advisory-lock helper to a dependency direction usable by both `store.py` and `pregrain.py`, or provide an equivalently narrow private module. It must not introduce a public locking API or circular import.

## Required proof for any implementation

At minimum, exact-head verification must prove:

1. the reproduced cross-writer topology can no longer leave a structurally invalid project;
2. when pre-Grain holds the shared lock, competing child authoring fails closed before creating a journal, child file, or parent mutation;
3. when child authoring holds the shared lock, competing pre-Grain persistence fails closed before target mutation;
4. successful sequential child authoring and shape/refine/grain remain unchanged;
5. child-authoring recovery behavior remains valid and independently tested;
6. pre-Grain contention, crash-release, unsafe-anchor, exact-preimage, and postimage guarantees from Specification 025 remain valid;
7. read-only operations remain outside the mutation lock;
8. the implementation adds no runtime dependency, retry loop, blocking wait, timeout, lease, heartbeat, or distributed coordination claim;
9. all five permanent CI cells succeed on the exact implementation head;
10. historical `v0.3.0` remains unchanged.

## Explicit non-authority

This evidence does not justify:

- coordination with arbitrary manual/non-SpecGrain writers;
- a general transaction system for every repository mutation;
- child-authoring journal schema or recovery redesign;
- distributed or network locking;
- blocking waits, retries, leases, heartbeats, or timeout ownership inference;
- database or filesystem replacement;
- new runtime dependencies;
- lifecycle expansion beyond the current supported path;
- executor/provider/result/verification/evidence orchestration;
- automatic context/network/model behavior;
- Spec Kit runtime integration;
- release publication;
- hosted scope;
- benchmark claims or superiority claims.

## Selection conclusion

The post-025 evidence criterion is satisfied by an exact cross-platform machine-run reproduction using two supported public mutation APIs.

```text
BOUNDED_PRODUCT_GAP = SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION
SUCCESSOR_SHAPING_JUSTIFIED = true
IMPLEMENTATION_AUTHORIZED = false
```

A Specification 026 shaping candidate may therefore be created. Product implementation remains blocked until the documentation/governance-only shaping package is merged canonically and the resulting `main` passes the permanent five-cell CI matrix.
