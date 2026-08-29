# Tasks 015 — SpecGrainBench

## Planning

- [x] T001 Re-read canonical post-014 `main`, benchmark strategy, roadmap, and cross-spec execution rules.
- [x] T002 Close Specification 014 from PR #16 exact-head/post-merge evidence.
- [x] T003 Record ADR-0015 deterministic reproducible benchmark ledger.
- [x] T004 Define canonical arms, case/run/preflight/report contracts, and no-automatic-winner rule.

## Implementation

- [x] T005 Add immutable benchmark case/arm/run contracts and stable digests.
- [x] T006 Implement strict initial-arm plan validation and expected cell generation.
- [x] T007 Implement contamination/missing-cell preflight with stable issue codes.
- [x] T008 Implement deterministic arm summaries and report serialization without filtering failed runs or declaring a winner.

## Verification

- [x] T009 Test canonical arm/config/cell validation and deterministic digests.
- [x] T010 Test contamination detection for workspace/context reuse, baseline/config mismatch, scorer leakage, missing/duplicate cells.
- [x] T011 Test failure retention, metrics aggregation, and no-winner report semantics.
- [x] T012 Run exact full regression, changed-surface Ruff, baseline/full Ruff diagnostics, compile, install, entry-point parity, and line-length gates on byte-identical product/test blobs.
- [x] T013 Review exact diff for hidden exclusions, ranking claims, process/network execution, actor scoring, or dependency creep.

## PR closeout

- [x] T014 Open bounded PR #17 at exact documentation head `14e3d7e6a301148e0a25c2e98134fe8a6c573b54`.
- [x] T015 Resolve every material exact-head review defect; no material review threads remained, while CodeRabbit auto-review and Qodo review were unavailable as substantive reviewers.
- [x] T016 Merge with expected-head protection into canonical merge commit `001a70fcabff497c565fa7339381c4da0b4a3881`; second parent is exact reviewed PR head `14e3d7e6a301148e0a25c2e98134fe8a6c573b54`.
