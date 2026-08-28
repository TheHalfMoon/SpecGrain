# Tasks 014 — Agent Adapters

## Planning

- [x] T001 Re-read canonical `main`, `AGENTS.md`, `CURRENT.md`, constitution, execution master plan, roadmap, and WorkPacket/result contracts.
- [x] T002 Close Specification 013 from PR #15 exact-head/post-merge evidence.
- [x] T003 Record ADR-0014 generic agent-adapter boundary and vendor-demand deferral.
- [x] T004 Define request/result normalization contracts and exact change surface.

## Implementation

- [ ] T005 Add immutable adapter kind/request/error contracts and deterministic request digest.
- [ ] T006 Implement exact `generic-json` and deterministic `generic-markdown` WorkPacket rendering.
- [ ] T007 Implement strict object/JSON executor-result normalization with adapter-owned packet binding.
- [ ] T008 Add bounded public exports without modifying core packet semantics.

## Verification

- [ ] T009 Test request determinism, packet binding, and round-trip representation.
- [ ] T010 Test strict result normalization, spoof/unknown-field rejection, duplicate/non-finite JSON rejection, and canonical ExecutionResult output.
- [ ] T011 Run full 001–014 regression plus compile/package/entry-point and available static checks.
- [ ] T012 Review exact uploaded diff for execution, network, credential, provider, lifecycle, verification-authority, or dependency creep.

## PR closeout

- [ ] T013 Open bounded PR with exact-head evidence.
- [ ] T014 Resolve every material exact-head review defect.
- [ ] T015 Merge only with expected-head evidence, re-read canonical `main`, then begin 015.
