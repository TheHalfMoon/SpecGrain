# Plan 012 — Diff, Drift, and Metrics

## Design

Add one dependency-free `metrics.py` module plus bounded public exports and focused tests.

### Change scope

Normalize authorized surfaces and observed changed paths. A changed path is authorized only when it is exactly a declared surface or a descendant of one.

### Drift

Compare caller-supplied exact revisions. Emit stable signals for SpecNode revision, repository revision, and optional context-plan digest. Do not interpret why the values changed.

### Metrics

Aggregate immutable `DeliveryObservation` values. Use integer `Ratio` values for bounded rates; represent mean cycle seconds as an exact numerator/denominator pair. Do not store actor identity.

## Change surface

- `src/specgrain/metrics.py`
- `src/specgrain/__init__.py`
- `tests/test_metrics.py`
- Specification/ADR/continuation records only.

## Verification

Run full 001–012 pytest regression, compileall, editable install using available local build dependencies, console/module parity, line-length inspection, exact uploaded blob verification, and exact-diff review.
