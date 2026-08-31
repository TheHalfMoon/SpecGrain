# Tasks 026 — Supported Mutation Cross-Writer Coordination

## Shaping and authority

- [x] **T001** Reverify exact post-025 canonical baseline `1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1`, canonical governance, zero open PRs/issues, successful post-normalization CI, and historical `v0.3.0` identity before observation.
- [x] **T002** Reproduce the supported child-authoring / pre-Grain cross-writer partial-mutation race using only public `create_child_draft_spec` and `shape_draft_spec` APIs on observation branch `obs/post-025-supported-cross-writer-fixture`.
- [x] **T003** Preserve the first harness-invalid head `975c47b288cddbfbde34fbbca06afa77ee86f9af` as non-selection evidence because CI `33441425481` stopped at Ruff before test execution; make no product inference from it.
- [x] **T004** Qualify final observation head `3b557f91ec80c147b30f797198d736c2b6b42518`, fixture blob `ba8cea9510d09415a5bd4d2f123a72f5c8affee8`, with CI `33441481985` completed/success across all five permanent cells.
- [x] **T005** Record the bounded reproduced gap `SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION` and its explicit non-authority boundaries.
- [x] **T006** Shape Specification 026 around one shared project-scoped non-blocking advisory lock for existing supported pre-Grain persistence and native child authoring while preserving journal recovery.
- [x] **T007** Record ADR-0021 selecting shared advisory ownership without journal redesign, retry/wait policy, public locking API, distributed coordination, dependency addition, lifecycle expansion, release work, or benchmark claims.
- [ ] **T008** Verify the exact final shaping head/base/diff, permanent push CI, open PR head/base/scope, PR CI, reviews/comments/inline threads/mergeability, and review-system availability without treating unavailable/skipped systems as PASS.
- [ ] **T009** Merge the shaping PR with expected-head protection only after T008 is proven.
- [ ] **T010** Re-read canonical governance on the exact shaping merge and require permanent five-cell canonical post-shaping CI `success` before any product implementation begins.

## Product implementation — blocked until T010

- [ ] **T011** Refactor or relocate the existing private Specification 025 advisory-lock abstraction only as needed so both `store.py` and `pregrain.py` can use one dependency-safe helper without circular imports.
- [ ] **T012** Preserve the existing lock anchor `.specgrain/tmp/pregrain-mutation.lock`, non-blocking `fcntl`/`msvcrt` semantics, unsafe-anchor rejection, descriptor/process ownership, and deterministic contention error behavior.
- [ ] **T013** Keep pre-Grain `_persist` under the complete existing advisory critical section with all exact-preimage, fsync, replace, postimage, and project-validation defenses intact.
- [ ] **T014** Acquire the same advisory lock in `create_child_draft_spec` before authoring journal creation and hold it through normal completion or handled recovery of the authoring attempt.
- [ ] **T015** Preserve `AUTHORING_TRANSACTION_VERSION`, journal schema, recovery classifications, child creation order inside the transaction, and explicit recovery semantics.
- [ ] **T016** Add corrected-invariant tests proving pre-Grain ownership makes a competing child writer fail before journal/child/parent side effects and leaves a valid project.
- [ ] **T017** Add corrected-invariant tests proving child-authoring ownership makes competing shape/refine/grain persistence fail before target mutation and leaves a valid project.
- [ ] **T018** Prove losing-writer contention paths leave canonical parent/child bytes unchanged and successful sequential operations preserve existing lifecycle and authoring behavior.
- [ ] **T019** Keep all Specification 025 serialization/lifetime/unsafe-anchor/read-only tests and existing child-authoring recovery tests green.

## Product merge gates — blocked until T011-T019

- [ ] **T020** Run focused shared-lock, child-authoring recovery, and Specification 025 regression tests on the exact implementation head.
- [ ] **T021** Run full pytest, Ruff source/tests/examples, tracked-tree cleanliness, compileall, source CLI smoke, package build, built-wheel install, and installed CLI smoke.
- [ ] **T022** Verify exact implementation diff remains within the Specification 026 product surface and adds no runtime dependency.
- [ ] **T023** Require permanent CI `success` across Ubuntu/Python 3.11, Ubuntu/Python 3.12, Ubuntu/Python 3.13, macOS/Python 3.11, and Windows/Python 3.11 on the exact implementation head.
- [ ] **T024** Open/update the product PR, recheck exact head/base/scope/CI/reviews/comments/threads/mergeability immediately before merge, and record unavailable/skipped review systems accurately.
- [ ] **T025** Merge product work only with expected-head protection and only when all product gates are proven.
- [ ] **T026** Require canonical post-product CI `success` across all five permanent cells and reverify historical `v0.3.0` source/assets unchanged.

## Canonical closeout

- [ ] **T027** Add exact verification/review/closeout evidence and reconcile Specification 026/current program documents without widening delivered authority.
- [ ] **T028** Verify documentation-only closeout/reconciliation exact heads, diffs, CI, reviews/comments/threads/mergeability, and merge with expected-head protection only when proven.
- [ ] **T029** Require canonical post-closeout/reconciliation permanent CI success, reverify historical release preservation, re-read all canonical authority, and return to observation unless fresh independent evidence selects another bounded unit.

## Standing prohibitions

Specification 026 does not authorize:

- arbitrary external/manual writer coordination;
- a universal project transaction manager;
- child-authoring journal schema/version/recovery redesign;
- distributed/network locking;
- blocking waits, retries, sleeps, backoff, leases, heartbeats, or timeout ownership inference;
- runtime dependency additions;
- lifecycle expansion;
- executor/provider/result/verification/evidence orchestration;
- automatic context/network/model behavior;
- Spec Kit runtime integration;
- release publication;
- hosted scope;
- benchmark or superiority claims;
- inspection, search, materialization, reproduction, or use of the invalidated `SGB-EXP-001` hidden scorer.
