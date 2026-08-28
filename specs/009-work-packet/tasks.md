# Tasks 009 — Work Packet

## Planning

- [x] T001 Re-read canonical `main` at `e1336acc3f764241d79d5051f34309ae2f66d6e4`, AGENTS, constitution, execution master plan, roadmap, architecture, SpecNode, and 008 contracts; confirm 009 is next.
- [x] T002 Close Specification 008 canonical task state from PR #10 exact-head/post-merge evidence.
- [x] T003 Record ADR-0009 portable digest-bound WorkPacket / executor self-report authority boundary.
- [x] T004 Define packet context snapshot, WorkPacket, ExecutionResult, normalization, digest, and builder contracts.

## Implementation

- [x] T005 Add packet validation helpers and portable selected-context snapshot.
- [x] T006 Add immutable WorkPacket model, canonical serialization, and digest.
- [x] T007 Add strict WorkPacket deserialization with unknown-field/tamper rejection.
- [x] T008 Add provider-neutral ExecutionResult status/error contract and digest.
- [x] T009 Add strict ExecutionResult deserialization and tamper rejection.
- [x] T010 Add `build_work_packet` composition from SpecNode + passing context plan.
- [x] T011 Add bounded public exports without CLI/store/lifecycle changes.

## Verification

- [x] T012 Add packet/source validation, immutability, normalization, and revision-binding tests.
- [x] T013 Add permutation/digest/JSON round-trip/tamper tests.
- [x] T014 Add ExecutionResult status/error/digest/self-report tests.
- [x] T015 Run all 001–009 tests plus compile/package/entry-point and available lint/static checks.
- [x] T016 Review exact uploaded diff for executor/provider/prompt, verification/evidence, lifecycle/store/scheduler, CLI, subprocess, or dependency creep.

## PR closeout

- [ ] T017 Open bounded implementation PR with exact-head evidence.
- [ ] T018 Resolve every material exact-head external/repository review defect.
- [ ] T019 Merge only with expected-head evidence, re-read canonical `main`, then begin `010-verification-evidence`.