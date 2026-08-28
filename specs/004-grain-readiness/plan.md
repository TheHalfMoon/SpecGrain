# Plan 004 — Grain Readiness

## Strategy

Add one dependency-free `specgrain.readiness` module. Keep authored readiness declarations inside existing content-significant `SpecNode` fields instead of changing the SpecNode schema or inventing a second planning object.

## Planned source surface

```text
src/specgrain/readiness.py
src/specgrain/__init__.py
tests/test_readiness.py
```

Do not modify `model.py`, `lifecycle.py`, or `refinement.py` unless exact implementation evidence proves a compatibility defect.

## Readiness contract version

Expose:

```text
GRAIN_READINESS_VERSION = 1
```

Require `metadata.readiness.version == 1`. This versions the interpretation of readiness metadata independently from SpecNode schema/canonicalization version.

## Implementation shape

Use:

- `MinimalityChoice(StrEnum)`;
- `SafetyStatus(StrEnum)`;
- `ReadinessIssueCode(StrEnum)`;
- frozen/slotted `ReadinessIssue`;
- frozen/slotted `GrainReadinessReport` with `is_ready` property;
- `GrainReadinessError` carrying exact report;
- pure `evaluate_grain_readiness` and `require_grain_readiness` functions.

No score, no LLM, no policy engine, no persistence authority, and no lifecycle mutator.

## Forest/candidate binding

Materialize the forest once. Run `validate_refinement` first.

If the forest is structurally invalid, emit deterministic `REFINEMENT_INVALID` readiness issues mapped from the structured refinement issues and stop gates that depend on trusted leaf/reference semantics.

For a structurally valid forest:

1. find candidate by ID;
2. require existence;
3. compare candidate/forest `revision_digest`;
4. evaluate intrinsic readiness fields on the candidate.

`revision_digest` intentionally excludes lifecycle state, so candidate binding proves semantic content identity while the source-state gate separately checks state for the supplied evaluation input.

## Transition-freshness boundary

A `GrainReadinessReport` is an evaluation result, not a reusable transition token.

Because lifecycle state is intentionally excluded from `revision_digest`, a future state-mutating subsystem MUST NOT accept an earlier passing report as sufficient authority. Immediately before a `REFINING -> GRAIN` write it must:

1. load the current candidate and current refinement forest;
2. evaluate current Grain readiness again;
3. verify current state is still `REFINING`;
4. commit under that subsystem's own concurrency/precondition mechanism.

Adding `source_state` to the report would only record what was observed; it would not prevent stale reuse. The smaller and stronger contract is to require fresh evaluation at the mutation boundary and keep mutation/concurrency out of 004.

## Parsing authored declarations

SpecNode nested objects are already frozen JSON mappings/tuples. Readiness helpers should accept the in-memory Mapping/tuple representation and produce issues rather than leaking `KeyError`, `TypeError`, or enum parser errors.

Avoid normalizing or silently repairing malformed declarations. Readiness is fail-closed.

## Issue ordering

Sort issues by:

```text
(code.value, field, message)
```

When mapping Specification 003 issues, preserve their deterministic order through deterministic messages/fields.

## Minimality declaration

Validate:

```text
metadata.readiness.minimality.choice
metadata.readiness.minimality.rationale
```

Choice is one of the five canonical rungs. Rationale must be non-empty after whitespace inspection.

Do not inspect the repository or automatically decide a better rung in 004. Specification 007 will provide repository facts; Specification 012 can later measure unnecessary change.

## Safety declaration

Validate status and requirements consistency only. Do not infer security requirements from code in 004.

## Context declaration

Reject bools as integers. Require:

- positive `budget_tokens`;
- non-negative `estimated_tokens`;
- estimate <= budget.

Specification 008 later owns deterministic source accounting. 004 only establishes the versioned fit contract.

## Risk/recovery declaration

Require risk level enum text and a non-empty recovery value. Accept either:

- non-empty string; or
- non-empty Mapping.

Do not impose method-specific fields yet.

## Evidence declaration

Require `evidence.required` as a non-empty tuple/list-like sequence of unique non-empty strings. The SpecNode freezer already prevents mutation; 004 still validates semantics because `evidence` is intentionally generic at schema level.

## Verification plan

Tests must cover:

- fully passing candidate;
- valid forest/candidate binding;
- invalid forest mapping;
- candidate absent/revision mismatch;
- source state and leaf gates;
- acceptance/scope/change-surface exception;
- risk level and recovery shapes;
- context type/range/budget failures including bool rejection;
- evidence required shape/duplicates;
- readiness version;
- unresolved decisions shape/non-empty blocking;
- every minimality choice and malformed declaration;
- both safety statuses and inconsistent requirements;
- deterministic issue ordering;
- exact error report preservation;
- no node mutation/state promotion;
- all 001–003 regressions.

Transition freshness is a contract requirement for the future mutating subsystem, not a claim that 004 can test persistence/concurrency it does not implement.

## Donor synthesis mapping

- **Ponytail:** minimality is explicit but safety floors cannot be simplified away.
- **Karpathy-inspired:** success criteria, assumptions/uncertainty, and surgical boundaries are explicit spec content.
- **Spec Kit:** readiness functions as a constitution-like gate before implementation, while remaining recursive-spec-native rather than task-list-native.

## Risk

The main risks are pretending declarations are stronger evidence than they are and treating a historical readiness result as current authorization. Documentation and API names must remain precise: 004 evaluates the **readiness contract** for supplied inputs, while later repository intelligence, persistence/concurrency, and verification prove external/current facts.
