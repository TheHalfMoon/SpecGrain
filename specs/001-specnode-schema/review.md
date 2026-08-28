# Review 001 — SpecNode Schema

**Review date:** 2026-08-28  
**Initial implementation head:** `2132979aa91f05db1eedab7a5af5d5f4aa24f2ef`

## Scope review

The implementation remains bounded to the Specification 001 schema/serialization contract. It introduces no lifecycle transition rules, recursive tree validation, dependency scheduling, Grain readiness, CLI behavior, repository scanning, WorkPackets, agent execution, or evidence-ledger state.

## Findings

### F-001 — Canonicalization contract lacked an explicit version

**Severity:** material  
**Status:** remediated

The initial implementation hashed normalized semantic content but did not encode which schema/canonicalization contract gave those bytes meaning. A future incompatible canonicalization change could therefore make historical digests ambiguous.

**Resolution:** add public `SPECNODE_SCHEMA_VERSION = 1`, persist `schema_version` on every SpecNode, reject unsupported versions, and include the version in canonical semantic content and the revision digest.

### F-002 — Generic JSON settings did not provide byte-level interoperability evidence

**Severity:** material  
**Status:** remediated

`json.dumps(sort_keys=True, ...)` is deterministic for the tested Python implementation but the digest is a trust primitive that may later be reproduced by other runtimes. Generic JSON serializer settings alone do not prove identical bytes, especially for numeric rendering.

**Resolution:** define schema-v1 canonicalization as a byte-level contract and add a golden vector that includes set-like ordering, nested list/object data, Unicode, and finite floating-point rendering. Any compatible implementation must reproduce the exact bytes and SHA-256. A change to those bytes requires a future schema-version change.

## Re-verification after remediation

- pytest: **24 passed**;
- `compileall`: **PASS**;
- cross-process hash-seed smoke: **PASS** with identical digest for `PYTHONHASHSEED=1` and `777`;
- golden canonical JSON vector: **PASS** with digest `sha256:30ce9cd0616d9d5ed87e181265b73f8fad61e8dd5a1b3309a8f3f8b61a357b1c`;
- ruff: **NOT RUN** because the tool is unavailable in the local execution environment.

A fresh exact-head GitHub diff review and repository checks are still required before merge.
