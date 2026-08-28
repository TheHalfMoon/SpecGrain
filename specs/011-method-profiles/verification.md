# Verification 011 — Method Profiles

## Exact product state

Exact implementation commit:

`48626e69c155f08710337c2c7605d05c2eb9ff3a`

Exact uploaded product/test blobs:

```text
src/specgrain/method.py          32d03bd815751cd654af26a6b2bdbd9fb7c152e1
src/specgrain/__init__.py        5f4478764a30abb65b88ed1fc95d58033da84047
tests/test_method.py             0b01d1a1ce332759654cf5eb90183c2e5454e332
```

The exact implementation diff from planning head `024f5de0d72670f2e189ebaf3b00716f7a2b25bb` contains only those three files.

## Regression

- `pytest -q`: 448 passed.
- `python -m compileall -q src tests`: PASS.
- Editable install with the already-installed build environment: `python -m pip install -e . --no-build-isolation`: PASS.
- Plain build-isolated editable install could not resolve `setuptools>=68` because the execution environment had no DNS/network access; this is an environment availability result, not a product PASS.
- Installed console/module `--help` parity: PASS.
- Changed implementation/test lines over 100 characters: 0.
- Ruff: NOT RUN because unavailable.

## Behavioral evidence

- `quick` adds no method-specific metadata/evidence ceremony.
- `dmaic-lite`, `dmadv-lite`, `experiment`, and `controlled` require only bounded method metadata plus stable evidence identifiers.
- Method-aware readiness composes the existing 004 Grain-readiness report rather than modifying its semantics.
- Method-required evidence reuses `SpecNode.evidence.required`, so 009 transports it and 010 independently verifies it.

No lifecycle mutation, store change, CLI change, provider/model logic, executor invocation, or runtime dependency is introduced.
