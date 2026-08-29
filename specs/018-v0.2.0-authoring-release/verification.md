# Specification 018 Verification Record

## Authority

Specification 018 shaping became canonical through PR #23. The exact shaping head was `68e830dc51d0df4bc521607be46ce9f11dc34acd`; exact-head CI run `33237175016` completed successfully before expected-head merge `b170aed92812c367282fbacb5d46e5acb450a196`. The merge second parent is the exact shaping head. Canonical shaping post-merge CI run `33245330017` then completed the permanent five-cell matrix successfully.

## Implementation history

Implementation branch: `feat/018-v0.2.0-authoring-release`, created from exact canonical shaping merge `b170aed92812c367282fbacb5d46e5acb450a196`.

- `22be323e4d73a310d6f89d4dd7cb27d7b09efd69` — initial bounded v0.2.0 release implementation.
- `d6f5730daec6960e772e004630c8b4da1609e5b4` — forward repair that added verification of the metadata-derived GitHub Release title on the already-published path.

No `src/specgrain/` product-behavior file changed in the implementation diff.

## Exact implementation-head CI

Push CI run `33245538486` executed on exact head `d6f5730daec6960e772e004630c8b4da1609e5b4` and completed successfully across all permanent jobs:

- Windows / Python 3.11 — job `99082235897`;
- Ubuntu / Python 3.11 — job `99082236028`;
- macOS / Python 3.11 — job `99082236039`;
- Ubuntu / Python 3.13 — job `99082236040`;
- Ubuntu / Python 3.12 — job `99082236045`.

Ubuntu/Python 3.11 recorded:

- Ruff source/tests/examples: success;
- full regression: `531 passed in 1.37s`;
- tracked-tree cleanliness: success;
- compile: success;
- CLI smoke: `init`, `draft`, `check`, `next`, `scan`, `prove`, `import-spec-kit` present;
- package build: `specgrain-0.2.0.tar.gz` and `specgrain-0.2.0-py3-none-any.whl` built successfully;
- built wheel reinstall and installed CLI smoke: success.

The evidence commit that adds this record and focused release-contract guards advances the PR head. That newer exact head must complete the same required CI gate before product merge; this record does not pre-authorize merge of an unproved successor head.

## External review boundary

At the `d6f5730...` review point, GitHub reported no submitted pull-request reviews and no inline review threads. Qodo reported that reviews were paused because the trial ended. CodeRabbit reported that automatic review was skipped because the repository had fewer than ten stars. Neither condition is treated as external approval or verification.

## Publication boundary

No `v0.2.0` release is claimed by this verification record. Publication authority begins only after expected-head product merge, successful canonical post-merge CI on that exact merge, the release workflow result, and live tag/release/asset verification required by Specification 018.
