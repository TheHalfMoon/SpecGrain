# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–025 are `CLOSED_CANONICAL`. Fresh post-025 observation has selected **026 — Supported Mutation Cross-Writer Coordination** as a `SHAPED_CANDIDATE`. Product implementation is blocked until the documentation/governance-only shaping package is merged canonically and the exact canonical shaping merge passes permanent five-cell CI. The latest published release remains GitHub Release `378962445` / tag `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

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
- **025 — Supported Pre-Grain Writer Serialization:** `CLOSED_CANONICAL`; bounded cooperative non-blocking serialization of supported `pregrain.py::_persist` transactions.
- **026 — Supported Mutation Cross-Writer Coordination:** `SHAPED_CANDIDATE`; share the existing non-blocking advisory ownership boundary between supported pre-Grain persistence and native child authoring only.

## Specification 025 closed frontier

Specification 025 remains `CLOSED_CANONICAL`. Exact canonical evidence includes:

```text
product_merge = 5e3966fb0db3d8971b5abe19106949001ed55ba9
post_product_ci = 33434910548
reconciliation_merge = 8a0da2908f6251100a0d7ab71178c2a7c3ed64bb
post_reconciliation_ci = 33437077692
post_normalization_merge = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
post_normalization_ci = 33440739066
```

Historical `v0.3.0` remains unchanged at source `70dd66aba0e68ae710e6ef12605ed153d107bab4`, Release `378962445`, wheel digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`, and source digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

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

The fixture uses only supported public APIs. `create_child_draft_spec` can successfully create/confirm a child and parent reference between `shape_draft_spec`'s final exact preimage check and `os.replace`. The pre-Grain writer then overwrites that successful parent postimage, later fails full-project validation, and leaves the stored project structurally invalid.

The earlier observation run `33441425481` on head `975c47b288cddbfbde34fbbca06afa77ee86f9af` stopped at Ruff before test execution and is explicitly not product-selection evidence.

## Specification 026 bounded candidate

Selected:

- one shared project-scoped non-blocking advisory lock for existing supported pre-Grain persistence and native child authoring;
- existing `.specgrain/tmp/pregrain-mutation.lock` anchor retained unless an equivalently narrow migration-free implementation is required;
- private lock helper may move to a dependency-neutral module only to avoid circular imports;
- child authoring acquires the shared lock before journal creation and holds it through completion or handled recovery;
- existing authoring journal remains the separate recovery mechanism;
- all Specification 025 lock, preimage/postimage, platform, unsafe-anchor, process-exit, and read-only guarantees remain required;
- exact cross-platform CI remains part of acceptance.

Still unselected:

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

The invalidated `SGB-EXP-001` hidden scorer remains outside inspection/search/materialization/use authority.

## Specification 026 execution gate

Current authority:

```text
SHAPING_JUSTIFIED = true
SHAPED_CANDIDATE = true
IMPLEMENTATION_AUTHORIZED = false
```

Before product implementation:

1. verify the final shaping diff is documentation/governance/evidence-only and exactly based on canonical `1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1`;
2. require shaping push CI success across all five permanent cells;
3. open/update the shaping PR and recheck exact head/base/scope/PR CI/reviews/comments/threads/mergeability;
4. do not treat unavailable/skipped review systems as PASS;
5. merge with expected-head protection;
6. re-read canonical `main` and full Specification 026 authority;
7. require canonical post-shaping permanent five-cell CI success;
8. only then authorize the bounded implementation branch `feat/026-supported-mutation-cross-writer-coordination`.

## Continuation discipline

Execute only the selected Specification 026 gates. Do not widen the specification from deferred roadmap categories. After each canonical merge, re-read live repository truth. When Specification 026 is genuinely closed, return to observation unless fresh reproducible evidence independently selects another bounded product gap.
