# Plan 001 — SpecNode Schema

## Implementation strategy

Keep the first product slice deliberately small and dependency-light. Use Python 3.11 standard-library dataclasses and deterministic helper functions rather than introducing a validation framework before its value is demonstrated.

## Planned package layout

```text
pyproject.toml
src/
  specgrain/
    __init__.py
    model.py
tests/
  test_specnode.py
```

No CLI module is added in this spec.

## Internal design

### `SpecValidationError`

One public validation exception for contract failures in 001.

### JSON freezing

A private recursive helper converts:

- mappings -> read-only mappings with recursively frozen values;
- lists/tuples -> tuples;
- scalars -> unchanged after JSON-safety validation.

A corresponding canonicalization helper produces ordinary JSON-compatible objects for serialization.

### `SpecNode`

Use `@dataclass(frozen=True, slots=True)` and normalize caller inputs in `__post_init__` using `object.__setattr__` only during construction.

Required human strings are validated without prose rewriting. Set-like sequence fields are frozen as tuples and duplicate-checked.

### Serialization surfaces

- `to_dict()` returns a detached ordinary Python dictionary suitable for inspection/round trip.
- `canonical_content_dict()` returns semantic digest content with sorted set-like fields and no `state`.
- `canonical_content_json()` returns normalized UTF-8 JSON bytes.
- `revision_digest` returns SHA-256 over `canonical_content_json()`.
- `from_dict()` accepts the documented external field names and converts them into a `SpecNode`.

## Packaging

Create a minimal `pyproject.toml` with:

- project name `specgrain` provisionally;
- version `0.0.0` while unreleased;
- Python `>=3.11`;
- no runtime dependencies;
- pytest/ruff as optional development dependencies;
- pytest configured with `src` on import path.

Registry publication is out of scope for 001. The distribution name can still be revisited before the first release if registry/trademark due diligence requires it.

## Verification

Focused tests must cover:

- valid/invalid IDs;
- required strings;
- duplicate set-like values;
- caller mutation isolation;
- nested mappings/lists;
- Unicode;
- non-finite floats;
- non-string mapping keys;
- canonical ordering;
- round trips;
- state-excluded digest behavior;
- content-sensitive digest behavior.

Run at minimum:

```text
python -m pytest -q
python -m ruff check .
```

If ruff is unavailable in the execution environment, record that explicitly rather than claiming it passed.

## Risk

Primary risk is accidentally defining semantics that belong to later specs. Keep graph, lifecycle, readiness, IO, CLI, and evidence behavior out of 001 even if easy to add.
