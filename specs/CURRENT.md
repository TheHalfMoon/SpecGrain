# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `b37ea3a06f86d68cb220ec1cd6cc57e71e76653f`  
**Closed specification:** `specs/014-agent-adapters/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/015-specgrain-bench/`  
**Active branch:** `feat/015-specgrain-bench`  
**Active status:** `RUNNING`

## Canonical 014 closeout evidence

Specification 014 closed through PR #16. Final reviewed PR head `35db1bb8a078a68f412def8b50fa4f4e65b7afe5` was merged with expected-head protection into canonical merge commit `b37ea3a06f86d68cb220ec1cd6cc57e71e76653f`; the merge commit's second parent is the exact reviewed head.

## 015 objective

Turn the benchmark strategy into a deterministic public experiment ledger that rejects contaminated comparisons, retains failed runs, and produces reproducible arm summaries without fabricating execution results or automatically claiming a winner.

## Immediate ordering

Implement only `benchmark.py` and focused tests, verify on byte-identical GitHub-runner state, review and merge the bounded PR with expected-head evidence, then begin 016 Public Launch immediately.
