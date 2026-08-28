# Tasks 003 — Refinement Tree

## Planning

- [x] T001 Re-read canonical `main` at `2c3d87bd95f57286f494adbd84c58c8cd877bfd6` and confirm 003 is next.
- [x] T002 Define structural forest invariants and explicit semantic/readiness exclusions.
- [x] T003 Choose dependency-free functions plus structured issues instead of a heavyweight forest abstraction.
- [x] T004 Define identity-blocker and deterministic issue/cycle ordering rules.

## Implementation

- [ ] T005 Add refinement issue codes, immutable issue model, and aggregate error.
- [ ] T006 Implement materialization/type/duplicate-ID validation.
- [ ] T007 Implement missing/self reference checks.
- [ ] T008 Implement reciprocal parent/child consistency checks.
- [ ] T009 Implement deterministic cycle detection and canonical cycle reporting.
- [ ] T010 Implement valid-forest root query and public exports.

## Verification

- [ ] T011 Add valid empty/single/multi/deep forest tests.
- [ ] T012 Add duplicate/missing/self/reciprocity malformed-forest tests.
- [ ] T013 Add deterministic 2-node/3-node cycle tests.
- [ ] T014 Add input-order invariance and fail-closed root-query tests.
- [ ] T015 Run full available pytest/compile/lint checks and record evidence.
- [ ] T016 Review exact diff for 004 readiness, 006 dependency-DAG, CLI/store, or semantic-decomposition creep.

## PR closeout

- [ ] T017 Open bounded implementation PR with exact-head evidence.
- [ ] T018 Resolve all external/exact-head review defects.
- [ ] T019 Merge only with expected-head evidence, re-read canonical `main`, then begin `004-grain-readiness`.
