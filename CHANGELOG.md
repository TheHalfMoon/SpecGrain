# Changelog

All notable public release changes are recorded here.

## Unreleased

_No changes recorded yet._

## [0.2.0] — 2026-08-29

Backward-compatible authoring release.

### Added

- native root-DRAFT authoring through the public `create_draft_spec` API and `specgrain draft` CLI command, with deterministic local ID allocation and create-if-absent persistence;
- deterministic text/JSON creation output that reports DRAFT state and semantic revision without implying Grain readiness or execution authority.

### Changed

- the README quickstart now demonstrates the public `init -> draft -> check` path;
- GitHub release automation now derives version, tag, distribution filenames, title, and release-note path from package metadata while preserving historical releases as immutable-by-contract anchors.

### Evidence boundary

v0.2.0 adds no recursive refinement, executor/provider invocation, PyPI distribution, runtime dependency, or empirical benchmark winner claim.

See [`docs/releases/v0.2.0.md`](docs/releases/v0.2.0.md) for detailed release notes.

## [0.1.0] — 2026-08-28

First public alpha release.

### Added

- recursive immutable SpecNode model and lifecycle/refinement validation;
- deterministic Grain readiness and dependency scheduling primitives;
- repository-local store plus `init`, `check`, and `next` CLI commands;
- bounded brownfield repository scan and context-budget accounting;
- portable WorkPacket/execution-result contracts and generic agent adapters;
- independent verification, append-oriented evidence, and `prove` CLI output;
- method profiles plus change-scope, drift, and delivery metrics;
- explicit read-only GitHub Spec Kit import reports;
- SpecGrainBench experiment ledger and contamination/comparability preflight;
- permanent Linux/macOS/Windows CI, runnable zero-to-verified example, migration guide, trust/security documentation, and launch assets.

### Evidence boundary

v0.1.0 publishes no empirical benchmark winner. The benchmark harness exists, but a controlled public multi-arm dataset has not yet been published.

See [`docs/releases/v0.1.0.md`](docs/releases/v0.1.0.md) for detailed release notes.
