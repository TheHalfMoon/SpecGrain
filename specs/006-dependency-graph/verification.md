# Verification 006 — Dependency Graph

**Verification date:** 2026-08-28  
**Environment:** Python `3.13.5`

## Implementation refinement

The planning document originally expected dependency-aware local orchestration to extend `store.py`. During implementation review, that change surface was reduced: Specification 005 persistence remains unchanged, and Specification 006 adds a small `project.py` orchestration layer that composes the existing store with refinement/dependency checks.

This preserves the 005 storage boundary while keeping 006 limited to dependency analysis and read-only project orchestration.

## Pytest

```text
python -m pytest -q
........................................................................ [ 26%]
........................................................................ [ 52%]
........................................................................ [ 78%]
...........................................................              [100%]
```

Result: **275 passed**.

This is the 236-test Specification 001–005 baseline plus 39 new Specification 006 tests.

The new tests cover:

- empty/single-node dependency graphs;
- non-SpecNode input rejection;
- duplicate identity fail-closed behavior;
- missing and self dependencies;
- deterministic two/three-node cycle detection independent of input order;
- exact aggregate dependency validation errors;
- satisfied, waiting, and hard-blocker lifecycle classifications;
- direct waiting and direct/transitive hard blockers;
- traversal stopping at VERIFIED/CONTROLLED nodes;
- sorted waiting/blocker reports;
- missing/non-GRAIN report refusal;
- deterministic ready-set ordering;
- dependency-only wave projection and first-wave equality with the ready set;
- exclusion of unresolved non-GRAIN and hard-blocked chains;
- independent Grain projection while another chain is stuck;
- no node/input mutation;
- local `check` dependency validation before readiness reporting;
- read-only `next` orchestration, deterministic waves, and transitive blocker output;
- `next` text/JSON/exit-code and fail-closed internal-error behavior.

## Compile check

```text
python -m compileall -q src tests
```

Result: **PASS**.

## Packaging / entry-point checks

```text
python -m pip install -e . --no-build-isolation -q
diff -u <(specgrain --help) <(python -m specgrain --help)
```

Result: **PASS**.

Both entry points expose the same command surface including `next`.

## Style preflight

The exact changed source/tests were checked for lines longer than 100 characters.

Result: **0 long lines**.

## Ruff

`ruff` remains unavailable in the execution environment and cannot be installed because outbound package-index access is unavailable. Ruff is therefore **NOT RUN**, not PASS.

## Scope verification

The final implementation changes only:

- new deterministic dependency kernel;
- new dependency-aware local project orchestration;
- CLI `next` integration;
- bounded public exports;
- focused dependency/project tests.

Specification 005 `store.py` is intentionally unchanged. The implementation adds no lifecycle mutation, repository scanning, dependency inference, file-conflict analysis, evidence storage, execution adapter, or third-party graph/runtime dependency.
