# Tasks 005 — CLI and Local Store

## Planning

- [x] T001 Re-read canonical `main` at `2a719a8ed2a7c22c0f65402c95361b32b230b511`, AGENTS, constitution, roadmap, and architecture; confirm 005 is next.
- [x] T002 Close Specification 004 canonical task state using PR #6 exact-head/merge evidence.
- [x] T003 Record ADR-0005 choosing dependency-free JSON store + stdlib CLI for M2.
- [x] T004 Define store-v1 manifest, policy, spec-file, strict-JSON, and symlink contracts.
- [x] T005 Define `readiness_mode=report|enforce`, check semantics, CLI commands, and exit codes.

## Implementation

- [ ] T006 Add store constants, enums, immutable manifest/policy/project/check models, and stable errors.
- [ ] T007 Implement strict JSON parsing/serialization and safe name/path validation.
- [ ] T008 Implement atomic `init_project` with staging cleanup and no overwrite.
- [ ] T009 Implement `load_project` with symlink rejection, manifest/policy validation, deterministic spec loading, and filename/ID binding.
- [ ] T010 Implement `check_project` refinement validation plus report/enforce readiness behavior.
- [ ] T011 Implement argparse CLI text/JSON rendering and 0/1/2 exit semantics.
- [ ] T012 Add `python -m specgrain` and console-script entry points without new runtime dependencies.
- [ ] T013 Export the bounded 005 public store API.

## Verification

- [ ] T014 Add initialization/store/parser/version/name/symlink/spec-loading tests.
- [ ] T015 Add structural check and readiness report/enforce tests.
- [ ] T016 Add CLI init/check/text/JSON/exit-code tests.
- [ ] T017 Run all 001–005 tests, compileall, and available lint/static checks with exact evidence.
- [ ] T018 Review exact diff for 006+ DAG, repository-scan, lifecycle-mutation, evidence-store, YAML, subprocess, provider, or dependency creep.

## PR closeout

- [ ] T019 Open bounded implementation PR with exact-head evidence.
- [ ] T020 Resolve every exact-head external/repository review defect.
- [ ] T021 Merge only with expected-head evidence, re-read canonical `main`, then begin `006-dependency-graph`.
