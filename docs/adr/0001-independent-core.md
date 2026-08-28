# ADR-0001: Build an Independent Core Instead of Forking Spec Kit

**Status:** Accepted  
**Date:** 2026-08-28

## Context

GitHub Spec Kit is a mature MIT-licensed spec-driven development project and a valuable source of lessons, compatibility opportunities, and potentially reusable implementation patterns.

SpecGrain, however, changes the core planning model from a primarily staged spec/plan/tasks flow to recursive SpecNodes, computed Grain readiness, execution DAGs, context budgets, and evidence-bound state transitions.

## Decision

SpecGrain will be an independent repository and architecture, not a GitHub fork of Spec Kit.

Spec Kit will be treated as:

- an upstream design reference;
- a compatibility and migration target;
- a possible MIT-licensed donor for narrowly selected components with recorded provenance.

## Consequences

Positive:

- product identity is independent;
- core domain model is not constrained by upstream compatibility;
- Git history represents SpecGrain's own architecture;
- migration can be designed explicitly rather than through inherited assumptions.

Costs:

- bootstrap work that a direct fork might initially provide must be implemented or selectively adapted;
- compatibility requires explicit tests;
- donor provenance must be maintained.

## Rejected alternative

Fork Spec Kit and progressively replace its workflow. Rejected because the inherited architecture and public positioning would obscure the core conceptual break SpecGrain is intended to test.
