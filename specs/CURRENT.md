# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Active specification:** `specs/000-foundation/`  
**Active status:** `FOUNDATION_PLANNING`  
**Last verified canonical main:** `4bfd6cfb5abddc94badb116671c221f9a41d5ea4`

## Current objective

Establish the canonical product thesis, constitution, domain model, architecture boundaries, methodology, donor policy, benchmark strategy, roadmap, and launch thesis before product implementation begins.

## Immediate ordering

1. Complete `000-foundation` documents.
2. Run a cross-document consistency and gap review.
3. Reconcile any foundation defects.
4. Merge foundation only after the exact PR head is reviewed.
5. Re-read canonical `main`.
6. Start `001-core-model`, the first implementation specification.

## Non-authorized shortcuts

Until the foundation spec closes, do not:

- build a web dashboard;
- add SaaS infrastructure;
- implement vendor-specific agent orchestration in the core;
- import large bodies of Spec Kit or other donor code;
- create a large detailed backlog for distant milestones;
- claim benchmark superiority without reproducible evidence.

## Canonical next spec after foundation

`001-core-model` — define and implement the deterministic recursive SpecNode model, Grain readiness contract, state machine, dependency primitives, and serialization boundary.
