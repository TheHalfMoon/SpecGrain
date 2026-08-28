# Plan 006 — Dependency Graph

## Strategy

Add one dependency-free `specgrain.dependency` module and a small read-only `next` CLI integration. Reuse existing `SpecNode.dependencies`, lifecycle states, and local store rather than creating a second graph model or persistence format.

## Planned source surface

```text
src/specgrain/dependency.py
src/specgrain/__init__.py
src/specgrain/store.py
src/specgrain/cli.py
tests/test_dependency.py
tests/test_store.py
tests/test_cli.py
```

No changes are planned for `model.py`, `lifecycle.py`, `refinement.py`, or `readiness.py`.

## Core data structures

Use standard-library only:

- `DependencyIssueCode(StrEnum)`;
- frozen/slotted `DependencyIssue`;
- `DependencyValidationError`;
- frozen/slotted `GrainDependencyReport`;
- pure functions over `Iterable[SpecNode]`.

Do not introduce a mutable graph object or NetworkX.

## Structural validation

Materialize once and validate member types.

### Duplicate IDs

Use ID counts. If any duplicate exists, return only deterministic `DUPLICATE_ID` issues. Identity ambiguity prevents safe reference/cycle analysis.

### Reference checks

For each canonical node ID and each dependency in sorted order:

- same ID => `SELF_DEPENDENCY`;
- missing ID => `MISSING_DEPENDENCY`.

### Cycle detection

Run deterministic iterative DFS over valid non-self dependency edges. Canonicalize each directed cycle by rotating to the smallest ID, then sort issues.

Dependency edge orientation is `node -> dependency`. Cycle diagnostics should render that authored orientation.

## State classification

Constants should be immutable and public only when useful:

```text
DEPENDENCY_SATISFIED_STATES = {VERIFIED, CONTROLLED}
DEPENDENCY_BLOCKER_STATES = {BLOCKED, FAILED, STALE, CANCELLED, SUPERSEDED}
```

All remaining lifecycle states are waiting for dependency purposes.

## Grain dependency report

For a valid graph and current `GRAIN` node:

1. collect direct dependencies not in satisfied states as `waiting_on`;
2. walk each unresolved dependency depth-first/breadth-first with a visited set;
3. stop at satisfied states;
4. add hard-blocker nodes to `blocked_by` and stop through that node;
5. traverse other waiting nodes to discover transitive blockers;
6. `eligible = not waiting_on`.

A candidate with a blocked dependency is necessarily not eligible because its direct dependency is unresolved; `blocked_by` explains why.

Reject requests for a missing ID or a node not currently in `GRAIN` with a stable `ValueError` subtype or documented validation error. Do not manufacture eligibility reports for non-Grain lifecycle states.

## Ready set

`ready_grains(nodes)`:

1. require structurally valid dependency graph;
2. inspect current GRAIN nodes in canonical ID order;
3. include only reports with `eligible=True`.

Do not evaluate 004 readiness again; GRAIN state represents a prior readiness transition boundary. 006 is dependency analysis, not historical readiness proof.

## Wave projection

Use a simple fixed-point/topological simulation:

1. `completed` starts as IDs currently `VERIFIED` or `CONTROLLED`;
2. `pending` is current GRAIN IDs;
3. wave = pending nodes whose every dependency is in `completed`;
4. append wave in canonical ID order and add its IDs to `completed`;
5. repeat until no wave exists.

Because structural cycles are rejected first, remaining unprojected GRAINs are blocked by current unresolved non-Grain/hard-blocker dependencies or depend on another unprojected Grain.

This algorithm naturally makes wave 1 equal `ready_grains`.

## Local-project integration

Extend `check_project` only after successful refinement validation:

- run dependency validation;
- map dependency issues to existing `ProjectCheckIssue`;
- return invalid result before readiness evaluation when dependency graph is malformed;
- otherwise preserve all 005 result fields/semantics.

Do not add dependency readiness to `ProjectCheckResult` yet unless a concrete CLI need requires it. Keep `check` compact.

## Next result

Add immutable `NextResult` in the store or dependency-facing local-product layer containing:

- `valid`;
- `project_id`;
- `eligible_ids`;
- `waves` as tuple-of-tuples IDs;
- issues.

Prefer store-layer orchestration function `next_project(root)` so CLI does no graph logic.

When store/refinement/dependency validation fails, return deterministic structured issues rather than raising through normal CLI flow.

## CLI

Add:

```text
specgrain next [PATH] [--json]
```

Text example:

```text
SpecGrain next: PASS
Project: demo
Eligible: 2
- SG-000003
- SG-000004
Projected waves: 2
Wave 1: SG-000003, SG-000004
Wave 2: SG-000005
```

If no eligible Grain:

```text
Eligible: 0
Projected waves: 0
```

and exit `0` when the project graphs are valid.

JSON is deterministic with IDs only, no absolute paths/timestamps.

## Verification plan

### Dependency module

Cover:

- empty/single-node graph;
- duplicate IDs fail closed;
- missing/self dependencies;
- two/three-node cycles;
- cycle/input-order determinism;
- all satisfied states;
- each waiting state;
- each blocker state;
- direct and transitive blocker propagation;
- blocker traversal stops at satisfied nodes;
- sorted `waiting_on`/`blocked_by`;
- non-Grain report refusal;
- ready set ordering;
- wave chains/parallelism;
- unresolved non-Grain wave exclusion;
- first-wave equality with ready set;
- no input/node mutation.

### Store/CLI

Cover:

- dependency-invalid local check;
- dependency validation occurs before readiness summary;
- valid dependency project preserves 005 check semantics;
- `next` with eligible, waiting, blocked, and empty projects;
- deterministic JSON/text;
- invalid project exit 1;
- empty eligible valid exit 0;
- read-only filesystem snapshot.

Run all 001–006 tests, compileall, editable-install/entry-point smoke, and available lint/static checks.

## Scope review

Before PR confirm no:

- state mutation/persistence transaction;
- repository scan;
- semantic dependency inference;
- conflict/file-overlap analysis;
- evidence storage;
- execution adapter;
- third-party graph/runtime dependency.

## Risk

The main risk is confusing “projectable wave” with guaranteed safe parallel execution. 006 waves are dependency-order projections only. File/conflict intelligence is not available yet and MUST NOT be implied by output or docs.
