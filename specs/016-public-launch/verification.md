# Verification — Specification 016 Public Launch

## Candidate identity

- Canonical base: `001a70fcabff497c565fa7339381c4da0b4a3881`
- Verified candidate: `65cc610a3fd87b9b695769ee6cd0a54ce6cd1faf`
- Candidate tree: `20e06969a3ccfd63630afadbb9fcc99c43205daf`
- Permanent CI run: `33200760574`
- CI conclusion: `success`

## Permanent cross-platform CI

The exact candidate completed the permanent five-cell matrix successfully:

- Ubuntu / Python 3.11 — job `98949340764`
- Ubuntu / Python 3.12 — job `98949340814`
- Ubuntu / Python 3.13 — job `98949340901`
- macOS / Python 3.11 — job `98949340865`
- Windows / Python 3.11 — job `98949340465`

Every cell completed the same release gate:

1. `actions/checkout@v7` and `actions/setup-python@v7`;
2. pinned verification tools with `ruff==0.6.9`;
3. Ruff for `src`, `tests`, and `examples`;
4. editable package installation with no runtime dependencies;
5. full regression;
6. tracked-tree immutability after tests;
7. `compileall` for source, tests, and examples;
8. module and installed-console CLI help smoke checks;
9. sdist/wheel build;
10. wheel reinstall with `--no-deps`;
11. installed CLI smoke.

The Ubuntu/Python 3.11 exact-head log reports `520 passed` and successful creation of both `specgrain-0.1.0.tar.gz` and `specgrain-0.1.0-py3-none-any.whl`.

## Launch-surface verification

`tests/test_launch.py` additionally verifies that:

- package metadata is version `0.1.0`, runtime dependencies remain empty, and SPDX/PEP 639 license metadata is present;
- CI covers Ubuntu, macOS, Windows and supported Python cells;
- current Node 24 GitHub Actions majors are used and the retired workflow majors are absent;
- release creation is post-CI, exact-SHA-bound, includes wheel/sdist assets, rejects conflicting partial release state, and becomes a no-op after a valid immutable release already exists;
- README exposes only implemented CLI commands;
- the zero-to-verified example executes and reaches `GRAIN`, `VERIFIED`, and `VERIFIED` proof states;
- required public launch/community files exist;
- Python source/test/example lines do not exceed 100 characters;
- relative Markdown links in the public launch document set resolve;
- brownfield examples remain pinned and publish no precomputed fake output;
- the benchmark report declares no empirical dataset and no winner;
- Spec Kit migration keeps legacy flat tasks outside the core ontology.

## Release hardening discovered during verification

The initial permanent gate exposed pre-existing Ruff debt in source and tests. The findings were repaired mechanically through bounded forward changes, and were retained only after Ruff, full regression, compile, and whitespace checks passed. These repairs did not add product behavior.

Packaging verification also exposed deprecated legacy license metadata. The candidate now uses SPDX `MIT`, includes `LICENSE`, requires `setuptools>=77`, and builds without the prior Setuptools license-classifier deprecation.

GitHub runner logs exposed Node 20 deprecation warnings from older action majors. The final candidate uses `actions/checkout@v7` and `actions/setup-python@v7`; the exact-head v7 logs do not emit that deprecation warning.

## Not yet proven

The following are intentionally not claimed by this pre-merge verification:

- product PR merge;
- canonical post-merge `main` CI;
- creation of Git tag `v0.1.0`;
- GitHub Release publication and exact release-asset verification;
- post-release documentation-only canonical closeout.

Those gates remain ordered after the product PR merge.

## Result

`PR_READY`
