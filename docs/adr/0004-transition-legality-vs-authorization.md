# ADR-0004: Separate Lifecycle Legality from Transition Authorization

**Status:** Accepted  
**Date:** 2026-08-28

## Context

SpecGrain needs a deterministic lifecycle graph, but several lifecycle edges correspond to trust gates owned by later subsystems. For example, `REFINING -> GRAIN` must eventually require Grain-readiness evidence, `GRAIN -> READY` must require dependency/repository preconditions, and `VERIFYING -> VERIFIED` must require verification evidence.

If the lifecycle module both declares an edge legal and mutates a node into the target state, it would create a bypass around those future authorities.

## Decision

Specification 002 defines and validates **structural lifecycle legality only**.

The lifecycle module may:

- define canonical state names;
- parse and normalize state values;
- expose the legal adjacency graph;
- answer whether an edge is structurally legal;
- reject illegal edges with explainable deterministic errors.

The lifecycle module MUST NOT expose a general-purpose API that mutates a `SpecNode` into a new protected lifecycle state.

Authorization to perform a legal edge belongs to the subsystem that owns the corresponding gate. Later specifications may call lifecycle legality validation only after their own gate succeeds.

## Consequences

- `is_transition_allowed(REFINING, GRAIN)` means the edge is structurally valid, not that Grain readiness passed.
- agents cannot use the lifecycle module alone to self-promote a node to `GRAIN`, `READY`, or `VERIFIED`;
- future gate-owning modules remain responsible for exact evidence and state mutation;
- lifecycle tests can remain deterministic and independent from repository IO, agent execution, or evidence stores.

## Recovery rule

Exceptional states `BLOCKED`, `FAILED`, and `STALE` recover through `SHAPED` rather than blindly resuming the prior phase. This deliberately forces re-evaluation after an exceptional condition. More advanced history-aware resume semantics require a later explicit specification.
