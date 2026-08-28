# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `85d1bef8ee5c1c8e8d78baa52f509803a78a43d8`  
**Closed specification:** `specs/006-dependency-graph/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/007-repository-scan/`  
**Active branch:** `feat/007-repository-scan`  
**Active status:** `PR_READY`

## Canonical continuation references

Read `docs/execution-master-plan.md` after the constitution. It contains the durable 007→016 execution sequence, cross-spec gates, donor/benchmark references, and fresh-session continuation protocol. `docs/roadmap.md` remains the milestone-level sequencing reference.

Live GitHub truth always overrides this state file if the branch, PRs, checks, or canonical `main` move.

## Current objective

Open, review, and canonically close the first deterministic brownfield repository map without executing repository code, following symlinks, requiring `.specgrain/`, or using an LLM. Then re-read canonical `main` and begin `008-context-budget`.

## 007 boundary

Repository Scan v1 owns:

- bounded lexical filesystem traversal;
- generated/vendor/control-directory skipping;
- manifest/config/test/language/component signals;
- bounded declared dependency/reuse signals from selected manifests;
- safe ordinary/indirect/absent Git metadata facts;
- deterministic normalized map digest;
- standalone `specgrain scan` text/JSON output.

It does not perform AST/semantic indexing, embeddings, arbitrary content indexing, package resolution, context selection, lifecycle mutation, dependency scheduling changes, evidence verification, or subprocess execution.

## Exact verified 007 product state

The exact reviewed product commit is:

`20d36002720fe5c7183e8e7defd02451c134516f`

Exact product/test blobs:

```text
src/specgrain/repository.py      20d6068a53965c776b7eddd359fbdeb9960b15c8
src/specgrain/cli.py             93614f13c01cc70cfb55c0dd2e9e1dda463c09cb
src/specgrain/__init__.py        2bcff16c1db87a564a96f45054d233f4646f0b10
tests/test_repository.py         4ce1600e1d1fe126f5e4e04a9639fbef649bc8a9
tests/test_repository_cli.py     5f6922be235b2c746a6e6ce813d5a7d5c2b4b95b
```

Verification for those exact uploaded bytes:

- 304 pytest tests PASS;
- `python -m compileall -q src tests` PASS;
- editable install PASS;
- `specgrain --help` and `python -m specgrain --help` parity PASS;
- 0 changed source/test lines over 100 characters;
- Ruff NOT RUN because unavailable in the execution environment.

The exact implementation review also repaired the selected-manifest/Git metadata bounded-read race before this PR-ready state. The net implementation diff from planning head `b720b321510204eb463602e418dbef7fc65a077d` contains only the five planned implementation/test files.

## Review records

Repository-local verification and exact-diff review are recorded in:

- `specs/007-repository-scan/verification.md`;
- `specs/007-repository-scan/review.md`.

The review-record commit before this state update is `8c0005ac274f726bcfb503e29a97bce0be8f4c1e`. This `CURRENT.md` update moves the branch head again; therefore every PR check/review and merge guard MUST bind to the live exact PR head, not to the product or review-record commit above.

## Immediate ordering

1. Re-read live branch head and confirm no competing 007 PR exists.
2. Open the bounded 007 implementation PR against canonical `main` using the live exact head.
3. Re-read the PR diff, exact head, checks, reviews, and inline threads.
4. Resolve every material exact-head defect using forward-only commits and repeat verification as needed.
5. Merge only with `expected_head_sha` bound to the final reviewed PR head.
6. Re-read canonical `main` after merge and prove the merge landed.
7. On the next canonical planning branch, close T017–T019 from exact PR/merge evidence and mark 007 `CLOSED_CANONICAL`.
8. Begin `008-context-budget` immediately and continue through 009–016 according to `docs/execution-master-plan.md` and `docs/roadmap.md` unless live repository evidence changes the sequence.
