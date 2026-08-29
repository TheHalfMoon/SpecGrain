# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Program status:** `SPEC_021_SHAPING`  
**Last closed specification:** `specs/020-v0.3.0-recursive-authoring-release/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/021-public-launch-readiness-hardening/` — prospective `SHAPED` on its shaping branch; implementation is not authorized until canonical shaping merge and post-merge CI succeed  
**Active branch:** `spec/021-public-launch-readiness-hardening` for shaping only  
**Next planned work:** canonicalize Specification 021 shaping, prove post-merge CI, then implement only the bounded public-launch hardening tasks  
**Published release:** `v0.3.0`  
**Published release source commit:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Published release ID:** `378962445`

## Specification 020 canonical closeout

Specification 020 is `CLOSED_CANONICAL`. Product merge `70dd66aba0e68ae710e6ef12605ed153d107bab4` passed canonical product CI `33249920673`; Release workflow `33249956337`, job `99093825183`, published new GitHub Release `378962445` / tag `v0.3.0` from that exact product revision. Documentation-only closeout merged as `123e1ded9d6bdc1aa15767ec7185bfffab5f8eba`; canonical post-closeout CI `33250422380` succeeded and Release verification `33250468134`, job `99095156240`, proved historical v0.3.0 remained published at product source `70dd66a...` without mutation.

Final canonical reconciliation merge `1ea1ee8554ce84f96f67d12eb86188324c81534a` recorded Specification 020 as `CLOSED_CANONICAL`, all 020 tasks complete, and the program frontier as `POST_V0.3_OBSERVATION` with no selected successor.

## Fresh Specification 021 evidence

An explicit maintainer public-launch-readiness request triggered a fresh repository audit at exact canonical revision `1ea1ee8554ce84f96f67d12eb86188324c81534a`.

`docs/research/public-launch-readiness-audit-2026-08-29.md` records the bounded evidence:

- GitHub repository metadata has no description and no topics;
- `main` is not protected and no repository ruleset exists;
- MIT licensing is present, recognized by GitHub, and consistent with package metadata;
- package keywords, current v0.3.0 README install/CLI truth, community files, changelog, release notes, permanent cross-platform CI, and monotonic release automation are present;
- `SECURITY.md` is stale because it still presents `0.1.x` as the supported release line;
- `docs/launch-strategy.md` is stale because it still presents a `v0.1.0 launch demo`;
- README is accurate but has a bounded first-screen presentation improvement available without capability expansion.

These reproducible documentation defects plus the concrete maintainer request are fresh evidence of launch/adoption friction and are sufficient to shape Specification 021 narrowly.

## Specification 021 shaped boundary

Specification 021 is repository-side public launch hardening only. Expected implementation changes are limited to `README.md`, `SECURITY.md`, `docs/launch-strategy.md`, bounded launch tests, and 021 evidence/status files.

021 does not authorize `src/specgrain/` behavior changes, package version changes, runtime dependencies, release-workflow changes, PyPI, lifecycle/readiness/execution authority, hosted surfaces, provider integration, benchmark execution, or historical release mutation.

GitHub description/topics/ruleset targets are recorded as platform metadata recommendations. They must not be claimed as applied without live GitHub settings evidence.

## Implementation gate

This shaping chain is prospective until merged to canonical `main` with expected-head protection. Implementation may begin only after:

1. the exact shaping head passes required PR CI/review;
2. the shaping PR merges with expected-head protection;
3. canonical post-merge CI succeeds on the exact shaping merge;
4. canonical `main` is re-read and 021 implementation eligibility is confirmed.
