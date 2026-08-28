# Specification 003 — Refinement Tree

**Status:** SHAPED  
**Type:** implementation  
**Created:** 2026-08-28  
**Depends on:** `002-lifecycle-state` (`CLOSED_CANONICAL`)

## Problem

SpecGrain has a recursive `SpecNode` schema and lifecycle vocabulary, but a collection of nodes can still describe an impossible refinement structure: duplicate identities, missing parents or children, self-links, inconsistent parent/child declarations, or cycles.

Later Grain readiness must be able to trust that "leaf" and "parent" have deterministic structural meaning before it evaluates semantic readiness.

## Outcome

Provide a dependency-free deterministic refinement validator for a collection of `SpecNode` values. It reports structured, stably ordered structural issues and can fail closed when the collection is not a valid forest.

## In scope

- duplicate node-ID detection;
- missing parent detection;
- missing child detection;
- self-parent detection;
- self-child detection;
- reciprocal parent/child consistency;
- multiple-parent inconsistency detection through reciprocal declarations;
- directed cycle detection;
- deterministic root identification for a valid forest;
- structured validation issues and one aggregate validation error;
- deterministic issue ordering;
- tests for valid forests and malformed structures.

## Out of scope

- semantic quality of decomposition;
- whether children collectively cover a parent's acceptance criteria;
- duplicated semantic responsibility across children;
- AI-generated refinement proposals;
- Grain readiness or `REFINING -> GRAIN` authorization;
- dependency DAG validation (the `dependencies` field is Specification 006 territory);
- lifecycle mutation;
- repository storage or CLI;
- ordering/prioritization of children for execution.

## Structural model

A refinement forest is a finite set of uniquely identified `SpecNode` values in which:

1. every non-root node's `parent_id` resolves to exactly one node in the same collection;
2. a parent that names a child in `children` is reciprocated by that child's `parent_id`;
3. a child with `parent_id=X` is named in X's `children`;
4. no node names itself as parent or child;
5. following parent/child refinement edges cannot return to an already visited node;
6. roots are exactly nodes whose `parent_id is None`.

`children` order is not semantic in Specification 003. Specification 001 already treats `children` as set-like for canonical content. Execution ordering belongs to dependency/scheduling specifications.

## Identity blocker rule

Duplicate IDs make relationship resolution ambiguous. If duplicate node IDs exist, validation MUST report deterministic duplicate-ID issues and MUST NOT pretend deeper parent/child resolution is trustworthy. Callers must fix identity ambiguity before relying on additional structural diagnostics.

## Public API

### `RefinementIssueCode`

A `StrEnum` with exactly these initial codes:

- `DUPLICATE_ID`
- `MISSING_PARENT`
- `MISSING_CHILD`
- `SELF_PARENT`
- `SELF_CHILD`
- `PARENT_CHILD_MISMATCH`
- `CHILD_PARENT_MISMATCH`
- `CYCLE`

### `RefinementIssue`

An immutable structured issue with:

- `code`;
- `node_id`;
- optional `related_id`;
- concise deterministic `message`.

### `validate_refinement(nodes)`

Returns `tuple[RefinementIssue, ...]` sorted deterministically. Empty tuple means structurally valid.

The function MUST reject non-`SpecNode` collection members with `TypeError`; malformed SpecNode field values are already rejected by Specifications 001/002.

### `require_valid_refinement(nodes)`

Returns `None` for a valid forest and raises `RefinementValidationError` containing the exact structured issue tuple otherwise.

### `refinement_roots(nodes)`

Returns root nodes sorted by canonical node ID only if the forest is valid. Invalid forests MUST raise `RefinementValidationError` rather than returning a partial root view.

## Functional requirements

### FR-001 Stable identity pass

Validation MUST materialize the input once and detect duplicate IDs before relationship resolution. Duplicate issues MUST be deterministic regardless of input order.

### FR-002 Reference integrity

A non-null `parent_id` MUST resolve within the collection. Every `children` reference MUST resolve within the collection.

### FR-003 Self-link rejection

A node MUST NOT use its own ID as `parent_id` or include its own ID in `children`.

### FR-004 Reciprocal declarations

For unique IDs:

- if child `C.parent_id == P`, then `C.id` MUST be present in `P.children`;
- if parent P includes C in `P.children`, then `C.parent_id` MUST equal `P.id`.

These failures MUST use distinct structured issue codes so callers can explain which declaration is missing or conflicting.

### FR-005 Cycle detection

Validation MUST detect directed cycles in refinement relationships and report a deterministic cycle issue. A cycle issue message MUST identify a canonical cycle path independent of input collection order.

### FR-006 Deterministic issue ordering

For the same semantic collection, issue tuples MUST have the same order regardless of input node order. Ordering MUST be defined from issue code/value and involved canonical IDs, not traversal insertion order.

### FR-007 Valid roots

A valid forest may contain zero nodes, one tree, or multiple trees. Root results MUST be sorted by node ID.

### FR-008 No semantic overreach

Specification 003 MUST NOT infer that a structurally valid leaf is a Grain. It MUST NOT judge value, acceptance quality, risk, context fit, minimality, safety floors, or unresolved decisions.

## Non-functional requirements

- standard library only;
- no filesystem/network/model access;
- deterministic and side-effect free;
- no mutation of input SpecNodes;
- public behavior type annotated;
- no heavyweight graph abstraction or dependency unless this narrow contract cannot be met without one.

## Acceptance criteria

1. empty, single-root, and multi-root valid forests pass.
2. duplicate IDs fail before ambiguous relationship diagnostics are trusted.
3. missing parent and child references are reported structurally.
4. self-parent and self-child links are reported.
5. parent/child reciprocal mismatches are reported with distinct codes.
6. cycles are detected with deterministic canonical paths.
7. input order does not change issue ordering or root ordering.
8. invalid forests cannot return a partial root view.
9. no API promotes lifecycle state or claims Grain readiness.
10. Specifications 001/002 regression tests remain green.

## Success criterion

Specification 004 can rely on a deterministic valid refinement forest and trustworthy leaf/root semantics without importing AI judgment, execution scheduling, or semantic decomposition logic into the structural kernel.
