# Verification 004 — Grain Readiness

**Verification date:** 2026-08-28  
**Environment:** Python `3.13.5`

## Pytest

A reconstructed workspace used the canonical Specification 001–003 source/tests plus the exact candidate `readiness.py`, public exports, and 004 test suite uploaded by implementation head `f8e4e3a2e32647cc324b1c059b2c9d0c173db561`.

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

## Exact-head contract remediation

Review of initial PR head `f8e4e3a2e32647cc324b1c059b2c9d0c173db561` identified F-001: documentation could be read as making a passing readiness report reusable transition authority even though lifecycle state is excluded from the semantic digest.

The remediation is documentation-only. It clarifies that a report is not a durable transition token and that any future state-mutating subsystem must re-read/re-evaluate current candidate/current forest and current `REFINING` state immediately before its write. No runtime source or test behavior changed, so the 182-test implementation evidence remains the exact product-code evidence for the remediated PR.

See `specs/004-grain-readiness/review.md`.

## Scope verification

The implementation adds one dependency-free readiness module, public exports, and focused tests. It does not modify `model.py`, `lifecycle.py`, or `refinement.py`, and it does not scan repositories, validate dependency DAGs, apply method profiles, execute evidence, persist/mutate lifecycle state, or implement CLI/store behavior.
