# Specification 021 — Public Launch Readiness Hardening

## Status

`SHAPED`

## Outcome

Make the current public SpecGrain repository surface truthful, current, and professionally launch-ready by correcting stale support/launch documentation, improving first-screen README presentation, and adding bounded regression checks, without changing product behavior, package version, release identity, runtime dependencies, or distribution authority.

## Why this is the next frontier

Specification 020 is `CLOSED_CANONICAL`, v0.3.0 is published, and the program entered `POST_V0.3_OBSERVATION` with no pre-authorized successor.

A fresh maintainer launch-readiness request and `docs/research/public-launch-readiness-audit-2026-08-29.md` supply new evidence:

- `SECURITY.md` still advertises `0.1.x` as the supported release line after v0.3.0 publication;
- `docs/launch-strategy.md` still presents a `v0.1.0 launch demo` rather than the current versioned release;
- the README is accurate but can present release/Python/license trust signals more clearly at first glance;
- GitHub repository metadata has no description and no topics, and `main` has no branch protection/ruleset. These are platform-setting gaps that must not be misrepresented as file-backed changes.

The stale public documents are reproducible defects, and the explicit maintainer request is concrete user/adoption friction. This is sufficient fresh evidence under the post-v0.3 frontier rules to shape a narrow public-launch hardening specification.

## In scope

- preserve the existing product tagline while making the README opening consistently describe SpecGrain as an agent-neutral delivery control plane;
- add concise current-release, Python-version, CI, and MIT-license signals near the top of the README without implying unsupported capability;
- keep the stable v0.3.0 release installation path prominent and truthful;
- update `SECURITY.md` so the supported-version table reflects the current `0.3.x` release line and explicitly states the older-line policy;
- update `docs/launch-strategy.md` from the historical v0.1.0 launch demo to current v0.3.0 public-release guidance;
- add/adjust launch regression tests to require the root MIT license in the public surface, current security support text, and current launch-strategy version truth;
- preserve current `pyproject.toml` version `0.3.0`, MIT license metadata, package keywords, Python requirement, build backend, and zero runtime dependencies unchanged;
- preserve `.github/workflows/ci.yml` and `.github/workflows/release.yml` unchanged unless an exact verification finding proves a correction is required;
- run the permanent five-cell CI matrix on the exact implementation PR head;
- merge only with expected-head protection;
- verify canonical post-merge CI on the exact merge and confirm the Release workflow treats v0.3.0 as already published and performs no mutation;
- close through a separate documentation/status evidence change after exact canonical evidence exists.

## Platform metadata recorded but not file-backed

The public-launch audit records an exact recommended GitHub description, topic set, and minimal `main` ruleset target.

These are repository platform settings rather than committed files. Specification 021 may record their live state and recommendations, but it MUST NOT claim they were applied without live GitHub settings evidence. File-backed implementation can close independently while preserving these settings as explicit residual launch operations if the available repository interface cannot perform them.

## Out of scope

- any `src/specgrain/` behavior change;
- package version bump or new GitHub Release;
- edits to historical v0.1.0, v0.2.0, or v0.3.0 tags/releases/assets;
- package-registry publication, including PyPI;
- lifecycle mutation, broad `refine`, generic DRAFT editing, readiness synthesis, executor/provider behavior, or verification-authority expansion;
- runtime dependency additions;
- hosted service, docs website, accounts, telemetry, dashboards, or provider integration;
- empirical benchmark execution or superiority claims;
- speculative CodeQL/Dependabot/action-SHA hardening without separate security evidence;
- hidden mutation of GitHub repository settings that cannot be independently verified.

## Acceptance conditions

1. README retains `Big ideas. Small specs. Proven software.` and truthfully identifies SpecGrain as an open-source/local-first agent-neutral delivery control plane.
2. README first-screen presentation includes current CI, release, Python 3.11+, and MIT license signals and retains the stable `v0.3.0` install path.
3. README continues to advertise only the supported CLI and preserves explicit no-lifecycle-promotion/no-agent-runner/no-hosted-service trust boundaries.
4. `SECURITY.md` names `0.3.x` as the supported security-fix line and does not leave `0.1.x` presented as current support.
5. `docs/launch-strategy.md` presents v0.3.0 as the current public release and uses only currently shipped commands/surfaces.
6. Root `LICENSE` remains exact MIT text, GitHub continues to recognize MIT, and `pyproject.toml` license metadata remains `MIT` with `license-files = ["LICENSE"]`.
7. `pyproject.toml` version remains `0.3.0`, dependencies remain `[]`, existing package keywords remain unchanged, and no package/release identity drift is introduced.
8. Launch regression tests require `LICENSE`, current SECURITY version truth, current launch-strategy version truth, README release URL/current CLI boundaries, and existing public community files.
9. Full regression, Ruff, compileall, package build/install, CLI smoke, and permanent Ubuntu 3.11/3.12/3.13, macOS 3.11, Windows 3.11 CI succeed on the exact implementation PR head.
10. Exact diff review proves no product behavior, package version, runtime dependency, release workflow, PyPI, historical-release, benchmark, hosted, or unrelated scope change.
11. Product/documentation merge uses expected-head protection against the exact reviewed CI-proven head.
12. Canonical post-merge CI succeeds on the exact merge, and the subsequent Release workflow verifies historical v0.3.0 without mutation.
13. Closeout records live GitHub description/topics/branch-rule state separately from file-backed completion and does not claim external settings that are not proven live.
14. Specification 021 becomes `CLOSED_CANONICAL` only through a bounded closeout change, exact-head verification, expected-head merge, and canonical post-closeout CI/release verification.

## Dependencies

- Specifications 000 through 020 are `CLOSED_CANONICAL` by live repository truth.
- Canonical pre-021 `main`: `1ea1ee8554ce84f96f67d12eb86188324c81534a`.
- Published release: v0.3.0 / GitHub Release `378962445` sourced from `70dd66aba0e68ae710e6ef12605ed153d107bab4`.
- `docs/research/post-v0.3-product-audit-2026-08-29.md` established observation as the prior frontier and permits a later successor only from fresh evidence.
- `docs/research/public-launch-readiness-audit-2026-08-29.md` supplies the fresh evidence for this specification.
- ADR-0017 governs historical release immutability and no-mutation verification while package version remains 0.3.0.

## Risks and recovery

- **Marketing overreach:** README/launch wording may accidentally imply autonomous execution or lifecycle authority. Preserve existing explicit non-claims and use current shipped CLI only.
- **Release drift:** changing `pyproject.toml` at the same version could make canonical builds differ from historical v0.3.0. Therefore package metadata is outside the expected implementation change surface.
- **Security-policy ambiguity:** support-version text is a public promise. Keep the correction minimal and aligned with the existing latest-release-line policy rather than inventing long-term support commitments.
- **Platform-setting false claim:** repository description/topics/rulesets are not committed files. Record live state and never claim configuration without GitHub evidence.
- **Scope creep:** do not use launch polish as authority for new product features, hosted surfaces, package registries, security tooling, or benchmark claims.

## Constitution and architecture

No constitution amendment or new ADR is required. The change improves evidence/truthfulness and public usability while preserving the deterministic control plane, vendor neutrality, zero runtime dependencies, bounded scope, and evidence-over-assertion principles.

This shaped status is prospective on its documentation-only branch. Implementation authority exists only after this exact shaping chain is merged canonically and canonical shaping post-merge CI succeeds.
