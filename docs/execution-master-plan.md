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
- Specification 021 — Public Launch Readiness Hardening: `CLOSED_CANONICAL`; canonical closeout `3b98914200c68909f09db08642faf56de48305eb` after reconciliation PR #36.

The latest published release remains `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## Active frontier — Specification 022

Fresh reproduced adoption friction selected Specification 022 — Native Grain Preparation. The shaping authority chain was merged through PR #37 as exact canonical shaped base `4919a4261f649e81cb1f507c0e80bc5c98d848d8`. Canonical post-shaping permanent CI `33260132438` succeeded before product implementation began.

022's bounded outcome is:

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
- WorkPacket CLI generation;
- executor/provider invocation or agent orchestration;
- running verification/evidence commands;
- evidence-record mutation;
- AI-generated shaping or hidden readiness defaults;
- readiness-rule weakening;
- PyPI/new-release scope;
- hosted/provider/account scope;
- empirical benchmark claims.

### Implementation state

Implementation is on `feat/022-native-grain-preparation`, based exactly on shaped canonical `4919a4261f649e81cb1f507c0e80bc5c98d848d8` with no behind-main drift at the pre-document checkpoint.

Checkpoint `05865fdfeb89e259be237f5e020a87424384d122` delivered:

- dedicated bounded `src/specgrain/pregrain.py` mutation module reusing existing store safety primitives;
- public APIs for explicit DRAFT shaping, state-only refinement, and readiness-gated Grain promotion;
- `shape`, `refine`, and `grain` CLI commands;
- exact-preimage single-file mutation with pending ADR-0018 refusal;
- proposed refinement/dependency validation;
- deterministic text/JSON output and blocker/no-mutation semantics;
- semantic revision preservation for state-only transitions;
- existing `next` integration;
- zero runtime dependency growth.

Permanent CI `33260707422` succeeded on exact checkpoint `05865fdfeb89e259be237f5e020a87424384d122` across all five supported cells. Ubuntu/Python 3.11 recorded 573 passing tests plus Ruff for source/tests/examples, editable installation, tracked-tree cleanliness, compile, CLI smoke, package build, built-wheel installation, and installed CLI smoke.

The checkpoint was not yet the final product candidate because README/architecture/changelog/launch guards and current governance state still required reconciliation. Final product CI and review must bind to the documentation-reconciled exact head.

### Published-release boundary

The historical `v0.3.0` tag and GitHub Release remain the published contract. They contain root/child DRAFT authoring and explicit recovery, but do not contain `shape`, `refine`, or `grain`.

Specification 022 is an unreleased current-source product change. No package version, tag, GitHub Release, release asset, or release note may be rewritten to imply otherwise.

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

## Completion rule for Specification 022

022 is canonical only when:

- its shaped authority chain is present on canonical `main` before implementation begins;
- implementation is performed on a bounded branch from the exact shaped canonical base;
- required focused/full/static/package checks and permanent five-cell exact-head CI succeed on the final product candidate;
- exact-head review confirms no readiness weakening, hidden defaults, edge skipping, post-GRAIN authority, recovery widening, dependency creep, false historical-release claims, or unrelated scope;
- implementation PR review threads/submitted reviews/mergeability and review-bot availability are rechecked without treating unavailable/skipped bots as PASS;
- merge uses expected-head protection;
- canonical post-merge state, CI, and historical v0.3.0 release no-mutation behavior are re-verified;
- a documentation-only closeout records exact evidence and re-evaluates the next frontier;
- the exact closeout head is merged with expected-head protection and final canonical state/CI are verified.

The likely later need for a WorkPacket/execution workflow is not pre-authorized. It must be selected, shaped, and implemented only from fresh post-022 evidence.

No empirical benchmark winner is claimed without a reproducible completed dataset. No aspirational CLI command is presented as shipped historical-release behavior.
