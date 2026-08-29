# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Program status:** `POST_V0.1_ACTIVE`  
**Last closed specification:** `specs/017-native-draft-cli/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/018-v0.2.0-authoring-release/` — `RUNNING`  
**Active branch:** `feat/018-v0.2.0-authoring-release`  
**Next planned specification:** none beyond 018  
**Published release:** `v0.1.0` until live v0.2.0 publication is verified  
**Published v0.1.0 source:** `5eb46db0479cb8707afe070027dab4f3c558849a`  
**Canonical 018 shaping merge:** `b170aed92812c367282fbacb5d46e5acb450a196`

## Specification 018 authority

Shaping PR #23 exact head `68e830dc51d0df4bc521607be46ce9f11dc34acd` completed exact-head CI run `33237175016` successfully with no submitted reviews or inline review threads. It merged with expected-head protection as `b170aed92812c367282fbacb5d46e5acb450a196`; that merge has the exact shaping head as its second parent. Canonical shaping post-merge CI run `33245330017` also completed the permanent five-cell matrix successfully.

ADR-0017 is therefore canonical authority for monotonic metadata-derived GitHub releases. Implementation is bounded to package/release identity, release automation, release-facing documentation, and deterministic release-contract guards; it adds no new SpecGrain product behavior.

## Product/release boundary

Current canonical product behavior includes `specgrain draft` and public `create_draft_spec`. The implementation branch prepares package version `0.2.0`, release notes, and a reusable fail-closed GitHub release workflow. No `v0.2.0` release claim is valid until the product merge, exact post-merge CI, release workflow, live tag/release, and asset evidence required by Specification 018 succeed.

No PyPI publication, recursive refinement CLI, executor orchestration, hosted service, runtime dependency, or benchmark winner is authorized by Specification 018.
