# Specification 000 — Foundation

**Status:** SHAPED  
**Type:** product/governance  
**Created:** 2026-08-28

## Problem

SpecGrain is a new repository with a strong product hypothesis but no canonical rules. Beginning implementation before the core domain model, trust model, methodology boundaries, and roadmap are explicit would invite the same over-planning, context drift, and architecture churn the product is intended to prevent.

## Outcome

Establish a coherent, reviewable foundation that makes the first implementation specification (`001-core-model`) unambiguous enough to plan without re-litigating product identity.

## In scope

- repository governance and constitution;
- product thesis and non-goals;
- recursive SpecNode / Grain domain model;
- lifecycle and evidence concepts;
- architecture boundaries;
- methodology and method-profile philosophy;
- competitive positioning;
- donor/provenance policy;
- benchmark strategy;
- progressive roadmap;
- launch thesis;
- execution rules for future agents.

## Out of scope

- product source code;
- CLI implementation;
- schema implementation;
- agent execution adapters;
- benchmark execution;
- marketing claims of superiority;
- copying donor code.

## Functional requirements

### FR-001 Independent identity

The foundation MUST state that SpecGrain is an independent project rather than a Spec Kit fork.

### FR-002 Recursive primitive

The foundation MUST define one recursive canonical planning primitive and MUST NOT require epic/story/task taxonomy in the core.

### FR-003 Grain readiness

The foundation MUST define Grain as an executable leaf that passes explicit readiness conditions, not merely a small task label.

### FR-004 Evidence boundary

The foundation MUST separate executor assertions from verification state and define evidence binding to exact revisions.

### FR-005 Deterministic trust core

The foundation MUST identify which control-plane decisions require deterministic validation.

### FR-006 Context policy

The foundation MUST treat execution context as bounded, attributable input that can affect readiness.

### FR-007 Adaptive methodology

The foundation MUST define how Agile/Lean, project-management, and Six Sigma ideas are adopted without mandatory ceremony.

### FR-008 Brownfield priority

Existing repositories MUST be a first-class product environment.

### FR-009 Progressive roadmap

The roadmap MUST avoid detailed far-future task generation and define the next implementation spec explicitly.

### FR-010 Evidence-backed competition

The launch and benchmark strategy MUST prohibit unsupported superiority claims.

## Non-functional requirements

- Foundation documents must use consistent vocabulary.
- Canonical technical content is English.
- The foundation must be understandable without chat history.
- Durable decisions should be captured in ADRs.
- External references must be clearly distinguished from copied material.

## Acceptance criteria

1. A new contributor can explain the difference between `SpecNode`, `Grain`, `WorkPacket`, `ExecutionRun`, and `EvidenceRecord` from repository docs alone.
2. The repository documents why it is not a Spec Kit fork.
3. The constitution explicitly prohibits AI-only authority over verified state.
4. The roadmap identifies `001-core-model` as the next implementation spec.
5. The competitive document identifies recursive readiness + evidence + context accounting as the differentiation target.
6. The benchmark document defines reproducibility and anti-gaming constraints.
7. `AGENTS.md` gives future agents an unambiguous canonical reading and execution order.

## Success criterion

Foundation can be merged without unresolved contradictions that would materially change the scope of `001-core-model`.
