# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `7f4682f88dd9988f12f2a466c071beb67d660a2d`  
**Closed specification:** `specs/003-refinement-tree/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/004-grain-readiness/`  
**Active branch:** `feat/004-grain-readiness`  
**Active status:** `IMPLEMENTATION_PLANNED`

## Current objective

Make Grain readiness a deterministic, versioned, explainable binary contract rather than an agent/human label.

## Readiness-v1 boundary

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

## Trust boundary

004 verifies deterministic authored readiness content. It does not prove repository reuse claims, compute context-source sizes, validate dependency DAGs, run evidence, apply method-specific policies, or mutate lifecycle state.

## Immediate ordering

1. Implement readiness models/report.
2. Implement forest/candidate and intrinsic gates.
3. Add exhaustive focused tests plus all regressions.
4. Review exact diff for scope creep.
5. Open and close a bounded expected-head PR.
