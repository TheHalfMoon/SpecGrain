# SpecGrain Execution Master Plan

This document is the durable continuation plan for SpecGrain. `specs/CURRENT.md` owns the active frontier, and live GitHub state overrides stale text when they disagree.

## Canonical reading order

Before changing the repository, read:

1. `AGENTS.md`;
2. `specs/CURRENT.md`;
3. `.specify/memory/constitution.md`;
4. this file;
5. the active `spec.md`, `plan.md`, and `tasks.md` when an active specification exists;
6. referenced ADRs, contracts, research, evidence, and implementation files.

## Product objective

> Make every software change small enough to understand, execute, verify, recover, measure, and prove.

SpecGrain is an independent, agent-neutral delivery system built around recursively refined specifications. Probabilistic systems may propose work; deterministic validation owns correctness-sensitive state transitions.

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

Specification 000 established the project foundation and constitution. Specifications 000 through 025 are `CLOSED_CANONICAL`. Specification 026 is in its terminal final reconciliation gate; no further Specification 026 product work is authorized.

## Versioned product history

- `v0.1.0` product source: `5eb46db0479cb8707afe070027dab4f3c558849a`; initial program closeout: `7c343841424ca48207f9c42eae725a53213d19e5`.
- Specification 017 — Native DRAFT CLI: `CLOSED_CANONICAL`.
- Specification 018 — v0.2.0 Authoring Release: `CLOSED_CANONICAL`.
- Specification 019 — Native Child-DRAFT Authoring: `CLOSED_CANONICAL`.
- Specification 020 — v0.3.0 Recursive Authoring Release: `CLOSED_CANONICAL`; release source `70dd66aba0e68ae710e6ef12605ed153d107bab4`; Release `378962445`.
- Specifications 021–025: `CLOSED_CANONICAL`.
- Specification 026 — Supported Mutation Cross-Writer Coordination: product and closeout canonical; final reconciliation pending.

The latest published release remains historical `v0.3.0` at exact source `70dd66aba0e68ae710e6ef12605ed153d107bab4` / Release `378962445`.

## Specification 026 selection and shaping proof

```text
canonical_base = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
observation_head = 3b557f91ec80c147b30f797198d736c2b6b42518
fixture_blob = ba8cea9510d09415a5bd4d2f123a72f5c8affee8
observation_ci = 33441481985
reproduced_gap = SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION

shaping_head = 51079a25cdd0f90a9af1cc34ae7577c72ecdf2d6
shaping_push_ci = 33441902147
shaping_pr = 59
shaping_pr_ci = 33442057984
shaping_merge = d27e000728823e93d2fce9ecd669629a839bfdb3
post_shaping_ci = 33442261877
```

The qualifying fixture used only supported public `shape_draft_spec` and `create_child_draft_spec` APIs. The earlier observation head `975c47b288cddbfbde34fbbca06afa77ee86f9af` / CI `33441425481` remains non-selection evidence because Ruff stopped before the fixture executed.

Selection record: `docs/research/post-025-supported-cross-writer-reproduction-2026-09-01.md`.  
Architectural decision: `docs/adr/0021-supported-mutation-cross-writer-coordination.md`.

## Specification 026 product proof

Delivered product surface:

```text
src/specgrain/store.py
src/specgrain/pregrain.py
tests/test_pregrain_serialization.py
```

The implementation shares one project-scoped non-blocking advisory lock between supported pre-Grain persistence and native child authoring. `create_child_draft_spec` acquires the shared lock before journal creation; pre-Grain `_persist` retains its complete critical section. The historical lock anchor, standard-library platform primitives, unsafe-anchor rejection, descriptor/process ownership, exact-preimage/postimage defenses, separate child-authoring journal/recovery contract, lifecycle behavior, read-only behavior, and zero runtime dependencies are preserved.

```text
first_final_logic_head = fd27a146b8c39c777b5fb3f1611b2689a1fad3d5
first_final_logic_ci = 33442865903
first_final_logic_result = Ruff failure before tests; not acceptance evidence

final_product_head = 24728cd52b2daef2c83c5b83f084421b8096a11f
product_push_ci = 33443061640
product_pr = 60
product_pr_ci = 33443161567
product_merge = 69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b
post_product_ci = 33485603844
```

Final push CI, PR CI, and canonical post-product CI completed `success` across all five permanent cells. PR #60 merged with expected-head protection after exact gate qualification; unavailable/skipped/neutral review systems were not treated as PASS.

## Specification 026 canonical closeout proof

```text
closeout_base = 69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b
closeout_head = 9b6cd1769c24688172ca435b2a77118fa6f4228c
closeout_push_ci = 33486149999
closeout_pr = 61
closeout_pr_ci = 33486307568
closeout_merge = 2c9b18afb74e2254beb254bb84d9c07feec68aa0
post_closeout_ci = 33486523094
```

The closeout diff changed exactly eight documentation/governance/evidence paths and no product/test/workflow/dependency/release surface. Push CI, PR CI, and canonical post-closeout CI all completed `success` across the permanent five-cell matrix.

At the final PR #61 gate, exact base/head/eight-path scope remained unchanged, `mergeable=true`, submitted reviews and inline review threads were zero, Qodo was billing-blocked, CodeRabbit automatic review was skipped by repository-star policy, and Cubic produced no submitted approval. None was treated as PASS.

PR #61 was merged by concurrent activity as signed GitHub merge `2c9b18afb74e2254beb254bb84d9c07feec68aa0`, with exact parents `69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b` and `9b6cd1769c24688172ca435b2a77118fa6f4228c`. GitHub REST proves the exact qualified closeout head was merged but does not expose whether the concurrent caller supplied an `expected_head_sha` parameter; this plan makes no claim about that unobservable mechanism.

## Historical release preservation

Historical `v0.3.0` remains unchanged after canonical closeout:

- source `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release `378962445`;
- wheel asset `535129008`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset `535129009`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

Specification 026 did not authorize release work.

## Delivered boundary and explicit non-authority

Specification 026 delivered only cooperative mutual exclusion between pre-Grain persistence and native child authoring through one existing project-scoped non-blocking advisory lock while preserving the journal as the separate durable recovery mechanism.

It does not authorize arbitrary external writer coordination, universal transaction management, journal schema/version/recovery redesign, distributed locking, blocking waits/retries/timeouts/leases, runtime dependencies, lifecycle expansion, executor/provider/result/verification/evidence orchestration, automatic context/network/model behavior, Spec Kit runtime adoption, release publication, hosted scope, benchmark/superiority claims, or any use of the invalidated `SGB-EXP-001` hidden scorer.

## Final reconciliation gate

This reconciliation is the terminal Specification 026 documentation/evidence unit. No further product mutation is authorized.

Required live sequence:

1. verify the exact final reconciliation diff from closeout merge `2c9b18afb74e2254beb254bb84d9c07feec68aa0` is exactly eight documentation/governance/evidence paths;
2. require permanent push CI success across all five cells on the exact final head;
3. open/update the final reconciliation PR and recheck exact head/base/scope/PR CI/reviews/comments/threads/mergeability;
4. record unavailable/skipped/neutral review systems accurately and never treat them as PASS;
5. merge only with expected-head protection;
6. require canonical post-reconciliation CI success across all five permanent cells;
7. reverify historical `v0.3.0` unchanged and re-read canonical authority;
8. if all prior conditions hold, realize `CLOSED_CANONICAL`, set the program state to `POST_026_OBSERVATION`, and perform a bounded observation pass;
9. do not create another documentation-only PR merely to record the final reconciliation merge SHA, post-reconciliation CI run ID, or to flip a stale task checkbox;
10. do not invent Specification 027 merely to continue activity—shape a successor only when fresh reproducible evidence against live canonical truth independently selects a bounded product gap.

## Cross-spec execution rules

1. Live GitHub/repository truth overrides chat handoffs.
2. No force-push, rebase, or destructive shared-history rewriting.
3. Use bounded feature branches and pull requests.
4. Verify exact PR head, checks, threads, comments, scope, and mergeability before merge.
5. Merge with expected-head protection where available.
6. Never claim PASS, VERIFIED, MERGED, COMPLETE, or `CLOSED_CANONICAL` without exact evidence.
7. Re-read canonical `main` after every merge.
8. Prefer smaller native implementations over dependencies without demonstrated need.
9. Do not execute untrusted repository commands merely to inspect a brownfield project.
10. Do not make AI reasoning transcripts repository authority.
11. Preserve residual risks and blockers.
12. External ideas/code require license-aware provenance.
13. Post-v0.1 product work requires a newly shaped specification derived from live reproducible evidence; deferred roadmap categories, audits, external reviewers, and upstream-tool comparisons are not implicit implementation authority.

## Program continuation rule

Complete the exact final reconciliation gate. If its canonical post-merge CI succeeds and release/governance truth remains intact, Specification 026 is closed by the condition recorded in this reconciliation and the program returns to bounded observation. Do not create a recursive meta-closeout solely to record that the condition was realized.
