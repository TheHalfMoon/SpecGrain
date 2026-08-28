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

## Re-verification after remediation

- pytest: **23 passed**;
- `compileall`: **PASS**;
- cross-process hash-seed smoke: **PASS** with identical digest for `PYTHONHASHSEED=1` and `777`;
- ruff: **NOT RUN** because the tool is unavailable in the local execution environment.

A fresh exact-head GitHub diff review and repository checks are still required before merge.
