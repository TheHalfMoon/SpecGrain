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

- [x] T009 Exact implementation head `e95bbafdd2bc66ea67e40e0690c053806acf85c3` passed permanent five-cell CI `33256769276`; Ubuntu/Python 3.11 job `99111766462` recorded `558 passed in 1.58s` plus successful Ruff, tracked-tree cleanliness, compileall, package build/install, and CLI smoke.
- [x] T010 Exact PR #34 diff review proved exactly six changed paths and no `src/specgrain/`, package/version/dependency, release-workflow, historical-release, PyPI, hosted/provider, lifecycle/readiness/execution, benchmark-data, unsupported marketing, or unrelated scope drift. Final review recheck found no submitted reviews or inline review threads.
- [x] T011 PR #34 merged with expected-head protection from exact reviewed head `e95bbafdd2bc66ea67e40e0690c053806acf85c3` as canonical merge `88e174818870cb90d18537b0c8aea810c84fc244`; canonical CI `33256836246` succeeded across all five cells and Release verification `33256877372`, job `99112050245`, proved historical v0.3.0 remained at `70dd66aba0e68ae710e6ef12605ed153d107bab4` without mutation.

## Canonical closeout

- [x] T012 Record exact implementation/review/merge/CI/release-verification evidence; re-read live GitHub repository metadata, `main` protection, and rulesets; preserve description/topics/ruleset gaps as explicit unproven platform residuals because the available repository interface is read-only for those settings.
- [ ] T013 Close Specification 021 through this bounded closeout change, exact-head CI/review, expected-head merge, canonical post-closeout CI, and post-closeout no-mutation Release verification.
