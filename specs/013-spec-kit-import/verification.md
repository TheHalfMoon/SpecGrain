# Verification 013 — Spec Kit Import

## Exact product candidate

Implementation commit: `49817d5c99adb131125f8e3fc4f605cc6e42c0e3`

Exact implementation/test blobs:

```text
src/specgrain/speckit.py          4d1048723af296d178deaa2c23a51570df0c0100
src/specgrain/cli.py              6dd2437fe3490aa6153bed75966d52b5c46d699b
src/specgrain/__init__.py         ccee33cee4c28a1764e0a2fd500a40a30e5f9dcf
tests/test_speckit.py             3c9d8257723985b2c6c174788f70a0d994054c35
tests/test_speckit_cli.py         2f926b3189c7c1a24a884b28eb587612c0a154a5
```

GitHub object and path verification confirmed that the published implementation uses the same blob identities as the previously tested candidate.

## Regression evidence

The exact candidate above was exercised before publication with:

- `480 passed` across Specifications 001–013;
- `python -m compileall -q src tests` — PASS;
- editable installation using available local build dependencies with `--no-build-isolation` — PASS;
- console/module `--help` parity — PASS;
- changed implementation/test lines over 100 characters — 0;
- Ruff — NOT RUN because Ruff was unavailable.

This record does not claim a fresh rerun after the temporary local workspace was discarded; it binds the prior run to the exact Git blob identities published in the implementation commit.

## Boundary verification

- import is read-only and does not create or mutate `.specgrain`;
- supported artifact roles are limited to known Spec Kit basenames;
- local loading rejects symlinks/non-files, invalid UTF-8, and artifacts exceeding the configured hard byte ceiling;
- direct in-memory import enforces the same positive byte ceiling;
- unresolved feature names, unresolved independent tests, duplicate structured identifiers, duplicate artifact roles, and duplicate legacy task IDs fail closed;
- `tasks.md` remains `LegacyTask` migration evidence and is never promoted to core SpecGrain ontology;
- constitution bytes are digest-bound but policy adoption is never inferred;
- partial mapping of spec/plan content is made explicit through notices rather than silently discarded;
- no subprocess, Git command, network client, provider/model integration, or third-party runtime dependency is introduced.
