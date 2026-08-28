# Specification 007 — Repository Scan

**Status:** SHAPED  
**Type:** implementation  
**Created:** 2026-08-28  
**Depends on:** `006-dependency-graph` (`CLOSED_CANONICAL`)

## Problem

SpecGrain can validate local specifications and dependencies but cannot yet describe the brownfield repository in which a Grain will be implemented. Without deterministic repository facts, minimality and context decisions risk depending on giant prompts, agent memory, or speculative new abstractions.

## Outcome

Implement a bounded deterministic repository scanner plus `specgrain scan [PATH] [--json]`. It reports compact repository facts from layout, recognized manifests/config/tests, language extensions, component/dependency signals, and safe in-repository Git metadata without executing repository code or sending content to an LLM.

## Public model

### `ScanLimits`

Frozen/slotted limits:

- `max_files` (default `20_000`);
- `max_depth` (default `12`);
- `max_manifest_bytes` (default `1_048_576`).

All values must be positive integers and bool is invalid.

### `RepositoryManifest`

- `path`;
- `kind`;
- `size_bytes`.

### `LanguageSignal`

- `language`;
- `file_count`.

### `DependencySignal`

- `ecosystem`;
- `name`;
- `source_path`.

A dependency signal means only that a recognized manifest declares the name.

### `ComponentSignal`

- `kind` (`top-level`, `src-module`, `package`, `app`, `service`, `crate`);
- `name`;
- repository-relative `path`.

### `GitFacts`

- `present`;
- `layout`: `none | ordinary | indirect`;
- optional `head_ref`;
- optional `head_commit`.

### `RepositoryMap`

Immutable scan result containing at least:

- `scan_version=1`;
- repository basename only;
- total scanned regular-file count;
- skipped symlink count;
- deterministic top-level entries;
- recognized manifests;
- recognized config paths;
- recognized test paths/directories;
- language counts;
- dependency signals;
- component signals;
- Git facts;
- stable `content_digest` over normalized map content excluding the digest itself.

Expose deterministic `to_dict()`.

### Errors

`RepositoryScanError` carries stable code + repository-relative location/message where applicable.

Required codes include:

- `ROOT_INVALID`;
- `SCAN_FILE_LIMIT`;
- `SCAN_DEPTH_LIMIT`;
- `MANIFEST_TOO_LARGE`;
- `MANIFEST_INVALID`.

## Root and traversal safety

- root must exist, be a directory, and not be a symlink;
- scanner MUST NOT follow symlink files or directories;
- symlinks are counted and skipped;
- traversal order is lexical by repository-relative path;
- ignore directory names at minimum: `.git`, `.specgrain`, `node_modules`, `.venv`, `venv`, `target`, `dist`, `build`, `.next`, `.cache`, `coverage`, `__pycache__`;
- max depth is measured from root children as depth 1;
- encountering a regular file beyond `max_depth` or exceeding `max_files` fails closed rather than silently returning a partial map.

## Manifest detection

Recognize exact/structured names including:

- `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements*.txt`;
- `package.json` and common JS lockfiles;
- `Cargo.toml`, `Cargo.lock`;
- `go.mod`, `go.sum`;
- `pom.xml`, `build.gradle`, `build.gradle.kts`;
- `Gemfile`;
- `composer.json`;
- solution/project files such as `*.sln`, `*.csproj`.

Manifest recognition is path/name evidence, not proof the ecosystem is currently active.

## Dependency/reuse signals

V1 extracts dependency names only from bounded recognized formats that can be safely parsed with the standard library:

- `pyproject.toml` using `tomllib`: `[project].dependencies`, `[project.optional-dependencies]`, and dependency tables under `[tool.poetry.dependencies]` when present;
- `package.json`: `dependencies`, `devDependencies`, `peerDependencies`, `optionalDependencies` object keys;
- `Cargo.toml` using `tomllib`: `dependencies`, `dev-dependencies`, `build-dependencies` table keys;
- `go.mod`: module names from direct `require` directives/blocks using bounded text parsing.

Do not parse arbitrary build scripts. Invalid recognized manifests fail with `MANIFEST_INVALID` only when the scanner attempts semantic extraction from that manifest.

Dependency names are unique by `(ecosystem, name, source_path)` and sorted deterministically.

## Language signals

Count regular files by a small explicit extension map, including Python, JavaScript, TypeScript, Rust, Go, Java, Kotlin, C/C++, C#, Ruby, PHP, Swift, Shell, SQL, and Markdown.

Unknown extensions remain included in total file count but are not assigned a guessed language.

## Test/config signals

Report deterministic relative paths for known test directories/files and config/automation signals. Examples:

- `tests`, `test`, `__tests__`;
- `test_*.py`, `*_test.py`, `*_test.go`, `*.test.*`, `*.spec.*`;
- `.github/workflows`, `Dockerfile`, compose files, `Makefile`, `justfile`, `tox.ini`, `pytest.ini`, `ruff.toml`, `mypy.ini`, `tsconfig.json`, `.pre-commit-config.yaml`.

The scanner does not execute tests or configuration.

## Component signals

Generate conservative path-based component signals only:

- ordinary top-level directories not ignored;
- direct child directories under `src/`, `packages/`, `apps/`, `services/`, `crates/`.

No semantic naming or architecture inference is allowed in 007.

## Git facts

- absent `.git` => `layout=none`, `present=false`;
- ordinary `.git/` directory => `layout=ordinary`, `present=true`;
- `.git` regular file => `layout=indirect`, `present=true`; do not follow its target;
- symlink `.git` is skipped/rejected as untrusted metadata and must not be followed.

For ordinary layout, parse `.git/HEAD` only when it is an ordinary bounded text file. If symbolic, expose the ref and resolve a commit only from an ordinary in-repository loose ref or `packed-refs`. Detached 40-hex HEAD may be exposed as `head_commit`.

Do not run `git`.

## CLI

Add:

```text
specgrain scan [PATH] [--json]
```

PATH defaults to `.` and does not require `.specgrain/`.

Text output includes compact counts and signals. JSON uses deterministic normalized content and contains no absolute path, timestamp, username, hostname, or environment-specific temporary path.

Exit codes:

- `0` successful scan;
- `1` scan failure;
- argparse usage remains `2`.

## Explicit out of scope

- embeddings, semantic search, AST/call graph analysis;
- arbitrary file-content indexing;
- executing package managers/build/test/git commands;
- dependency vulnerability/version resolution;
- change-surface conflict proof;
- context selection/token accounting (`008`);
- modifying `.specgrain` state;
- AI-generated architecture descriptions.

## Acceptance criteria

1. scans an ordinary repository with no SpecGrain initialization.
2. output is deterministic across repeated scans when repository bytes/metadata are unchanged.
3. no symlink is followed.
4. vendor/generated/control directories are skipped.
5. file/depth/manifest budgets fail closed with stable errors.
6. manifest/config/test/language signals are deterministic and repository-relative.
7. bounded pyproject/package/Cargo/go dependency extraction produces sorted reuse signals.
8. invalid parsed manifests fail explicitly rather than being silently ignored.
9. component signals remain path-based and conservative.
10. ordinary/indirect/absent Git layouts are distinguished without running Git or following external gitdir targets.
11. map digest is stable for identical normalized facts.
12. `scan --json` contains no absolute paths/timestamps.
13. CLI and API never mutate repository contents.
14. Specifications 001–006 regressions remain green.

## Success criterion

SpecGrain can produce a compact, deterministic, bounded brownfield repository map that later Grain planning/context stages can cite as factual evidence without loading or executing the whole repository.
