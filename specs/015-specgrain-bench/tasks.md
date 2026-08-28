# Tasks 015 — SpecGrainBench

## Planning

- [x] T001 Re-read canonical post-014 `main`, benchmark strategy, roadmap, and cross-spec execution rules.
- [x] T002 Close Specification 014 from PR #16 exact-head/post-merge evidence.
- [x] T003 Record ADR-0015 deterministic reproducible benchmark ledger.
- [x] T004 Define canonical arms, case/run/preflight/report contracts, and no-automatic-winner rule.

## Implementation

- [ ] T005 Add immutable benchmark case/arm/run contracts and stable digests.
- [ ] T006 Implement strict initial-arm plan validation and expected cell generation.
- [ ] T007 Implement contamination/missing-cell preflight with stable issue codes.
- [ ] T008 Implement deterministic arm summaries and report serialization without filtering failed runs or declaring a winner.

## Verification

- [ ] T009 Test canonical arm/config/cell validation and deterministic digests.
- [ ] T010 Test contamination detection for workspace/context reuse, baseline/config mismatch, scorer leakage, missing/duplicate cells.
- [ ] T011 Test failure retention, metrics aggregation, and no-winner report semantics.
- [ ] T012 Run exact full regression, Ruff, compile, install, entry-point parity, and line-length gates.
- [ ] T013 Review exact diff for hidden exclusions, ranking claims, process/network execution, actor scoring, or dependency creep.

## PR closeout

- [ ] T014 Open bounded PR with exact-head evidence.
- [ ] T015 Resolve every material exact-head review defect.
- [ ] T016 Merge only with expected-head evidence, re-read canonical `main`, then begin 016.
