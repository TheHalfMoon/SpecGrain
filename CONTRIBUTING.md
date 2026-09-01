# Contributing to SpecGrain

Thanks for helping improve SpecGrain.

The project favors **small, reproducible, evidence-backed contributions** over broad rewrites. A strong contribution should be easy for another developer to understand, verify, and recover from independently.

Before changing product behavior, read:

1. [`AGENTS.md`](AGENTS.md)
2. [`specs/CURRENT.md`](specs/CURRENT.md)
3. [`.specify/memory/constitution.md`](.specify/memory/constitution.md)
4. [`docs/execution-master-plan.md`](docs/execution-master-plan.md)

Live canonical repository state overrides stale plans or chat handoffs.

## Good places to contribute

Useful bounded contributions include:

- reproducible bug fixtures;
- deterministic validation improvements selected by current authority;
- repository-scanner signals;
- adapter and contract representations;
- focused test coverage;
- documentation and examples;
- visualization layers over stable JSON contracts;
- benchmark-methodology improvements that preserve contamination and unfavorable-result evidence.

Product behavior must not be expanded just because an adjacent improvement looks useful. Product changes need an active specification or fresh reproducible evidence that canonically selects the gap.

## Development setup

SpecGrain requires Python 3.11 or newer.

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check src tests examples
python -m compileall -q src tests examples
```

Permanent CI exercises:

- Ubuntu / Python 3.11
- Ubuntu / Python 3.12
- Ubuntu / Python 3.13
- macOS / Python 3.11
- Windows / Python 3.11

The runtime package intentionally has zero third-party dependencies.

## Keep the change small

Prefer one independently understandable outcome per pull request.

A change is probably too large if it requires:

- unrelated cleanup to make the main change reviewable;
- a broad change surface with no explicit justification;
- multiple independent outcomes;
- hidden assumptions about risk, recovery, context, or evidence;
- a large prompt instead of further refinement.

When in doubt, reduce the change until the acceptance boundary is obvious.

## Before opening a pull request

Run the relevant focused tests first, then the repository-wide checks when the change is ready:

```bash
python -m pytest
python -m ruff check src tests examples
python -m compileall -q src tests examples
```

Also verify that tests did not mutate tracked repository state.

For product changes, confirm the exact changed-path surface matches the active specification or bounded issue.

## Pull request checklist

A strong PR description states:

- the specification/task, reproducible defect, or documentation issue being addressed;
- the exact changed paths;
- the intended behavior and explicit non-goals;
- tests and static checks run;
- acceptance evidence;
- residual risks or known limitations;
- recovery or rollback expectations when relevant;
- provenance for adapted external material.

Do not treat author or executor self-report as verification. Green CI is necessary where configured, but it is not by itself proof that the active acceptance conditions are satisfied.

Do not force-push, rebase shared history, or destructively rewrite published commits. Resolve material review findings with forward commits and re-run verification on the exact resulting head.

## Documentation contributions

Documentation improvements are welcome, especially when they:

- make the first-run experience clearer;
- correct stale repository truth;
- explain an existing deterministic contract more precisely;
- add a minimal reproducible example;
- reduce ambiguity without widening product authority.

Avoid documentation that promises behavior not present in the referenced release or current source revision.

## Donor and external code

External projects are references and donors, not undocumented code sources.

Before adapting external material:

- verify its license;
- preserve required copyright and license notices;
- record material provenance;
- prefer a smaller native implementation when it is clearer.

GitHub Spec Kit is an influence and compatibility target; SpecGrain remains architecturally independent.

## Benchmarks

Benchmark contributions must preserve failed runs, ties, limitations, contamination failures, and unfavorable outcomes.

Do not optimize prompts, fixtures, or implementations using hidden evaluation answers. Never manufacture a winner from incomplete or invalid evidence.

## Security and conduct

Follow [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

Do not disclose exploitable vulnerability details in a public issue. Use the process in [`SECURITY.md`](SECURITY.md) for security reports.

For ordinary defects or proposals, use the repository's GitHub issue templates and include the smallest reproducible evidence you can provide.
