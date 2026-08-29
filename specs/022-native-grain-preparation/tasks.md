# Tasks 022 — Native Grain Preparation

## Shaping

- [x] T001 Re-read live canonical `main`, AGENTS, CURRENT, constitution, execution master plan, roadmap, v0.3 audit, current CLI/store/readiness/lifecycle source, and live PR/issue state.
- [x] T002 Reproduce the maintainer-supplied external adoption finding against canonical source: native v0.3 authoring stops at DRAFT while readiness only evaluates REFINING leaves and `next` only considers GRAIN nodes.
- [x] T003 Record the fresh adoption-friction audit and select the smallest pre-execution frontier rather than a full DRAFT-to-VERIFIED expansion.
- [x] T004 Record ADR-0019 bounded pre-Grain mutation authority.
- [x] T005 Shape Specification 022 outcome, scope, command contracts, acceptance gates, risks, plan, and expected change surface.
- [ ] T006 Merge the exact shaping head with expected-head protection and prove canonical post-shaping `main`/CI before implementation.

## Implementation

- [ ] T007 Add store/API support for explicit DRAFT shaping to SHAPED with exact-preimage single-file replacement.
- [ ] T008 Add state-only SHAPED-to-REFINING mutation with semantic revision preservation.
- [ ] T009 Add readiness-gated REFINING-to-GRAIN promotion with deterministic blocker/no-mutation behavior.
- [ ] T010 Add `shape`, `refine`, and `grain` CLI surfaces with deterministic text/JSON output and stable failures.
- [ ] T011 Export the bounded public API and preserve existing compatibility surfaces.
- [ ] T012 Add focused API/CLI tests covering success, wrong states, invalid declarations, dependencies, pending recovery, drift, readiness blockers, revision preservation, and `next` integration.
- [ ] T013 Update README/architecture/changelog to the exact newly supported pre-execution workflow without implying READY/execution/verification authority.

## Verification and product merge

- [ ] T014 Run focused tests, full regression, Ruff, compileall, tracked-tree cleanliness, CLI help/smoke, package build, built-wheel install, and launch/document guards.
- [ ] T015 Review the exact diff for hidden defaults, readiness weakening, lifecycle edge skipping, semantic mutation outside shape, post-GRAIN authority, recovery widening, dependency creep, and unrelated scope.
- [ ] T016 Open a bounded implementation PR from the exact shaped canonical base and prove permanent five-cell CI on the exact PR head.
- [ ] T017 Resolve every material exact-head review defect; do not treat unavailable/skipped review bots as PASS.
- [ ] T018 Merge the product PR only with expected-head protection and prove canonical post-merge `main`, CI, and historical v0.3.0 release no-mutation behavior.

## Canonical closeout

- [ ] T019 Record exact implementation head, CI jobs, review state, merge parentage, canonical post-merge CI, and release-verification evidence.
- [ ] T020 Re-evaluate the next frontier from post-022 product truth; do not pre-authorize WorkPacket/executor scope merely because it is the likely next idea.
- [ ] T021 Merge a documentation-only closeout with expected-head protection.
- [ ] T022 Prove final canonical `main`, post-closeout CI, release target preservation, closed PRs, and Specification 022 `CLOSED_CANONICAL`.
