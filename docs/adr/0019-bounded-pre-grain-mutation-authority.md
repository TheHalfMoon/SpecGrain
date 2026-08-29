# ADR-0019 — Bounded Pre-Grain Mutation Authority

**Status:** Proposed by Specification 022; effective only after canonical shaping merge

## Context

SpecGrain v0.3.0 can author validated root/child `DRAFT` SpecNodes, but the supported CLI cannot populate the fields required by Grain readiness or advance a candidate into the readiness-evaluated lifecycle states. The deterministic lifecycle graph already defines legal edges, and the readiness engine already validates exact `REFINING` leaf revisions, but legality alone is not mutation authority under ADR-0004.

The next user-visible product gap is therefore authorization, not a new schema or new readiness algorithm.

## Decision

1. Specification 022 authorizes only these ordinary pre-execution lifecycle edges:
   - `DRAFT -> SHAPED`;
   - `SHAPED -> REFINING`;
   - `REFINING -> GRAIN` only after the existing Grain-readiness evaluator returns no blockers for the exact candidate revision and complete current forest.
2. `DRAFT -> SHAPED` may update exactly one existing SpecNode file and may populate only existing schema fields required to express a bounded candidate: `scope_in`, `scope_out`, `acceptance`, `dependencies`, `risk`, `context`, `change_surface`, `evidence`, and `metadata.readiness`. Existing identity, title, outcome, rationale, parent/children structure, labels, method, and schema version are preserved by the initial 022 surface.
3. The native shaping command MUST construct a new immutable `SpecNode`, validate the complete proposed refinement/dependency state before replacement, then replace exactly the selected canonical spec file only if its exact preimage still matches.
4. A supported shaping mutation is a single-file mutation. It MUST refuse a pending ADR-0018 authoring transaction and MUST NOT reuse or widen the multi-file child-authoring journal contract.
5. `SHAPED -> REFINING` is state-only authority. It MUST preserve the semantic revision digest because lifecycle state is intentionally excluded from SpecNode content hashing.
6. `REFINING -> GRAIN` is state-only authority gated by `evaluate_grain_readiness()` on the exact current candidate and forest. A blocked readiness report produces no canonical mutation.
7. 022 does not authorize `GRAIN -> READY`, execution, WorkPacket emission, result ingestion, verification execution, evidence appends, or any later lifecycle transition.
8. 022 does not authorize automatic model-generated content, hidden defaults that fabricate risk/context/evidence claims, provider calls, hosted services, networking, or new runtime dependencies.
9. CLI text and JSON output MUST expose the spec ID, source state, resulting state, semantic revision digest, and for blocked promotion the deterministic readiness blocker codes.
10. Every mutation MUST fail closed on malformed IDs, missing specs, wrong source state, invalid proposed schema/refinement/dependency state, symlink/unsafe store paths, pending authoring recovery, or exact-preimage drift.

## Consequences

- A user can move a native authored DRAFT into the actual deterministic Grain-readiness path without hand-editing `.specgrain/specs/*.json`.
- The pre-execution lifecycle becomes product-reachable while execution authority remains separate.
- Readiness remains authoritative and unchanged; 022 wires existing semantics rather than weakening gates.
- The public CLI gains more explicit arguments, but no readiness fact is silently invented.
- A future request for interactive/AI-assisted shaping, `GRAIN -> READY`, WorkPacket CLI, executor/provider orchestration, or verification/evidence mutation requires fresh evidence and separately shaped authority.
