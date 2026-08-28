# Specification 009 — Work Packet

**Status:** SHAPED  
**Type:** implementation  
**Created:** 2026-08-28  
**Depends on:** `008-context-budget` (`CLOSED_CANONICAL`)

## Problem

SpecGrain can define a Grain and compute a bounded context plan, but it cannot yet hand the complete authorized boundary to a human or external executor through a portable deterministic contract. Without that boundary, integrations drift toward giant prompts, vendor-specific state, or unbound executor claims.

## Outcome

Implement immutable digest-bound `WorkPacket` and `ExecutionResult` contracts. A packet binds the exact SpecNode revision and passing context-plan revision, carries the bounded execution boundary, serializes deterministically, and remains independent from providers/agents. An execution result is structured self-report only and never verification authority.

## Public contract

### `PacketContextSource`

Portable selected-context snapshot containing:

- `source_id`;
- `provenance`;
- `selection_reason`;
- `revision`;
- `size_bytes`;
- `token_cost`.

It intentionally excludes policy-only `requirement` and `priority` fields.

### `WorkPacket`

Frozen/slotted v1 record containing:

- `packet_version=1`;
- `spec_id` and exact `spec_revision`;
- outcome;
- acceptance criteria;
- in/out scope;
- dependencies;
- authorized change surface;
- method;
- risk/recovery object;
- required evidence identifiers;
- exact `context_plan_digest`;
- selected `PacketContextSource` snapshots;
- explicit decisions;
- explicit assumptions;
- minimality/reuse evidence.

`packet_digest` is SHA-256 over canonical normalized packet content excluding the digest itself.

Expose deterministic `content_dict()`, `to_dict()`, canonical compact `to_json()`, and strict `from_dict()` that rejects unknown/missing fields and mismatched declared digest.

### `ExecutionResult`

Frozen/slotted v1 executor self-report containing:

- `result_version=1`;
- exact `packet_digest`;
- status: `succeeded | failed | blocked`;
- non-empty summary;
- changed-path claims;
- reported-evidence references;
- `error_code` required for failed/blocked and forbidden for succeeded.

`result_digest` is SHA-256 over normalized result content excluding the digest itself. Strict `from_dict()` verifies the declared digest.

## Builder

`build_work_packet(node, context_sources, context_report, ...)` must:

- require a `SpecNode` and a passing `ContextBudgetReport`;
- bind `node.revision_digest` and `context_report.plan_digest`;
- require supplied context sources to correspond exactly to the report's selected IDs;
- snapshot exact selected source revisions/costs/provenance;
- carry SpecNode outcome, acceptance, scope, dependencies, change surface, method, risk, and required evidence;
- normalize decisions/assumptions/minimality evidence deterministically;
- perform no lifecycle mutation or execution authorization.

## Determinism and validation

- set-like string collections are unique and canonically sorted;
- duplicate context source IDs fail closed;
- SHA-256 fields must use lowercase `sha256:<64 hex>` form;
- finite JSON floats remain allowed where inherited from valid SpecNode JSON; non-finite floats fail;
- deserialization never trusts a declared digest without recomputing it;
- serialization contains no timestamp, hostname, username, provider, model, or environment path.

## Authority boundary

A packet is an immutable handoff boundary, not proof that a Grain is currently eligible to execute. Callers remain responsible for current readiness/dependency/baseline/authority checks.

An execution result is executor self-report. `status=succeeded` MUST NOT imply `VERIFIED`, acceptance compliance, scope compliance, or evidence sufficiency. Specification 010 owns those determinations.

## Explicit out of scope

- running an executor or subprocess;
- vendor/model/agent adapters;
- prompt templating;
- storing packets/results in `.specgrain`;
- lifecycle mutation;
- verification/evidence authority;
- changed-scope validation;
- CLI orchestration;
- third-party runtime dependencies.

## Acceptance criteria

1. packet construction binds exact spec and context-plan digests.
2. packet content contains the complete bounded Grain handoff fields required by the execution master plan.
3. selected context snapshots are exact and deterministic.
4. packet digest is stable under input permutation and changes when bound semantic content changes.
5. canonical JSON round-trips through strict deserialization with digest verification.
6. tampered packet/result payloads are rejected.
7. execution results distinguish succeeded/failed/blocked and enforce error-code semantics.
8. executor success remains only self-report with no verification field/authority.
9. no provider/model/prompt/runtime dependency becomes canonical.
10. Specifications 001–008 regressions remain green.

## Success criterion

A human or external executor can receive the complete authorized Grain boundary as portable deterministic data, and later verification can bind independently observed evidence to exact packet/result revisions without trusting executor assertion.