# Specification 011 — Method Profiles

**Status:** SHAPED  
**Depends on:** 004, 009, 010  
**Milestone:** M5 Adaptive delivery control

## Outcome

`SpecNode.method` selects a deterministic lightweight delivery-control profile that adds only proportionate readiness metadata and evidence requirements while preserving existing Grain readiness, WorkPacket, and independent-verification authority.

## In scope

- canonical `quick`, `dmaic-lite`, `dmadv-lite`, `experiment`, `controlled` names;
- immutable profile records;
- deterministic profile-specific metadata and evidence requirements;
- exact-revision method reports;
- composition with existing Grain readiness through a separate method-aware readiness report;
- existing `evidence.required` as the only evidence-requirement channel;
- public API and tests.

## Out of scope

- mandatory ceremony documents;
- lifecycle mutation;
- automated profile selection/routing from AI reasoning;
- new evidence storage or verification semantics;
- agent/provider selection;
- process metrics (012);
- CLI changes;
- runtime dependencies.

## Acceptance criteria

1. only the five canonical profile names are accepted by the method-profile gate.
2. `quick` adds no new requirement and remains backward compatible.
3. each non-quick profile has a bounded documented metadata/evidence set.
4. missing metadata/evidence yields stable deterministic issues.
5. profile-required evidence must flow through `SpecNode.evidence.required` so 009/010 reuse it.
6. method-aware readiness is ready only when both core 004 readiness and the method profile pass.
7. profile evaluation is immutable, deterministic, and revision-bound.
8. no lifecycle/verification/store/provider behavior changes occur.
9. specifications 001–010 regressions remain green.

## Exit

SpecGrain can proportionately strengthen delivery control for defect, new-design, experiment, and high-risk work without turning the core into a ceremony framework.
