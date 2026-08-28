# Review 013 — Spec Kit Import

## Reviewed head

Exact product commit reviewed: `49817d5c99adb131125f8e3fc4f605cc6e42c0e3`.

The implementation comparison from planning commit `6276ae9604e602bbf8d7d0c71dfb1a3bca406e15` is one commit ahead and changes exactly:

- `src/specgrain/speckit.py`;
- `src/specgrain/cli.py`;
- `src/specgrain/__init__.py`;
- `tests/test_speckit.py`;
- `tests/test_speckit_cli.py`.

No implementation path outside the planned change surface changed.

## Findings

No material repository-review defect remains in the exact product diff.

The importer deliberately produces a conversion report rather than a SpecNode or local-store mutation. Mapping is structural and conservative: independently testable stories, FR/SC identifiers, assumptions, Technical Context, Constitution Check text, source digests, and legacy task records are preserved where deterministic anchors exist. Unsupported or partially represented source meaning remains source-bound and is surfaced through notices for explicit migration review.

Legacy Spec Kit tasks do not become SpecGrain core ontology. Constitution content does not become repository policy. No command execution or network access occurs inside the importer.

## Residual boundaries

- free-form Spec Kit prose outside recognized structural anchors requires human migration review;
- the importer supports the bounded v1 artifact names documented in the specification and does not claim compatibility with arbitrary forks or custom templates;
- migration reports are descriptive and provenance-bound; downstream adoption into canonical SpecGrain state remains an explicit separate action;
- external automated review is not treated as PASS when bots skip or are unavailable.
