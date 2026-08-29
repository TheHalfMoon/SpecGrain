# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Program status:** `POST_V0.3_CLOSEOUT`  
**Last closed specification:** `specs/019-native-child-draft-authoring/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/020-v0.3.0-recursive-authoring-release/` — `CLOSEOUT_PENDING_CANONICAL`  
**Active branch:** `chore/020-v0.3.0-recursive-authoring-release-closeout`  
**Next planned specification:** none; the fresh post-v0.3 audit selects observation and finds no evidence-supported successor  
**Published release:** `v0.3.0`  
**Published release source commit:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Published release ID:** `378962445`

## Specification 019 canonical closeout

Specification 019 is `CLOSED_CANONICAL`. Product merge `d6727b6c5cdafcf6265b6d999418c0fe853249a7` passed canonical product CI `33248014390`. Documentation-only closeout merged as `3f8f3d825c3171a3a9ac7761ee5bc642e68a9d2d`; post-closeout CI `33248332725` succeeded and Release verification `33248368659` / job `99089652500` preserved historical `v0.2.0` without mutation.

## Specification 020 canonical shaping and product delivery

Documentation-only shaping PR #29 exact head `61f97bd24d2fe9e1ce5a216170368adae38671e3` passed exact-head CI `33248501598` and merged with expected-head protection as shaping merge `05219b4ea7ce1be201c8fb2ff31e707ae02cba17`. Canonical shaping post-merge CI `33248559704` succeeded across the permanent five-cell matrix.

Implementation PR #30 repaired its only material manual-review finding forward before final evidence. Product candidate `d207d54317457a744cb8887a260fcb78dc0710be` passed CI `33249652226`; Ubuntu/Python 3.11 recorded `555 passed` plus successful v0.3.0 build/install/CLI smoke. Final evidence head `bf59a2ceba3e28cabc2294a0bd95e4e973b1e2bf` then passed exact-head PR CI `33249768557` across all five permanent cells.

PR #30 merged with expected-head protection as canonical product merge `70dd66aba0e68ae710e6ef12605ed153d107bab4`. Its first parent is exact shaping merge `05219b4...`; its second parent is exact final PR head `bf59a2c...`; GitHub signature verification is valid.

Canonical product post-merge CI run `33249920673` completed successfully across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11.

## v0.3.0 publication

Release workflow run `33249956337`, job `99093825183`, checked out exact canonical product merge `70dd66a...`, resolved package version `0.3.0`, built the exact expected wheel/source distribution, created new tag `v0.3.0`, and created GitHub Release `378962445`.

Live release truth:

- tag `v0.3.0` targets exact product merge `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- release title is `SpecGrain v0.3.0`;
- draft `false`, prerelease `false`;
- wheel `specgrain-0.3.0-py3-none-any.whl`: asset `535129008`, size `70463`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source distribution `specgrain-0.3.0.tar.gz`: asset `535129009`, size `104057`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

Historical v0.1.0 and v0.2.0 tag/release/asset identities were reverified unchanged after publication.

## Delivered 020 boundary

Specification 020 is distribution-only. It publishes already-canonical root/child DRAFT authoring and explicit recovery without changing `src/specgrain/` product behavior or the Release workflow. Runtime dependencies remain empty.

020 does not authorize generic editing, lifecycle promotion, readiness synthesis, executor/provider behavior, PyPI publication, hosted surfaces, stronger multi-writer semantics, or empirical benchmark claims.

## Fresh frontier evidence

`docs/research/post-v0.3-product-audit-2026-08-29.md` records that v0.3.0 closes the distribution discontinuity that motivated Specification 020. Canonical `main` and the latest public versioned release are now aligned for native recursive DRAFT authoring and supported explicit recovery.

The audit selects **no successor specification**. Repository adoption evidence remains too sparse to justify lifecycle mutation, generic editing, execution orchestration, broader distribution, multi-writer locking, hosted/provider scope, or benchmark claims. Observation is the smallest defensible next state.

A future specification requires fresh evidence such as concrete user friction, a reproducible defect/security finding, controlled benchmark data, or a clearly bounded interoperability/governance blocker.

## Closeout rule

This branch is documentation-only closeout. Specification 020 becomes `CLOSED_CANONICAL` only if the exact closeout head completes required CI/review checks, merges with expected-head protection, the closeout merge second parent is that exact head, canonical post-closeout CI succeeds, and the triggered Release workflow verifies historical `v0.3.0` at product source `70dd66a...` without mutation. Live v0.3.0 tag/release/assets must remain unchanged afterward.

If those conditions succeed, the program enters `POST_V0.3_OBSERVATION` with no active successor specification.
