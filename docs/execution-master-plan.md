# SpecGrain Execution Master Plan

This document is the durable continuation plan for SpecGrain. `specs/CURRENT.md` is authoritative for the active frontier, and live GitHub state overrides stale text when they disagree.

## Canonical reading order

Before changing the repository, read:

1. `AGENTS.md`;
2. `specs/CURRENT.md`;
3. `.specify/memory/constitution.md`;
4. this file;
5. the active `spec.md`, `plan.md`, and `tasks.md`;
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

## Completed frontier

Specifications 000 through 015 are closed canonically on `main`.

The post-015 canonical baseline is:

`001a70fcabff497c565fa7339381c4da0b4a3881`

This is the merge of PR #17. Its second parent is exact reviewed PR head `14e3d7e6a301148e0a25c2e98134fe8a6c573b54`.

Completed capabilities include recursive/versioned specs, lifecycle/refinement/readiness validation, local state, dependency scheduling, brownfield scanning, context budgets, portable WorkPackets/results, independent evidence, method profiles, drift/metrics, Spec Kit import, generic agent adapters, and benchmark comparability controls.

## Active frontier — 016 Public Launch

Active branch: `feat/016-public-launch`.

Read `specs/016-public-launch/spec.md`, `plan.md`, `tasks.md`, and ADR-0016 before acting.

016 must ship:

- versioned installable `0.1.0` package;
- permanent Linux/macOS/Windows CI;
- truthful README and runnable zero-to-verified example;
- pinned brownfield examples;
- Spec Kit migration and benchmark reports;
- contribution/security/trust/conduct surfaces;
- release notes and launch assets;
- tag `v0.1.0` and a GitHub Release;
- exact post-release canonical closeout.

No empirical benchmark winner may be claimed without a reproducible completed dataset. No aspirational CLI command may be presented as shipped behavior.

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

016 is the final planned specification in this program sequence. The program is complete only after the product PR merges, `v0.1.0` is published at the exact release commit, and a post-release documentation-only closeout leaves `specs/CURRENT.md` at `CLOSED_CANONICAL` with no next planned specification.

Any subsequent feature begins a new explicitly shaped specification derived from then-current repository truth; it is not implicitly authorized by this completed sequence.
