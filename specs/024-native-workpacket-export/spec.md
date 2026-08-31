# Specification 024 — Native WorkPacket Export

## Status

`CLOSEOUT_CANDIDATE`

Canonical shaping and product implementation are complete. Specification 024 becomes `CLOSED_CANONICAL` only after documentation-only closeout, canonical post-closeout CI, historical release re-verification, and final evidence reconciliation are proven and merged.

## Outcome

Allow a CLI user to export the existing deterministic `WorkPacket` contract from one dependency-eligible stored `GRAIN` without leaving the native SpecGrain command surface and without introducing execution, verification, lifecycle, provider, or evidence-mutation authority.

## Selection evidence

Specification 024 was selected from the deterministic post-023 reproduction recorded in:

`docs/research/post-023-workpacket-handoff-reproduction-2026-08-31.md`

Exact observation evidence:

```text
canonical_base = f2e8378dcba0cfea2beedc6da61324b0c3fea95e
observation_head = 95e5358ed420cd2e6fbd0bc7c56690763cea1283
fixture_blob = 58cb3e355468f6bcd7de63b676dba52361ff0dd7
ci_run = 33416110142
ci_result = completed/success across all five permanent cells
```

The fixture proved that native CLI reached a dependency-eligible `GRAIN`, native CLI had no `packet` command, and the same Grain could be converted into the existing portable WorkPacket only through custom Python API glue.

## Delivered behavior

Current source now provides:

```text
specgrain packet <spec_id> [path] --context-sources <json-file> [--json]
```

The command:

1. loads repository-local SpecGrain state without mutation;
2. requires a canonical `<spec_id>` that exists exactly once and is stored in exact `GRAIN` state;
3. requires a valid dependency graph and membership in the current native `next` eligible set;
4. accepts one bounded regular non-symlink UTF-8 JSON file whose top-level value is an array;
5. accepts exactly the existing `ContextSource.to_dict()` fields: `source_id`, `provenance`, `selection_reason`, `revision`, `size_bytes`, `token_cost`, `requirement`, and `priority`;
6. rejects duplicate JSON keys, malformed JSON, non-finite numeric tokens, missing/unknown fields, invalid ContextSource values, duplicate `source_id` values, non-files, symlinks, invalid UTF-8, and input above the documented `1048576`-byte limit;
7. derives only `ContextBudgetPolicy(max_tokens=node.context["budget_tokens"])` and reuses existing deterministic context-budget semantics;
8. calls the existing `build_work_packet` primitive rather than duplicating WorkPacket normalization or digest logic;
9. leaves builder-only `decisions`, `assumptions`, and `minimality_evidence` empty;
10. emits canonical `WorkPacket.to_json()` plus a terminal newline in JSON mode, or a stable text summary containing spec ID, semantic revision, context-plan digest, and packet digest;
11. does not read source content named by provenance, discover context, fetch network content, call an LLM/provider/executor, run verification, create/ingest an ExecutionResult, mutate evidence, or advance lifecycle state.

## Acceptance proof

Final implementation head:

`7e1db87f69108fc8693b987e77d20f92e4f46866`

Exact push CI `33421885016` and PR CI `33422062846` completed `success` across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11.

Ubuntu/Python 3.11 on the final push head recorded `592 passed`, followed by successful tracked-tree cleanliness, compile, source CLI smoke, package build, built-wheel reinstall with `--no-deps`, and installed CLI smoke.

Focused/full evidence proves:

- eligible `GRAIN` native export;
- `WorkPacket.from_dict` digest validation;
- exact API/CLI canonical JSON equality;
- deterministic source-order canonicalization;
- successful and failed command non-mutation;
- wrong-state, missing/noncanonical target, dependency-ineligible, and invalid dependency-graph failures;
- malformed/duplicate/non-finite JSON and strict source-schema failures;
- duplicate source-ID and required-token-budget failures;
- existing optional-source selection semantics;
- symlink/non-file/oversized/invalid-UTF-8 failures;
- stable text and canonical JSON output;
- source and installed CLI command exposure.

PR #50 merged with expected-head protection as canonical product merge `1666ba8c135ee8575f1546019ab592db32947dd2`. Canonical post-product CI `33422235433` completed `success` across the permanent five-cell matrix.

## Review evidence

PR #50 had no submitted reviews and no inline review threads. Qodo was billing-blocked, automatic CodeRabbit review was skipped by repository-star policy, and Cubic supplied descriptive summary text only. None was treated as independent approval or PASS.

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

No new ADR was required because the implementation exposes existing public contracts through a bounded CLI adapter rather than creating a new architectural authority boundary.

## Historical release preservation

After product merge, live GitHub truth remains:

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
- automatic source discovery, file-content packing, retrieval, network access, or LLM context selection;
- SpecNode, WorkPacket, or ContextSource schema/version redesign;
- stronger multi-writer locking or recovery changes;
- Spec Kit runtime integration;
- package versioning or release publication;
- hosted/account/dashboard scope;
- any benchmark superiority claim.

## Residual boundaries

The bounded concurrent-writer race retained after Specification 022 remains outside this specification.

A later native executor/result/verification workflow remains separately shapeable only from fresh reproducible evidence after this export boundary is observed in actual use. Specification 024 does not pre-build that authority.

## Remaining closure gate

This closeout candidate must pass documentation-only exact-head push/PR CI and review/mergeability checks, merge with expected-head protection, then pass canonical post-closeout five-cell CI and historical release re-verification. A final documentation-only evidence reconciliation may then publish `CLOSED_CANONICAL` and return the program to observation/evidence gathering if no fresh successor evidence exists.
