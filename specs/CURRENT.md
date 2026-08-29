# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Program status:** `SHAPING_022`  
**Last closed specification:** `specs/021-public-launch-readiness-hardening/` — `CLOSED_CANONICAL`  
**Prospective active specification:** `specs/022-native-grain-preparation/` — `SHAPED` on documentation branch only  
**Shaping branch:** `docs/022-native-grain-preparation`  
**Canonical pre-022 main:** `3b98914200c68909f09db08642faf56de48305eb`  
**Published release:** `v0.3.0`  
**Published release source commit:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Published release ID:** `378962445`

## Fresh evidence selecting Specification 022

A maintainer-supplied external adversarial review exercised the public workflow and identified a concrete adoption blocker: native authoring can create DRAFTs but cannot populate Grain-readiness fields or reach the readiness-evaluated lifecycle through the supported CLI.

The repository-side audit `docs/research/post-v0.3-native-workflow-friction-2026-08-29.md` reproduced that finding against exact canonical source:

- public CLI has no existing semantic shaping command;
- no public CLI transition reaches `SHAPED`, `REFINING`, or `GRAIN`;
- `check_project()` evaluates readiness only for `REFINING` leaves;
- `next_project()` considers only nodes already in `GRAIN`.

This is the fresh concrete user/adoption friction required by the post-v0.1 governance rules. It authorizes shaping a successor, not unrestricted execution scope.

## Prospective 022 boundary

Specification 022 — Native Grain Preparation closes only the pre-execution dead end:

```text
DRAFT -> SHAPED -> REFINING -> GRAIN
```

It authorizes:

- explicit DRAFT shaping using existing schema/readiness fields;
- state-only `SHAPED -> REFINING`;
- existing-readiness-gated `REFINING -> GRAIN`;
- native `shape`, `refine`, and `grain` CLI commands;
- exact-preimage single-file mutation and deterministic failure evidence.

It does **not** authorize `GRAIN -> READY`, WorkPacket CLI, agent/provider execution, verification execution, evidence mutation, PyPI, release/version changes, hosted scope, or readiness weakening.

ADR-0019 records the bounded mutation authority. Implementation may begin only after the exact shaping head is merged to canonical `main`, post-shaping CI succeeds, and the canonical authority chain is re-read.

## Live GitHub platform truth

Live repository metadata now reports the recommended repository description and the ten recommended topics (`ai-agents`, `cli`, `coding-agents`, `developer-tools`, `python`, `software-delivery`, `software-engineering`, `spec-driven-development`, `spec-kit`, `verification`). These settings were changed outside the file-backed 021 implementation and are recorded here only because live GitHub now proves them.

No claim is made here that native branch protection/rulesets are configured; those platform controls require separate direct evidence.

## Immediate order

1. Publish the documentation-only 022 shaping commit.
2. Run permanent CI on the exact shaping head.
3. Open and review the bounded shaping PR.
4. Merge only with expected-head protection.
5. Prove canonical post-shaping `main` and CI.
6. Re-read the canonical 022 authority chain.
7. Implement the bounded pre-Grain workflow on a fresh implementation branch from exact shaped canonical main.
