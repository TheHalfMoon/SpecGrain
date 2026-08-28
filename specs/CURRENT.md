# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `2a719a8ed2a7c22c0f65402c95361b32b230b511`  
**Closed specification:** `specs/004-grain-readiness/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/005-cli-local-store/`  
**Active branch:** `feat/005-cli-local-store`  
**Active status:** `HARDENED_REVIEW_PENDING`

## Current objective

Close the first repository-local SpecGrain product surface through exact-head review: dependency-free store v1 plus `init` and read-only `check` with deterministic policy-aware readiness reporting.

## Implemented store-v1 boundary

Canonical state:

```text
.specgrain/
  project.json
  specs/*.json
  policies/default.json
```

005 owns strict JSON/store parsing, safe path/symlink rules, atomic initialization, project/policy loading, refinement validation, readiness report/enforce policy, and CLI rendering/exit codes.

ADR-0005 replaces the earlier provisional YAML preference for M2 with dependency-free JSON v1. YAML remains a possible later adapter, not a 005 dependency.

## Verification front

- pytest: **236 passed** (182 existing + 54 005 tests);
- compileall: **PASS**;
- editable install: **PASS**;
- `specgrain` and `python -m specgrain` entry points: **PASS**;
- fresh `init -> check -> JSON` smoke: **PASS**;
- console/module JSON equivalence: **PASS**;
- line-length preflight for new/changed source/tests: **0 lines over 100**;
- Ruff: **NOT RUN — unavailable locally; installation attempt blocked by offline DNS/network**.

The final hardening adds direct coverage for canonical symlink boundaries and unexpected CLI internal errors. See `specs/005-cli-local-store/verification.md`.

## Trust boundary

005 remains read-only during `check` and does not:

- mutate lifecycle state;
- treat readiness reports as transition tokens;
- validate the dependency DAG;
- scan repository source;
- execute subprocesses/agents;
- create evidence-ledger semantics;
- add generic spec mutation APIs.

## Immediate ordering

1. Commit the hardening changes on the active branch.
2. Review the exact uploaded diff for scope/trust-boundary defects.
3. Open a bounded PR with exact-head evidence.
4. Resolve every exact-head external/repository defect.
5. Merge only with expected-head guard.
6. Re-read canonical `main` and begin `006-dependency-graph`.
