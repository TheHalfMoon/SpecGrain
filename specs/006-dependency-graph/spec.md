# Specification 006 — Dependency Graph

**Status:** SHAPED  
**Type:** implementation  
**Created:** 2026-08-28  
**Depends on:** `005-cli-local-store` (`CLOSED_CANONICAL`)

## Problem

SpecGrain now stores recursive specs and can determine whether REFINING leaves satisfy Grain readiness, but `SpecNode.dependencies` remains only data. The system cannot reject malformed dependency references, distinguish waiting from blocked dependency chains, identify currently eligible Grains, or project deterministic parallel waves.

Without an explicit dependency contract, an agent or user could treat a Grain as executable while an upstream requirement is unresolved, failed, cancelled, stale, or structurally cyclic.

## Outcome

Implement a dependency-free deterministic dependency-graph layer plus a read-only `specgrain next` command. The layer validates dependency references/cycles, reports waiting and transitive hard blockers, computes the current eligible Grain set, and provides advisory Grain wave projection.

Specification 006 does not mutate lifecycle state.

## Dependency state semantics

ADR-0006 is canonical for state interpretation.

### Satisfied dependency states

- `VERIFIED`
- `CONTROLLED`

### Hard-blocker dependency states

- `BLOCKED`
- `FAILED`
- `STALE`
- `CANCELLED`
- `SUPERSEDED`

### Waiting dependency states

- `DRAFT`
- `SHAPED`
- `REFINING`
- `GRAIN`
- `READY`
- `RUNNING`
- `VERIFYING`

Only current `GRAIN` nodes are candidates for eligibility.

## Structural dependency invariants

For a collection of SpecNodes:

1. IDs MUST be unique; duplicate IDs are an identity blocker and stop deeper analysis.
2. every dependency ID MUST resolve to exactly one node in the collection;
3. a node MUST NOT depend on itself;
4. the dependency graph MUST be acyclic;
5. diagnostic ordering MUST be deterministic and independent of input order.

Refinement-tree validity is a separate Specification 003 concern. Local project `check` must require both refinement and dependency structural validity before readiness/eligibility summaries can be trusted.

## Public API

### `DependencyIssueCode`

Stable codes:

- `DUPLICATE_ID`
- `MISSING_DEPENDENCY`
- `SELF_DEPENDENCY`
- `CYCLE`

### `DependencyIssue`

Frozen/slotted issue with:

- `code`;
- `node_id`;
- `dependency_id` when applicable;
- deterministic `message`.

### `DependencyValidationError`

Aggregate error carrying the exact ordered issue tuple.

### `GrainDependencyReport`

Frozen/slotted report for one current Grain candidate:

- `node_id`;
- `eligible`;
- `waiting_on`: sorted direct unresolved dependency IDs;
- `blocked_by`: sorted reachable hard-blocker IDs.

A report is current-state analysis, not transition authority.

### `validate_dependencies(nodes)`

Returns ordered structural dependency issues and never mutates input.

### `require_valid_dependencies(nodes)`

Raises `DependencyValidationError` on any structural issue.

### `grain_dependency_report(node_id, nodes)`

Requires a structurally valid graph and an existing node currently in `GRAIN`. It computes current dependency eligibility.

### `ready_grains(nodes)`

Returns SpecNodes currently in `GRAIN` whose direct dependencies are all `VERIFIED`/`CONTROLLED`, sorted by canonical ID. A structurally invalid graph fails closed.

### `dependency_waves(nodes)`

Returns deterministic tuples of currently `GRAIN` nodes that can be projected as parallel waves by simulating completion of prior projected Grain waves.

A Grain is excluded from projection when any unresolved dependency is:

- a hard blocker;
- a non-Grain waiting state that cannot be simulated by 006; or
- another unprojectable Grain.

The first projected wave MUST equal `ready_grains(nodes)`.

## Blocker propagation

For a Grain candidate, traverse unresolved dependency chains only:

- stop traversal at `VERIFIED`/`CONTROLLED` nodes;
- record a node in a hard-blocker state in `blocked_by` and do not traverse beyond it;
- continue through waiting states to discover transitive hard blockers.

`waiting_on` contains only the candidate's direct unresolved dependency IDs. `blocked_by` may contain transitive blockers.

This distinction allows a user to see both the immediate prerequisite and the known root blocker.

## Local-project integration

Specification 006 extends `check_project` after refinement validation:

1. validate the dependency graph;
2. if dependency issues exist, return invalid `ProjectCheckResult` and skip readiness summaries;
3. otherwise preserve Specification 005 readiness report/enforce behavior.

Dependency issue paths use `.specgrain/specs/<node-id>.json`.

No dependency policy mode is introduced in 006: malformed dependency graphs are always invalid.

## `specgrain next`

CLI surface:

```text
specgrain next [PATH] [--json]
```

Behavior:

1. load local project;
2. require valid refinement and dependency graphs;
3. compute `ready_grains` and `dependency_waves`;
4. render current eligible Grain IDs plus concise dependency summaries;
5. never mutate canonical files or lifecycle state.

Text output is compact. JSON output is deterministic, contains no timestamps/absolute paths, and includes:

- `valid`;
- `project_id`;
- `eligible` IDs;
- `waves` as arrays of IDs;
- structural issues when invalid.

Exit codes:

- `0`: project graphs valid, including when eligible set is empty;
- `1`: store/refinement/dependency structural failure;
- `2`: argparse usage error.

An empty eligible set is a valid current state, not a CLI failure.

## Explicit non-goals

006 does NOT:

- mutate `GRAIN -> READY`;
- infer or rewrite dependencies;
- prove that declared dependencies are semantically complete;
- scan repository source;
- perform conflict analysis between parallel Grains;
- execute work;
- create evidence records;
- treat `READY/RUNNING/VERIFYING` as completed dependencies;
- automatically replace `SUPERSEDED` dependencies;
- add NetworkX or another graph runtime dependency.

## Acceptance criteria

1. duplicate IDs fail closed before deeper dependency diagnostics.
2. missing dependency references are rejected deterministically.
3. self-dependencies are rejected.
4. two-node and multi-node dependency cycles are detected deterministically independent of input order.
5. VERIFIED and CONTROLLED dependencies satisfy eligibility.
6. every other non-hard state causes waiting rather than eligibility.
7. hard-blocker states are reported and propagate transitively through unresolved chains.
8. `waiting_on` contains sorted direct unresolved IDs while `blocked_by` contains sorted reachable hard blockers.
9. only current GRAIN nodes can appear in `ready_grains`.
10. `dependency_waves` first wave equals `ready_grains` and projects only currently projectable GRAIN chains.
11. unresolved non-Grain dependencies exclude downstream Grains from wave projection.
12. local `check` fails on malformed dependency graphs before readiness evaluation.
13. `next` text/JSON output is deterministic and read-only.
14. empty eligible set returns exit `0` when graphs are valid.
15. no lifecycle state is mutated.
16. no runtime dependency is added.
17. Specifications 001–005 regressions remain green.

## Success criterion

A local SpecGrain project can answer, deterministically and without an AI model, **which current Grains are genuinely eligible now, what they are waiting on, what known blockers propagate to them, and which additional Grain waves could follow if earlier projected Grains complete successfully**.
