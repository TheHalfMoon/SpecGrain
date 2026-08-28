# Specification 008 — Context Budget

**Status:** SHAPED  
**Type:** implementation  
**Created:** 2026-08-28  
**Depends on:** `007-repository-scan` (`CLOSED_CANONICAL`)

## Problem

SpecGrain can now describe a brownfield repository deterministically, but it still lacks a precise portable contract for the context a Grain requires. Without revision-bound source records and deterministic budget accounting, humans or agents can silently grow prompts, omit required context to fit a window, or depend on model-specific hidden token estimates.

## Outcome

Implement a dependency-free deterministic context-budget kernel. It records why each context source is selected, binds the record to explicit provenance/revision and cost inputs, guarantees required sources are never silently dropped, deterministically packs optional sources, and returns an explainable budget result that later WorkPackets can bind to.

008 does not retrieve source contents and does not invoke a tokenizer, model, embedding service, repository command, or execution adapter.

## Public model

### `ContextRequirement`

Canonical values:

- `required`;
- `optional`.

### `ContextSource`

Frozen/slotted source record:

- `source_id`: non-empty stable identifier;
- `provenance`: non-empty origin description/path/logical source;
- `selection_reason`: non-empty explanation for inclusion;
- `revision`: non-empty digest/repository/source revision identifier;
- `size_bytes`: non-negative integer, bool invalid;
- `token_cost`: non-negative integer accounting input, bool invalid;
- `requirement`: `ContextRequirement` or canonical string;
- `priority`: non-negative integer, bool invalid; lower values are considered first for optional packing.

The record is data only. `token_cost` does not mean SpecGrain executed a tokenizer; it is an explicit revision-bound accounting input.

Expose deterministic `to_dict()`.

### `ContextBudgetPolicy`

Frozen/slotted policy:

- `max_tokens`: positive integer, bool invalid;
- `max_bytes`: optional positive integer, bool invalid when present;
- `max_sources`: optional positive integer, bool invalid when present.

A missing optional ceiling means that dimension is not constrained by this policy.

Expose deterministic `to_dict()`.

### `ContextBudgetIssueCode`

Required blocking codes:

- `REQUIRED_TOKENS_EXCEEDED`;
- `REQUIRED_BYTES_EXCEEDED`;
- `REQUIRED_SOURCE_COUNT_EXCEEDED`.

### `ContextBudgetIssue`

Frozen/slotted issue:

- code;
- message.

### `ContextBudgetReport`

Frozen/slotted deterministic result containing at least:

- `fits`;
- canonical required source IDs;
- canonical selected source IDs;
- canonical omitted optional source IDs;
- required byte/token/source-count totals;
- selected byte/token/source-count totals;
- blocking issues;
- `plan_digest` over normalized policy, all source records, and the selected/omitted plan.

Expose deterministic `to_dict()`.

### Errors

`ContextValidationError` rejects structurally invalid source collections, including duplicate `source_id` values or non-`ContextSource` members.

`ContextBudgetError` carries the exact failing report returned by `evaluate_context_budget`.

## Deterministic budgeting

`evaluate_context_budget(sources, policy)` MUST be input-order invariant.

1. validate and canonicalize sources by `source_id`;
2. collect all required sources in canonical ID order;
3. if required sources alone exceed any configured ceiling, return a blocking report and select no optional sources;
4. otherwise consider optional sources by `(priority, source_id)`;
5. include an optional source only if the resulting selected set remains within every configured ceiling;
6. omit an optional source that does not fit and continue evaluating later optional sources;
7. never drop a required source to manufacture a passing result.

`fits` means all required context fits policy. Omitted optional context is recorded but is not itself a blocker.

`require_context_budget(sources, policy)` returns the passing report or raises `ContextBudgetError` with the exact failing report.

## Plan digest

`plan_digest` is `sha256:<hex>` over compact UTF-8 JSON with sorted keys and no non-finite values. The normalized digest input includes:

- policy;
- every canonical source record;
- required IDs;
- selected IDs;
- omitted optional IDs;
- required/selected cost totals;
- blocking issue codes/messages.

Input collection order must not affect the digest.

## Repository-map integration

Provide `repository_map_context_source(...)` that creates one `ContextSource` from a 007 `RepositoryMap` without reading repository file contents.

Required behavior:

- bind `revision` to `sha256:<RepositoryMap.content_digest>`;
- derive `size_bytes` from compact deterministic JSON of `RepositoryMap.to_dict()`;
- accept explicit `token_cost`, `selection_reason`, requirement, priority, and source ID;
- use provenance that identifies the normalized repository map rather than an absolute filesystem path;
- never call Git, open repository source files, execute commands, or invoke a tokenizer/LLM.

The helper treats Repository Scan facts as factual context evidence only; it does not infer semantic relevance or architecture intent.

## Trust and safety boundary

008 MUST NOT:

- read arbitrary source-file contents;
- execute repository/package/build/test/Git commands;
- follow filesystem links;
- perform embeddings, semantic search, or LLM relevance ranking;
- secretly estimate tokens from content or a model-specific tokenizer;
- mutate `.specgrain` storage or lifecycle state;
- alter dependency-wave scheduling;
- construct WorkPackets or evidence records;
- add a third-party runtime dependency.

## Acceptance criteria

1. all public records are frozen/slotted and validate their canonical fields.
2. duplicate source IDs and invalid collection members fail explicitly.
3. policy ceilings reject non-positive integers and bool values.
4. source cost fields reject negative/non-integer/bool values.
5. budget evaluation is invariant to input order.
6. required sources are always selected when the report fits.
7. required token overflow produces `REQUIRED_TOKENS_EXCEEDED` and a failing report.
8. configured required byte/source-count overflow produces the corresponding stable blocker code.
9. optional sources are packed deterministically by `(priority, source_id)` and omitted rather than causing failure.
10. a later smaller optional source may fit after an earlier optional source is omitted.
11. plan digest is stable for identical normalized inputs and changes when policy/source/selection facts change.
12. repository-map integration binds to the 007 map digest and normalized-map byte size without reading repository contents.
13. no lifecycle/store/scheduler/evidence state is mutated.
14. Specifications 001–007 regressions remain green.

## Success criterion

SpecGrain can produce and enforce one portable deterministic context plan whose required sources cannot be silently dropped, whose costs are explainable, and whose exact normalized state can be bound into Specification 009 WorkPackets.
