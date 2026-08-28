# Specification 001 — SpecNode Schema

**Status:** SHAPED  
**Type:** implementation  
**Created:** 2026-08-28  
**Depends on:** `000-foundation` (`CLOSED_CANONICAL`)

## Problem

SpecGrain requires one recursive specification primitive before it can implement lifecycle rules, refinement, readiness, scheduling, or evidence. If this primitive is ambiguous or mutable in uncontrolled ways, every later digest, WorkPacket, graph edge, and evidence record becomes unstable.

## Outcome

Provide a dependency-light Python model for `SpecNode` with deterministic validation, normalized serialization, and a content revision digest that is stable across semantically irrelevant ordering differences.

## In scope

- Python package scaffold for the deterministic core;
- canonical SpecGrain ID syntax validation;
- immutable `SpecNode` construction;
- the foundation-defined SpecNode fields;
- JSON-safe nested metadata validation/freezing;
- deterministic mapping-key normalization;
- deterministic ordering for set-like SpecNode collections;
- normalized UTF-8 JSON serialization;
- SHA-256 content revision digest;
- round-trip parsing from dictionaries;
- explicit validation errors;
- unit tests for all behavior in this spec.

## Out of scope

- state-transition legality;
- recursive tree/forest validation;
- dependency graph validation or scheduling;
- Grain readiness decisions;
- ID allocation;
- YAML parsing or `.specgrain/` store IO;
- CLI commands;
- AI decomposition/refinement;
- repository context selection;
- WorkPackets and execution results;
- verification/evidence state.

## Data contract

A `SpecNode` contains these fields in 001:

- `id: str`
- `title: str`
- `outcome: str`
- `rationale: str`
- `parent_id: str | None`
- `scope_in: tuple[str, ...]`
- `scope_out: tuple[str, ...]`
- `acceptance: tuple[str, ...]`
- `dependencies: tuple[str, ...]`
- `risk: JSON object`
- `context: JSON object`
- `change_surface: tuple[str, ...]`
- `evidence: JSON object`
- `method: str`
- `state: str`
- `children: tuple[str, ...]`
- `labels: tuple[str, ...]`
- `metadata: JSON object`

`state` is an opaque stored string in 001. Legal states and transitions belong to `002-lifecycle-state`.

## Functional requirements

### FR-001 Canonical ID syntax

A SpecGrain repository-local ID MUST match `SG-` followed by exactly six decimal digits, for example `SG-000001`.

001 validates IDs but does not allocate them.

### FR-002 Required human meaning

`title` and `outcome` MUST be non-empty after whitespace inspection. The model MUST preserve authored string content rather than silently rewriting prose.

### FR-003 Immutable normalized collections

Sequence fields MUST be stored as tuples. Mapping/list values inside JSON-object fields MUST be recursively frozen so mutation through caller-owned containers cannot change an already-created SpecNode's revision digest.

### FR-004 JSON-safe metadata

Nested object fields MUST accept only JSON-compatible values with string object keys. Non-finite floats (`NaN`, positive/negative infinity) MUST be rejected.

### FR-005 Set-like normalization

The following fields are semantically set-like for canonical content and MUST be sorted deterministically when serialized/digested:

- `scope_in`
- `scope_out`
- `acceptance`
- `dependencies`
- `change_surface`
- `children`
- `labels`

Duplicate values in these fields MUST be rejected rather than silently collapsed.

### FR-006 Mapping normalization

Object keys MUST be sorted recursively in canonical output. Unknown nested list order MUST be preserved because its semantics are not known to the core.

### FR-007 Canonical serialization

Canonical JSON MUST:

- use UTF-8;
- sort object keys;
- use compact separators;
- preserve Unicode characters rather than forcing ASCII escapes;
- reject non-finite numeric values;
- produce identical bytes for semantically equivalent SpecNodes under the normalization rules above.

### FR-008 Content revision digest

`revision_digest` MUST be `sha256:<lowercase hex>` over canonical semantic content.

The operational `state` field MUST be excluded from the content digest so lifecycle movement does not create a new specification-content revision. All other 001 fields are content-significant.

### FR-009 Round trip

`SpecNode.from_dict(node.to_dict())` MUST preserve the same authored values under the model's normalization contract and MUST produce the same revision digest.

### FR-010 Explicit failures

Invalid inputs MUST raise a stable `SpecValidationError` (or documented subclass) rather than leaking incidental low-level exceptions as the public contract.

## Non-functional requirements

- Core model implementation SHOULD use the Python standard library only for 001 unless a dependency becomes demonstrably necessary.
- Python requirement is 3.11+.
- Public behavior MUST be type annotated.
- Canonical serialization/digest code MUST be deterministic and side-effect free.
- Tests MUST not depend on network access or environment-specific state.

## Acceptance criteria

1. Two nodes differing only in order of set-like fields have identical canonical semantic JSON and revision digests.
2. Two nodes differing in a content-significant field have different revision digests.
3. Two otherwise identical nodes differing only in `state` have the same revision digest.
4. Mutating caller-owned input dictionaries/lists after construction cannot change the node's serialized value or digest.
5. Nested Unicode content round-trips deterministically.
6. Non-string object keys and non-finite floats are rejected.
7. Duplicate set-like values are rejected.
8. Invalid IDs are rejected while valid `SG-000001` style IDs pass.
9. The test suite passes on the supported local Python baseline.

## Success criterion

The exact implementation revision provides a trustworthy immutable content object that later lifecycle, refinement, graph, WorkPacket, and evidence specs can build on without redefining serialization or revision semantics.
