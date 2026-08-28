# ADR-0011 — Lightweight composable method profiles

**Status:** Accepted  
**Date:** 2026-08-28  
**Specification:** `011-method-profiles`

## Context

SpecGrain already carries `SpecNode.method` but, before 011, it is descriptive rather than a deterministic delivery-control gate. The methodology calls for quick, DMAIC-lite, DMADV-lite, experiment, and controlled flows without turning PMP or Six Sigma practices into document factories.

## Decision

1. Define five canonical profiles: `quick`, `dmaic-lite`, `dmadv-lite`, `experiment`, and `controlled`.
2. A profile contributes only a small set of non-empty `metadata.method` fields and required evidence identifiers.
3. `quick` contributes no additional ceremony beyond existing Grain readiness/evidence rules.
4. Method-specific evidence requirements must be present in `SpecNode.evidence.required`; therefore WorkPacket 009 and independent verification 010 already carry/enforce them without a parallel evidence system.
5. `evaluate_method_readiness` composes the existing 004 Grain-readiness report with the profile report instead of modifying or replacing the 004 engine.
6. No profile may authorize lifecycle movement, execute checks, select an agent/provider, or weaken core safety/evidence requirements.

## Profile v1 requirements

- `quick`: no additions.
- `dmaic-lite`: baseline, cause, control metadata; `baseline` + `regression` evidence.
- `dmadv-lite`: value, baseline, analysis, design metadata; `baseline` + `verification` evidence.
- `experiment`: hypothesis, resource boundary, decision rule, explicit non-production marker; `experiment-result` evidence.
- `controlled`: rollback, review separation, control metadata; `rollback` + `independent-review` evidence.

## Consequences

The profiles are measurable gates rather than templates. Existing quick-flow projects remain compatible, and stronger methods reuse the existing WorkPacket/verification path rather than creating ceremony-specific execution machinery.
