# ADR-0002: Use One Recursive Spec Primitive

**Status:** Accepted  
**Date:** 2026-08-28

## Context

Many planning systems encode mandatory levels such as initiative, epic, feature, story, task, and subtask. These labels can be useful views, but they also hard-code organizational ceremony and make decomposition semantics depend on naming conventions.

SpecGrain needs decomposition that can continue until execution safety and verification conditions are satisfied.

## Decision

The canonical planning entity is `SpecNode`. A `SpecNode` may have child `SpecNode` objects recursively.

`Grain` is a computed status/property of an executable leaf that passes readiness gates; it is not a separate planning schema.

Organizations may add labels or projections such as epic/story, but the core does not require them.

## Consequences

- decomposition depth is determined by work, not framework vocabulary;
- validators can apply the same structural rules recursively;
- migration from other planning hierarchies maps labels to metadata rather than core types;
- the UI/CLI must clearly distinguish a generic leaf from a leaf that has actually passed Grain readiness.
