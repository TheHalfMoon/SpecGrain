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

Specification 000 established the project foundation and constitution. Specifications 000 through 016 are `CLOSED_CANONICAL`.

## Versioned product history

- `v0.1.0` product source: `5eb46db0479cb8707afe070027dab4f3c558849a`; initial program closeout: `7c343841424ca48207f9c42eae725a53213d19e5`.
- Specification 017 — Native DRAFT CLI: `CLOSED_CANONICAL`; root DRAFT authoring.
- Specification 018 — v0.2.0 Authoring Release: `CLOSED_CANONICAL`; published root DRAFT authoring.
- Specification 019 — Native Child-DRAFT Authoring: `CLOSED_CANONICAL`; recoverable reciprocal child authoring under ADR-0018.
- Specification 020 — v0.3.0 Recursive Authoring Release: `CLOSED_CANONICAL`; product/release source `70dd66aba0e68ae710e6ef12605ed153d107bab4`; GitHub Release `378962445`.
- Specification 021 — Public Launch Readiness Hardening: `CLOSED_CANONICAL`; repository-side public launch hardening without product/release mutation.
- Specification 022 — Native Grain Preparation: `CLOSED_CANONICAL`; current source closes the bounded native `DRAFT -> SHAPED -> REFINING -> GRAIN` pre-execution gap without READY/execution/verification authority.

The latest published release remains `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## Closed frontier — Specification 022

Fresh reproduced adoption friction selected Specification 022 — Native Grain Preparation. Its shaped authority merged through PR #37 as canonical base `4919a4261f649e81cb1f507c0e80bc5c98d848d8`; post-shaping CI `33260132438` succeeded before implementation.

022's bounded outcome was exactly:

```text
DRAFT -> SHAPED -> REFINING -> GRAIN
```

using explicit existing-schema inputs and the existing Grain-readiness evaluator.

ADR-0019 authorized only:

- semantic shaping of one existing DRAFT into SHAPED;
- state-only SHAPED-to-REFINING mutation;
- readiness-gated state-only REFINING-to-GRAIN promotion;
- exact-preimage single-file replacement;
- native `shape`, `refine`, and `grain` CLI surfaces.

022 did not authorize:

- `GRAIN -> READY` or later lifecycle transitions;
- WorkPacket CLI generation/execution;
- executor/provider invocation or agent orchestration;
- verification/evidence execution or evidence mutation;
- generic mature-SpecNode editing;
- multi-writer locking/recovery expansion;
- PyPI/new-release scope;
- hosted/provider/account scope;
- runtime dependency growth;
- readiness weakening;
- empirical benchmark claims.

### Canonical closure evidence

Final product head `8af20015bd59424c7882b8c8fa7ea4c78e0af2e5` passed exact push CI `33261979828` and exact PR CI `33261982603`, each across the permanent five-cell matrix. Ubuntu/Python 3.11 recorded 575 passing tests plus all required Ruff, cleanliness, compile, CLI, package build, wheel-install, and installed-smoke gates.

Exact review repaired one lifecycle-authority defect before the final head: full Grain readiness is evaluated only for `REFINING -> GRAIN`; `shape` validates its explicit input contract without becoming an early hidden Grain gate.

PR #38 merged with expected-head protection as signature-verified product merge `653cfb64c8885174ea3ea729d1bbb6418613b10d`; post-product CI `33262123902` completed `success` across all five permanent cells.

Documentation closeout head `7b3b5beed297d024ad897e3b7e4d5376c8c5f24a` changed only seven documentation/governance paths and passed push CI `33262421052` plus PR CI `33262442496`, each across all five permanent cells. Review-bot unavailability/rate-limiting was recorded without treating it as PASS.

PR #39 merged with expected-head protection as signature-verified canonical closeout merge `9cd52eb6d1ba6839910ceb973fedf5b3a727cc0a`, with exact parents `653cfb64c8885174ea3ea729d1bbb6418613b10d` and `7b3b5beed297d024ad897e3b7e4d5376c8c5f24a`.

Canonical post-closeout CI `33262519733` completed `success` across the permanent five-cell matrix. PR #38 and PR #39 are merged/closed. The historical `v0.3.0` tag, Release `378962445`, published assets, digests, and historical command list remain unchanged.

Specification 022 is therefore `CLOSED_CANONICAL`.

### Residual state

A bounded concurrent-writer race remains an explicit residual. Specification 022 excluded multi-writer locking and recovery widening, so stronger coordination was not silently added. Future concurrency work requires separately shaped authority from fresh evidence.

## Cross-spec execution rules

1. Live GitHub/repository truth overrides chat handoffs.
2. No force-push, rebase, or destructive shared-history rewriting.
3. Use bounded feature branches and pull requests.
4. Verify exact PR head, checks, threads, and scope before merge.
5. Merge with expected-head protection where available.
6. Never claim PASS, VERIFIED, MERGED, COMPLETE, or `CLOSED_CANONICAL` without exact evidence.
7. Re-read canonical `main` after every merge.
8. Prefer smaller native implementations over dependencies without demonstrated need.
9. Do not execute untrusted repository commands merely to inspect a brownfield project.
10. Do not make AI reasoning transcripts repository authority.
11. Preserve residual risks and blockers.
12. External ideas/code require license-aware provenance.
13. Post-v0.1 work requires a newly shaped specification derived from live evidence; roadmap deferrals, audits, external reviewers, and upstream-tool comparisons are not implicit implementation authority.

## Post-022 frontier rule

The program is now at `POST_022_OBSERVATION`. No successor is pre-authorized or currently selected.

A planned external architectural review and comparison with GitHub Spec Kit may be useful evidence collection. The review must compare against exact canonical SpecGrain truth and preserve SpecGrain's architectural independence. Neither an external reviewer nor Spec Kit may confer product authority. Concrete findings must be reproduced and shaped into a new bounded specification before implementation.

In particular, READY mutation, WorkPacket CLI/execution, executor/provider orchestration, verification execution, evidence mutation, multi-writer locking, or a new release remain unselected until fresh evidence justifies one of those bounded frontiers.

No empirical benchmark winner is claimed without a reproducible completed dataset. No aspirational CLI command is presented as shipped historical-release behavior.