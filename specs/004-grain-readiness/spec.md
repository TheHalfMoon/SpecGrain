# Specification 004 — Grain Readiness

**Status:** SHAPED  
**Type:** implementation  
**Created:** 2026-08-28  
**Depends on:** `003-refinement-tree` (`CLOSED_CANONICAL`)

## Problem

A structurally valid leaf is not automatically a Grain. SpecGrain needs a deterministic, explainable readiness contract that prevents humans or agents from labeling work "atomic" merely because it is small or because implementation has begun.

The contract must encode enough explicit information to make execution bounded and verifiable while preserving later ownership boundaries for dependency scheduling, repository scanning, context computation, method profiles, execution, state mutation, and evidence verification.

## Outcome

Implement a versioned, binary Grain-readiness evaluation for one `SpecNode` revision inside a valid refinement forest. A **fresh passing evaluation of the current candidate and current forest** is a deterministic precondition for any future authority that attempts the structurally legal `REFINING -> GRAIN` transition. Specification 004 does not mutate lifecycle state and its report is not a reusable transition capability.

## Core rule

> A Grain is a structurally valid leaf with explicit acceptance, bounded authorized change, declared risk/recovery and context fit, no unresolved decisions, explicit minimality/safety declarations, and required evidence.

There is no readiness score. A candidate either has zero blocking issues or it does not.

## Versioned readiness declaration

Specification 004 interprets `SpecNode.metadata["readiness"]` as a content-significant declaration. It MUST contain:

```text
version: 1
unresolved_decisions: [string, ...]
minimality:
  choice: reuse-existing | stdlib | native | installed-dependency | new-code
  rationale: non-empty string
safety:
  status: none-identified | requirements-defined
  requirements: [string, ...]
```

Optional:

```text
change_surface_exception: non-empty string
```

`readiness.version` is independent from `SPECNODE_SCHEMA_VERSION`. Changing readiness semantics may require a future readiness-version change without changing SpecNode canonicalization.

Because metadata participates in the Specification 001 content digest, readiness declarations are bound to the exact semantic spec revision.

## Other required declarations

### Risk

`SpecNode.risk` MUST contain:

```text
level: low | medium | high | critical
recovery: non-empty string or non-empty JSON object
```

004 checks explicit declaration and shape. Method-specific risk obligations remain Specification 011.

### Context

`SpecNode.context` MUST contain:

```text
budget_tokens: positive integer
estimated_tokens: non-negative integer
```

`estimated_tokens <= budget_tokens` is required.

004 treats these as declared accounting inputs. Specification 008 will later compute/strengthen context-source accounting; it must preserve or migrate this readiness contract explicitly.

### Evidence

`SpecNode.evidence["required"]` MUST be a non-empty sequence of unique non-empty evidence identifiers.

004 proves only that required evidence is named. Specification 010 proves whether the evidence actually exists and passes.

## Minimality interpretation

The minimality choice adapts the canonical Ponytail/Karpathy planning synthesis:

1. `reuse-existing`
2. `stdlib`
3. `native`
4. `installed-dependency`
5. `new-code`

A non-empty rationale is required for every choice. Specification 004 does not claim the rationale is true; later repository intelligence and verification may challenge it. The purpose here is to prevent silent speculative implementation and bind the decision to the spec revision.

Minimality MUST NOT override required security, validation, accessibility, data-protection, recovery, or acceptance obligations.

## Safety declaration

`safety.status` is either:

- `none-identified`: the candidate explicitly declares that no additional safety-specific requirements were identified; `requirements` MUST be empty.
- `requirements-defined`: `requirements` MUST contain at least one unique non-empty requirement.

This is not a security proof. It prevents safety from being silently omitted from planning and gives later WorkPacket/verification stages content to enforce.

## Public API

### `GRAIN_READINESS_VERSION`

Public integer constant equal to `1`.

### `MinimalityChoice`

`StrEnum` containing the five choices above.

### `SafetyStatus`

`StrEnum` containing `none-identified` and `requirements-defined`.

### `ReadinessIssueCode`

Stable machine-readable issue codes for each failed gate.

### `ReadinessIssue`

Immutable issue with:

- `code`;
- `field`;
- deterministic `message`.

### `GrainReadinessReport`

Immutable evaluation result containing:

- `node_id`;
- semantic `revision_digest`;
- ordered `issues`.

It exposes `is_ready: bool` as `not issues`.

The report records the result of one evaluation. It is **not** a durable authorization token, lease, lock, or compare-and-swap precondition for a later state write.

### `evaluate_grain_readiness(node, forest)`

Returns a report and never mutates state.

### `require_grain_readiness(node, forest)`

Returns the passing report or raises `GrainReadinessError` containing it.

Neither helper grants mutation authority. A future state-mutating subsystem MUST evaluate readiness against the **current** candidate and **current** forest and MUST verify that current state is still `REFINING` immediately before committing the write, under that subsystem's concurrency/precondition rules. A previously passing report by itself MUST NOT authorize `REFINING -> GRAIN`.

## Why freshness is separate from the semantic digest

Specification 001 intentionally excludes lifecycle `state` from `revision_digest`; changing only state does not change specification meaning. Therefore the digest proves semantic-content identity, not lifecycle freshness.

Specification 004 keeps that contract intact. It does not add state to the digest and does not add a report field that pretends to make stale reports safe. Freshness belongs to the future mutation boundary, which must re-read/re-evaluate current state rather than trust an earlier report.

## Deterministic gates

### G1 — Valid refinement forest

The forest MUST pass Specification 003. Structural issues become readiness blockers.

### G2 — Exact candidate binding

The candidate ID MUST exist exactly once in the valid forest and the forest copy MUST have the same `revision_digest` as the candidate.

### G3 — Promotion source state

Candidate `state` MUST be `REFINING`, the only lifecycle source structurally permitted to enter `GRAIN` under Specification 002.

This gate is true only for the evaluation inputs supplied to 004. A future mutation authority must re-check it against current repository state at write time.

### G4 — Leaf

Candidate MUST have no children.

### G5 — Acceptance

Candidate MUST contain at least one acceptance condition.

### G6 — Scope

`scope_in` MUST contain at least one authorized behavior/surface.

### G7 — Change surface

`change_surface` MUST be non-empty OR readiness metadata MUST contain a non-empty `change_surface_exception` explaining why exact paths/surfaces cannot yet be declared.

### G8 — Risk and recovery

Risk level and recovery declaration MUST satisfy the shape above.

### G9 — Context fit

Declared `budget_tokens` and `estimated_tokens` MUST be valid integers and estimate MUST not exceed budget.

### G10 — Evidence requirements

At least one unique non-empty required evidence identifier MUST be declared.

### G11 — No unresolved decisions

`unresolved_decisions` MUST be explicitly present and empty.

### G12 — Minimality declaration

A valid minimality choice and non-empty rationale MUST be present.

### G13 — Safety declaration

A valid safety status and internally consistent requirements collection MUST be present.

## Explicit non-gates in 004

004 does NOT:

- semantically judge whether `outcome` prose secretly combines multiple outcomes;
- prove acceptance criteria are good tests;
- verify minimality rationale against repository facts;
- compute context-source token sizes;
- validate the separate dependency DAG or dependency satisfaction;
- apply method-profile-specific risk requirements;
- execute tests/evidence;
- persist or mutate lifecycle state;
- provide concurrency control, compare-and-swap, locks, or durable transition authorization.

Those are owned by later specifications. 004 makes the current readiness boundary explicit instead of pretending deterministic code can prove facts it cannot yet observe.

## Acceptance criteria

1. a fully declared REFINING leaf in a valid forest produces a passing report.
2. a parent/non-leaf cannot pass.
3. invalid forest or candidate revision mismatch cannot pass.
4. missing acceptance/scope/change-surface authorization cannot pass.
5. malformed/missing risk, recovery, context, or evidence declarations cannot pass.
6. context estimate greater than budget cannot pass.
7. missing/non-empty unresolved decisions block readiness.
8. missing/invalid minimality declaration blocks readiness.
9. inconsistent safety declaration blocks readiness.
10. issue ordering is deterministic.
11. `require_grain_readiness` exposes the exact report and never mutates the node.
12. passing readiness does not itself change `REFINING` to `GRAIN`.
13. a previously passing report alone is insufficient authority for any future lifecycle write; current readiness and current `REFINING` state must be re-evaluated at the mutation boundary.
14. Specifications 001–003 regressions remain green.

## Success criterion

For the first time in the repository, "this spec is a Grain" has a deterministic, versioned, explainable evaluation contract rather than being an agent/human label, without turning that evaluation into stale or implicit lifecycle authority.
