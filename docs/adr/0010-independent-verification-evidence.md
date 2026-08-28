# ADR-0010 — Independent verification and append-oriented evidence

**Status:** Accepted  
**Date:** 2026-08-28  
**Specification:** `010-verification-evidence`

## Context

Specification 009 introduced `ExecutionResult` as an executor self-report. The constitution requires `VERIFIED` to depend on independent, machine-readable evidence bound to exact specification and implementation revisions. Treating executor success, reported changed paths, or executor-provided evidence references as verification authority would collapse that trust boundary.

## Decision

1. Verification is a deterministic function over the current `SpecNode`, exact `WorkPacket`, exact `ExecutionResult`, independently observed implementation revision/change paths, and independent acceptance/evidence checks.
2. An executor-reported `succeeded` status is necessary but never sufficient. At least one independent acceptance or evidence check is required even when a packet carries no explicit required checks.
3. Changed-scope v1 uses literal repository-relative path or directory-prefix authorization. Globs, regexes, semantic scopes, and filesystem execution are out of scope.
4. A `VerificationReport` binds exact spec revision, packet digest, result digest, implementation revision, observed changed paths, independent checks, and deterministic blocker codes. It does not mutate lifecycle state.
5. Evidence records are immutable hash-chained JSON records under `.specgrain/evidence/<SPEC_ID>/<record-digest>.json`. Failed verification reports may also be appended so the chain preserves re-verification history.
6. Evidence loading is strict and fail-closed: duplicate JSON keys, non-finite numbers, oversized records, symlinks, filename/digest mismatch, forks, cycles, missing links, and unexpected entries are rejected.
7. Appends use exclusive file creation. A post-write chain validation failure rolls back only the just-created candidate so a concurrent append cannot leave a permanent fork through the normal API.
8. `specgrain prove` is read-only and deterministic. It reports the validated chain head and exits successfully only when the latest report is independently verified.

## Consequences

- The executor cannot confer verified state.
- Verification remains portable and provider-neutral.
- Evidence is auditable without introducing a database or service.
- Store v1 gains an optional evidence subtree without changing existing project/spec/policy parsing.
- Strong multi-process locking is intentionally deferred; the append API detects/rolls back normal concurrent forks rather than introducing platform-specific locks.
