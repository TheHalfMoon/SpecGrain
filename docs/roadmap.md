# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–024 are `CLOSED_CANONICAL`. No successor product specification is selected. The program is in `POST_024_OBSERVATION`. The canonical Specification 024 closure reconciliation merge is `326e013836814bd3566d1da8887fd028981a8cec`, with post-reconciliation CI `33425454115` completed `success` across all five permanent cells. The latest published release remains GitHub Release `378962445` / tag `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

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

## Specification 024 canonical proof

The invalidated SGB-EXP-001 experiment is retained as methodology evidence only and produced no comparative product authority.

A separate deterministic interoperability fixture selected Specification 024:

```text
canonical_base = f2e8378dcba0cfea2beedc6da61324b0c3fea95e
observation_head = 95e5358ed420cd2e6fbd0bc7c56690763cea1283
fixture_blob = 58cb3e355468f6bcd7de63b676dba52361ff0dd7
ci_run = 33416110142
ci_result = completed/success across all five permanent cells
```

The selected product boundary was intentionally narrower than execution orchestration:

```text
specgrain packet <spec_id> [path] --context-sources <json-file> [--json]
```

It exports the existing WorkPacket from an exact dependency-eligible stored `GRAIN`, using explicit bounded ContextSource records, the existing Grain token budget, current context-budget primitives, and `build_work_packet`, without lifecycle/evidence mutation or execution authority.

Shaping:

- exact head `043abdf8f15f688cdbae746c0abd83dda74d0dae`;
- push CI `33416602621` and PR CI `33416635970` — success across five cells;
- PR #49 expected-head merge `440a8b14459ade2fe8235cc873229dd87ba926b5`;
- post-shaping CI `33416908615` — success across five cells.

Product:

- final implementation head `7e1db87f69108fc8693b987e77d20f92e4f46866`;
- push CI `33421885016` and PR CI `33422062846` — success across five cells;
- Ubuntu/Python 3.11 final push evidence — `592 passed` plus cleanliness, compile, source CLI smoke, build, wheel reinstall, and installed CLI smoke;
- PR #50 expected-head merge `1666ba8c135ee8575f1546019ab592db32947dd2`;
- post-product CI `33422235433` — success across five cells.

Closeout:

- exact documentation-only head `12f89e22955efc632f62d52f2f0396430f4bee01`;
- exact closeout diff contained only seven authorized governance/evidence/status paths;
- push CI `33422814705` and PR CI `33422950629` — success across five cells;
- PR #51 had no submitted reviews or inline review threads and was mergeable before merge; Qodo was billing-blocked, automatic CodeRabbit review was skipped by repository-star policy, and Cubic was descriptive only;
- PR #51 expected-head merge `519680c5cf378dfcb4673cf7292bcf51e9c36af1`;
- closeout merge parent `1666ba8c135ee8575f1546019ab592db32947dd2`;
- post-closeout CI `33423123321` — success across five cells.

Final closure reconciliation:

- exact reconciliation head `e6ac770c191289ff3ddc58789c87d7a97e1c6178`;
- push CI `33425082595` and PR #52 CI `33425201892` — success across five cells;
- PR #52 had no submitted reviews or inline review threads and was mergeable before merge; Qodo was billing-blocked, automatic CodeRabbit review was skipped by repository-star policy, and Cubic was descriptive only;
- PR #52 expected-head merge `326e013836814bd3566d1da8887fd028981a8cec`;
- post-reconciliation CI `33425454115` — success across five cells.

At product, closeout, and final reconciliation review gates, unavailable or skipped review systems were never treated as PASS.

Historical `v0.3.0` remains unchanged at source `70dd66aba0e68ae710e6ef12605ed153d107bab4`, Release `378962445`, wheel digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`, and source digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

## Explicit residual beyond 022

A bounded multi-writer race remains possible around exact-preimage validation and atomic replacement. Specification 024 did not select or alter that boundary.

## Still deferred unless newly shaped

- `GRAIN -> READY` or later lifecycle mutation;
- executor/provider invocation or result orchestration;
- verification execution or evidence mutation;
- automatic context discovery, source-content packing, retrieval, network access, or LLM context selection;
- stronger multi-writer/recovery concurrency;
- PyPI publication or broader distribution changes;
- hosted SaaS, dashboard, account/enterprise, or provider runtime scope;
- Spec Kit preset/hook/extension/bundle/workflow execution or architectural adoption;
- arbitrary Markdown semantic inference;
- empirical benchmark superiority claims without a reproducible completed dataset.

## Post-024 continuation discipline

No successor product specification is selected by Specification 024. Remain in observation/evidence gathering and shape a successor only from fresh reproducible evidence against live canonical truth.
