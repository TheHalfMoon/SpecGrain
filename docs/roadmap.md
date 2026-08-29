# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–021 are `CLOSED_CANONICAL`. Specification 022 — Native Grain Preparation is the active `SHAPED` specification. Its documentation-only shaping PR #37 is canonical at `4919a4261f649e81cb1f507c0e80bc5c98d848d8`, and canonical post-shaping CI `33260132438` succeeded. Product implementation is being verified on `feat/022-native-grain-preparation`. The latest published release remains GitHub Release `378962445` / tag `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

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

- **013 — Spec Kit Import:** explicit bounded migration reports with no silent flat-task promotion.
- **014 — Agent Adapters:** generic deterministic WorkPacket/result adapter boundary.

## M7 — Public proof

- **015 — SpecGrainBench:** reproducible experiment ledger and contamination/comparability preflight.
- **016 — Public Launch:** versioned package, cross-platform CI, public examples/guides/trust surfaces, release notes/assets, and `v0.1.0` publication.

The initial v0.1 sequence ended at Specification 016. Exact release and closeout evidence lives in `specs/016-public-launch/closeout.md`.

## Post-v0.1 — Evidence-shaped product adoption

- **017 — Native DRAFT CLI:** `CLOSED_CANONICAL`; deterministic creation of the first native root `DRAFT` after `specgrain init` without hand-authoring internal JSON or granting Grain/readiness/execution authority.
- **018 — v0.2.0 Authoring Release:** `CLOSED_CANONICAL`; published the native root-DRAFT surface as v0.2.0.
- **019 — Native Child-DRAFT Authoring:** `CLOSED_CANONICAL`; recoverable reciprocal child DRAFT authoring and explicit recovery without lifecycle promotion.
- **020 — v0.3.0 Recursive Authoring Release:** `CLOSED_CANONICAL`; product/release source `70dd66aba0e68ae710e6ef12605ed153d107bab4`; Release `378962445` / `v0.3.0`; publishes root/child DRAFT authoring and explicit recovery with no new product behavior.
- **021 — Public Launch Readiness Hardening:** `CLOSED_CANONICAL`; hardens README first-screen trust signals, v0.3.0 install prominence, current security/launch truth, licensing recognition, and launch regression checks without changing product behavior or release identity.
- **022 — Native Grain Preparation:** active `SHAPED` specification. Canonical shaping base `4919a4261f649e81cb1f507c0e80bc5c98d848d8`; bounded current-source implementation adds explicit native `DRAFT -> SHAPED -> REFINING -> GRAIN` preparation using existing schema/lifecycle/readiness semantics. It does not authorize READY/execution/verification/evidence/provider scope or a release/version change.

## Specification 022 implementation checkpoint

Pre-document implementation checkpoint `05865fdfeb89e259be237f5e020a87424384d122` passed permanent CI `33260707422` across all five cells with 573 tests in the Ubuntu/Python 3.11 cell plus all static/package/CLI gates. The final product candidate includes public documentation and launch-guard reconciliation, so exact-head product CI/review remains required before merge.

The historical v0.3.0 release remains unchanged and does not contain `shape`, `refine`, or `grain`; those commands are Specification 022 current-source additions until a separately authorized future release publishes them.

## Evidence selecting 022

The prior post-v0.3 audit selected observation because no concrete adoption blocker had yet been reproduced. A later maintainer-supplied adversarial product review exercised the public workflow and identified the native authoring dead end. Repository inspection then reproduced it at canonical source:

- DRAFT authoring exists;
- published v0.3.0 has no CLI that populates readiness fields on an existing DRAFT;
- published v0.3.0 has no CLI that advances lifecycle into readiness evaluation;
- `check` evaluates only REFINING leaves;
- `next` consumes only GRAIN nodes.

`docs/research/post-v0.3-native-workflow-friction-2026-08-29.md` records the evidence and explains why 022 stops at GRAIN instead of combining authoring, WorkPacket, executor, verification, and evidence mutation in one oversized specification.

## Explicitly deferred beyond 022

Future work requires a newly shaped specification and fresh post-022 evidence. No item below is automatically authorized:

- `GRAIN -> READY` or later lifecycle mutation;
- WorkPacket CLI generation or executor/result orchestration;
- automatic/LLM-assisted spec shaping or provider-specific command installation;
- generic arbitrary editing of mature SpecNodes;
- stronger multi-writer/recovery concurrency;
- PyPI publication or broader distribution changes without publishing-governance shaping;
- hosted SaaS, dashboard, account/enterprise, or provider runtime scope;
- visual workflow designer or large agent-persona catalog;
- empirical benchmark superiority claims without a reproducible completed dataset.

After Specification 022 closes, the next frontier must be re-evaluated from actual post-022 product/adoption evidence rather than assumed to be WorkPacket/executor work.
