# Plan 018 — v0.2.0 Authoring Release

## Strategy

Treat 018 as a release/distribution Grain, not a feature-development container. The product capability to publish already exists on canonical `main`; implementation changes are limited to release identity, monotonic release automation, release-facing documentation, and deterministic verification of that boundary.

## Phase A — Canonical shaping

1. Bind the specification to canonical post-017 closeout revision `d7c3f8e5734264824cd6ed1d8e931802a242c50a`.
2. Record `0.2.0` as the backward-compatible feature release identity and accept ADR-0017 as the durable post-v0.1 release progression rule.
3. Merge this documentation-only authority before release implementation begins.

## Phase B — Release implementation

1. Bump package metadata to `0.2.0`.
2. Promote the current Unreleased authoring entries into a dated `0.2.0` changelog section while restoring a clean Unreleased section.
3. Add `docs/releases/v0.2.0.md` with exact capability and limitation language.
4. Update README/release-facing references only where current public-release truth requires it.
5. Generalize `.github/workflows/release.yml` so release identity is derived from package metadata and historical releases remain immutable-by-contract.
6. Add or adjust deterministic repository tests/guards for version/release consistency and historical-release safety without introducing runtime dependencies.

## Phase C — Exact-head verification and product merge

1. Run the permanent five-cell CI matrix on the exact implementation head.
2. Review the exact diff for historical release mutation, target binding, version drift, unsupported claims, external publishing scope, dependency drift, and accidental product feature additions.
3. Resolve every material finding with forward commits and re-prove the new exact head.
4. Merge only with expected-head protection.

## Phase D — Canonical publication evidence

1. Re-read canonical product merge and verify post-merge CI on the exact merge SHA.
2. Observe the release workflow triggered by that successful main CI; do not manually retarget historical tags or bypass the workflow contract.
3. Verify live `v0.2.0` tag target, release state, release ID, asset names, asset sizes, and asset SHA-256 digests.
4. Re-verify that `v0.1.0` still points to `5eb46db0479cb8707afe070027dab4f3c558849a` with its historical assets unchanged.

## Phase E — Canonical closeout and next-frontier audit

1. Record exact product PR, merge, CI, release-workflow, tag/release, asset-digest, and historical-release evidence.
2. Perform a fresh post-018 product audit from live repository/release/adoption truth.
3. Open a documentation-only closeout PR. Do not claim `CLOSED_CANONICAL` until its exact head is merged and post-closeout CI succeeds.
4. Do not automatically select recursive refinement or any other deferred idea; shape the next frontier from the fresh audit.

## Expected implementation change surface

Primary expected paths:

- `pyproject.toml`
- `.github/workflows/release.yml`
- `CHANGELOG.md`
- `README.md`
- `docs/releases/v0.2.0.md`
- release-contract tests or verification helpers under `tests/` if needed
- Specification 018 evidence files

No `src/specgrain/` change is expected unless exact verification reveals a release-blocking version-surface defect; such a change would require explicit scope reconciliation before implementation.

## Recovery

Before publication, revert the bounded implementation through ordinary forward history if release gates fail. After publication, never retarget or rewrite a published version; fix a defective published release with a newly shaped later version.
