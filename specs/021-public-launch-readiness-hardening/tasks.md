# Tasks 021 — Public Launch Readiness Hardening

## Shaping

- [x] T001 Re-read exact canonical `main`, `AGENTS.md`, `specs/CURRENT.md`, constitution, execution master plan, roadmap, current release, package metadata, public README/community/security surfaces, workflows, repository metadata, rulesets, and launch strategy.
- [x] T002 Verify Specification 020 is `CLOSED_CANONICAL`, v0.3.0 is published, no active specification exists, and post-v0.3 observation requires fresh evidence before successor shaping.
- [x] T003 Record fresh launch-readiness evidence in `docs/research/public-launch-readiness-audit-2026-08-29.md`, including stale SECURITY/launch guidance plus GitHub description/topics/ruleset gaps.
- [x] T004 Shape bounded repository-side public launch hardening with no product behavior, package version, runtime dependency, release identity, workflow, PyPI, hosted, or benchmark expansion.
- [x] T005 Merge exact shaping head `70e511e73feb4e561a8137ffd39e481b393c5ec4` through PR #33 with expected-head protection as canonical shaping merge `5c8cfe64f5481c42c53b6fefa91f92e7a2c68811`; exact PR CI `33256371898` and canonical post-merge CI `33256530949` both succeeded across all five permanent cells before implementation.

## Implementation

- [x] T006 Improve README first-screen positioning/trust signals while preserving v0.3.0 install truth, current CLI, and explicit non-claims.
- [x] T007 Correct `SECURITY.md` current supported-version truth and refresh `docs/launch-strategy.md` to v0.3.0.
- [x] T008 Add bounded launch regression checks for LICENSE presence, SECURITY current-version truth, and launch-strategy current-release truth.

## Verification

- [ ] T009 Run full regression, Ruff, compileall, package build/install, CLI smoke, and permanent five-cell CI on the exact implementation head.
- [ ] T010 Review exact diff for `src/specgrain/`, package/version/dependency, release-workflow, historical-release, PyPI, hosted, benchmark, unsupported marketing, and unrelated scope drift.
- [ ] T011 Merge the exact reviewed implementation head with expected-head protection; prove canonical post-merge CI and no-mutation historical v0.3.0 Release verification.

## Canonical closeout

- [ ] T012 Record exact implementation/review/merge/CI/release-verification evidence, re-read live GitHub description/topics/ruleset state, and preserve unproven platform settings as explicit residual operations.
- [ ] T013 Close Specification 021 through a bounded closeout change, exact-head CI/review, expected-head merge, canonical post-closeout CI, and post-closeout no-mutation Release verification.
