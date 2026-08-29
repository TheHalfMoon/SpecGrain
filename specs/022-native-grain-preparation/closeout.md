# Closeout Candidate — Specification 022 Native Grain Preparation

**Closeout state:** `PENDING_CANONICAL_CLOSEOUT`  
**Canonical shaping merge:** `4919a4261f649e81cb1f507c0e80bc5c98d848d8`  
**Final implementation head:** `8af20015bd59424c7882b8c8fa7ea4c78e0af2e5`  
**Implementation PR:** #38  
**Canonical product merge:** `653cfb64c8885174ea3ea729d1bbb6418613b10d`  
**Canonical post-product CI:** `33262123902` — `completed/success`  
**Published release preserved:** `v0.3.0` / Release `378962445`

This document is the documentation-only closeout candidate for Specification 022. It does not claim `CLOSED_CANONICAL` until this closeout is merged with expected-head protection and the resulting canonical `main` passes the permanent five-cell CI with the historical `v0.3.0` release still unchanged.

## Outcome delivered

Specification 022 closes the native pre-execution dead end with exactly:

```text
DRAFT -> SHAPED -> REFINING -> GRAIN
```

Current source now provides bounded `shape`, `refine`, and `grain` API/CLI surfaces using existing schema, lifecycle, refinement, dependency, readiness, and local-store safety semantics.

The implementation does not authorize `GRAIN -> READY`, WorkPacket execution, executor/provider/agent orchestration, verification execution, evidence mutation, generic mature-SpecNode editing, release/version changes, hosted/account scope, runtime dependency growth, or readiness weakening.

## Shaping authority

Documentation-only shaping PR #37 merged with expected-head protection as `4919a4261f649e81cb1f507c0e80bc5c98d848d8`. Canonical post-shaping CI `33260132438` completed successfully across the permanent Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11 matrix before implementation began.

ADR-0019 remained the exact mutation authority. The implementation used `src/specgrain/pregrain.py` as a bounded module while reusing existing store safety primitives; this was an implementation-detail refinement, not an authority expansion.

## Exact implementation evidence

The initial product checkpoint `05865fdfeb89e259be237f5e020a87424384d122` passed permanent CI `33260707422` with 573 tests in Ubuntu/Python 3.11 and every permanent matrix cell green.

The documentation-reconciled checkpoint `4bee0d729ded1ae3ca826ff20d79c11eee50d740` passed permanent CI `33261247016` with 574 tests.

Exact review then found that the first implementation applied full Grain readiness during `shape`, which exceeded the shaped lifecycle contract. The defect was repaired forward without history rewriting:

- `bfb87942af2904468dcfed48a1822084b0fcfcd9` moved Grain readiness back to `REFINING -> GRAIN`;
- `946323e9d1b0f946010af36364f56de0c139e3f3` retained explicit shape-input validation for `context_budget > 0` and `context_estimate >= 0` while leaving `estimate > budget` as a Grain-readiness blocker;
- `8af20015bd59424c7882b8c8fa7ea4c78e0af2e5` clarified the verification-gate wording after review.

The final implementation candidate `8af20015bd59424c7882b8c8fa7ea4c78e0af2e5` passed:

- push CI `33261979828` — `completed/success` across all five permanent cells;
- PR CI `33261982603` — `completed/success` across all five permanent cells;
- Ubuntu/Python 3.11 full regression — `575 passed`;
- Ruff over `src`, `tests`, and `examples`;
- editable installation with `--no-deps`;
- tracked-tree cleanliness;
- compileall;
- source CLI smoke;
- package build;
- built-wheel reinstall with `--no-deps`;
- installed CLI smoke.

The final shaped-base-to-head product diff contained 15 expected Specification 022 product/documentation/test paths and no runtime dependency, package-version, release-workflow, provider/executor, post-GRAIN, or unrelated scope.

## Review disposition

PR #38 review state was rechecked before merge.

- CodeRabbit submitted a `COMMENTED` review on an earlier candidate and produced two actionable inline threads.
- The documentation wording finding was fixed.
- The suggestion to move context bounds into global `SpecNode` validation was rejected because Specification 022 explicitly excludes changing the SpecNode schema; CodeRabbit rechecked the scoped validation and withdrew the finding.
- All inline review threads were resolved before merge.
- Qodo was unavailable because review billing was paused and was not treated as PASS.
- CodeRabbit automatic final-head review was skipped by its repository-star policy and was not treated as PASS.
- Cubic supplied a PR summary but was not treated as an independent approval.
- CodeRabbit's docstring-coverage warning was advisory and was not a repository or Specification 022 verification gate.

### Residual multi-writer risk

CodeRabbit also recorded a bounded race risk for concurrent local writers between exact-preimage validation and atomic replacement. This is preserved explicitly as a residual risk rather than silently widened: Specification 022 excludes multi-writer locking expansion and ADR-0018 recovery widening. The delivered authority remains exact-preimage single-file replacement, pending-authoring refusal, same-directory atomic replacement, and post-write validation. Stronger multi-writer coordination requires separately shaped authority from fresh evidence.

No claim of proven concurrent-writer safety is made by Specification 022.

## Product merge proof

PR #38 merged only after the final exact-head checks and review dispositions were established. GitHub accepted the merge with expected head:

`8af20015bd59424c7882b8c8fa7ea4c78e0af2e5`

and produced canonical product merge:

`653cfb64c8885174ea3ea729d1bbb6418613b10d`

The GitHub-signature-verified merge has exact parents:

1. shaped canonical base `4919a4261f649e81cb1f507c0e80bc5c98d848d8`;
2. final implementation head `8af20015bd59424c7882b8c8fa7ea4c78e0af2e5`.

Canonical post-product CI `33262123902` completed `success` across all five permanent cells:

- Ubuntu / Python 3.11 — job `99125746481`;
- Ubuntu / Python 3.12 — job `99125746533`;
- Ubuntu / Python 3.13 — job `99125746518`;
- macOS / Python 3.11 — job `99125746522`;
- Windows / Python 3.11 — job `99125746487`.

## Historical v0.3.0 preservation

After the product merge, live GitHub truth remained unchanged:

- tag `v0.3.0` -> `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release ID `378962445`;
- wheel asset ID `535129008`, size `70463`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset ID `535129009`, size `104057`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

The historical release notes still enumerate only `init`, `draft`, `recover`, `check`, `next`, `scan`, `prove`, and `import-spec-kit`. They do not claim `shape`, `refine`, or `grain` as v0.3.0 behavior.

## Next-frontier reevaluation

The post-022 product truth removes the specific DRAFT-to-GRAIN dead end that selected Specification 022. No fresh canonical evidence in this closeout proves that READY mutation, WorkPacket CLI/execution, executor/provider orchestration, verification execution, evidence mutation, stronger multi-writer locking, or a new release is the next bounded product need.

The program therefore returns to an observation/evidence-gathering frontier after 022 closes. A planned external architectural review and comparison against GitHub Spec Kit may supply future evidence, but that review is not itself product authority. Any successor specification must be shaped from the resulting concrete findings and canonical repository truth.

## Canonical closeout gate

This closeout candidate may become the canonical Specification 022 closeout only when:

1. its exact documentation-only head passes permanent five-cell CI;
2. exact diff/review/mergeability and review-bot availability are rechecked;
3. the closeout PR is merged with expected-head protection;
4. canonical post-closeout `main` passes permanent five-cell CI;
5. `v0.3.0` tag/release/assets remain unchanged;
6. the implementation and closeout PRs are confirmed merged/closed.

Only after those conditions exist may Specification 022 be described as `CLOSED_CANONICAL`.