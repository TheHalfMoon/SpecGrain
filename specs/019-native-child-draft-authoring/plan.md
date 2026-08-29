# Plan 019 — Native Child-DRAFT Authoring

## Authority

Follow `AGENTS.md`, `specs/CURRENT.md`, `.specify/memory/constitution.md`, `docs/execution-master-plan.md`, `docs/research/post-v0.2-product-audit-2026-08-29.md`, Specifications 001/002/003/005/017, ADR-0004, ADR-0005, ADR-0018, this specification, and live GitHub truth.

Implementation begins only after this exact shaping chain is merged canonically.

## Delivery slices

### A. Recoverable authoring transaction

- add one versioned internal journal under ignored `.specgrain/tmp/` runtime state;
- make ordinary store loading/writing fail closed while a pending journal exists;
- add explicit deterministic recovery that recognizes only no-write, child-only, or fully-completed exact states;
- keep reads free of automatic repair side effects;
- add same-directory temporary-file replacement for the one existing parent file while preserving exact-preimage checks;
- preserve the zero-runtime-dependency contract.

### B. Child-DRAFT authoring primitive

- add a public child-DRAFT operation sharing the existing deterministic ID allocator;
- require an existing `DRAFT` parent;
- construct the child with `parent_id` and the parent postimage with one reciprocal child ID;
- validate the entire proposed forest before the journal/canonical writes;
- execute journal -> child create-if-absent -> parent replace -> exact post-state confirmation -> journal removal;
- return explicit parent-before/parent-after/child revision information.

### C. CLI and documentation

- extend `specgrain draft` with optional `--parent` while keeping no-parent behavior unchanged;
- add `specgrain recover` with text and deterministic JSON output;
- update README quickstart/examples so recursion is demonstrated only through shipped DRAFT behavior;
- update architecture and Unreleased changelog without implying lifecycle progression or a new release.

### D. Verification and canonicalization

- add store tests for normal child/nested creation, state restriction, forest validation, collision handling, journal blocking, all safe recovery classifications, and ambiguous recovery refusal;
- add CLI tests for root compatibility, child text/JSON output, recovery text/JSON output, non-zero errors, and internal-error redaction;
- run exact regression/static/package gates through permanent cross-platform CI;
- review exact implementation diff for lifecycle authority, semantic overwrite, recovery safety, unsupported atomicity claims, dependency creep, and unrelated scope;
- merge only with expected-head protection;
- prove canonical post-merge CI, record exact evidence, and close 019 through a separate documentation-only PR;
- run a fresh post-019 product audit before shaping any successor.

## Expected change surface

Implementation is expected to remain within:

- `src/specgrain/store.py`;
- `src/specgrain/cli.py`;
- `src/specgrain/__init__.py`;
- `tests/test_store.py`;
- `tests/test_cli.py`;
- `README.md`;
- `docs/architecture.md`;
- `CHANGELOG.md`;
- `specs/019-native-child-draft-authoring/**`;
- `specs/CURRENT.md` and bounded program-frontier documentation during closeout.

`.gitignore` already excludes `.specgrain/tmp/`; no ignore-rule expansion is expected.

No SpecNode schema, lifecycle graph, readiness, dependency graph, WorkPacket, adapter, verifier, benchmark, release workflow, package version, or runtime dependency change is expected.
