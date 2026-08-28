# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `001a70fcabff497c565fa7339381c4da0b4a3881`  
**Closed specification:** `specs/015-specgrain-bench/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/016-public-launch/`  
**Active branch:** `feat/016-public-launch`  
**Active status:** `VERIFYING`

## Canonical 015 closeout evidence

Specification 015 closed through PR #17. Final reviewed PR head `14e3d7e6a301148e0a25c2e98134fe8a6c573b54` was merged with expected-head protection into canonical merge commit `001a70fcabff497c565fa7339381c4da0b4a3881`; the merge commit's second parent is the exact reviewed head.

## 016 release candidate surface

The active branch contains the v0.1.0 package metadata, permanent cross-platform CI, truthful launch README, runnable zero-to-verified example, pinned brownfield examples, Spec Kit migration guide, no-winner benchmark report, trust/security/community documentation, release notes, launch asset, and launch-surface tests. The permanent Ruff gate exposed pre-existing source/test style debt during release verification; those findings were repaired mechanically and retained only after Ruff, full regression, compile, and whitespace checks succeeded. No behavioral product expansion was introduced by that hardening.

The release contract is post-CI and exact-SHA-bound. It builds and attaches the v0.1.0 wheel and source distribution, refuses conflicting partial release state, and becomes a no-op after the immutable public v0.1.0 release exists so later canonical closeout commits cannot move the tag.

## Immediate ordering

Complete exact-head regression/static/package verification, prove Linux/macOS/Windows permanent CI, record exact verification and diff-review evidence, open and merge the bounded product PR with expected-head protection, publish `v0.1.0`, then perform the documentation-only release closeout.
