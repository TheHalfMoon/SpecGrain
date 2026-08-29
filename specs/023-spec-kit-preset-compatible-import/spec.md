# Specification 023 — Spec Kit Preset-Compatible Import

## Status

`CLOSED_CANONICAL` when this final reconciliation is canonical.

Specification 023 is fully implemented, product-merged, documentation-closeout-merged, and post-closeout verified. This status text becomes canonical only after the final reconciliation itself is merged to `main`.

## Outcome

Allow the deterministic read-only `import-spec-kit` boundary to accept bounded template-light GitHub Spec Kit feature artifacts from official preset workflows, notably the bundled Lean preset, without requiring the full canonical Spec Kit Markdown template and without inventing missing semantics.

## Evidence

The selection evidence is recorded in:

`docs/research/post-022-spec-kit-1.0-compatibility-audit-2026-08-29.md`

Reviewed upstream truth included GitHub Spec Kit `main` `51e52be6c3b26fed3ff5424c671f4a559519a759`, observed release `v1.0.1`, the standard spec template, and the bundled Lean preset artifacts.

The reproduced gap was structural: pre-023 SpecGrain required the canonical `# Feature Specification:` heading, while the official Lean preset intentionally does not require full-template boilerplate.

## Delivered behavior

1. Preserve canonical full-template feature identity exactly when `# Feature Specification: <name>` exists.
2. When absent, derive feature identity only from a concrete explicit feature-path parent.
3. Reject bare top-level or placeholder-like fallback identity.
4. Emit `FEATURE_NAME_DERIVED_FROM_PATH` for every fallback.
5. Preserve existing deterministic structured parsers; do not infer unrecognized semantics from arbitrary prose.
6. Preserve normalized path, known-role, UTF-8, size, duplicate-role, source-revision, SHA-256 binding, symlink, and read-only safety.
7. Preserve legacy tasks as evidence only and constitutions as non-authoritative source material.
8. Preserve `SPECKIT_IMPORT_VERSION == 1` and the exact pre-023 canonical full-template report digest.
9. Add no runtime dependency and execute no Spec Kit preset, hook, extension, bundle, workflow, or command.

## Acceptance proof

The canonical pre-023 report digest remains:

`sha256:678fcc87985902002a9d2bc852196fbffdc59b332740660f1deeaf0d4f58746a`.

Final implementation head `83fcc6add4e982df523f6c606399f08c317d3ffe` passed push CI `33264389193` and PR CI `33264479954` across the permanent five-cell matrix. PR #42 merged with expected-head protection as product merge `037f137cdd6e7a0fe224bd3fa3371d6da7460f22`; post-product CI `33265277105` succeeded.

Documentation-only closeout head `fb23602a3aa234b88b0a223443c8c974ff8ed25a` passed push CI `33265481647` and PR CI `33265501850`. PR #43 merged with expected-head protection as closeout merge `5b3a8b906309de642a0b35dfa8e260b5fa6bedd1`; post-closeout CI `33265589133` succeeded across all five permanent cells.

Historical `v0.3.0` tag, Release `378962445`, asset identities, sizes, digests, release notes, and command surface remain unchanged.

## Architecture decision

ADR-0020 governs path-bound fallback identity:

`docs/adr/0020-path-bound-template-light-speckit-import.md`

## Explicitly out of scope

Specification 023 does not authorize arbitrary Markdown semantic inference, SpecNode schema changes, automatic SpecNode creation, task promotion, constitution adoption, Spec Kit runtime integration, READY/execution/verification/evidence mutation, provider orchestration, stronger multi-writer locking, package versioning, release publication, or broader compatibility claims beyond the tested bounded forms.

## Residual limitations

Template-light prose that does not match recognized deterministic structures remains intentionally unmapped and source-digest-bound. The bounded concurrent-writer race retained after Specification 022 remains unchanged and outside 023 authority.

## Post-023 frontier

No successor product specification is selected. After this reconciliation becomes canonical, the program returns to observation/evidence gathering until fresh reproducible evidence justifies a new bounded shaping cycle.
