# Tasks 002 — Lifecycle State

## Planning

- [x] T001 Re-read canonical `main` at `619b7501fc659588fc344af8835cc910a42bff31` and confirm 002 is next.
- [x] T002 Define the 14-state vocabulary and complete adjacency table.
- [x] T003 Record ADR-0004 separating transition legality from authorization.
- [x] T004 Define conservative exceptional recovery through `SHAPED`.

## Implementation

- [ ] T005 Add `SpecState`, lifecycle errors, immutable state classifications, and parser.
- [ ] T006 Implement immutable structural transition graph and `allowed_transitions`.
- [ ] T007 Implement `is_transition_allowed` and `require_transition_allowed`.
- [ ] T008 Integrate canonical state validation into `SpecNode` without changing valid-state content digests.
- [ ] T009 Export the 002 public lifecycle API from `specgrain`.

## Verification

- [ ] T010 Add exhaustive 14x14 transition-matrix tests.
- [ ] T011 Add parsing, classification, terminal-state, and exceptional-recovery tests.
- [ ] T012 Add SpecNode state-validation and Specification 001 digest-regression tests.
- [ ] T013 Run available full pytest/compile/lint checks and record exact evidence.
- [ ] T014 Review exact branch diff for authorization bypass or 003/004 scope creep.

## PR closeout

- [ ] T015 Open bounded PR with exact-head evidence.
- [ ] T016 Resolve all external/exact-head review defects.
- [ ] T017 Merge only with expected-head evidence, re-read canonical `main`, then begin `003-refinement-tree`.
