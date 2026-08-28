# Review 015 — SpecGrainBench

## Reviewed product head

`7548becacb65b890fdfafc3dc4789fee215172fd`

Exact product diff from planning head `a4882860ea9e21b43ea5b64cc1481acc69780ae1` is two commits ahead and changes exactly:

- `src/specgrain/benchmark.py`;
- `tests/test_benchmark.py`.

## Findings

No material repository-review defect remains in the exact product diff.

The benchmark core is a deterministic experiment ledger, not an agent runner. It validates comparable cells before reporting, retains failed/blocked observations, and exposes totals/counts without post-hoc exclusion or automatic method ranking.

The initial arm set is fixed to prompt-only, GitHub Spec Kit, and SpecGrain. The same benchmark case pins repository, task, acceptance oracle, environment, scorer, repetitions, and optional common model/provider configuration. Each arm pins its method configuration digest.

Preflight invalidates missing/duplicate cells, workspace/context reuse, baseline/config mismatches, and hidden-scorer leakage. Invalid datasets may still be summarized diagnostically, but `valid_comparison` remains false and no superiority claim is produced.

## Verification disposition

Verification-only run `33196205039` on byte-identical product/test blobs completed successfully across pytest, changed-surface Ruff, prior-baseline Ruff, full-repository Ruff, compile, install, entry-point parity, and line-length gates.

## Residual boundary

Specification 015 does not claim that SpecGrain outperforms another method. No real coding-agent comparison dataset was executed inside the repository because the deterministic core has no authorization or capability to invent external model executions. Public empirical claims require external runner observations that satisfy this ledger and must publish ties, losses, failures, and limitations.
