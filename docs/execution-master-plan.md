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

The v0.1.0 product release source commit is:

`5eb46db0479cb8707afe070027dab4f3c558849a`

This is the expected-head-protected merge of PR #18. Its second parent is exact reviewed PR head `1e4b36b169c7ac6d9e59741bb62b6a29b7649a17`. PR-head CI run `33234332746` and canonical post-merge CI run `33234395766` each completed the five-cell Linux/macOS/Windows matrix successfully.

Release workflow run `33234424696` published tag `v0.1.0` at that exact product merge commit and GitHub Release `378876694` with the versioned wheel and source distribution. Specification 016 documentation-only closeout then merged through PR #19 as canonical `main` `7c343841424ca48207f9c42eae725a53213d19e5`; final CI run `33234669930` and post-closeout release workflow `33234703124` succeeded.

Completed v0.1 capabilities include recursive/versioned specs, lifecycle/refinement/readiness validation, local state, dependency scheduling, brownfield scanning, context budgets, portable WorkPackets/results, independent evidence, method profiles, drift/metrics, Spec Kit import, generic agent adapters, benchmark comparability controls, permanent cross-platform CI, public migration/trust/community surfaces, and the published v0.1.0 release.

## Post-v0.1 evidence-shaped frontier

The initial sequence ended at Specification 016 and does not authorize an automatic successor. Every post-v0.1 specification must be shaped from current product/repository evidence.

The first post-v0.1 audit is `docs/research/post-v0.1-product-audit-2026-08-29.md`. It identified the missing supported first-party path from an initialized empty store to the first native SpecNode as the smallest adoption gap and shaped Specification 017 — Native DRAFT CLI.

017 shaping became canonical at `5c7783dde897c975b3519b37bfd45b547244b273`. Product PR #21 exact reviewed head `1255a9187f85591edd041a3125359e70d2eea379` completed final-head CI run `33235889444` successfully, then merged with expected-head protection as `dedb9ee30a6b8856c9c06439c68f3a37225f0563`. Canonical post-merge CI run `33236142514` completed the permanent five-cell matrix successfully.

017 closes the empty-project authoring gap on current `main`: users can create one validated root `DRAFT` through `specgrain draft` without hand-authoring internal JSON or receiving implied Grain/readiness/execution authority.

The fresh audit `docs/research/post-017-product-audit-2026-08-29.md` observes that published `v0.1.0` predates `draft` and recommends a versioned public release of the already-completed current authoring surface as the strongest next shaping candidate. That recommendation is not authority. No successor specification, release version, tag, PyPI publication, recursive refinement, or executor work is authorized until a separate shaped authority chain becomes canonical.

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

The 017 `CLOSED_CANONICAL` statement in its documentation-only closeout tree becomes authoritative only after the exact closeout head is merged and live GitHub post-closeout evidence confirms canonical `main`.
