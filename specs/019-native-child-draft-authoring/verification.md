# Specification 019 Verification Record

## Authority

Specification 019 shaping became canonical through PR #26. The exact shaping head was `25ed7e1b86b232cf869635dd9947ccf5b54324de`; exact-head CI run `33246570813` completed successfully before expected-head merge `e10cce6b11cbe4724881936858d7721baa938667`. The merge second parent is the exact shaping head. Canonical shaping post-merge CI run `33246611384` then completed the permanent five-cell matrix successfully.

## Implementation history

Implementation branch: `feat/019-native-child-draft-authoring`, created from exact canonical shaping merge `e10cce6b11cbe4724881936858d7721baa938667`.

- `cae5fe95b72d197c27eda43c5221010af41e9b7f` — initial bounded child-DRAFT authoring, transaction/recovery, CLI, documentation, and focused tests.
- `e7f7f1e76650494a5c3dce5bf423da7d5df0dcb8` — implementation candidate completion before manual collision review.
- `8b0a89252f3b43bcfd0a1d6c72756b7754876cc2` — forward safety repair preserving an externally created colliding child instead of entering child-only rollback.
- `994f40f84ad3696b4037ea05eaec746c19bb473f` — forward regression-fixture repair after the isolated repository CLI fixture did not expose the new store imports.

No force-push, rebase, history rewrite, package-version bump, release mutation, runtime dependency, lifecycle promotion, readiness synthesis, executor/provider behavior, or benchmark claim is part of this implementation chain.

## Exact product-head CI

Push CI run `33247361906` executed on exact product head `994f40f84ad3696b4037ea05eaec746c19bb473f` and completed successfully across all permanent jobs:

- Ubuntu / Python 3.12 — job `99087054969`;
- Ubuntu / Python 3.13 — job `99087055093`;
- Windows / Python 3.11 — job `99087055097`;
- macOS / Python 3.11 — job `99087055116`;
- Ubuntu / Python 3.11 — job `99087055170`.

Ubuntu/Python 3.11 recorded:

- Ruff source/tests/examples: success;
- full regression: `554 passed in 1.57s`;
- tracked-tree cleanliness: success;
- compileall across source/tests/examples: success;
- source and installed CLI smoke expose `init`, `draft`, `recover`, `check`, `next`, `scan`, `prove`, and `import-spec-kit`;
- package build produced `specgrain-0.2.0.tar.gz` and `specgrain-0.2.0-py3-none-any.whl` successfully;
- built-wheel reinstall and installed CLI smoke: success.

The immediately preceding run `33247281069` on `8b0a892...` failed only in four isolated `tests/test_repository_cli.py` fixture imports after `550 passed`; Ruff had succeeded. Commit `994f40f...` updated that fixture to expose the new store symbols, and the successor exact-head matrix passed all gates.

## Product behavior evidence

Focused tests cover normal and nested child creation, lowest-unused ID allocation, reciprocal structure, non-DRAFT and missing-parent rejection, invalid existing forests, pending-journal blocking, safe recovery classifications, ambiguous recovery refusal, parent-replacement rollback, child-collision ownership, deterministic CLI text/JSON behavior, and internal-error redaction.

The implementation preserves root-DRAFT behavior when `--parent` is absent. Child authoring creates a child fixed to `DRAFT`, requires an existing parent fixed to `DRAFT`, validates the complete proposed forest before the journal/canonical write sequence, and changes the selected parent only by appending the child ID to `children`.

## External review boundary

At exact product head `994f40f...`, GitHub reported no submitted pull-request reviews and no inline review threads. Qodo reported billing/trial review suspension. CodeRabbit reported that automatic review was skipped because the repository had fewer than ten stars. Neither condition is treated as approval or verification.

## Successor-head rule

This evidence commit advances the PR head. The successor exact head must complete the required permanent CI matrix and be rechecked for reviews, threads, mergeability, and exact diff before expected-head product merge. This record does not pre-authorize merge of an unproved successor head.
