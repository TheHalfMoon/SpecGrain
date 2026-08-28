# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `7f4682f88dd9988f12f2a466c071beb67d660a2d`  
**Closed specification:** `specs/003-refinement-tree/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/004-grain-readiness/`  
**Active branch:** `feat/004-grain-readiness`  
**Active status:** `CONTRACT_REMEDIATED_PR_REVIEW_PENDING`

## Current objective

Close Grain readiness through fresh exact-head review after clarifying that readiness evaluation is not reusable lifecycle authority.

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

The F-001 remediation after this test run changes documentation/contracts only; product source and tests are unchanged. See `specs/004-grain-readiness/verification.md` and `review.md`.

## Trust boundary

004 verifies deterministic authored readiness content for supplied inputs. A report is not a durable transition token. Any future lifecycle mutator must re-read current candidate/current forest, re-evaluate readiness, and verify current state remains `REFINING` immediately before the write under its own concurrency/precondition rules.

004 does not prove repository reuse claims, compute context-source sizes, validate dependency DAGs, run evidence, apply method-specific policies, or persist/mutate lifecycle state.

## Immediate ordering

1. Commit the F-001 contract remediation to PR #6.
2. Re-run exact-head external/repository checks.
3. Resolve every remaining material defect.
4. Merge only with expected-head guard.
5. Re-read canonical `main` and begin `005-cli-local-store`.
