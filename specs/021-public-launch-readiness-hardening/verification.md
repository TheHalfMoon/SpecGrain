# Verification — Specification 021 Public Launch Readiness Hardening

**Verified implementation head:** `e95bbafdd2bc66ea67e40e0690c053806acf85c3`  
**Canonical shaping base:** `5c8cfe64f5481c42c53b6fefa91f92e7a2c68811`  
**Implementation PR:** #34  
**Exact PR CI:** `33256769276` — `completed/success`

## Permanent matrix

The exact implementation candidate passed every permanent CI cell:

- Ubuntu / Python 3.11 — job `99111766462` — success;
- Ubuntu / Python 3.12 — job `99111766475` — success;
- Ubuntu / Python 3.13 — job `99111766478` — success;
- macOS / Python 3.11 — job `99111766461` — success;
- Windows / Python 3.11 — job `99111766486` — success.

Ubuntu/Python 3.11 recorded `558 passed in 1.58s`, successful Ruff checks for `src`, `tests`, and `examples`, editable installation of `specgrain-0.3.0` with `--no-deps`, a clean tracked-tree check after tests, successful `compileall`, module/installed CLI smoke, successful wheel/sdist build, built-wheel reinstall with `--no-deps`, and installed CLI smoke.

The CLI remained exactly:

- `init`
- `draft`
- `recover`
- `check`
- `next`
- `scan`
- `prove`
- `import-spec-kit`

## Exact implementation scope

PR #34 changed exactly six paths, with 87 additions and 54 deletions:

- `README.md`;
- `SECURITY.md`;
- `docs/launch-strategy.md`;
- `specs/021-public-launch-readiness-hardening/tasks.md`;
- `specs/CURRENT.md`;
- `tests/test_launch.py`.

There were no `src/specgrain/`, `pyproject.toml`, runtime-dependency, package-version, workflow, changelog, release-note, PyPI, hosted/provider, lifecycle/readiness/execution, benchmark-data, or historical-release changes.

## Canonical product/documentation merge

PR #34 merged with expected-head protection from exact reviewed head `e95bbafdd2bc66ea67e40e0690c053806acf85c3` as canonical merge `88e174818870cb90d18537b0c8aea810c84fc244`.

The merge is GitHub-signature verified and has:

- first parent: canonical shaping merge `5c8cfe64f5481c42c53b6fefa91f92e7a2c68811`;
- second parent: exact implementation head `e95bbafdd2bc66ea67e40e0690c053806acf85c3`.

Canonical post-merge CI `33256836246` completed `success` across all five permanent cells on exact merge `88e174818870cb90d18537b0c8aea810c84fc244`.

Post-merge matrix jobs:

- Ubuntu / Python 3.11 — `99111941746` — success;
- Ubuntu / Python 3.12 — `99111941689` — success;
- Ubuntu / Python 3.13 — `99111941802` — success;
- macOS / Python 3.11 — `99111941744` — success;
- Windows / Python 3.11 — `99111941796` — success.

## Historical v0.3.0 release preservation

Release verification run `33256877372`, job `99112050245`, completed `success` after checking out exact canonical merge `88e174818870cb90d18537b0c8aea810c84fc244`.

The workflow resolved metadata version `0.3.0`, built the expected wheel and source distribution, and reported:

`SpecGrain v0.3.0 is already published at historical tag target 70dd66aba0e68ae710e6ef12605ed153d107bab4; no release mutation is required.`

Live GitHub release truth remained unchanged after verification:

- Release ID: `378962445`;
- tag: `v0.3.0`;
- target: `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- draft: `false`;
- prerelease: `false`;
- wheel asset ID `535129008`, size `70463`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset ID `535129009`, size `104057`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

## External GitHub platform state

Live repository settings were re-read after the canonical implementation merge:

- repository description: `null`;
- topics: `[]`;
- `main` branch protection: disabled;
- repository rulesets: `[]`.

These are explicit platform residuals. The repository interface available to this execution can read but cannot mutate those settings, so this verification does not claim they were applied.
