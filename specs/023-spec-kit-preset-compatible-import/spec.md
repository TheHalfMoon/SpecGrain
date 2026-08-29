# Specification 023 — Spec Kit Preset-Compatible Import

## Status

`CLOSEOUT_CANDIDATE`

Canonical shaping and product implementation are complete. Specification 023 becomes `CLOSED_CANONICAL` only after documentation-only closeout and final evidence reconciliation are merged and canonical post-closeout CI is proven.

## Outcome

Allow the existing deterministic read-only `import-spec-kit` boundary to accept bounded template-light GitHub Spec Kit feature artifacts from official preset workflows, notably the bundled Lean preset, without requiring the full canonical Spec Kit Markdown template and without inventing missing semantics.

## Evidence

Post-022 compatibility audit:

`docs/research/post-022-spec-kit-1.0-compatibility-audit-2026-08-29.md`

Exact comparison revisions:

- pre-023 SpecGrain canonical base: `ff9f640bf0e4de5bdd5bf2af0e11b98d86f6587b`;
- canonical shaped base: `99d8ee5bc7ce49c00ae542f3c06f564d05641a70`;
- GitHub Spec Kit reviewed `main`: `51e52be6c3b26fed3ff5424c671f4a559519a759`;
- latest observed upstream release: `v1.0.1`;
- standard upstream spec template blob: `ceb28776215a098e977650ac090c785dcbf53651`;
- bundled Lean README blob: `ab17257f96091590d2289699aaf2b114cc05bbbe`;
- bundled Lean `speckit.specify` blob: `c15353557aa941b18e811c15aef605c41ff64133`.

The reproduced gap was structural: pre-023 SpecGrain required the exact canonical `# Feature Specification:` heading, while the bundled Lean preset intentionally produces focused Markdown without requiring full-template boilerplate.

## Delivered behavior

1. Preserve the canonical full-template import path exactly when `# Feature Specification: <name>` is present.
2. When that canonical heading is absent, derive feature identity only from a concrete explicit feature-path parent.
3. Reject fallback identity for a bare top-level `spec.md`, absent identity, or unresolved placeholder-like parent.
4. Emit `FEATURE_NAME_DERIVED_FROM_PATH` whenever path-bound fallback identity is used.
5. Continue to parse stories, FR/SC items, assumptions, Technical Context, Constitution Check, and legacy tasks only through existing deterministic recognized structures.
6. Do not infer unrecognized structured semantics from arbitrary prose; unmatched source remains source-digest-bound and explicitly partially mapped.
7. Preserve normalized source paths, known-role-only input, ordinary UTF-8 file checks, byte limits, duplicate-role rejection, source revision binding, and SHA-256 artifact binding.
8. Preserve legacy tasks as evidence only; `tasks_promoted_to_core` remains false.
9. Preserve read-only behavior: no `.specgrain` writes, source mutation, repository command execution, preset installation, hook execution, or upstream code execution.
10. Keep `SPECKIT_IMPORT_VERSION == 1`.
11. Preserve exact serialized report content and digest for already-supported canonical full-template fixtures.
12. Add no runtime dependency.

## Acceptance proof

### A1 — Existing canonical format stability

The canonical pre-023 full-template report digest remains:

`sha256:678fcc87985902002a9d2bc852196fbffdc59b332740660f1deeaf0d4f58746a`

and `SPECKIT_IMPORT_VERSION == 1`.

### A2 — Template-light bounded acceptance

A template-light `spec.md` under a concrete feature path such as `specs/search-workspace/spec.md` imports with `feature_name == "search-workspace"`, emits `FEATURE_NAME_DERIVED_FROM_PATH`, and does not fabricate unrecognized structured semantics.

### A3 — Fail closed without explicit identity

A bare top-level template-light `spec.md` and placeholder-like parent identity fail deterministically.

### A4 — Existing safety boundary unchanged

All existing unsafe-path, duplicate-role, unknown-artifact, size-limit, symlink, UTF-8, duplicate-identifier, and unresolved canonical placeholder checks remain green.

### A5 — Read-only and no ontology promotion

The importer remains read-only; legacy tasks are never promoted, constitutions are not adopted, and no preset/hook/extension runtime execution exists.

### A6 — Exact verification

Final implementation head `83fcc6add4e982df523f6c606399f08c317d3ffe` passed exact push CI `33264389193` and exact PR CI `33264479954` across the permanent five-cell matrix. PR #42 merged with expected-head protection as canonical product merge `037f137cdd6e7a0fe224bd3fa3371d6da7460f22`, whose post-product CI `33265277105` completed `success` across the same matrix.

## In scope

- bounded parser identity fallback in `src/specgrain/speckit.py`;
- focused tests in `tests/test_speckit.py`;
- migration documentation clarifying standard-template and template-light preset behavior;
- Specification 023 governance/evidence documents;
- canonical CURRENT/master-plan/roadmap status reconciliation.

## Out of scope

- arbitrary Markdown semantic inference;
- SpecNode schema or core ontology changes;
- importing or executing Spec Kit extensions, presets, hooks, bundles, workflows, agents, or commands;
- installing Spec Kit or adding it as a dependency;
- direct SpecNode creation from imported artifacts;
- automatic constitution adoption;
- promoting Spec Kit tasks into core work units;
- READY, execution, verification, or evidence-mutation authority;
- provider/agent orchestration;
- multi-writer locking changes;
- package version, tag, GitHub Release, or historical `v0.3.0` mutation;
- broad compatibility claims beyond explicitly tested bounded source forms.

## Architecture decision

ADR-0020 governs the path-bound fallback identity:

`docs/adr/0020-path-bound-template-light-speckit-import.md`

## Residual limitations

Template-light prose that does not match existing deterministic structures remains intentionally unmapped and source-digest-bound. The bounded multi-writer race retained after Specification 022 also remains unchanged and outside 023 authority.

## Constitution check

No constitution exception is required. Recursive ontology, deterministic authority, agent/vendor neutrality, brownfield safety, and open provenance remain intact.
