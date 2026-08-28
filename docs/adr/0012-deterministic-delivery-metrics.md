# ADR-0012 — Deterministic delivery diff, drift, and metrics

## Status

Accepted for Specification 012.

## Decision

SpecGrain will represent delivery-control signals as deterministic data contracts:

- authorized change-surface analysis uses normalized repository-relative literal paths/prefixes;
- drift is an exact revision mismatch signal and never guesses cause or severity;
- aggregate delivery metrics use integer counts and exact ratios rather than floating-point scores;
- metrics contain no actor identity and are not individual productivity scores.

Context efficiency requires an explicit `useful_context_tokens` measurement supplied by the measurement harness. The core does not infer usefulness from token count.

## Consequences

The kernel can reproduce and audit scope accuracy, revision drift, first-pass verification, rework, cycle time, context efficiency, and unscoped-change counts without telemetry services or probabilistic interpretation.
