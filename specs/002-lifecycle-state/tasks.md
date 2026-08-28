# Tasks 002 — Lifecycle State

## Planning

- [x] T001 Re-read canonical `main` at `619b7501fc659588fc344af8835cc910a42bff31` and confirm 002 is next.
- [x] T002 Define the 14-state vocabulary and complete adjacency table.
- [x] T003 Record ADR-0004 separating transition legality from authorization.
- [x] T004 Define conservative exceptional recovery through `SHAPED`.

## Implementation

- [x] T005 Add `SpecState`, lifecycle errors, immutable state classifications, and parser.
- [x] T006 Implement immutable structural transition graph and `allowed_transitions`.
- [x] T007 Implement `is_transition_allowed` and `require_transition_allowed`.
- [x] T008 Integrate canonical state validation into `SpecNode` without changing valid-state content digests.
- [x] T009 Export the 002 public lifecycle API from `specgrain`.

## Verification

- [x] T010 Add exhaustive 14x14 transition-matrix tests.
- [x] T011 Add parsing, classification, terminal-state, and exceptional-recovery tests.
- [x] T012 Add SpecNode state-validation and Specification 001 digest-regression tests.
- [x] T013 Run available full pytest/compile/lint checks and record exact evidence: 98 pytest tests PASS, compileall PASS, Ruff NOT RUN because unavailable.
- [x] T014 Review exact implementation diff at `526dcc4de03d2338f1842475573d2064ccb5a45f` for authorization bypass or 003/004 scope creep; none found.

## PR closeout

- [ ] T015 Open bounded PR with exact-head evidence.
- [ ] T016 Resolve all external/exact-head review defects.
- [ ] T017 Merge only with expected-head evidence, re-read canonical `main`, then begin `003-refinement-tree`.
