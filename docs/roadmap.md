# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–022 are `CLOSED_CANONICAL`. There is no active specification. The program is at `POST_022_OBSERVATION`. Specification 022 canonical product merge is `653cfb64c8885174ea3ea729d1bbb6418613b10d`; canonical closeout merge is `9cd52eb6d1ba6839910ceb973fedf5b3a727cc0a`; post-closeout CI `33262519733` succeeded across all five permanent cells. The latest published release remains GitHub Release `378962445` / tag `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

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
- **022 — Native Grain Preparation:** `CLOSED_CANONICAL`; current source provides explicit native `DRAFT -> SHAPED -> REFINING -> GRAIN` preparation through bounded `shape`, `refine`, and `grain` surfaces using existing schema/lifecycle/readiness semantics.

## Specification 022 canonical proof

Final implementation head `8af20015bd59424c7882b8c8fa7ea4c78e0af2e5` passed exact push CI `33261979828` and exact PR CI `33261982603` across the permanent five-cell matrix, with 575 tests in Ubuntu/Python 3.11 plus all required static/package/CLI gates.

PR #38 merged with expected-head protection as product merge `653cfb64c8885174ea3ea729d1bbb6418613b10d`. Canonical post-product CI `33262123902` succeeded across all five permanent cells.

Documentation closeout head `7b3b5beed297d024ad897e3b7e4d5376c8c5f24a` passed push CI `33262421052` and PR CI `33262442496`, then PR #39 merged with expected-head protection as canonical closeout merge `9cd52eb6d1ba6839910ceb973fedf5b3a727cc0a`. Canonical post-closeout CI `33262519733` succeeded across all five permanent cells. PR #38 and PR #39 are merged/closed.

The historical v0.3.0 release remains unchanged and does not contain `shape`, `refine`, or `grain`; those commands are unreleased current-source Specification 022 additions.

## Explicit residual beyond 022

A bounded multi-writer race remains possible around exact-preimage validation and atomic replacement. Specification 022 intentionally did not widen into multi-writer locking or recovery semantics. Stronger concurrency requires fresh evidence and a separately shaped specification.

## Post-022 observation frontier

The program is now in observation/evidence gathering with no active successor specification.

A planned external architectural review and comparison with GitHub Spec Kit may provide useful evidence about interoperability, workflow gaps, excessive ceremony, missing bounded surfaces, or architectural divergence. That comparison must treat GitHub Spec Kit as an upstream influence/compatibility target, not as repository authority or an instruction to copy its architecture.

Concrete review findings may shape a future specification only after they are reproduced against exact canonical SpecGrain truth.

## Explicitly deferred unless fresh evidence selects them

No item below is automatically authorized:

- `GRAIN -> READY` or later lifecycle mutation;
- WorkPacket CLI generation or executor/result orchestration;
- automatic/LLM-assisted spec shaping or provider-specific command installation;
- generic arbitrary editing of mature SpecNodes;
- stronger multi-writer/recovery concurrency;
- PyPI publication or broader distribution changes without publishing-governance shaping;
- hosted SaaS, dashboard, account/enterprise, or provider runtime scope;
- visual workflow designer or large agent-persona catalog;
- empirical benchmark superiority claims without a reproducible completed dataset.

The next product frontier must be selected from actual post-022 evidence rather than assumed from this deferred list.