# Tasks 025 — Supported Pre-Grain Writer Serialization

## Shaping and authority

- [x] **T001** Reproduce the post-024 concurrent-writer residual on exact canonical base `101f018095868fc011c4ebea15dcac64f64d1061` using supported public pre-Grain mutation APIs.
- [x] **T002** Prove the final supported-writer fixture on exact head `58174dbc87e9c02ebbb3a19d38727e1f42149226`, blob `b0852096a6f8916955a6a31b3a785ca8bb0d708d`, with permanent CI run `33431133156` succeeding across all five cells.
- [x] **T003** Shape the smallest candidate boundary: non-blocking cooperative serialization of `pregrain.py::_persist` only.
- [x] **T004** Record ADR-0020 selecting a standard-library advisory lock with no lock-file ownership inference, retry loop, timeout, or dependency.
- [x] **T005** Verify exact shaping head `e12dc2996f663f5d4a98eb5af212deb73ead5eff`; shaping push CI `33432149125` and PR #54 CI `33432301056` succeeded across all five permanent cells, the shaping diff remained documentation/governance-only, no submitted reviews or inline review threads were present, and unavailable/skipped review systems were not treated as PASS.
- [x] **T006** Merge shaping PR #54 with expected-head protection as `e394ab0c7efabbfade91b64bcdf9a11c8146f469`; canonical post-shaping CI `33432447491` succeeded across all five permanent cells before product implementation proceeded.

## Product implementation

- [x] **T007** Add one private project-scoped non-blocking advisory lock abstraction in `src/specgrain/pregrain.py` using conditional `fcntl` / `msvcrt` standard-library primitives.
- [x] **T008** Safely create/open `.specgrain/tmp/pregrain-mutation.lock` as an inert regular non-symlink runtime anchor and distinguish active contention from unsafe/open failures.
- [x] **T009** Acquire the lock around the complete `_persist` validation/read/replace/postimage-confirmation transaction without weakening existing checks.
- [x] **T010** Preserve existing shape/refine/grain lifecycle, semantic revision, readiness, dependency, postimage, and error contracts outside the new contention failure.
- [x] **T011** Add focused deterministic tests proving competing supported writers cannot both return success and that stale callers fail closed rather than overwrite.
- [x] **T012** Add lock-lifetime tests proving release after success/failure and automatic ownership release after subprocess/process exit while the persistent anchor remains.
- [x] **T013** Add unsafe-anchor tests and prove read-only behavior remains outside the serialization boundary.

## Product merge gates

- [x] **T014** Final implementation head `bb1fa1406ef9dab6a65c1721378025943ba3f6de` passed permanent push CI `33434286534` across all five cells, including Ruff, full regression, cleanliness, compileall, source CLI smoke, package build, built-wheel install, and installed CLI smoke; macOS/Python 3.11 recorded `600 passed`.
- [x] **T015** Verify the exact final implementation diff from canonical shaping merge changes only `src/specgrain/pregrain.py` and `tests/test_pregrain_serialization.py`, remains five commits ahead and zero behind, and stays inside Specification 025 authority.
- [x] **T016** Product PR #55 exact head `bb1fa1406ef9dab6a65c1721378025943ba3f6de` passed PR CI `33434757539` across all five cells; exact head/base, two-file scope, mergeability, reviews, comments, and inline threads were rechecked without treating Qodo billing-blocked, CodeRabbit skipped, or Cubic descriptive output as PASS.
- [x] **T017** Merge product PR #55 with expected-head protection as canonical product merge `5e3966fb0db3d8971b5abe19106949001ed55ba9`, with parents `e394ab0c7efabbfade91b64bcdf9a11c8146f469` and `bb1fa1406ef9dab6a65c1721378025943ba3f6de`.
- [x] **T018** Canonical post-product CI `33434910548` succeeded across all five permanent cells on exact merge `5e3966fb0db3d8971b5abe19106949001ed55ba9`; historical `v0.3.0` remained at source `70dd66aba0e68ae710e6ef12605ed153d107bab4`, Release `378962445`, with wheel/source asset IDs and digests unchanged.

## Canonical closeout

- [x] **T019** Add Specification 025 verification/review/closeout evidence and reconcile the current program documentation as a documentation-only `CLOSEOUT_CANDIDATE` without widening the delivered boundary.
- [ ] **T020** Require exact-head closeout CI, scope/review/thread/mergeability checks, and expected-head closeout merge.
- [ ] **T021** Require successful permanent post-closeout CI, re-read canonical governance, complete final evidence reconciliation, and mark Specification 025 `CLOSED_CANONICAL` only if every preceding gate is proven.

## Standing prohibitions

Until a separately shaped successor exists, Specification 025 tasks MUST NOT implement:

- general project-wide locking;
- child-authoring journal or recovery redesign;
- coordination with arbitrary external/manual writers;
- distributed/network locking;
- blocking waits, retries, leases, heartbeats, or timeout ownership inference;
- new runtime dependencies;
- `GRAIN -> READY` or later lifecycle mutation;
- executor/provider invocation or result ingestion;
- verification execution or evidence mutation;
- automatic context discovery or LLM selection;
- Spec Kit runtime integration;
- release publication;
- benchmark superiority claims.
