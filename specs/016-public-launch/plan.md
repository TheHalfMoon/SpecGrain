# Plan 016 — Public Launch

## Authority

Follow `AGENTS.md`, `.specify/memory/constitution.md`, `docs/execution-master-plan.md`, ADR-0016, this specification, and live GitHub truth.

## Delivery slices

### A. Release foundation

- set package version and public metadata;
- add permanent cross-platform CI;
- add release/build verification without runtime dependencies.

### B. Truthful product onboarding

- replace stale foundation-phase README;
- add a runnable zero-to-verified example and test;
- include only current CLI/API behavior.

### C. Public proof and community surface

- add pinned brownfield examples;
- add Spec Kit migration guide;
- add benchmark report with explicit no-data/no-winner semantics where applicable;
- add contribution, security/trust, conduct, issue/PR templates, release notes, and a lightweight launch asset;
- link existing architecture/methodology/provenance documents instead of duplicating them.

### D. Verification and release

- run full test/Ruff/compile/help/build/install gates on the exact candidate;
- require successful Linux/macOS/Windows permanent CI on the exact PR head;
- review the exact diff for unsupported commands, fabricated evidence, benchmark claims, dependency creep, and security regressions;
- merge only with expected-head evidence;
- create `v0.1.0` tag and GitHub Release at the exact product merge commit;
- close the specification in a post-release documentation-only change with exact release evidence.

## Change surface

Expected product/release paths are limited to:

- `pyproject.toml`;
- `.github/workflows/ci.yml`;
- `.github/ISSUE_TEMPLATE/**` and `.github/pull_request_template.md`;
- `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`;
- `examples/**`;
- `docs/**` launch/migration/benchmark/release assets;
- `tests/test_launch.py`;
- `specs/015-specgrain-bench/tasks.md`;
- `specs/016-public-launch/**`;
- `specs/CURRENT.md` and program-state documentation.

Core source changes under `src/specgrain/**` are not expected. If launch verification reveals a real product defect, repair it in a bounded forward commit and record why the source change became necessary.
