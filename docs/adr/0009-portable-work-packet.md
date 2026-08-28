# ADR-0009: WorkPacket Is a Portable Digest-Bound Execution Boundary

**Status:** Accepted  
**Date:** 2026-08-28

## Context

Specification 009 turns a ready Grain boundary into data that a human or external executor can consume. The execution boundary must remain independent from model vendors, agent products, prompt templates, and transcript semantics. It must also preserve exact provenance so later verification can distinguish the authorized packet from executor self-report.

## Decision

WorkPacket v1 is an immutable, deterministic, JSON-compatible contract bound to:

- the exact `SpecNode.revision_digest`;
- the exact passing `ContextBudgetReport.plan_digest`;
- snapshots of only the selected context sources and their revisions;
- the Grain outcome, acceptance criteria, scope, dependencies, authorized change surface, method, risk/recovery data, required evidence, decisions, assumptions, and minimality evidence.

The packet digest is SHA-256 over normalized packet content excluding the digest itself.

A generic `ExecutionResult` is also immutable and digest-bound. It records executor-reported status, summary, changed paths, reported evidence references, and an error code when failed or blocked.

## Authority boundary

A WorkPacket does not authorize lifecycle movement by itself. Its builder does not replace readiness, dependency eligibility, repository-baseline, or execution-authority checks.

An `ExecutionResult(status="succeeded")` is only executor self-report. It cannot create `VERIFIED`, satisfy acceptance evidence, or prove changed-scope compliance. Specification 010 owns independent verification and evidence authority.

## Portability rules

- no provider/model/IDE/agent field is required by the canonical contract;
- no giant procedural prompt is canonical packet state;
- strict deserialization rejects unknown fields and mismatched declared digests;
- canonical JSON is deterministic and environment-free;
- selected context is represented by compact source metadata, not arbitrary file contents.

## Consequences

Adapters can translate the same packet into a terminal view, human handoff, or vendor-specific execution request without changing the kernel. Later verification can bind evidence to exact packet and result digests while treating executor claims as untrusted input.