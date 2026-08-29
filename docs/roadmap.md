# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–023 are `CLOSED_CANONICAL` when the final Specification 023 reconciliation is canonical. No successor product specification is selected. The program returns to observation/evidence gathering. The latest published release remains GitHub Release `378962445` / tag `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

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
- **023 — Spec Kit Preset-Compatible Import:** `CLOSED_CANONICAL` when this reconciliation is canonical; deterministic path-bound identity fallback for bounded template-light read-only Spec Kit imports.

## Specification 023 canonical proof

Specification 023 was selected from exact post-022 comparison with GitHub Spec Kit `main` `51e52be6c3b26fed3ff5424c671f4a559519a759` and official bundled Lean preset evidence.

Shaping PR #41 merged exact head `e19484f292c7601036e1993e58203554d1267594` as canonical shaping merge `99d8ee5bc7ce49c00ae542f3c06f564d05641a70`; post-shaping CI `33263898618` succeeded across all five permanent cells.

Final implementation head `83fcc6add4e982df523f6c606399f08c317d3ffe` passed push CI `33264389193` and PR CI `33264479954`. PR #42 merged with expected-head protection as canonical product merge `037f137cdd6e7a0fe224bd3fa3371d6da7460f22`; post-product CI `33265277105` succeeded.

Documentation-only closeout head `fb23602a3aa234b88b0a223443c8c974ff8ed25a` passed push CI `33265481647` and PR CI `33265501850`. PR #43 merged with expected-head protection as canonical closeout merge `5b3a8b906309de642a0b35dfa8e260b5fa6bedd1`; post-closeout CI `33265589133` succeeded across all five permanent cells.

The canonical pre-023 full-template report digest remains `sha256:678fcc87985902002a9d2bc852196fbffdc59b332740660f1deeaf0d4f58746a`; `SPECKIT_IMPORT_VERSION == 1`.

The historical `v0.3.0` tag, Release `378962445`, asset identities, sizes, digests, release notes, and command surface remain unchanged.

## Explicit residual beyond 022

A bounded multi-writer race remains possible around exact-preimage validation and atomic replacement. Specification 023 does not select or alter that boundary.

## Post-023 observation frontier

No successor item is automatically authorized. Fresh reproducible evidence must select the next bounded specification.

Deferred unless newly shaped:

- `GRAIN -> READY` or later lifecycle mutation;
- WorkPacket CLI generation or executor/result orchestration;
- verification execution or evidence mutation;
- automatic/LLM-assisted shaping or provider-specific command installation;
- stronger multi-writer/recovery concurrency;
- PyPI publication or broader distribution changes;
- hosted SaaS, dashboard, account/enterprise, or provider runtime scope;
- Spec Kit preset/hook/extension/bundle/workflow execution or architectural adoption;
- arbitrary Markdown semantic inference;
- empirical benchmark superiority claims without a reproducible completed dataset.
