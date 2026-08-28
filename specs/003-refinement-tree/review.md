# Review 003 — Refinement Tree

**Review date:** 2026-08-28  
**Initial exact PR head:** `f3084543f66c22ec2bf7d84522e2498f5f312292`

## Finding F-001 — Cycle detection did not cover all declared refinement edges

**Severity:** material  
**Status:** remediated

The initial implementation detected cycles by following `parent_id` only. The specification described cycles in the refinement relationship more broadly. A malformed pair such as A listing B as a child and B listing A as a child, while both parent pointers were empty, produced reciprocity issues but no `CYCLE` issue.

This made the implementation narrower than the structural contract and could make later diagnostics depend on which redundant relationship field happened to express the cycle.

## Resolution

Cycle adjacency is now the union of every resolvable non-self declared edge:

- child `parent_id` contributes parent -> child;
- parent `children` contributes parent -> child.

Cycle detection uses deterministic iterative DFS with canonical ordering and canonical ring rotation. Self-links remain dedicated self-link issues.

A child-list-only cycle regression test was added. Full local verification after remediation is 116 pytest tests PASS and compileall PASS; Ruff remains NOT RUN because unavailable locally.

## Scope result

No 004 Grain readiness, 006 dependency-DAG, CLI/store, lifecycle mutation, AI refinement, or semantic-decomposition logic is introduced by the remediation.

A fresh exact-head external/repository review remains required before merge.
