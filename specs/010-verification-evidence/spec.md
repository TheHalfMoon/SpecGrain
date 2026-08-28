# Specification 010 — Verification and Evidence

**Status:** SHAPED  
**Depends on:** 001–009  
**Milestone:** M4 Portable execution boundary / first complete MVP vertical slice

## Outcome

SpecGrain can independently decide whether an exact WorkPacket execution is verified, record that verdict in a deterministic append-oriented evidence chain, and show a read-only proof without trusting executor self-report as verification authority.

## In scope

- independent verification bound to current `SpecNode.revision_digest`;
- exact WorkPacket and ExecutionResult digest binding;
- independently observed implementation revision and changed paths;
- required acceptance/evidence check presence and pass/fail evaluation;
- literal repository-relative change-surface verification;
- executor-reported vs independently observed changed-path mismatch detection;
- explicit blocker codes for failed verification gates;
- at least one independent check requirement;
- deterministic `VerificationReport` normalization;
- immutable hash-chained evidence records;
- strict bounded evidence loading and chain validation;
- append API with no overwrite and concurrent-fork rollback;
- read-only deterministic `specgrain prove SPEC_ID [PATH] [--json]`.

## Out of scope

- executing tests, builds, package managers, Git, or external verifiers;
- trusting executor-reported evidence as independent evidence;
- lifecycle mutation to `VERIFIED`;
- signatures, remote transparency logs, databases, or hosted ledgers;
- glob/regex/semantic change-surface matching;
- automated Git diff discovery;
- method profiles and metrics (011–012);
- provider/model/agent-specific verification logic;
- third-party runtime dependencies.

## Contract

### Independent check evidence

A check record carries:

- `check_id`;
- `passed`;
- stable `evidence_ref`;
- optional detail.

Check execution occurs outside this deterministic kernel. The kernel validates and evaluates the supplied independent results.

### Verification blockers

Stable v1 blockers include:

- stale SpecNode revision;
- result/packet digest mismatch;
- executor status not succeeded;
- executor changed-path report mismatch;
- unscoped observed path;
- required acceptance missing/failed;
- required evidence missing/failed;
- no independent check at all.

### Evidence chain

Each record contains the exact normalized report, optional previous record digest, version, and derived record digest. The file name is the record digest suffix. The latest valid chain head owns current proof status; a later failed re-verification therefore makes `prove` fail until a later independently verified record is appended.

## Acceptance criteria

1. executor `succeeded` alone can never create a verified report.
2. stale SpecNode or mismatched result packet digest blocks verification.
3. independently observed paths must equal executor-reported paths and remain inside the authorized literal path/prefix surface.
4. every packet acceptance criterion and required evidence identifier must have a passing independent check.
5. verification output is permutation-invariant and deterministic.
6. serialized reports re-derive their `verified` value rather than trusting it.
7. evidence records are digest-bound and tampering is rejected.
8. evidence loading rejects duplicate keys, non-finite JSON, symlinks, oversized records, filename mismatch, forks, missing links, cycles, and unexpected entries.
9. appending never overwrites an existing record and rolls back its own candidate when post-write chain validation fails.
10. failed verification reports may be appended and the latest chain head determines proof status.
11. `specgrain prove` text/JSON is deterministic, read-only, and exits 0 only for a verified latest head.
12. no lifecycle/store parser/scheduler/provider behavior changes occur.
13. specifications 001–009 regressions remain green.

## Exit

An executor assertion is only an input. SpecGrain possesses a deterministic independent proof boundary and append-oriented evidence history, closing the first complete MVP vertical slice.
