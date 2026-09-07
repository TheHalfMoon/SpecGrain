# Tasks 027 — Execution Attempt Identity Contract

## Shaping

- [x] T001 Re-read exact live canonical governance and confirm no active product specification remained after realized Specification 026 closure.
- [x] T002 Reproduce the repeated-execution attempt identity gap using supported deterministic APIs only.
- [x] T003 Qualify observation head `67f8562c30f7e2adfa3d93a82ca3cf0091c6f4e6` with CI `34163498855` success across all five permanent cells.
- [x] T004 Record bounded selection evidence and explicit non-authority boundary.
- [x] T005 Shape the smallest independent attempt-identity contract and ADR without product code.
- [x] T006 Qualify shaping head `e43a6680808b155010d2a4adeb7839fc417fe086` with push CI `34163943883` success 5/5.
- [x] T007 Qualify shaping PR #65 with PR CI `34164096581`, exact scope, mergeability, and review-state checks.
- [x] T008 Merge shaping with expected-head protection as `c1853d5b547c1f1ec14b5042917e824f4ad3975e`.
- [x] T009 Require canonical post-shaping CI `34164197679` success 5/5, reread authority, and confirm release unchanged.

## Product implementation

- [x] T010 Create `feat/027-execution-attempt-identity` from exact canonical post-shaping `main`.
- [x] T011 Implement isolated `ExecutionAttemptStatus` and `ExecutionAttemptRecord` contracts with strict version/ID/digest/status validation.
- [x] T012 Implement deterministic `content_dict()`, `to_dict()`, `to_json()`, `attempt_digest`, and strict `from_dict()`.
- [x] T013 Add focused tests proving separate occurrence identity for repeated packet/request/result content.
- [x] T014 Add progressive-binding tests for STARTED through terminal records without persistence or mutation.
- [x] T015 Prove malformed IDs/digests/status combinations and tampered declared digests fail closed.
- [x] T016 Prove existing WorkPacket, AgentRequest, and ExecutionResult v1 serialized identity remains unchanged.
- [x] T017 Prove attempt records confer no verification/lifecycle authority and add no runtime dependency.
- [x] T018 Run repository verification through configured CI; exact product-head workflow includes Ruff, regression, cleanliness, compile, CLI, package build, wheel install, and installed CLI smoke.
- [x] T019 Qualify exact product head `a795ac0de30ff254ce1697c49690a5f741c75fbe` through push CI `34164406219` success 5/5.
- [x] T020 Qualify product PR #66 with PR CI `34164578794`, exact scope, mergeability, and review-state checks.
- [x] T021 Merge product with expected-head protection as `08f3ca9e6bb46386e23a196339d7157362b2a9b6`.
- [x] T022 Require canonical post-product CI `34164674946` success across all five permanent cells.
- [x] T023 Reverify historical `v0.3.0` source/release/assets unchanged.

## Closeout

- [x] T024 Record exact implementation and verification evidence without expanding scope.
- [x] T025 Reconcile `specs/CURRENT.md`, roadmap/master-plan status, Specification 027 review/verification, and residual risks through documentation-only closeout.
- [ ] T026 Qualify and merge this closeout package under exact-head/review/CI rules, then require canonical post-closeout CI and release preservation.
- [ ] T027 Re-read canonical authority after the closeout merge; if all documented closure conditions hold, realize `CLOSED_CANONICAL` and return to bounded observation without inventing Specification 028.

T026/T027 are intentionally realized by live closeout merge/post-merge evidence. Do not create a recursive docs-only PR solely to write its own merge SHA/run ID or flip these final textual checkboxes.