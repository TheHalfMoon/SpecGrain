# Specification 018 Canonical Closeout

## Outcome

Specification 018 delivered and published the bounded `v0.2.0` authoring release without adding new SpecGrain product behavior beyond the already-verified Specification 017 native root-DRAFT surface.

The release generalized the first-release-only GitHub workflow into metadata-derived monotonic publication under ADR-0017 while preserving `v0.1.0` as an unchanged historical anchor.

## Shaping authority

Shaping PR #23 was documentation-only.

- canonical pre-shaping main: `d7c3f8e5734264824cd6ed1d8e931802a242c50a`;
- exact final shaping head: `68e830dc51d0df4bc521607be46ce9f11dc34acd`;
- exact-head shaping CI run: `33237175016` — success across the permanent five-cell matrix;
- submitted reviews: none;
- inline review threads: none;
- shaping merge: `b170aed92812c367282fbacb5d46e5acb450a196`;
- merge first parent: `d7c3f8e5734264824cd6ed1d8e931802a242c50a`;
- merge second parent: exact shaping head `68e830dc51d0df4bc521607be46ce9f11dc34acd`;
- merge used expected-head protection;
- canonical shaping post-merge CI run: `33245330017` — success.

Post-merge shaping job IDs:

- Ubuntu / Python 3.11: `99081695480`;
- macOS / Python 3.11: `99081695535`;
- Windows / Python 3.11: `99081695549`;
- Ubuntu / Python 3.12: `99081695589`;
- Ubuntu / Python 3.13: `99081695649`.

## Product implementation and review

Implementation branch `feat/018-v0.2.0-authoring-release` was created from exact canonical shaping merge `b170aed92812c367282fbacb5d46e5acb450a196`.

Implementation history:

- `22be323e4d73a310d6f89d4dd7cb27d7b09efd69` — initial bounded release implementation;
- `d6f5730daec6960e772e004630c8b4da1609e5b4` — forward repair to verify the metadata-derived GitHub Release title on the historical verification path;
- `bf63dbb4ef2259f79dc4e88e3b7f5abc0d05c178` — final exact reviewed head with focused release-contract guards and verification/review evidence.

No `src/specgrain/` product-behavior path changed in Specification 018.

The first repaired implementation head `d6f5730...` completed CI run `33245538486` successfully. Ubuntu/Python 3.11 recorded `531 passed`, successful Ruff/compile/CLI checks, successful `specgrain-0.2.0` wheel/sdist build, built-wheel reinstall, and installed CLI smoke.

Final exact PR-head push CI run `33245686864` completed successfully on `bf63dbb4ef2259f79dc4e88e3b7f5abc0d05c178` across all permanent jobs:

- Ubuntu / Python 3.13: `99082621664`;
- macOS / Python 3.11: `99082621794`;
- Windows / Python 3.11: `99082621796`;
- Ubuntu / Python 3.12: `99082621807`;
- Ubuntu / Python 3.11: `99082621853`.

PR #24 had no submitted reviews and no inline review threads at merge. Qodo reported review billing/trial blocking. CodeRabbit reported automatic review skipped because the repository had fewer than ten stars. Cubic produced an automated summary only. None of those conditions is treated as external approval or verification authority.

## Canonical product merge

PR #24 merged with expected-head protection on exact reviewed head `bf63dbb4ef2259f79dc4e88e3b7f5abc0d05c178`.

- canonical product merge: `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`;
- merge first parent: canonical shaping merge `b170aed92812c367282fbacb5d46e5acb450a196`;
- merge second parent: exact reviewed product head `bf63dbb4ef2259f79dc4e88e3b7f5abc0d05c178`;
- GitHub commit signature verification: verified;
- canonical post-merge CI run: `33245753969` — success on exact merge `baf00995...`.

Post-merge job IDs:

- Ubuntu / Python 3.12: `99082791641`;
- Ubuntu / Python 3.11: `99082791688`;
- Ubuntu / Python 3.13: `99082791696`;
- macOS / Python 3.11: `99082791786`;
- Windows / Python 3.11: `99082791812`.

## v0.2.0 publication evidence

Release workflow run `33245783948`, job `99082870129`, completed successfully from exact canonical product merge `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`.

The workflow log proves that it:

- checked out exact release source `baf00995...`;
- derived package version `0.2.0`;
- derived tag `v0.2.0`;
- derived title `SpecGrain v0.2.0`;
- derived notes path `docs/releases/v0.2.0.md`;
- built exactly `specgrain-0.2.0-py3-none-any.whl` and `specgrain-0.2.0.tar.gz`;
- created new tag `v0.2.0`;
- created the GitHub Release for `v0.2.0`.

Live GitHub tag truth:

- `refs/tags/v0.2.0` is a lightweight tag directly targeting commit `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`.

Live GitHub Release truth:

- Release ID: `378936896`;
- tag: `v0.2.0`;
- target: `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`;
- title: `SpecGrain v0.2.0`;
- draft: `false`;
- prerelease: `false`;
- published at: `2026-08-29T09:34:16Z`;
- GitHub API `immutable` field: `false`; SpecGrain therefore describes this release as **immutable-by-contract**, not as using a GitHub immutable-release feature.

Published assets:

1. `specgrain-0.2.0-py3-none-any.whl`
   - asset ID: `535032845`;
   - size: `66709` bytes;
   - SHA-256: `08b04328fd3896a19d3404928a582049887b0238b044e6e854b32769f132ab77`.
2. `specgrain-0.2.0.tar.gz`
   - asset ID: `535032844`;
   - size: `96850` bytes;
   - SHA-256: `0b8c4b02652c162649c7970904269be3038d04ce8604dbd7469e475b229c0bfd`.

Both asset download counts were `0` at closeout-audit time. That is an absence of adoption evidence, not a product-quality conclusion.

## Historical v0.1.0 preservation

Live GitHub confirms that Specification 018 did not mutate the first release:

- `refs/tags/v0.1.0` still targets `5eb46db0479cb8707afe070027dab4f3c558849a`;
- Release ID remains `378876694`;
- release target remains `5eb46db0479cb8707afe070027dab4f3c558849a`;
- title remains `SpecGrain v0.1.0`;
- draft/prerelease remain `false`/`false`;
- wheel remains `specgrain-0.1.0-py3-none-any.whl`, size `65542`, SHA-256 `61d4b0f81cac9fb0a3b347eb5ed740d71c61004e329ada5f9243b8c2a3a14a00`;
- sdist remains `specgrain-0.1.0.tar.gz`, size `93125`, SHA-256 `9864215c96406dd5e821fb3e53fba22e2ac5f8586941c5e384a4b5e43b9dfd0b`;
- no additional v0.1.0 release asset was introduced.

## Product boundary after release

v0.2.0 publicly exposes the root-DRAFT authoring path already completed in Specification 017. It does not add recursive child authoring, lifecycle mutation, Grain-readiness synthesis, executor/provider invocation, PyPI publication, a hosted service, runtime dependencies, or a benchmark winner claim.

The fresh post-v0.2 audit is recorded in `docs/research/post-v0.2-product-audit-2026-08-29.md`. It recommends native child-DRAFT authoring as the smallest next shaping candidate, but the audit is not successor authority and no Specification 019 is created by this closeout branch.

## Canonical closeout boundary

This file is authored on a documentation-only closeout branch from exact product merge `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`.

The closeout PR merge SHA is intentionally not fabricated here. Specification 018 may be called `CLOSED_CANONICAL` only after:

1. the exact closeout head containing this evidence completes required CI/review checks;
2. that exact head is merged with expected-head protection;
3. live GitHub confirms canonical `main` contains that exact closeout head as the merge second parent;
4. post-closeout canonical CI succeeds;
5. the generalized `Release` workflow, if triggered by that CI, successfully verifies the already-published `v0.2.0` historical release without moving or mutating it.
