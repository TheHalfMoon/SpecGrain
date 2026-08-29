# Verification — Specification 022 Native Grain Preparation

**Status:** `IN_PROGRESS`  
**Canonical shaped base:** `4919a4261f649e81cb1f507c0e80bc5c98d848d8`  
**Implementation branch:** `feat/022-native-grain-preparation`  
**Pre-document checkpoint:** `05865fdfeb89e259be237f5e020a87424384d122`  
**Checkpoint CI:** `33260707422` — `success`

This document records exact evidence as Specification 022 advances. It is not a closeout and does not claim `CLOSED_CANONICAL` before product merge, post-merge CI, documentation-only closeout, and final canonical verification exist.

## Shaping authority proof

Documentation-only shaping PR #37 merged with expected-head protection as canonical commit:

`4919a4261f649e81cb1f507c0e80bc5c98d848d8`

Canonical post-shaping CI run `33260132438` completed `success` on that exact merge. Implementation therefore began only after the shaped 022 authority chain was canonical and permanent CI succeeded.

## Implementation checkpoint identity

Exact compare from shaped canonical base `4919a4261f649e81cb1f507c0e80bc5c98d848d8` to checkpoint `05865fdfeb89e259be237f5e020a87424384d122` is `ahead` by three commits, `behind` by zero, with the shaped canonical base as merge base.

The checkpoint changed exactly five paths:

- `src/specgrain/__init__.py`;
- `src/specgrain/cli.py`;
- `src/specgrain/pregrain.py`;
- `tests/test_pregrain.py`;
- `tests/test_pregrain_cli.py`.

The implementation uses a bounded `pregrain.py` module rather than placing the new authority directly in `store.py`. It reuses existing store safety primitives and does not create generic SpecNode editing authority. This is an implementation-detail refinement of the shaped plan, not a scope expansion.

## Checkpoint permanent CI

Permanent CI run `33260707422` executed on exact head `05865fdfeb89e259be237f5e020a87424384d122` and completed `success` across all five matrix cells:

- Ubuntu / Python 3.11 — job `99122040342` — `success`;
- Ubuntu / Python 3.12 — job `99122040264` — `success`;
- Ubuntu / Python 3.13 — job `99122040347` — `success`;
- macOS / Python 3.11 — job `99122040361` — `success`;
- Windows / Python 3.11 — job `99122040355` — `success`.

Ubuntu/Python 3.11 recorded:

- Ruff source: pass;
- Ruff tests: pass;
- Ruff examples: pass;
- editable install with `--no-deps`: pass;
- full regression: `573 passed in 1.89s`;
- tracked-tree cleanliness: pass;
- compileall: pass;
- source CLI smoke: pass;
- package build: pass;
- built-wheel reinstall with `--no-deps`: pass;
- installed CLI smoke: pass.

The CLI smoke on that exact head exposed:

```text
init
draft
shape
refine
grain
recover
check
next
scan
prove
import-spec-kit
```

The checkpoint CI is strong implementation evidence, but it is not the final product-candidate proof because public documentation reconciliation changes the branch head afterward.

## Bounded-authority review at checkpoint

Manual source/test review found the following against the shaped 022 contract:

- **Hidden defaults:** no risk, recovery, context, evidence, minimality, or safety claims are invented; the command requires explicit values. Canonical readiness version and empty unresolved decisions are the exact shaped contract, not hidden product assertions.
- **Readiness weakening:** none found. Grain promotion calls the existing `evaluate_grain_readiness()` on the exact current REFINING candidate and complete project and writes nothing when blockers exist.
- **Lifecycle edge skipping:** none found. The only authorized edges are `DRAFT -> SHAPED`, `SHAPED -> REFINING`, and readiness-gated `REFINING -> GRAIN`.
- **Semantic mutation outside shaping:** none found. State-only transitions compare semantic revision digests and fail closed if the digest changes.
- **Post-GRAIN authority:** none found. The public API and CLI added by 022 stop at `GRAIN`.
- **Recovery widening:** none found. Every pre-Grain mutation refuses a pending ADR-0018 authoring journal and does not reuse or widen the multi-file transaction journal.
- **Dependency/refinement bypass:** none found. Existing and proposed complete-project refinement/dependency validation runs before persistence.
- **Concurrent/manual drift:** exact preimage is checked before replacement and rechecked at the mutation boundary; drift fails closed.
- **Dependency creep:** none found. Runtime dependency count remains zero and package installation continues to use `--no-deps`.
- **Unrelated executor/provider/network scope:** none found.

Final exact-head review must be repeated after documentation reconciliation and before product merge.

## Public documentation reconciliation contract

The final product candidate must preserve two simultaneously true contracts:

1. Historical GitHub Release `v0.3.0` contains only the already-published command surface and remains unchanged.
2. Current source after Specification 022 product merge adds `shape`, `refine`, and `grain` without claiming a new published release.

README, architecture, changelog, launch guards, tasks, CURRENT, execution master plan, and roadmap are reconciled under this rule. Historical `docs/releases/v0.3.0.md` remains unchanged.

## Historical v0.3.0 evidence before product merge

Live GitHub Release `378962445` remains:

- tag: `v0.3.0`;
- target: `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- wheel asset: ID `535129008`, size `70463`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset: ID `535129009`, size `104057`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

Its release notes enumerate only `init`, `draft`, `recover`, `check`, `next`, `scan`, `prove`, and `import-spec-kit` and explicitly deny automatic lifecycle promotion. Specification 022 must not mutate this historical evidence anchor.

## Remaining verification gates

Before product merge:

1. bind focused/full/static/package/launch tests to the documentation-reconciled exact candidate;
2. prove permanent five-cell CI on that exact head;
3. review exact shaped-base-to-head changed paths and diff;
4. verify PR head, reviews, inline threads, mergeability, and review-bot availability;
5. resolve every material defect forward without force-push/rebase/history rewriting;
6. merge only with expected-head protection.

After product merge:

1. prove merge parentage and canonical `main`;
2. prove permanent five-cell post-merge CI;
3. prove the v0.3.0 tag/release target/assets remain unchanged;
4. record all exact evidence in a documentation-only closeout;
5. re-evaluate the next frontier from post-022 product truth without pre-authorizing WorkPacket/executor work;
6. merge closeout with expected-head protection and prove final canonical CI/release preservation before declaring `CLOSED_CANONICAL`.
