# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Program status:** `POST_V0.1_ACTIVE`  
**Last closed specification:** `specs/016-public-launch/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/017-native-draft-cli/` — `SHAPED`  
**Active implementation branch:** none; create only from the canonical 017 shaping merge  
**Next planned specification:** none  
**Published release:** `v0.1.0`  
**Release source commit:** `5eb46db0479cb8707afe070027dab4f3c558849a`

## Canonical v0.1 evidence

Specifications 000 through 016 are closed canonically. Specification 016 product delivery closed through PR #18 and the documentation-only closeout through PR #19. Canonical closeout merge `7c343841424ca48207f9c42eae725a53213d19e5` has exact second parent `fcc4cb218c1c85a6e34a3f52ecd67b685e35b085` and successful five-cell Linux/macOS/Windows CI run `33234669930`. Post-closeout release workflow run `33234703124` also completed successfully without mutating the already-published release.

The public `v0.1.0` tag and GitHub Release `378876694` target product merge `5eb46db0479cb8707afe070027dab4f3c558849a`. Exact release-asset digests remain recorded in `specs/016-public-launch/closeout.md`.

## Post-v0.1 frontier

A fresh product audit at `docs/research/post-v0.1-product-audit-2026-08-29.md` found no public adoption evidence yet and no open issue/PR demand signal. Because the release is less than a day old, those zero signals are not interpreted as product failure.

The smallest evidence-backed product gap is first-party native authoring: `specgrain init` creates an empty store, but v0.1.0 exposes no supported CLI command for creating the first native SpecNode. Specification 017 is therefore shaped as a bounded root-DRAFT authoring command.

017 does not authorize recursive refinement, lifecycle promotion, WorkPacket/executor CLI orchestration, provider-specific integration, hosted services, benchmark execution, PyPI publication, or another release. Those remain future evidence-shaped decisions.

## Execution rule

Implementation may begin only after this shaped 017 authority chain is merged to canonical `main` with expected-head evidence. After 017 closes canonically, re-run the product-frontier audit before shaping any further specification; do not assume a successor.

This active-frontier state becomes authoritative only when the exact shaping head containing this file is merged and live GitHub confirms the resulting canonical `main`.
