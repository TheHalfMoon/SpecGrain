# ADR-0008: Context Costs Are Explicit Revision-Bound Inputs

**Status:** Accepted  
**Date:** 2026-08-28

## Context

Specification 008 must make context a finite deterministic engineering resource without making a model vendor, tokenizer, embedding service, or LLM selector part of the SpecGrain core. Repository Scan 007 provides compact deterministic repository facts, but it intentionally does not select file contents or estimate semantic relevance.

A context budget needs two distinct concerns:

1. source provenance/revision and why a source is selected;
2. deterministic accounting over explicit cost inputs.

Silently estimating model tokens from arbitrary bytes inside the core would create hidden model assumptions. Silently dropping required context to make a budget pass would weaken Grain safety.

## Decision

Context Budget v1 uses immutable `ContextSource` records. Each source explicitly carries:

- stable `source_id`;
- provenance;
- selection reason;
- revision/digest identifier;
- `size_bytes`;
- `token_cost`;
- requirement class: `required` or `optional`;
- non-negative optional-selection priority.

`token_cost` is an accounting input, not a claim that SpecGrain tokenized the source. A caller or future adapter may measure it with an appropriate tokenizer, but the deterministic core only validates and sums the supplied revision-bound value.

`ContextBudgetPolicy` has a mandatory positive token ceiling and optional positive byte/source-count ceilings. Bool is invalid where integers are required.

Required sources are never omitted. If required sources alone exceed any configured ceiling, the report is blocking. Optional sources are considered deterministically by `(priority, source_id)` and are included only when the resulting selected set stays within every configured ceiling. An optional source that does not fit is omitted; later optional sources may still fit.

The report is deterministic, explains required-budget blockers, records selected and omitted source IDs, totals byte/token costs, and carries a SHA-256 digest over the normalized policy/source/selection plan.

Repository-map integration creates a context source from the normalized `RepositoryMap` only. It binds `revision` to the map content digest and derives byte size from canonical normalized map JSON. It never reads repository file contents or invokes a tokenizer/LLM.

## Consequences

- The core remains model/tokenizer neutral.
- Required context cannot be hidden to manufacture a passing budget.
- Optional packing is reproducible and input-order invariant.
- Token-cost measurement provenance can be strengthened by later adapters without changing the accounting kernel.
- WorkPacket 009 can bind to a deterministic passing context plan instead of giant prompt text.
- Context Budget 008 does not mutate lifecycle/store state; callers use the blocking report or `require_context_budget` at the appropriate authorization boundary.
