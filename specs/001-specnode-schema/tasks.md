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
- [x] T014 Add canonical ordering, Unicode, round-trip, and schema-version tests.
- [x] T015 Add digest equivalence/difference tests, including state exclusion.
- [x] T016 Run available local verification: 23 pytest tests PASS, compileall PASS, digest seed smoke PASS; ruff explicitly NOT RUN because unavailable. See `verification.md`.
- [ ] T017 Review exact branch diff against 001 scope and confirm no lifecycle/graph/CLI/readiness creep.

## PR closeout

- [ ] T018 Open bounded implementation PR with exact test evidence and no unsupported completion claims.
- [ ] T019 Resolve all exact-head review/check defects.
- [ ] T020 Merge only with expected-head evidence, then re-read canonical `main` before `002-lifecycle-state`.
