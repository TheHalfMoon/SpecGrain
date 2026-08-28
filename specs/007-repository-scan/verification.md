# Verification 007 — Repository Scan

**Verification date:** 2026-08-28  
**Environment:** Python `3.13.5`, pytest `9.0.2`  
**Exact verified product head:** `20d36002720fe5c7183e8e7defd02451c134516f`

## Exact uploaded bytes

The locally verified implementation/test bytes match the GitHub blobs at the exact product head:

```text
src/specgrain/repository.py      20d6068a53965c776b7eddd359fbdeb9960b15c8
src/specgrain/cli.py             93614f13c01cc70cfb55c0dd2e9e1dda463c09cb
src/specgrain/__init__.py        2bcff16c1db87a564a96f45054d233f4646f0b10
tests/test_repository.py         4ce1600e1d1fe126f5e4e04a9639fbef649bc8a9
tests/test_repository_cli.py     5f6922be235b2c746a6e6ce813d5a7d5c2b4b95b
```

The net diff from the 007 planning head `b720b321510204eb463602e418dbef7fc65a077d` to the exact product head contains only those five planned files.

## Pytest

```text
python -m pytest -q
........................................................................ [ 23%]
........................................................................ [ 47%]
........................................................................ [ 71%]
........................................................................ [ 94%]
................                                                         [100%]
```

Result: **304 passed**.

This is the 275-test Specification 001–006 baseline plus 29 Specification 007 tests.

The new tests cover traversal determinism, root validation, ignore rules, symlink non-following, file/depth/manifest limits, broad manifest detection, bounded dependency extraction, strict JSON/TOML/go.mod failures, language/test/config/component signals, ordinary/indirect/absent Git layouts, digest stability/change sensitivity, no repository mutation, no absolute-path/timestamp leakage, and CLI text/JSON/error behavior.

## Compile check

```text
python -m compileall -q src tests
```

Result: **PASS**.

## Packaging / entry-point checks

```text
python -m pip install -e . --no-build-isolation -q
specgrain --help
python -m specgrain --help
```

Result: **PASS**. Console and module help outputs are identical and include `scan`.

## Style preflight

Changed source/tests were checked for lines longer than 100 characters.

Result: **0 long lines**.

`ruff` is unavailable in the execution environment. Ruff is therefore **NOT RUN**, not PASS.

## Bounded-read review repair

Exact-diff review found that the first uploaded implementation checked manifest/Git file size before using an unbounded text read. That left a file-growth window inconsistent with the plan requirement to read at most the configured byte budget.

The exact verified product head repairs this by reading binary data with `limit + 1`, rejecting over-budget manifests with `MANIFEST_TOO_LARGE`, bounding Git metadata reads similarly, and decoding UTF-8 only after the bounded read. Full verification above was repeated after the repair.

## Scope verification

The final net implementation adds only:

- deterministic bounded repository facts and digest;
- lexical traversal with ignored control/vendor/generated directories and no symlink following;
- bounded selected-manifest parsing and dependency signals;
- conservative language/test/config/component signals;
- bounded in-repository Git metadata parsing without `git` or subprocesses;
- standalone `specgrain scan` CLI integration and public exports;
- focused tests.

It adds no AST/semantic indexing, embeddings, vulnerability/package resolution, arbitrary repository-content indexing, context selection, lifecycle mutation, dependency-scheduler changes, evidence semantics, agent/provider execution, subprocesses, or third-party runtime dependency.
