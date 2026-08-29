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

SpecGrain is an independent, agent-neutral delivery system built around recursively refined specifications. A specification is refined until a leaf satisfies the deterministic Definition of Grain. Probabilistic systems may propose work; they are never the sole authority for correctness-sensitive state transitions.

## Canonical initial program sequence

```text
001 SpecNode schema
  -> 002 lifecycle state
  -> 003 refinement tree
  -> 004 Grain readiness
  -> 005 CLI/local store
  -> 006 dependency graph
  -> 007 repository scan
  -> 008 context budget
  -> 009 WorkPacket
  -> 010 verification/evidence
  -> 011 method profiles
  -> 012 diff/drift/metrics
  -> 013 Spec Kit import
  -> 014 agent adapters
  -> 015 SpecGrainBench
  -> 016 public launch
```

Specification 000 established the project foundation and constitution.

## Initial v0.1 program completion

Specifications 000 through 016 are closed canonically.

The v0.1.0 product release source commit is `5eb46db0479cb8707afe070027dab4f3c558849a`. Exact first-release and closeout evidence is recorded under `specs/016-public-launch/`.

Completed v0.1 capabilities include recursive/versioned specs, lifecycle/refinement/readiness validation, local state, dependency scheduling, brownfield scanning, context budgets, portable WorkPackets/results, independent evidence, method profiles, drift/metrics, Spec Kit import, generic agent adapters, benchmark comparability controls, permanent cross-platform CI, public migration/trust/community surfaces, and the published v0.1.0 release.

## Post-v0.1 evidence-shaped frontier

The initial sequence ended at Specification 016 and does not authorize an automatic successor. Every post-v0.1 specification must be shaped from current product/repository evidence.

Specification 017 — Native DRAFT CLI is `CLOSED_CANONICAL`. Its product merge is `dedb9ee30a6b8856c9c06439c68f3a37225f0563`; its closeout merge is `d7c3f8e5734264824cd6ed1d8e931802a242c50a`.

Specification 018 — v0.2.0 Authoring Release completed product delivery at merge `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`. Canonical product post-merge CI run `33245753969` succeeded, and release workflow run `33245783948` published GitHub Release `378936896` / tag `v0.2.0` from that exact merge. Live release and historical v0.1.0 preservation evidence is recorded in `specs/018-v0.2.0-authoring-release/closeout.md`.

The fresh post-v0.2 audit `docs/research/post-v0.2-product-audit-2026-08-29.md` recommends native child-DRAFT authoring as the smallest next shaping candidate because the public product can create one root DRAFT while the deterministic recursive model is not yet writable through the supported authoring surface. The audit is not authority. No successor specification is implied until Specification 018 closeout becomes canonical and a separate shaping chain is merged.

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
13. Post-v0.1 work requires a newly shaped specification derived from live evidence; roadmap deferrals and audit recommendations are not implicit authority.

## Completion rule for a post-v0.1 specification

A post-v0.1 specification is canonical only when:

- its shaped authority chain is present on canonical `main` before implementation begins;
- implementation is performed on a bounded branch from the exact shaped canonical base;
- required exact-head CI and review evidence succeeds;
- merge uses expected-head protection;
- canonical post-merge state and required CI are re-verified;
- closeout documentation records exact evidence before claiming `CLOSED_CANONICAL`;
- the exact closeout head is merged with expected-head protection and post-closeout canonical state/CI are verified;
- the next product frontier is re-evaluated from current truth rather than assumed.

No empirical benchmark winner is claimed without a reproducible completed dataset. No aspirational CLI command is presented as shipped behavior.

The Specification 018 `CLOSED_CANONICAL` state authored on its documentation-only closeout branch is prospective until that exact closeout head is merged and post-closeout canonical CI plus the no-mutation release verification path succeed.
