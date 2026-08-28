# Plan 015 — SpecGrainBench

## Design

Add one dependency-free `benchmark.py` public module with immutable experiment/run/report contracts, strict validation, contamination preflight, deterministic serialization/digests, and actor-neutral arm summaries.

The harness validates observations supplied by external runners. It does not execute benchmark arms itself and therefore cannot manufacture an empirical performance claim.

## Change surface

- `src/specgrain/benchmark.py`
- `tests/test_benchmark.py`
- Specification/ADR/continuation records only.

No CLI, store, lifecycle, verification, packet, adapter, repository, context, or runtime dependency change is authorized.

## Verification

Use a verification-only branch derived from the exact product commit to run:

- full pytest regression;
- Ruff on the 015 surface and full repository;
- compileall;
- editable install;
- console/module entry-point parity;
- changed-line length inspection;
- exact product/test blob review.

The verification workflow is not part of the product PR.
