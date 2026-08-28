# Verification 015 — SpecGrainBench

## Exact product candidate

Product commit: `7548becacb65b890fdfafc3dc4789fee215172fd`.

```text
src/specgrain/benchmark.py        d118e7879691bd6b24541d37f84cd513903f95e5
tests/test_benchmark.py           73bf295f130539e1a3d23e652fc9e2a457b6d8c2
```

The implementation comparison from planning commit `a4882860ea9e21b43ea5b64cc1481acc69780ae1` changes exactly those two paths. The second implementation commit removes an unused import discovered during self-review before PR creation.

## Exact remote regression

Verification-only branch `verify/015-specgrain-bench` was forked from the exact product candidate and changed only `.github/workflows/verify-015.yml`, preserving product/test blob identities.

Successful verification commit: `7ce70d65c90b64fb3bd6f6250d8cf01d47666fab`.

GitHub Actions run `33196205039` completed with conclusion `success`. Job `98933857624` recorded:

- Install — PASS;
- Full regression (`python -m pytest -q`) — PASS;
- Ruff 015 surface — PASS;
- Ruff prior baseline diagnostic — PASS;
- Ruff full repository diagnostic — PASS;
- compileall — PASS;
- console/module entry-point parity — PASS;
- changed-line length inspection — PASS.

Two earlier diagnostic workflow runs showed non-stable failures in a broad Ruff invocation while the 015 changed surface and pytest regression were already passing. Run `33196205039` repeated the same byte-identical product/test state with explicit surface/baseline/full checks and all static gates passed. No product suppression or result filtering was introduced.

## Benchmark-integrity evidence

- v1 requires prompt-only, Spec Kit, and SpecGrain arms exactly once in the plan;
- every expected `(arm, repetition)` cell must be present exactly once;
- workspace and context/session identifiers must be unique across cells;
- repository baseline, scorer revision, method configuration, and controlled model configuration are checked;
- hidden scorer visibility invalidates comparison;
- failed and blocked runs remain in arm summaries;
- report output includes `automatic_winner: null` and does not rank methods;
- no agent/model/process/network execution is introduced.
