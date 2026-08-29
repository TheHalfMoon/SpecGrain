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

The latest published release remains `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## Closing frontier — Specification 022

Fresh reproduced adoption friction selected Specification 022 — Native Grain Preparation. Its shaping authority was merged through PR #37 as exact canonical shaped base `4919a4261f649e81cb1f507c0e80bc5c98d848d8`; canonical post-shaping CI `33260132438` succeeded before implementation.

022's bounded outcome is exactly:

```text
DRAFT -> SHAPED -> REFINING -> GRAIN
```

using explicit existing-schema inputs and the existing Grain-readiness evaluator.

ADR-0019 authorizes only:

- semantic shaping of one existing DRAFT into SHAPED;
- state-only SHAPED-to-REFINING mutation;
- readiness-gated state-only REFINING-to-GRAIN promotion;
- exact-preimage single-file replacement;
- native `shape`, `refine`, and `grain` CLI surfaces.

022 explicitly does not authorize:

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

### Product implementation state

Final product head `8af20015bd59424c7882b8c8fa7ea4c78e0af2e5` passed exact push CI `33261979828` and exact PR CI `33261982603`, each across the permanent five-cell matrix. Ubuntu/Python 3.11 recorded 575 passing tests plus all required Ruff, cleanliness, compile, CLI, package build, wheel-install, and installed-smoke gates.

Exact review repaired one lifecycle-authority defect before the final head: full Grain readiness is evaluated only for `REFINING -> GRAIN`; `shape` validates its explicit input contract without becoming an early hidden Grain gate.

PR #38 merged with expected-head protection as signature-verified canonical product merge `653cfb64c8885174ea3ea729d1bbb6418613b10d`. Its exact parents are shaped canonical base `4919a4261f649e81cb1f507c0e80bc5c98d848d8` and final implementation head `8af20015bd59424c7882b8c8fa7ea4c78e0af2e5`.

Canonical post-product CI `33262123902` completed `success` across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11.

### Review and residual state

All material inline review threads were resolved before product merge. Unavailable/skipped Qodo and final-head automatic CodeRabbit review were recorded as unavailable/skipped rather than PASS. Cubic descriptive output was not treated as independent approval.

A bounded concurrent-writer race remains an explicit residual. Specification 022 excludes multi-writer locking and recovery widening, so stronger coordination was not silently added. Future concurrency work requires separately shaped authority from fresh evidence.

### Published-release boundary

The historical `v0.3.0` tag and GitHub Release remain the published contract. After the 022 product merge:

- tag target remains `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release remains `378962445`;
- published wheel/source asset IDs, sizes, and digests remain unchanged;
- release notes still list only the historical command set and do not claim `shape`, `refine`, or `grain`.

Specification 022 is an unreleased current-source product change. No package version, tag, GitHub Release, asset, or historical release note is rewritten by 022.

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

## Remaining completion rule for Specification 022

Product implementation and canonical post-product verification are complete. 022 becomes canonical only when the remaining closeout sequence succeeds:

- a documentation-only closeout records exact product/review/merge/CI/release evidence and next-frontier reevaluation;
- permanent five-cell CI succeeds on the exact closeout head;
- exact closeout diff, reviews, threads, mergeability, and review-bot availability are rechecked without treating unavailable/skipped bots as PASS;
- closeout merge uses expected-head protection;
- resulting canonical `main` passes permanent five-cell CI;
- the historical v0.3.0 tag/release/assets remain unchanged;
- implementation and closeout PRs are confirmed merged/closed.

Only after those conditions exist may Specification 022 be declared `CLOSED_CANONICAL`.

## Post-022 frontier rule

No successor is pre-authorized. After canonical 022 closeout, the program returns to observation/evidence gathering.

A planned external architectural review and comparison with GitHub Spec Kit may be useful evidence collection. The review must compare against exact canonical SpecGrain truth and preserve SpecGrain's architectural independence. Neither an external reviewer nor Spec Kit may confer product authority. Concrete findings must be shaped into a new bounded specification before implementation.

In particular, READY mutation, WorkPacket CLI/execution, executor/provider orchestration, verification execution, evidence mutation, multi-writer locking, or a new release remain unselected until fresh evidence justifies one of those bounded frontiers.

No empirical benchmark winner is claimed without a reproducible completed dataset. No aspirational CLI command is presented as shipped historical-release behavior.