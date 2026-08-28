# SpecGrain Repository Instructions

This file defines repository-level operating rules for humans and AI coding agents.

## 1. Mission

SpecGrain makes every software change small enough to understand, execute, verify, recover, and prove. The project is not a generic project-management suite and is not a fork of GitHub Spec Kit. It is an independent, agent-neutral delivery system centered on recursively refined specifications and evidence-backed execution.

## 2. Canonical reading order

Before changing the repository, read in this order:

1. `AGENTS.md`
2. `specs/CURRENT.md`
3. `.specify/memory/constitution.md`
4. The active `spec.md`
5. The active `plan.md`
6. The active `tasks.md`
7. Referenced ADRs, contracts, schemas, and source files

Live repository state overrides stale chat handoffs or external notes.

## 3. Language

Repository technical content MUST be written in English, including code, comments, commit messages, pull-request text, reports, specifications, and reviewer responses.

## 4. Execution discipline

- Work only on tasks that are eligible under the active task order and dependency graph.
- Prefer the smallest coherent change that can be independently verified.
- Do not expand scope merely because an adjacent improvement looks useful.
- Do not mark work complete because code was written. Completion requires the evidence defined by the active spec.
- Do not skip a failed gate. Record the blocker and stop dependent work.
- Re-read canonical `main` after a merge before starting the next specification.
- Do not force-push, rebase shared branches, or rewrite published history.

## 5. Status vocabulary

Use precise states:

- `DRAFT`: intent exists but the spec is not shaped.
- `SHAPED`: outcome and boundaries are understood.
- `REFINING`: the spec is being recursively decomposed.
- `GRAIN`: the leaf passed all Grain readiness gates.
- `READY`: dependencies and repository preconditions are satisfied.
- `RUNNING`: implementation is in progress.
- `VERIFYING`: required evidence is being evaluated.
- `VERIFIED`: all required evidence passed for the exact implementation state.
- `CONTROLLED`: post-verification control conditions are satisfied when required.
- `BLOCKED`, `FAILED`, `SUPERSEDED`, `CANCELLED`, `STALE`: exceptional states.

Never claim `VERIFIED`, `MERGED`, or equivalent without exact repository evidence.

## 6. Grain discipline

A spec leaf is a Grain only when it satisfies the repository's Definition of Grain. At minimum it must have:

- one independently understandable outcome;
- bounded in-scope and out-of-scope behavior;
- explicit acceptance conditions;
- explicit dependencies;
- known risk and recovery expectations;
- a context footprint that fits policy;
- an allowed change surface or justified exception;
- evidence requirements that can independently verify the result.

If a proposed Grain fails these conditions, refine it into smaller specs rather than compensating with a larger prompt.

## 7. Deterministic core, probabilistic helpers

The core state machine, schema validation, dependency checks, readiness decisions, evidence binding, and provenance rules MUST be deterministic. LLMs may propose decomposition, context, implementation, or review conclusions, but deterministic validation owns repository state transitions.

## 8. Provenance and donor code

- External projects are references and donors, not undocumented code sources.
- Before copying or adapting material, verify its license and record provenance.
- Preserve required copyright and license notices.
- GitHub Spec Kit is an upstream influence and compatibility target; SpecGrain MUST remain architecturally independent.
- Do not copy code merely to accelerate implementation when a smaller native implementation is clearer.

## 9. Quality gates

Every implementation PR should state:

- active spec and task IDs;
- exact scope changed;
- tests and static checks run;
- acceptance evidence;
- residual risks or known limitations;
- provenance for adapted external material.

A green CI result is necessary where configured but is not by itself sufficient proof of spec compliance.

## 10. Planning rules

SpecGrain uses progressive refinement. Near-term work may be detailed; distant work should remain coarse until dependencies and evidence make refinement useful. Avoid generating a large backlog of detailed tasks that will become stale before execution.

## 11. Repository evolution

The constitution governs product invariants. ADRs govern durable architectural decisions. Specs govern bounded product changes. Tasks govern execution order. When these disagree, resolve the conflict explicitly rather than silently choosing one.
