# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Program status:** `IMPLEMENTING_022`  
**Last closed specification:** `specs/021-public-launch-readiness-hardening/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/022-native-grain-preparation/` — `SHAPED`, product implementation in verification  
**Canonical shaped base:** `4919a4261f649e81cb1f507c0e80bc5c98d848d8`  
**Shaping PR:** `#37` — merged with expected-head protection  
**Canonical post-shaping CI:** `33260132438` — `success` across the permanent five-cell matrix  
**Implementation branch:** `feat/022-native-grain-preparation`  
**Pre-document implementation checkpoint:** `05865fdfeb89e259be237f5e020a87424384d122`  
**Checkpoint CI:** `33260707422` — `success`, 573 tests on Ubuntu/Python 3.11 and all five matrix cells green  
**Published release:** `v0.3.0`  
**Published release source commit:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Published release ID:** `378962445`

## Evidence selecting Specification 022

A maintainer-supplied external adversarial review exercised the public workflow and identified a concrete adoption blocker: native authoring can create DRAFTs but cannot populate Grain-readiness fields or reach the readiness-evaluated lifecycle through the published v0.3.0 CLI.

The repository-side audit `docs/research/post-v0.3-native-workflow-friction-2026-08-29.md` reproduced that finding against exact canonical source:

- published v0.3.0 has no semantic shaping command;
- published v0.3.0 has no CLI transition reaching `SHAPED`, `REFINING`, or `GRAIN`;
- `check_project()` evaluates readiness only for `REFINING` leaves;
- `next_project()` considers only nodes already in `GRAIN`.

This concrete user/adoption friction authorized Specification 022's bounded pre-execution frontier, not unrestricted execution scope.

## Canonical 022 authority

Specification 022 closes only the pre-execution dead end:

```text
DRAFT -> SHAPED -> REFINING -> GRAIN
```

It authorizes:

- explicit DRAFT shaping using existing schema/readiness fields;
- state-only `SHAPED -> REFINING`;
- existing-readiness-gated `REFINING -> GRAIN`;
- native `shape`, `refine`, and `grain` CLI commands;
- exact-preimage single-file mutation and deterministic failure evidence.

It does **not** authorize `GRAIN -> READY`, WorkPacket CLI/execution, agent/provider invocation, verification execution, evidence mutation, PyPI, release/version changes, hosted scope, or readiness weakening.

ADR-0019 governs this bounded mutation authority. The implementation uses `src/specgrain/pregrain.py` as a bounded module while reusing existing store safety primitives; this does not expand the shaped authority.

## Current implementation evidence

The implementation checkpoint `05865fdfeb89e259be237f5e020a87424384d122` is exactly three commits ahead of shaped canonical base `4919a4261f649e81cb1f507c0e80bc5c98d848d8` and changes only:

- `src/specgrain/__init__.py`;
- `src/specgrain/cli.py`;
- `src/specgrain/pregrain.py`;
- `tests/test_pregrain.py`;
- `tests/test_pregrain_cli.py`.

Permanent CI run `33260707422` succeeded on that exact checkpoint across Ubuntu/Python 3.11, 3.12, and 3.13, macOS/Python 3.11, and Windows/Python 3.11. The Ubuntu/Python 3.11 cell recorded 573 passing tests plus Ruff, editable install, tracked-tree cleanliness, compile, CLI smoke, package build, built-wheel installation, and installed CLI smoke.

Public documentation reconciliation is part of the product candidate and therefore requires a new exact-head CI proof before the implementation PR is mergeable under 022 governance.

## Published release truth

The latest published release remains GitHub Release `378962445` / tag `v0.3.0` at exact historical source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

The historical v0.3.0 release contains `init`, `draft`, `recover`, `check`, `next`, `scan`, `prove`, and `import-spec-kit`. It does not contain Specification 022's `shape`, `refine`, or `grain` commands. Repository documentation must preserve that distinction.

## Immediate order

1. Commit the bounded README/architecture/changelog/launch-guard/governance reconciliation on the implementation branch without rewriting history.
2. Run permanent CI on the new exact candidate and fix real failures forward.
3. Review exact shaped-base-to-head diff for hidden defaults, readiness weakening, edge skipping, semantic mutation outside shaping, post-GRAIN authority, recovery widening, dependency creep, unrelated scope, and false historical v0.3.0 claims.
4. Open the bounded Specification 022 implementation PR from exact shaped base `4919a4261f649e81cb1f507c0e80bc5c98d848d8`.
5. Verify exact PR head, changed files, permanent CI, review threads, submitted reviews, mergeability, and review-bot availability. Unavailable/skipped review bots are not PASS.
6. Merge only with expected-head protection after every required gate is genuinely satisfied.
7. Prove merge parentage, canonical post-merge `main`, five-cell post-merge CI, and historical v0.3.0 release preservation.
8. Create a documentation-only Specification 022 closeout recording exact product-merge evidence and re-evaluating the next frontier from post-022 product truth.
9. Merge closeout with expected-head protection, then prove final canonical main, post-closeout CI, release preservation, PR closure, and Specification 022 `CLOSED_CANONICAL`.
10. Shape a successor only if fresh post-022 canonical evidence genuinely authorizes one; WorkPacket/executor scope is not pre-authorized.
