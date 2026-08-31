# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–024 are `CLOSED_CANONICAL`. Specification 025 — Supported Pre-Grain Writer Serialization — is a `CLOSEOUT_CANDIDATE`: its bounded product implementation is canonical at `5e3966fb0db3d8971b5abe19106949001ed55ba9`, canonical post-product CI `33434910548` succeeded across all five permanent cells, and only documentation-only closeout/final evidence gates remain. The latest published release remains GitHub Release `378962445` / tag `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

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

- **013 — Spec Kit Import:** `CLOSED_CANONICAL`; explicit bounded migration reports with no silent flat-task promotion.
- **014 — Agent Adapters:** generic deterministic WorkPacket/result adapter boundary.

## M7 — Public proof

- **015 — SpecGrainBench:** reproducible experiment ledger and contamination/comparability preflight.
- **016 — Public Launch:** versioned package, cross-platform CI, public examples/guides/trust surfaces, release notes/assets, and `v0.1.0` publication.

## Post-v0.1 — Evidence-shaped product adoption

- **017 — Native DRAFT CLI:** `CLOSED_CANONICAL`.
- **018 — v0.2.0 Authoring Release:** `CLOSED_CANONICAL`.
- **019 — Native Child-DRAFT Authoring:** `CLOSED_CANONICAL`.
- **020 — v0.3.0 Recursive Authoring Release:** `CLOSED_CANONICAL`; product/release source `70dd66aba0e68ae710e6ef12605ed153d107bab4`; Release `378962445` / `v0.3.0`.
- **021 — Public Launch Readiness Hardening:** `CLOSED_CANONICAL`.
- **022 — Native Grain Preparation:** `CLOSED_CANONICAL`; bounded native `DRAFT -> SHAPED -> REFINING -> GRAIN` preparation.
- **023 — Spec Kit Preset-Compatible Import:** `CLOSED_CANONICAL`; deterministic path-bound identity fallback for bounded template-light read-only Spec Kit imports.
- **024 — Native WorkPacket Export:** `CLOSED_CANONICAL`; bounded read-only `packet` export from one exact dependency-eligible stored `GRAIN`.
- **025 — Supported Pre-Grain Writer Serialization:** `CLOSEOUT_CANDIDATE`; bounded cooperative non-blocking serialization of supported `pregrain.py::_persist` transactions is canonical and post-product verified.

## Specification 024 canonical proof

The invalidated SGB-EXP-001 experiment is retained as methodology evidence only and produced no comparative product authority.

Specification 024 was instead selected by deterministic interoperability evidence and is fully `CLOSED_CANONICAL`. Its final post-024 normalization merge is `101f018095868fc011c4ebea15dcac64f64d1061`; canonical post-normalization CI `33427947122` succeeded across all five permanent cells.

## Specification 025 selection proof

The bounded multi-writer residual retained after Specification 022 was reproduced with supported public pre-Grain APIs on the exact post-024 canonical baseline:

```text
canonical_base = 101f018095868fc011c4ebea15dcac64f64d1061
observation_head = 58174dbc87e9c02ebbb3a19d38727e1f42149226
fixture_blob = b0852096a6f8916955a6a31b3a785ca8bb0d708d
ci_run = 33431133156
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_PRE_GRAIN_MULTI_WRITER_LOST_UPDATE
```

Two supported `shape_draft_spec` calls could both return success with distinct semantic revisions while one confirmed successful revision was silently overwritten between another writer's final exact-preimage check and unconditional `os.replace`.

The selected Specification 025 boundary remained intentionally narrower than general concurrency:

```text
serialize supported pre-Grain persistence in pregrain.py::_persist
```

ADR-0020 selected one project-scoped non-blocking advisory lock anchor at `.specgrain/tmp/pregrain-mutation.lock`, using Python standard-library Unix/Windows primitives while retaining existing exact-preimage and postimage validation.

## Specification 025 canonical product proof

Shaping:

```text
shaping_head = e12dc2996f663f5d4a98eb5af212deb73ead5eff
push_ci = 33432149125
pr = 54
pr_ci = 33432301056
shaping_merge = e394ab0c7efabbfade91b64bcdf9a11c8146f469
post_shaping_ci = 33432447491
```

Product:

```text
final_head = bb1fa1406ef9dab6a65c1721378025943ba3f6de
push_ci = 33434286534
pr = 55
pr_ci = 33434757539
product_merge = 5e3966fb0db3d8971b5abe19106949001ed55ba9
post_product_ci = 33434910548
```

The final product diff changed only `src/specgrain/pregrain.py` and `tests/test_pregrain_serialization.py`. The final push, PR, and post-product CI gates all succeeded across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11.

The product now prevents two cooperating supported pre-Grain writers from both returning success after silently overwriting one another, while preserving existing lifecycle/readiness/dependency/preimage/postimage semantics and leaving read-only operations unlocked.

At product review gates, unavailable or skipped review systems were never treated as PASS.

Historical `v0.3.0` remains unchanged at source `70dd66aba0e68ae710e6ef12605ed153d107bab4`, Release `378962445`, wheel digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`, and source digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

## Specification 025 closeout discipline

Product mutation is finished. Closeout is documentation/governance/evidence-only.

Before Specification 025 can become `CLOSED_CANONICAL`, the repository must prove:

1. exact-head closeout CI success across all five permanent cells;
2. closeout scope remains documentation/governance/evidence-only;
3. exact PR head/base, reviews, threads, comments, and mergeability are rechecked;
4. expected-head closeout merge succeeds;
5. canonical post-closeout CI succeeds across all five permanent cells;
6. historical release identity remains unchanged;
7. final evidence reconciliation records the exact closeout evidence;
8. canonical governance re-read supports publishing `CLOSED_CANONICAL` and returning to observation.

## Still deferred unless newly shaped

- coordination with arbitrary external/manual writers;
- general project-wide locking and child-authoring journal redesign;
- distributed/network locking;
- blocking waits, retry loops, leases, heartbeats, or timeout ownership inference;
- `GRAIN -> READY` or later lifecycle mutation;
- executor/provider invocation or result orchestration;
- verification execution or evidence mutation;
- automatic context discovery, source-content packing, retrieval, network access, or LLM context selection;
- new runtime dependencies;
- PyPI publication or broader distribution changes;
- hosted SaaS, dashboard, account/enterprise, or provider runtime scope;
- Spec Kit preset/hook/extension/bundle/workflow execution or architectural adoption;
- arbitrary Markdown semantic inference;
- empirical benchmark superiority claims without a reproducible completed dataset.

## Specification 025 continuation discipline

Finish only the bounded documentation closeout and final evidence gates. After canonical closeout, return to observation/evidence gathering and do not invent a successor merely to continue activity.