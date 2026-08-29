# Changelog

All notable public release changes are recorded here.

## Unreleased

### Added

- native root-DRAFT authoring through the public `create_draft_spec` API and `specgrain draft` CLI command, with deterministic local ID allocation and create-if-absent persistence;
- deterministic text/JSON creation output that reports DRAFT state and semantic revision without implying Grain readiness or execution authority.

### Changed

- the README quickstart now demonstrates `init -> draft -> check` on current `main` while distinguishing the published v0.1.0 command surface.

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
