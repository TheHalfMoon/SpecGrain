# Review — Specification 022 Native Grain Preparation

**Reviewed product head:** `8af20015bd59424c7882b8c8fa7ea4c78e0af2e5`  
**Implementation PR:** #38  
**Canonical product merge:** `653cfb64c8885174ea3ea729d1bbb6418613b10d`

## Scope conclusion

The final product diff stays within the shaped Specification 022 authority:

```text
DRAFT -> SHAPED -> REFINING -> GRAIN
```

No `GRAIN -> READY`, WorkPacket execution, executor/provider invocation, verification execution, evidence mutation, generic mature-node editing, release/version mutation, hosted/account scope, or runtime dependency growth was introduced.

## Exact-head review checklist

- **Hidden readiness-sensitive defaults:** none found. Risk, recovery, context, evidence, minimality, and safety declarations are explicit.
- **Readiness weakening:** none found. Grain promotion uses the existing Grain-readiness evaluator on the exact `REFINING` candidate and complete forest.
- **Readiness moved to the wrong edge:** repaired before final head. `shape` validates only its explicit input contract; semantic Grain-readiness blockers remain at `grain`.
- **Lifecycle edge skipping:** none found.
- **Semantic mutation outside shaping:** none found. State-only transitions preserve the semantic revision digest.
- **Post-GRAIN authority:** none found.
- **Recovery widening:** none found. New operations refuse pending ADR-0018 authoring recovery and do not widen its transaction protocol.
- **Refinement/dependency bypass:** none found. Complete proposed project validation precedes shaping persistence.
- **Dependency creep:** none found. Runtime dependency count remains zero.
- **Historical release misstatement:** repaired documentation clearly separates current-source 022 commands from published `v0.3.0`.
- **Unrelated executor/provider/network scope:** none found.

## Review-system evidence

CodeRabbit produced a `COMMENTED` review against an earlier exact candidate. Two actionable inline threads were handled explicitly:

1. verification-gate wording was clarified in `docs/execution-master-plan.md`;
2. a proposal to enforce context bounds globally in `SpecNode` was declined because changing the SpecNode schema is explicitly outside Specification 022. CodeRabbit re-ran analysis against the scoped `shape_draft_spec` validation, agreed with the authority boundary, withdrew the finding, and resolved the thread.

All inline review threads were resolved before product merge.

Qodo reported that reviews were paused because billing was unavailable. That state was recorded as unavailable, not PASS. CodeRabbit's automatic final-head review was later skipped because the repository did not meet its automatic-review star threshold; that skip was also not treated as PASS. Cubic's generated summary was treated as descriptive metadata, not independent approval.

A CodeRabbit docstring-coverage warning was advisory rather than a configured repository or Specification 022 gate.

## Residual risk

A review walkthrough identified a bounded concurrent-writer race around exact-preimage validation and atomic replacement. The risk is real and remains unproven rather than being reclassified as safe. Specification 022 explicitly excludes multi-writer locking expansion and ADR-0018 recovery widening, so adding a broader locking protocol in this implementation would have exceeded authority.

The delivered recovery boundary is therefore intentionally limited to:

- exact-preimage comparison;
- pending ADR-0018 refusal;
- same-directory temporary write and `os.replace`;
- post-write project validation;
- fail-closed behavior when detected state differs from the expected preimage.

A stronger concurrency contract is separately shapeable only if future evidence justifies it.

## Verification conclusion

The final implementation head passed both exact-head push and PR permanent CI (`33261979828` and `33261982603`), including 575 tests in Ubuntu/Python 3.11 and all static, cleanliness, compile, CLI, build, wheel-install, and installed-smoke gates. Product merge used expected-head protection and canonical post-product CI `33262123902` succeeded across all five permanent cells.

The review conclusion is therefore: Specification 022's product implementation satisfies its bounded shaped authority, with the explicit multi-writer residual retained. Canonical closure still depends on the documentation-only closeout merge and its post-merge canonical verification.