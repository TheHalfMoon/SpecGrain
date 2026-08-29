# Specification 020 — v0.3.0 Recursive Authoring Release

## Status

`SHAPED`

## Outcome

Publish the already-canonical native recursive DRAFT authoring and explicit recovery behavior as a new monotonic GitHub Release `v0.3.0`, binding first publication to the exact successful canonical `main` CI head while preserving historical `v0.1.0` and `v0.2.0` identities and making no new product-behavior change.

## Why this is the next frontier

Specification 019 is `CLOSED_CANONICAL` through closeout merge `3f8f3d825c3171a3a9ac7761ee5bc642e68a9d2d`, canonical post-closeout CI run `33248332725`, and historical-release no-mutation Release run `33248368659` / job `99089652500`.

Current canonical `main` includes the backward-compatible public behavior delivered by Specifications 017 and 019:

- root DRAFT authoring;
- child DRAFT authoring under an existing DRAFT parent;
- explicit recovery of exact supported interrupted authoring transactions.

Published `v0.2.0` predates the Specification 019 child/recovery surfaces. The fresh post-019 audit identifies this distribution discontinuity as the smallest current product gap.

ADR-0017 requires a backward-compatible public feature addition before 1.0 to advance the minor component. Therefore the shaped candidate is package version `0.3.0` / GitHub tag `v0.3.0`, not a patch release and never a mutation of `v0.2.0`.

## In scope

- change package metadata version from `0.2.0` to `0.3.0` while preserving Python support, license, build system, and zero runtime dependencies;
- add truthful `docs/releases/v0.3.0.md` release notes describing the already-delivered root/child DRAFT authoring and explicit recovery boundaries;
- promote the current Unreleased child-authoring/recovery changelog content into a dated `[0.3.0]` section and restore an empty Unreleased boundary;
- update README release/install truth so `v0.3.0` is the candidate current release after publication and no unreleased command is represented as part of an older release;
- update release/launch contract tests for version `0.3.0`, release-note presence, current release truth, and preservation of generalized monotonic release automation;
- preserve the existing generalized Release workflow unchanged unless an exact implementation finding proves a correction is required;
- run the permanent five-cell CI matrix on the exact implementation PR head before merge;
- merge only with expected-head protection;
- require canonical post-merge CI success on the exact product merge before first publication is accepted;
- require the Release workflow to create new lightweight tag `v0.3.0` at the exact successful canonical `main` CI head and publish one public/non-draft/non-prerelease GitHub Release titled `SpecGrain v0.3.0`;
- require exactly the expected `specgrain-0.3.0-py3-none-any.whl` and `specgrain-0.3.0.tar.gz` assets;
- inspect and record live tag target, release ID/state, asset IDs/sizes/digests, and preservation of historical `v0.1.0` / `v0.2.0` tags/releases;
- close through a separate documentation-only exact-head PR and fresh post-v0.3 audit.

## Out of scope

- any change to `src/specgrain/` product behavior merely to justify this release;
- lifecycle transition mutation, broad `refine`, automatic state progression, or generic DRAFT editing;
- changes to ADR-0018 child-authoring/recovery semantics or stronger multi-writer guarantees;
- readiness synthesis, Grain promotion, dependency scheduling changes, WorkPacket/executor/provider behavior, or verification-authority changes;
- PyPI or any registry other than GitHub Releases;
- signing/notarization/SBOM/provenance infrastructure not already required by the repository contract;
- runtime dependency additions;
- hosted services, networking, telemetry, dashboards, accounts, or provider lock-in;
- empirical benchmark execution or competitive superiority claims;
- retargeting, editing, deleting, or re-uploading assets to historical `v0.1.0` or `v0.2.0` releases.

## Release contract

ADR-0017 remains the governing release architecture.

For first publication of `0.3.0`:

1. package metadata is the candidate-version source;
2. expected tag/title/assets/notes are derived as `v0.3.0`, `SpecGrain v0.3.0`, the versioned wheel/sdist, and `docs/releases/v0.3.0.md`;
3. implementation PR exact-head CI must succeed before merge;
4. expected-head merge creates the candidate canonical product source;
5. canonical CI on that exact merge must succeed;
6. the Release workflow triggered from that successful canonical CI checks out the exact CI head SHA;
7. because neither `v0.3.0` tag nor release should exist before first publication, the workflow creates the new tag at that exact head and publishes exactly the two expected assets using the release notes;
8. live GitHub truth is re-read before `RELEASED` or equivalent is claimed.

If a tag-only/release-only state appears, publication fails closed under ADR-0017. Historical `v0.1.0` and `v0.2.0` are never rewritten to repair a new-version problem.

After first publication, later successful `main` CI heads with package version still `0.3.0` may only verify the existing historical release identity/assets and exit without mutation.

## Acceptance conditions

1. `pyproject.toml` candidate version is exactly `0.3.0`; runtime dependencies remain `[]` and supported Python/build/license metadata is otherwise unchanged unless an independently required correction is explicitly reviewed.
2. No `src/specgrain/` file changes in the release implementation PR.
3. `docs/releases/v0.3.0.md` exists before any canonical CI can trigger first publication and truthfully describes only already-canonical behavior.
4. `CHANGELOG.md` has an empty `Unreleased` section followed by `[0.3.0] — 2026-08-29` containing the child-DRAFT/recovery changes previously recorded as Unreleased.
5. README installation/release text points to `refs/tags/v0.3.0.zip` and distinguishes the published v0.3.0 surface from future unreleased work without overclaiming lifecycle/readiness/execution authority.
6. Launch/release contract tests bind `0.3.0`, the v0.3.0 release-note path, and current README/changelog release truth while retaining assertions that the Release workflow is metadata-derived, monotonic, and contains no hard-coded historical version.
7. Full regression, Ruff, compileall, CLI help parity, package build/install, and the permanent Ubuntu 3.11/3.12/3.13, macOS 3.11, Windows 3.11 matrix succeed on the exact implementation PR head.
8. Exact diff/review confirms no product behavior, lifecycle authority, runtime dependency, PyPI path, historical release mutation, or unrelated scope.
9. Product merge uses expected-head protection against the exact reviewed/CI-proven final PR head.
10. Canonical post-merge CI succeeds on the exact product merge before first publication is accepted.
11. First-publication Release workflow succeeds from that exact canonical CI head and live `refs/tags/v0.3.0` targets the exact product merge / successful canonical CI head.
12. Live GitHub Release `v0.3.0` is public, non-draft, non-prerelease, titled `SpecGrain v0.3.0`, and contains exactly the expected wheel and sdist.
13. Asset names, IDs, sizes, and GitHub-provided SHA-256 digests are recorded from live truth after publication.
14. Live `v0.1.0` and `v0.2.0` tag targets, release identities, and expected asset sets remain unchanged.
15. No PyPI publication or additional binary distribution channel occurs.
16. Specification 020 becomes `CLOSED_CANONICAL` only through a bounded documentation-only closeout PR whose exact head passes required CI/review, merges with expected-head protection, canonical post-closeout CI succeeds, and post-closeout Release verification confirms historical `v0.3.0` without mutation.

## Dependencies

- Specifications 000 through 019 are `CLOSED_CANONICAL` by live repository truth.
- Specification 019 closeout merge: `3f8f3d825c3171a3a9ac7761ee5bc642e68a9d2d`.
- Specification 019 post-closeout CI: `33248332725` — success across all five permanent jobs.
- Specification 019 post-closeout Release verification: `33248368659`, job `99089652500` — success; historical `v0.2.0` remained at `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85` without mutation.
- `docs/research/post-019-product-audit-2026-08-29.md` supplies frontier evidence only.
- ADR-0017 supplies monotonic version/release semantics and requires a pre-1.0 minor bump for backward-compatible public features.
- ADR-0018 supplies the already-delivered child-authoring/recovery boundary that this release publishes without changing.
- The generalized `.github/workflows/release.yml` delivered by Specification 018 is the existing publication mechanism.

## Risks and recovery

- **Wrong version class:** ADR-0017 requires minor progression for the new backward-compatible public capability, so candidate is `0.3.0`; tests bind the metadata.
- **Publishing before release notes exist:** release metadata resolution requires the derived notes file; implementation must add it before merge.
- **Historical release mutation:** workflow and exact review forbid force-tagging, release editing, asset upload mutation, or retargeting old versions; live history is reverified after publication.
- **Partial new-version publication:** tag-only or release-only state fails closed under ADR-0017; no automatic repair rewrites historical identity.
- **Accidental product change disguised as release work:** `src/specgrain/` is outside the expected implementation change surface and exact diff review must reject behavior changes.
- **Overclaiming adoption or benchmark value:** release notes describe shipped capability only; zero stars/forks/download evidence is not interpreted as success or failure.

## Constitution and architecture

No constitution amendment or new ADR is required. Specification 020 uses the accepted monotonic release architecture rather than introducing a new distribution mechanism. It improves availability of already-proven recursive authoring while preserving deterministic authority, reversibility, vendor neutrality, and evidence-first claims.

This shaped status is prospective on its documentation-only branch. Implementation authority exists only after the exact shaping head is merged canonically and canonical `main` is re-read.
