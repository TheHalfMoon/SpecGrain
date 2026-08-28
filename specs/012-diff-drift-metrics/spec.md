# Specification 012 — Diff, Drift, and Metrics

## Outcome

Make surgical-change compliance and core delivery-quality signals deterministic and reproducible.

## Required behavior

1. Partition observed repository-relative changed paths into authorized and unscoped sets using the same literal path/prefix model as verification.
2. Reject ambiguous, absolute, parent-traversal, backslash, duplicate, or empty path inputs.
3. Detect exact SpecNode, repository, and optional context-plan revision drift without assigning guessed cause or severity.
4. Aggregate these process measurements without actor identity:
   - first-pass verification rate;
   - rework ratio;
   - mean Grain cycle time;
   - context efficiency from explicitly measured useful/selected tokens;
   - change-scope accuracy;
   - spec drift rate;
   - unscoped path count.
5. Use exact integer ratios, stable serialization, and deterministic digests.
6. Preserve existing verification, lifecycle, store, method, CLI, and dependency semantics.

## Non-goals

- filesystem/Git diff discovery;
- background telemetry;
- employee/developer scoring;
- probabilistic relevance inference;
- dashboards;
- automatic remediation;
- changing 010 verification authority.

## Acceptance

- path partitioning and drift detection are permutation-stable and fail closed on malformed inputs;
- aggregate metrics are reproducible under observation reordering;
- zero-denominator context/scope metrics are explicit `null`, not invented percentages;
- the full 001–012 regression passes on exact uploaded bytes.
