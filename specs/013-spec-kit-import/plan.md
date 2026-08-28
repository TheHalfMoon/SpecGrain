# Plan 013 — Spec Kit Import

## Design

Add one dependency-free `speckit.py` migration module, bounded exports, a read-only CLI command, and focused tests.

### Source boundary

Supported v1 roles are inferred only from known basenames: `spec.md`, `plan.md`, `tasks.md`, and explicit `constitution.md`. Input paths are normalized repository-relative POSIX paths; local loading rejects symlinks/non-files and reads at most the configured byte ceiling.

### Mapping boundary

Map only fields with deterministic structural anchors in current Spec Kit artifacts. Preserve source artifact digests and emit partial-mapping notices for material source content not represented as structured fields.

Legacy tasks remain `LegacyTask` records in the migration report and are not converted into SpecGrain task/spec ontology.

### CLI

`specgrain import-spec-kit <feature_dir> --source-revision <revision> [--constitution <path>] [--json]`

The CLI returns a report only. It performs no repository mutation.

## Change surface

- `src/specgrain/speckit.py`
- `src/specgrain/cli.py`
- `src/specgrain/__init__.py`
- `tests/test_speckit.py`
- `tests/test_speckit_cli.py`
- Specification/ADR/continuation records only.

## Verification

Run full 001–013 pytest regression, compileall, editable install using available local build dependencies, console/module parity, line-length inspection, read-only CLI tests, exact uploaded blob verification, and exact-diff review.
