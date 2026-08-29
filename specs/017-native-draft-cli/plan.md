# Plan 017 — Native DRAFT CLI

## Authority

Follow `AGENTS.md`, `.specify/memory/constitution.md`, `docs/execution-master-plan.md`, `docs/research/post-v0.1-product-audit-2026-08-29.md`, this specification, existing store/model contracts, and live GitHub truth.

## Delivery slices

### A. Deterministic authoring primitive

- add one public store function that validates the current local project;
- allocate the lowest unused canonical SpecNode ID;
- construct a root `DRAFT` through the existing `SpecNode` model;
- persist with create-if-absent semantics and never overwrite an existing spec.

### B. CLI surface

- add `specgrain draft` with required `--title` and `--outcome`, optional `--rationale`, local project path, and `--json`;
- keep output explicit about `DRAFT` state and semantic revision;
- fail closed on invalid store/input and unexpected internal exceptions.

### C. Adoption documentation

- update README one-minute start so a user creates a real native DRAFT before `check`;
- update CLI architecture text to distinguish shipped commands from still-deferred commands;
- add an Unreleased changelog entry without implying a release has occurred.

### D. Verification and canonicalization

- add store and CLI tests for deterministic allocation, output, validation, collision handling, and non-overwrite behavior;
- run full CI/static/package gates on the exact implementation head;
- review exact diff against 017 scope and trust boundaries;
- merge only with expected-head protection;
- record post-merge evidence and close 017 canonically only after canonical `main` CI succeeds.

## Expected change surface

Implementation is expected to remain within:

- `src/specgrain/store.py`;
- `src/specgrain/cli.py`;
- `src/specgrain/__init__.py`;
- `tests/test_store.py` and/or `tests/test_cli.py`;
- `README.md`;
- `docs/architecture.md`;
- `CHANGELOG.md`;
- `specs/017-native-draft-cli/**`;
- `specs/CURRENT.md` and bounded program-frontier documentation.

No dependency, benchmark, adapter, WorkPacket, verification-engine, repository-scanner, or release-workflow change is expected.
