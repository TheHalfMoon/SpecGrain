# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–025 are `CLOSED_CANONICAL`. Specification 026 — Supported Mutation Cross-Writer Coordination — is in its terminal final reconciliation. It has `CLOSED_CANONICAL` disposition if and only if this exact reconciliation becomes canonical and canonical post-reconciliation CI succeeds across all five permanent cells. No further Specification 026 product work is authorized. The latest published release remains GitHub Release `378962445` / tag `v0.3.0` at exact historical source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## M0–M7 canonical program

- **000 — Foundation:** `CLOSED_CANONICAL`.
- **001 — SpecNode Schema:** `CLOSED_CANONICAL`.
- **002 — Lifecycle State:** `CLOSED_CANONICAL`.
- **003 — Refinement Tree:** `CLOSED_CANONICAL`.
- **004 — Grain Readiness:** `CLOSED_CANONICAL`.
- **005 — CLI and Local Store:** `CLOSED_CANONICAL`.
- **006 — Dependency Graph:** `CLOSED_CANONICAL`.
- **007 — Repository Scan:** `CLOSED_CANONICAL`.
- **008 — Context Budget:** `CLOSED_CANONICAL`.
- **009 — Work Packet:** `CLOSED_CANONICAL`.
- **010 — Verification and Evidence:** `CLOSED_CANONICAL`.
- **011 — Method Profiles:** `CLOSED_CANONICAL`.
- **012 — Diff, Drift, and Metrics:** `CLOSED_CANONICAL`.
- **013 — Spec Kit Import:** `CLOSED_CANONICAL`.
- **014 — Agent Adapters:** `CLOSED_CANONICAL`.
- **015 — SpecGrainBench:** `CLOSED_CANONICAL` as the repository benchmark framework; invalidated SGB-EXP-001 provides no comparative authority.
- **016 — Public Launch:** `CLOSED_CANONICAL`.

## Post-v0.1 evidence-shaped product adoption

- **017 — Native DRAFT CLI:** `CLOSED_CANONICAL`.
- **018 — v0.2.0 Authoring Release:** `CLOSED_CANONICAL`.
- **019 — Native Child-DRAFT Authoring:** `CLOSED_CANONICAL`.
- **020 — v0.3.0 Recursive Authoring Release:** `CLOSED_CANONICAL`; source `70dd66aba0e68ae710e6ef12605ed153d107bab4`; Release `378962445`.
- **021 — Public Launch Readiness Hardening:** `CLOSED_CANONICAL`.
- **022 — Native Grain Preparation:** `CLOSED_CANONICAL`.
- **023 — Spec Kit Preset-Compatible Import:** `CLOSED_CANONICAL`.
- **024 — Native WorkPacket Export:** `CLOSED_CANONICAL`.
- **025 — Supported Pre-Grain Writer Serialization:** `CLOSED_CANONICAL`.
- **026 — Supported Mutation Cross-Writer Coordination:** product and closeout are canonical; final reconciliation is the only remaining gate.

## Specification 026 selection proof

```text
canonical_base = 1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1
observation_head = 3b557f91ec80c147b30f797198d736c2b6b42518
fixture_blob = ba8cea9510d09415a5bd4d2f123a72f5c8affee8
observation_ci = 33441481985
reproduced_gap = SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION
```

The qualifying fixture used only supported public APIs. A supported child writer could complete between the pre-Grain writer's final exact preimage check and `os.replace`; the pre-Grain writer could then overwrite that successful parent postimage and leave structurally invalid refinement before failing full-project validation.

The earlier observation head `975c47b288cddbfbde34fbbca06afa77ee86f9af` / run `33441425481` stopped at Ruff before test execution and remains non-selection evidence.

## Specification 026 shaping and product proof

```text
shaping_head = 51079a25cdd0f90a9af1cc34ae7577c72ecdf2d6
shaping_push_ci = 33441902147
shaping_pr = 59
shaping_pr_ci = 33442057984
shaping_merge = d27e000728823e93d2fce9ecd669629a839bfdb3
post_shaping_ci = 33442261877

final_product_head = 24728cd52b2daef2c83c5b83f084421b8096a11f
product_push_ci = 33443061640
product_pr = 60
product_pr_ci = 33443161567
product_merge = 69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b
post_product_ci = 33485603844
```

Exact product scope was `src/specgrain/store.py`, `src/specgrain/pregrain.py`, and `tests/test_pregrain_serialization.py`. Delivered behavior is one shared project-scoped non-blocking advisory lock for existing supported pre-Grain persistence and native child authoring, with the existing lock anchor, separate authoring journal/recovery mechanism, Specification 025 preimage/postimage/platform/lifetime/unsafe-anchor/read-only guarantees, lifecycle semantics, and zero runtime dependencies preserved.

The superseded final-logic head `fd27a146b8c39c777b5fb3f1611b2689a1fad3d5` / CI `33442865903` remains non-acceptance evidence because Ruff stopped before tests. Final product push, PR, and canonical post-product CI all completed `success` across the permanent five-cell matrix. PR #60 merged with expected-head protection after exact gate qualification; unavailable/skipped/neutral review systems were not treated as PASS.

## Specification 026 canonical closeout proof

```text
closeout_base = 69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b
closeout_head = 9b6cd1769c24688172ca435b2a77118fa6f4228c
closeout_push_ci = 33486149999
closeout_pr = 61
closeout_pr_ci = 33486307568
closeout_merge = 2c9b18afb74e2254beb254bb84d9c07feec68aa0
post_closeout_ci = 33486523094
```

The closeout changed exactly eight documentation/governance/evidence paths. Push CI, PR CI, and canonical post-closeout CI completed `success` across the permanent five-cell matrix. At the final PR #61 gate, exact base/head/eight-path scope remained unchanged, `mergeable=true`, submitted reviews and inline review threads were zero, Qodo was billing-blocked, CodeRabbit automatic review was skipped by repository-star policy, and Cubic produced no submitted approval. None was treated as PASS.

PR #61 was merged by concurrent activity as GitHub-signature-verified merge `2c9b18afb74e2254beb254bb84d9c07feec68aa0`, with exact parents `69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b` and `9b6cd1769c24688172ca435b2a77118fa6f4228c`. GitHub REST confirms the exact qualified head was merged but does not expose whether the concurrent caller supplied `expected_head_sha`; no claim is made about that unobservable parameter.

## Historical release preservation

Historical `v0.3.0` remains unchanged after canonical closeout:

- source `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release `378962445`;
- wheel asset `535129008`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset `535129009`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

## Still unselected

Arbitrary external/manual writer coordination, universal project transaction management, child-authoring journal redesign, distributed/network locking, blocking waits/retries/leases/timeouts, lifecycle expansion, executor/provider/result/verification/evidence orchestration, automatic context/network/model behavior, new runtime dependencies, broader package publication, hosted/account/dashboard scope, Spec Kit runtime adoption, release publication, empirical benchmark superiority claims, and use of the invalidated `SGB-EXP-001` hidden scorer remain unselected.

## Final reconciliation and continuation discipline

The terminal reconciliation must remain documentation/governance/evidence only and change exactly eight paths. It must receive exact-head push CI and PR CI success across all five permanent cells, unchanged head/base/scope, rechecked reviews/comments/threads/mergeability, and an expected-head merge followed by canonical post-reconciliation five-cell CI.

If those live gates succeed and `v0.3.0` remains unchanged, Specification 026 is `CLOSED_CANONICAL` and the program enters `POST_026_OBSERVATION` without another meta-closeout PR solely to restate merge/CI facts.

After closure, perform a bounded observation/evidence pass against live canonical `main`. Do not invent Specification 027 merely to continue activity; shape a successor only when fresh reproducible evidence independently selects another bounded product gap.
