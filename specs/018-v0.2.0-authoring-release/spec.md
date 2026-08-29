# Specification 018 — v0.2.0 Authoring Release

## Status

`CLOSED_CANONICAL` — prospective inside the documentation-only closeout branch; authoritative only after exact-head closeout merge and post-closeout proof.

## Outcome

Publish a new immutable-by-contract GitHub release that makes the already-verified native root-DRAFT authoring surface from Specification 017 available through the public versioned product, without adding unrelated product behavior or mutating the existing `v0.1.0` release.

## Why this is the next frontier

Specification 017 closed the first-use authoring gap on canonical `main`, but the previous public release `v0.1.0` did not contain `specgrain draft` or `create_draft_spec`. The post-017 audit identified this distribution discontinuity as the smallest adoption-oriented gap.

`0.2.0` was selected as the next package/release version because the unreleased change added a backward-compatible public CLI/API capability. ADR-0017 records the durable release progression rule.

## Delivered scope

- package version `0.2.0` with zero runtime dependencies;
- Git tag and GitHub Release `v0.2.0` bound at first publication to exact successful canonical product merge `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`;
- truthful `docs/releases/v0.2.0.md` release notes;
- changelog promotion of Specification 017's native DRAFT authoring entries;
- README/install/version truth for the v0.2.0 public surface;
- metadata-derived monotonic GitHub release workflow under ADR-0017;
- historical `v0.1.0` preservation;
- deterministic release-contract guards;
- exact-head CI/review, expected-head product merge, canonical post-merge CI, live release/tag/asset evidence, and bounded closeout evidence.

## Preserved exclusions

Specification 018 did not add:

- recursive child refinement or new authoring behavior beyond Specification 017;
- lifecycle promotion, readiness synthesis, WorkPacket/executor orchestration, agent/provider execution, or evidence mutation;
- PyPI, trusted publishing, package registries, signing infrastructure, attestations, or new external credentials;
- hosted services, networking, telemetry, dashboards, accounts, or model calls;
- runtime dependencies;
- benchmark execution, benchmark superiority claims, or unsupported adoption claims;
- mutation, retargeting, deletion, replacement, or new asset upload to `v0.1.0`;
- branch-protection or unrelated repository-administration changes.

## Acceptance evidence

1. `pyproject.toml` declares `0.2.0`; runtime dependencies remain empty.
2. v0.2.0 release notes truthfully document native root-DRAFT authoring and preserved boundaries.
3. Release workflow derives version/tag/assets/notes/title from package metadata.
4. Workflow triggers only after successful canonical `main` CI and checks out its exact head SHA.
5. Existing `v0.1.0` remains bound to `5eb46db0479cb8707afe070027dab4f3c558849a` with original assets/digests.
6. Existing-version verification is no-mutation and does not require a historical tag to move to later `main`.
7. Partial tag/release publication states fail closed by contract.
8. First v0.2.0 publication created the tag/release at exact product merge `baf00995...` and uploaded only the expected wheel and sdist.
9. Release source contains the Specification 017 authoring surface and zero-runtime-dependency contract.
10. Exact final implementation-head CI run `33245686864` succeeded across the permanent five-cell matrix.
11. Exact-head review found and repaired release-title verification before merge; no unresolved material finding remained.
12. Product merge used expected-head protection and canonical post-merge CI run `33245753969` succeeded.
13. Live GitHub proves v0.2.0 release identity and asset SHA-256 digests; exact values are in `closeout.md`.
14. Canonical closeout remains conditional on exact closeout merge plus post-closeout CI/no-mutation release verification.

## Canonical evidence chain

- 018 shaping exact head: `68e830dc51d0df4bc521607be46ce9f11dc34acd`;
- shaping CI: `33237175016`;
- shaping merge: `b170aed92812c367282fbacb5d46e5acb450a196`;
- shaping post-merge CI: `33245330017`;
- final product head: `bf63dbb4ef2259f79dc4e88e3b7f5abc0d05c178`;
- final product-head CI: `33245686864`;
- product merge: `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`;
- product post-merge CI: `33245753969`;
- release workflow run: `33245783948`;
- v0.2.0 Release ID: `378936896`.

## Risks and recovery retained after release

Historical tags/releases are evidence anchors and are not rewritten. The generalized workflow fails closed on ambiguous partial publication. Git tag creation and GitHub Release creation remain separate external writes; an interrupted first publication may therefore require explicit evidence-preserving recovery rather than an automatic guess.

The GitHub API currently reports the v0.2.0 Release `immutable` field as `false`; immutability is a SpecGrain repository contract enforced by workflow behavior, not a claim that GitHub itself has locked the release object.

## Successor boundary

The post-v0.2 audit recommends native child-DRAFT authoring as the smallest next shaping candidate, but no successor specification is authorized by this file. Fresh canonical shaping is still required after this closeout becomes authoritative.
