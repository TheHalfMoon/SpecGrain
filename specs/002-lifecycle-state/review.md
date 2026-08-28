# Review 002 — Lifecycle State

**Review date:** 2026-08-28  
**Reviewed implementation head:** `526dcc4de03d2338f1842475573d2064ccb5a45f`

## Review objective

Check that Specification 002 introduces one canonical deterministic lifecycle graph without accidentally creating transition authority or implementing work reserved for Specifications 003 and 004.

## Findings

### F-001 — Structural legality remains separated from authorization

**Status:** PASS

The public API parses states, exposes immutable allowed targets, tests adjacency, and rejects illegal edges. It contains no node-state mutator. A structurally legal edge therefore cannot self-promote a SpecNode.

### F-002 — Existing digest contract remains intact

**Status:** PASS

`SpecNode.state` is normalized to a canonical value but remains excluded from Specification 001 canonical semantic content. The existing golden vector continues to pass.

### F-003 — Exceptional recovery is conservative

**Status:** PASS

`BLOCKED`, `FAILED`, and `STALE` can recover only through `SHAPED` or terminate through `CANCELLED`/`SUPERSEDED`; they cannot jump directly back into protected downstream states.

### F-004 — Scope remains bounded

**Status:** PASS

No refinement-tree validation, Grain readiness, dependency scheduling, CLI/store behavior, execution orchestration, transition history, or evidence authorization was added.

## Result

No unresolved material implementation defect was found in the pre-PR review. Exact-head external/repository checks are still required before merge.
