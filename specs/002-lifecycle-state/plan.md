# Plan 002 — Lifecycle State

## Strategy

Implement lifecycle semantics in a new dependency-free `specgrain.lifecycle` module. Keep state mutation out of the module. Integrate only state-name validation into `SpecNode`.

## Planned files

```text
src/specgrain/lifecycle.py
src/specgrain/model.py
src/specgrain/__init__.py
tests/test_lifecycle.py
specs/002-lifecycle-state/*
```

## API

### `SpecState`

Use `enum.StrEnum` because Python 3.11 is the project baseline. Enum values are the canonical uppercase strings.

### Errors

- `LifecycleStateError(ValueError)` for invalid state values.
- `LifecycleTransitionError(ValueError)` for structurally illegal edges.

### Parsing

`parse_spec_state(value)` performs strict case-sensitive parsing. No whitespace trimming or case coercion occurs; authored mistakes fail explicitly.

### Transition graph

Keep a private mapping from every `SpecState` to `frozenset[SpecState]`. Public callers receive immutable frozensets through `allowed_transitions`.

`is_transition_allowed` parses both sides, then checks exact membership.

`require_transition_allowed` uses the same graph and emits a deterministic error that lists allowed targets sorted by canonical value.

### SpecNode integration

`model.py` imports only the state parser/error from `lifecycle.py`; `lifecycle.py` does not import `SpecNode`. This avoids a circular dependency and preserves the rule that the lifecycle module has no node-mutation authority.

`SpecNode.__post_init__` normalizes a valid state to `SpecState.value` and wraps lifecycle input errors as `SpecValidationError` to preserve the model's public validation contract.

## Verification

Add exhaustive matrix tests rather than testing a small sample. The expected transition table in the test is independently declared and compared against every source/target pair.

Also test:

- enum completeness/uniqueness;
- invalid/case-mismatched state parsing;
- terminal and exceptional collections;
- deterministic error messages;
- conservative exceptional recovery;
- SpecNode validation for all canonical states and unknown states;
- unchanged Specification 001 golden digest;
- full existing test suite.

Run available local checks:

```text
python -m pytest -q
python -m compileall -q src tests
python -m ruff check .
```

If Ruff is unavailable, record `NOT RUN` rather than claiming PASS.

## Risk

The main risk is confusing adjacency with authority. Tests and documentation must never imply that a `True` structural edge proves readiness/evidence. ADR-0004 is the durable boundary.
