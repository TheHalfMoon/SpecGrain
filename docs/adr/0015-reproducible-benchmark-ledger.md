# ADR-0015 — Reproducible Benchmark Ledger

## Status

Accepted for Specification 015.

## Decision

SpecGrainBench v1 will be a deterministic experiment ledger and validation/reporting harness. It will not invoke coding agents or fabricate comparative outcomes.

The harness owns exact case baselines, arm configurations, repetition cells, contamination preflight, run observations, and deterministic summaries. External benchmark runners may execute prompt-only, GitHub Spec Kit, and SpecGrain arms, but their observations must satisfy the ledger before any comparison is considered valid.

Failed and blocked runs remain in the dataset. A contamination failure invalidates the affected comparison rather than being averaged away. The deterministic report does not automatically declare a winning method.

## Consequences

- public benchmark claims can be tied to a portable machine-readable dataset;
- isolated workspace/context requirements become enforceable rather than prose-only;
- fair model/method/scorer configuration can be checked before aggregation;
- the repository can launch the benchmark harness without inventing agent-performance results that were not actually run.
