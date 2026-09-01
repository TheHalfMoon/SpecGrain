# Roadmap

The roadmap is intentionally progressive. Only the nearest active specification should have implementation-level detail. Future work is shaped from current evidence rather than pre-authorized by stale backlog detail.

**Current program state:** Specifications 000–025 are `CLOSED_CANONICAL`. Specification 026 — Supported Mutation Cross-Writer Coordination — is in its terminal final reconciliation. It has `CLOSED_CANONICAL` disposition if and only if this exact reconciliation becomes canonical and canonical post-reconciliation CI succeeds across all five permanent cells. No further Specification 026 product work is authorized. The latest published release remains GitHub Release `378962445` / tag `v0.3.0` at exact historical source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

## M0 — Foundation

**000 — Foundation** established the constitution, product thesis, domain model, architecture, methodology, competitive boundaries, donor policy, benchmark strategy, launch thesis, and program sequence.

## M1 — Deterministic specification kernel

- **001 — SpecNode Schema:** immutable/versioned recursive data model and semantic digest.
- **002 — Lifecycle State:** legal states and deterministic transition validation.
- **003 — Refinement Tree:** recursive structural integrity and parent/child rules.
- **004 — Grain Readiness:** deterministic Definition of Grain and structured blockers.

## M2 — Local product surface

- **005 — CLI and Local Store:** `init`, `check`, repository-local `.specgrain/` storage.
- **006 — Dependency Graph:** dependency validation, blockers, eligible Grains, waves, `next`.

## M3 — Brownfield context

- **007 — Repository Scan:** bounded deterministic repository map.
- **008 — Context Budget:** revision-bound source accounting and required-context blockers.

## M4 — Portable execution boundary

- **009 — Work Packet:** immutable digest-bound WorkPacket and execution-result contracts.
- **010 — Verification and Evidence:** exact-revision independent verification, changed-scope checks, evidence records, and `prove`.

Specification 010 closed the first complete MVP vertical slice at the API layer.

## M5 — Adaptive delivery control

- **011 — Method Profiles:** `quick`, `dmaic-lite`, `dmadv-lite`, `experiment`, `controlled`.
- **012 — Diff, Drift, and Metrics:** scope analysis, drift signals, and delivery metrics.

## M6 — Ecosystem interoperability

- **013 — Spec Kit Import:** `CLOSED_CANONICAL`.
- **014 — Agent Adapters:** generic deterministic WorkPacket/result adapter boundary.

## M7 — Public proof

- **015 — SpecGrainBench:** reproducible experiment ledger and contamination/comparability preflight.
- **016 — Public Launch:** versioned package, cross-platform CI, public examples/guides/trust surfaces, release notes/assets, and `v0.1.0` publication.

## Post-v0.1 — Evidence-shaped product adoption

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

Exact product scope:

- `src/specgrain/store.py`;
- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

Delivered behavior:

- one shared project-scoped non-blocking advisory lock for existing supported pre-Grain persistence and native child authoring;
- existing `.specgrain/tmp/pregrain-mutation.lock` anchor retained;
- child authoring acquires the lock before journal creation and holds it through completion or handled recovery;
- existing authoring journal remains the separate durable recovery mechanism;
- Specification 025 lock/preimage/postimage/platform/lifetime/unsafe-anchor/read-only guarantees remain preserved;
- no journal schema/version, lifecycle, public locking API, runtime dependency, or release change.

The superseded final-logic head `fd27a146b8c39c777b5fb3f1611b2689a1fad3d5` / CI `33442865903` remains non-acceptance evidence because Ruff stopped before tests.

Final product push, PR, and canonical post-product CI all completed `success` across Ubuntu/Python 3.11, Ubuntu/Python 3.12, Ubuntu/Python 3.13, macOS/Python 3.11, and Windows/Python 3.11. PR #60 merged with expected-head protection after exact head/base/scope/review/thread/comment/mergeability rechecks; unavailable/skipped/neutral systems were not treated as PASS.

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

The closeout changed exactly eight documentation/governance/evidence paths. Push CI, PR CI, and canonical post-closeout CI completed `success` across the permanent five-cell matrix.

At the final PR #61 gate, exact base/head/eight-path scope remained unchanged, `mergeable=true`, submitted reviews and inline review threads were zero, Qodo was billing-blocked, CodeRabbit automatic review was skipped by repository-star policy, and Cubic provided descriptive auto-generated summary text rather than a submitted approval. None was treated as PASS.

PR #61 merged with expected-head protection as GitHub-signature-verified merge `2c9b18afb74e2254beb254bb84d9c07feec68aa0`.

## Historical release preservation

Historical `v0.3.0` remains unchanged after canonical closeout:

- source `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release `378962445`;
- wheel asset `535129008`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset `535129009`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

## Still unselected

- arbitrary external/manual writer coordination;
- universal project transaction management;
- child-authoring journal schema/version/recovery redesign;
- distributed/network locking;
- blocking waits, retries, leases, heartbeats, or timeout ownership inference;
- lifecycle expansion;
- executor/provider/result/verification/evidence orchestration;
- automatic context/network/model behavior;
- new runtime dependencies;
- broader package publication;
- hosted/account/dashboard scope;
- Spec Kit runtime adoption;
- release publication;
- empirical benchmark superiority claims.

The invalidated `SGB-EXP-001` hidden scorer remains outside inspection/search/materialization/reproduction/use authority.

## Final reconciliation and continuation discipline

The terminal reconciliation must remain documentation/governance/evidence only and change exactly the same eight program/specification paths used by the closeout family. It must receive exact-head push CI and PR CI success across all five permanent cells, unchanged head/base/scope, rechecked reviews/comments/threads/mergeability, and an expected-head merge followed by canonical post-reconciliation five-cell CI.

If those live gates succeed and `v0.3.0` remains unchanged, Specification 026 is `CLOSED_CANONICAL` and the program enters `POST_026_OBSERVATION` without another meta-closeout PR solely to restate the merge/CI facts.

After closure, perform a bounded observation/evidence pass against live canonical `main`. Do not invent Specification 027 merely to continue activity; shape a successor only when fresh reproducible evidence independently selects another bounded product gap.