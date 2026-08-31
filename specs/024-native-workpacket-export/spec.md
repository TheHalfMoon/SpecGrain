# Specification 024 — Native WorkPacket Export

## Status

`CLOSED_CANONICAL` when this final evidence reconciliation is canonical.

All shaping, product, closeout, review-availability, permanent CI, merge, and historical-release-preservation gates are proven from live GitHub truth. This reconciliation changes documentation only.

## Outcome

Allow a CLI user to export the existing deterministic `WorkPacket` contract from one dependency-eligible stored `GRAIN` without leaving the native SpecGrain command surface and without introducing execution, verification, lifecycle, provider, or evidence-mutation authority.

## Selection evidence

Specification 024 was selected from the deterministic post-023 reproduction recorded in `docs/research/post-023-workpacket-handoff-reproduction-2026-08-31.md`:

```text
canonical_base = f2e8378dcba0cfea2beedc6da61324b0c3fea95e
observation_head = 95e5358ed420cd2e6fbd0bc7c56690763cea1283
fixture_blob = 58cb3e355468f6bcd7de63b676dba52361ff0dd7
ci_run = 33416110142
ci_result = completed/success across all five permanent cells
```

The fixture proved that native CLI reached a dependency-eligible `GRAIN`, native CLI lacked a `packet` command, and the same Grain could be converted into the existing portable WorkPacket only through custom Python API glue.

## Delivered behavior

Current source provides:

```text
specgrain packet <spec_id> [path] --context-sources <json-file> [--json]
```

The command:

1. loads repository-local SpecGrain state without mutation;
2. requires a canonical target that exists exactly once and is stored in exact `GRAIN` state;
3. requires a valid dependency graph and current native dependency eligibility;
4. accepts one bounded regular non-symlink UTF-8 JSON array containing exactly the existing `ContextSource.to_dict()` fields;
5. rejects duplicate JSON keys, malformed JSON, non-finite numeric tokens, missing/unknown fields, invalid ContextSource values, duplicate source IDs, non-files, symlinks, invalid UTF-8, and input above `1048576` bytes;
6. derives only `ContextBudgetPolicy(max_tokens=node.context["budget_tokens"])` and reuses existing deterministic context-budget semantics;
7. constructs output only through the existing `build_work_packet` primitive;
8. keeps `decisions`, `assumptions`, and `minimality_evidence` empty;
9. emits canonical `WorkPacket.to_json()` plus one terminal newline in JSON mode or a stable text summary containing spec ID, semantic revision, context-plan digest, and packet digest;
10. does not read source content named by provenance, discover context, fetch network content, call an LLM/provider/executor, run verification, create or ingest an ExecutionResult, mutate evidence, or advance lifecycle state.

## Canonical evidence

Shaping:

- head `043abdf8f15f688cdbae746c0abd83dda74d0dae`;
- push CI `33416602621` and PR CI `33416635970` — success across five cells;
- PR #49 expected-head merge `440a8b14459ade2fe8235cc873229dd87ba926b5`;
- post-shaping CI `33416908615` — success across five cells.

Product:

- final implementation head `7e1db87f69108fc8693b987e77d20f92e4f46866`;
- push CI `33421885016` and PR CI `33422062846` — success across five cells;
- Ubuntu/Python 3.11 final push — `592 passed` plus cleanliness, compile, source CLI smoke, build, wheel reinstall, and installed CLI smoke;
- PR #50 expected-head merge `1666ba8c135ee8575f1546019ab592db32947dd2`;
- post-product CI `33422235433` — success across five cells.

Closeout:

- exact documentation-only head `12f89e22955efc632f62d52f2f0396430f4bee01`;
- push CI `33422814705` and PR CI `33422950629` — success across five cells;
- PR #51 had no submitted reviews or inline review threads and was mergeable before merge;
- Qodo billing-blocked, automatic CodeRabbit skipped by repository-star policy, Cubic descriptive only; none treated as PASS;
- PR #51 expected-head merge `519680c5cf378dfcb4673cf7292bcf51e9c36af1` with exact parent `1666ba8c135ee8575f1546019ab592db32947dd2`;
- post-closeout CI `33423123321` — success across five cells.

Superseded implementation failures remain recorded in `verification.md`; they were corrected before the final product head without weakening invariants.

## Existing contracts retained

Specification 024 preserves:

- `WORK_PACKET_VERSION`;
- `ContextSource` validation semantics;
- context-plan digest semantics;
- WorkPacket normalization and packet digest semantics;
- dependency eligibility semantics;
- lifecycle state graph;
- verification/evidence contracts;
- zero runtime third-party dependencies.

No new ADR was required because this work exposes existing public contracts through a bounded CLI adapter rather than creating a new architectural authority boundary.

## Historical release preservation

After closeout, live GitHub truth remains:

- `v0.3.0` -> `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release `378962445`, target `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- wheel asset `535129008`, size `70463`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset `535129009`, size `104057`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

`packet` remains a current-source addition and is not attributed to the historical v0.3.0 command surface.

## Explicitly out of scope

Specification 024 does not authorize:

- `GRAIN -> READY` or later lifecycle transitions;
- executor/provider selection or invocation;
- `ExecutionResult` creation or ingestion;
- verification execution or evidence-record mutation;
- automatic source discovery, source-content packing, retrieval, network access, or LLM context selection;
- SpecNode, WorkPacket, or ContextSource schema/version redesign;
- stronger multi-writer locking or recovery changes;
- Spec Kit runtime integration;
- package versioning or release publication;
- hosted/account/dashboard scope;
- any benchmark superiority claim.

## Residual boundaries and next frontier

The bounded concurrent-writer race retained after Specification 022 remains outside this specification.

A later native executor/result/verification workflow remains separately shapeable only from fresh reproducible evidence. Specification 024 does not pre-build that authority.

When this reconciliation is canonical, Specification 024 is closed and there is no active successor specification. The program returns to observation/evidence gathering.
