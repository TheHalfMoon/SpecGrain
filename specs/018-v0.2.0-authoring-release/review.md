# Specification 018 Exact-Head Review

## Reviewed product head

`d6f5730daec6960e772e004630c8b4da1609e5b4`

The subsequent evidence/guard commit changes verification material and focused contract tests only; it must receive its own exact-head CI before merge.

## Scope review

The product diff is bounded to release/version/documentation/test/specification surfaces. No `src/specgrain/` behavior is changed. Package runtime dependencies remain empty.

## Release identity and source binding

- Package metadata is `0.2.0`.
- Tag, wheel name, source-distribution name, release-note path, and release title are derived from package metadata.
- A new publication creates the candidate tag at `github.event.workflow_run.head_sha`, the exact successful canonical `main` CI head, and passes the same SHA to `gh release create --target`.
- The release notes file must exist before publication proceeds.

## Historical-release safety

The generalized workflow contains no hard-coded `v0.1.0`, force-tag, force-push, release-edit, or release-upload path. Existing versions are not retargeted. For an already-published candidate version, the workflow verifies tag presence, release tag/name/public state, and the exact two expected asset names, then exits without mutation. It intentionally does not require a historical tag to move to a later `main` CI head.

A candidate tag without a GitHub Release, or a GitHub Release without its tag, fails closed as an ambiguous partial-publication state rather than being silently repaired.

## Findings and repairs

1. The initial implementation verified an already-published candidate's tag/state/assets but did not verify the metadata-derived release title. This was repaired forward in `d6f5730daec6960e772e004630c8b4da1609e5b4`.
2. Focused release-contract guards were added after the first successful exact implementation-head CI to make dynamic `--target`, `--title`, and `--notes-file` binding explicit in repository tests. Their successor head requires fresh exact-head CI.

No unresolved material finding is known at this review point.

## Residual risk

Git tag creation and GitHub Release creation are separate external writes. If release creation fails after a new tag is pushed, a partial candidate tag may remain. The workflow deliberately refuses to guess a repair on rerun. Recovery must be explicit and evidence-preserving; no historical release may be retargeted or mutated.

GitHub-hosted runner/API availability remains external. A workflow success is not itself proof of publication; live release state and asset digests must be inspected before `RELEASED` is claimed.

## Review boundary

Qodo billing status and CodeRabbit's automatic-review skip are not review approvals. No submitted external review or inline thread existed at the reviewed head. Manual review plus exact-head automated evidence is the current review basis, consistent with repository rules that external agents are not verification authority.
