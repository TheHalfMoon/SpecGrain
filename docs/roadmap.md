# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

## Completed foundation and v0.1 program

Specifications 000 through 016 are `CLOSED_CANONICAL`. SpecGrain v0.1.0 is published from product release source commit `5eb46db0479cb8707afe070027dab4f3c558849a`.

- **M0 — Foundation:** 000 Foundation.
- **M1 — Deterministic specification kernel:** 001 SpecNode Schema, 002 Lifecycle State, 003 Refinement Tree, 004 Grain Readiness.
- **M2 — Local product surface:** 005 CLI/Local Store, 006 Dependency Graph.
- **M3 — Brownfield context:** 007 Repository Scan, 008 Context Budget.
- **M4 — Portable execution boundary:** 009 WorkPacket, 010 Verification/Evidence.
- **M5 — Adaptive delivery control:** 011 Method Profiles, 012 Diff/Drift/Metrics.
- **M6 — Ecosystem interoperability:** 013 Spec Kit Import, 014 Agent Adapters.
- **M7 — Public proof:** 015 SpecGrainBench, 016 Public Launch.

## Post-v0.1 evidence-shaped product adoption

- **017 — Native DRAFT CLI:** adds deterministic creation of the first native root `DRAFT` after `specgrain init`, without granting Grain/readiness/execution authority.

017 product delivery merged through PR #21 as `dedb9ee30a6b8856c9c06439c68f3a37225f0563`; canonical post-merge CI run `33236142514` succeeded across the permanent five-cell matrix. Its documentation-only closeout records the exact evidence.

No successor specification is implicitly authorized. The fresh post-017 audit identifies a versioned public release of the already-completed current authoring surface as the strongest next shaping candidate because published `v0.1.0` predates `specgrain draft`. That recommendation remains non-authoritative until a separate specification is shaped and merged canonically.

## Explicitly deferred

Future work requires a newly shaped specification and fresh evidence. No item below is automatically authorized by this roadmap:

- a new release or exact version number until release scope is separately shaped;
- recursive CLI refinement beyond the 017 root-DRAFT surface;
- WorkPacket/executor orchestration commands;
- PyPI publication or another distribution channel without publishing-governance authority;
- hosted SaaS or web dashboard;
- own LLM or fine-tuning;
- account/enterprise system;
- visual workflow designer;
- large agent-persona catalog;
- provider-specific orchestration without adoption evidence;
- empirical benchmark superiority claims without a reproducible completed dataset.

The 017 `CLOSED_CANONICAL` statement in this closeout tree becomes authoritative only after the exact closeout head is merged and live GitHub post-closeout evidence confirms canonical `main`.
