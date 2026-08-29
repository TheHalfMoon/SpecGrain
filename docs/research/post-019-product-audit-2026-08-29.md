# Post-019 Product Audit — 2026-08-29

**Audit source revision:** `d6727b6c5cdafcf6265b6d999418c0fe853249a7`  
**Published release inspected:** `v0.2.0`, GitHub Release `378936896`

## Purpose

This audit re-evaluates the smallest defensible product frontier after Specification 019 product delivery. It is evidence for later shaping only. It does not authorize a successor specification, version bump, release, lifecycle mutation, or implementation.

## Live repository and adoption snapshot

At audit time:

- canonical product `main` is `d6727b6c5cdafcf6265b6d999418c0fe853249a7`;
- PR #27 merged with expected-head protection from exact final head `53cd8482b727d4f61bfafbea6ed363e4e8783d52`;
- canonical product post-merge CI run `33248014390` succeeded across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11;
- post-product Release workflow run `33248070688` succeeded and verified existing historical `v0.2.0` without mutation;
- live tag `v0.2.0` still targets historical product source `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`;
- GitHub Release `378936896` remains public/non-prerelease with the same wheel and source-distribution IDs, sizes, and digests;
- there are no open issues or pull requests;
- GitHub reports zero stars and zero forks;
- both v0.2.0 release assets still report zero downloads;
- the repository remains less than two days old.

The popularity and download counts are an absence of adoption evidence, not evidence of product failure.

## Current canonical product journey

Current unreleased `main` can support the bounded first-party path:

```text
init -> draft root -> draft child -> check
                       |
                       +-> recover only if an exact supported authoring transaction is pending
```

A child remains `DRAFT`; its parent remains `DRAFT`. The product can now express recursive structure natively without hand-authoring internal JSON and without silently granting Grain/readiness/execution authority.

Published `v0.2.0`, however, intentionally predates Specification 019. Its `draft` surface creates roots only and it has no `recover` command. Therefore the exact current canonical product behavior is not available through the latest versioned release.

## Candidate frontier comparison

| Candidate | User value now | Scope/risk | Existing leverage | Decision |
| --- | --- | --- | --- | --- |
| v0.3.0 Recursive Authoring Release | High: makes already-proven child-DRAFT/recovery behavior available through a monotonic versioned release | Low/medium: metadata, release notes, changelog/docs/tests and publication proof; no new product behavior required | ADR-0017, generalized Release workflow, successful v0.1/v0.2 history, exact 019 evidence | **Recommend shaping next** |
| Lifecycle-aware broad `refine` / automatic progression | High eventually | High: combines semantic editing, lifecycle authority, readiness prerequisites, and recursive mutation | Structural/lifecycle validators exist but mutation authority does not | Defer; do not bundle with distribution |
| Generic DRAFT editing | Medium/high later | Medium/high: arbitrary replacement semantics, revision authority, collision/recovery rules | Immutable SpecNode and ADR-0018 patterns exist | Reassess after current recursive behavior is versioned or new evidence appears |
| Stronger multi-writer/recovery concurrency | Low/medium without observed demand | Medium: requires an explicit locking/generation contract and cross-platform evidence | ADR-0018 documents current residual limits | Defer unless real concurrent-authoring evidence justifies it |
| PyPI publication | Medium installation convenience | Medium/external: package identity, trusted publishing, credentials, registry governance | GitHub release automation is reusable | Defer while adoption evidence remains absent and GitHub release installation works |
| WorkPacket/executor CLI | Medium later-stage value | Medium/high | WorkPacket/adapter APIs exist | Defer until first-party authoring has an explicit lifecycle/readiness mutation path |
| Empirical benchmark program | Potential proof value | High/resource-sensitive | Benchmark harness exists | Defer: no controlled public comparative dataset |
| Hosted dashboard/provider orchestration | Premature | High/lock-in risk | No adoption signal demanding it | Defer |

## Recommended next shaping candidate

The smallest next candidate is **v0.3.0 Recursive Authoring Release**.

The rationale is not feature appetite; it is a concrete distribution discontinuity. Specification 019 is already implemented and verified on canonical `main`, while the latest immutable-by-contract release is still v0.2.0 from before child authoring existed.

ADR-0017 already establishes the relevant durable policy:

- historical tags/releases are append-only by repository contract;
- package metadata supplies the candidate version;
- first publication binds the exact successful canonical `main` CI head;
- an already-published version verifies historical identity/state/assets without moving the historical tag;
- backward-compatible public feature additions before 1.0 require a minor version bump.

Therefore later shaping should prefer `0.3.0` / `v0.3.0`, not republishing or moving `v0.2.0`.

A bounded release specification should be limited to:

- package metadata version `0.3.0`;
- truthful v0.3.0 release notes covering root/child DRAFT authoring and explicit recovery;
- promoting the current Unreleased changelog content into a dated 0.3.0 section and restoring an empty Unreleased boundary;
- README/versioned-install truth that distinguishes current release from future unreleased work;
- release-contract/launch tests required by existing repository conventions;
- exact-head CI, expected-head merge, canonical post-merge CI, first-publication Release workflow evidence, live tag/release/asset identity and digest evidence;
- preservation of v0.1.0 and v0.2.0 historical releases.

It should not change `src/specgrain/` product behavior merely to justify a release.

## Why not lifecycle progression next

The recursive authoring model is now usable but deliberately incomplete. That is a safer state than granting broad mutation authority prematurely.

A lifecycle-aware authoring surface would need explicit answers for at least:

- which fields may be edited at each state;
- whether edits create a new immutable semantic revision or replace canonical content;
- how state-transition legality is coupled to mutation authority;
- when readiness metadata may be populated and by whom;
- how parent/child lifecycle relationships interact;
- how multi-file edit transactions and recovery compose beyond the narrow ADR-0018 child case;
- what CLI/API output proves the exact new revision and authority boundary.

Those are shaping questions, not reasons to expand the release candidate.

## Boundaries to preserve in later shaping

- never move or mutate historical v0.1.0/v0.2.0 tags/releases;
- no PyPI publication bundled into the GitHub release without separate registry authority;
- no lifecycle promotion or generic editing bundled into the release;
- no new runtime dependency;
- no hosted/network/provider behavior;
- no claim that current adoption counts establish success or failure;
- no empirical benchmark superiority claim without a reproducible completed dataset.

## Successor authority rule

This audit does not make v0.3.0 canonical work. Specification 019 must first close canonically through its exact closeout merge and post-closeout CI. Only then may a separate Specification 020 shaping chain decide whether this recommendation remains the smallest defensible frontier under live GitHub truth.
