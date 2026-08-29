# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Program status:** `POST_V0.1_ACTIVE`  
**Last closed specification:** `specs/019-native-child-draft-authoring/` — `CLOSED_CANONICAL` by live closure evidence  
**Active specification:** `specs/020-v0.3.0-recursive-authoring-release/` — prospective `SHAPED` pending exact shaping merge  
**Active branch:** `spec/020-v0.3.0-recursive-authoring-release`  
**Next planned specification:** none after 020  
**Published release:** `v0.2.0`  
**Published release source commit:** `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`  
**Published release ID:** `378936896`

## Specification 019 canonical closeout

Specification 019 product PR #27 merged with expected-head protection as canonical product merge `d6727b6c5cdafcf6265b6d999418c0fe853249a7`; canonical product CI `33248014390` succeeded and Release verification `33248070688` preserved historical `v0.2.0` without mutation.

Documentation-only closeout PR #28 exact head `f83e0ed27fbb0e73c31804cc77a76643a0457b33` completed exact-head CI `33248240870` successfully and merged with expected-head protection as `3f8f3d825c3171a3a9ac7761ee5bc642e68a9d2d`. The merge second parent is the exact closeout head and GitHub signature verification is valid.

Canonical post-closeout CI `33248332725` completed successfully across the permanent five-cell matrix on exact closeout merge `3f8f3d8...`. Release workflow `33248368659`, job `99089652500`, checked out that exact closeout merge and recorded that `v0.2.0` was already published at historical tag target `baf00995...`; no release mutation was required.

Therefore Specification 019 is `CLOSED_CANONICAL` by the live conditions declared in its closeout contract.

## Specification 020 shaping frontier

The canonical fresh audit `docs/research/post-019-product-audit-2026-08-29.md` identifies a distribution discontinuity: current canonical `main` ships verified root/child DRAFT authoring and explicit recovery, while published `v0.2.0` predates the child/recovery surfaces.

ADR-0017 requires a backward-compatible public feature addition before 1.0 to advance the minor version. 020 therefore shapes a bounded `v0.3.0` GitHub Release that publishes existing canonical behavior without changing `src/specgrain/` product behavior.

Shaped implementation scope is package version/release notes/changelog/README/release-contract tests plus exact CI, expected-head merge, first-publication evidence, historical release preservation, and documentation-only closeout. It does not authorize lifecycle/edit/refine behavior, PyPI, new runtime dependencies, hosted/provider behavior, or benchmark claims.

## Authority rule

This branch is shaping only. Specification 020 implementation is not authorized until the exact shaping head completes required CI/review checks, merges with expected-head protection, canonical shaping post-merge CI succeeds, and canonical `main` is re-read.
