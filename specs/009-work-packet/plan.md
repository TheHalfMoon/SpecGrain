# Plan 009 — Work Packet

## Strategy

Add one dependency-free `specgrain.packet` module plus bounded public exports. Compose existing `SpecNode` and Specification 008 context records rather than duplicating readiness, storage, scheduling, or repository behavior.

## Planned source surface

```text
src/specgrain/packet.py
src/specgrain/__init__.py
tests/test_packet.py
```

No CLI, store, lifecycle, readiness, dependency, repository-scan, or project-orchestration change is planned.

## Packet construction

`build_work_packet` accepts:

- one exact `SpecNode`;
- the exact selected `ContextSource` records;
- a passing `ContextBudgetReport`;
- optional explicit decisions, assumptions, and minimality/reuse evidence.

It binds the node revision and context-plan digest and snapshots selected context metadata. The builder is structural only: it does not claim current execution authorization.

## Normalization and digests

All public records are frozen/slotted. Set-like string collections are unique/sorted. Objects are recursively frozen and later detached for serialization. SHA-256 digests cover normalized semantic content excluding their derived digest field.

Strict `from_dict()` reconstructs records and compares declared vs recomputed digest so portable payload tampering fails closed.

## Execution result

Define one provider-neutral result contract with succeeded/failed/blocked status, changed-path claims, reported-evidence references, summary, error semantics, and stable result digest. It is intentionally self-report only; no `verified` field exists.

## Verification

Cover validation, immutability, canonical ordering, spec/context revision binding, permutation invariance, digest sensitivity, JSON round-trip, tamper/unknown-field rejection, finite JSON compatibility, execution-result status/error rules, no verification authority, and absence of provider/model/prompt fields.

Run all 001–009 tests, compileall, editable install, console/module entry-point parity, line-length preflight, and available lint/static checks.

## Scope review

Confirm no executor invocation, provider adapter, prompt template, lifecycle/store/scheduler mutation, evidence verification, changed-scope proof, CLI behavior change, or third-party runtime dependency.