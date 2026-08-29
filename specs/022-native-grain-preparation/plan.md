# Plan 022 — Native Grain Preparation

## Objective

Close the public v0.3.0 pre-execution authoring dead end by wiring existing schema/lifecycle/readiness semantics into bounded native mutation commands without changing readiness rules or granting execution authority.

## Canonical base

The documentation-only shaping PR #37 merged with expected-head protection as canonical shaped base `4919a4261f649e81cb1f507c0e80bc5c98d848d8`. Canonical post-shaping CI run `33260132438` succeeded before implementation began.

Implementation branch: `feat/022-native-grain-preparation`.

## Change strategy

### 1. Bounded pre-Grain mutation module

Implement the authorized single-node operations in a dedicated `src/specgrain/pregrain.py` module:

- shape one existing `DRAFT` using explicit existing-schema readiness fields and transition to `SHAPED`;
- advance one `SHAPED` node to `REFINING` without semantic mutation;
- promote one `REFINING` candidate to `GRAIN` only after exact existing readiness success.

The shaped plan originally named `src/specgrain/store.py` as the likely implementation location. Implementation instead keeps the authority in the bounded `pregrain.py` module while reusing the existing store safety primitives. This is an implementation-detail refinement, not an authority expansion.

Reuse the current safe local-store machinery:

- project load and pending-authoring refusal;
- immutable `SpecNode` reconstruction;
- refinement/dependency validation;
- exact preimage read;
- same-directory temporary file + `os.replace` replacement;
- post-write project validation.

Do not widen ADR-0018's multi-file journal. 022 operations touch one canonical SpecNode file each.

### 2. Lifecycle authorization

Use the existing lifecycle validator for each edge. No direct skipping is permitted:

```text
DRAFT -> SHAPED
SHAPED -> REFINING
REFINING -> GRAIN
```

The last edge additionally requires existing Grain-readiness v1 success on the exact current candidate and complete forest.

### 3. CLI

Extend `src/specgrain/cli.py` with:

- `shape` and explicit readiness-field arguments;
- `refine`;
- `grain`;
- deterministic text/JSON output and stable non-zero failure behavior.

Do not add interactive/model-assisted authoring in 022. Explicit CLI inputs keep CI and trust semantics deterministic.

### 4. Public API

Export the bounded functions/result types from `src/specgrain/__init__.py` without changing existing API names or behavior.

### 5. Tests

Primary tests are intentionally isolated from the older DRAFT-authoring suites:

- `tests/test_pregrain.py` for API mutation authority and exact failure/no-mutation semantics;
- `tests/test_pregrain_cli.py` for CLI parse/output/workflow behavior;
- `tests/test_launch.py` for public release/current-source document truth and release preservation guards.

Required workflow fixture:

```text
init
-> draft
-> shape
-> refine
-> check (Grain-ready: 1)
-> grain
-> next (candidate considered by dependency eligibility)
```

Also prove a readiness-blocked candidate remains `REFINING` and unchanged after `grain` failure.

### 6. Documentation

Update only the bounded product truth:

- README published-release vs. current-source workflow and CLI distinction;
- architecture/product-surface description;
- CHANGELOG `Unreleased` section while preserving the historical v0.3.0 section;
- Specification 022 task/status/verification evidence;
- canonical `CURRENT`, execution master plan, and roadmap frontier text.

No release/version bump is part of 022. The historical v0.3.0 tag/release remains the published contract and must not be rewritten to include Specification 022 commands.

## Expected implementation change surface

```text
src/specgrain/pregrain.py
src/specgrain/cli.py
src/specgrain/__init__.py
tests/test_pregrain.py
tests/test_pregrain_cli.py
tests/test_launch.py
README.md
docs/architecture.md
CHANGELOG.md
specs/022-native-grain-preparation/plan.md
specs/022-native-grain-preparation/tasks.md
specs/022-native-grain-preparation/verification.md
specs/CURRENT.md
docs/execution-master-plan.md
docs/roadmap.md
```

`src/specgrain/store.py` remains reused but unchanged. A path outside this set requires explicit review and justification before product merge.

## Verification checkpoints

Initial implementation checkpoint `05865fdfeb89e259be237f5e020a87424384d122` passed permanent CI run `33260707422` across all five cells, including 573 full-regression tests, Ruff, tracked-tree cleanliness, compile, CLI smoke, package build, built-wheel install, and installed CLI smoke.

That checkpoint is not the final product candidate because public documentation reconciliation still had to be committed. Final verification must bind to the documentation-reconciled exact head.

## Verification order

1. focused pre-Grain API tests;
2. focused pre-Grain CLI tests;
3. launch/document guards;
4. full pytest regression;
5. Ruff over `src`, `tests`, and `examples`;
6. compileall;
7. tracked-tree cleanliness after tests;
8. CLI help/smoke including new commands;
9. package build and built-wheel reinstall smoke;
10. exact base-to-head diff review;
11. permanent five-cell CI on exact PR head;
12. review threads/comments and mergeability recheck;
13. expected-head merge;
14. canonical post-merge CI and historical-release no-mutation verification;
15. documentation-only closeout and final canonical verification.

## Non-goals

No `READY`, `RUNNING`, `VERIFYING`, `VERIFIED`, or `CONTROLLED` transition authority. No WorkPacket CLI. No executor. No automatic test command execution. No evidence append. No agent/provider integration. No PyPI/release scope. No readiness redesign.
