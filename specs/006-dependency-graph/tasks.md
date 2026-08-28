# Tasks 006 — Dependency Graph

## Planning

- [x] T001 Re-read canonical `main` at `ccd4a825c2a951a8000a2833ede05cdb3218d477`, AGENTS, constitution, roadmap, architecture, lifecycle, and local-store contracts; confirm 006 is next.
- [x] T002 Close Specification 005 canonical task state from PR #7 exact-head/merge evidence.
- [x] T003 Record ADR-0006 dependency satisfied/waiting/hard-blocker semantics.
- [x] T004 Define structural dependency invariants, ready-set semantics, blocker propagation, and advisory wave projection.
- [x] T005 Define read-only `next` integration and explicit non-goals.

## Implementation

- [x] T006 Add dependency issue/report/error models and lifecycle-state classifications.
- [x] T007 Implement duplicate/missing/self dependency validation.
- [x] T008 Implement deterministic dependency cycle detection.
- [x] T009 Implement Grain dependency reports with direct waiting + transitive blocker propagation.
- [x] T010 Implement `ready_grains` and deterministic Grain wave projection.
- [x] T011 Integrate dependency validation into local project checks before readiness summaries through a bounded project orchestration layer while leaving Specification 005 persistence unchanged.
- [x] T012 Add structured `next_project` local-product orchestration.
- [x] T013 Add `specgrain next [PATH] [--json]` without mutation.
- [x] T014 Export the bounded 006 public API.

## Verification

- [x] T015 Add structural dependency and cycle-determinism tests.
- [x] T016 Add satisfied/waiting/blocker/report/ready-set tests.
- [x] T017 Add wave projection and transitive blocker tests.
- [x] T018 Add local check/next integration and read-only tests.
- [x] T019 Add CLI next text/JSON/exit-code tests.
- [x] T020 Run all 001–006 tests plus compile/package/smoke and available lint/static checks: 275 pytest tests PASS, compileall PASS, editable install PASS, console/module help equivalence PASS, 0 lines >100; Ruff NOT RUN because unavailable/offline.
- [x] T021 Review exact uploaded implementation head `72409ba2881b04a7db41a3b30b9dc05c9eb69603`; no material defect or scope/trust-boundary leak remains. See `review.md`.

## PR closeout

- [ ] T022 Open bounded implementation PR with exact-head evidence.
- [ ] T023 Resolve every exact-head external/repository review defect.
- [ ] T024 Merge only with expected-head evidence, re-read canonical `main`, then begin `007-repository-scan`.
