# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Canonical product merge:** `1666ba8c135ee8575f1546019ab592db32947dd2`  
**Canonical Specification 024 closeout merge:** `519680c5cf378dfcb4673cf7292bcf51e9c36af1`  
**Canonical Specification 024 closure reconciliation merge:** `326e013836814bd3566d1da8887fd028981a8cec`  
**Canonical post-024 normalization merge:** `101f018095868fc011c4ebea15dcac64f64d1061`  
**Canonical post-normalization CI:** `33427947122` — `completed/success` across all five permanent cells  
**Program status:** `SPEC_025_SHAPING`  
**Last closed specification:** `specs/024-native-workpacket-export/` — `CLOSED_CANONICAL`  
**Active specification:** `specs/025-supported-pregrain-writer-serialization/` — `SHAPED` candidate  
**Product implementation:** blocked until the Specification 025 shaping package is canonical and canonical post-shaping CI succeeds  
**Published release:** `v0.3.0`  
**Published release source:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Published release ID:** `378962445`

## Canonical closed frontier

Specification 024 delivered one bounded read-only native WorkPacket export surface:

```text
specgrain packet <spec_id> [path] --context-sources <json-file> [--json]
```

It requires an exact dependency-eligible stored `GRAIN`, explicit bounded `ContextSource.to_dict()` JSON records, the Grain's existing token budget, current context-budget primitives, and existing `build_work_packet` semantics. It does not advance lifecycle state, invoke an executor/provider, ingest execution results, run verification, mutate evidence, discover context automatically, fetch network content, select an LLM, change contract versions, publish a release, or authorize hosted scope.

The SGB-EXP-001 comparative experiment remains preserved as `INVALIDATED_ORACLE_REVEALED_PRE_FREEZE`; it produced no valid comparative result, supports no superiority claim, and selected no product work.

## Specification 024 closure proof

Selection:

```text
canonical_base = f2e8378dcba0cfea2beedc6da61324b0c3fea95e
observation_head = 95e5358ed420cd2e6fbd0bc7c56690763cea1283
fixture_blob = 58cb3e355468f6bcd7de63b676dba52361ff0dd7
ci_run = 33416110142
ci_result = completed/success across all five permanent cells
```

Shaping:

- exact shaping head `043abdf8f15f688cdbae746c0abd83dda74d0dae`;
- push CI `33416602621` and PR CI `33416635970` — `completed/success` across all five permanent cells;
- PR #49 expected-head merge `440a8b14459ade2fe8235cc873229dd87ba926b5`;
- canonical post-shaping CI `33416908615` — `completed/success` across all five permanent cells.

Product:

- final implementation head `7e1db87f69108fc8693b987e77d20f92e4f46866`;
- push CI `33421885016` and PR CI `33422062846` — `completed/success` across all five permanent cells;
- Ubuntu/Python 3.11 final push evidence — `592 passed` plus cleanliness, compile, source CLI smoke, package build, wheel reinstall, and installed CLI smoke;
- PR #50 expected-head product merge `1666ba8c135ee8575f1546019ab592db32947dd2`;
- canonical post-product CI `33422235433` — `completed/success` across all five permanent cells.

Closeout and reconciliation:

- exact closeout head `12f89e22955efc632f62d52f2f0396430f4bee01`;
- closeout push CI `33422814705` and PR #51 CI `33422950629` — success across five cells;
- PR #51 expected-head closeout merge `519680c5cf378dfcb4673cf7292bcf51e9c36af1`;
- canonical post-closeout CI `33423123321` — success across five cells;
- exact reconciliation head `e6ac770c191289ff3ddc58789c87d7a97e1c6178`;
- reconciliation push CI `33425082595` and PR #52 CI `33425201892` — success across five cells;
- PR #52 expected-head merge `326e013836814bd3566d1da8887fd028981a8cec`;
- canonical post-reconciliation CI `33425454115` — success across five cells;
- final post-024 normalization PR #53 exact head `6cd40b122021d6a4ca361d613cc88fd389cebc0f`;
- PR #53 push CI `33427600665` and PR CI `33427745392` — success across five cells;
- PR #53 expected-head merge `101f018095868fc011c4ebea15dcac64f64d1061`;
- canonical post-normalization CI `33427947122` — success across five cells.

No unavailable or skipped review system was treated as PASS at any merge gate. Qodo was billing-blocked, automatic CodeRabbit review was skipped by repository-star policy, and Cubic was descriptive only where those systems appeared.

Historical `v0.3.0` remains unchanged at source `70dd66aba0e68ae710e6ef12605ed153d107bab4`, Release `378962445`, wheel asset `535129008` / digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`, and source asset `535129009` / digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

## Fresh post-024 selection evidence

The previously retained bounded multi-writer residual has now been reproduced using two supported public pre-Grain mutation calls.

Exact final evidence:

```text
canonical_base = 101f018095868fc011c4ebea15dcac64f64d1061
observation_branch = obs/025-multi-writer-parent-replace-fixture
observation_head = 58174dbc87e9c02ebbb3a19d38727e1f42149226
fixture = tests/test_post_024_multi_writer_observation.py
fixture_blob = b0852096a6f8916955a6a31b3a785ca8bb0d708d
ci_run = 33431133156
ci_result = completed/success across all five permanent cells
reproduced_gap = SUPPORTED_PRE_GRAIN_MULTI_WRITER_LOST_UPDATE
```

The fixture proves that writer A and writer B can both use `shape_draft_spec`, both return success with distinct semantic revisions, and writer A can then silently overwrite writer B's already-confirmed successful postimage because the final exact-preimage check and `os.replace` are separate operations.

The selection record is:

`docs/research/post-024-supported-pregrain-multi-writer-reproduction-2026-08-31.md`

The architectural decision is:

`docs/adr/0020-supported-pregrain-writer-serialization.md`

## Active Specification 025 boundary

Specification 025 shapes only cooperative, non-blocking serialization of the existing `src/specgrain/pregrain.py::_persist` persistence-critical section.

The intended guarantee is:

```text
one active supported pre-Grain persistence transaction per project
```

A competing supported pre-Grain persistence call fails closed immediately on active contention rather than waiting, retrying, or racing.

The candidate uses one inert runtime anchor:

```text
.specgrain/tmp/pregrain-mutation.lock
```

with conditional Python standard-library advisory-lock primitives on Unix-family and Windows runners. Lock-file presence alone is never transaction ownership or recovery state.

The current exact-preimage, temp-file fsync, atomic replacement, postimage confirmation, lifecycle, dependency, readiness, and semantic-digest contracts remain authoritative.

## Explicitly unselected under Specification 025

No current authority exists for:

- coordination with arbitrary manual/non-SpecGrain writers;
- general project-wide locking of unrelated mutations;
- child-authoring journal/recovery redesign;
- distributed/network locking;
- blocking waits, retries, leases, heartbeats, or timeout ownership inference;
- new runtime dependencies;
- `GRAIN -> READY` or later lifecycle mutation;
- executor/provider invocation or result orchestration;
- verification execution or evidence mutation;
- automatic source discovery, source-content packing, retrieval, network access, or LLM context selection;
- SpecNode, WorkPacket, or ContextSource contract version redesign;
- Spec Kit runtime integration or architectural adoption;
- PyPI publication or broader distribution changes;
- hosted/account/dashboard/enterprise scope;
- empirical benchmark superiority claims.

## Current execution gate

Specification 025 is a documentation-only `SHAPED` candidate on its shaping branch.

Product implementation remains blocked until all of the following are proven on the exact shaping head:

1. only authorized research/ADR/specification/governance paths changed;
2. permanent five-cell CI succeeds;
3. reviews, inline threads, mergeability, and exact head/base are rechecked without treating unavailable review systems as PASS;
4. the shaping PR merges with expected-head protection;
5. canonical post-shaping CI succeeds on the resulting `main`.

Only then may `feat/025-supported-pregrain-writer-serialization` begin.

## Next frontier discipline

Do not widen Specification 025 merely because adjacent concurrency work is visible. After Specification 025 closes, return to observation/evidence gathering and shape any later successor only from fresh reproducible evidence against live canonical truth.
