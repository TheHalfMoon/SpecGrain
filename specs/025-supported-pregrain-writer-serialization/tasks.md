# Tasks 025 — Supported Pre-Grain Writer Serialization

## Shaping and authority

- [x] **T001** Reproduce the post-024 concurrent-writer residual on exact canonical base `101f018095868fc011c4ebea15dcac64f64d1061` using supported public pre-Grain mutation APIs.
- [x] **T002** Prove the final supported-writer fixture on exact head `58174dbc87e9c02ebbb3a19d38727e1f42149226`, blob `b0852096a6f8916955a6a31b3a785ca8bb0d708d`, with permanent CI run `33431133156` succeeding across all five cells.
- [x] **T003** Shape the smallest candidate boundary: non-blocking cooperative serialization of `pregrain.py::_persist` only.
- [x] **T004** Record ADR-0020 selecting a standard-library advisory lock with no lock-file ownership inference, retry loop, timeout, or dependency.
- [ ] **T005** Verify the exact shaping head changes only authorized research/governance/specification paths, passes permanent five-cell CI, has no unresolved material review threads, and is mergeable.
- [ ] **T006** Merge the shaping PR with expected-head protection and require successful permanent post-shaping CI on canonical `main` before product implementation begins.

## Product implementation — blocked until T006

- [ ] **T007** Add one private project-scoped non-blocking advisory lock abstraction in `src/specgrain/pregrain.py` using conditional `fcntl` / `msvcrt` standard-library primitives.
- [ ] **T008** Safely create/open `.specgrain/tmp/pregrain-mutation.lock` as an inert regular non-symlink runtime anchor and distinguish active contention from unsafe/open failures.
- [ ] **T009** Acquire the lock around the complete `_persist` validation/read/replace/postimage-confirmation transaction without weakening existing checks.
- [ ] **T010** Preserve existing shape/refine/grain lifecycle, semantic revision, readiness, dependency, postimage, and error contracts outside the new contention failure.
- [ ] **T011** Add focused deterministic tests proving competing supported writers cannot both return success and that stale callers fail closed rather than overwrite.
- [ ] **T012** Add lock-lifetime tests proving release after success/failure and automatic ownership release after subprocess/process exit while the persistent anchor remains.
- [ ] **T013** Add unsafe-anchor tests and prove read-only behavior remains outside the serialization boundary.

## Product merge gates

- [ ] **T014** Run focused tests, full regression, Ruff, cleanliness, compileall, source CLI smoke, package build, built-wheel install, and installed CLI smoke.
- [ ] **T015** Verify the exact implementation diff remains inside Specification 025 authority and expected product surface.
- [ ] **T016** Require permanent five-cell push/PR CI success on the exact final implementation head and inspect all review comments/threads without treating unavailable review systems as PASS.
- [ ] **T017** Merge the product PR with expected-head protection.
- [ ] **T018** Require successful permanent post-product CI on the exact canonical merge and re-verify historical `v0.3.0` identity.

## Canonical closeout

- [ ] **T019** Add Specification 025 verification/review/closeout evidence and reconcile current program documentation without widening the delivered boundary.
- [ ] **T020** Require exact-head closeout CI, scope/review/thread/mergeability checks, and expected-head closeout merge.
- [ ] **T021** Require successful permanent post-closeout CI, re-read canonical governance, and mark Specification 025 `CLOSED_CANONICAL` only if every preceding gate is proven.

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
