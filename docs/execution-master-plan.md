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

Specification 017 — Native DRAFT CLI is `CLOSED_CANONICAL`. Its product merge is `dedb9ee30a6b8856c9c06439c68f3a37225f0563`; its closeout merge is `d7c3f8e5734264824cd6ed1d8e931802a242c50a`; exact product and closeout CI evidence is recorded under `specs/017-native-draft-cli/`.

017 closes the empty-project authoring gap on current `main`: users can create one validated root `DRAFT` through `specgrain draft` without hand-authoring internal JSON or receiving implied Grain/readiness/execution authority.

The fresh audit `docs/research/post-017-product-audit-2026-08-29.md` identified the distribution discontinuity between current `main` and public `v0.1.0` as the smallest adoption-oriented gap and shaped Specification 018 — v0.2.0 Authoring Release.

Specification 018 is `CLOSED_CANONICAL`. Product merge `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85` passed canonical CI `33245753969`; release workflow `33245783948` published GitHub Release `378936896` / tag `v0.2.0`. Documentation-only closeout merged as `c5282caa29fbfeb8c118755766b6a7b8a49d2781`; post-closeout CI `33246162550` succeeded and release verification `33246212598` confirmed the existing historical `v0.2.0` release without mutation.

The fresh post-v0.2 audit `docs/research/post-v0.2-product-audit-2026-08-29.md` selected native child-DRAFT authoring as the smallest recursive product gap and shaped Specification 019 narrowly under ADR-0018.

Specification 019 is `CLOSED_CANONICAL`. Product merge `d6727b6c5cdafcf6265b6d999418c0fe853249a7` passed canonical product CI `33248014390`; historical-release verification `33248070688` preserved `v0.2.0`. Documentation-only closeout merged as `3f8f3d825c3171a3a9ac7761ee5bc642e68a9d2d`; post-closeout CI `33248332725` succeeded and Release verification `33248368659` again preserved historical `v0.2.0` without mutation.

019 adds bounded native child-DRAFT authoring and explicit recovery without lifecycle promotion, readiness synthesis, or execution authority.

The fresh post-019 audit `docs/research/post-019-product-audit-2026-08-29.md` identified the distribution discontinuity between canonical recursive authoring and public `v0.2.0` as the smallest next gap and shaped Specification 020 — v0.3.0 Recursive Authoring Release.

Specification 020 is `CLOSED_CANONICAL`.

- final implementation/evidence PR head `bf59a2ceba3e28cabc2294a0bd95e4e973b1e2bf` passed exact-head PR CI `33249768557` across the permanent five-cell matrix;
- canonical product merge `70dd66aba0e68ae710e6ef12605ed153d107bab4` passed canonical product CI `33249920673`;
- Release workflow `33249956337` published GitHub Release `378962445` / tag `v0.3.0` from exact product merge `70dd66a...`;
- documentation-only closeout PR #31 exact head `a9cb5c65598b12e005034b3fec3b356239bbaf29` passed exact-head CI `33250227572` and merged with expected-head protection as canonical closeout merge `123e1ded9d6bdc1aa15767ec7185bfffab5f8eba`;
- the closeout merge has first parent exact product merge `70dd66a...`, second parent exact closeout head `a9cb5c6...`, and a valid GitHub signature;
- canonical post-closeout CI `33250422380` succeeded across all five permanent cells;
- Release verification `33250468134`, job `99095156240`, checked out exact closeout merge and proved historical `v0.3.0` remained published at product source `70dd66a...` without mutation;
- live `v0.3.0` tag, Release ID, asset IDs, sizes, and digests remained unchanged after verification.

020 is distribution-only: it makes the already-canonical root/child DRAFT authoring and explicit recovery surface available in the latest versioned GitHub Release without changing `src/specgrain/` product behavior, release automation, or runtime dependencies.

The fresh post-v0.3 audit `docs/research/post-v0.3-product-audit-2026-08-29.md` found that the distribution discontinuity was closed and initially selected no evidence-supported successor. Repository adoption evidence was too sparse to justify lifecycle mutation, generic editing, stronger multi-writer semantics, executor orchestration, PyPI/broader distribution, hosted/provider scope, or empirical benchmark claims.

A subsequent explicit maintainer request to make the public repository launch surface professional and audit keywords, licensing, security truth, launch presentation, and GitHub metadata supplied fresh adoption/launch evidence. `docs/research/public-launch-readiness-audit-2026-08-29.md` reproduced stale `SECURITY.md` support-line text, stale launch guidance, and missing GitHub description/topics/ruleset metadata, and shaped Specification 021 — Public Launch Readiness Hardening.

Specification 021 is `CLOSED_CANONICAL`.

- exact shaping head `70e511e73feb4e561a8137ffd39e481b393c5ec4` passed PR #33 CI `33256371898` and merged with expected-head protection as canonical shaping merge `5c8cfe64f5481c42c53b6fefa91f92e7a2c68811`;
- canonical shaping post-merge CI `33256530949` succeeded across all five permanent cells before implementation;
- exact implementation head `e95bbafdd2bc66ea67e40e0690c053806acf85c3` passed PR #34 CI `33256769276`; Ubuntu/Python 3.11 job `99111766462` recorded `558 passed in 1.58s` plus successful Ruff, tracked-tree cleanliness, compileall, package build/install, and CLI smoke;
- PR #34 changed exactly six bounded public-launch/status/test paths and no `src/specgrain/`, package/version/dependency, workflow, changelog/release-note, PyPI, hosted/provider, lifecycle/readiness/execution, benchmark-data, or historical-release surface;
- canonical implementation merge `88e174818870cb90d18537b0c8aea810c84fc244` passed canonical CI `33256836246` across all five permanent cells;
- Release verification `33256877372`, job `99112050245`, proved historical v0.3.0 remained at source `70dd66a...` without mutation;
- documentation/status-only closeout head `29f213efef3e1a5c3ed7a68abec17e7a213639d4` passed exact-head PR #35 CI `33257372972` across all five permanent cells and had no submitted reviews or inline review threads at final recheck;
- PR #35 merged with expected-head protection as canonical closeout merge `96df6391a0a6be5267e15f88d768d6c0c70c8bf5`, with a valid GitHub signature, first parent exact implementation merge `88e1748...`, and second parent exact closeout head `29f213e...`;
- canonical post-closeout CI `33257485950` succeeded across all five permanent cells;
- Release verification `33257527462`, job `99113736087`, checked out exact closeout merge and proved historical `v0.3.0` remained published at `70dd66a...` without mutation.

021 hardens only the public launch surface: README first-screen trust signals and stable v0.3.0 install prominence, current `0.3.x` SECURITY support truth, current v0.3.0 launch guidance, and bounded launch regression checks. It does not change product behavior or release identity.

Live GitHub platform settings observed during 021 still have no repository description, no topics, no `main` branch protection, and no repository ruleset. The available repository interface is read-only for those settings, so they are explicit residual platform operations rather than fabricated completed work.

The current program state is `POST_V0.3_OBSERVATION`. No active specification exists. Any future Specification 022 must be shaped from fresh evidence such as concrete user/adoption friction, a reproducible defect/security finding, controlled benchmark data, a demonstrated authoring/recovery limitation, or a clearly bounded interoperability/governance blocker.

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
