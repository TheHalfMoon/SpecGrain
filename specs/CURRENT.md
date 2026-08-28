# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `197ddfb68d94bf8998d68d1371c26431f3816ca0`  
**Closed specification:** `specs/007-repository-scan/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/008-context-budget/`  
**Active branch:** `feat/008-context-budget`  
**Active status:** `SHAPED`

## Canonical continuation references

Read `docs/execution-master-plan.md` after the constitution. `docs/roadmap.md` remains the milestone-level sequencing reference. Live GitHub truth always overrides this state file if branches, PRs, checks, or canonical `main` move.

## Canonical 007 closeout evidence

Specification 007 closed through PR #9.

- final reviewed PR head: `35571d5cdcbe441b04a8e975c5eb6be0fe088698`;
- merge commit: `197ddfb68d94bf8998d68d1371c26431f3816ca0`;
- merge commit parent 1: prior canonical `main` `85d1bef8ee5c1c8e8d78baa52f509803a78a43d8`;
- merge commit parent 2: exact PR head `35571d5cdcbe441b04a8e975c5eb6be0fe088698`;
- PR #9 is closed and merged;
- no force-push, rebase, or destructive history rewriting was used.

The exact reviewed 007 product/test bytes passed 304 pytest tests, compileall, editable install, entry-point parity, and changed-line-length preflight. Ruff was NOT RUN because unavailable in the execution environment.

## Current objective — 008 Context Budget

Implement deterministic revision-bound context-source records and budget accounting without reading source content, selecting context through an LLM, mutating lifecycle/store state, or depending on a model-specific tokenizer.

008 owns:

- immutable context-source records with provenance, selection reason, revision, requirement class, byte size, token cost, and optional priority;
- deterministic validation and canonical serialization;
- required-context budget blockers;
- deterministic optional-context packing by `(priority, source_id)`;
- explicit token/byte/source-count policy limits;
- explainable budget reports and fail-closed `require_context_budget` behavior;
- repository-map integration that binds to the normalized 007 map digest without loading repository contents.

008 does not own:

- file-content retrieval or arbitrary repository indexing;
- semantic relevance scoring or LLM context selection;
- tokenizer execution or hidden token estimation;
- WorkPacket construction (`009`);
- evidence verification (`010`);
- lifecycle/store mutation;
- scheduler changes.

## Immediate ordering

1. Read `specs/008-context-budget/spec.md`, `plan.md`, `tasks.md`, and ADR-0008.
2. Implement the bounded context kernel in task order.
3. Verify all 001–008 tests plus compile/package/entry-point checks and available static checks.
4. Review the exact uploaded diff for content retrieval, hidden token estimation, lifecycle/store/scheduler mutation, evidence semantics, or dependency creep.
5. Open and close the bounded 008 PR using exact-head evidence.
6. Re-read canonical `main`, close 008 canonical task state, and immediately begin `009-work-packet`.
