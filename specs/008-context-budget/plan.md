# Plan 008 — Context Budget

## Strategy

Add one dependency-free `specgrain.context` kernel that treats context as revision-bound accounting data rather than prompt text. Keep source retrieval, semantic relevance selection, tokenization, WorkPacket construction, lifecycle mutation, and execution outside 008.

## Planned source surface

```text
src/specgrain/context.py
src/specgrain/__init__.py
tests/test_context.py
```

No changes are planned for repository traversal, schema, lifecycle, refinement, readiness, dependency, persistence, project orchestration, or CLI behavior.

## Source records

Use frozen/slotted `ContextSource` records with explicit provenance, selection reason, revision, byte size, token cost, requirement class, and optional-selection priority.

Costs are explicit inputs. The core does not infer token counts from source content and does not bind itself to a model tokenizer.

## Policy

`ContextBudgetPolicy` requires a positive token ceiling and may also constrain bytes and source count. All integer validation rejects bool.

## Evaluation

Canonicalize by source ID so results do not depend on caller collection order.

Required sources are immutable budget obligations. If required sources alone exceed any configured ceiling, emit stable blocker issues and do not select optional sources.

When required sources fit, consider optional sources in `(priority, source_id)` order. Include each source only when all configured ceilings remain satisfied. An omitted optional source does not prevent a later smaller source from fitting.

Return a frozen/slotted report with required/selected/omitted IDs, cost totals, issues, and a deterministic plan digest. `require_context_budget` raises with the exact failed report rather than mutating any project state.

## Repository-map bridge

Add a narrow `repository_map_context_source` helper. It consumes an already-built `RepositoryMap`, serializes only its normalized `to_dict()` form to compute byte size, binds revision to the map digest, and accepts an explicit token cost. It must not scan again or open repository source files.

## Verification

Cover:

- model/policy validation and bool rejection;
- duplicate/non-source collection failures;
- permutation-invariant evaluation;
- required token/byte/count blockers;
- optional priority/tie ordering;
- skip-large-then-fit-smaller optional behavior;
- exact passing/error report preservation;
- plan digest stability/change sensitivity;
- repository-map bridge provenance/revision/size behavior;
- no source-file reads, subprocess, lifecycle/store/scheduler mutation, or third-party runtime dependency.

Run all 001–008 tests, compileall, editable install, console/module help parity, changed-line length preflight, and available lint/static checks.

## Scope review

Confirm the exact uploaded diff adds no file-content retrieval, tokenization, LLM/embedding selection, WorkPacket/evidence semantics, lifecycle/store writes, dependency scheduling, subprocess execution, or runtime dependency.
