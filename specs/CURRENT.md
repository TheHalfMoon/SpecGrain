# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `ccd4a825c2a951a8000a2833ede05cdb3218d477`  
**Closed specification:** `specs/005-cli-local-store/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/006-dependency-graph/`  
**Active branch:** `feat/006-dependency-graph`  
**Active status:** `PR_READY`

## Current objective

Open and close Specification 006 from the reviewed dependency kernel + local project orchestration, then re-read canonical `main` and begin `007-repository-scan`.

## Implemented dependency semantics

ADR-0006 defines:

- satisfied: `VERIFIED`, `CONTROLLED`;
- hard blockers: `BLOCKED`, `FAILED`, `STALE`, `CANCELLED`, `SUPERSEDED`;
- all other lifecycle states: waiting.

Only current `GRAIN` nodes are candidates for the ready set. Eligibility analysis never mutates `GRAIN -> READY`.

## Implemented 006 boundary

006 provides:

- duplicate/missing/self dependency validation;
- deterministic dependency cycle detection;
- direct waiting + transitive hard-blocker reporting;
- current eligible Grain computation;
- advisory dependency-only Grain wave projection;
- dependency-aware local `check` orchestration;
- read-only `next` text/JSON output.

The final implementation leaves Specification 005 `store.py` unchanged and uses a small `project.py` orchestration layer instead, reducing change surface without changing the 006 outcome.

## Verification front

- pytest: **275 passed** (236 existing + 39 new 006 tests);
- compileall: **PASS**;
- editable install: **PASS**;
- `specgrain` / `python -m specgrain` help equivalence: **PASS**;
- changed-source/test line-length preflight: **0 lines over 100**;
- Ruff: **NOT RUN — unavailable/offline**.

Exact uploaded implementation head `72409ba2881b04a7db41a3b30b9dc05c9eb69603` passed internal exact-diff review; `review.md` records the result. The review-record commit will become the PR head and must receive fresh external/exact-head checks.

## Trust boundary

006 does not infer dependencies, scan repository source, analyze file conflicts, execute work, store evidence, or mutate lifecycle state. Projected waves describe dependency order only and MUST NOT be represented as proven conflict-safe parallel execution.

## Immediate ordering

1. Commit the exact-head review record.
2. Open bounded PR #8 with exact-head evidence.
3. Run fresh exact-head CodeRabbit/repository checks and manual head confirmation.
4. Resolve every material defect.
5. Merge only with expected-head guard.
6. Re-read canonical `main` and begin `007-repository-scan`.
