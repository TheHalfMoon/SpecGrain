# Review 005 — CLI and Local Store

**Review date:** 2026-08-28  
**Reviewed implementation head:** `e454112e265fe0e145a5971b4db372b3b2df3572`

## Objective

Verify that Specification 005 exposes only the bounded repository-local `init`/`check` product surface, preserves the deterministic 001–004 kernel, and does not pull dependency scheduling, repository intelligence, lifecycle mutation, evidence storage, agent execution, or third-party runtime dependencies into M2 prematurely.

## Exact-diff result

No material implementation defect remains after the pre-PR hardening commits.

The uploaded source surface is limited to:

- dependency-free JSON store v1;
- strict manifest/policy/spec loading;
- canonical path and symlink rejection;
- atomic same-parent staged initialization for normal write failures;
- read-only structural/readiness checking;
- `report` / `enforce` readiness policy;
- stdlib `argparse` CLI;
- module and console entry points;
- bounded public store exports.

The exact diff contains no:

- dependency-DAG algorithm or ready-set computation;
- repository source scan;
- lifecycle-state write API;
- readiness-report transition capability;
- evidence ledger/storage semantics;
- YAML parser;
- subprocess or command execution;
- agent/provider integration;
- generic spec mutation API;
- third-party runtime dependency.

## Pre-PR hardening

Before this review, boundary-focused tests were added for repository/store symlink handling and fail-closed unexpected CLI exceptions. Import ordering was normalized without changing behavior. The final local verification is 236 pytest tests PASS plus compile, editable-install, entry-point, and product-smoke checks.

## Residual boundary R-001 — Concurrent initializer coordination

**Status:** accepted non-blocking boundary for 005

005 guarantees staged initialization and no partially canonical `.specgrain` for the normal write-failure contract defined by this specification. It does not claim to provide an inter-process transaction/lock protocol against a separate actor concurrently creating or mutating `.specgrain` during the final initialization race window.

That stronger concurrency guarantee belongs with the future state-mutation/persistence authority rather than being implied by this read-mostly local-store milestone. No 005 acceptance criterion claims cross-process serialization.

## Conclusion

Specification 005 is ready for a bounded pull request from this reviewed product head. A fresh exact-head review is still required after the review-record commit because that documentation commit will move the PR head.
