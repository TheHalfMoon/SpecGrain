# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–025 are `CLOSED_CANONICAL`. **026 — Supported Mutation Cross-Writer Coordination** has canonical shaping, a merged bounded product implementation, and successful canonical post-product five-cell CI; it is now `PRODUCT_VERIFIED_CLOSEOUT_PENDING`. No further Specification 026 product work is authorized. The latest published release remains GitHub Release `378962445` / tag `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## M0 — Foundation

**000 — Foundation** established the constitution, product thesis, domain model, architecture, methodology, competitive boundaries, donor policy, benchmark strategy, launch thesis, and program sequence.

## M1 — Deterministic specification kernel

- **001 — SpecNode Schema:** immutable/versioned recursive data model and semantic digest.
- **002 — Lifecycle State:** legal states and deterministic transition validation.
- **003 — Refinement Tree:** recursive structural integrity and parent/child rules.
- **004 — Grain Readiness:** deterministic Definition of Grain and structured blockers.

## M2 — Local product surface

- **005 — CLI and Local Store:** `init`, `check`, repository-local `.specgrain/` storage.
- **006 — Dependency Graph:** dependency validation, blockers, eligible Grains, waves, `next`.

## M3 — Brownfield context

- **007 — Repository Scan:** bounded deterministic repository map.
- **008 — Context Budget:** revision-bound source accounting and required-context blockers.

## M4 — Portable execution boundary

- **009 — Work Packet:** immutable digest-bound WorkPacket and execution-result contracts.
- **010 — Verification and Evidence:** exact-revision independent verification, changed-scope checks, evidence records, and `prove`.

Specification 010 closed the first complete MVP vertical slice at the API layer.

## M5 — Adaptive delivery control

- **011 — Method Profiles:** `quick`, `dmaic-lite`, `dmadv-lite`, `experiment`, `controlled`.
- **012 — Diff, Drift, and Metrics:** scope analysis, drift signals, and delivery metrics.

## M6 — Ecosystem interoperability

- **013 — Spec Kit Import:** `CLOSED_CANONICAL`.
- **014 — Agent Adapters:** generic deterministic WorkPacket/result adapter boundary.

## M7 — Public proof

- **015 — SpecGrainBench:** reproducible experiment ledger and contamination/comparability preflight.
- **016 — Public Launch:** versioned package, cross-platform CI, public examples/guides/trust surfaces, release notes/assets, and `v0.1.0` publication.

## Post-v0.1 — Evidence-shaped product adoption

- **017 — Native DRAFT CLI:** `CLOSED_CANONICAL`.
- **018 — v0.2.0 Authoring Release:** `CLOSED_CANONICAL`.
- **019 — Native Child-DRAFT Authoring:** `CLOSED_CANONICAL`.
- **020 — v0.3.0 Recursive Authoring Release:** `CLOSED_CANONICAL`; source `70dd66aba0e68ae710e6ef12605ed153d107bab4`; Release `378962445`.
- **021 — Public Launch Readiness Hardening:** `CLOSED_CANONICAL`.
- **022 — Native Grain Preparation:** `CLOSED_CANONICAL`.
- **023 — Spec Kit Preset-Compatible Import:** `CLOSED_CANONICAL`.
- **024 — Native WorkPacket Export:** `CLOSED_CANONICAL`.
- **025 — Supported Pre-Grain Writer Serialization:** `CLOSED_CANONICAL`.
- **026 — Supported Mutation Cross-Writer Coordination:** `PRODUCT_VERIFIED_CLOSEOUT_PENDING`; product scope is complete and only closeout/reconciliation remains.

## Specification 025 closed frontier

Specification 025 remains `CLOSED_CANONICAL`. Its post-closeout normalization baseline is:

```text
post_normalization_merge = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
post_normalization_ci = 33440739066
```

## Specification 026 selection proof

Fresh evidence against exact post-025 canonical truth:

```text
canonical_base = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
canonical_tree = ffe4dbff9658524eedf359451578a9d0446fed4c
observation_branch = obs/post-025-supported-cross-writer-fixture
observation_head = 3b557f91ec80c147b30f797198d736c2b6b42518
fixture_blob = ba8cea9510d09415a5bd4d2f123a72f5c8affee8
ci_run = 33441481985
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION
```

The fixture used only supported public APIs. `create_child_draft_spec` could successfully create/confirm a child and parent reference between `shape_draft_spec`'s final exact preimage check and `os.replace`; the pre-Grain writer could then overwrite that successful parent postimage and leave structurally invalid stored refinement before failing full-project validation.

The earlier observation run `33441425481` on head `975c47b288cddbfbde34fbbca06afa77ee86f9af` stopped at Ruff before test execution and remains explicitly non-selection evidence.

## Specification 026 shaping proof

```text
shaping_head = 51079a25cdd0f90a9af1cc34ae7577c72ecdf2d6
push_ci = 33441902147
pr = 59
pr_ci = 33442057984
shaping_merge = d27e000728823e93d2fce9ecd669629a839bfdb3
post_shaping_ci = 33442261877
```

The shaping diff was documentation/governance/evidence only, and every shaping gate above completed `success` across the permanent five-cell matrix before product work began.

## Specification 026 product proof

Final exact product head:

```text
24728cd52b2daef2c83c5b83f084421b8096a11f
```

Exact product scope:

- `src/specgrain/store.py`;
- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

Delivered behavior:

- one shared project-scoped non-blocking advisory lock for existing supported pre-Grain persistence and native child authoring;
- existing `.specgrain/tmp/pregrain-mutation.lock` anchor retained;
- child authoring acquires the lock before journal creation and holds it through completion or handled recovery;
- existing authoring journal remains the separate durable recovery mechanism;
- Specification 025 lock/preimage/postimage/platform/lifetime/unsafe-anchor/read-only guarantees remain preserved;
- no journal schema/version, lifecycle, public locking API, runtime dependency, or release change.

Product evidence:

```text
first_final_logic_head = fd27a146b8c39c777b5fb3f1611b2689a1fad3d5
first_final_logic_ci = 33442865903
first_final_logic_result = Ruff failure before tests; not acceptance evidence

final_head = 24728cd52b2daef2c83c5b83f084421b8096a11f
push_ci = 33443061640
pr = 60
pr_ci = 33443161567
product_merge = 69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b
post_product_ci = 33485603844
```

Final push, PR, and canonical post-product CI all completed `success` across Ubuntu/Python 3.11, Ubuntu/Python 3.12, Ubuntu/Python 3.13, macOS/Python 3.11, and Windows/Python 3.11.

At the product merge gate, exact head/base/three-path scope remained unchanged, mergeability was true, submitted reviews and inline review threads were both zero, and unavailable/skipped review systems were not treated as PASS. PR #60 merged with expected-head protection.

## Historical release preservation

Historical `v0.3.0` remains unchanged:

- source `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release `378962445`;
- wheel asset `535129008`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset `535129009`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

## Specification 026 closeout gate

The product is complete. Remaining work is documentation/governance/evidence only:

1. qualify the exact closeout head/diff with permanent push CI;
2. open/update closeout PR and verify exact head/base/scope/PR CI/reviews/comments/threads/mergeability;
3. record unavailable/skipped review systems accurately and never treat them as PASS;
4. merge closeout with expected-head protection;
5. require canonical post-closeout five-cell CI;
6. perform one final evidence reconciliation recording exact closeout merge/CI facts and `CLOSED_CANONICAL` disposition;
7. qualify/merge reconciliation with expected-head protection and require canonical post-reconciliation five-cell CI;
8. reverify the historical release and canonical governance;
9. return to observation unless fresh reproducible evidence independently selects another bounded product gap.

## Still unselected

- arbitrary external/manual writer coordination;
- universal project transaction management;
- child-authoring journal schema/version/recovery redesign;
- distributed/network locking;
- blocking waits, retries, leases, heartbeats, or timeout ownership inference;
- lifecycle expansion;
- executor/provider/result/verification/evidence orchestration;
- automatic context/network/model behavior;
- new runtime dependencies;
- broader package publication;
- hosted/account/dashboard scope;
- Spec Kit runtime adoption;
- release publication;
- empirical benchmark superiority claims.

The invalidated `SGB-EXP-001` hidden scorer remains outside inspection/search/materialization/reproduction/use authority.

## Continuation discipline

Complete Specification 026 closeout and reconciliation only. Do not widen the specification from deferred roadmap categories. When Specification 026 is genuinely `CLOSED_CANONICAL`, return to observation. Do not invent a successor merely to continue activity.
