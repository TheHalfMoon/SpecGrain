# Plan 022 — Native Grain Preparation

## Objective

Close the public v0.3.0 pre-execution authoring dead end by wiring existing schema/lifecycle/readiness semantics into bounded native mutation commands without changing readiness rules or granting execution authority.

## Canonical base

Implementation begins only after this shaping chain is merged to canonical `main` and re-read. The prospective shaping base is `3b98914200c68909f09db08642faf56de48305eb`.

## Change strategy

### 1. Store-level mutation primitives

Add narrowly scoped public operations in `src/specgrain/store.py`:

- shape one existing `DRAFT` using explicit existing-schema readiness fields and transition to `SHAPED`;
- advance one `SHAPED` node to `REFINING` without semantic mutation;
- promote one `REFINING` candidate to `GRAIN` only after exact existing readiness success.

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

The last edge additionally requires existing Grain-readiness v1 success.

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

Primary tests:

- `tests/test_authoring.py` for store/API mutation authority and exact failure/no-mutation semantics;
- `tests/test_authoring_cli.py` for CLI parse/output/workflow behavior;
- focused existing lifecycle/readiness/dependency tests only if a regression fixture needs extension;
- `tests/test_launch.py` only for public command/document truth if required by existing launch guards.

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

- README one-minute/native workflow;
- supported CLI table;
- architecture/product-surface description where current docs explicitly stop at DRAFT;
- CHANGELOG unreleased/current canonical section if used by repository convention;
- Specification 022 evidence files during verification/closeout.

No release/version bump is part of 022.

## Expected implementation change surface

```text
src/specgrain/store.py
src/specgrain/cli.py
src/specgrain/__init__.py
tests/test_authoring.py
tests/test_authoring_cli.py
README.md
docs/architecture.md
CHANGELOG.md
specs/022-native-grain-preparation/*
specs/CURRENT.md
docs/execution-master-plan.md
docs/roadmap.md
```

A path outside this set requires explicit review and justification before merge.

## Verification order

1. focused authoring/API tests;
2. focused authoring CLI tests;
3. full pytest regression;
4. Ruff over `src`, `tests`, and `examples`;
5. compileall;
6. tracked-tree cleanliness after tests;
7. CLI help/smoke including new commands;
8. package build and built-wheel reinstall smoke;
9. exact base-to-head diff review;
10. permanent five-cell CI on exact PR head;
11. review threads/comments and mergeability recheck;
12. expected-head merge;
13. canonical post-merge CI and historical-release no-mutation verification;
14. documentation-only closeout and final canonical verification.

## Non-goals

No `READY`, `RUNNING`, `VERIFYING`, `VERIFIED`, or `CONTROLLED` transition authority. No WorkPacket CLI. No executor. No automatic test command execution. No evidence append. No agent/provider integration. No PyPI/release scope. No readiness redesign.
