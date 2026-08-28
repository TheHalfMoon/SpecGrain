# Tasks 014 — Agent Adapters

## Planning

- [x] T001 Re-read canonical `main`, `AGENTS.md`, `CURRENT.md`, constitution, execution master plan, roadmap, and WorkPacket/result contracts.
- [x] T002 Close Specification 013 from PR #15 exact-head/post-merge evidence.
- [x] T003 Record ADR-0014 generic agent-adapter boundary and vendor-demand deferral.
- [x] T004 Define request/result normalization contracts and exact change surface.

## Implementation

- [x] T005 Add immutable adapter kind/request/error contracts and deterministic request digest.
- [x] T006 Implement exact `generic-json` and deterministic `generic-markdown` WorkPacket rendering.
- [x] T007 Implement strict object/JSON executor-result normalization with adapter-owned packet binding.
- [x] T008 Publish the bounded `specgrain.adapter` module surface without modifying core packet semantics or root exports.

## Verification

- [x] T009 Test request determinism, packet binding, and round-trip representation.
- [x] T010 Test strict result normalization, spoof/unknown-field rejection, duplicate/non-finite JSON rejection, and canonical ExecutionResult output.
- [x] T011 Run full 001–014 regression plus install, Ruff, compile, entry-point parity, and line-length gates on identical product/test blobs.
- [x] T012 Review exact uploaded diff for execution, network, credential, provider, lifecycle, verification-authority, or dependency creep.

## PR closeout

- [x] T013 Open bounded PR #16 with exact-head evidence.
- [x] T014 Resolve every material exact-head review defect; external automated review was unavailable/skipped and no manual exact-head defect remained.
- [x] T015 Merge PR #16 with expected head `35db1bb8a078a68f412def8b50fa4f4e65b7afe5`, re-read canonical merge `b37ea3a06f86d68cb220ec1cd6cc57e71e76653f`, then begin 015.
