# Contributing to SpecGrain

SpecGrain welcomes small, evidence-backed contributions. The repository's governing instructions are in `AGENTS.md` and `.specify/memory/constitution.md`; contributors should read them before changing product behavior.

## Good contribution shapes

Useful first contributions include bounded repository scanner signals, deterministic validation rules, benchmark cases, adapter representations, documentation examples, and visualization layers over stable JSON contracts.

Prefer one independently understandable outcome per pull request. If a change needs a large prompt, broad change surface, or unrelated cleanup to be reviewable, refine it further.

## Development setup

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check src tests examples
python -m compileall -q src tests examples
```

Python 3.11 is the minimum supported version. Permanent CI also exercises Python 3.12 and 3.13 on Ubuntu plus Python 3.11 on macOS and Windows.

## Pull requests

A product PR should state:

- the specification/task or bounded issue it implements;
- exact scope changed;
- tests and static checks run;
- acceptance evidence;
- residual risks or limitations;
- provenance for adapted external material.

Do not treat executor or author self-report as sufficient verification. Do not force-push or rewrite published shared history. Resolve material review defects with forward commits and re-run exact-head verification.

## Donor and external code

External projects are references/donors, not undocumented code sources. Verify licenses before adapting material, preserve required notices, and record material provenance. GitHub Spec Kit is a compatibility target and influence; SpecGrain is architecturally independent.

## Benchmarks

Benchmark contributions must preserve failed runs, ties, limitations, contamination failures, and unfavorable results. Do not optimize fixtures or prompts using hidden evaluation answers.

## Conduct and security

Follow [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Do not disclose exploitable vulnerability details in a public issue; follow [`SECURITY.md`](SECURITY.md).
