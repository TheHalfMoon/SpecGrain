# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Canonical base before current shaping:** `f2e8378dcba0cfea2beedc6da61324b0c3fea95e`  
**Program status:** `SHAPING_024` when this shaping package is canonical  
**Last closed specification:** `specs/023-spec-kit-preset-compatible-import/` — `CLOSED_CANONICAL`  
**Active shaping candidate:** `specs/024-native-workpacket-export/` — `SHAPED` candidate; implementation blocked pending canonical shaping merge  
**Published release:** `v0.3.0`  
**Published release source:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Published release ID:** `378962445`

## Last canonical closed state

Specification 023 is `CLOSED_CANONICAL`. Its bounded template-light Spec Kit import compatibility repair remains unchanged:

- canonical full-template behavior and digest remain stable;
- template-light fallback identity is path-bound and explicit;
- arbitrary prose is not inferred into structured semantics;
- no Spec Kit runtime dependency or workflow execution exists.

The canonical pre-023 full-template report digest remains:

`sha256:678fcc87985902002a9d2bc852196fbffdc59b332740660f1deeaf0d4f58746a`.

The historical `v0.3.0` tag and GitHub Release remain unchanged at `70dd66aba0e68ae710e6ef12605ed153d107bab4` / Release `378962445`.

The SGB-EXP-001 comparative experiment is preserved as `INVALIDATED_ORACLE_REVEALED_PRE_FREEZE`; it produced no valid comparative result and selects no product work.

A bounded concurrent-writer race around exact-preimage validation and atomic replacement remains an explicit residual outside Specification 024 authority.

## Fresh post-023 evidence that selected Specification 024

Selection evidence is recorded in:

`docs/research/post-023-workpacket-handoff-reproduction-2026-08-31.md`

Exact machine-run evidence:

```text
observation_branch = obs/024-workpacket-handoff-fixture
observation_head = 95e5358ed420cd2e6fbd0bc7c56690763cea1283
fixture_blob = 58cb3e355468f6bcd7de63b676dba52361ff0dd7
ci_run = 33416110142
ci_result = completed/success across all five permanent cells
```

The fixture establishes on the exact canonical base that:

1. native CLI reaches an exact stored `GRAIN`;
2. `next --json` reports that Grain as dependency-eligible;
3. current CLI has no `packet` command;
4. the repository already exposes `ContextSource`, context budgeting, `build_work_packet`, and WorkPacket JSON through the public Python API;
5. the exact same Grain can be exported only after leaving the native CLI and assembling those API objects through custom Python glue.

This satisfies the previously stated deterministic-interoperability evidence criterion for shaping a bounded successor. It is not a benchmark or superiority claim.

## Specification 024 bounded outcome

Specification 024 proposes only a read-only native WorkPacket export surface:

```text
specgrain packet <spec_id> [path] --context-sources <json-file> [--json]
```

The candidate:

- requires the exact stored target state `GRAIN`;
- requires the target to be in the current dependency-eligible `next` set;
- accepts explicit bounded `ContextSource.to_dict()` records only;
- applies the Grain's existing token budget through existing context-budget primitives;
- calls the existing `build_work_packet` primitive;
- emits deterministic portable WorkPacket output;
- does not mutate lifecycle, store, execution result, verification, or evidence state;
- adds no provider, executor, network, LLM, or runtime-dependency authority.

No new ADR is selected because the candidate is constrained to expose existing public contracts through a bounded CLI adapter rather than create a new architectural authority boundary.

## Current execution gate

Specification 024 product implementation is **not yet authorized**.

The only eligible work before the shaping merge is documentation-only shaping. T004 and T005 must prove from live GitHub truth that:

1. the exact shaping head changes only authorized research/governance/specification paths;
2. permanent five-cell CI passes on that exact head;
3. reviews, threads, mergeability, and review-system availability are rechecked without treating unavailable systems as PASS;
4. the shaping PR merges with expected-head protection;
5. resulting canonical `main` passes permanent five-cell CI;
6. historical `v0.3.0` remains unchanged.

Only after T005 closes may implementation branch `feat/024-native-workpacket-export` begin.

## Explicitly unselected

Specification 024 does not authorize:

- `GRAIN -> READY` or later lifecycle mutation;
- executor/provider invocation;
- `ExecutionResult` creation or ingestion;
- verification execution or evidence mutation;
- automatic source discovery, source-content packing, retrieval, network access, or LLM context selection;
- SpecNode, WorkPacket, or context contract version redesign;
- stronger multi-writer locking/recovery;
- Spec Kit runtime integration;
- release publication;
- hosted/account/dashboard scope;
- empirical benchmark superiority claims.