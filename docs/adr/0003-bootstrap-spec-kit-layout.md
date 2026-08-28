# ADR-0003: Keep Bootstrap Spec Kit Layout Separate from Product Runtime

**Status:** Accepted  
**Date:** 2026-08-28

## Context

SpecGrain is using a Spec Kit-style repository planning layout during its own bootstrap, including `.specify/memory/constitution.md` and `specs/<id>/spec.md`, `plan.md`, and `tasks.md`.

Without an explicit boundary, contributors could incorrectly infer that the SpecGrain product runtime depends on `.specify/` or that SpecGrain is implemented as a Spec Kit extension.

## Decision

The `.specify/` directory in the SpecGrain repository is development-process scaffolding for building SpecGrain itself. It is not the product's canonical runtime format and does not create an architectural dependency on Spec Kit.

The planned SpecGrain product state root is `.specgrain/`.

The product must remain able to run without Spec Kit installed. Future Spec Kit support belongs behind an importer/compatibility boundary.

## Consequences

- bootstrap governance may continue to use familiar spec/plan/tasks artifacts;
- product tests must never assume `.specify/` exists in a user's project;
- `.specgrain/` schemas and behavior are defined by SpecGrain specifications, not by Spec Kit templates;
- future migration tooling must make source/target semantics explicit.
