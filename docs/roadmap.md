# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–017 are `CLOSED_CANONICAL`. Specification 018 has completed product merge, canonical post-merge CI, and live v0.2.0 publication; its documentation-only closeout carries prospective `CLOSED_CANONICAL` state until exact-head closeout merge and post-closeout proof. No later specification is planned or implicitly authorized.

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

## Post-v0.1 — Evidence-shaped product adoption

- **017 — Native DRAFT CLI:** `CLOSED_CANONICAL`; deterministic creation of the first native root `DRAFT` after `specgrain init` without Grain/readiness/execution authority.
- **018 — v0.2.0 Authoring Release:** product merge `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`; v0.2.0 Release `378936896` published from that exact merge after successful canonical CI. Closeout canonicalization remains pending until its documentation-only exact-head merge and post-closeout proof.

The post-v0.2 audit recommends native child-DRAFT authoring as the strongest next shaping candidate. That recommendation does not create Specification 019 or authorize implementation.

## Explicitly deferred

Future work requires a newly shaped specification and fresh evidence. No item below is automatically authorized by this roadmap:

- lifecycle-aware broad recursive refinement or automatic state progression;
- generic DRAFT editing or protected lifecycle mutation without a bounded authority contract;
- WorkPacket/executor orchestration commands;
- hosted SaaS or web dashboard;
- own LLM or fine-tuning;
- account/enterprise system;
- visual workflow designer;
- large agent-persona catalog;
- provider-specific orchestration without adoption evidence;
- PyPI publication or broader distribution changes without publishing-governance shaping;
- empirical benchmark superiority claims without a reproducible completed dataset.

No successor after 018 is implied. A fresh canonical shaping chain must be created only after 018 closeout becomes authoritative.
