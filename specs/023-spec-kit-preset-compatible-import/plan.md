# Plan 023 — Spec Kit Preset-Compatible Import

## Objective

Repair the smallest reproduced GitHub Spec Kit compatibility gap by allowing the existing read-only migration report to establish feature identity for template-light preset artifacts from their explicit normalized source path while preserving full-template behavior, deterministic parsing, source binding, and fail-closed safety.

## Canonical base

Shaping candidate base:

`ff9f640bf0e4de5bdd5bf2af0e11b98d86f6587b`

Implementation MUST NOT begin until the documentation-only shaping PR is merged with expected-head protection and resulting canonical `main` passes the permanent five-cell CI matrix.

Planned implementation branch after that gate:

`feat/023-spec-kit-preset-compatible-import`

## Change strategy

### 1. Preserve existing canonical parser first

Keep canonical full-template feature extraction as the first and preferred path. Existing supported artifacts containing:

```text
# Feature Specification: <name>
```

must produce the same feature name, report dictionary, version, and digest as before 023.

### 2. Add path-bound fallback identity only

Refactor the private feature-name helper so it receives both `spec.md` text and the already-normalized source path.

If the canonical heading is absent:

- inspect only the `PurePosixPath` parent already accepted by the importer;
- require a concrete final parent component;
- reject absent or placeholder-like identity;
- return that component verbatim;
- record that fallback was used so the report can emit `FEATURE_NAME_DERIVED_FROM_PATH`.

Do not title-case, strip numeric prefixes, infer from prose, or search arbitrary headings.

### 3. Preserve partial mapping semantics

Existing story, FR/SC, assumptions, plan context, constitution-check, and legacy-task parsers remain authoritative for structured extraction.

If template-light content does not match them:

- structured fields remain empty rather than guessed;
- existing `NO_USER_STORIES_EXTRACTED` / partial-mapping notices remain available;
- the new path-derived identity notice makes the fallback explicit.

### 4. Preserve import version and digest stability

Do not bump `SPECKIT_IMPORT_VERSION`.

Before changing parser behavior, capture the exact current full-template fixture report and digest in a regression assertion. The implementation must prove that canonical existing input output is unchanged.

The only newly accepted inputs are those that previously failed at feature-name extraction but have a concrete path-bound identity.

### 5. Focused tests

Extend `tests/test_speckit.py` with:

- canonical full-template output/digest stability;
- Lean-style template-light `spec.md` under `specs/search-workspace/spec.md` succeeds;
- path fallback identity is exact `search-workspace`;
- `FEATURE_NAME_DERIVED_FROM_PATH` is emitted;
- unmatched prose is not promoted into stories/FR/SC fields;
- a bare `spec.md` without canonical heading fails closed;
- placeholder-like parent identity fails closed;
- reversed mapping order remains deterministic;
- existing unsafe-input tests remain unchanged and green.

No upstream Spec Kit code or fixtures need to be vendored. A small native fixture may model the documented Lean artifact contract and must cite the exact upstream reference in test/documentation comments only when useful.

### 6. Documentation

Update the bounded migration guide to state:

- full-template artifacts receive structured extraction under existing recognized forms;
- template-light preset artifacts may receive path-bound identity plus partial extraction;
- missing semantics are not inferred;
- source artifacts remain digest-bound and read-only;
- Spec Kit presets/hooks/extensions themselves are not imported or executed.

Reconcile Specification 023 tasks/verification and canonical program status. Preserve historical `v0.3.0` claims exactly.

## Expected implementation change surface

```text
src/specgrain/speckit.py
tests/test_speckit.py
docs/migration-from-spec-kit.md
specs/023-spec-kit-preset-compatible-import/plan.md
specs/023-spec-kit-preset-compatible-import/tasks.md
specs/023-spec-kit-preset-compatible-import/verification.md
specs/CURRENT.md
docs/execution-master-plan.md
docs/roadmap.md
```

The shaping-only evidence/authority paths already created for 023 are expected to remain unchanged unless review discovers a factual defect:

```text
docs/research/post-022-spec-kit-1.0-compatibility-audit-2026-08-29.md
docs/adr/0020-path-bound-template-light-speckit-import.md
specs/023-spec-kit-preset-compatible-import/spec.md
```

A product path outside the expected implementation surface requires explicit review against 023 authority before merge.

## Verification order

1. focused `tests/test_speckit.py`;
2. exact full-template report/digest compatibility assertion;
3. template-light bounded acceptance/fail-closed tests;
4. full pytest regression;
5. Ruff over `src`, `tests`, and `examples`;
6. tracked-tree cleanliness after tests;
7. compileall;
8. source CLI smoke including `import-spec-kit --help`;
9. package build;
10. built-wheel reinstall with `--no-deps` and installed CLI smoke;
11. exact shaped-base-to-head diff review;
12. permanent five-cell CI on exact implementation PR head;
13. review comments/threads and review-bot availability recheck without treating unavailable systems as PASS;
14. expected-head product merge;
15. canonical post-product CI and historical `v0.3.0` preservation proof;
16. documentation-only closeout and final canonical verification.

## Non-goals

No Spec Kit runtime integration, preset installer, hooks, extension catalog, bundle parser, workflow runner, agent invocation, SpecNode creation, task promotion, constitution adoption, lifecycle expansion, execution/verification authority, concurrency changes, or release publication.
