# Review — Specification 016 Public Launch

## Reviewed identity

- Canonical base: `001a70fcabff497c565fa7339381c4da0b4a3881`
- Reviewed candidate: `65cc610a3fd87b9b695769ee6cd0a54ce6cd1faf`
- Compare state: candidate is ahead of canonical base and not behind.

## Scope review

The exact compare is limited to the public launch/release surface, Specification 016 state, the Specification 015 closeout task update, mechanical source/test lint hardening discovered by the release gate, and launch-surface tests.

The source changes are bounded to eleven existing `src/specgrain/**` files and are mechanical Ruff/import/simplification hardening. They were generated or applied from explicit Ruff findings and preserved only after full regression. No new runtime feature or execution authority is introduced by those edits.

## Claim review

- README describes SpecGrain v0.1.0 as a deterministic control plane and does not present it as an autonomous agent runner.
- README uses only current commands: `init`, `check`, `next`, `scan`, `prove`, and `import-spec-kit`.
- Brownfield examples pin real repository revisions and intentionally publish no precomputed scan output.
- The benchmark report states that no empirical comparative dataset is published and declares no winner.
- Release notes distinguish shipped behavior from deferred work.
- No popularity, market, benchmark-superiority, or competitor-obsolescence claim is asserted as evidence-backed fact.

## Dependency and packaging review

- Runtime dependencies remain `[]`.
- Development-only Ruff is pinned to `0.6.9` for reproducible lint behavior.
- Package metadata uses SPDX `MIT` and includes `LICENSE`.
- Build backend requires `setuptools>=77` for the PEP 639 metadata contract.
- Permanent CI builds and reinstalls the wheel with `--no-deps`.

## Release-safety review

The release workflow:

- runs only after successful `CI` on branch `main`;
- checks out `workflow_run.head_sha` rather than a moving branch;
- builds the two exact v0.1.0 distribution names before release mutation;
- creates tag `v0.1.0` at the successful main SHA only when absent;
- refuses an existing pre-release tag that points elsewhere;
- requires an existing release to be public, non-draft, non-prerelease, and to expose exactly the wheel/sdist assets;
- becomes a successful no-op after that valid immutable release exists, preventing later closeout CI from moving the tag;
- does not use force-fetch, force-push, rebase, or destructive history rewriting.

## Security and provenance review

- The core remains network-free and runtime-dependency-free.
- Release automation receives only the repository-scoped `GITHUB_TOKEN` permission needed for contents/tag/release writes.
- No secrets are introduced into repository content.
- No donor repository code was copied into the launch implementation; external repositories appear only as pinned brownfield examples or documented provenance/reference material.

## Residual boundaries

- Real multi-arm benchmark execution is not part of this release; the report states that limitation.
- Tag and GitHub Release existence cannot be reviewed before product merge and successful canonical-main CI.
- External review services may be unavailable; exact-head automated checks and manual diff review do not imply an external reviewer approval that did not occur.

## Review result

No material pre-merge defect remains on reviewed candidate `65cc610a3fd87b9b695769ee6cd0a54ce6cd1faf`.
