# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–025 are `CLOSED_CANONICAL`. There is no active product specification. The program is in `POST_025_OBSERVATION`. The latest published release remains GitHub Release `378962445` / tag `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

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

## Specification 024 canonical frontier

Specification 024 remains `CLOSED_CANONICAL`. Its final post-024 normalization merge is `101f018095868fc011c4ebea15dcac64f64d1061`; canonical post-normalization CI `33427947122` succeeded across all five permanent cells.

The invalidated SGB-EXP-001 experiment remains methodology evidence only and produced no comparative product authority.

## Specification 025 selection proof

```text
canonical_base = 101f018095868fc011c4ebea15dcac64f64d1061
observation_head = 58174dbc87e9c02ebbb3a19d38727e1f42149226
fixture_blob = b0852096a6f8916955a6a31b3a785ca8bb0d708d
ci_run = 33431133156
reproduced_gap = SUPPORTED_PRE_GRAIN_MULTI_WRITER_LOST_UPDATE
```

Two supported `shape_draft_spec` calls could both report success while one confirmed semantic revision was silently overwritten. ADR-0020 selected the smallest repair: serialize supported pre-Grain persistence through the common `_persist` boundary.

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

The final product diff changed only `src/specgrain/pregrain.py` and `tests/test_pregrain_serialization.py`. The product prevents two cooperating supported pre-Grain writers from both returning success after silently overwriting one another while preserving prior lifecycle/readiness/dependency/preimage/postimage behavior and leaving read-only operations unlocked.

All final shaping/product CI gates succeeded across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11. Unavailable or skipped review systems were never treated as PASS.

## Specification 025 canonical closeout and reconciliation proof

```text
closeout_head = 885823e0e56dfd3e7c7c8e63d8dacc41b14448f2
closeout_push_ci = 33435480927
closeout_pr = 56
closeout_pr_ci = 33435703680
closeout_merge = e05df4bd046590ee043115c1edbcd7b83163b4ad
post_closeout_ci = 33436130730
reconciliation_head = c145578694100383d7292fc76b5995cee8a0e121
reconciliation_push_ci = 33436685449
reconciliation_pr = 57
reconciliation_pr_ci = 33436869583
reconciliation_merge = 8a0da2908f6251100a0d7ab71178c2a7c3ed64bb
post_reconciliation_ci = 33437077692
```

The closeout and reconciliation changes remained documentation/governance/evidence-only. Canonical post-closeout and post-reconciliation CI each completed `success` across all five permanent cells.

Historical `v0.3.0` remains unchanged at source `70dd66aba0e68ae710e6ef12605ed153d107bab4`, Release `378962445`, wheel digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`, and source digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

## Post-025 observation frontier

All currently shaped and authorized product work is complete and no active product specification remains.

Still deferred unless newly selected by fresh reproducible evidence:

- arbitrary non-cooperating writer coordination;
- general project-wide or distributed locking;
- child-authoring journal redesign;
- blocking waits, retries, leases, heartbeats, or timeout ownership inference;
- `GRAIN -> READY` or later lifecycle mutation;
- executor/provider invocation or result orchestration;
- verification execution or evidence mutation;
- automatic context discovery, retrieval, network access, or model selection;
- new runtime dependencies;
- broader package publication;
- hosted/account/dashboard scope;
- Spec Kit runtime adoption;
- empirical benchmark superiority claims without a reproducible completed dataset.

## Continuation discipline

Remain in observation/evidence gathering. Do not invent a successor merely to continue activity. Shape another specification only when fresh reproducible evidence against live canonical truth selects a bounded product gap.
