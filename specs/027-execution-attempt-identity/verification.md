# Verification 027 — Execution Attempt Identity Contract

## Result

Specification 027 product behavior is implemented on canonical `main` and has completed exact-head push, pull-request, and post-product CI qualification across the permanent five-cell matrix.

This document is closeout evidence only. Final `CLOSED_CANONICAL` status is realized only after this closeout package is merged with expected-head protection, canonical post-closeout CI succeeds across all five permanent cells, historical release identity remains unchanged, and canonical authority is reread.

## Selection evidence

```text
canonical_selection_base = e4fb1bf5463c72f164ffb842088a07df4a63abb2
observation_head = 67f8562c30f7e2adfa3d93a82ca3cf0091c6f4e6
fixture_blob = 4613b5cea6ee86a9a17bd459de70bee47e7dfe24
observation_ci = 34163498855
observation_result = completed/success across all five permanent cells
reproduced_gap = REPEATED_PACKET_EXECUTION_ATTEMPT_IDENTITY_COLLAPSE
```

The observation proved that deterministic request/result content identity could not distinguish two separate otherwise-identical execution occurrences. It did not justify persistence or orchestration.

## Shaping evidence

```text
shaping_head = e43a6680808b155010d2a4adeb7839fc417fe086
shaping_push_ci = 34163943883 = completed/success
shaping_pr = 65
shaping_pr_ci = 34164096581 = completed/success
shaping_merge = c1853d5b547c1f1ec14b5042917e824f4ad3975e
post_shaping_ci = 34164197679 = completed/success
```

All five permanent cells succeeded at each recorded CI gate.

PR #65 had no submitted reviews and no inline review threads at the merge gate. Qodo was billing-blocked and CodeRabbit skipped automatic review because of repository star policy; neither was treated as PASS. Cubic supplied only an auto-generated summary, not a submitted approval.

## Product implementation evidence

```text
product_base = c1853d5b547c1f1ec14b5042917e824f4ad3975e
product_head = a795ac0de30ff254ce1697c49690a5f741c75fbe
product_tree = 020fb6b348495893693bf169a155ddb585360727
product_push_ci = 34164406219 = completed/success
product_pr = 66
product_pr_ci = 34164578794 = completed/success
product_merge = 08f3ca9e6bb46386e23a196339d7157362b2a9b6
post_product_ci = 34164674946 = completed/success
```

Product PR #66 changed exactly:

```text
src/specgrain/__init__.py
src/specgrain/attempt.py
tests/test_attempt.py
```

GitHub records merge `08f3ca9e6bb46386e23a196339d7157362b2a9b6` as `verified=true`, reason `valid`, with parents exactly:

```text
c1853d5b547c1f1ec14b5042917e824f4ad3975e
a795ac0de30ff254ce1697c49690a5f741c75fbe
```

PR #66 had `mergeable=true`, no submitted reviews, and no inline review threads at the final gate. Qodo was billing-blocked and CodeRabbit skipped automatic review; neither was treated as PASS. Cubic supplied a descriptive summary only.

## Permanent CI matrix

Every qualified exact-head CI gate recorded above used the permanent matrix:

```text
ubuntu-latest / Python 3.11
ubuntu-latest / Python 3.12
ubuntu-latest / Python 3.13
macos-latest / Python 3.11
windows-latest / Python 3.11
```

The final canonical post-product CI `34164674946` passed Ruff source/tests/examples, editable install, full regression, tracked-tree cleanliness, compile, CLI smoke, package build, built-wheel installation, and installed CLI smoke in all five cells.

## Acceptance mapping

1. **Separate occurrence identity — PASS.** Distinct valid attempt IDs bind identical packet/request/result digests but produce distinct attempt records/digests.
2. **Deterministic serialization — PASS.** Identical normalized attempt content has stable canonical JSON and `attempt_digest`.
3. **Strict ID/digest validation — PASS.** Non-canonical/nil IDs and malformed lowercase SHA-256 bindings fail closed.
4. **Status invariants — PASS.** STARTED/SUCCEEDED/FAILED/BLOCKED/INTERRUPTED enforce the shaped result/error rules.
5. **Progressive binding — PASS.** Separate immutable records may reuse one attempt ID as exact request/result bindings become available.
6. **No verification authority — PASS.** Attempt records expose no `verified`, verification, lifecycle, or SpecState authority field.
7. **v1 compatibility — PASS.** `WORK_PACKET_VERSION`, `EXECUTION_RESULT_VERSION`, and `ADAPTER_PROTOCOL_VERSION` remain 1 and existing AgentRequest/ExecutionResult field sets remain unchanged.
8. **Dependency-free, agent-neutral core — PASS.** Implementation uses Python standard library only and adds no provider/model/IDE/runtime dependency.
9. **Bounded implementation surface — PASS.** Exactly three shaped product paths changed.
10. **Cross-platform exact-head qualification — PASS.** Product push, PR, and canonical post-product CI all succeeded across the five permanent cells.

## Historical release preservation

Reverified after canonical post-product CI:

```text
release_id = 378962445
tag = v0.3.0
source = 70dd66aba0e68ae710e6ef12605ed153d107bab4
wheel_asset = 535129008
wheel_sha256 = b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817
source_asset = 535129009
source_sha256 = e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835
```

Specification 027 did not publish or mutate a release.

## Preserved boundaries

No attempt persistence, automatic attempt-ID generation, executor/provider/model invocation, agent orchestration, lifecycle mutation, automatic retries/backoff/timeouts/leases/heartbeats, verification/evidence mutation, hidden reasoning storage, hidden benchmark/evaluation access, networking, hosted scope, runtime dependency, or release publication was added.

The invalidated `SGB-EXP-001` hidden scorer remained outside inspection/search/materialization/reproduction/use authority.