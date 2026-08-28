# Tasks 005 — CLI and Local Store

## Planning

- [x] T001 Re-read canonical `main` at `2a719a8ed2a7c22c0f65402c95361b32b230b511`, AGENTS, constitution, roadmap, and architecture; confirm 005 is next.
- [x] T002 Close Specification 004 canonical task state using PR #6 exact-head/merge evidence.
- [x] T003 Record ADR-0005 choosing dependency-free JSON store + stdlib CLI for M2.
- [x] T004 Define store-v1 manifest, policy, spec-file, strict-JSON, and symlink contracts.
- [x] T005 Define `readiness_mode=report|enforce`, check semantics, CLI commands, and exit codes.

## Implementation

- [x] T006 Add store constants, enums, immutable manifest/policy/project/check models, and stable errors.
- [x] T007 Implement strict JSON parsing/serialization and safe name/path validation.
- [x] T008 Implement atomic `init_project` with staging cleanup and no overwrite.
- [x] T009 Implement `load_project` with symlink rejection, manifest/policy validation, deterministic spec loading, and filename/ID binding.
- [x] T010 Implement `check_project` refinement validation plus report/enforce readiness behavior.
- [x] T011 Implement argparse CLI text/JSON rendering and 0/1/2 exit semantics.
- [x] T012 Add `python -m specgrain` and console-script entry points without new runtime dependencies.
- [x] T013 Export the bounded 005 public store API.

## Verification

- [x] T014 Add initialization/store/parser/version/name/symlink/spec-loading tests.
- [x] T015 Add structural check and readiness report/enforce tests.
- [x] T016 Add CLI init/check/text/JSON/exit-code tests.
- [x] T017 Run all 001–005 tests and compile/package/smoke checks after boundary hardening: 236 pytest tests PASS, compileall PASS, editable install PASS, console/module smoke PASS; Ruff NOT RUN because unavailable and installation is blocked by offline DNS/network.
- [x] T018 Review exact implementation head `e454112e265fe0e145a5971b4db372b3b2df3572`; no material scope/trust-boundary defect remains. Record accepted non-blocking concurrency boundary R-001 in `review.md`.

## PR closeout

- [x] T019 Open bounded PR #7; final exact head `ced3084cdfd4c8eda6b206592ab0435fc7b04868`.
- [x] T020 Exact head had CodeRabbit SUCCESS, no unresolved review threads, mergeable state, and internal exact-head COMMENT review; no material defect remained.
- [x] T021 Merge PR #7 with expected-head guard; canonical merge commit is `ccd4a825c2a951a8000a2833ede05cdb3218d477`, then re-read canonical `main` before beginning 006.

**Result:** `CLOSED_CANONICAL` at merge commit `ccd4a825c2a951a8000a2833ede05cdb3218d477`.
