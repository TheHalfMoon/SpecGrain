# Tasks 001 — SpecNode Schema

Tasks are intentionally small and ordered.

## Planning

- [x] T001 Re-read canonical `main` after foundation merge and confirm `001-specnode-schema` is next.
- [x] T002 Define exact 001 in-scope/out-of-scope behavior and acceptance criteria.
- [x] T003 Choose a standard-library-only core implementation for this slice and document the serialization/digest boundary.

## Package scaffold

- [x] T004 Add minimal `pyproject.toml` for Python 3.11+, src layout, pytest, and ruff dev configuration.
- [x] T005 Add `src/specgrain/__init__.py` public exports.
- [x] T006 Add `SpecValidationError` and SpecGrain ID validation in `src/specgrain/model.py`.

## SpecNode model

- [x] T007 Implement recursive JSON-safe freezing/canonicalization helpers.
- [x] T008 Implement immutable `SpecNode` construction and field validation.
- [x] T009 Implement detached `to_dict()` and `from_dict()` round trip.
- [x] T010 Implement canonical semantic content dictionary/JSON normalization.
- [x] T011 Implement state-excluded, schema-version-bound SHA-256 `revision_digest`.

## Verification

- [x] T012 Add focused unit tests for ID/string/duplicate validation.
- [x] T013 Add mutation-isolation and nested JSON-safety tests.
- [x] T014 Add canonical ordering, Unicode, round-trip, schema-version, and golden-vector tests.
- [x] T015 Add digest equivalence/difference tests, including state exclusion.
- [x] T016 Run available local verification: 24 pytest tests PASS, compileall PASS, digest seed smoke PASS, golden vector PASS; ruff explicitly NOT RUN because unavailable. See `verification.md`.
- [x] T017 Review exact PR head `0381d5b3b5699ea5959d197bcbbc961a69b22904` against 001 scope; no lifecycle/graph/CLI/readiness creep or material defect remained.

## PR closeout

- [x] T018 Open bounded implementation PR #2 with exact test evidence and no unsupported completion claims.
- [x] T019 Resolve exact-head review defects F-001/F-002; CodeRabbit SUCCESS and no unresolved review threads on the final head.
- [x] T020 Merge PR #2 with expected-head guard; canonical merge commit is `619b7501fc659588fc344af8835cc910a42bff31`. Re-read canonical `main` before starting 002.

**Result:** `CLOSED_CANONICAL` at merge commit `619b7501fc659588fc344af8835cc910a42bff31`.
