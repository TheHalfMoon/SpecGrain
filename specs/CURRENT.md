# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `2a719a8ed2a7c22c0f65402c95361b32b230b511`  
**Closed specification:** `specs/004-grain-readiness/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/005-cli-local-store/`  
**Active branch:** `feat/005-cli-local-store`  
**Active status:** `IMPLEMENTATION_PLANNED`

## Current objective

Ship the first repository-local SpecGrain product surface: dependency-free store v1 plus `init` and `check` with deterministic policy-aware readiness reporting.

## Store-v1 boundary

Canonical state:

```text
.specgrain/
  project.json
  specs/*.json
  policies/default.json
```

005 owns strict JSON/store parsing, safe path/symlink rules, initialization, project/policy loading, refinement validation, readiness report/enforce policy, and CLI rendering/exit codes.

ADR-0005 replaces the earlier provisional YAML preference for M2 with dependency-free JSON v1. YAML remains a possible later adapter, not a 005 dependency.

## Trust boundary

005 MUST remain read-only during `check` and MUST NOT:

- mutate lifecycle state;
- treat readiness reports as transition tokens;
- validate the dependency DAG;
- scan repository source;
- execute subprocesses/agents;
- create evidence-ledger semantics;
- add generic spec mutation APIs.

## Immediate ordering

1. Implement store models/errors and strict JSON/path validation.
2. Implement atomic `init_project` and deterministic `load_project`.
3. Implement policy-aware `check_project`.
4. Implement CLI/entry points without runtime dependencies.
5. Add store/CLI tests plus all kernel regressions.
6. Review exact diff and close a bounded expected-head PR.
