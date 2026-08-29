# Specification 019 Closeout

## Status

`CLOSEOUT_PENDING_CANONICAL`

This document is authored on the documentation-only closeout branch. Specification 019 becomes `CLOSED_CANONICAL` only if the exact closeout head passes required CI/review, merges with expected-head protection, and canonical post-closeout CI succeeds. The branch text is not itself closure authority.

## Canonical shaping authority

Specification 019 shaping was canonical before implementation began:

- shaping PR: #26;
- exact shaping head: `25ed7e1b86b232cf869635dd9947ccf5b54324de`;
- exact-head shaping CI: `33246570813` — success across the permanent five-cell matrix;
- shaping merge: `e10cce6b11cbe4724881936858d7721baa938667`;
- shaping merge first parent: `c5282caa29fbfeb8c118755766b6a7b8a49d2781`;
- shaping merge second parent: exact shaping head `25ed7e1...`;
- canonical shaping post-merge CI: `33246611384` — success across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11.

ADR-0018 was part of that canonical authority chain and defined the recoverable/fail-closed multi-file authoring boundary.

## Product implementation and review

Implementation branch `feat/019-native-child-draft-authoring` started from exact canonical shaping merge `e10cce6...`.

Material forward repairs were preserved in history:

1. `8b0a89252f3b43bcfd0a1d6c72756b7754876cc2` repaired child-collision ownership so a supported `O_EXCL` collision cannot delete an externally created matching child through handled rollback.
2. `994f40f84ad3696b4037ea05eaec746c19bb473f` repaired the isolated repository-CLI fixture after CI exposed four import errors following `550 passed`; this did not alter product behavior.

Exact reviewed product head `994f40f84ad3696b4037ea05eaec746c19bb473f` completed push CI run `33247361906` successfully across all five permanent jobs. Ubuntu/Python 3.11 recorded `554 passed`, Ruff success, tracked-tree cleanliness, compileall, CLI smoke including `recover`, package build, built-wheel reinstall, and installed CLI smoke.

The final PR evidence head was `53cd8482b727d4f61bfafbea6ed363e4e8783d52`. Its delta after the reviewed product head contained only `review.md`, `verification.md`, and task-state reconciliation. Exact-head PR CI run `33247844945` completed `success` across all five permanent matrix cells on that exact final head.

At merge time PR #27 was mergeable, had no submitted reviews, and had no inline review threads. Qodo billing/trial suspension and CodeRabbit automatic-review skip were not treated as approvals.

## Product merge proof

PR #27 merged with expected-head protection at exact final head `53cd8482b727d4f61bfafbea6ed363e4e8783d52`.

Canonical product merge:

`d6727b6c5cdafcf6265b6d999418c0fe853249a7`

GitHub records:

- first parent: canonical shaping merge `e10cce6b11cbe4724881936858d7721baa938667`;
- second parent: exact final PR head `53cd8482b727d4f61bfafbea6ed363e4e8783d52`;
- commit signature verification: `verified` / `valid`.

Canonical product post-merge CI run `33248014390` completed `success` on exact product merge `d6727b6...` across the permanent five-cell matrix.

## Release-preservation proof

Specification 019 intentionally did not change package version or publish a new release. Package metadata remained `0.2.0`.

Post-product Release workflow run `33248070688`, job `99088883873`, checked out exact canonical product merge `d6727b6...`, derived release metadata from package version `0.2.0`, rebuilt the expected wheel and source distribution, and completed successfully through the existing-release verification path.

The log records:

> `SpecGrain v0.2.0 is already published at historical tag target baf00995a7ae9cf01b6196d68c62f4eca2c1ec85; no release mutation is required.`

Live GitHub truth after the run remained:

- tag `v0.2.0` -> `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`;
- GitHub Release ID `378936896`;
- release name `SpecGrain v0.2.0`, public/non-prerelease;
- wheel ID `535032845`, size `66709`, digest `sha256:08b04328fd3896a19d3404928a582049887b0238b044e6e854b32769f132ab77`;
- sdist ID `535032844`, size `96850`, digest `sha256:0b8c4b02652c162649c7970904269be3038d04ce8604dbd7469e475b229c0bfd`.

## Delivered product boundary

Current canonical product source now supports:

- existing root `DRAFT` authoring through `create_draft_spec` / `specgrain draft`;
- native child `DRAFT` authoring through `create_child_draft_spec` / `specgrain draft --parent` only under an existing `DRAFT` parent;
- deterministic reciprocal parent/child structure and lowest-unused ID allocation;
- ADR-0018 recoverable/fail-closed authoring journal semantics;
- explicit `recover_authoring_transaction` / `specgrain recover`;
- fail-closed ordinary reads while a journal is pending;
- no automatic lifecycle promotion, readiness synthesis, execution/provider authority, dependency change, package-version bump, or benchmark claim.

Residual concurrency and filesystem limits remain documented in `review.md`; they are not hidden or represented as stronger locking/durability guarantees.

## Fresh product audit

`docs/research/post-019-product-audit-2026-08-29.md` re-evaluates the frontier from exact canonical product source `d6727b6...`.

The audit observes a new distribution discontinuity: canonical `main` now contains child-DRAFT authoring and explicit recovery, while published `v0.2.0` intentionally predates both surfaces. It recommends a bounded **v0.3.0 Recursive Authoring Release** as the smallest next shaping candidate because ADR-0017 already defines monotonic release semantics and pre-1.0 backward-compatible public features require a minor version bump.

That recommendation is evidence only. It does not authorize Specification 020, a version bump, a release, or implementation work. Any successor requires a separate shaping chain after 019 is genuinely `CLOSED_CANONICAL`.

## Closure gate

Specification 019 may be called `CLOSED_CANONICAL` only after all of the following are live facts:

1. this documentation-only closeout branch has a fixed exact head;
2. required exact-head CI/review checks succeed on that head;
3. the closeout PR merges with expected-head protection using that same head;
4. the merge second parent is that exact closeout head;
5. canonical post-closeout CI succeeds on the exact closeout merge;
6. the existing `v0.2.0` release remains unchanged if release verification is triggered again.

Until then, the status remains `CLOSEOUT_PENDING_CANONICAL`.
