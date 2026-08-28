# Verification 004 — Grain Readiness

**Verification date:** 2026-08-28  
**Environment:** Python `3.13.5`

## Pytest

A reconstructed workspace used the canonical Specification 001–003 source/tests plus the exact candidate `readiness.py`, public exports, and 004 test suite that are uploaded by this implementation commit.

```text
python -m pytest -q
........................................................................ [ 39%]
........................................................................ [ 79%]
......................................                                   [100%]
```

Result: **182 passed**.

The 66 new readiness tests cover:

- passing exact-revision candidate binding;
- invalid refinement forest mapping;
- missing candidate and semantic revision mismatch;
- REFINING source-state and leaf gates;
- acceptance and scope requirements;
- change-surface exception behavior;
- all canonical risk levels and invalid recovery shapes;
- context integer/range/budget rules including bool rejection;
- required evidence shape, uniqueness, and non-empty identifiers;
- readiness-v1 declaration/version behavior;
- unresolved-decision shape and blocking behavior;
- all five minimality choices plus invalid choice/rationale cases;
- both safety statuses and inconsistent/duplicate/blank requirements;
- deterministic issue ordering;
- exact error-report preservation;
- no lifecycle mutation;
- readiness metadata remaining content-digest significant.

The 116 pre-existing Specification 001–003 regression tests also pass.

## Compile check

```text
python -m compileall -q src tests
```

Result: **PASS**.

## Ruff

```text
python -m ruff check .
```

Result: **NOT RUN — `ruff` is not installed in the local environment (`No module named ruff`)**.

This is not reported as PASS. Exact-head repository/external review remains required before merge.

## Scope verification

The implementation adds one dependency-free readiness module, public exports, and focused tests. It does not modify `model.py`, `lifecycle.py`, or `refinement.py`, and it does not scan repositories, validate dependency DAGs, apply method profiles, execute evidence, mutate lifecycle state, or implement CLI/store behavior.
