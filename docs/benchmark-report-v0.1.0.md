# SpecGrainBench Report — v0.1.0

## Publication status

**Harness status:** implemented and repository-verified.  
**Empirical comparative dataset:** not yet published.  
**Declared winner:** none.

This report intentionally contains no fabricated prompt-only vs GitHub Spec Kit vs SpecGrain score table. v0.1.0 proves the benchmark control surface, not a comparative product advantage.

## What v0.1.0 ships

Specification 015 implements deterministic benchmark records for the initial three arms:

1. prompt-only development;
2. GitHub Spec Kit;
3. SpecGrain.

The harness validates expected `(case, arm, repetition)` cells and rejects comparisons when experiment integrity is not established. Its preflight detects missing or duplicate cells, workspace/context reuse, repository baseline mismatch, scorer/config mismatch, method/model configuration mismatch, and hidden-scorer leakage. Failed and blocked runs remain in the ledger instead of being filtered out.

Reports aggregate recorded outcome/efficiency observations but deliberately expose no automatic `winner` field.

## What has not been measured yet

The repository does not currently contain a public completed multi-arm dataset with controlled external agent/model executions. Therefore v0.1.0 makes no numerical claim about acceptance rate, token cost, cycle time, rework, regression rate, scope accuracy, or human intervention differences between the three methods.

A missing empirical dataset is not evidence of a tie and is not evidence of superiority. It means the comparison is not yet authorized for publication.

## Gate for a future comparative report

A publishable comparative dataset must include, for every case and run:

- immutable repository snapshot;
- task intent and acceptance oracle;
- allowed/forbidden surfaces where applicable;
- exact method/plugin/skill configuration;
- model/provider configuration when applicable;
- fresh isolated workspace and context/session identity;
- repetition/seed policy;
- scoring code revision;
- contamination-preflight result;
- raw run status including failures/blocks;
- tokens/context cost when available;
- cycle/retry/rework observations;
- repository diff and scope metrics;
- human interventions;
- safety/adversarial results for applicable cases.

Unfavorable results, ties, invalidated cells, and corrected claims must remain visible.

## Reproduce the control-plane verification

The repository test suite exercises the benchmark ledger and contamination rules. Run:

```bash
python -m pip install -e ".[dev]"
python -m pytest tests/test_benchmark.py
python -m ruff check src/specgrain/benchmark.py tests/test_benchmark.py
```

For methodology and anti-gaming rules, see [`benchmark-strategy.md`](benchmark-strategy.md). For the exact shipped contract, see `specs/015-specgrain-bench/`.
