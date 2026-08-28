# SpecGrain Execution Master Plan

This document is the durable program-level continuation plan for SpecGrain. It exists so a fresh human or AI session can continue from repository truth without depending on chat history.

`specs/CURRENT.md` is authoritative for the active execution frontier. Live GitHub state overrides stale text in this file when they disagree.

## Canonical reading order

Before changing the repository, read:

1. `AGENTS.md`
2. `specs/CURRENT.md`
3. `.specify/memory/constitution.md`
4. `docs/execution-master-plan.md`
5. the active specification's `spec.md`
6. the active specification's `plan.md`
7. the active specification's `tasks.md`
8. referenced ADRs, contracts, research notes, and implementation files

Also consult `docs/roadmap.md` for milestone-level sequencing.

## Product objective

SpecGrain is an independent, agent-neutral software-delivery system built around recursively refined specifications. A specification is refined until a leaf is small enough to become a Grain: one bounded, understandable, context-safe, independently verifiable unit of delivery.

The product is not a GitHub Spec Kit fork and must not regress into a large prompt/template framework. Spec Kit is an upstream influence and compatibility target. Ponytail and Karpathy-inspired skills are planning/design donors. Their useful principles are converted into deterministic or measurable SpecGrain contracts where possible.

Core thesis:

> Make every software change small enough to understand, execute, verify, recover, measure, and prove.

## Durable architecture

The program develops progressively through these capabilities:

```text
Recursive SpecNode model
        ↓
Lifecycle state
        ↓
Refinement tree
        ↓
Grain readiness
        ↓
Local store + CLI
        ↓
Dependency DAG + eligibility
        ↓
Brownfield repository map
        ↓
Context budget
        ↓
Portable WorkPacket
        ↓
Independent verification + evidence
        ↓
Adaptive method profiles
        ↓
Diff / drift / metrics
        ↓
Spec Kit migration + agent adapters
        ↓
SpecGrainBench + public launch
```

The deterministic kernel owns schema, lifecycle legality, structural validation, readiness rules, dependency validation, context budgets, evidence binding, and state-transition preconditions. Probabilistic systems may propose work but cannot silently become authority.

## Completed program frontier

Specifications `000` through `006` are closed canonically on `main`.

Current verified canonical `main` at the time this plan was refreshed:

`85d1bef8ee5c1c8e8d78baa52f509803a78a43d8`

This is the merge of PR #8 for Specification 006.

Completed capabilities include:

- project constitution, domain model, architecture, donor policy, benchmark strategy, launch strategy, and roadmap;
- immutable/versioned SpecNode schema and deterministic digest;
- lifecycle legality separated from transition authorization;
- deterministic recursive refinement validation;
- deterministic Grain readiness gates;
- dependency-free JSON local store;
- `specgrain init` and `specgrain check`;
- dependency graph validation, transitive blockers, eligible Grain computation, advisory dependency-only waves;
- `specgrain next`.

## Active frontier — 007 Repository Scan

Active branch:

`feat/007-repository-scan`

Planning commit at the time this plan was refreshed:

`a879c0f76345dd82b9f3719831f952a25777461a`

Read `specs/007-repository-scan/spec.md`, `plan.md`, `tasks.md`, and ADR-0007 before implementing.

### 007 outcome

Build a deterministic brownfield repository map without requiring `.specgrain/`, executing repository code, running Git subprocesses, following symlinks, or using an LLM.

Repository Scan v1 owns:

- bounded lexical filesystem traversal;
- generated/vendor/control-directory skipping;
- manifest/config/test/language/component signals;
- bounded declared dependency/reuse signals from selected manifests;
- safe ordinary/indirect/absent Git metadata facts;
- deterministic normalized map digest;
- standalone `specgrain scan [PATH] [--json]`.

It must not perform AST/semantic indexing, embeddings, arbitrary content indexing, package resolution, context selection, lifecycle mutation, scheduler changes, evidence verification, or subprocess execution.

### Uncommitted verified candidate at handoff

A local reconstructed workspace contained a 007 implementation candidate with these Git blob hashes:

```text
src/specgrain/repository.py      f87f14bb75af6bcbf5de383e30da4d88db02e9a5
src/specgrain/cli.py             d80d146aafa8c909eb8daf76eb06f9b2001a7ec2
src/specgrain/__init__.py        8fbe2faaa990831f487d26c46d56170787af22b8
tests/test_repository.py         1a9d845080b4677efa0090f6ba1f3bb9e130a3c5
tests/test_repository_cli.py     af781b905868179a3c6a68e20ce55582c541a561
```

Local evidence for that candidate:

- 304 tests collected / PASS;
- `compileall` PASS;
- editable install PASS;
- console/module help parity PASS;
- 0 changed source/test lines over 100 characters;
- Ruff NOT RUN because it was unavailable/offline.

These bytes were **not committed to GitHub** when this execution plan was refreshed. They are continuation evidence only, not canonical repository state. A new session must re-read the live branch and either recover/reproduce those exact bytes or implement 007 from the canonical spec. Never claim 007 COMPLETE, MERGED, or CLOSED_CANONICAL from this local evidence alone.

## Remaining program sequence

The sequence below is canonical at milestone level. Per repository planning rules, only the nearest work should be refined to implementation detail; distant work remains deliberately coarse until its dependencies are real.

### 008 — Context Budget

Implement deterministic context-source records and budget accounting.

Required capabilities:

- source records with provenance and selection reason;
- mandatory vs optional context classification;
- deterministic size/token-cost accounting boundary;
- context budget policy;
- explainable overflow/blocker results;
- integration with repository-map facts without sending the full repository to an LLM.

Exit: required context that cannot fit policy can block progress with an explainable deterministic result.

### 009 — Work Packet

Implement immutable digest-bound WorkPackets and a generic structured execution-result contract.

Packets must carry outcome, acceptance/success criteria, authorized change surface, decisions/assumptions, dependencies, context records, reuse/minimality evidence, risk/recovery requirements, and required evidence. They must not depend on giant vendor-specific prompt text.

Exit: a human or external agent can receive the complete authorized Grain boundary through a portable data contract.

### 010 — Verification and Evidence

Implement independent verification and append-oriented evidence semantics.

Required capabilities include:

- exact SpecNode revision binding;
- exact implementation/result binding;
- acceptance/check evidence;
- changed-scope verification;
- detection of unscoped/drive-by changes;
- evidence records and deterministic `prove` output;
- executor self-report treated as input, never sufficient authority.

Exit: executor assertion alone cannot create `VERIFIED`.

**Specification 010 closes the first complete MVP vertical slice.**

### 011 — Method Profiles

Add incremental delivery-control profiles rather than ceremony-heavy project-management frameworks:

- `quick`;
- `dmaic-lite`;
- `dmadv-lite`;
- `experiment`;
- `controlled`.

Profiles add bounded readiness/evidence requirements and must remain composable with the deterministic kernel.

### 012 — Diff, Drift, and Metrics

Implement spec-aware delivery control and useful measurements:

- authorized change-surface diff;
- spec/repository drift signals;
- first-pass verification rate;
- rework ratio;
- Grain cycle time;
- context efficiency;
- change-scope accuracy;
- unnecessary-change / overproduction signals.

Metrics must be reproducible and should not create process theater.

### 013 — Spec Kit Import

Implement explicit migration from relevant GitHub Spec Kit artifacts.

Preserve useful constitution, technical-context, dependency, and independent-testability information. Produce conversion reports and reject silent data loss. Do not import a mandatory flat `tasks.md` ontology into the SpecGrain core.

### 014 — Agent Adapters

Keep the generic WorkPacket/result protocol canonical. Add thin selected agent integrations only where real use justifies them. Providers and agents are adapters, never the delivery process itself.

### 015 — SpecGrainBench

Build public reproducible comparisons using isolated workspaces and fresh contexts.

Initial comparison arms:

- prompt-only development;
- GitHub Spec Kit;
- SpecGrain.

Add other systems only when fair automation is possible.

Benchmark requirements include:

- identical repository/task baselines;
- contamination preflight;
- fresh isolated workspace/context per arm;
- repeated probabilistic runs where appropriate;
- correctness and acceptance results;
- tokens/context cost;
- cycle time;
- retries/rework;
- regression rate;
- change size/scope accuracy;
- human interventions;
- safety/adversarial cases where relevant;
- publication of unfavorable results as well as wins.

See `docs/benchmark-strategy.md` and `docs/research/planning-donor-synthesis-2026-08-28.md`.

### 016 — Public Launch

Ship the complete open-source launch surface:

- installable versioned release;
- README that demonstrates the product in under one minute;
- zero-to-verified example;
- real brownfield examples;
- Spec Kit migration guide;
- benchmark report;
- contribution guide;
- security/trust documentation;
- architecture/methodology docs;
- release notes and launch assets.

The launch claim must be evidence-based. Do not invent benchmark advantages or claim competitors are obsolete without reproducible proof.

## Cross-spec execution rules

These rules apply through the rest of the project:

1. Live GitHub/repository truth overrides chat handoffs.
2. No force-push, rebase, or destructive history rewriting.
3. Use bounded feature branches and pull requests.
4. Before merging, verify the exact PR head, checks/statuses, review threads, and manual scope review.
5. Merge with an expected-head guard where available.
6. Never claim PASS, VERIFIED, MERGED, COMPLETE, or CLOSED_CANONICAL without exact evidence.
7. Re-read canonical `main` after every merge before starting dependent work.
8. Prefer smaller native implementations over dependencies or abstractions without demonstrated need.
9. Every changed line should trace to the active bounded outcome.
10. Do not turn donor advice into optional prompt prose when it can become a deterministic/measurable contract.
11. Do not execute untrusted repository commands merely to understand a brownfield project.
12. Do not let AI reasoning transcripts become repository authority.
13. Preserve explicit residual risks and blockers instead of hiding them behind green tests.
14. Refine near-term work deeply; do not generate stale implementation-level task lists for distant milestones.

## Planning and research references

The full program is intentionally distributed across specialized canonical documents rather than duplicated into one giant spec. Key references:

- `docs/roadmap.md` — milestone sequence and exit points;
- `docs/product-thesis.md` — product/category thesis;
- `docs/domain-model.md` — recursive specification model;
- `docs/architecture.md` — system boundaries;
- `docs/methodology.md` — Agile/Lean/PMP/Six-Sigma-inspired operating model;
- `docs/donor-policy.md` — provenance and external-project usage;
- `docs/research/planning-donor-synthesis-2026-08-28.md` — Ponytail, Karpathy-inspired, and Spec Kit synthesis;
- `docs/benchmark-strategy.md` — public proof methodology;
- `docs/competitive-positioning.md` — differentiation boundaries;
- `docs/launch-strategy.md` — public launch direction;
- `docs/adr/` — durable architecture decisions;
- `specs/<NNN-...>/` — bounded canonical implementation contracts.

## Fresh-session continuation protocol

A new session should not ask the founder to restate prior work. It should:

1. read the canonical order above;
2. verify live `main`, active branch, PRs, checks, and exact heads;
3. compare repository truth with `specs/CURRENT.md`;
4. continue the next incomplete task in the active spec;
5. close the active spec through exact-head PR evidence;
6. re-read canonical state and immediately begin the next eligible specification;
7. continue until a genuine repository/governance/tooling blocker is reached.

This file is a durable continuation map, not permission to bypass the active spec, task order, evidence gates, or live repository truth.
