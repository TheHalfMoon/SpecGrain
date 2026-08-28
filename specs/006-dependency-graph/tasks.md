# Tasks 006 — Dependency Graph

## Planning

- [x] T001 Re-read canonical `main` at `ccd4a825c2a951a8000a2833ede05cdb3218d477`, AGENTS, constitution, roadmap, architecture, lifecycle, and local-store contracts; confirm 006 is next.
- [x] T002 Close Specification 005 canonical task state from PR #7 exact-head/merge evidence.
- [x] T003 Record ADR-0006 dependency satisfied/waiting/hard-blocker semantics.
- [x] T004 Define structural dependency invariants, ready-set semantics, blocker propagation, and advisory wave projection.
- [x] T005 Define read-only `next` integration and explicit non-goals.

## Implementation

- [ ] T006 Add dependency issue/report/error models and lifecycle-state classifications.
- [ ] T007 Implement duplicate/missing/self dependency validation.
- [ ] T008 Implement deterministic dependency cycle detection.
- [ ] T009 Implement Grain dependency reports with direct waiting + transitive blocker propagation.
- [ ] T010 Implement `ready_grains` and deterministic Grain wave projection.
- [ ] T011 Integrate dependency validation into local `check_project` before readiness summaries.
- [ ] T012 Add structured `next_project` local-product orchestration.
- [ ] T013 Add `specgrain next [PATH] [--json]` without mutation.
- [ ] T014 Export the bounded 006 public API.

## Verification

- [ ] T015 Add structural dependency and cycle-determinism tests.
- [ ] T016 Add satisfied/waiting/blocker/report/ready-set tests.
- [ ] T017 Add wave projection and transitive blocker tests.
- [ ] T018 Add store check/next integration and read-only tests.
- [ ] T019 Add CLI next text/JSON/exit-code tests.
- [ ] T020 Run all 001–006 tests plus compile/package/smoke and available lint/static checks.
- [ ] T021 Review exact diff for mutation, scan, semantic inference, conflict analysis, evidence, execution, or dependency-library creep.

## PR closeout

- [ ] T022 Open bounded implementation PR with exact-head evidence.
- [ ] T023 Resolve every exact-head external/repository review defect.
- [ ] T024 Merge only with expected-head evidence, re-read canonical `main`, then begin `007-repository-scan`.
