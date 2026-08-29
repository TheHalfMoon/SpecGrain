# Migrating from GitHub Spec Kit

SpecGrain is not a fork of GitHub Spec Kit. v0.1.0 provides an explicit, read-only importer for reviewing supported Spec Kit feature artifacts before any SpecGrain-native modeling decision is made.

## Supported source boundary

`specgrain import-spec-kit` accepts:

- one feature directory containing required `spec.md`;
- optional `plan.md` and `tasks.md` in that feature directory;
- an optional constitution only when its path is supplied explicitly;
- a caller-supplied source revision that binds the report to the repository state being inspected.

The importer reads only known ordinary UTF-8 artifacts under bounded size limits. It rejects unsafe or ambiguous inputs such as symlinks, oversized files, malformed paths, duplicate identifiers, and unresolved critical placeholders.

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

Where present and supported, the report preserves feature identity/status, independently testable user stories and priorities, functional requirements, measurable success criteria, assumptions, Technical Context, Constitution Check text, and legacy task records. Every loaded source artifact is bound by role, repository-relative path, byte size, SHA-256 digest, and the supplied source revision.

## What it deliberately does not do

- It does not write `.specgrain/` state.
- It does not modify the Spec Kit source directory.
- It does not run Spec Kit commands or repository commands.
- It does not automatically create SpecNodes.
- It does not automatically adopt a source constitution.
- It does not infer missing requirements.
- It does not promote `tasks.md` into SpecGrain's core ontology.

Legacy tasks remain migration evidence. The report's `tasks_promoted_to_core` value is always false in v1. Review the conversion report, then model recursive SpecNodes according to the destination repository's own governance.

## Why the boundary is explicit

Spec Kit and SpecGrain use different planning models. SpecGrain's core primitive is a recursively refinable specification whose executable leaves must satisfy deterministic Grain readiness. Preserving source material without silently treating flat tasks as canonical avoids migration data loss and avoids importing an incompatible ontology by accident.

See `specs/013-spec-kit-import/` for the exact importer contract and evidence.
