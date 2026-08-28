# Tasks 003 — Refinement Tree

## Planning

- [x] T001 Re-read canonical `main` at `2c3d87bd95f57286f494adbd84c58c8cd877bfd6` and confirm 003 is next.
- [x] T002 Define structural forest invariants and explicit semantic/readiness exclusions.
- [x] T003 Choose dependency-free functions plus structured issues instead of a heavyweight forest abstraction.
- [x] T004 Define identity-blocker and deterministic issue/cycle ordering rules.

## Implementation

- [x] T005 Add refinement issue codes, immutable issue model, and aggregate error.
- [x] T006 Implement materialization/type/duplicate-ID validation.
- [x] T007 Implement missing/self reference checks.
- [x] T008 Implement reciprocal parent/child consistency checks.
- [x] T009 Implement deterministic cycle detection across the union of declared refinement edges.
- [x] T010 Implement valid-forest root query and public exports.

## Verification

- [x] T011 Add valid empty/single/multi/deep forest tests.
- [x] T012 Add duplicate/missing/self/reciprocity malformed-forest tests.
- [x] T013 Add deterministic reciprocal and child-list-only cycle tests.
- [x] T014 Add input-order invariance and fail-closed root-query tests.
- [x] T015 Run full available pytest/compile/lint checks after cycle remediation: 116 pytest tests PASS, compileall PASS, Ruff NOT RUN because unavailable.
- [x] T016 Review initial exact head `f3084543f66c22ec2bf7d84522e2498f5f312292`; find and remediate F-001 where cycle detection considered only `parent_id` despite the broader declared-edge contract.

## PR closeout

- [x] T017 Open bounded implementation PR #5 with exact-head evidence.
- [x] T018 Resolve exact-head review defect F-001; final head `854cbe7efa5cd6357f0b2d1fb889bac9787d9726` had CodeRabbit SUCCESS and no unresolved review threads.
- [x] T019 Merge PR #5 with expected-head guard; canonical merge commit is `7f4682f88dd9988f12f2a466c071beb67d660a2d`, then re-read canonical `main` before beginning `004-grain-readiness`.

**Result:** `CLOSED_CANONICAL` at merge commit `7f4682f88dd9988f12f2a466c071beb67d660a2d`.
