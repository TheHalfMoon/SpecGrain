# Specification 024 — Native WorkPacket Export

## Status

`SHAPED` candidate. Product implementation is blocked until this documentation-only shaping package is merged canonically and the resulting `main` passes the permanent five-cell CI matrix.

## Outcome

Allow a CLI user to export the existing deterministic `WorkPacket` contract from one dependency-eligible stored `GRAIN` without leaving the native SpecGrain command surface and without introducing execution, verification, lifecycle, provider, or evidence-mutation authority.

## Selection evidence

Specification 024 is selected from the deterministic post-023 reproduction recorded in:

`docs/research/post-023-workpacket-handoff-reproduction-2026-08-31.md`

Exact observation evidence:

```text
canonical_base = f2e8378dcba0cfea2beedc6da61324b0c3fea95e
observation_head = 95e5358ed420cd2e6fbd0bc7c56690763cea1283
fixture_blob = 58cb3e355468f6bcd7de63b676dba52361ff0dd7
ci_run = 33416110142
ci_result = success across all five permanent cells
```

The fixture proves that current native CLI flow reaches an eligible `GRAIN`, current CLI has no `packet` command, and the same Grain can be converted into the existing portable WorkPacket only after switching to custom Python API glue.

## Required behavior

### 1. Add one bounded read-only command

Add:

```text
specgrain packet <spec_id> [path] --context-sources <json-file> [--json]
```

The command MUST NOT mutate `.specgrain/`, product files, verification evidence, or lifecycle state.

### 2. Require the exact existing Grain boundary

The command MUST fail closed unless:

- the repository-local project loads successfully;
- `<spec_id>` exists exactly once;
- the stored node state is exactly `GRAIN`;
- the dependency graph is valid;
- the target Grain is present in the current native `next` eligible set.

The command MUST NOT promote the node to `READY` or any later state.

### 3. Accept explicit context-source records only

`--context-sources` MUST point to one bounded UTF-8 JSON file whose top-level value is an array.

Each array item MUST contain exactly the existing `ContextSource.to_dict()` fields:

```text
source_id
provenance
selection_reason
revision
size_bytes
token_cost
requirement
priority
```

No additional fields are accepted. Missing fields, duplicate object keys, malformed JSON, non-finite numeric tokens, invalid `ContextSource` values, duplicate `source_id` values, symlink input, non-regular-file input, or input above the implementation's documented bounded byte limit MUST fail closed.

The command MUST NOT read source content named by provenance, fetch network content, discover context automatically, or infer context with an LLM.

### 4. Reuse current context-budget semantics

The command MUST derive only the token ceiling already stored on the Grain:

```text
ContextBudgetPolicy(max_tokens=node.context["budget_tokens"])
```

It MUST pass the explicit context-source records through the existing deterministic context-budget implementation and reject required-context budget failures.

Specification 024 does not add byte/source-count policy semantics to `SpecNode` and does not infer that selected context is semantically sufficient beyond the existing contracts.

### 5. Reuse the existing WorkPacket contract

After the gates above pass, the command MUST call the existing `build_work_packet` primitive rather than duplicate WorkPacket normalization or digest rules.

Specification 024 v1 export leaves optional builder-only annotations empty:

```text
decisions = ()
assumptions = ()
minimality_evidence = ()
```

No CLI inference or hidden default content may be inserted into those fields.

### 6. Preserve deterministic portable output

With `--json`, stdout MUST be the canonical portable WorkPacket JSON produced by the existing `WorkPacket.to_json()` contract, followed only by the CLI's normal terminal newline.

Without `--json`, stdout MUST provide a stable human-readable export summary containing at minimum:

- spec ID;
- exact semantic spec revision;
- context-plan digest;
- WorkPacket digest.

The same valid inputs over byte-identical project/context records MUST produce the same packet digest and JSON payload on every supported platform.

### 7. Fail closed without side effects

Every command failure MUST leave the repository-local store byte-identical to its pre-command state.

JSON-mode failures MUST follow the current CLI fail-closed machine-readable error convention. Text-mode failures MUST use the current stderr convention and non-zero exit status.

## Acceptance proof required

Implementation must prove at minimum:

1. an eligible `GRAIN` exports a WorkPacket through the native CLI;
2. exported JSON parses through `WorkPacket.from_dict` and retains the declared digest;
3. CLI output matches a WorkPacket constructed through the existing public API from the same node, sources, and budget;
4. repeated export is deterministic and non-mutating;
5. source records are canonicalized according to the existing context-budget rules regardless of JSON array order;
6. wrong lifecycle state fails;
7. dependency-ineligible Grain fails;
8. malformed/duplicate/unknown/missing context input fails;
9. duplicate `source_id` fails;
10. required context exceeding the Grain token budget fails;
11. symlink/non-file/oversized context input fails;
12. no network/provider/executor/verification action occurs;
13. full permanent cross-platform CI remains green;
14. historical `v0.3.0` release identity remains unchanged.

## Existing contracts retained

Specification 024 MUST preserve:

- `WORK_PACKET_VERSION`;
- `ContextSource` validation semantics;
- context-plan digest semantics;
- WorkPacket normalization and packet digest semantics;
- dependency eligibility semantics;
- lifecycle state graph;
- verification/evidence contracts;
- zero runtime dependencies unless a separate shaped change demonstrates necessity.

No new ADR is required by this shaping candidate because the implementation is constrained to expose existing API contracts through a bounded CLI adapter rather than introduce a new architectural authority boundary.

## Explicitly out of scope

Specification 024 does not authorize:

- `GRAIN -> READY` or later lifecycle transitions;
- executor or provider selection/invocation;
- `ExecutionResult` creation or ingestion;
- verification execution;
- evidence-record mutation;
- automatic source discovery, file-content packing, retrieval, network access, or LLM context selection;
- changes to the SpecNode schema;
- changes to WorkPacket or context contract versions;
- stronger multi-writer locking or recovery changes;
- Spec Kit runtime integration;
- package versioning or release publication;
- hosted/account/dashboard scope;
- any benchmark superiority claim.

## Residual boundaries

The bounded concurrent-writer race retained after Specification 022 remains outside this specification.

A later native executor/result/verification workflow remains separately shapeable only from fresh evidence after this export boundary is proven in actual use. Specification 024 must not pre-build that later authority.