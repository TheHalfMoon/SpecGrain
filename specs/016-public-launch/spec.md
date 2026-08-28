# Specification 016 — Public Launch

## Status

`VERIFYING`

## Outcome

Ship a truthful, installable, cross-platform SpecGrain v0.1.0 release whose public documentation lets a new user understand the product quickly, run real supported commands, execute a tested zero-to-verified API example, inspect migration and benchmark boundaries, and find the repository's contribution/security/trust surfaces.

## In scope

- version `0.1.0` package metadata and release notes;
- permanent GitHub Actions CI covering Linux, macOS, and Windows;
- package build and install verification;
- launch README using only real CLI/API surfaces;
- runnable and tested zero-to-verified example;
- three pinned brownfield example references with reproducible instructions and no fabricated output;
- GitHub Spec Kit migration guide tied to `import-spec-kit` behavior;
- benchmark report that states the distinction between harness verification and empirical comparison results;
- contribution, security/trust, conduct, issue/PR templates, and launch asset surfaces;
- links to existing architecture, methodology, provenance, roadmap, and benchmark strategy documents;
- `v0.1.0` Git tag and GitHub Release after product merge;
- final repository closeout with exact release evidence.

## Out of scope

- new executor/orchestration commands such as `ask`, `packet`, or `verify` merely to match an aspirational demo;
- hosted services, dashboards, accounts, telemetry, model/provider SDKs, or network execution in the core;
- empirical benchmark runs requiring paid/external agents during this spec;
- invented benchmark advantages, popularity guarantees, or competitor-obsolescence claims;
- copying donor code or external documentation into the release without provenance/license review;
- runtime dependency growth without demonstrated necessity.

## Acceptance conditions

1. `pyproject.toml` reports version `0.1.0` and the package remains runtime-dependency-free.
2. Permanent CI runs the full test suite, Ruff, compileall, CLI help parity, and package build/install checks; Linux, macOS, and Windows jobs all pass on the exact product PR head.
3. README quickstart contains only currently implemented commands and can be followed without hidden services.
4. `examples/zero_to_verified.py` reaches an independently verified result using public deterministic APIs, and an automated test executes the example.
5. Brownfield examples identify three real public repositories/revisions or equivalent canonical repositories and provide commands without invented outputs.
6. Migration documentation explains the bounded `import-spec-kit` contract, source revision binding, preserved information, notices, and non-promotion of legacy flat tasks.
7. Benchmark report publishes no numerical arm comparison unless backed by a reproducible run dataset; absence of an empirical dataset is stated plainly when applicable.
8. `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, issue templates, and PR template exist and are consistent with repository governance.
9. Release notes enumerate shipped capabilities and known limitations without claiming deferred features.
10. The product PR is merged with expected-head evidence; live GitHub contains tag `v0.1.0` and a non-draft, non-prerelease GitHub Release targeting the exact release commit.
11. A post-release closeout records exact tag/release evidence and leaves canonical `main` with Specification 016 `CLOSED_CANONICAL` and no next program specification.

## Risks and recovery

- **Documentation drift:** every public command is checked against current CLI source and launch tests; recovery is a normal forward documentation fix.
- **Cross-platform defect:** do not release until the failing platform is repaired or the release is explicitly blocked.
- **Packaging defect:** do not publish/tag until wheel/sdist build and clean wheel install smoke checks pass.
- **Benchmark overclaim:** benchmark report must fail review if it implies comparative superiority without data.
- **Release mutation risk:** tag/release creation occurs only after exact product merge; if release creation fails, leave 016 `RELEASE_BLOCKED` and do not claim completion.

## Dependencies

Specifications 000 through 015 closed canonically. The exact 015 merge commit is `001a70fcabff497c565fa7339381c4da0b4a3881`.
