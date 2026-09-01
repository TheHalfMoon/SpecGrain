# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Canonical post-025 normalization baseline:** `1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1`  
**Canonical Specification 026 shaping merge:** `d27e000728823e93d2fce9ecd669629a839bfdb3`  
**Canonical Specification 026 post-shaping CI:** `33442261877` — `completed/success` across all five permanent cells  
**Canonical Specification 026 product merge:** `69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b`  
**Canonical Specification 026 post-product CI:** `33485603844` — `completed/success` across all five permanent cells  
**Program status:** `SPEC_026_CLOSEOUT_CANDIDATE`  
**Last closed specification:** `specs/025-supported-pregrain-writer-serialization/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/026-supported-mutation-cross-writer-coordination/` — `PRODUCT_VERIFIED_CLOSEOUT_PENDING`  
**Active product implementation:** none; Specification 026 product work is merged and post-product verified  
**Published release:** `v0.3.0`  
**Published release source:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Published release ID:** `378962445`

## Previous canonical frontier

Specification 025 — Supported Pre-Grain Writer Serialization — remains `CLOSED_CANONICAL`. The post-025 normalization baseline is `1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1`, with canonical post-normalization CI `33440739066` successful across all five permanent cells.

The SGB-EXP-001 comparative experiment remains `INVALIDATED_ORACLE_REVEALED_PRE_FREEZE`; it produced no valid comparative result, supports no superiority claim, selected no product work, and its hidden scorer remains outside all authority.

## Specification 026 selection proof

Fresh observation against the exact post-025 canonical baseline reproduced the bounded supported-writer gap:

```text
canonical_base = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
canonical_tree = ffe4dbff9658524eedf359451578a9d0446fed4c
observation_branch = obs/post-025-supported-cross-writer-fixture
observation_head = 3b557f91ec80c147b30f797198d736c2b6b42518
fixture = tests/test_post_025_supported_cross_writer_observation.py
fixture_blob = ba8cea9510d09415a5bd4d2f123a72f5c8affee8
ci_run = 33441481985
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION
```

The final fixture proved that supported `create_child_draft_spec` could complete successfully after a supported pre-Grain writer's final parent preimage check but before `os.replace`, after which the pre-Grain writer could overwrite the successful parent postimage and leave invalid refinement before failing project revalidation.

The earlier observation head `975c47b288cddbfbde34fbbca06afa77ee86f9af` / CI `33441425481` is not selection evidence because Ruff stopped the harness before test execution.

Selection record: `docs/research/post-025-supported-cross-writer-reproduction-2026-09-01.md`  
Architectural decision: `docs/adr/0021-supported-mutation-cross-writer-coordination.md`

## Specification 026 shaping proof

```text
shaping_head = 51079a25cdd0f90a9af1cc34ae7577c72ecdf2d6
shaping_push_ci = 33441902147
shaping_pr = 59
shaping_pr_ci = 33442057984
shaping_merge = d27e000728823e93d2fce9ecd669629a839bfdb3
post_shaping_ci = 33442261877
```

The shaping diff was documentation/governance/evidence only. Push CI, PR CI, and canonical post-shaping CI completed `success` across Ubuntu/Python 3.11, Ubuntu/Python 3.12, Ubuntu/Python 3.13, macOS/Python 3.11, and Windows/Python 3.11 before implementation authority became live.

## Specification 026 product proof

Final implementation head:

```text
24728cd52b2daef2c83c5b83f084421b8096a11f
```

Exact product diff changed only:

- `src/specgrain/store.py`;
- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

The delivered implementation shares one project-scoped non-blocking advisory lock between supported pre-Grain persistence and native child authoring. The existing `.specgrain/tmp/pregrain-mutation.lock` anchor, standard-library Unix/Windows primitives, fail-closed contention/unsafe-anchor behavior, descriptor/process ownership, exact-preimage/postimage defenses, authoring journal and recovery semantics, lifecycle rules, read-only behavior, and zero runtime dependencies are preserved.

```text
final_product_head = 24728cd52b2daef2c83c5b83f084421b8096a11f
push_ci = 33443061640
product_pr = 60
product_pr_ci = 33443161567
product_merge = 69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b
post_product_ci = 33485603844
```

The first final-logic head `fd27a146b8c39c777b5fb3f1611b2689a1fad3d5` / push CI `33442865903` is explicitly not acceptance evidence because Ruff source stopped before tests. The subsequent repair normalized imports only.

At the final PR #60 merge gate, exact head/base and three-file scope remained unchanged, `mergeable=true`, submitted reviews were `0`, and inline review threads were `0`. Qodo was billing-blocked, automatic CodeRabbit review was skipped by repository-star policy, and Cubic was neutral because its monthly review line limit was reached. None was treated as PASS.

PR #60 merged with expected-head protection. Canonical post-product CI `33485603844` completed `success` across all five permanent cells.

## Historical release preservation

Live GitHub truth after the product merge remains:

- tag `v0.3.0` -> `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release ID `378962445`, target `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- wheel asset `535129008`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset `535129009`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

Specification 026 did not publish or mutate a release.

## Explicitly unselected after product delivery

No Specification 026 authority exists for arbitrary non-cooperating writer coordination, universal project transaction management, child-authoring journal schema/recovery redesign, distributed locking, blocking waits/retries/timeouts/leases, runtime dependencies, lifecycle expansion, executor/provider/result/verification/evidence orchestration, automatic context/network/model behavior, Spec Kit runtime adoption, release publication, hosted scope, or benchmark superiority claims.

## Current execution gate

Current exact state:

1. Specification 025 remains `CLOSED_CANONICAL`;
2. Specification 026 shaping is canonical and its product implementation is merged;
3. canonical post-product CI is successful across all five permanent cells;
4. historical `v0.3.0` remains unchanged;
5. no further Specification 026 product implementation is authorized;
6. the active work is documentation/governance/evidence-only closeout;
7. Specification 026 must not be called `CLOSED_CANONICAL` until the exact closeout PR and final evidence reconciliation are merged with expected-head protection and their canonical post-merge CI gates succeed;
8. after closure, return to observation unless fresh reproducible evidence independently selects another bounded product gap.

Do not widen Specification 026 and do not use the invalidated `SGB-EXP-001` hidden scorer for product selection or benchmark claims.
