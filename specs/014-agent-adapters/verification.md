# Verification 014 — Agent Adapters

## Exact product candidate

Product commit: `e48c0e07f1c9d135e378ff3ca367a9db088c3ec8`

```text
src/specgrain/adapter.py          81d134e9078d05474a74bceb78f256f839a89d0d
tests/test_adapter.py             3a6bbb9a4f7fa9b2967bb7cac15cd45bf3a6fb28
```

GitHub path verification confirmed those exact blob identities at the product commit.

## Exact remote regression

A verification-only branch was created from the exact product commit and changed only `.github/workflows/verify-014.yml`; therefore the product and test blobs remained byte-identical.

Successful verification commit: `4cbec602e522384839a300e30953c2c50c2e9076`.

GitHub Actions run `33195455173` completed with conclusion `success`. Job `98931307401` recorded:

- Install — PASS;
- Full regression (`python -m pytest -q`) — PASS;
- Ruff 014 surface — PASS;
- Ruff full repository diagnostic — PASS;
- compileall — PASS;
- console/module entry-point parity — PASS;
- changed-line length inspection — PASS.

The new focused test file contains 13 adapter tests. The prior canonical 013 candidate had 480 tests; this record does not invent a combined collection count that is not exposed by the retrieved run metadata.

## Boundary evidence

- implementation comparison from planning commit `d55076aff8b3cff62f1ecd86d2742273524a4091` to product commit changes exactly `adapter.py` and `test_adapter.py`;
- external payloads cannot supply packet/result digests or verification authority;
- packet binding is injected from the canonical WorkPacket by the adapter;
- JSON duplicate keys and non-finite constants fail closed;
- no agent, subprocess, network, credential, provider SDK, lifecycle, store, verification-authority, or runtime dependency behavior is introduced;
- vendor-specific adapters remain deferred until real adoption demand exists.
