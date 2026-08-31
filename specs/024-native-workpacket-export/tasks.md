# Tasks 024 — Native WorkPacket Export

## Shaping and authority

- [x] **T001** Reproduce the post-023 native WorkPacket handoff discontinuity on exact canonical base `f2e8378dcba0cfea2beedc6da61324b0c3fea95e`.
- [x] **T002** Prove the final observation fixture on exact head `95e5358ed420cd2e6fbd0bc7c56690763cea1283` with permanent CI run `33416110142` succeeding across all five cells.
- [x] **T003** Shape the smallest candidate boundary: read-only native WorkPacket export from an existing dependency-eligible `GRAIN`.
- [x] **T004** Verify the exact shaping head changes only authorized research/governance/specification paths, passes permanent five-cell CI, has no unresolved material review threads, and is mergeable. Exact shaping head `043abdf8f15f688cdbae746c0abd83dda74d0dae`; push CI `33416602621` and PR CI `33416635970` both completed `success`; PR #49 had no submitted reviews or inline review threads and was mergeable before merge.
- [x] **T005** Merge the shaping PR with expected-head protection and require successful permanent post-shaping CI on canonical `main` before product implementation begins. PR #49 merged as canonical shaping merge `440a8b14459ade2fe8235cc873229dd87ba926b5`; post-shaping CI `33416908615` completed `success` across all five permanent cells.

## Product implementation

- [x] **T006** Add the bounded `specgrain packet <spec_id> [path] --context-sources <json-file> [--json]` command without lifecycle or evidence mutation.
- [x] **T007** Add strict bounded ContextSource-file parsing that rejects unsafe/non-canonical input and delegates semantic field validation to existing context primitives.
- [x] **T008** Require exact stored `GRAIN` state and current dependency eligibility before export.
- [x] **T009** Apply the stored Grain token budget through existing `ContextBudgetPolicy` / `require_context_budget` semantics.
- [x] **T010** Build the export exclusively through existing `build_work_packet` and preserve existing packet/context contract versions and digest semantics.
- [x] **T011** Add stable text and full canonical JSON stdout behavior plus current CLI failure conventions.
- [x] **T012** Add focused cross-platform tests for valid export, API/CLI equality, determinism, non-mutation, state/dependency gates, malformed context input, budget failure, and bounded file safety.
- [x] **T013** Update current-source README command documentation without rewriting historical `v0.3.0` claims.

## Product merge gates

- [x] **T014** Run focused tests, full regression, Ruff, cleanliness, compileall, source CLI smoke, package build, built-wheel install, and installed CLI smoke. Final implementation head `7e1db87f69108fc8693b987e77d20f92e4f46866` passed push CI `33421885016` across all five permanent cells; Ubuntu/Python 3.11 recorded `592 passed` plus every required gate.
- [x] **T015** Verify exact implementation diff remains inside Specification 024 authority and expected product surface. Final diff from canonical shaped base `440a8b14459ade2fe8235cc873229dd87ba926b5` changed exactly `README.md`, `src/specgrain/cli.py`, `tests/test_workpacket_cli.py`, `tests/test_launch.py`, and `tests/test_repository_cli.py`; the latter two are explicit test-only regression compatibility exceptions and add no runtime authority.
- [x] **T016** Require permanent five-cell push/PR CI success on the exact final implementation head and inspect all review comments/threads without treating unavailable review systems as PASS. Push CI `33421885016` and PR CI `33422062846` completed `success`; PR #50 had no submitted reviews or inline threads; Qodo was billing-blocked, automatic CodeRabbit review was skipped by repository-star policy, and Cubic was descriptive only.
- [x] **T017** Merge the product PR with expected-head protection. PR #50 merged exact head `7e1db87f69108fc8693b987e77d20f92e4f46866` as canonical product merge `1666ba8c135ee8575f1546019ab592db32947dd2`.
- [x] **T018** Require successful permanent post-product CI on the exact canonical merge and re-verify historical `v0.3.0` identity. Canonical post-product CI `33422235433` completed `success` across all five cells; `v0.3.0` remained at source `70dd66aba0e68ae710e6ef12605ed153d107bab4`, Release `378962445`, with historical asset identities/digests unchanged.

## Canonical closeout

- [x] **T019** Add Specification 024 verification/closeout evidence and reconcile current program documentation without widening the delivered boundary. This documentation-only closeout candidate records all product evidence already proven and does not declare final canonical closure.
- [ ] **T020** Require exact-head closeout CI, scope/review/thread/mergeability checks, and expected-head closeout merge.
- [ ] **T021** Require successful permanent post-closeout CI, re-read canonical governance, and publish Specification 024 as `CLOSED_CANONICAL` only through final evidence reconciliation after every preceding gate is proven.

## Superseded implementation evidence

Failed pre-final implementation runs are retained rather than hidden:

- head `e0ec4b400d9a5df815382c6f3e8070b6358d0afc`, run `33417702813` — regression exposed stale test assumptions and fixture defects;
- head `482606f0a8632d1a391aa2a059354b320419d477`, run `33421661140` — only the remaining help-format smoke assertion failed;
- both were corrected without weakening product invariants before final head `7e1db87f69108fc8693b987e77d20f92e4f46866` passed all gates.

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
