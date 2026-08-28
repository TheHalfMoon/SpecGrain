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
..................                                                       [100%]
```

Result: **18 tests passed**.

### Compile check

```text
python -m compileall -q src tests
```

Result: **PASS**.

### Digest process determinism smoke check

The same Unicode-containing SpecNode was serialized and hashed in separate Python processes with `PYTHONHASHSEED=1` and `PYTHONHASHSEED=777`.

Both produced:

```text
sha256:2dfd8aa6605d8632292008bb994e984b289b1c0d12d2961e6ba83d95211f9fcb
```

Result: **PASS** for this deterministic smoke case.

### Ruff

`python -m ruff` could not run because `ruff` is not installed in the execution environment and network access is unavailable.

Result: **NOT RUN — tool unavailable**.

This is not reported as PASS. Source was manually reconciled to the configured 100-character line limit and standard-library import grouping before upload. Repository/CI or external review remains responsible for the exact-head lint gate if available.

## Scope review before upload

Implementation contains only:

- package metadata;
- public SpecNode exports;
- deterministic model/validation/serialization/digest code;
- focused tests.

It does not implement lifecycle transition rules, graph algorithms, Grain readiness, CLI, YAML store IO, agent execution, repository scanning, or evidence ledger behavior.
