# SpecGrain Constitution

**Version:** 0.1.0  
**Ratified:** 2026-08-28  
**Status:** Active foundation constitution

## Preamble

SpecGrain exists to reduce the failure modes of large, ambiguous, context-heavy software changes executed by humans or AI agents. The project treats specification granularity, evidence, flow, and recoverability as engineering concerns rather than documentation preferences.

## Principle I — The specification is recursive

A specification is the fundamental planning primitive. A spec may contain smaller specs of the same semantic kind. Artificial hierarchy names such as epic, feature, story, task, and subtask MUST NOT be required by the core model. A leaf becomes executable only when it satisfies the Definition of Grain.

## Principle II — Grain before execution

No unit may enter execution merely because it appears on a task list. A candidate leaf MUST pass deterministic readiness rules covering outcome isolation, scope, acceptance, dependencies, risk, context fit, change surface, evidence, and recovery.

When work is too large, the default remedy is further refinement, not a larger context window or a longer agent prompt.

## Principle III — Evidence over assertion

Agents and humans may propose that work is complete; they do not confer verified state. `VERIFIED` requires machine-readable evidence bound to the exact spec revision and implementation revision. The verifier must distinguish test success, scope compliance, acceptance compliance, provenance, and unresolved risk.

## Principle IV — Small batches and bounded context

SpecGrain optimizes for small, independently verifiable batches. Context is a finite engineering resource. Context selection MUST be relevant and explainable, and context budgets SHOULD be measurable. Unbounded context growth is a design smell and may invalidate Grain readiness.

## Principle V — Adaptive method, minimal ceremony

SpecGrain borrows useful practices from Agile, Lean, PMI project management, Six Sigma, DevOps, TDD, BDD, and related disciplines without forcing a ceremony framework. Method selection MUST be proportionate to work type and risk. Process that does not improve value, evidence, safety, flow, or learning SHOULD be removed.

## Principle VI — Progressive refinement

Near-term work may be precise while distant work remains intentionally coarse. Plans MUST be refined as evidence arrives. Stale detail is waste. The project SHOULD prefer rolling refinement over comprehensive up-front task generation.

## Principle VII — Deterministic control plane

Schema validation, graph correctness, readiness, state transitions, provenance binding, and evidence integrity MUST remain deterministic and testable. Probabilistic AI may assist but MUST NOT be the only authority for a state transition that affects correctness or trust.

## Principle VIII — Agent and vendor neutrality

SpecGrain MUST define portable work packets and result contracts. No model vendor, coding agent, IDE, hosted service, or proprietary protocol may become necessary for the core workflow. Integrations are adapters around the core.

## Principle IX — Brownfield first

Existing repositories are a first-class environment. SpecGrain MUST understand and respect existing architecture, conventions, tests, ownership, and change boundaries before proposing broad new structure. Greenfield-only assumptions are defects.

## Principle X — Measure outcomes and process quality

The project SHOULD measure a compact set of useful indicators such as first-pass verification, rework ratio, Grain cycle time, context efficiency, drift, escaped defects, and change-scope accuracy. Metrics MUST be used to learn and improve, not to reward activity volume.

## Principle XI — Reversibility and blast-radius control

A Grain SHOULD have a comprehensible failure and recovery boundary. High-risk work MUST carry stronger evidence and recovery requirements. The scheduler must not allow dependent work to proceed through a known failed or blocked prerequisite.

## Principle XII — Open provenance

SpecGrain is open source. External ideas and code MUST be attributed according to their licenses and material provenance. Benchmarks MUST disclose methodology sufficiently for independent reproduction. Competitive claims MUST be evidence-backed.

## Governance

1. This constitution is the highest project-level product-governance document.
2. A change that violates a principle requires a constitution amendment, not a hidden exception.
3. Amendments require a dedicated pull request that states motivation, compatibility impact, migration impact, and affected specs.
4. Semantic versions apply to this constitution: major for incompatible principle changes, minor for new principles or materially stronger obligations, patch for clarifications.
5. Specs and ADRs MUST identify constitution exceptions or unresolved tensions before implementation begins.
