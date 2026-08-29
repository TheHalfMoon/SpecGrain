# ADR-0020 — Path-Bound Identity for Template-Light Spec Kit Imports

## Status

Proposed for Specification 023.

## Context

Specification 013 established an explicit, deterministic, read-only GitHub Spec Kit migration report. Its parser was shaped against the canonical full templates and currently requires the exact full-template feature heading `# Feature Specification: ...` to establish feature identity.

GitHub Spec Kit `main` at `51e52be6c3b26fed3ff5424c671f4a559519a759` ships the Lean workflow as a bundled preset. Lean intentionally replaces the full template commands with focused Markdown artifacts and does not require the canonical full-template feature heading.

The result is a compatibility gap: a source can be valid under an official bundled Spec Kit workflow while SpecGrain rejects it before producing the bounded migration report.

The deterministic importer must not solve that gap by guessing semantics from arbitrary prose.

## Decision

SpecGrain may establish feature identity for a template-light Spec Kit `spec.md` using a strict two-level rule:

1. If the existing canonical `# Feature Specification: <name>` heading is present, preserve the existing parsed identity and behavior exactly.
2. Otherwise, derive migration-report feature identity only from the final parent component of the already-normalized, repository-relative `spec.md` source path.

For the path fallback:

- a concrete parent component is required;
- the component is preserved verbatim rather than humanized or semantically interpreted;
- a placeholder-looking or absent parent identity is rejected;
- an explicit `FEATURE_NAME_DERIVED_FROM_PATH` notice is emitted;
- no additional prose is promoted into structured report fields unless it already matches an existing deterministic parser;
- unmatched content remains source-digest-bound and covered by partial-mapping notices.

A bare top-level `spec.md` without a canonical feature heading remains invalid because it provides no bounded explicit feature identity.

## Compatibility

The report schema does not change. `SPECKIT_IMPORT_VERSION` remains `1`.

For already-supported canonical full-template inputs, serialized report content and report digest must remain unchanged. The new behavior is additive only for inputs that previously failed at feature-name extraction.

## Safety boundary

This decision does not authorize:

- arbitrary Markdown semantic inference;
- LLM-assisted parsing inside the deterministic importer;
- importing or executing Spec Kit presets, hooks, extensions, bundles, or workflows;
- source repository mutation;
- automatic SpecNode creation;
- constitution adoption;
- task promotion into the SpecGrain ontology;
- a runtime dependency on GitHub Spec Kit;
- any lifecycle or execution authority.

## Consequences

SpecGrain can produce a bounded migration report for template-light official preset artifacts without coupling its architecture to upstream prompt templates. The price is deliberately incomplete semantic extraction when template-light prose does not match existing deterministic patterns; that incompleteness is explicit rather than guessed.
