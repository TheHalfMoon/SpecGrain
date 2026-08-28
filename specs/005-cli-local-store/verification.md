# Verification 005 — CLI and Local Store

**Verification date:** 2026-08-28  
**Environment:** Python `3.13.5`

## Pytest

The exact candidate source and tests in the local reconstructed workspace were exercised with the canonical 001–004 kernel.

```text
python -m pytest -q
........................................................................ [ 31%]
........................................................................ [ 62%]
........................................................................ [ 93%]
..............                                                           [100%]
```

Result: **230 passed**.

This is 182 pre-existing 001–004 tests plus 48 new 005 store/CLI tests.

## Compile check

```text
python -m compileall -q src tests
```

Result: **PASS**.

## Packaging / entry-point checks

```text
python -m pip install -e . --no-build-isolation
specgrain --help
python -m specgrain --help
```

Result: **PASS**.

Both installed console and module entry points expose exactly `init` and `check`.

## Product smoke

A fresh temporary directory was exercised through the installed console entry point:

```text
specgrain init /tmp/sg005-smoke --project-id smoke
specgrain check /tmp/sg005-smoke
specgrain check /tmp/sg005-smoke --json
python -m specgrain check /tmp/sg005-smoke --json
```

Results:

- initialization PASS;
- text check PASS;
- console JSON check PASS;
- module JSON check PASS;
- console/module JSON payloads matched and contained no timestamp or absolute-path fields.

## Style preflight

A local line-length preflight found **0 lines over 100 characters** in:

- `src/specgrain/store.py`;
- `src/specgrain/cli.py`;
- `tests/test_store.py`;
- `tests/test_cli.py`.

## Ruff

```text
python -m ruff check .
```

Result: **NOT RUN — `ruff` is not installed in the execution environment**.

An installation attempt could not reach the Python package index because the environment has no DNS/network access. This is not reported as PASS.

## Scope verification

005 adds only:

- dependency-free JSON local-store primitives;
- `init` and read-only `check` CLI surfaces;
- package/module entry points;
- store/CLI tests and bounded public exports.

It does not add dependency-DAG algorithms, repository scanning, lifecycle mutation, evidence-ledger storage, YAML parsing, subprocess execution, provider/agent integration, or a generic spec mutation API.
