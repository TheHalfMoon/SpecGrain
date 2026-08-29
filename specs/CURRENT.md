# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Program status:** `POST_V0.1_ACTIVE`  
**Last closed specification:** `specs/019-native-child-draft-authoring/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/020-v0.3.0-recursive-authoring-release/` — `IMPLEMENTING`  
**Active branch:** `feat/020-v0.3.0-recursive-authoring-release`  
**Next planned specification:** none after 020  
**Published release:** `v0.2.0`  
**Published release source commit:** `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`  
**Published release ID:** `378936896`

## Specification 019 canonical closeout

Specification 019 is `CLOSED_CANONICAL`. Product merge `d6727b6c5cdafcf6265b6d999418c0fe853249a7` passed canonical product CI `33248014390`. Documentation-only closeout merged as `3f8f3d825c3171a3a9ac7761ee5bc642e68a9d2d`; post-closeout CI `33248332725` succeeded and Release verification `33248368659` / job `99089652500` preserved historical `v0.2.0` at `baf00995...` without mutation.

## Specification 020 canonical shaping authority

Documentation-only shaping PR #29 exact head `61f97bd24d2fe9e1ce5a216170368adae38671e3` completed exact-head CI run `33248501598` successfully across the permanent five-cell matrix with no submitted reviews or inline review threads.

PR #29 merged with expected-head protection as canonical shaping merge `05219b4ea7ce1be201c8fb2ff31e707ae02cba17`. Its first parent is exact 019 closeout merge `3f8f3d8...`; its second parent is exact shaping head `61f97bd...`; GitHub signature verification is valid.

Canonical shaping post-merge CI run `33248559704` completed successfully across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11. Therefore Specification 020 implementation authority is active from exact shaping merge `05219b4...`.

## Specification 020 implementation frontier

The release candidate is intentionally distribution-only:

- package version `0.3.0` with runtime dependencies still empty;
- new `docs/releases/v0.3.0.md` describing already-canonical root/child DRAFT authoring and explicit recovery;
- current recursive-authoring/recovery changelog entries promoted from Unreleased into v0.3.0;
- README current-release/install truth updated to v0.3.0;
- launch/release-contract tests updated for the new version while keeping Release workflow monotonic and metadata-derived;
- no `src/specgrain/` product behavior or Release workflow change.

At implementation entry, live GitHub truth had neither `refs/tags/v0.3.0` nor a GitHub Release for `v0.3.0`, so first publication remains eligible only after exact-head PR CI, expected-head merge, and successful canonical post-merge CI.

## Authority rule

Do not claim v0.3.0 released before live tag/release/asset truth proves first publication from the exact successful canonical CI/product head. Historical v0.1.0/v0.2.0 identities must remain unchanged, and no PyPI publication is authorized.
