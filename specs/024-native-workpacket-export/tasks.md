# Tasks 024 — Native WorkPacket Export

## Shaping and authority

- [x] **T001** Reproduce the post-023 native WorkPacket handoff discontinuity on exact canonical base `f2e8378dcba0cfea2beedc6da61324b0c3fea95e`.
- [x] **T002** Prove the final observation fixture on exact head `95e5358ed420cd2e6fbd0bc7c56690763cea1283` with permanent CI run `33416110142` succeeding across all five cells.
- [x] **T003** Shape the smallest candidate boundary: read-only native WorkPacket export from an existing dependency-eligible `GRAIN`.
- [ ] **T004** Verify the exact shaping head changes only authorized research/governance/specification paths, passes permanent five-cell CI, has no unresolved material review threads, and is mergeable.
- [ ] **T005** Merge the shaping PR with expected-head protection and require successful permanent post-shaping CI on canonical `main` before product implementation begins.

## Product implementation — blocked until T005

- [ ] **T006** Add the bounded `specgrain packet <spec_id> [path] --context-sources <json-file> [--json]` command without lifecycle or evidence mutation.
- [ ] **T007** Add strict bounded ContextSource-file parsing that rejects unsafe/non-canonical input and delegates semantic field validation to existing context primitives.
- [ ] **T008** Require exact stored `GRAIN` state and current dependency eligibility before export.
- [ ] **T009** Apply the stored Grain token budget through existing `ContextBudgetPolicy` / `require_context_budget` semantics.
- [ ] **T010** Build the export exclusively through existing `build_work_packet` and preserve existing packet/context contract versions and digest semantics.
- [ ] **T011** Add stable text and full canonical JSON stdout behavior plus current CLI failure conventions.
- [ ] **T012** Add focused cross-platform tests for valid export, API/CLI equality, determinism, non-mutation, state/dependency gates, malformed context input, budget failure, and bounded file safety.
- [ ] **T013** Update current-source README command documentation without rewriting historical `v0.3.0` claims.

## Product merge gates

- [ ] **T014** Run focused tests, full regression, Ruff, cleanliness, compileall, source CLI smoke, package build, built-wheel install, and installed CLI smoke.
- [ ] **T015** Verify exact implementation diff remains inside Specification 024 authority and expected product surface.
- [ ] **T016** Require permanent five-cell push/PR CI success on the exact final implementation head and inspect all review comments/threads without treating unavailable review systems as PASS.
- [ ] **T017** Merge the product PR with expected-head protection.
- [ ] **T018** Require successful permanent post-product CI on the exact canonical merge and re-verify historical `v0.3.0` identity.

## Canonical closeout

- [ ] **T019** Add Specification 024 verification/review evidence and reconcile current program documentation without widening the delivered boundary.
- [ ] **T020** Require exact-head closeout CI, scope/review/thread/mergeability checks, and expected-head closeout merge.
- [ ] **T021** Require successful permanent post-closeout CI, re-read canonical governance, and mark Specification 024 `CLOSED_CANONICAL` only if every preceding gate is proven.

## Standing prohibitions

Until a separately shaped successor exists, Specification 024 tasks MUST NOT implement:

- `GRAIN -> READY` or later lifecycle mutation;
- executor/provider invocation;
- `ExecutionResult` ingestion;
- verification execution or evidence mutation;
- automatic context discovery or LLM context selection;
- WorkPacket or ContextSource version/schema redesign;
- stronger multi-writer locking;
- Spec Kit runtime integration;
- release publication;
- benchmark superiority claims.