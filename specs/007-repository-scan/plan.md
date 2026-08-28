# Plan 007 — Repository Scan

## Strategy

Add one dependency-free `specgrain.repository` module and a thin `scan` CLI surface. Scan repositories as untrusted data, collect bounded facts only, and keep semantic/context decisions for later specifications.

## Planned source surface

```text
src/specgrain/repository.py
src/specgrain/cli.py
src/specgrain/__init__.py
tests/test_repository.py
tests/test_repository_cli.py
```

No changes are planned for schema, lifecycle, readiness, dependency, persistence, or project orchestration modules.

## Traversal

Use `os.scandir`/`pathlib` without recursive symlink following. Sort names before processing. Track relative POSIX paths, depth, regular-file count, and skipped symlink count.

Skip known generated/vendor/control directories before descending. Fail closed when a regular file is encountered beyond the depth budget or when file count exceeds the budget.

## Normalized map and digest

All public records are frozen/slotted. `RepositoryMap.to_dict()` emits stable JSON-compatible primitives in canonical sorted order. `content_digest` is SHA-256 over compact UTF-8 JSON of normalized map content excluding the digest field.

No timestamps, mtimes, inode values, absolute paths, usernames, or host facts participate.

## Manifest parsing

Detect broad manifest names but semantically parse only bounded formats needed for reuse signals:

- TOML via `tomllib` for pyproject/Cargo;
- JSON via a duplicate-key/non-finite rejecting helper for package.json;
- bounded line parser for go.mod.

Read at most `max_manifest_bytes`; fail when a manifest selected for semantic parsing exceeds the limit.

## Git metadata

Never call `git`. Treat `.git` as control metadata, not normal scan content.

- ordinary directory: inspect bounded HEAD/loose ref/packed-refs;
- regular file: report indirect layout, do not follow `gitdir:` target;
- symlink: never follow; report indirect/untrusted layout without commit resolution.

## CLI

Add `scan` independently from `.specgrain` project commands. CLI only invokes `scan_repository` and renders result/error.

## Verification

Cover traversal determinism, ignore lists, symlink non-following, all limits, manifests and invalid manifests, dependency extraction, language/test/config/component signals, Git layouts, digest stability/change sensitivity, no absolute paths/timestamps, no mutation, and CLI text/JSON/error behavior.

Run all 001–007 tests, compileall, editable install, console/module smoke, and available lint/static checks.

## Scope review

Confirm no AST/semantic indexing, subprocess, embeddings, vulnerability resolution, context selection, state mutation, evidence semantics, dependency-scheduler changes, or third-party runtime dependency.
