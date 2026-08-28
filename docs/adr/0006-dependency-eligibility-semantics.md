# ADR-0006: Dependency Eligibility and Blocker Semantics

**Status:** Accepted  
**Date:** 2026-08-28

## Context

`SpecNode.dependencies` already stores canonical SpecGrain IDs, but Specifications 001–005 do not define what dependency states mean for execution eligibility. Specification 006 must compute deterministic ready sets without silently turning dependency analysis into lifecycle mutation or assuming that every non-terminal state is equivalent.

## Decision

Dependency state semantics are:

### Satisfied

A dependency is satisfied only when its current lifecycle state is:

- `VERIFIED`; or
- `CONTROLLED`.

These states represent completed work with verification evidence semantics owned by the lifecycle/verification model.

### Hard blocker

A dependency in any of these states is a hard blocker:

- `BLOCKED`;
- `FAILED`;
- `STALE`;
- `CANCELLED`;
- `SUPERSEDED`.

Known hard blockers propagate transitively through unresolved dependency chains.

### Waiting

Every other dependency state is unresolved but not a hard blocker:

- `DRAFT`;
- `SHAPED`;
- `REFINING`;
- `GRAIN`;
- `READY`;
- `RUNNING`;
- `VERIFYING`.

A waiting dependency prevents current eligibility but does not by itself mark downstream work failed.

## Grain eligibility

Only a node currently in `GRAIN` is a candidate for the Specification 006 ready set. It is eligible when:

1. the dependency graph is structurally valid;
2. every direct dependency is currently satisfied;
3. no unresolved dependency chain contains a hard blocker.

Specification 006 reports eligibility only. It MUST NOT mutate `GRAIN -> READY`.

## Wave projection

Wave projection is advisory and deterministic. It simulates completion only for currently `GRAIN` nodes whose dependencies can be satisfied by the already-satisfied set plus earlier projected Grain waves.

A Grain depending on an unresolved non-Grain state is not projected until that external state changes. Hard-blocked dependency chains are not projected.

## Consequences

- `next` can identify genuinely eligible current Grains without rewriting state.
- A node in `READY`, `RUNNING`, or `VERIFYING` is still unresolved as a dependency until it becomes `VERIFIED` or `CONTROLLED`.
- `SUPERSEDED` does not silently satisfy a dependency; replacement/rebinding semantics require an explicit future contract.
- Blocker propagation is explainable and current-state based.
- Historical readiness reports are not reused as dependency completion evidence.
