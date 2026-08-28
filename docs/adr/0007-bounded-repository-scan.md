# ADR-0007: Repository Scan Is Bounded, Read-Only Fact Collection

**Status:** Accepted  
**Date:** 2026-08-28

## Context

Specification 007 introduces the first brownfield repository intelligence. The scanner must help later minimality/context decisions without becoming an unrestricted indexer, executing repository commands, following untrusted links, or pretending path/name heuristics are semantic understanding.

## Decision

Repository Scan v1 is a deterministic, read-only fact collector implemented with the Python standard library.

It MUST:

- operate on an existing ordinary directory, with or without `.specgrain/`;
- never execute repository commands or subprocesses;
- never follow filesystem symlinks;
- skip known generated/vendor/VCS/control directories;
- enforce explicit file-count/depth/manifest-size budgets and fail closed when a required budget is exceeded;
- expose only repository-relative paths in deterministic output;
- treat manifest-derived dependencies/components as signals, not proof that a capability is safe or reusable;
- read Git metadata only from an ordinary in-repository `.git/` directory and never follow external `gitdir:` indirection in v1.

## Scan classes

The scanner may report:

- top-level layout;
- recognized manifests and configuration files;
- language/file-extension counts;
- test-layout signals;
- component/module path signals;
- dependency/reuse signals extracted from bounded recognized manifests;
- ordinary Git HEAD/reference facts when safely available;
- skipped symlink count and scan-budget usage.

## Explicit non-claims

A scan does not prove:

- architecture intent;
- code ownership;
- semantic dependency correctness;
- API compatibility;
- whether a declared dependency should actually be reused;
- file-conflict safety;
- security of repository contents.

Later planning/verification layers may use scan facts as evidence but must not silently strengthen them into semantic truth.

## Consequences

- `specgrain scan` can work before initialization and without an LLM.
- Brownfield facts remain portable and reproducible.
- Very large repositories may require later configurable policies; v1 prefers explicit bounded failure over hidden partial scans.
- Worktree/submodule-style external Git metadata is reported as unsupported/indirect rather than followed across the repository boundary.
