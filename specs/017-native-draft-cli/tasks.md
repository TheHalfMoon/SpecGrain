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
- [ ] T011 Run exact regression, Ruff, compileall, CLI help parity, package build/install, and documentation guards through repository CI.
- [ ] T012 Review the exact implementation diff for scope, lifecycle authority, store safety, dependency creep, unsupported claims, and hidden execution.

## Product PR and canonical closeout

- [ ] T013 Open the bounded implementation PR from the exact shaped canonical base.
- [ ] T014 Resolve every material exact-head review defect and re-prove CI after head movement.
- [ ] T015 Merge only with expected-head evidence and prove the exact product merge on canonical `main`.
- [ ] T016 Record post-merge CI and exact merge evidence, close 017 canonically, and re-audit the next product frontier before authorizing another specification.

Checked implementation tasks on the feature branch are implementation evidence only. T011 onward require exact live GitHub evidence before they may be checked or treated as canonical completion.
