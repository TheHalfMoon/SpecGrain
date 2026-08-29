# Plan 021 — Public Launch Readiness Hardening

## Authority

Follow `AGENTS.md`, `specs/CURRENT.md`, `.specify/memory/constitution.md`, `docs/execution-master-plan.md`, `docs/research/post-v0.3-product-audit-2026-08-29.md`, `docs/research/public-launch-readiness-audit-2026-08-29.md`, ADR-0017, this specification, and live GitHub truth.

Implementation begins only after this exact shaping chain is merged canonically and canonical shaping post-merge CI succeeds.

## Delivery slices

### A. Public first-screen truth

- preserve the product tagline;
- align the README opening on the current agent-neutral delivery-control-plane positioning;
- add concise CI/current-release/Python/MIT trust signals;
- keep the v0.3.0 release install path prominent;
- preserve current CLI and explicit non-claims.

### B. Support and launch documentation truth

- update `SECURITY.md` from stale `0.1.x` current-support text to the current `0.3.x` supported line and explicit older-version policy;
- refresh `docs/launch-strategy.md` from the historical v0.1.0 demo to current v0.3.0 public guidance;
- do not invent a docs site, support channel, SLA, or long-term-support policy.

### C. Regression protection

- update `tests/test_launch.py` only as needed to require the root MIT license as a public launch file;
- assert SECURITY current-version truth;
- assert launch-strategy current-release truth and reject the stale historical demo heading;
- preserve all existing README CLI/release/trust assertions.

### D. Exact-head verification and closeout

- run permanent CI on the exact implementation PR head;
- review exact diff for package/release/product/workflow drift and unrelated launch scope;
- merge with expected-head protection;
- prove canonical post-merge CI;
- prove subsequent Release workflow performs historical v0.3.0 verification only;
- close through a separate bounded status/evidence change;
- record live GitHub description/topics/ruleset state as external platform metadata without fabricating configuration.

## Expected implementation change surface

Implementation is expected to remain within:

- `README.md`;
- `SECURITY.md`;
- `docs/launch-strategy.md`;
- `tests/test_launch.py`;
- `specs/021-public-launch-readiness-hardening/**` for evidence/status updates;
- `specs/CURRENT.md` for active-state reconciliation.

No `src/specgrain/`, `pyproject.toml`, `CHANGELOG.md`, release notes, workflow, package-version, runtime-dependency, lifecycle/readiness/execution, PyPI, benchmark-data, hosted, or provider change is expected.

## External platform observations

The launch audit records recommended repository description/topics and a minimal `main` ruleset target. These are GitHub settings, not committed product files. They remain explicit platform operations unless live settings evidence proves they were applied.
