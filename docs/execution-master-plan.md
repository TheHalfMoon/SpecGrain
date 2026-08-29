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

## Canonical program sequence

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

Specifications 000 through 016 are closed canonically after the documentation-only 016 closeout reaches `main` and its exact merge evidence is verified.

The v0.1.0 product release source commit is:

`5eb46db0479cb8707afe070027dab4f3c558849a`

This is the expected-head-protected merge of PR #18. Its second parent is exact reviewed PR head `1e4b36b169c7ac6d9e59741bb62b6a29b7649a17`. PR-head CI run `33234332746` and canonical post-merge CI run `33234395766` each completed the five-cell Linux/macOS/Windows matrix successfully.

Release workflow run `33234424696` published tag `v0.1.0` at that exact product merge commit and GitHub Release `378876694` with the versioned wheel and source distribution. Exact asset digests and release-state evidence are recorded in `specs/016-public-launch/closeout.md`.

Completed capabilities include recursive/versioned specs, lifecycle/refinement/readiness validation, local state, dependency scheduling, brownfield scanning, context budgets, portable WorkPackets/results, independent evidence, method profiles, drift/metrics, Spec Kit import, generic agent adapters, benchmark comparability controls, permanent cross-platform CI, public migration/trust/community surfaces, and the published v0.1.0 release.

## Program frontier

There is no active or next planned specification in the initial v0.1 program. Specification 016 Public Launch is the final planned specification in that sequence.

No empirical benchmark winner is claimed without a reproducible completed dataset. No aspirational CLI command is presented as shipped behavior.

Any future feature, release train, hosted product, empirical benchmark program, provider-specific integration, or other expansion must begin with a newly shaped specification derived from then-current repository truth. Deferred roadmap ideas are not implicitly authorized by completion of v0.1.

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

## Completion rule

The initial v0.1 program is complete only when all of the following are true in live GitHub truth:

- PR #18 is merged from exact reviewed head `1e4b36b169c7ac6d9e59741bb62b6a29b7649a17`;
- canonical product merge `5eb46db0479cb8707afe070027dab4f3c558849a` passes post-merge CI;
- tag `v0.1.0` and the public GitHub Release target that exact product merge and expose the expected distribution assets;
- the post-release documentation-only closeout is merged with expected-head protection;
- final canonical `specs/CURRENT.md` and Specification 016 report `CLOSED_CANONICAL` with no next planned specification.

The first three conditions are recorded as satisfied in `specs/016-public-launch/closeout.md`. The final two become canonical only after live post-merge verification of the closeout PR.
