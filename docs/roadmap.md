# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–022 are `CLOSED_CANONICAL`. Specification 023 — Spec Kit Preset-Compatible Import is a documentation-only shaping candidate derived from post-022 evidence; implementation remains blocked until its shaping PR merges and canonical post-shaping CI succeeds. The latest published release remains GitHub Release `378962445` / tag `v0.3.0` at exact historical product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

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

The initial v0.1 sequence ended at Specification 016. Exact release and closeout evidence lives in `specs/016-public-launch/closeout.md`.

## Post-v0.1 — Evidence-shaped product adoption

- **017 — Native DRAFT CLI:** `CLOSED_CANONICAL`; deterministic creation of the first native root `DRAFT` after `specgrain init` without hand-authoring internal JSON or granting Grain/readiness/execution authority.
- **018 — v0.2.0 Authoring Release:** `CLOSED_CANONICAL`; published the native root-DRAFT surface as v0.2.0.
- **019 — Native Child-DRAFT Authoring:** `CLOSED_CANONICAL`; recoverable reciprocal child DRAFT authoring and explicit recovery without lifecycle promotion.
- **020 — v0.3.0 Recursive Authoring Release:** `CLOSED_CANONICAL`; product/release source `70dd66aba0e68ae710e6ef12605ed153d107bab4`; Release `378962445` / `v0.3.0`; publishes root/child DRAFT authoring and explicit recovery with no new product behavior.
- **021 — Public Launch Readiness Hardening:** `CLOSED_CANONICAL`; hardens README first-screen trust signals, v0.3.0 install prominence, current security/launch truth, licensing recognition, and launch regression checks without changing product behavior or release identity.
- **022 — Native Grain Preparation:** `CLOSED_CANONICAL`; current source provides explicit native `DRAFT -> SHAPED -> REFINING -> GRAIN` preparation through bounded `shape`, `refine`, and `grain` surfaces using existing schema/lifecycle/readiness semantics.
- **023 — Spec Kit Preset-Compatible Import:** `SHAPED` candidate pending canonical shaping merge; broadens only the existing read-only migration identity boundary so template-light official preset artifacts can be reported without requiring the full-template feature heading.

## Specification 022 canonical proof

Final implementation head `8af20015bd59424c7882b8c8fa7ea4c78e0af2e5` passed exact push CI `33261979828` and exact PR CI `33261982603`. PR #38 merged as product merge `653cfb64c8885174ea3ea729d1bbb6418613b10d`; canonical post-product CI `33262123902` succeeded.

Documentation closeout head `7b3b5beed297d024ad897e3b7e4d5376c8c5f24a` passed push CI `33262421052` and PR CI `33262442496`; PR #39 merged as canonical closeout `9cd52eb6d1ba6839910ceb973fedf5b3a727cc0a`; post-closeout CI `33262519733` succeeded.

PR #40 reconciled final canonical status as `ff9f640bf0e4de5bdd5bf2af0e11b98d86f6587b`; post-reconciliation CI `33262914956` succeeded across all five permanent cells.

The historical `v0.3.0` release remains unchanged and does not contain `shape`, `refine`, or `grain`.

## Specification 023 evidence and boundary

The exact post-022 comparison reviewed GitHub Spec Kit `main` `51e52be6c3b26fed3ff5424c671f4a559519a759` and latest observed release `v1.0.1`.

The standard upstream template still uses `# Feature Specification: ...`, but the official bundled Lean preset explicitly replaces full templates with focused Markdown artifacts and does not require that boilerplate. Current SpecGrain requires the exact full-template heading before it can establish feature identity.

Specification 023 therefore selects only this bounded repair:

- standard full-template reports remain unchanged, including digest and import version;
- template-light `spec.md` may derive report identity only from its concrete normalized parent directory;
- fallback identity is explicitly noticed;
- no unrecognized semantics are inferred;
- all current read-only/source-safety/task-non-promotion/constitution-non-adoption rules remain intact;
- no upstream runtime dependency or command execution is added.

Implementation cannot begin until the shaping candidate is canonically merged and post-shaping CI succeeds.

## Explicit residual beyond 022

A bounded multi-writer race remains possible around exact-preimage validation and atomic replacement. Specification 023 does not select or alter that boundary.

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
- Spec Kit preset/hook/extension/bundle/workflow execution or architectural adoption;
- empirical benchmark superiority claims without a reproducible completed dataset.

The next product frontier after 023 must again be selected from actual canonical evidence rather than assumed from this deferred list.
