# Plan 003 — Refinement Tree

## Strategy

Use small pure functions in a new `specgrain.refinement` module. Do not introduce a `SpecForest` object or graph-library dependency for behavior that can be implemented clearly with dictionaries, sets, and deterministic traversal.

## Planned files

```text
src/specgrain/refinement.py
src/specgrain/__init__.py
tests/test_refinement.py
specs/003-refinement-tree/*
```

`model.py` and `lifecycle.py` should not need behavioral changes for 003.

## Validation phases

### Phase 1 — Materialize and type-check

Materialize the iterable exactly once. Reject non-`SpecNode` elements explicitly.

### Phase 2 — Identity

Group nodes by ID. If any ID appears more than once, return only deterministic `DUPLICATE_ID` issues. Relationship resolution stops because an ID no longer identifies one canonical node.

### Phase 3 — Local references

With unique IDs, inspect each node in canonical ID order for:

- self parent;
- missing parent;
- self child;
- missing child.

### Phase 4 — Reciprocity

Where both endpoints exist and are not self-links:

- child parent pointer missing from parent's children -> `PARENT_CHILD_MISMATCH` on the child;
- parent's child declaration disagrees with child's parent pointer -> `CHILD_PARENT_MISMATCH` on the parent/child pair.

Avoid emitting misleading reciprocal issues for unresolved missing references.

### Phase 5 — Cycles

Build refinement adjacency from existing parent-child declarations after unique identity is established. Cycle detection should be iterative or recursively bounded only by Python limitations; deterministic DFS in canonical child-ID order is acceptable for the initial kernel.

Canonicalize a detected cycle by rotating its node-ID ring so the lexicographically smallest ID is first, choosing the encountered directed orientation. Deduplicate the same cycle if discovered from another starting node.

### Phase 6 — Deterministic result

Sort structured issues by:

```text
(code.value, node_id, related_id or "", message)
```

Root listing calls validation first, then returns `parent_id is None` nodes sorted by ID.

## Public types

Use:

- `RefinementIssueCode(StrEnum)`;
- `@dataclass(frozen=True, slots=True) RefinementIssue`;
- `RefinementValidationError(ValueError)` carrying `issues: tuple[RefinementIssue, ...]`.

These are justified because downstream CLI/readiness must consume structured failures rather than parse prose.

## Verification

Tests should independently declare malformed fixtures for:

- empty forest;
- one root;
- multiple roots;
- deep valid tree;
- duplicate identity;
- missing parent;
- missing child;
- self parent;
- self child;
- child points to parent but parent omits child;
- parent names child whose parent is another node or none;
- 2-node and 3-node cycles;
- input-order invariance;
- aggregate error carries structured issues;
- invalid root query fails closed.

Run all existing tests plus new tests. Record Ruff as NOT RUN if unavailable rather than claiming PASS.

## Donor discipline

The implementation follows the newly canonical planning synthesis:

- simplest sufficient stdlib structure;
- no new dependency;
- no semantic/AI features beyond the requested structural outcome;
- every source change must trace to 003;
- tests define success rather than a procedural agent prompt.
