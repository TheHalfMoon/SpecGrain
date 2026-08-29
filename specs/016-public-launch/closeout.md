# Closeout — Specification 016 Public Launch

## Product PR evidence

- Product PR: `#18` — `feat: publish SpecGrain v0.1.0 launch surface`
- Exact reviewed PR head: `1e4b36b169c7ac6d9e59741bb62b6a29b7649a17`
- Exact PR-head CI run: `33234332746`
- PR-head CI result: all five matrix jobs completed successfully:
  - Ubuntu / Python 3.11 — job `99052529952`
  - Ubuntu / Python 3.12 — job `99052530045`
  - Ubuntu / Python 3.13 — job `99052530110`
  - macOS / Python 3.11 — job `99052530058`
  - Windows / Python 3.11 — job `99052530084`
- Inline review threads at merge readiness: none.
- Submitted reviews at merge readiness: none.
- Qodo review was unavailable because the trial had ended; no Qodo PASS is claimed.
- CodeRabbit automatic review was skipped because the repository had fewer than 10 stars; no CodeRabbit PASS is claimed.

## Canonical product merge evidence

- Product merge commit: `5eb46db0479cb8707afe070027dab4f3c558849a`
- First parent: `001a70fcabff497c565fa7339381c4da0b4a3881`
- Second parent: exact reviewed PR head `1e4b36b169c7ac6d9e59741bb62b6a29b7649a17`
- Merge used expected-head protection against `1e4b36b169c7ac6d9e59741bb62b6a29b7649a17`.
- Canonical post-merge CI run: `33234395766`
- Canonical post-merge CI result: all five Linux/macOS/Windows matrix jobs completed successfully.

## Release publication evidence

- Release workflow run: `33234424696`
- Release workflow result: `success`
- Git ref: `refs/tags/v0.1.0`
- Tag target type: `commit`
- Tag target: `5eb46db0479cb8707afe070027dab4f3c558849a`
- GitHub Release ID: `378876694`
- Release name: `SpecGrain v0.1.0`
- Release tag: `v0.1.0`
- Release target commitish: `5eb46db0479cb8707afe070027dab4f3c558849a`
- Draft: `false`
- Prerelease: `false`
- Published at: `2026-08-29T04:41:43Z`

Published assets:

1. `specgrain-0.1.0-py3-none-any.whl`
   - size: `65542` bytes
   - SHA-256: `61d4b0f81cac9fb0a3b347eb5ed740d71c61004e329ada5f9243b8c2a3a14a00`
2. `specgrain-0.1.0.tar.gz`
   - size: `93125` bytes
   - SHA-256: `9864215c96406dd5e821fb3e53fba22e2ac5f8586941c5e384a4b5e43b9dfd0b`

The GitHub Release API currently reports its platform-level `immutable` field as `false`; this closeout therefore does not claim GitHub's optional release-object immutability feature is enabled. The repository's release contract instead binds `v0.1.0` to the exact successful main SHA and fails closed if an existing tag points elsewhere.

## Program completion boundary

Specification 016 is the final planned specification in the initial SpecGrain v0.1 program sequence. No next specification is authorized by this closeout. Deferred ideas require a newly shaped specification based on then-current repository truth.

The closeout PR itself is documentation-only. Its future merge SHA is intentionally not fabricated in this file. `CLOSED_CANONICAL` may be claimed only after the exact closeout head is merged with expected-head protection and live GitHub proves canonical `main` contains that head as the merge second parent.
