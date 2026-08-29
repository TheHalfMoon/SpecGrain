# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–018 are `CLOSED_CANONICAL`. Specification 019 product delivery is canonical at `d6727b6c5cdafcf6265b6d999418c0fe853249a7` after post-merge CI `33248014390` and historical-release verification `33248070688`; 019 remains in documentation-only closeout until the exact closeout merge and post-closeout CI succeed. No later specification is planned or implicitly authorized. The fresh post-019 audit recommends a v0.3.0 Recursive Authoring Release candidate for later shaping only.

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
- **019 — Native Child-DRAFT Authoring:** product delivery canonical at `d6727b6c5cdafcf6265b6d999418c0fe853249a7`; adds a recoverable reciprocal child write only under a `DRAFT` parent plus explicit recovery, with no lifecycle promotion; documentation-only closeout pending.

019 remains bounded by ADR-0018. Fresh audit `docs/research/post-019-product-audit-2026-08-29.md` recommends a v0.3.0 Recursive Authoring Release as the smallest later shaping candidate because the latest versioned release still predates 019 behavior. The recommendation is not authority.

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

No successor after 019 is implied. A later shaping chain must re-check live truth after 019 is `CLOSED_CANONICAL`; the post-019 release recommendation may be superseded if evidence changes.
