# Tasks 026 — Supported Mutation Cross-Writer Coordination

## Shaping and authority

- [x] **T001** Reverify exact post-025 canonical baseline `1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1`, canonical governance, zero open PRs/issues, successful post-normalization CI, and historical `v0.3.0` identity before observation.
- [x] **T002** Reproduce the supported child-authoring / pre-Grain cross-writer partial-mutation race using only public `create_child_draft_spec` and `shape_draft_spec` APIs on observation branch `obs/post-025-supported-cross-writer-fixture`.
- [x] **T003** Preserve the first harness-invalid head `975c47b288cddbfbde34fbbca06afa77ee86f9af` as non-selection evidence because CI `33441425481` stopped at Ruff before test execution; make no product inference from it.
- [x] **T004** Qualify final observation head `3b557f91ec80c147b30f797198d736c2b6b42518`, fixture blob `ba8cea9510d09415a5bd4d2f123a72f5c8affee8`, with CI `33441481985` completed/success across all five permanent cells.
- [x] **T005** Record the bounded reproduced gap `SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION` and its explicit non-authority boundaries.
- [x] **T006** Shape Specification 026 around one shared project-scoped non-blocking advisory lock for existing supported pre-Grain persistence and native child authoring while preserving journal recovery.
- [x] **T007** Record ADR-0021 selecting shared advisory ownership without journal redesign, retry/wait policy, public locking API, distributed coordination, dependency addition, lifecycle expansion, release work, or benchmark claims.
- [x] **T008** Verify final shaping head `51079a25cdd0f90a9af1cc34ae7577c72ecdf2d6` on base `1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1`, documentation-only eight-path scope, push CI `33441902147`, PR #59 CI `33442057984`, mergeability/review state, and review-system availability without treating unavailable/skipped systems as PASS.
- [x] **T009** Merge shaping PR #59 with expected-head protection as `d27e000728823e93d2fce9ecd669629a839bfdb3`.
- [x] **T010** Re-read canonical governance on the shaping merge and require canonical post-shaping CI `33442261877` success across all five permanent cells before product implementation.

## Product implementation

- [x] **T011** Relocate the existing private Specification 025 advisory-lock implementation into lower-level `store.py` so `store.py` and `pregrain.py` use one dependency-safe helper without circular imports.
- [x] **T012** Preserve `.specgrain/tmp/pregrain-mutation.lock`, non-blocking `fcntl`/`msvcrt` semantics, unsafe-anchor rejection, descriptor/process ownership, and deterministic contention errors.
- [x] **T013** Keep pre-Grain `_persist` under the complete existing advisory critical section with exact-preimage, fsync, replace, postimage, and project-validation defenses intact.
- [x] **T014** Acquire the same advisory lock in `create_child_draft_spec` before authoring journal creation and hold it through normal completion or handled recovery of the authoring attempt.
- [x] **T015** Preserve `AUTHORING_TRANSACTION_VERSION`, journal schema, recovery classifications, child creation order inside the transaction, and explicit recovery semantics.
- [x] **T016** Add corrected-invariant coverage proving pre-Grain ownership makes a competing child writer fail before journal/child/parent side effects and leaves a valid project.
- [x] **T017** Add corrected-invariant coverage proving child-authoring ownership makes competing pre-Grain persistence fail before target mutation and leaves a valid project; refine/grain remain on the common `_persist` boundary.
- [x] **T018** Prove losing-writer contention paths do not publish their canonical mutation and successful writer results leave valid refinement; preserve sequential supported behavior through regression.
- [x] **T019** Keep Specification 025 serialization/lifetime/unsafe-anchor/read-only coverage and existing child-authoring recovery coverage green in the full regression suite.

## Product merge gates

- [x] **T020** Qualify focused shared-lock/corrected-invariant behavior and retained recovery/Specification 025 regressions on exact implementation head `24728cd52b2daef2c83c5b83f084421b8096a11f`.
- [x] **T021** Pass full pytest, Ruff source/tests/examples, tracked-tree cleanliness, compileall, source CLI smoke, package build, built-wheel install, and installed CLI smoke on qualifying exact-head CI.
- [x] **T022** Verify exact implementation diff changes only `src/specgrain/store.py`, `src/specgrain/pregrain.py`, and `tests/test_pregrain_serialization.py`, with no runtime dependency addition.
- [x] **T023** Require exact-head permanent CI success across all five cells: push CI `33443061640` and PR CI `33443161567`.
- [x] **T024** Recheck PR #60 exact head/base/three-path scope/CI/reviews/comments/threads/mergeability and record Qodo billing-blocked, CodeRabbit skipped by star policy, and Cubic neutral due plan limit; none treated as PASS.
- [x] **T025** Merge PR #60 with expected-head protection as `69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b`.
- [x] **T026** Require canonical post-product CI `33485603844` success across all five permanent cells and reverify historical `v0.3.0` source/assets unchanged.

## Canonical closeout

- [x] **T027** Add exact verification/review/closeout evidence and reconcile Specification 026/current program documents without widening delivered authority.
- [ ] **T028** Verify the documentation/governance/evidence-only closeout exact head/diff, push CI, PR head/base/scope/PR CI/reviews/comments/threads/mergeability, merge with expected-head protection, then perform the final evidence reconciliation.
- [ ] **T029** Require canonical post-closeout and post-reconciliation permanent CI success, reverify historical release preservation, re-read all canonical authority, and return to observation unless fresh independent evidence selects another bounded unit.

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
