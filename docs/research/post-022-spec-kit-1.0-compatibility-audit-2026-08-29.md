# Post-022 GitHub Spec Kit 1.0 Compatibility Audit — 2026-08-29

## Purpose

This audit is evidence collection at the `POST_022_OBSERVATION` frontier. It compares the exact current SpecGrain import boundary with exact current GitHub Spec Kit artifacts to determine whether a bounded successor specification is justified.

This document is evidence, not product authority. GitHub Spec Kit remains an upstream influence and compatibility target, not repository authority, and no external reviewer can expand SpecGrain scope without a shaped specification.

## Exact revisions reviewed

### SpecGrain

- repository: `TheHalfMoon/SpecGrain`
- canonical `main`: `ff9f640bf0e4de5bdd5bf2af0e11b98d86f6587b`
- program state: `POST_022_OBSERVATION`
- active specification before this audit: none
- current Spec Kit importer: `src/specgrain/speckit.py`
- importer blob: `fe68ca91d9bca3b649a80bf7fc4d2942db6a18a0`
- importer tests: `tests/test_speckit.py`
- test blob: `f0664f8d42b86d48a2938f15b64e91418772e90b`
- governing migration ADR: `docs/adr/0013-bounded-spec-kit-migration.md`

### GitHub Spec Kit

- repository: `github/spec-kit`
- reviewed `main`: `51e52be6c3b26fed3ff5424c671f4a559519a759`
- latest published release observed: `v1.0.1`, release ID `374643230`
- standard spec template: `templates/spec-template.md`
- standard spec-template blob: `ceb28776215a098e977650ac090c785dcbf53651`
- bundled Lean preset README: `presets/lean/README.md`
- Lean README blob: `ab17257f96091590d2289699aaf2b114cc05bbbe`
- Lean specify command: `presets/lean/commands/speckit.specify.md`
- Lean specify blob: `c15353557aa941b18e811c15aef605c41ff64133`
- Lean plan command: `presets/lean/commands/speckit.plan.md`
- Lean plan blob: `9fbbe4c3713203a363169b9ca4d7f0dedbd0d1e0`
- Lean tasks command: `presets/lean/commands/speckit.tasks.md`
- Lean tasks blob: `724a7b840074b8e34cf107f2ca37d211745d15be`

No upstream code is copied by this audit or by the proposed compatibility change. The comparison concerns artifact contracts only.

## Current SpecGrain contract

Specification 013 intentionally built a deterministic, read-only, source-bound migration report. The current importer still preserves the important trust boundary:

- only known ordinary UTF-8 artifacts are accepted;
- paths must be normalized and repository-relative;
- source paths, sizes, SHA-256 digests, and caller-supplied source revision are bound into the report;
- legacy tasks remain migration evidence and are never promoted to the SpecGrain core ontology;
- constitution bytes are source-bound but not adopted as SpecGrain policy;
- no source repository command is executed;
- no `.specgrain` state is mutated;
- partially mapped source content is surfaced through explicit notices.

Those properties remain desirable and are not the observed problem.

## Reproduced compatibility finding

The current `_feature()` parser accepts a feature identity only when `spec.md` contains the exact canonical heading form:

```text
# Feature Specification: <name>
```

If that heading is absent, the importer raises:

```text
spec.md is missing '# Feature Specification:' heading
```

The existing test fixture mirrors the full standard Spec Kit template, so the test suite proves compatibility with that template family.

Current upstream Spec Kit, however, ships the Lean preset as a bundled preset. Its own README describes Lean as the normal `specify -> plan -> tasks -> implement` pipeline "without the ceremony of the full templates" and states that its commands produce focused Markdown files with no boilerplate sections. The bundled `speckit.specify` command requires a `spec.md` containing overview, functional requirements, user scenarios, and success criteria, but it does not require the standard `# Feature Specification:` heading or the full standard template structure.

Therefore a valid feature artifact produced under an official bundled Spec Kit preset can be rejected by SpecGrain solely because it is template-light rather than because it is unsafe, ambiguous in source identity, oversized, malformed, or semantically invalid under an explicitly supported extraction rule.

This is a real compatibility gap in the bounded Spec Kit migration surface.

## Why broad parsing is not justified

The finding does not justify treating arbitrary Markdown as fully understood Spec Kit semantics.

SpecGrain should not:

- infer feature identity from arbitrary prose;
- use an LLM or heuristic title classifier in the deterministic importer;
- reinterpret unrecognized prose as user stories, functional requirements, success criteria, or tasks;
- import Spec Kit presets, hooks, extensions, bundles, workflows, or runtime code;
- execute upstream commands;
- adopt upstream constitutions or governance;
- change the SpecGrain recursive ontology;
- add a runtime dependency on Spec Kit.

The smallest safe repair is identity compatibility, not semantic generalization.

## Bounded candidate repair

When the canonical full-template feature heading exists, preserve current behavior exactly.

When that heading does not exist:

1. use only the already-normalized explicit repository-relative `spec.md` source path;
2. if `spec.md` has a concrete parent directory, use the final parent path component verbatim as the migration-report feature identity;
3. emit an explicit notice that feature identity was derived from the source path rather than parsed from canonical full-template content;
4. leave structured fields empty when their existing deterministic parsers do not match, while preserving the existing partial-mapping notices;
5. fail closed when there is no concrete parent identity, for example a bare top-level `spec.md` without the canonical heading.

This fallback is deterministic, inspectable, source-bound, and does not invent semantics.

## Compatibility requirement

For existing canonical full-template artifacts, the migration report must remain unchanged, including:

- `SPECKIT_IMPORT_VERSION == 1`;
- serialized report content;
- deterministic report digest.

A version bump would unnecessarily invalidate report digests for already-supported artifacts even though the report schema and their interpretation do not change.

## Selected frontier

The evidence selects a bounded successor candidate:

**Specification 023 — Spec Kit Preset-Compatible Import**

Outcome: accept bounded template-light feature artifacts from official Spec Kit preset workflows, notably Lean, into the existing deterministic read-only migration report without weakening source safety or inventing missing semantics.

The finding does not select READY mutation, WorkPacket execution, executor/provider orchestration, verification execution, evidence mutation, stronger local-store locking, a new release, or a general Spec Kit synchronization layer.

## External architecture review boundary

This audit is suitable input for an independent architectural review, including a Fable review outside repository authority. Any such review is additional evidence only. A reviewer may identify defects or alternatives, but implementation authority remains the canonical Specification 023 chain and live repository truth.
