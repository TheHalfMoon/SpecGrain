# Plan 020 — v0.3.0 Recursive Authoring Release

## Authority

Follow `AGENTS.md`, `specs/CURRENT.md`, `.specify/memory/constitution.md`, `docs/execution-master-plan.md`, `docs/research/post-019-product-audit-2026-08-29.md`, ADR-0017, ADR-0018, Specification 019 closeout evidence, this specification, and live GitHub truth.

Implementation begins only after this exact shaping chain is merged canonically and canonical shaping post-merge CI succeeds.

## Delivery slices

### A. Versioned release metadata

- set package version to `0.3.0` and preserve zero runtime dependencies;
- add `docs/releases/v0.3.0.md` before first-publication eligibility;
- promote current Unreleased recursive-authoring/recovery changelog entries into the dated v0.3.0 section and restore the empty Unreleased boundary;
- update README current-release/install truth to v0.3.0 without implying lifecycle/readiness/execution capability that is not shipped.

### B. Release contract verification

- update release/launch tests for version `0.3.0`, v0.3.0 notes, changelog ordering, README tag URL, and current CLI truth;
- preserve tests proving metadata-derived Release automation, historical-release monotonicity, exact asset-set verification, and absence of force/edit/re-upload paths;
- do not modify the Release workflow unless an exact failing contract exposes a required bounded correction.

### C. Exact-head product canonicalization and publication

- run full permanent CI on the exact release implementation head;
- review the exact diff and reject any `src/specgrain/`, runtime-dependency, PyPI, historical-release, lifecycle, or unrelated behavior change;
- merge only with expected-head protection;
- prove canonical post-merge CI on the exact product merge;
- inspect the Release workflow first-publication run and prove that it checked out the exact successful canonical CI head before creating `v0.3.0`;
- verify live tag/release state and exact asset IDs/sizes/digests;
- reverify historical v0.1.0 and v0.2.0 identities/assets unchanged.

### D. Closeout

- record exact implementation, review, merge, canonical CI, publication, tag, release, asset, and historical-preservation evidence;
- run a fresh post-v0.3 product audit from the exact release source;
- close Specification 020 through a separate documentation-only exact-head PR, expected-head merge, canonical post-closeout CI, and no-mutation Release verification;
- shape no successor until the fresh audit and closeout are canonical.

## Expected change surface

Implementation is expected to remain within:

- `pyproject.toml`;
- `CHANGELOG.md`;
- `README.md`;
- `docs/releases/v0.3.0.md`;
- `tests/test_launch.py`;
- `tests/test_release_contract.py` only if existing release-contract assertions require a v0.3-specific update;
- `specs/020-v0.3.0-recursive-authoring-release/**`;
- `specs/CURRENT.md` for active-state/evidence reconciliation.

No `src/specgrain/`, SpecNode schema, lifecycle/refinement/readiness/dependency/packet/verification behavior, runtime dependency, PyPI configuration, Release workflow, benchmark dataset, hosted surface, or provider integration change is expected.
