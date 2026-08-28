# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `619b7501fc659588fc344af8835cc910a42bff31`  
**Closed specification:** `specs/001-specnode-schema/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/002-lifecycle-state/`  
**Active branch:** `feat/002-lifecycle-state`  
**Active status:** `IMPLEMENTATION_PLANNED`

## Current objective

Define and implement canonical lifecycle state names plus deterministic structural transition validation without creating a bypass around readiness, scheduling, execution, or verification authorization.

## Explicit scope boundary

`002-lifecycle-state` MUST NOT implement:

- Grain readiness evidence or promotion authority;
- dependency/repository readiness authorization;
- execution orchestration;
- verification/evidence authorization;
- recursive tree integrity;
- dependency DAG algorithms;
- CLI or store IO;
- transition history persistence;
- automatic resume to a pre-exception state.

## Immediate ordering

1. Define the complete state set and legal adjacency graph.
2. Define terminal and exceptional-state recovery semantics.
3. Implement state parsing/normalization and explainable transition validation.
4. Make `SpecNode` reject unknown lifecycle state strings while preserving known-state digest behavior.
5. Verify the full transition matrix and all Specification 001 regression tests.
6. Open and review a bounded exact-head PR.

## Trust boundary

Lifecycle legality is not lifecycle authorization. Specification 002 does not expose a general-purpose node state mutator. Later gate-owning specifications may apply a legal transition only after their own evidence/preconditions pass. See `docs/adr/0004-transition-legality-vs-authorization.md`.
