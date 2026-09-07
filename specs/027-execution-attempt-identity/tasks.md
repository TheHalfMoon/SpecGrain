# Tasks 027 — Execution Attempt Identity Contract

## Shaping

- [x] T001 Re-read exact live canonical governance and confirm no active product specification remains after realized Specification 026 closure.
- [x] T002 Reproduce the repeated-execution attempt identity gap using supported deterministic APIs only.
- [x] T003 Qualify exact observation head `67f8562c30f7e2adfa3d93a82ca3cf0091c6f4e6` with CI `34163498855` success across all five permanent cells.
- [x] T004 Record the bounded selection evidence and explicit non-authority boundary.
- [x] T005 Shape the smallest independent attempt-identity contract and ADR without product code.
- [ ] T006 Qualify the exact shaping head with permanent five-cell push CI.
- [ ] T007 Open shaping PR and recheck exact base/head/scope, PR CI, reviews, comments, threads, mergeability, and review-system availability.
- [ ] T008 Merge shaping with expected-head protection only after all required gates pass.
- [ ] T009 Require canonical post-shaping CI success across all five permanent cells and re-read canonical authority.

## Product implementation

Blocked until T009.

- [ ] T010 Create `feat/027-execution-attempt-identity` from exact canonical post-shaping `main`.
- [ ] T011 Implement isolated `ExecutionAttemptStatus` and `ExecutionAttemptRecord` contracts with strict version/ID/digest/status validation.
- [ ] T012 Implement deterministic `content_dict()`, `to_dict()`, `to_json()`, `attempt_digest`, and strict `from_dict()`.
- [ ] T013 Add focused tests proving separate occurrence identity for repeated packet/request/result content.
- [ ] T014 Add progressive-binding tests for STARTED through terminal records without persistence or mutation.
- [ ] T015 Prove malformed IDs/digests/status combinations and tampered declared digests fail closed.
- [ ] T016 Prove existing WorkPacket, AgentRequest, and ExecutionResult v1 serialized identity remains unchanged.
- [ ] T017 Prove attempt records confer no verification/lifecycle authority and add no runtime dependency.
- [ ] T018 Run focused and full local verification available in the repository environment; record unavailable checks accurately.
- [ ] T019 Qualify exact product head through permanent five-cell push CI.
- [ ] T020 Open/update product PR; recheck exact base/head/scope, PR CI, reviews, comments, threads, mergeability, and review-system availability.
- [ ] T021 Merge product with expected-head protection only after exact qualification.
- [ ] T022 Require canonical post-product CI success across all five permanent cells.
- [ ] T023 Reverify historical `v0.3.0` source/release/assets unchanged.

## Closeout

- [ ] T024 Record exact implementation and verification evidence without expanding scope.
- [ ] T025 Reconcile `specs/CURRENT.md`, roadmap/master-plan status, Specification 027 review/verification, and residual risks through documentation-only closeout if required.
- [ ] T026 Qualify and merge closeout/reconciliation under the same exact-head/review/CI rules.
- [ ] T027 Re-read canonical authority after final merge; if all closure conditions hold, realize `CLOSED_CANONICAL` and return to bounded observation without inventing Specification 028.