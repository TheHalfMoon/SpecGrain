# Plan 024 — Native WorkPacket Export

## Objective

Close the reproduced native handoff discontinuity with the smallest possible adapter: expose the existing deterministic WorkPacket builder through one read-only CLI command for an already dependency-eligible `GRAIN`.

## Canonical shaping base

```text
f2e8378dcba0cfea2beedc6da61324b0c3fea95e
```

Selection evidence is fixed to observation head `95e5358ed420cd2e6fbd0bc7c56690763cea1283` and successful permanent CI run `33416110142`.

Implementation MUST NOT begin until the shaping PR is merged with expected-head protection and the resulting canonical `main` passes the permanent five-cell CI matrix.

Planned implementation branch after that gate:

```text
feat/024-native-workpacket-export
```

## Change strategy

### 1. Keep the product boundary read-only

Add only the native export command:

```text
specgrain packet <spec_id> [path] --context-sources <json-file> [--json]
```

The command loads and validates current project state. It does not persist any lifecycle, WorkPacket, result, verification, or evidence record.

### 2. Gate export on existing native eligibility

Reuse `load_project` and `next_project` rather than invent another dependency gate.

Before packet construction:

- validate canonical spec ID;
- require the stored node to exist and be exactly `GRAIN`;
- require `next_project(root)` to be valid;
- require the target ID in `eligible_ids`.

Do not call a lifecycle transition and do not reinterpret GRAIN readiness on a post-promotion node.

### 3. Parse a bounded explicit ContextSource file

Implement a private CLI parser for `--context-sources`.

The parser should:

- reject symlinks and non-regular files;
- enforce a small fixed maximum byte size before decoding;
- decode UTF-8 strictly;
- parse JSON with duplicate-key rejection and non-finite-number rejection;
- require a top-level array;
- require each item to have exactly the eight `ContextSource.to_dict()` fields;
- instantiate the existing `ContextSource` type so canonical field validation remains centralized;
- pass the materialized sequence through existing context validation/budget logic, which also rejects duplicate source IDs and canonicalizes source order.

Do not add a new public input schema, runtime dependency, source fetcher, or content loader.

### 4. Reuse the Grain's existing context token ceiling

Construct exactly:

```text
ContextBudgetPolicy(max_tokens=node.context["budget_tokens"])
```

Then call `require_context_budget` with the explicit sources.

No new `max_bytes` or `max_sources` semantics are added to the SpecNode contract. The file byte limit protects the CLI input surface only; it is not a new context-planning semantic.

### 5. Reuse `build_work_packet`

Call the existing public builder with:

```text
build_work_packet(node, sources, context_report)
```

Do not duplicate WorkPacket serialization, normalization, source binding, or digest calculation. Leave decisions, assumptions, and minimality evidence at their existing empty defaults in this CLI version.

### 6. Stable output

For `--json`, write only `packet.to_json()` plus one terminal newline to stdout.

For text mode, emit a stable summary with:

```text
SpecGrain packet: EXPORTED
Spec: <id>
Revision: <sha256:...>
Context plan: <sha256:...>
Packet: <sha256:...>
```

Errors follow existing CLI conventions and go to stderr with non-zero status.

### 7. Focused proof

Create focused CLI tests covering:

- valid export;
- exact API/CLI payload equality;
- deterministic reordered-source input;
- byte-identical store before/after successful export;
- byte-identical store after every representative failure;
- wrong state;
- invalid project/dependency state;
- dependency-ineligible Grain;
- missing target;
- malformed JSON;
- duplicate JSON key;
- non-finite numeric token;
- non-array root;
- missing/unknown source fields;
- invalid ContextSource field values;
- duplicate source IDs;
- required token-budget overflow;
- symlink input where supported by the test platform;
- non-file input;
- oversized input;
- text output;
- JSON output;
- source and installed CLI `packet --help` smoke.

### 8. Documentation

Update current-source command documentation to explain that `packet` exports a portable WorkPacket only. It does not execute it or advance lifecycle state.

Historical `v0.3.0` command/release claims remain untouched.

## Expected product implementation surface

```text
src/specgrain/cli.py
tests/test_workpacket_cli.py
README.md
```

A product path outside this surface requires explicit review against Specification 024 authority before merge.

Documentation-only closeout may later update:

```text
specs/024-native-workpacket-export/tasks.md
specs/024-native-workpacket-export/verification.md
specs/024-native-workpacket-export/review.md
specs/024-native-workpacket-export/spec.md
specs/CURRENT.md
docs/execution-master-plan.md
docs/roadmap.md
```

The selection evidence document remains immutable unless a factual correction is required.

## Verification order

1. focused `tests/test_workpacket_cli.py`;
2. full pytest regression;
3. Ruff over `src`, `tests`, and `examples`;
4. tracked-tree cleanliness after tests;
5. compileall;
6. source CLI smoke including `specgrain packet --help`;
7. package build;
8. built-wheel reinstall with `--no-deps`;
9. installed CLI smoke including `specgrain packet --help`;
10. exact shaped-base-to-head diff review;
11. permanent five-cell CI on exact implementation head;
12. review comments/threads and review-system availability recheck without treating unavailable systems as PASS;
13. expected-head product merge;
14. canonical post-product CI;
15. historical `v0.3.0` preservation check;
16. documentation-only closeout;
17. exact-head closeout CI/review/expected-head merge;
18. canonical post-closeout CI and final governance re-read.

## Non-goals

No READY mutation, executor/provider orchestration, result ingestion, verification execution, evidence mutation, automatic context discovery, source-content bundling, network access, LLM selection, SpecNode schema change, WorkPacket/context version change, multi-writer locking, Spec Kit runtime integration, release publication, or hosted product scope.