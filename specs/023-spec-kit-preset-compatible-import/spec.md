# Specification 023 — Spec Kit Preset-Compatible Import

## Status

`SHAPED`

This specification is a shaping candidate until its documentation-only shaping head is merged with expected-head protection and canonical post-shaping CI succeeds.

## Outcome

Allow the existing deterministic read-only `import-spec-kit` boundary to accept bounded template-light GitHub Spec Kit feature artifacts from official preset workflows, notably the bundled Lean preset, without requiring the full canonical Spec Kit Markdown template and without inventing missing semantics.

## Evidence

Post-022 compatibility audit:

`docs/research/post-022-spec-kit-1.0-compatibility-audit-2026-08-29.md`

Exact comparison revisions:

- SpecGrain canonical base: `ff9f640bf0e4de5bdd5bf2af0e11b98d86f6587b`;
- GitHub Spec Kit reviewed `main`: `51e52be6c3b26fed3ff5424c671f4a559519a759`;
- latest observed upstream release: `v1.0.1`;
- standard upstream spec template blob: `ceb28776215a098e977650ac090c785dcbf53651`;
- bundled Lean README blob: `ab17257f96091590d2289699aaf2b114cc05bbbe`;
- bundled Lean `speckit.specify` blob: `c15353557aa941b18e811c15aef605c41ff64133`.

The current SpecGrain importer rejects any `spec.md` that lacks the exact canonical `# Feature Specification:` heading. The bundled Lean preset explicitly produces focused Markdown without requiring full-template boilerplate. Therefore an official current Spec Kit artifact can fail before migration solely because of template shape.

## Required behavior

1. Preserve the current canonical full-template import path exactly when `# Feature Specification: <name>` is present.
2. When that canonical heading is absent, derive feature identity only from the final parent component of the normalized repository-relative `spec.md` path.
3. Reject fallback identity when the source is a bare top-level `spec.md`, when the parent identity is absent, or when it is an unresolved placeholder-like component.
4. Emit an explicit `FEATURE_NAME_DERIVED_FROM_PATH` notice whenever path-bound fallback identity is used.
5. Continue to parse stories, FR/SC items, assumptions, Technical Context, Constitution Check, and legacy tasks only through existing deterministic recognized structures.
6. Do not infer unrecognized structured semantics from arbitrary prose. Unmatched source remains source-digest-bound and explicitly partially mapped.
7. Preserve existing source-safety rules: normalized repository-relative paths, known roles only, ordinary UTF-8 files, byte limits, duplicate-role rejection, source revision binding, and SHA-256 artifact binding.
8. Preserve legacy tasks as evidence only; `tasks_promoted_to_core` remains false.
9. Preserve read-only behavior: no `.specgrain` writes, source mutation, repository command execution, preset installation, hook execution, or upstream code execution.
10. Keep `SPECKIT_IMPORT_VERSION == 1` because the report schema and existing full-template interpretation do not change.
11. Preserve exact serialized report content and digest for already-supported canonical full-template fixtures.
12. Add no runtime dependency.

## Acceptance

### A1 — Existing canonical format stability

For the current full-template test fixture, after 023 implementation:

- `to_dict()` is identical to the pre-023 result;
- report digest is identical to the pre-023 result;
- `SPECKIT_IMPORT_VERSION` remains `1`.

### A2 — Template-light bounded acceptance

Given a template-light `spec.md` at a path such as:

```text
specs/search-workspace/spec.md
```

with no canonical `# Feature Specification:` heading, import succeeds and:

- `feature_name == "search-workspace"`;
- `FEATURE_NAME_DERIVED_FROM_PATH` is present;
- source path/size/digest/revision remain bound;
- unrecognized stories/requirements/success criteria are not fabricated.

### A3 — Fail closed without explicit identity

A bare top-level `spec.md` without a canonical heading fails deterministically rather than deriving a name from arbitrary prose or the filename itself.

### A4 — Existing safety boundary unchanged

All existing unsafe-path, duplicate-role, unknown-artifact, size-limit, symlink, UTF-8, duplicate identifier, and unresolved canonical placeholder failures continue to pass.

### A5 — Read-only and no ontology promotion

The CLI/API remain read-only, legacy tasks are never promoted, constitutions are not adopted, and no preset/hook/extension execution exists.

### A6 — Exact verification

Focused Spec Kit tests, full regression, Ruff, compile, tracked-tree cleanliness, CLI smoke, package build/reinstall smoke, exact diff review, and the permanent five-cell CI matrix pass on the exact implementation head.

## In scope

- bounded parser identity fallback in `src/specgrain/speckit.py`;
- focused tests in `tests/test_speckit.py`;
- migration documentation clarifying standard-template and template-light preset behavior;
- Specification 023 governance/evidence documents;
- canonical CURRENT/master-plan/roadmap status reconciliation.

## Out of scope

- parsing arbitrary Markdown into inferred SpecGrain semantics;
- modifying the SpecGrain core ontology or SpecNode schema;
- importing Spec Kit extensions, presets, hooks, bundles, workflow definitions, agents, or command implementations;
- executing Spec Kit commands;
- installing Spec Kit or adding it as a dependency;
- direct SpecNode creation from imported artifacts;
- automatic constitution adoption;
- promoting Spec Kit tasks to core work units;
- READY, execution, verification, or evidence-mutation authority;
- provider/agent orchestration;
- multi-writer locking changes;
- package version, tag, GitHub Release, or historical `v0.3.0` mutation;
- broad compatibility claims beyond explicitly tested bounded source forms.

## Architecture decision

ADR-0020 governs the path-bound fallback identity:

`docs/adr/0020-path-bound-template-light-speckit-import.md`

## Risks

### R1 — Over-accepting arbitrary Markdown

Mitigation: fallback supplies identity only. Structured semantics continue to require existing deterministic parsers; unmatched content remains explicitly partially mapped.

### R2 — Silent compatibility drift for existing reports

Mitigation: preserve `SPECKIT_IMPORT_VERSION == 1` and add a regression assertion for the exact pre-023 full-template report/digest.

### R3 — Path-derived identity ambiguity

Mitigation: require a concrete normalized parent component and emit an explicit notice; fail for bare top-level `spec.md`.

### R4 — Architectural coupling to upstream Spec Kit

Mitigation: no upstream runtime dependency or command/preset import. The compatibility surface remains artifact-level and source-bound.

## Constitution check

No constitution exception is required.

- Recursive ontology is unchanged.
- Deterministic control remains authoritative.
- No probabilistic parser is introduced.
- Vendor/agent neutrality is preserved.
- Brownfield/read-only source safety remains intact.
- External provenance is recorded by exact upstream revision and artifact identities.
