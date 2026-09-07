# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification receives implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by a stale backlog.

## Current program state

Specifications 000–026 are `CLOSED_CANONICAL`.

Fresh post-026 evidence has selected **027 — Execution Attempt Identity Contract** as a `SHAPED_CANDIDATE`. Product implementation is blocked until the shaping package becomes canonical and canonical post-shaping CI succeeds across all five permanent cells.

The latest published release remains GitHub Release `378962445` / tag `v0.3.0` at exact historical source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## Canonical program

- **000 — Foundation:** `CLOSED_CANONICAL`.
- **001 — SpecNode Schema:** `CLOSED_CANONICAL`.
- **002 — Lifecycle State:** `CLOSED_CANONICAL`.
- **003 — Refinement Tree:** `CLOSED_CANONICAL`.
- **004 — Grain Readiness:** `CLOSED_CANONICAL`.
- **005 — CLI and Local Store:** `CLOSED_CANONICAL`.
- **006 — Dependency Graph:** `CLOSED_CANONICAL`.
- **007 — Repository Scan:** `CLOSED_CANONICAL`.
- **008 — Context Budget:** `CLOSED_CANONICAL`.
- **009 — Work Packet:** `CLOSED_CANONICAL`.
- **010 — Verification and Evidence:** `CLOSED_CANONICAL`.
- **011 — Method Profiles:** `CLOSED_CANONICAL`.
- **012 — Diff, Drift, and Metrics:** `CLOSED_CANONICAL`.
- **013 — Spec Kit Import:** `CLOSED_CANONICAL`.
- **014 — Agent Adapters:** `CLOSED_CANONICAL`.
- **015 — SpecGrainBench:** `CLOSED_CANONICAL` as framework only; invalidated `SGB-EXP-001` provides no comparative authority.
- **016 — Public Launch:** `CLOSED_CANONICAL`.
- **017 — Native DRAFT CLI:** `CLOSED_CANONICAL`.
- **018 — v0.2.0 Authoring Release:** `CLOSED_CANONICAL`.
- **019 — Native Child-DRAFT Authoring:** `CLOSED_CANONICAL`.
- **020 — v0.3.0 Recursive Authoring Release:** `CLOSED_CANONICAL`.
- **021 — Public Launch Readiness Hardening:** `CLOSED_CANONICAL`.
- **022 — Native Grain Preparation:** `CLOSED_CANONICAL`.
- **023 — Spec Kit Preset-Compatible Import:** `CLOSED_CANONICAL`.
- **024 — Native WorkPacket Export:** `CLOSED_CANONICAL`.
- **025 — Supported Pre-Grain Writer Serialization:** `CLOSED_CANONICAL`.
- **026 — Supported Mutation Cross-Writer Coordination:** `CLOSED_CANONICAL`.
- **027 — Execution Attempt Identity Contract:** `SHAPED_CANDIDATE`; implementation blocked pending canonical shaping qualification.

## Specification 027 selection proof

```text
canonical_base = e4fb1bf5463c72f164ffb842088a07df4a63abb2
observation_head = 67f8562c30f7e2adfa3d93a82ca3cf0091c6f4e6
fixture_blob = 4613b5cea6ee86a9a17bd459de70bee47e7dfe24
observation_ci = 34163498855
observation_result = completed/success across all five permanent cells
reproduced_gap = REPEATED_PACKET_EXECUTION_ATTEMPT_IDENTITY_COLLAPSE
```

The current packet/request/result digests are deterministic content identities. The reproduced gap is that separate retries of identical content have no separate portable occurrence identity.

## Specification 027 bounded outcome

Add a separate immutable/versioned `ExecutionAttemptRecord` that can bind one caller-supplied `attempt_id` to exact existing packet/request/result content identities without changing v1 schemas or granting lifecycle/verification authority.

Expected first implementation surface:

```text
src/specgrain/attempt.py
src/specgrain/__init__.py
tests/test_attempt.py
```

Still explicitly deferred:

- attempt persistence or append ledgers;
- executor/provider/model invocation;
- orchestration and automatic retries;
- lifecycle mutation;
- verification/evidence mutation;
- hidden reasoning or hidden evaluation access;
- fixed donor workflow stages;
- networking/hosted scope;
- runtime dependencies;
- release publication.

## Why this is next

LoopForge and SkillHone were qualified only as design references. Their presence did not select work.

The successor was selected only after a local observation fixture against exact live SpecGrain reproduced a correctness-relevant representational gap and succeeded across the permanent cross-platform CI matrix.

The smallest repair is identity-only. Durable repository persistence remains a future evidence-shaped decision rather than being bundled into this specification.

## Shaping-to-product gate

Implementation begins only after:

1. documentation/governance/evidence-only shaping diff is exact;
2. shaping push CI succeeds across all five cells;
3. shaping PR CI succeeds across all five cells;
4. reviews/comments/threads/mergeability are rechecked;
5. skipped/unavailable review systems are not treated as PASS;
6. expected-head shaping merge succeeds;
7. canonical post-shaping CI succeeds across all five cells;
8. canonical authority is reread;
9. `v0.3.0` remains unchanged.

## Historical release preservation

```text
release = 378962445
tag = v0.3.0
source = 70dd66aba0e68ae710e6ef12605ed153d107bab4
wheel_sha256 = b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817
source_sha256 = e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835
```

No Specification 027 shaping or product work authorizes release publication.

## Continuation discipline

Follow the active specification and task ledger. After closure, return to bounded observation. Do not create the next specification merely to continue activity.