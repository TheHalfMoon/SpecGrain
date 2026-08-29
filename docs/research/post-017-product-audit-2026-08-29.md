# Post-017 Product Audit — 2026-08-29

**Audit source revision:** `dedb9ee30a6b8856c9c06439c68f3a37225f0563`  
**Published release inspected:** `v0.1.0` at `5eb46db0479cb8707afe070027dab4f3c558849a`

## Purpose

This audit re-evaluates the smallest defensible product frontier after Specification 017 product delivery. It is evidence for later shaping; it is not implementation authority and does not create a successor specification.

## Live repository and adoption snapshot

At audit time:

- canonical product `main` is `dedb9ee30a6b8856c9c06439c68f3a37225f0563`;
- canonical post-product CI run `33236142514` succeeded across Ubuntu 3.11/3.12/3.13, macOS 3.11, and Windows 3.11;
- there are no open issues or pull requests;
- GitHub reports zero stars and forks;
- both `v0.1.0` release assets still report zero downloads;
- the repository remains less than two days old.

These popularity and download counts remain an absence of adoption evidence, not evidence of product failure.

## Product-surface change from the previous audit

Specification 017 closed the first-use authoring gap on `main`: a user can now run `init -> draft -> check` without hand-authoring internal JSON. The new `draft` command creates exactly one validated root node in `DRAFT` and intentionally grants no Grain/readiness/execution authority.

The next user journey still has two material discontinuities:

1. **Distribution discontinuity:** the public `v0.1.0` release predates `draft`, so users installing the published release do not receive the newly completed first-party authoring path.
2. **Refinement discontinuity:** current `main` can create a root DRAFT but cannot author reciprocal parent/child refinement through the CLI.

## Candidate frontier comparison

| Candidate | User value now | Scope/risk | Evidence dependency | Decision |
| --- | --- | --- | --- | --- |
| Publish current authoring surface in a new versioned GitHub release | High: makes the completed `draft` path available through the public release channel | Small/medium, release-governance sensitive | Existing cross-platform CI and release contract | **Recommend shaping next** |
| Native recursive refine CLI | High after DRAFT creation | Medium: atomic reciprocal tree mutation and lifecycle semantics | 017 authoring boundary exists | Reassess immediately after current surface is publicly deliverable |
| PyPI publication | Medium: simpler install | External identity/credential/trusted-publishing governance | Publishing setup not currently established | Defer |
| WorkPacket/executor CLI | Medium later-stage value | Medium | More useful after native authoring/refinement loop is usable | Defer |
| Empirical benchmark program | Potential proof value | High | Controlled run dataset/resources | Defer |
| Hosted dashboard or provider orchestration | Premature | High/lock-in risk | Adoption evidence | Defer |

## Recommended next shaping candidate

The smallest adoption-oriented next candidate is a **versioned public release of the already-verified current authoring surface**.

The reason is sequencing rather than feature count: adding more unreleased capability would widen the gap between repository `main` and the public installable product. A release-focused specification can make the completed 017 value available before adding recursive mutation semantics.

A later shaping step must still decide the exact version number and release workflow changes from canonical truth. This audit does not authorize a tag, release mutation, PyPI publication, or implementation work.

## Boundaries to preserve in later shaping

- do not retarget or mutate `v0.1.0`;
- do not claim that current `v0.1.0` contains `draft`;
- do not add PyPI or another distribution channel without explicit publishing-governance authority;
- do not bundle recursive refinement or executor orchestration into a release-only specification merely because those features are adjacent;
- preserve the zero-runtime-dependency contract unless a separate demonstrated need is shaped;
- keep benchmark and adoption claims evidence-backed.
