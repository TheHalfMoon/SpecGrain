# ADR-0013 — Explicit bounded Spec Kit migration

## Status

Accepted for Specification 013.

## Context

Live `github/spec-kit` `main` was re-read before implementation. Current template identities used as compatibility references:

- `templates/constitution-template.md` — `a4670ff46919b276a4c9663b4ca51830108fcfc0`
- `templates/spec-template.md` — `ceb28776215a098e977650ac090c785dcbf53651`
- `templates/plan-template.md` — `36f2eab16880bac670fe43cbe7ef2b9bc8c3aa2f`
- `templates/tasks-template.md` — `7fff087cc5a3c51a889d865fd9126607a032d233`

## Decision

SpecGrain imports an explicit bounded set of Spec Kit artifacts into a deterministic **migration report**, not directly into repository authority.

The importer:

- preserves exact source path, size, SHA-256 digest, and caller-supplied source revision;
- maps independently testable user stories, FR/SC identifiers, assumptions, Technical Context, and Constitution Check material;
- preserves legacy tasks as migration evidence only and never promotes them to the SpecGrain core ontology;
- binds constitution bytes by digest but requires explicit governance review before policy adoption;
- emits notices for partially mapped source content so conversion is not silently lossy;
- reads only ordinary UTF-8 files under explicit byte limits and performs no writes or commands.

## Consequences

Migration is inspectable, portable, and fail-closed. A human or later explicit conversion step may use the report to shape SpecNodes, but Specification 013 does not silently invent missing semantics or mutate `.specgrain` state.
