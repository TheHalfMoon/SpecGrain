# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Canonical product merge:** `1666ba8c135ee8575f1546019ab592db32947dd2`  
**Program status:** `CLOSEOUT_024_CANDIDATE` when this documentation-only closeout becomes canonical  
**Last closed specification:** `specs/023-spec-kit-preset-compatible-import/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/024-native-workpacket-export/` — product delivered and post-product verified; final canonical closure still evidence-gated  
**Published release:** `v0.3.0`  
**Published release source:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Published release ID:** `378962445`

## Last canonical closed state

Specification 023 remains `CLOSED_CANONICAL`. Its bounded template-light Spec Kit import compatibility repair is unchanged.

The SGB-EXP-001 comparative experiment remains preserved as `INVALIDATED_ORACLE_REVEALED_PRE_FREEZE`; it produced no valid comparative result, supports no superiority claim, and selected no product work.

The bounded concurrent-writer race retained after Specification 022 remains an explicit residual outside Specification 024 authority.

## Specification 024 selection evidence

Selection evidence is recorded in:

`docs/research/post-023-workpacket-handoff-reproduction-2026-08-31.md`

Exact deterministic proof:

```text
canonical_base = f2e8378dcba0cfea2beedc6da61324b0c3fea95e
observation_head = 95e5358ed420cd2e6fbd0bc7c56690763cea1283
fixture_blob = 58cb3e355468f6bcd7de63b676dba52361ff0dd7
ci_run = 33416110142
ci_result = completed/success across all five permanent cells
```

That fixture proved the native handoff discontinuity: native authoring reached a dependency-eligible `GRAIN`, native CLI had no packet export, and the existing WorkPacket was available only through custom Python API glue.

## Canonical shaping proof

Specification 024 shaped only the read-only export boundary:

```text
specgrain packet <spec_id> [path] --context-sources <json-file> [--json]
```

Shaping head `043abdf8f15f688cdbae746c0abd83dda74d0dae` passed push CI `33416602621` and PR CI `33416635970`. PR #49 merged with expected-head protection as canonical shaping merge `440a8b14459ade2fe8235cc873229dd87ba926b5`; canonical post-shaping CI `33416908615` completed `success` across all five permanent cells before implementation began.

## Delivered Specification 024 boundary

Current source now exports the existing portable WorkPacket from one exact dependency-eligible stored `GRAIN`.

The command:

- requires exact `GRAIN` state and current dependency eligibility;
- accepts explicit bounded `ContextSource.to_dict()` JSON records only;
- rejects malformed, duplicate-key, non-finite, missing/unknown-field, invalid-source, duplicate-source-ID, symlink, non-file, oversized, and invalid-UTF-8 input;
- uses only the Grain's existing token budget through current context-budget primitives;
- constructs packets only through existing `build_work_packet` semantics;
- emits canonical JSON or a stable digest summary;
- does not mutate lifecycle, store, execution result, verification, or evidence state;
- adds no provider, executor, network, LLM, runtime dependency, or release authority.

## Product verification proof

Final implementation head:

`7e1db87f69108fc8693b987e77d20f92e4f46866`

Exact evidence:

- push CI `33421885016` — `completed/success` across all five permanent cells;
- PR CI `33422062846` — `completed/success` across all five permanent cells;
- Ubuntu/Python 3.11 on final push head — `592 passed`, then cleanliness, compile, source CLI smoke, package build, wheel reinstall, and installed CLI smoke all passed;
- PR #50 — no submitted reviews or inline review threads; Qodo billing-blocked, automatic CodeRabbit review skipped by repository-star policy, Cubic descriptive only;
- expected-head product merge — `1666ba8c135ee8575f1546019ab592db32947dd2`;
- canonical post-product CI `33422235433` — `completed/success` across all five permanent cells.

Historical `v0.3.0` remains unchanged at source `70dd66aba0e68ae710e6ef12605ed153d107bab4`, Release `378962445`, wheel digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`, and source digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

## Current execution gate

Specification 024 is now at documentation-only closeout.

Product work is complete and no further product mutation is authorized under 024. The only eligible dependent work is:

1. verify this exact closeout head changes only authorized documentation/governance/evidence paths;
2. require permanent five-cell push and PR CI on the exact head;
3. inspect reviews, inline threads, mergeability, and review-system availability without false PASS claims;
4. merge the closeout PR with expected-head protection;
5. require canonical post-closeout five-cell CI;
6. re-verify historical `v0.3.0` identity;
7. publish a final documentation-only evidence reconciliation that records those exact facts and only then marks Specification 024 `CLOSED_CANONICAL`.

## Explicitly unselected

Specification 024 does not authorize:

- `GRAIN -> READY` or later lifecycle mutation;
- executor/provider invocation;
- `ExecutionResult` creation or ingestion;
- verification execution or evidence mutation;
- automatic source discovery, source-content packing, retrieval, network access, or LLM context selection;
- SpecNode, WorkPacket, or ContextSource contract version redesign;
- stronger multi-writer locking/recovery;
- Spec Kit runtime integration;
- release publication;
- hosted/account/dashboard scope;
- empirical benchmark superiority claims.

## Next frontier discipline

No successor product specification is selected by Specification 024 closeout. After final canonical closure, return to observation/evidence gathering. Shape another specification only if fresh reproducible evidence against live canonical truth independently selects a bounded product gap.
