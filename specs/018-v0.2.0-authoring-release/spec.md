# Specification 018 — v0.2.0 Authoring Release

## Status

`CLOSED_CANONICAL` — prospective inside the documentation-only closeout branch; authoritative only after exact-head closeout merge and post-closeout proof.

## Outcome

Publish a new immutable-by-contract GitHub release that makes the already-verified native root-DRAFT authoring surface from Specification 017 available through the public versioned product, without adding unrelated product behavior or mutating the existing `v0.1.0` release.

## Why this is the next frontier

Specification 017 closed the first-use authoring gap on canonical `main`, but the latest public release at shaping time remained `v0.1.0` and did not contain `specgrain draft` or `create_draft_spec`. The post-017 audit identified this distribution discontinuity as the smallest current adoption gap.

`0.2.0` was selected as the next package/release version because the unreleased change added a backward-compatible public CLI/API capability. For the pre-1.0 product line, backward-compatible feature additions advance the minor component; corrections that add no public capability may use the patch component. ADR-0017 records the durable release progression rule.

## In scope

- package version `0.2.0`;
- Git tag and GitHub Release `v0.2.0` bound at first publication to the exact successful canonical product merge;
- release notes that describe only behavior present on the release source revision;
- changelog promotion of the current Unreleased native DRAFT authoring entries into `0.2.0`;
- README/install/version references required to make the current public release surface truthful;
- replacement of the one-off hard-coded `v0.1.0` workflow with a deterministic monotonic versioned-release workflow that derives the release identity from package metadata and fails closed on historical-release conflicts;
- preservation and verification of the existing `v0.1.0` tag/release/assets without mutation;
- tests/static checks for release metadata, expected asset names, release-note presence, historical release protection, and version consistency where repository-local deterministic tests are practical;
- exact-head CI, review, expected-head product merge, post-merge CI, live tag/release verification, asset digests, and documentation-only canonical closeout.

## Out of scope

- recursive child refinement or any new authoring behavior beyond Specification 017;
- lifecycle promotion, readiness synthesis, WorkPacket/executor orchestration, agent/provider execution, or evidence mutation;
- PyPI, trusted publishing, package registries, signing infrastructure, attestations, or new external credentials;
- hosted services, networking, telemetry, dashboards, accounts, or model calls;
- runtime dependency additions;
- benchmark execution, benchmark superiority claims, or adoption claims unsupported by public evidence;
- retargeting, deleting, replacing, or uploading new assets to `v0.1.0`;
- branch-protection or repository-administration changes unrelated to the release contract.

## Acceptance conditions

1. `pyproject.toml` declares package version `0.2.0`, and repository version/release references that are intended to describe the current public release are consistent with `v0.2.0`.
2. The `0.2.0` release notes truthfully include native root-DRAFT authoring and do not claim recursive refinement, provider execution, PyPI availability, empirical benchmark superiority, or any capability absent from the exact release revision.
3. The release workflow derives package version, tag, expected distribution filenames, release-note path, and public release title deterministically rather than embedding a one-off `0.1.0` release identity.
4. The workflow is triggered only from a successful canonical `main` CI result and checks out that exact successful CI head SHA before any release decision.
5. A historical tag/release for a different version is never mutated. Existing `v0.1.0` remains bound to `5eb46db0479cb8707afe070027dab4f3c558849a` with its original two assets.
6. If the current version is already fully published, the workflow verifies the tag/release counterpart, their consistent historical release identity, public non-draft/non-prerelease state, and exact expected assets, then exits successfully without mutation even when a later `main` CI head differs from the historical tag target.
7. A candidate-version release-without-tag, tag-without-release, release/tag identity disagreement, unexpected asset set, or other ambiguous partial-publication state fails closed.
8. If the current version is not yet published and neither its tag nor release exists, the workflow creates exactly the expected immutable-by-contract tag and public GitHub Release at the exact successful canonical product merge and uploads only the expected wheel and source distribution.
9. The release source revision contains `specgrain draft`, the public `create_draft_spec` API, the current zero-runtime-dependency contract, and all permanent CI gates.
10. Exact implementation PR-head CI succeeds across Ubuntu/Python 3.11, 3.12, and 3.13, macOS/Python 3.11, and Windows/Python 3.11 before merge.
11. Exact-head review confirms no historical release mutation path, no hidden external publishing channel, no unrelated product scope, no unsupported claims, and no weakened evidence boundary.
12. Product merge uses expected-head protection and canonical post-merge CI succeeds on that exact merge revision.
13. Live GitHub proves `v0.2.0` tag target, GitHub Release target/state, asset names, asset SHA-256 digests, and publication state before `RELEASED` is claimed.
14. Specification 018 is not `CLOSED_CANONICAL` until exact release evidence is recorded in a bounded documentation-only closeout PR, that exact closeout head is merged with expected-head protection, and post-closeout canonical CI is successful.

## Dependencies

- Specifications 000 through 017 are `CLOSED_CANONICAL`.
- Canonical starting revision: `d7c3f8e5734264824cd6ed1d8e931802a242c50a`.
- Canonical 018 shaping merge: `b170aed92812c367282fbacb5d46e5acb450a196`.
- Exact 018 shaping head: `68e830dc51d0df4bc521607be46ce9f11dc34acd`.
- Exact shaping CI run: `33237175016`.
- Canonical shaping post-merge CI run: `33245330017`.
- Specification 017 product merge: `dedb9ee30a6b8856c9c06439c68f3a37225f0563`.
- Specification 017 closeout merge: `d7c3f8e5734264824cd6ed1d8e931802a242c50a`.
- Published `v0.1.0` source: `5eb46db0479cb8707afe070027dab4f3c558849a`.
- ADR-0016 remains historical authority for the first public release invariants.
- ADR-0017 defines monotonic post-v0.1 GitHub release progression.

## Risks and recovery

- **Historical release mutation:** fail closed before any write when existing tag/release identity is inconsistent; never update `v0.1.0`.
- **Wrong release source:** bind new-publication writes to the exact successful `workflow_run.head_sha`; a wrong or stale target blocks publication.
- **False rerun conflict:** once a version is fully published, treat its tag target as the historical source and verify it without requiring later `main` heads to match.
- **Version/document drift:** deterministic repository checks bind package metadata, tag, asset names, and release-note path.
- **Partial publication:** workflow detects tag-without-release and release-without-tag as conflicts instead of silently repairing ambiguous external state.
- **Release rerun:** exact already-published `v0.2.0` becomes a no-mutation successful verification path.
- **Scope creep:** 018 changes distribution/versioning only; new product behavior requires a later shaped specification.

## Constitution and architecture

No constitution amendment is required. The release remains vendor-neutral, dependency-free at runtime, evidence-bound, and reversible before publication. After publication, tags/releases are historical anchors and are protected by fail-closed monotonic release rules rather than rewritten.

The shaped authority is canonical through merge `b170aed92812c367282fbacb5d46e5acb450a196`. Implementation was performed on a bounded branch from that exact base.

## Completion evidence

- final exact product head: `bf63dbb4ef2259f79dc4e88e3b7f5abc0d05c178`;
- final product-head CI: `33245686864` — success;
- expected-head product merge: `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`;
- canonical product post-merge CI: `33245753969` — success;
- release workflow run: `33245783948` — success;
- live GitHub Release: `v0.2.0`, ID `378936896`, exact target `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`;
- exact asset names, sizes, SHA-256 digests, reviewer boundaries, and v0.1.0 preservation evidence: `closeout.md`;
- fresh post-release frontier audit: `docs/research/post-v0.2-product-audit-2026-08-29.md`.

The prospective `CLOSED_CANONICAL` status becomes authoritative only after the exact documentation-only closeout head is merged with expected-head protection and post-closeout canonical CI plus no-mutation release verification succeed.
