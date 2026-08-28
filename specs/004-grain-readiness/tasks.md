# Tasks 004 — Grain Readiness

## Planning

- [x] T001 Re-read canonical `main` at `7f4682f88dd9988f12f2a466c071beb67d660a2d` and confirm 004 is next.
- [x] T002 Define readiness-v1 authored metadata, risk/context/evidence contracts, and explicit future-owner boundaries.
- [x] T003 Define binary report/error API with no score and no state mutator.
- [x] T004 Map Ponytail/Karpathy/Spec Kit donor lessons into deterministic declarations without prompt coupling.

## Implementation

- [x] T005 Add readiness enums, issue/report/error models, and version constant.
- [x] T006 Implement forest/candidate binding and structural blocker mapping.
- [x] T007 Implement leaf, state, acceptance, scope, and change-surface gates.
- [x] T008 Implement risk/recovery and context-fit gates.
- [x] T009 Implement evidence, unresolved-decision, minimality, and safety declaration gates.
- [x] T010 Implement deterministic report ordering and require helper.
- [x] T011 Export public readiness API.

## Verification

- [x] T012 Add passing-candidate and no-mutation tests.
- [x] T013 Add structural/candidate/state/leaf tests.
- [x] T014 Add scope/change-surface/risk/context/evidence tests.
- [x] T015 Add readiness-version/decision/minimality/safety tests.
- [x] T016 Add issue-order/error-report tests and run all 001–004 tests: 182 pytest tests PASS, compileall PASS, Ruff NOT RUN because unavailable.
- [x] T017 Review initial exact PR head `f8e4e3a2e32647cc324b1c059b2c9d0c173db561`; no runtime scope creep found, but remediate F-001 contract ambiguity so a passing report cannot be treated as reusable lifecycle authority.

## PR closeout

- [x] T018 Open bounded implementation PR #6 with exact-head evidence.
- [x] T019 Remediate F-001 at final head `11e43617590aca0e61b73f00e53e3783aff4f4ad`; CodeRabbit SUCCESS, no unresolved review threads, remediation docs-only, and exact-head internal review recorded as COMMENT because GitHub forbids self-approval.
- [x] T020 Merge PR #6 with expected-head guard; canonical merge commit is `2a719a8ed2a7c22c0f65402c95361b32b230b511`, then re-read canonical `main` before beginning 005.

**Result:** `CLOSED_CANONICAL` at merge commit `2a719a8ed2a7c22c0f65402c95361b32b230b511`.
