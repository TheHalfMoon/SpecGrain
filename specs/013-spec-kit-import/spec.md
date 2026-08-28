# Specification 013 — Spec Kit Import

## Outcome

Provide a read-only, explicit, deterministic migration path from relevant GitHub Spec Kit feature artifacts into a reviewable SpecGrain conversion report without silently changing SpecGrain ontology or repository state.

## Required behavior

1. Accept one explicit Spec Kit feature directory containing `spec.md` and optional `plan.md`/`tasks.md`; accept a constitution only through an explicit path.
2. Read only known ordinary UTF-8 files under a hard byte limit; reject symlinks, oversized content, ambiguous roles, malformed paths, duplicate identifiers, and unresolved critical placeholders.
3. Bind each source artifact by role, repository-relative source path, byte size, SHA-256 digest, and caller-supplied source revision.
4. Preserve useful migration information:
   - feature name/branch/status;
   - independently testable user stories and priorities;
   - functional requirements and measurable success criteria;
   - assumptions;
   - Technical Context, including dependency/tooling fields when present;
   - Constitution Check text;
   - legacy tasks as evidence only.
5. Never promote Spec Kit `tasks.md` into the SpecGrain core ontology.
6. Emit explicit notices for legacy tasks, constitution governance, and source sections that are only partially mapped.
7. Provide deterministic JSON/text CLI output through `specgrain import-spec-kit` without writing `.specgrain` or source artifacts.
8. Add no runtime dependency and execute no repository command.

## Non-goals

- automatic SpecNode creation;
- automatic constitution adoption;
- semantic inference for missing requirements;
- execution of Spec Kit commands;
- importing arbitrary research/contracts/data-model files in v1;
- compatibility claims beyond the source formats explicitly parsed and source-bound.

## Acceptance

- identical source bytes/revision produce identical reports/digests independent of mapping order;
- migration refuses unsafe/ambiguous inputs;
- legacy tasks are visibly preserved but `tasks_promoted_to_core` is always false;
- CLI operation is demonstrably read-only;
- full 001–013 regression passes on exact uploaded bytes.
