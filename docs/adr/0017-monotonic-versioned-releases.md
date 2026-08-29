# ADR-0017 — Monotonic Versioned GitHub Releases

**Status:** Accepted

## Context

ADR-0016 intentionally bound the first public release to a one-off `v0.1.0` contract. The current release workflow therefore embeds `0.1.0`, `v0.1.0`, its distribution filenames, and its release-notes path. Specification 017 subsequently added a backward-compatible public authoring API/CLI on `main`, while the public release remains `v0.1.0`.

A later release must not achieve progression by rewriting the first release or by replacing one hard-coded version with another hard-coded one-off workflow. Historical releases are evidence anchors and need a fail-closed monotonic progression rule.

## Decision

1. GitHub tags/releases are append-only historical product identities under the repository contract. A later release MUST NOT retarget or mutate an earlier version.
2. Package metadata is the deterministic source for the current candidate version. The Git tag is `v<package-version>`, the public title is `SpecGrain v<package-version>`, distribution filenames are derived from that version, and release notes live at `docs/releases/v<package-version>.md`.
3. A release workflow may publish only from an exact successful CI result on canonical `main` and MUST bind every **new publication write** to that successful CI head SHA.
4. If the candidate version is already fully published, the existing tag target is a historical release-source anchor and is not required to equal a later successful `main` CI head. The workflow MUST instead verify that the tag and release both exist, the GitHub Release resolves to that same historical release identity, the release is public/non-draft/non-prerelease, and the exact expected asset set is present. An exact match exits successfully without mutation.
5. If the candidate version has not been published and neither candidate tag nor release exists, the workflow may create the tag at the bound successful CI head SHA and publish the corresponding GitHub Release with only the expected wheel and source distribution.
6. A release-without-tag or tag-without-release conflict is not silently repaired after publication intent becomes ambiguous; it fails closed for explicit recovery.
7. Before 1.0, a backward-compatible public feature addition advances the minor component. A release containing corrections only and no new public capability may advance the patch component. Breaking public-contract changes require separate shaping and explicit migration analysis rather than relying on pre-1.0 instability as permission.
8. GitHub Releases remain the only authorized binary distribution channel under this ADR. PyPI or another registry requires separate authority and credential/trust design.
9. Runtime dependency count remains zero unless a separately shaped requirement proves a dependency necessary.

## Consequences

- Specification 018 uses package version `0.2.0` and release tag `v0.2.0`.
- `v0.1.0` remains a historical immutable-by-contract anchor at `5eb46db0479cb8707afe070027dab4f3c558849a`.
- The release workflow becomes reusable for later shaped versions without weakening publication-time exact-SHA binding, asset verification, or historical release identity.
- A later `main` CI run with unchanged package version can idempotently verify the already-published release without incorrectly requiring its historical tag to move to the newer `main` SHA.
- Release workflow success is not itself proof that a release was newly published; closeout must inspect live tag/release truth and record whether publication or idempotent verification occurred.
