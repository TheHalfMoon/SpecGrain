# Verification — Specification 026 Supported Mutation Cross-Writer Coordination

**Status:** `PRODUCT_VERIFIED_CLOSEOUT_PENDING`  
**Canonical shaping merge:** `d27e000728823e93d2fce9ecd669629a839bfdb3`  
**Canonical post-shaping CI:** `33442261877` — `completed/success` across all five permanent cells  
**Final implementation head:** `24728cd52b2daef2c83c5b83f084421b8096a11f`  
**Canonical product merge:** `69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b`  
**Canonical post-product CI:** `33485603844` — `completed/success` across all five permanent cells  
**Published release preserved:** `v0.3.0` / Release `378962445`

## Selection evidence

```text
canonical_base = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
canonical_tree = ffe4dbff9658524eedf359451578a9d0446fed4c
observation_head = 3b557f91ec80c147b30f797198d736c2b6b42518
fixture_blob = ba8cea9510d09415a5bd4d2f123a72f5c8affee8
ci_run = 33441481985
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION
```

The qualifying fixture used only supported public `shape_draft_spec` and `create_child_draft_spec` APIs. The earlier observation head `975c47b288cddbfbde34fbbca06afa77ee86f9af` / run `33441425481` is not selection evidence because Ruff stopped execution before the fixture ran.

## Shaping evidence

```text
shaping_base = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
shaping_head = 51079a25cdd0f90a9af1cc34ae7577c72ecdf2d6
shaping_push_ci = 33441902147
shaping_pr = 59
shaping_pr_ci = 33442057984
shaping_merge = d27e000728823e93d2fce9ecd669629a839bfdb3
post_shaping_ci = 33442261877
```

The shaping change was documentation/governance/evidence only. Push, PR, and canonical post-shaping CI completed `success` across Ubuntu/Python 3.11, Ubuntu/Python 3.12, Ubuntu/Python 3.13, macOS/Python 3.11, and Windows/Python 3.11 before implementation authority became live.

## Product implementation evidence

Final implementation head:

```text
24728cd52b2daef2c83c5b83f084421b8096a11f
```

Exact shaped-base-to-head product diff changed only:

- `src/specgrain/store.py`;
- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

The implementation moves the existing private operating-system advisory lock implementation into the lower-level store module as `_supported_mutation_lock`, aliases the historical pre-Grain private helper to that same callable, and makes `create_child_draft_spec` acquire the shared lock before authoring journal creation. The lock remains project-scoped, non-blocking, standard-library-only, anchored at `.specgrain/tmp/pregrain-mutation.lock`, descriptor/process-owned, and fail-closed on contention or unsafe anchors.

The existing authoring journal remains a separate durable recovery mechanism. `AUTHORING_TRANSACTION_VERSION`, journal schema, recovery classifications, child-ID semantics, lifecycle rules, exact preimage/postimage defenses, and read-only behavior were not widened.

Corrected-invariant coverage proves:

- pre-Grain and child authoring use the identical shared lock callable;
- pre-Grain ownership makes a competing supported child writer fail before journal/child/parent side effects;
- child-authoring ownership makes a competing supported pre-Grain writer fail before target mutation;
- the successful writer leaves a structurally valid project;
- Specification 025 stale-writer, lifetime, process-exit, unsafe-anchor, persistent-anchor, shape/refine/grain, and read-only guarantees remain covered;
- existing child-authoring recovery behavior remains in the full regression suite.

## Product CI evidence

A superseded final-logic head is retained as non-acceptance evidence:

```text
head = fd27a146b8c39c777b5fb3f1611b2689a1fad3d5
push_ci = 33442865903
result = failed at Ruff source before tests
```

The only subsequent repair normalized imports; it did not change product behavior or test topology.

Final exact-head push qualification:

```text
head = 24728cd52b2daef2c83c5b83f084421b8096a11f
push_ci = 33443061640
status = completed
conclusion = success
```

Exact-head PR qualification:

```text
product_pr = 60
product_pr_ci = 33443161567
status = completed
conclusion = success
```

Both qualifying runs passed the permanent five-cell matrix and the configured Ruff source/tests/examples, full regression, tracked-tree cleanliness, compileall, source CLI smoke, package build, built-wheel installation, and installed CLI smoke gates.

## Product review and merge evidence

At the final PR #60 merge gate:

```text
base = d27e000728823e93d2fce9ecd669629a839bfdb3
head = 24728cd52b2daef2c83c5b83f084421b8096a11f
changed_files = 3
mergeable = true
submitted_reviews = 0
inline_review_threads = 0
```

Review-system disposition was recorded without manufacturing approval:

- Qodo was billing-blocked — not PASS;
- CodeRabbit automatic review was skipped because the repository did not meet its star-policy threshold — not PASS;
- Cubic returned neutral because its monthly review line limit was reached — not PASS.

PR #60 merged with expected-head protection as:

```text
product_merge = 69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b
```

Canonical post-product CI:

```text
run = 33485603844
head = 69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b
status = completed
conclusion = success
```

All five permanent cells succeeded.

## Historical release preservation

Live GitHub truth after the product merge remains:

- tag `v0.3.0` -> `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release ID `378962445`, target `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- wheel asset `535129008`, size `70463`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset `535129009`, size `104057`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

Specification 026 published or mutated no release.

## Closeout gate

Product acceptance evidence is complete. Canonical closeout is not yet complete.

Required remaining evidence:

1. documentation/governance/evidence-only closeout branch exact diff and push CI;
2. closeout PR exact head/base/scope, PR CI, reviews/comments/threads/mergeability and review-system disposition;
3. expected-head closeout merge;
4. canonical post-closeout five-cell CI;
5. final evidence reconciliation recording exact closeout facts without widening product authority;
6. canonical post-reconciliation five-cell CI and final governance/release-preservation recheck.

Until those gates are proven, Specification 026 is not `CLOSED_CANONICAL`.