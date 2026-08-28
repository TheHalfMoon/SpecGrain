# Foundation Consistency and Gap Review

**Review date:** 2026-08-28  
**Reviewed head:** `bae1df316dd0f143c96f7f21cd6f9bff5efe1bdf`  
**Scope:** all `000-foundation` artifacts and repository governance added on `docs/foundation-plan`

## Review questions

- Is terminology consistent across constitution, domain model, architecture, spec, and roadmap?
- Does the plan accidentally recreate a mandatory epic/story/task hierarchy?
- Is the deterministic/probabilistic trust boundary explicit?
- Is Spec Kit treated as donor/compatibility target rather than architectural parent?
- Is the next implementation unit small enough to honor SpecGrain's own philosophy?
- Are competitive and benchmark claims evidence-disciplined?

## Findings

### F-001 — Next implementation spec was too broad

**Severity:** material  
**Status:** remediated

The initial roadmap grouped schema, lifecycle, dependency primitives, readiness inputs, and serialization into `001-core-model`. That was larger than necessary and contradicted the project's small-batch thesis.

**Resolution:** split the deterministic kernel into `001-specnode-schema`, `002-lifecycle-state`, `003-refinement-tree`, and `004-grain-readiness`. Subsequent roadmap IDs were refined accordingly.

### F-002 — `.specify/` bootstrap layout could imply runtime dependency

**Severity:** material  
**Status:** remediated

The repository uses Spec Kit-style planning files while simultaneously declaring an independent architecture. Without clarification, a contributor could infer that product runtime state depends on Spec Kit.

**Resolution:** add ADR-0003 and explicit `CURRENT.md` language: `.specify/` is bootstrap development scaffolding; product runtime state is planned under `.specgrain/` and must operate without Spec Kit installed.

### F-003 — Grain entity semantics

**Severity:** none  
**Status:** consistent

Across constitution, thesis, and domain model, Grain is consistently a computed/executable state or property of a SpecNode leaf, not a second planning schema.

### F-004 — Verification authority

**Severity:** none  
**Status:** consistent

Executor self-report is consistently separated from deterministic verification and evidence binding. No reviewed document grants an LLM sole authority to create `VERIFIED` state.

### F-005 — Competitive claim discipline

**Severity:** none  
**Status:** consistent

Competitive positioning and launch strategy prohibit unsupported claims. SpecGrainBench is the required evidence path for numeric superiority claims.

### F-006 — Methodology scope

**Severity:** none  
**Status:** consistent

Agile/Lean, PMP-inspired governance, and Six Sigma-inspired loops are treated as tailored methods, not mandatory ceremony frameworks.

## Result

No unresolved critical foundation contradiction was found after applying F-001 and F-002 remediation. The next gate is exact-head PR review because this review was performed before the remediation commit that records the fixes.
