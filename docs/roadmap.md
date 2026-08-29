# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–019 are `CLOSED_CANONICAL`. Specification 020 product delivery is canonical at `70dd66aba0e68ae710e6ef12605ed153d107bab4`; canonical product CI `33249920673` succeeded and GitHub Release `378962445` / tag `v0.3.0` was published by Release workflow `33249956337`. 020 remains in documentation-only closeout until the exact closeout merge, post-closeout CI, and historical v0.3.0 no-mutation verification succeed. The fresh post-v0.3 audit selects no evidence-supported successor.

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

Specification 010 closed the first complete MVP vertical slice.

## M5 — Adaptive delivery control

- **011 — Method Profiles:** `quick`, `dmaic-lite`, `dmadv-lite`, `experiment`, `controlled`.
- **012 — Diff, Drift, and Metrics:** scope analysis, drift signals, and delivery metrics.

## M6 — Ecosystem interoperability

- **013 — Spec Kit Import:** explicit bounded migration reports with no silent flat-task promotion.
- **014 — Agent Adapters:** generic deterministic WorkPacket/result adapter boundary.

## M7 — Public proof

- **015 — SpecGrainBench:** reproducible experiment ledger and contamination/comparability preflight.
- **016 — Public Launch:** versioned package, cross-platform CI, public examples/guides/trust surfaces, release notes/assets, and `v0.1.0` publication.

The initial v0.1 sequence ended at Specification 016. Exact release and closeout evidence lives in `specs/016-public-launch/closeout.md`.

## Post-v0.1 — Evidence-shaped product adoption

- **017 — Native DRAFT CLI:** `CLOSED_CANONICAL`; adds deterministic creation of the first native root `DRAFT` after `specgrain init` without Grain/readiness/execution authority.
- **018 — v0.2.0 Authoring Release:** `CLOSED_CANONICAL`; product merge `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`, Release `378936896`, closeout merge `c5282caa29fbfeb8c118755766b6a7b8a49d2781`.
- **019 — Native Child-DRAFT Authoring:** `CLOSED_CANONICAL`; product merge `d6727b6c5cdafcf6265b6d999418c0fe853249a7`, closeout merge `3f8f3d825c3171a3a9ac7761ee5bc642e68a9d2d`; adds recoverable reciprocal child DRAFT authoring and explicit recovery without lifecycle promotion.
- **020 — v0.3.0 Recursive Authoring Release:** product delivery canonical at `70dd66aba0e68ae710e6ef12605ed153d107bab4`; Release `378962445` / `v0.3.0` publishes the already-canonical root/child DRAFT and explicit recovery surface with no new product behavior; documentation-only closeout pending.

Fresh audit `docs/research/post-v0.3-product-audit-2026-08-29.md` selects no evidence-supported successor after 020. Once 020 closes canonically, the roadmap enters observation rather than pre-authorizing another specification. A later successor requires fresh user/adoption evidence, a reproducible defect/security finding, controlled benchmark data, or a clearly bounded interoperability/governance blocker.

## Explicitly deferred

Future work requires a newly shaped specification and fresh evidence. No item below is automatically authorized by this roadmap:

- lifecycle-aware broad recursive refinement or automatic state progression;
- generic DRAFT editing or protected lifecycle mutation without a bounded authority contract;
- stronger multi-writer/recovery concurrency without observed demand and a separately shaped locking contract;
- WorkPacket/executor orchestration commands;
- hosted SaaS or web dashboard;
- own LLM or fine-tuning;
- account/enterprise system;
- visual workflow designer;
- large agent-persona catalog;
- provider-specific orchestration without adoption evidence;
- PyPI publication or broader distribution changes without publishing-governance shaping;
- empirical benchmark superiority claims without a reproducible completed dataset.

No successor after 020 is implied or currently selected. Observation is the current evidence-shaped frontier once 020 canonical closeout completes.
