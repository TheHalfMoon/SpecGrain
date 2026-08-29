# Tasks 017 — Native DRAFT CLI

## Shaping

- [x] T001 Re-read canonical post-v0.1 `main`, repository instructions, constitution, execution master plan, roadmap, README, package metadata, source tree, release state, Actions, PRs, issues, and public adoption signals.
- [x] T002 Record the post-v0.1 product audit and compare plausible next frontiers without treating deferred roadmap ideas as authorized.
- [x] T003 Select native root DRAFT authoring as the smallest evidence-backed adoption gap.
- [x] T004 Define 017 outcome, exclusions, acceptance gates, risks/recovery, and expected change surface.

## Deterministic authoring primitive

- [x] T005 Add a public store-v1 root DRAFT creation primitive with deterministic lowest-unused positive ID allocation.
- [x] T006 Guarantee create-if-absent persistence, strict validation, and no overwrite of existing SpecNodes.

## CLI and documentation

- [x] T007 Add `specgrain draft` text and deterministic JSON output with fail-closed error handling.
- [x] T008 Update README, CLI architecture documentation, and Unreleased changelog truthfully.

## Verification

- [x] T009 Add API coverage for creation, allocation, invalid inputs, collisions, and non-overwrite behavior.
- [x] T010 Add CLI coverage for text/JSON output, exit behavior, compatibility, and internal-error redaction.
- [x] T011 Run exact regression, Ruff, compileall, CLI help parity, package build/install, and documentation guards through repository CI.
- [x] T012 Review the exact implementation diff for scope, lifecycle authority, store safety, dependency creep, unsupported claims, and hidden execution.

## Product PR and canonical closeout

- [x] T013 Open the bounded implementation PR from the exact shaped canonical base.
- [x] T014 Resolve every material exact-head review defect and re-prove CI after head movement.
- [x] T015 Merge only with expected-head evidence and prove the exact product merge on canonical `main`.
- [x] T016 Record post-merge CI and exact merge evidence, close 017 canonically, and re-audit the next product frontier before authorizing another specification.

Pre-merge verification/review evidence is recorded in `verification.md` and `review.md`. Final exact product PR head `1255a9187f85591edd041a3125359e70d2eea379` completed CI run `33235889444` successfully and merged through PR #21 as `dedb9ee30a6b8856c9c06439c68f3a37225f0563` with expected-head protection. Canonical post-merge CI run `33236142514` then completed all five permanent matrix jobs successfully.

T015 and T016 are recorded as completed work in this documentation-only closeout tree. They become canonical completion facts only if the exact closeout PR head containing this file is merged with expected-head protection and live GitHub post-closeout evidence confirms canonical `main`.
