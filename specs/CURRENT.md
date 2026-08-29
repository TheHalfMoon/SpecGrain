# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Program status:** `POST_V0.1_ACTIVE`  
**Last closed specification:** `specs/017-native-draft-cli/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/018-v0.2.0-authoring-release/` — `SHAPED` (prospective until shaping merge)  
**Active branch:** `spec/018-v0.2.0-authoring-release` (shaping only)  
**Next planned specification:** none beyond 018  
**Published release:** `v0.1.0`  
**Published release source commit:** `5eb46db0479cb8707afe070027dab4f3c558849a`  
**Latest canonical closeout merge:** `d7c3f8e5734264824cd6ed1d8e931802a242c50a`

## Canonical v0.1 evidence

Specifications 000 through 016 are `CLOSED_CANONICAL`. The public `v0.1.0` tag and GitHub Release `378876694` remain bound to product release source `5eb46db0479cb8707afe070027dab4f3c558849a`.

## Specification 017 evidence

Specification 017 is `CLOSED_CANONICAL`. Its product PR #21 exact reviewed head `1255a9187f85591edd041a3125359e70d2eea379` merged as `dedb9ee30a6b8856c9c06439c68f3a37225f0563`; canonical product post-merge CI run `33236142514` succeeded. Documentation-only closeout PR #22 exact head `c1b49e1751ae369ae8efb6269ec201b5f04e4f1d` merged as `d7c3f8e5734264824cd6ed1d8e931802a242c50a`, whose second parent is that exact closeout head; post-closeout CI run `33236900072` succeeded across all five permanent matrix jobs.

## Specification 018 shaping boundary

The fresh post-017 audit identifies the distribution gap between current `main` and published `v0.1.0` as the smallest adoption-oriented frontier. This shaping branch selects a bounded `v0.2.0` GitHub release of the already-completed authoring surface and ADR-0017 defines monotonic versioned-release progression.

No 018 implementation is authorized from this branch. The shaped authority becomes executable only after the exact shaping PR head is merged to canonical `main` with required evidence and `main` is re-read.

## Product/release boundary

Current canonical product behavior includes `specgrain draft`; published `v0.1.0` does not. Until 018 is actually released, `v0.1.0` remains the latest public release. No PyPI publication, recursive refinement CLI, executor orchestration, hosted service, or benchmark winner is authorized by 018 shaping.
