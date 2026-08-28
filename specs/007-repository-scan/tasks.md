# Tasks 007 — Repository Scan

## Planning

- [x] T001 Re-read canonical `main` at `85d1bef8ee5c1c8e8d78baa52f509803a78a43d8`, AGENTS, constitution, roadmap, architecture, and 006 contracts; confirm 007 is next.
- [x] T002 Close Specification 006 canonical task state from PR #8 exact-head/merge evidence.
- [x] T003 Record ADR-0007 bounded/read-only repository scan trust boundary.
- [x] T004 Define scan models, limits, normalized digest, signals, Git facts, and CLI contract.

## Implementation

- [x] T005 Add repository scan records/errors/limits and canonical map digest.
- [x] T006 Implement deterministic bounded traversal, ignore rules, and symlink non-following.
- [x] T007 Implement manifest/language/test/config/component signals.
- [x] T008 Implement bounded dependency extraction for pyproject/package/Cargo/go manifests.
- [x] T009 Implement safe ordinary/indirect/absent Git facts without subprocesses.
- [x] T010 Add `specgrain scan [PATH] [--json]` and bounded exports.

## Verification

- [x] T011 Add traversal/limit/symlink/determinism tests.
- [x] T012 Add manifest/dependency/language/test/config/component tests.
- [x] T013 Add Git facts/digest/no-mutation/no-environment-leak tests.
- [x] T014 Add CLI text/JSON/error tests.
- [x] T015 Run all 001–007 tests plus compile/package/smoke and available lint/static checks.
- [x] T016 Review exact uploaded diff for semantic indexing, subprocess, mutation, context, evidence, scheduler, or dependency creep.

## PR closeout

- [x] T017 Open bounded implementation PR #9 from exact branch head; final reviewed PR head was `35571d5cdcbe441b04a8e975c5eb6be0fe088698`.
- [x] T018 Resolve exact-head defects: repository review found and repaired stale master-plan state; CodeRabbit status was success on the final head but automatic substantive review was unavailable for the repository; Qodo was unavailable because its trial ended; no review threads or material external defects remained.
- [x] T019 Merge PR #9 with `expected_head_sha=35571d5cdcbe441b04a8e975c5eb6be0fe088698`; re-read canonical `main` at merge commit `197ddfb68d94bf8998d68d1371c26431f3816ca0`, whose second parent is the expected PR head; begin `008-context-budget`.
