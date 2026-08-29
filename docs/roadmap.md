# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–016 are `CLOSED_CANONICAL` and SpecGrain v0.1.0 is published from product release source commit `5eb46db0479cb8707afe070027dab4f3c558849a`. Specification 017 — Native DRAFT CLI has completed product delivery and canonical post-merge CI; its documentation-only closeout carries prospective `CLOSED_CANONICAL` state that becomes authoritative only after exact-head closeout merge and post-closeout verification. No later specification is planned or implicitly authorized.

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

- **017 — Native DRAFT CLI (CLOSEOUT):** create the first validated root SpecNode through a deterministic supported CLI command after `specgrain init`, without granting Grain/readiness/execution authority.

017 was selected by `docs/research/post-v0.1-product-audit-2026-08-29.md`. Its product implementation merged through PR #21 as `dedb9ee30a6b8856c9c06439c68f3a37225f0563`, and canonical post-merge CI run `33236142514` succeeded across the permanent five-cell matrix.

The fresh post-017 audit at `docs/research/post-017-product-audit-2026-08-29.md` identifies a versioned public release of the already-completed current authoring surface as the strongest next shaping candidate because published `v0.1.0` predates `specgrain draft`. The audit does not authorize a successor specification, version number, tag, release mutation, or distribution channel.

## Explicitly deferred

Future work requires a newly shaped specification and fresh evidence. No item below is automatically authorized by this roadmap:

- a new release or exact version number until release scope is separately shaped;
- recursive CLI refinement beyond the bounded 017 root-DRAFT surface;
- WorkPacket/executor orchestration commands;
- hosted SaaS or web dashboard;
- own LLM or fine-tuning;
- account/enterprise system;
- visual workflow designer;
- large agent-persona catalog;
- provider-specific orchestration without adoption evidence;
- PyPI publication or broader distribution changes without release-governance shaping;
- empirical benchmark superiority claims without a reproducible completed dataset.

The 017 `CLOSED_CANONICAL` statement in the documentation-only closeout tree becomes authoritative only after the exact closeout head is merged and live GitHub post-closeout evidence confirms canonical `main`.
