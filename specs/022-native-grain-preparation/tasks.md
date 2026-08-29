# Tasks 022 — Native Grain Preparation

## Shaping

- [x] T001 Re-read live canonical `main`, AGENTS, CURRENT, constitution, execution master plan, roadmap, v0.3 audit, current CLI/store/readiness/lifecycle source, and live PR/issue state.
- [x] T002 Reproduce the maintainer-supplied external adoption finding against canonical source: native v0.3 authoring stops at DRAFT while readiness only evaluates REFINING leaves and `next` only considers GRAIN nodes.
- [x] T003 Record the fresh adoption-friction audit and select the smallest pre-execution frontier rather than a full DRAFT-to-VERIFIED expansion.
- [x] T004 Record ADR-0019 bounded pre-Grain mutation authority.
- [x] T005 Shape Specification 022 outcome, scope, command contracts, acceptance gates, risks, plan, and expected change surface.
- [x] T006 Merge the exact shaping head with expected-head protection and prove canonical post-shaping `main`/CI before implementation. PR #37 merged as `4919a4261f649e81cb1f507c0e80bc5c98d848d8`; post-merge CI `33260132438` succeeded.

## Implementation

- [x] T007 Add bounded API support for explicit DRAFT shaping to SHAPED with exact-preimage single-file replacement.
- [x] T008 Add state-only SHAPED-to-REFINING mutation with semantic revision preservation.
- [x] T009 Add readiness-gated REFINING-to-GRAIN promotion with deterministic blocker/no-mutation behavior.
- [x] T010 Add `shape`, `refine`, and `grain` CLI surfaces with deterministic text/JSON output and stable failures.
- [x] T011 Export the bounded public API and preserve existing compatibility surfaces.
- [x] T012 Add focused API/CLI tests covering success, wrong states, invalid declarations, dependencies, pending recovery, drift, readiness blockers, revision preservation, and `next` integration.
- [x] T013 Reconcile README/architecture/changelog and launch guards to distinguish current-source Specification 022 behavior from the historical v0.3.0 release contract.

## Verification and product merge

- [x] T014 Bind focused/full/static/package/launch verification to final product head `8af20015bd59424c7882b8c8fa7ea4c78e0af2e5`. Push CI `33261979828` and PR CI `33261982603` both completed `success` across all five permanent cells; Ubuntu/Python 3.11 recorded 575 passing tests plus all required static/package/CLI gates.
- [x] T015 Review the final exact diff for hidden defaults, readiness weakening, lifecycle edge skipping, semantic mutation outside shape, post-GRAIN authority, recovery widening, dependency creep, unrelated scope, and false historical v0.3.0 claims. The premature shape-time readiness gate was repaired forward before final head.
- [x] T016 Open bounded implementation PR #38 from exact shaped canonical base `4919a4261f649e81cb1f507c0e80bc5c98d848d8` and prove permanent five-cell CI on exact PR head `8af20015bd59424c7882b8c8fa7ea4c78e0af2e5`.
- [x] T017 Resolve every material review defect without treating unavailable/skipped bots as PASS. Both CodeRabbit inline threads were resolved; the global SpecNode-validation finding was withdrawn after scoped re-verification. Qodo and final-head automatic CodeRabbit review remained unavailable/skipped and were recorded as such.
- [x] T018 Merge PR #38 with expected-head protection and prove canonical product merge `653cfb64c8885174ea3ea729d1bbb6418613b10d`, exact parentage, post-product five-cell CI `33262123902`, and historical v0.3.0 release preservation.

## Canonical closeout

- [x] T019 Record exact implementation head, final candidate CI, review state, merge parentage, canonical post-product CI, historical-release preservation, and the bounded multi-writer residual in documentation-only closeout evidence.
- [x] T020 Re-evaluate the next frontier from post-022 product truth. No successor product scope is automatically authorized; the program returns to observation/evidence gathering, including the planned external architectural review and GitHub Spec Kit comparison.
- [ ] T021 Merge the exact documentation-only closeout head with expected-head protection after its permanent five-cell CI and review/mergeability checks succeed.
- [ ] T022 Prove the resulting canonical `main`, post-closeout five-cell CI, preserved `v0.3.0` tag/release/assets, merged/closed implementation and closeout PRs, and only then declare Specification 022 `CLOSED_CANONICAL`.

## Closure rule

T021 and T022 are intentionally open on this closeout candidate. They may be marked complete only from exact canonical evidence after the closeout PR is merged. Until then, Specification 022 is product-merged and post-product verified but not `CLOSED_CANONICAL`.