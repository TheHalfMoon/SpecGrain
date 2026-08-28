# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `001a70fcabff497c565fa7339381c4da0b4a3881`  
**Closed specification:** `specs/015-specgrain-bench/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/016-public-launch/`  
**Active branch:** `feat/016-public-launch`  
**Active status:** `SHAPED`

## Canonical 015 closeout evidence

Specification 015 closed through PR #17. Final reviewed PR head `14e3d7e6a301148e0a25c2e98134fe8a6c573b54` was merged with expected-head protection into canonical merge commit `001a70fcabff497c565fa7339381c4da0b4a3881`; the merge commit's second parent is the exact reviewed head.

GitHub Actions verification-only run `33196205039` on byte-identical product/test blobs completed successfully with full pytest regression, changed-surface/baseline/full Ruff checks, compileall, install, entry-point parity, and line-length gates.

## Active 016 boundary

Specification 016 ships the first truthful public release. It must not add fake orchestration commands merely to match the aspirational launch demo, publish fabricated benchmark comparisons, or grow runtime dependencies without necessity. Release closure requires exact product merge evidence plus live `v0.1.0` tag/GitHub Release evidence.

## Immediate ordering

Implement the bounded launch surface, verify permanent Linux/macOS/Windows CI and packaging on the exact PR head, merge with expected-head evidence, create `v0.1.0`, then perform a documentation-only release closeout and prove the final canonical state.
