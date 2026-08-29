# Migrating from GitHub Spec Kit

SpecGrain is not a fork of GitHub Spec Kit. v0.1.0 introduced an explicit, read-only importer for reviewing supported Spec Kit feature artifacts before any SpecGrain-native modeling decision is made. Current source preserves that boundary while also accepting bounded template-light feature specifications from official preset workflows when a concrete feature-directory identity is available.

## Supported source boundary

`specgrain import-spec-kit` accepts:

- one feature directory containing required `spec.md`;
- optional `plan.md` and `tasks.md` in that feature directory;
- an optional constitution only when its path is supplied explicitly;
- a caller-supplied source revision that binds the report to the repository state being inspected.

The importer reads only known ordinary UTF-8 artifacts under bounded size limits. It rejects unsafe or ambiguous inputs such as symlinks, oversized files, malformed paths, duplicate identifiers, and unresolved critical placeholders.

## Standard-template and template-light behavior

For canonical full-template Spec Kit artifacts, SpecGrain continues to extract feature identity from:

```text
# Feature Specification: <name>
```

and deterministically maps the recognized user-story, requirement, measurable-outcome, assumption, Technical Context, Constitution Check, and legacy-task structures.

Current GitHub Spec Kit also ships official preset workflows such as Lean that intentionally produce focused Markdown without requiring the full template boilerplate. For a template-light `spec.md`, current SpecGrain source may establish only the migration-report feature identity from the concrete final component of the explicitly selected feature directory or normalized repository-relative `spec.md` path.

When that fallback is used, the report includes:

```text
FEATURE_NAME_DERIVED_FROM_PATH
```

This notice is not a claim that arbitrary Markdown was semantically understood. Structured fields are still populated only when they match the existing deterministic recognized forms. Unrecognized stories, requirements, success criteria, plan content, or other prose remain unmapped and source-digest-bound for explicit review.

A bare top-level template-light `spec.md` without the canonical feature heading is rejected because it provides no concrete path-bound feature identity. Placeholder-like feature-directory names are rejected as unresolved identity rather than guessed.

Existing canonical full-template report content remains stable; the importer report version remains `1`.

## Run the importer

First determine the source revision yourself. SpecGrain does not run Git commands on the source repository.

```bash
git -C /path/to/project rev-parse HEAD
```

Then inspect the feature:

```bash
specgrain import-spec-kit /path/to/project/specs/001-feature \
  --source-revision <git-sha> \
  --constitution /path/to/project/.specify/memory/constitution.md
```

For machine-readable output:

```bash
specgrain import-spec-kit /path/to/project/specs/001-feature \
  --source-revision <git-sha> \
  --constitution /path/to/project/.specify/memory/constitution.md \
  --json
```

## What the report preserves

Where present and supported, the report preserves feature identity/status, independently testable user stories and priorities, functional requirements, measurable success criteria, assumptions, Technical Context, Constitution Check text, and legacy task records. Every loaded source artifact is bound by role, source path, byte size, SHA-256 digest, and the supplied source revision.

Template-light compatibility does not weaken this rule: content that is not deterministically mapped remains represented by its source artifact identity/digest rather than being inferred.

## What it deliberately does not do

- It does not write `.specgrain/` state.
- It does not modify the Spec Kit source directory.
- It does not run Spec Kit commands or repository commands.
- It does not install or execute Spec Kit presets, hooks, extensions, bundles, or workflows.
- It does not automatically create SpecNodes.
- It does not automatically adopt a source constitution.
- It does not infer missing requirements or other structured semantics from arbitrary prose.
- It does not promote `tasks.md` into SpecGrain's core ontology.
- It does not add a runtime dependency on GitHub Spec Kit.

Legacy tasks remain migration evidence. The report's `tasks_promoted_to_core` value is always false in import version 1. Review the conversion report, then model recursive SpecNodes according to the destination repository's own governance.

## Why the boundary is explicit

Spec Kit and SpecGrain use different planning models. SpecGrain's core primitive is a recursively refinable specification whose executable leaves must satisfy deterministic Grain readiness. Preserving source material without silently treating flat tasks as canonical avoids migration data loss and avoids importing an incompatible ontology by accident.

Template-light compatibility follows the same rule: explicit source identity may be recovered from the selected feature path, but missing semantics are not invented.

See `specs/013-spec-kit-import/` for the original importer contract and `specs/023-spec-kit-preset-compatible-import/` for the bounded preset-compatibility authority.
