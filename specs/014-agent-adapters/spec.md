# Specification 014 — Agent Adapters

**Status:** SHAPED

## Outcome

Provide a thin deterministic adapter boundary that lets an external human or coding agent consume the canonical `WorkPacket` and return data normalized into the canonical `ExecutionResult` contract without becoming part of SpecGrain's deterministic trust authority.

## In scope

- immutable adapter request envelope;
- canonical `generic-json` request representation;
- canonical `generic-markdown` request representation;
- exact WorkPacket digest binding in every request;
- strict external-result JSON/object parsing;
- adapter-controlled packet binding when producing `ExecutionResult`;
- deterministic serialization and request digest;
- bounded public exports.

## Out of scope

- invoking an agent, model, CLI, subprocess, IDE, or hosted API;
- credentials, authentication, network access, streaming, tool calls, or sessions;
- vendor/model-specific SDK dependencies;
- provider-specific prompts or lifecycle semantics;
- verification, evidence authority, or lifecycle mutation;
- vendor adapters without demonstrated repository adoption demand.

## Contract

### Request

An `AgentRequest` is immutable and carries:

- protocol version;
- adapter kind;
- packet digest;
- media type;
- deterministic payload;
- derived request digest.

`generic-json` payload is the exact canonical `WorkPacket.to_json()` representation.

`generic-markdown` is a deterministic human/agent-readable envelope that embeds the same canonical packet JSON and explicitly states that the receiver returns an executor self-report, not verification.

### Result normalization

`parse_agent_result(packet, payload)` accepts only the executor-report fields owned by `ExecutionResult`: status, summary, changed paths, reported evidence, and conditional error code. The adapter injects the canonical packet digest itself. Unknown fields, invalid JSON, duplicate JSON keys, non-finite JSON values, invalid status/error combinations, or malformed field types fail closed.

The external payload MUST NOT supply `packet_digest`, `result_digest`, `verified`, or any verification/evidence authority field.

## Acceptance

1. Identical WorkPackets and adapter kinds produce byte-identical request payloads and request digests.
2. Both request formats bind the exact WorkPacket digest.
3. Result normalization cannot spoof a packet digest or verification state.
4. A normalized result is a canonical `ExecutionResult` and retains executor-self-report semantics.
5. The implementation introduces no runtime dependency, network/process execution, store/lifecycle mutation, or vendor-specific coupling.
