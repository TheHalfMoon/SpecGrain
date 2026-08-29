# Tasks 018 — v0.2.0 Authoring Release

## Shaping

- [x] T001 Re-read canonical post-017 `main`, repository instructions, constitution, execution master plan, roadmap, post-017 audit, release ADR, package metadata, changelog, live release state, Actions, PRs, and issues.
- [x] T002 Confirm the public distribution gap: current `main` contains native DRAFT authoring while latest public release `v0.1.0` does not.
- [x] T003 Select `0.2.0` as the next backward-compatible feature-release identity and define monotonic post-v0.1 release progression in ADR-0017.
- [x] T004 Shape the bounded release outcome, exclusions, acceptance conditions, risks/recovery, expected change surface, and exact canonical starting revision.
- [ ] T005 Merge the exact shaping authority with successful exact-head CI/review evidence and re-read canonical `main` before implementation.

## Release implementation

- [ ] T006 Bump package/release metadata to `0.2.0` without adding runtime dependencies.
- [ ] T007 Promote Unreleased 017 authoring entries into the `0.2.0` changelog and add truthful `v0.2.0` release notes.
- [ ] T008 Update README/release-facing installation and version truth required for the new public release.
- [ ] T009 Replace the one-off hard-coded `v0.1.0` workflow with deterministic metadata-derived monotonic release progression that preserves historical releases.
- [ ] T010 Add/adjust deterministic tests and guards for version consistency, expected assets, release-note presence, exact-target binding, and historical-release conflict behavior where repository-local verification is practical.

## Product verification and merge

- [ ] T011 Run full regression, Ruff, compileall, CLI smoke, package build/install, release-contract guards, and the permanent five-cell CI matrix on the exact implementation head.
- [ ] T012 Review the exact diff for release mutation risk, source-SHA binding, version drift, dependency creep, external publishing scope, unsupported claims, and accidental product behavior changes.
- [ ] T013 Resolve every material exact-head finding with forward commits and re-prove the current head.
- [ ] T014 Merge the implementation PR only with expected-head protection and prove the exact product merge on canonical `main`.

## Publication and canonical closeout

- [ ] T015 Verify successful canonical post-merge CI on the exact product merge.
- [ ] T016 Verify the release workflow publishes or idempotently verifies `v0.2.0` at the exact product merge without mutating `v0.1.0`.
- [ ] T017 Record live tag/release identity, release ID/state, asset names/sizes/SHA-256 digests, and historical `v0.1.0` preservation evidence.
- [ ] T018 Re-audit the next product frontier from post-release repository/adoption truth.
- [ ] T019 Merge a documentation-only exact-evidence closeout PR with expected-head protection and prove post-closeout canonical CI before claiming `CLOSED_CANONICAL`.

Task checks in this shaping branch are planning-state records only. T005 and later work become executable only after the exact shaping authority is merged to canonical `main`.
