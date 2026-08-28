# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `197ddfb68d94bf8998d68d1371c26431f3816ca0`  
**Closed specification:** `specs/007-repository-scan/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/008-context-budget/`  
**Active branch:** `feat/008-context-budget`  
**Active status:** `PR_READY`

## Canonical continuation references

Read `docs/execution-master-plan.md` after the constitution. `docs/roadmap.md` remains the milestone-level sequencing reference. Live GitHub truth always overrides this state file if branches, PRs, checks, or canonical `main` move.

## Canonical 007 closeout evidence

Specification 007 closed through PR #9: final reviewed PR head `35571d5cdcbe441b04a8e975c5eb6be0fe088698`, merged with expected-head protection into canonical merge commit `197ddfb68d94bf8998d68d1371c26431f3816ca0`. The merge commit's second parent is the exact reviewed PR head.

## 008 exact verified product state

Exact reviewed product commit:

`5d7822218888302d95ccfc580ea37a0853759d34`

Exact product/test blobs:

```text
src/specgrain/context.py          c68cf285ae4fa2358583163b136e55e53ee7cb0c
src/specgrain/__init__.py         b1a5d6f6678b3e83a3ab0075cf8d570ee348df15
tests/test_context.py             31fd6c0e13a8784bf7af8c91270e9da718649379
```

Verification for those exact uploaded bytes:

- 354 pytest tests PASS;
- compileall PASS;
- editable install PASS;
- console/module help parity PASS;
- 0 changed source/test lines over 100 characters;
- Ruff NOT RUN because unavailable.

The exact implementation diff from planning head `ca53852a2239483e2a51b72de8786e785b04f37a` contains only the three planned implementation/test files.

## 008 boundary

008 owns immutable revision-bound context-source records, explicit byte/token costs, required/optional classification, deterministic budget policy, required-context blockers, optional packing, plan digest, and a normalized RepositoryMap bridge.

It does not retrieve file contents, invoke a tokenizer/LLM/embedding service, mutate lifecycle/store state, alter dependency scheduling, build WorkPackets/evidence, execute subprocesses, or add runtime dependencies.

## Immediate ordering

1. Re-read live 008 branch head and confirm no competing PR exists.
2. Open the bounded 008 implementation PR against canonical `main` using the live exact documentation head.
3. Re-read exact PR head, diff, statuses, reviews, comments, and threads.
4. Resolve every material exact-head defect with forward-only commits and repeat affected verification.
5. Merge only with an expected-head guard.
6. Re-read canonical `main` after merge and prove the exact head landed.
7. On the 009 planning branch, close 008 T017–T019 and mark 008 `CLOSED_CANONICAL`.
8. Begin `009-work-packet` immediately.
