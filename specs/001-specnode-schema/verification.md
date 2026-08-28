# Verification 001 — SpecNode Schema

**Local verification date:** 2026-08-28  
**Implementation source:** exact content prepared for `feat/001-specnode-schema`

## Environment

- Python: `3.13.5`
- Network access: unavailable in local container
- Product runtime dependencies: none

## Results

### Pytest

```text
python -m pytest -q
.......................                                                  [100%]
```

Result: **23 tests passed**.

### Compile check

```text
python -m compileall -q src tests
```

Result: **PASS**.

### Digest process determinism smoke check

The same Unicode-containing SpecNode was serialized and hashed in separate Python processes with `PYTHONHASHSEED=1` and `PYTHONHASHSEED=777` after adding `schema_version=1` to canonical content.

Both produced:

```text
sha256:3990c4fc3dc00d51baa33e58d424d70da5fc0d34bf6ac737763444fa45549a9a
```

Result: **PASS** for this deterministic smoke case.

### Ruff

`python -m ruff` could not run because `ruff` is not installed in the execution environment and network access is unavailable.

Result: **NOT RUN — tool unavailable**.

This is not reported as PASS. Source was manually reconciled to the configured 100-character line limit and standard-library import grouping before upload. Repository/CI or external review remains responsible for the exact-head lint gate if available.

## Review finding remediated

The first uploaded implementation did not version the canonicalization contract. Review finding F-001 added public `SPECNODE_SCHEMA_VERSION = 1`, required `schema_version=1` on nodes, rejected unsupported versions, and included the version in canonical content/digest. See `review.md`.

## Scope review before upload

Implementation contains only:

- package metadata;
- public SpecNode exports;
- deterministic model/validation/serialization/digest code;
- focused tests.

It does not implement lifecycle transition rules, graph algorithms, Grain readiness, CLI, YAML store IO, agent execution, repository scanning, or evidence ledger behavior.
