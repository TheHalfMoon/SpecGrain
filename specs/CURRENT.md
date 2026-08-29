# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Program status:** `POST_V0.1_ACTIVE`  
**Last closed specification:** `specs/017-native-draft-cli/` — `CLOSED_CANONICAL`  
**Active specification:** none  
**Active branch:** none  
**Next planned specification:** none  
**Published release:** `v0.1.0`  
**Published release source commit:** `5eb46db0479cb8707afe070027dab4f3c558849a`  
**Latest product merge:** `dedb9ee30a6b8856c9c06439c68f3a37225f0563`

## Canonical v0.1 evidence

Specifications 000 through 016 closed canonically. The public `v0.1.0` tag and GitHub Release `378876694` remain bound to product release source `5eb46db0479cb8707afe070027dab4f3c558849a`.

## Specification 017 evidence

Specification 017 was shaped through PR #20 and canonical shaping merge `5c7783dde897c975b3519b37bfd45b547244b273`.

Product PR #21 exact reviewed head `1255a9187f85591edd041a3125359e70d2eea379` completed final-head CI run `33235889444` successfully and merged with expected-head protection as `dedb9ee30a6b8856c9c06439c68f3a37225f0563`. The merge first parent is `5c7783dde897c975b3519b37bfd45b547244b273`; the second parent is that exact reviewed product head.

Canonical post-merge CI run `33236142514` completed successfully across Ubuntu/Python 3.11, 3.12, and 3.13, macOS/Python 3.11, and Windows/Python 3.11. Exact job IDs and review boundaries are recorded in `specs/017-native-draft-cli/closeout.md`.

## Product/release boundary

Current `main` supports `specgrain draft`; published `v0.1.0` does not. No later release, PyPI publication, recursive refinement CLI, executor orchestration, hosted service, or benchmark winner is authorized by 017 closeout.

A fresh post-017 audit is recorded at `docs/research/post-017-product-audit-2026-08-29.md`. It recommends that later shaping first consider making the completed current authoring surface available through a new versioned public release. The audit is not implementation authority and no successor specification is planned by this file.

## Canonicalization rule

This `CLOSED_CANONICAL` state is prospective inside the documentation-only closeout branch. It becomes repository authority only if the exact closeout PR head containing this file is merged with expected-head protection and live GitHub post-closeout evidence confirms canonical `main`.
