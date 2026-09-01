# Specification 026 — Supported Mutation Cross-Writer Coordination

## Status

Specification 026 is in its terminal `FINAL_RECONCILIATION` gate.

Its disposition is `CLOSED_CANONICAL` if and only if this exact final reconciliation becomes canonical and canonical post-reconciliation CI succeeds across all five permanent cells. Before those live conditions are satisfied, the disposition remains pending. No further Specification 026 product implementation is authorized.

## Outcome

Prevent supported native child authoring and supported pre-Grain persistence from corrupting one another when they overlap on the same local project by making both writer families participate in one project-scoped non-blocking advisory mutation lock while preserving child-authoring journal recovery, pre-Grain exact-preimage/postimage defenses, lifecycle semantics, dependency-free runtime behavior, and the historical `v0.3.0` release.

## Selection evidence

```text
canonical_base = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
canonical_tree = ffe4dbff9658524eedf359451578a9d0446fed4c
observation_head = 3b557f91ec80c147b30f797198d736c2b6b42518
fixture_blob = ba8cea9510d09415a5bd4d2f123a72f5c8affee8
observation_ci = 33441481985
reproduced_gap = SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION
```

The qualifying observation used only supported `shape_draft_spec` and `create_child_draft_spec` APIs. It proved that child authoring could complete after the pre-Grain writer's final exact parent preimage check but before `os.replace`, after which the pre-Grain writer could overwrite the successful parent postimage and leave structurally invalid refinement before failing full-project validation.

The earlier observation head `975c47b288cddbfbde34fbbca06afa77ee86f9af` / CI `33441425481` is not selection evidence because Ruff stopped before test execution.

Selection record: `docs/research/post-025-supported-cross-writer-reproduction-2026-09-01.md`  
Architectural decision: `docs/adr/0021-supported-mutation-cross-writer-coordination.md`

## Authorized and delivered scope

Specification 026 authorized only:

- one project-scoped non-blocking advisory lock shared by supported pre-Grain persistence and native child authoring;
- retention of `.specgrain/tmp/pregrain-mutation.lock` as the advisory anchor;
- placement of the private lock abstraction where `store.py` and `pregrain.py` can share it without circular imports;
- acquisition by `create_child_draft_spec` before authoring journal creation;
- preservation of the complete pre-Grain `_persist` critical section;
- deterministic two-direction contention tests;
- preservation of standard-library-only Ubuntu/macOS/Windows behavior and zero runtime dependencies.

Explicitly outside authority:

- arbitrary manual/non-SpecGrain writer coordination;
- universal project transaction management;
- child-authoring journal schema/version/recovery redesign or automatic hidden recovery;
- blocking waits, retries, sleeps, backoff, timeouts, leases, heartbeats, or stale-owner inference;
- distributed/network/database locking;
- SpecNode schema or semantic revision changes;
- lifecycle expansion;
- executor/provider/result/verification/evidence orchestration;
- automatic context discovery, network access, or model selection;
- Spec Kit runtime integration;
- release publication or mutation of `v0.3.0`;
- hosted scope;
- benchmark or superiority claims;
- any inspection, search, materialization, reproduction, or use of the invalidated `SGB-EXP-001` hidden scorer.

## Functional requirements and verified disposition

### FR-001 — One shared advisory ownership boundary

Supported pre-Grain persistence and `create_child_draft_spec` use the same project-scoped non-blocking operating-system advisory lock. Active contention fails immediately with deterministic `StoreValidationError` semantics. **VERIFIED**.

### FR-002 — Child authoring acquires before transaction state

`create_child_draft_spec` acquires the shared lock before `.specgrain/tmp/authoring-transaction.json` creation. A contention loser creates no journal, child, or parent mutation. **VERIFIED**.

### FR-003 — Pre-Grain persistence remains fully serialized

The Specification 025 `_persist` boundary remains serialized through exact stored-postimage confirmation and full project revalidation. **VERIFIED**.

### FR-004 — Journal recovery remains separate and authoritative

The existing authoring journal remains the durable recovery mechanism after journal creation. Advisory lock contents/presence do not encode transaction or stale-owner state. **VERIFIED**.

### FR-005 — Safe dependency direction

The shared private helper is owned by lower-level `store.py`; `pregrain.py` reuses it without circular imports and no public locking API was added. **VERIFIED**.

### FR-006 — Cross-platform standard-library only

The implementation preserves standard-library advisory primitives and passes permanent CI on Ubuntu, macOS, and Windows. **VERIFIED**.

### FR-007 — Lock anchor safety and lifetime

The lock anchor remains a regular non-symlink file, ownership remains descriptor/process-bound, and existing process-exit/handled-failure/persistent-anchor/unsafe-anchor behavior remains covered. **VERIFIED**.

### FR-008 — Read-only behavior remains unlocked

Read-only project surfaces remain outside the mutation lock. **VERIFIED** through retained regression.

### FR-009 — No hidden contention policy

The deterministic core does not wait, retry, sleep, back off, or infer timeout ownership. **VERIFIED**.

## Shaping evidence

```text
shaping_head = 51079a25cdd0f90a9af1cc34ae7577c72ecdf2d6
shaping_push_ci = 33441902147
shaping_pr = 59
shaping_pr_ci = 33442057984
shaping_merge = d27e000728823e93d2fce9ecd669629a839bfdb3
post_shaping_ci = 33442261877
```

All shaping qualification gates completed `success` across the permanent five-cell matrix before product implementation authority became live.

## Product evidence

```text
final_product_head = 24728cd52b2daef2c83c5b83f084421b8096a11f
product_push_ci = 33443061640
product_pr = 60
product_pr_ci = 33443161567
product_merge = 69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b
post_product_ci = 33485603844
```

Exact product diff changed only:

```text
src/specgrain/store.py
src/specgrain/pregrain.py
tests/test_pregrain_serialization.py
```

The first final-logic head `fd27a146b8c39c777b5fb3f1611b2689a1fad3d5` / CI `33442865903` is explicitly not acceptance evidence because Ruff stopped before tests. The subsequent repair normalized imports only.

At the final product merge gate, exact head/base/three-path scope remained unchanged, `mergeable=true`, submitted reviews were `0`, inline review threads were `0`, and unavailable/skipped/neutral review systems were not treated as PASS. PR #60 merged with expected-head protection.

## Canonical closeout evidence

```text
closeout_base = 69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b
closeout_head = 9b6cd1769c24688172ca435b2a77118fa6f4228c
closeout_push_ci = 33486149999
closeout_pr = 61
closeout_pr_ci = 33486307568
closeout_merge = 2c9b18afb74e2254beb254bb84d9c07feec68aa0
post_closeout_ci = 33486523094
```

The closeout changed exactly eight documentation/governance/evidence paths. Push CI, PR CI, and canonical post-closeout CI all completed `success` across the permanent five-cell matrix.

At the final PR #61 merge gate, exact base/head/eight-path scope remained unchanged, `mergeable=true`, submitted reviews and inline review threads were both `0`, Qodo was billing-blocked, CodeRabbit automatic review was skipped by repository-star policy, and Cubic supplied descriptive auto-generated summary text rather than a submitted approval. None was treated as PASS. PR #61 merged with expected-head protection as signed GitHub merge `2c9b18afb74e2254beb254bb84d9c07feec68aa0`.

## Historical release preservation

```text
tag = v0.3.0
source = 70dd66aba0e68ae710e6ef12605ed153d107bab4
release_id = 378962445
wheel_asset = 535129008
wheel_sha256 = b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817
source_asset = 535129009
source_sha256 = e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835
```

No Specification 026 release work was authorized or performed.

## Risk and recovery

`medium`

The selected change touched two persistence paths and cross-platform advisory locking. Durable recovery remains in the existing journal and no schema migration exists. Reverting the bounded product implementation restores exact Specification 025 behavior without data conversion.

## Final reconciliation authority gate

```text
SHAPING_JUSTIFIED = true
PRODUCT_MERGED = true
POST_PRODUCT_VERIFIED = true
CLOSEOUT_MERGED = true
POST_CLOSEOUT_VERIFIED = true
FURTHER_PRODUCT_WORK_AUTHORIZED = false
```

This reconciliation is the terminal documentation/evidence unit. `CLOSED_CANONICAL` is realized only after the exact reconciliation head is qualified, its PR merge gate is rechecked, it is merged with expected-head protection, and canonical post-reconciliation CI succeeds across all five permanent cells while historical `v0.3.0` remains unchanged.

After that live gate succeeds, return to post-026 observation. Do not create another documentation-only PR solely to record the final reconciliation merge SHA or post-reconciliation CI identifier.