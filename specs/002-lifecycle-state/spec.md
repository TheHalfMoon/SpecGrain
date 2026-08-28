# Specification 002 — Lifecycle State

**Status:** SHAPED  
**Type:** implementation  
**Created:** 2026-08-28  
**Depends on:** `001-specnode-schema` (`CLOSED_CANONICAL`)

## Problem

Specification 001 deliberately stored `state` as an opaque string. Without a canonical state vocabulary and deterministic adjacency graph, later readiness, scheduling, execution, and verification modules could disagree about legal movement or allow unsafe jumps.

At the same time, a lifecycle helper must not become a backdoor that lets an agent move a node into `GRAIN`, `READY`, or `VERIFIED` without the gate owned by a later specification.

## Outcome

Provide a deterministic lifecycle vocabulary, state parser, classification helpers, and structural transition validator. Integrate canonical state validation into `SpecNode` construction while preserving Specification 001 content-digest semantics.

## In scope

- canonical lifecycle `SpecState` values;
- case-sensitive parsing/normalization;
- terminal-state classification;
- exceptional-state classification;
- complete structural adjacency graph;
- explainable illegal-transition errors;
- `allowed_transitions`, `is_transition_allowed`, and `require_transition_allowed` helpers;
- `SpecNode` rejection of unknown state values;
- full transition-matrix tests;
- Specification 001 regression tests.

## Out of scope

- applying/mutating a `SpecNode` into a target state;
- proving Grain readiness;
- dependency/repository readiness gates;
- execution authorization;
- verification/evidence authorization;
- transition history/audit persistence;
- automatic state restoration after a blocker/failure/staleness event;
- CLI, repository IO, or agent adapters.

## Canonical states

Normal/control states:

- `DRAFT`
- `SHAPED`
- `REFINING`
- `GRAIN`
- `READY`
- `RUNNING`
- `VERIFYING`
- `VERIFIED`
- `CONTROLLED`

Exceptional states:

- `BLOCKED`
- `FAILED`
- `STALE`

Terminal states:

- `CANCELLED`
- `SUPERSEDED`

## Structural transition graph

The canonical adjacency set is:

| From | Structurally allowed targets |
| --- | --- |
| `DRAFT` | `SHAPED`, `BLOCKED`, `CANCELLED`, `SUPERSEDED` |
| `SHAPED` | `REFINING`, `BLOCKED`, `STALE`, `CANCELLED`, `SUPERSEDED` |
| `REFINING` | `GRAIN`, `BLOCKED`, `STALE`, `CANCELLED`, `SUPERSEDED` |
| `GRAIN` | `READY`, `SHAPED`, `BLOCKED`, `STALE`, `CANCELLED`, `SUPERSEDED` |
| `READY` | `RUNNING`, `SHAPED`, `BLOCKED`, `STALE`, `CANCELLED`, `SUPERSEDED` |
| `RUNNING` | `VERIFYING`, `BLOCKED`, `FAILED`, `STALE`, `CANCELLED`, `SUPERSEDED` |
| `VERIFYING` | `VERIFIED`, `BLOCKED`, `FAILED`, `STALE`, `CANCELLED`, `SUPERSEDED` |
| `VERIFIED` | `CONTROLLED`, `STALE`, `SUPERSEDED` |
| `CONTROLLED` | `STALE`, `SUPERSEDED` |
| `BLOCKED` | `SHAPED`, `CANCELLED`, `SUPERSEDED` |
| `FAILED` | `SHAPED`, `CANCELLED`, `SUPERSEDED` |
| `STALE` | `SHAPED`, `CANCELLED`, `SUPERSEDED` |
| `CANCELLED` | none |
| `SUPERSEDED` | none |

This graph expresses structural possibility only. It does not authorize protected edges.

## Functional requirements

### FR-001 Canonical enum

Expose `SpecState` as a Python 3.11 `StrEnum` with exactly the 14 canonical values above.

### FR-002 State parsing

`parse_spec_state(value)` MUST accept a canonical string or `SpecState` and return `SpecState`. Unknown, differently cased, empty, or non-string values MUST fail with a stable `LifecycleStateError`.

### FR-003 SpecNode integration

`SpecNode` construction and `from_dict()` MUST reject unknown lifecycle state strings as `SpecValidationError`. Valid states MUST remain serialized as their canonical uppercase strings.

Adding lifecycle validation MUST NOT change Specification 001 canonical content or revision digests for nodes that already used valid states, because `state` remains excluded from the content digest.

### FR-004 Classification

Expose immutable `TERMINAL_STATES` and `EXCEPTIONAL_STATES` collections matching this specification.

### FR-005 Allowed targets

`allowed_transitions(state)` MUST return an immutable set of structurally legal target `SpecState` values.

### FR-006 Structural predicate

`is_transition_allowed(current, target)` MUST return `True` exactly for the adjacency table above and `False` for same-state or non-adjacent transitions. Invalid state input MUST raise `LifecycleStateError` rather than returning `False`.

### FR-007 Explainable rejection

`require_transition_allowed(current, target)` MUST return `None` for a legal edge and raise `LifecycleTransitionError` for an illegal edge. The error MUST include canonical source/target names and the source state's allowed targets (or explicitly report none).

### FR-008 No mutation authority

Specification 002 MUST NOT expose a generic function that changes a `SpecNode.state`. Later gate-owning specifications are responsible for applying authorized state changes after validating this structural graph.

### FR-009 Conservative exceptional recovery

`BLOCKED`, `FAILED`, and `STALE` may recover only to `SHAPED` (or terminate through `CANCELLED`/`SUPERSEDED`). Direct resume to `REFINING`, `GRAIN`, `READY`, `RUNNING`, `VERIFYING`, or `VERIFIED` MUST be structurally illegal.

## Non-functional requirements

- runtime implementation remains standard-library only;
- transition data is immutable from public callers;
- behavior is deterministic and side-effect free;
- public helpers are type annotated;
- no network, filesystem, Git, or model access is required.

## Acceptance criteria

1. The canonical enum contains exactly 14 unique values.
2. Every pair in the documented transition matrix produces the expected predicate result.
3. `CANCELLED` and `SUPERSEDED` have no outgoing edges.
4. Exceptional recovery cannot directly resume protected downstream phases.
5. invalid states produce stable parsing/validation errors.
6. `SpecNode(state="UNKNOWN")` fails while all 14 canonical states construct successfully.
7. Existing Specification 001 golden canonical bytes/digest remain unchanged.
8. No public 002 API mutates a node state or grants transition authorization.
9. Full available tests pass on the supported local Python baseline.

## Success criterion

Later readiness, scheduler, execution, and verification modules can rely on one deterministic lifecycle graph without gaining a lifecycle-only bypass around their own authorization gates.
