# Tasks 007 — Repository Scan

## Planning

- [x] T001 Re-read canonical `main` at `85d1bef8ee5c1c8e8d78baa52f509803a78a43d8`, AGENTS, constitution, roadmap, architecture, and 006 contracts; confirm 007 is next.
- [x] T002 Close Specification 006 canonical task state from PR #8 exact-head/merge evidence.
- [x] T003 Record ADR-0007 bounded/read-only repository scan trust boundary.
- [x] T004 Define scan models, limits, normalized digest, signals, Git facts, and CLI contract.

## Implementation

- [ ] T005 Add repository scan records/errors/limits and canonical map digest.
- [ ] T006 Implement deterministic bounded traversal, ignore rules, and symlink non-following.
- [ ] T007 Implement manifest/language/test/config/component signals.
- [ ] T008 Implement bounded dependency extraction for pyproject/package/Cargo/go manifests.
- [ ] T009 Implement safe ordinary/indirect/absent Git facts without subprocesses.
- [ ] T010 Add `specgrain scan [PATH] [--json]` and bounded exports.

## Verification

- [ ] T011 Add traversal/limit/symlink/determinism tests.
- [ ] T012 Add manifest/dependency/language/test/config/component tests.
- [ ] T013 Add Git facts/digest/no-mutation/no-environment-leak tests.
- [ ] T014 Add CLI text/JSON/error tests.
- [ ] T015 Run all 001–007 tests plus compile/package/smoke and available lint/static checks.
- [ ] T016 Review exact uploaded diff for semantic indexing, subprocess, mutation, context, evidence, scheduler, or dependency creep.

## PR closeout

- [ ] T017 Open bounded implementation PR with exact-head evidence.
- [ ] T018 Resolve every exact-head external/repository review defect.
- [ ] T019 Merge only with expected-head evidence, re-read canonical `main`, then begin `008-context-budget`.
