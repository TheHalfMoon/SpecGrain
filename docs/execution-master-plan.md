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
- Specification 017 — Native DRAFT CLI: `CLOSED_CANONICAL`.
- Specification 018 — v0.2.0 Authoring Release: `CLOSED_CANONICAL`.
- Specification 019 — Native Child-DRAFT Authoring: `CLOSED_CANONICAL`.
- Specification 020 — v0.3.0 Recursive Authoring Release: `CLOSED_CANONICAL`; product/release source `70dd66aba0e68ae710e6ef12605ed153d107bab4`; GitHub Release `378962445`.
- Specification 021 — Public Launch Readiness Hardening: `CLOSED_CANONICAL`.
- Specification 022 — Native Grain Preparation: `CLOSED_CANONICAL`; bounded `DRAFT -> SHAPED -> REFINING -> GRAIN` preparation.
- Specification 023 — Spec Kit Preset-Compatible Import: `CLOSED_CANONICAL`; bounded path-bound identity fallback for template-light read-only imports.
- Specification 024 — Native WorkPacket Export: `CLOSED_CANONICAL` when this final reconciliation becomes canonical; bounded read-only native export from one dependency-eligible stored `GRAIN`.

The latest published release remains `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## Closed frontier — Specification 024

Fresh deterministic interoperability evidence selected exactly one bounded native handoff repair.

Selection proof:

```text
canonical_base = f2e8378dcba0cfea2beedc6da61324b0c3fea95e
observation_head = 95e5358ed420cd2e6fbd0bc7c56690763cea1283
fixture_blob = 58cb3e355468f6bcd7de63b676dba52361ff0dd7
ci_run = 33416110142
ci_result = completed/success across all five permanent cells
```

Specification 024 delivered only:

```text
specgrain packet <spec_id> [path] --context-sources <json-file> [--json]
```

The command is constrained to an exact stored dependency-eligible `GRAIN`, explicit bounded ContextSource records, the Grain's existing token budget, existing context-budget primitives, and existing `build_work_packet` serialization/digest semantics. It is read-only and adds no lifecycle advancement, execution, verification, evidence mutation, provider, network, LLM, runtime-dependency, or release authority.

### Canonical shaping proof

- shaping head `043abdf8f15f688cdbae746c0abd83dda74d0dae`;
- push CI `33416602621` and PR CI `33416635970` — success across five cells;
- shaping PR #49 expected-head merge `440a8b14459ade2fe8235cc873229dd87ba926b5`;
- canonical post-shaping CI `33416908615` — success across five cells.

### Product proof

- final implementation head `7e1db87f69108fc8693b987e77d20f92e4f46866`;
- push CI `33421885016` and PR CI `33422062846` — success across five cells;
- Ubuntu/Python 3.11 final push evidence — `592 passed` plus cleanliness, compile, source CLI smoke, build, wheel reinstall, and installed CLI smoke;
- exact product diff: `README.md`, `src/specgrain/cli.py`, `tests/test_workpacket_cli.py`, `tests/test_launch.py`, `tests/test_repository_cli.py`; the last two were test-only compatibility exceptions with no runtime authority expansion;
- PR #50 had no submitted reviews or inline review threads; Qodo was billing-blocked, automatic CodeRabbit review was skipped by repository-star policy, and Cubic was descriptive only;
- PR #50 expected-head product merge `1666ba8c135ee8575f1546019ab592db32947dd2`;
- canonical post-product CI `33422235433` — success across five cells.

### Canonical closeout proof

- exact closeout head `12f89e22955efc632f62d52f2f0396430f4bee01`;
- exact closeout diff changed only seven authorized governance/evidence/status paths;
- closeout push CI `33422814705` and PR CI `33422950629` — success across five cells;
- PR #51 had no submitted reviews or inline review threads and was mergeable before merge; Qodo was billing-blocked, automatic CodeRabbit review was skipped by repository-star policy, and Cubic was descriptive only;
- PR #51 expected-head closeout merge `519680c5cf378dfcb4673cf7292bcf51e9c36af1`;
- closeout merge parent `1666ba8c135ee8575f1546019ab592db32947dd2`;
- canonical post-closeout CI `33423123321` — success across all five permanent cells.

Historical `v0.3.0` remains unchanged at source `70dd66aba0e68ae710e6ef12605ed153d107bab4`, Release `378962445`, wheel digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`, and source digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

The SGB-EXP-001 experiment remains `INVALIDATED_ORACLE_REVEALED_PRE_FREEZE`; it produced no valid comparative dataset, supports no superiority claim, and selected no product work.

The bounded multi-writer race retained after Specification 022 remains an explicit residual outside Specification 024 authority.

## Post-024 observation frontier

When this final reconciliation becomes canonical, Specification 024 is `CLOSED_CANONICAL` and no product specification is active.

No further product mutation is authorized by Specification 024. The program returns to observation/evidence gathering.

## Explicitly unselected after Specification 024

Without fresh canonical shaping, do not implement:

- `GRAIN -> READY` or later lifecycle mutation;
- executor/provider invocation or result orchestration;
- verification execution or evidence mutation;
- automatic context discovery, source-content packing, retrieval, network access, or LLM context selection;
- stronger multi-writer/recovery concurrency;
- PyPI publication or broader distribution changes;
- hosted SaaS, dashboard, account/enterprise, or provider runtime scope;
- Spec Kit preset/hook/extension/bundle/workflow execution or architectural adoption;
- arbitrary Markdown semantic inference;
- empirical benchmark superiority claims without a reproducible completed dataset.

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

## Program continuation rule

After this final reconciliation becomes canonical, return to observation/evidence gathering. Do not invent a successor merely to continue activity. Shape the next specification only when fresh reproducible evidence against live canonical truth selects a bounded product gap.
