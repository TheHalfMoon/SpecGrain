# Verification 008 — Context Budget

**Verification date:** 2026-08-28  
**Environment:** Python `3.13.5`, pytest `9.0.2`  
**Exact verified product head:** `5d7822218888302d95ccfc580ea37a0853759d34`

## Exact uploaded bytes

```text
src/specgrain/context.py          c68cf285ae4fa2358583163b136e55e53ee7cb0c
src/specgrain/__init__.py         b1a5d6f6678b3e83a3ab0075cf8d570ee348df15
tests/test_context.py             31fd6c0e13a8784bf7af8c91270e9da718649379
```

GitHub returned those same blob SHAs from the exact product head. The net implementation diff from planning head `ca53852a2239483e2a51b72de8786e785b04f37a` contains only those three planned files.

## Pytest

```text
python -m pytest
........................................................................ [ 20%]
........................................................................ [ 40%]
........................................................................ [ 61%]
........................................................................ [ 81%]
..................................................................       [100%]
354 passed in 0.89s
```

This is the 304-test Specification 001–007 baseline plus 50 new Specification 008 tests.

The new tests cover public frozen/slotted records, text/cost/policy validation, bool rejection, duplicate/non-source collection failures, empty/passing plans, required token/byte/source-count blockers, required non-omission, deterministic optional priority/tie packing, later-small-source fit after earlier omission, all configured dimensions, permutation invariance, digest change sensitivity, exact error-report preservation, and repository-map revision/size/no-rescan/no-mutation behavior.

## Compile / packaging / entry points

```text
python -m compileall -q src tests
python -m pip install -e . --no-build-isolation -q
diff -u <(specgrain --help) <(python -m specgrain --help)
```

Result: **PASS**.

No CLI command changed in 008; entry-point parity remains intact.

## Style preflight

Changed source/tests contain 0 lines over 100 characters.

Ruff is unavailable in the execution environment and is therefore **NOT RUN**, not PASS.

## Scope verification

The exact implementation adds only the context accounting kernel, public exports, and focused tests. It adds no file-content retrieval, tokenizer execution, LLM/embedding selection, WorkPacket/evidence semantics, lifecycle/store writes, dependency scheduling, subprocess execution, CLI behavior, or third-party runtime dependency.

## Residual boundary

`token_cost` is deliberately an explicit revision-bound accounting input. Specification 008 verifies its type and uses it deterministically but does not prove that an upstream tokenizer/measurement source calculated the value accurately. Later adapters may strengthen measurement provenance without changing the 008 accounting semantics.
