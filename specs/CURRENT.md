# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Active specification:** `specs/000-foundation/`  
**Active status:** `FOUNDATION_REVIEWED_PR_PENDING`  
**Last verified canonical main:** `4bfd6cfb5abddc94badb116671c221f9a41d5ea4`

## Current objective

Close the foundation specification through an exact-head pull-request review, merge it, then begin the first deliberately small implementation spec.

## Immediate ordering

1. Confirm the remediation commit contains the documented review fixes.
2. Open the bounded `000-foundation` pull request.
3. Review exact PR head and repository diff.
4. Merge only if no material foundation contradiction remains.
5. Re-read canonical `main` after merge.
6. Start `001-specnode-schema`.

## Bootstrap boundary

This repository currently uses a Spec Kit-style `.specify/` + `specs/` planning layout to build SpecGrain. This is development scaffolding only. The product runtime is planned around `.specgrain/` and MUST NOT depend on Spec Kit being installed. See `docs/adr/0003-bootstrap-spec-kit-layout.md`.

## Non-authorized shortcuts

Until the foundation spec closes, do not:

- build a web dashboard;
- add SaaS infrastructure;
- implement vendor-specific agent orchestration in the core;
- import large bodies of Spec Kit or other donor code;
- create a large detailed backlog for distant milestones;
- claim benchmark superiority without reproducible evidence.

## Canonical next spec after foundation

`001-specnode-schema` — define and implement only the deterministic recursive SpecNode schema, stable IDs, normalized serialization, and revision digest. Lifecycle transitions, refinement-tree rules, and Grain readiness are intentionally separate later specs.
