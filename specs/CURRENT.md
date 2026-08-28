# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `ccd4a825c2a951a8000a2833ede05cdb3218d477`  
**Closed specification:** `specs/005-cli-local-store/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/006-dependency-graph/`  
**Active branch:** `feat/006-dependency-graph`  
**Active status:** `IMPLEMENTATION_PLANNED`

## Current objective

Make `SpecNode.dependencies` an enforceable deterministic DAG contract and expose the first read-only eligibility surface through `specgrain next`.

## Dependency semantics

ADR-0006 defines:

- satisfied: `VERIFIED`, `CONTROLLED`;
- hard blockers: `BLOCKED`, `FAILED`, `STALE`, `CANCELLED`, `SUPERSEDED`;
- all other lifecycle states: waiting.

Only current `GRAIN` nodes are candidates for the ready set. Eligibility analysis never mutates `GRAIN -> READY`.

## 006 boundary

006 owns:

- duplicate/missing/self dependency validation;
- deterministic dependency cycle detection;
- direct waiting + transitive hard-blocker reporting;
- current eligible Grain computation;
- advisory dependency-only Grain wave projection;
- dependency validation integration into local `check`;
- read-only `next` text/JSON output.

It does not infer dependencies, scan repository source, analyze file conflicts, execute work, store evidence, or mutate lifecycle state.

## Immediate ordering

1. Implement dependency structural validation and deterministic cycles.
2. Implement current Grain dependency reports, blocker propagation, ready set, and waves.
3. Integrate dependency validation into local `check`.
4. Add `next_project` and `specgrain next` as read-only surfaces.
5. Run all regressions and exact-scope review.
6. Close a bounded expected-head PR before beginning 007.
