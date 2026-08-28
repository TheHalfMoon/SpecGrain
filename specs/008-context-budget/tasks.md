# Tasks 008 — Context Budget

## Planning

- [x] T001 Re-read canonical `main` at `197ddfb68d94bf8998d68d1371c26431f3816ca0`, AGENTS, constitution, execution master plan, roadmap, architecture, and 007 contracts; confirm 008 is next.
- [x] T002 Close Specification 007 canonical task state from PR #9 exact-head/post-merge evidence.
- [x] T003 Record ADR-0008 explicit revision-bound context-cost accounting and required-context non-omission.
- [x] T004 Define context-source, policy, budget report, digest, and repository-map bridge contracts.

## Implementation

- [x] T005 Add context requirement/source/policy records and validation errors.
- [x] T006 Add deterministic source-collection validation and canonical ordering.
- [x] T007 Implement required-context token/byte/source-count blocker accounting.
- [x] T008 Implement deterministic optional packing by `(priority, source_id)`.
- [x] T009 Implement normalized context-plan digest and exact budget error behavior.
- [x] T010 Add repository-map context-source bridge without content retrieval.
- [x] T011 Add bounded public exports without CLI/store/lifecycle changes.

## Verification

- [x] T012 Add model/policy/collection validation tests.
- [x] T013 Add required-overflow/optional-packing/permutation/digest tests.
- [x] T014 Add repository-map bridge/no-content-read/no-mutation tests.
- [x] T015 Run all 001–008 tests plus compile/package/entry-point and available lint/static checks.
- [x] T016 Review exact uploaded diff for retrieval/tokenizer/LLM, WorkPacket/evidence, lifecycle/store/scheduler, subprocess, or dependency creep.

## PR closeout

- [x] T017 Open bounded implementation PR #10 with exact-head evidence at `36d9a2f551088f5c38b42d7959c8521c1cf3b0de`.
- [x] T018 Resolve material exact-head external/repository review defects; CodeRabbit reported no actionable comments, its docstring-coverage warning was assessed non-material to the repository contract, and Qodo was unavailable due expired trial.
- [x] T019 Merge with expected head `36d9a2f551088f5c38b42d7959c8521c1cf3b0de`; canonical merge commit `e1336acc3f764241d79d5051f34309ae2f66d6e4` has the reviewed head as second parent.