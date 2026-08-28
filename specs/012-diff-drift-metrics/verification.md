# Verification 012 — Diff, Drift, and Metrics

## Exact product state

Exact implementation commit:

`7434b094f93df4fb72e03640623a626f5ea5d4e0`

Exact uploaded blobs:

```text
src/specgrain/metrics.py          3ae0415291c64daf0474e359de46e2c29a74918f
src/specgrain/__init__.py         d31bc4e0932eafde0b546f97e414167bba4cffa2
tests/test_metrics.py             c020f19f2aaea8806b6cf9b29c3de26a7ba2d5b7
```

The exact implementation diff from planning head `023e93ac1db0e5f81c803f8ed7472c7f389c6bfe` contains only those three files.

## Regression

- 464 pytest tests PASS.
- compileall PASS.
- editable install with `--no-build-isolation` PASS.
- installed console/module help parity PASS.
- 0 changed implementation/test lines over 100 characters.
- Ruff NOT RUN because unavailable.

## Contract evidence

- change-scope partitioning uses canonical literal path/prefix semantics and rejects ambiguous paths;
- drift signals only exact revision mismatches and never infer cause/severity;
- aggregate observations contain no actor identity;
- first-pass verification, rework, cycle, context-efficiency, scope-accuracy, and spec-drift measures use integer counts/ratios;
- metric aggregation is permutation invariant;
- context/scope ratios are explicit `null` when no denominator exists.

No Git/filesystem diff discovery, telemetry, dashboard, lifecycle/store/CLI change, verification-authority change, or runtime dependency was added.
