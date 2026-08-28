# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Last verified canonical main:** `b37ea3a06f86d68cb220ec1cd6cc57e71e76653f`  
**Closed specification:** `specs/014-agent-adapters/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/015-specgrain-bench/`  
**Active branch:** `feat/015-specgrain-bench`  
**Active status:** `PR_READY`

## Canonical 014 closeout evidence

Specification 014 closed through PR #16. Final reviewed PR head `35db1bb8a078a68f412def8b50fa4f4e65b7afe5` was merged with expected-head protection into canonical merge commit `b37ea3a06f86d68cb220ec1cd6cc57e71e76653f`; the merge commit's second parent is the exact reviewed head.

## 015 exact product evidence

Product commit: `7548becacb65b890fdfafc3dc4789fee215172fd`.

```text
src/specgrain/benchmark.py        d118e7879691bd6b24541d37f84cd513903f95e5
tests/test_benchmark.py           73bf295f130539e1a3d23e652fc9e2a457b6d8c2
```

Verification-only commit `7ce70d65c90b64fb3bd6f6250d8cf01d47666fab` preserved those exact blobs. GitHub Actions run `33196205039` completed successfully with full pytest regression, changed-surface/baseline/full Ruff checks, compileall, install, entry-point parity, and line-length gates all PASS.

## Immediate ordering

Open the bounded 015 PR at the current documentation head, resolve every material exact-head review defect, merge only with expected-head evidence, prove canonical `main`, then begin 016 Public Launch immediately.
