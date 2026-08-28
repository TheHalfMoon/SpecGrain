# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `7f4682f88dd9988f12f2a466c071beb67d660a2d`  
**Closed specification:** `specs/003-refinement-tree/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/004-grain-readiness/`  
**Active branch:** `feat/004-grain-readiness`  
**Active status:** `IMPLEMENTED_REVIEW_PENDING`

## Current objective

Close Grain readiness through exact-head review without allowing a readiness report to become a lifecycle mutation or external-fact proof.

## Implemented readiness-v1 boundary

A candidate must be a structurally valid REFINING leaf with:

- acceptance criteria;
- bounded `scope_in`;
- authorized `change_surface` or explicit exception;
- risk level + recovery declaration;
- context token estimate within declared budget;
- named required evidence;
- explicit empty unresolved-decision list;
- explicit minimality choice + rationale;
- explicit safety status + consistent requirements.

The readiness declaration lives in content-significant `metadata.readiness` and is versioned independently as readiness v1.

## Verification front

- pytest: **182 passed** (116 existing + 66 readiness tests);
- compileall: **PASS**;
- Ruff: **NOT RUN — unavailable locally**.

See `specs/004-grain-readiness/verification.md`.

## Trust boundary

004 verifies deterministic authored readiness content. It does not prove repository reuse claims, compute context-source sizes, validate dependency DAGs, run evidence, apply method-specific policies, or mutate lifecycle state.

## Immediate ordering

1. Review exact uploaded diff for scope/trust-boundary defects.
2. Open bounded PR with exact-head evidence.
3. Resolve all external/exact-head defects.
4. Merge only with expected-head guard.
5. Re-read canonical `main` and begin `005-cli-local-store`.
