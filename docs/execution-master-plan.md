# SpecGrain Execution Master Plan

This document is the durable continuation plan for SpecGrain. `specs/CURRENT.md` is authoritative for the active frontier, and live GitHub state overrides stale text when they disagree.

## Canonical reading order

Before changing the repository, read:

1. `AGENTS.md`;
2. `specs/CURRENT.md`;
3. `.specify/memory/constitution.md`;
4. this file;
5. the active `spec.md`, `plan.md`, and `tasks.md` when an active specification exists;
6. referenced ADRs, contracts, research, and implementation files.

## Product objective

> Make every software change small enough to understand, execute, verify, recover, measure, and prove.

SpecGrain is an independent, agent-neutral delivery system built around recursively refined specifications. Probabilistic systems may assist, but deterministic validation owns correctness-sensitive state transitions.

## Canonical initial program sequence

`000` established the foundation. Specifications `001` through `016` delivered the deterministic specification kernel, local store/CLI, dependency graph, brownfield context, WorkPacket/evidence boundaries, method/drift metrics, Spec Kit interoperability, agent adapters, SpecGrainBench controls, and public v0.1.0 launch.

Specifications 000 through 016 are `CLOSED_CANONICAL`. The published v0.1.0 product source is `5eb46db0479cb8707afe070027dab4f3c558849a`; exact release evidence remains in `specs/016-public-launch/closeout.md`.

## Post-v0.1 evidence-shaped frontier

Post-v0.1 specifications are never automatic successors. Each must be shaped from then-current product/repository/adoption evidence.

The first post-v0.1 audit shaped Specification 017 — Native DRAFT CLI. Its authority became canonical before implementation, product PR #21 merged with expected-head protection as `dedb9ee30a6b8856c9c06439c68f3a37225f0563`, and canonical post-merge CI run `33236142514` succeeded across all five permanent matrix jobs.

017 closes the empty-project authoring gap on `main`: users can create one validated native root DRAFT without hand-authoring internal JSON. It does not authorize recursive refinement, execution, hosted services, PyPI, or benchmark superiority work.

The fresh audit `docs/research/post-017-product-audit-2026-08-29.md` notes that published `v0.1.0` predates `draft` and recommends a versioned public release of the already-completed authoring surface as the next shaping candidate. This recommendation is not authority. No successor specification exists until a separate shaped authority chain is merged to canonical `main`.

## Cross-spec execution rules

1. Live GitHub/repository truth overrides chat handoffs.
2. No force-push, rebase, or destructive shared-history rewriting.
3. Use bounded feature branches and pull requests.
4. Verify exact PR head, checks, threads, and scope before merge.
5. Merge with expected-head protection where available.
6. Never claim PASS, VERIFIED, MERGED, COMPLETE, or CLOSED_CANONICAL without exact evidence.
7. Re-read canonical `main` after every merge.
8. Prefer smaller native implementations over dependencies without demonstrated need.
9. Do not execute untrusted repository commands merely to inspect a brownfield project.
10. Do not make AI reasoning transcripts repository authority.
11. Preserve residual risks and blockers.
12. External ideas/code require license-aware provenance.
13. Every post-v0.1 specification requires a newly shaped authority chain derived from current evidence.

## Completion rule for a post-v0.1 specification

A post-v0.1 specification is canonical only when:

- its shaped authority chain is present on canonical `main` before implementation begins;
- implementation is performed on a bounded branch from the exact shaped canonical base;
- required exact-head CI and review evidence succeeds;
- merge uses expected-head protection;
- canonical post-merge state and required CI are re-verified;
- closeout documentation records exact evidence before claiming `CLOSED_CANONICAL`;
- the exact closeout head is merged and post-closeout canonical truth is verified;
- the next product frontier is re-evaluated from current truth rather than assumed.

No empirical benchmark winner is claimed without a reproducible completed dataset. No aspirational CLI command is presented as shipped behavior.

The 017 `CLOSED_CANONICAL` statement in this closeout tree becomes authoritative only after the exact closeout head is merged and live GitHub post-closeout evidence confirms canonical `main`.
