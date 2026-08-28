# Review 004 — Grain Readiness

**Review date:** 2026-08-28  
**Initial exact PR head:** `f8e4e3a2e32647cc324b1c059b2c9d0c173db561`

## Review objective

Verify that Specification 004 creates a deterministic readiness evaluation without granting lifecycle mutation authority, overstating authored declarations as external proof, or pulling later repository/dependency/evidence behavior into the readiness kernel.

## Finding F-001 — Passing report wording could be read as reusable transition authority

**Severity:** material contract ambiguity  
**Status:** remediated

Specification 001 intentionally excludes lifecycle `state` from the semantic `revision_digest`. The initial 004 wording said that a passing report plus lifecycle legality authorizes `REFINING -> GRAIN`. Because the report contains the semantic digest but does not control repository concurrency or state freshness, that wording could encourage a future caller to reuse a historical passing report after state changed.

The runtime implementation did not mutate state and did not itself expose a transition function, so this was a contract/documentation defect rather than an implementation bypass.

## Resolution

004 now states explicitly:

- a `GrainReadinessReport` is an evaluation result, not a durable authorization token, lease, lock, or compare-and-swap capability;
- semantic `revision_digest` proves semantic-content identity, not lifecycle-state freshness;
- a future state-mutating subsystem must re-read the current candidate/current forest, re-evaluate readiness, and verify current state is still `REFINING` immediately before the write under its own concurrency/precondition rules;
- an old passing report alone is insufficient authority for mutation.

A proposed `source_state` report field was deliberately rejected: recording the observed state would not prevent stale report reuse and would add API surface without solving the concurrency problem.

## Scope result

No product source change was required for F-001. The exact runtime behavior remains the implementation verified by the 182-test run. No repository scan, dependency DAG, method profile, evidence execution, state persistence/mutation, or CLI/store behavior is added by the remediation.

A fresh exact-head external/repository review is required before merge.
