# Post-023 WorkPacket Handoff Reproduction — 2026-08-31

## Purpose

Determine whether live canonical SpecGrain has a bounded native handoff gap after `GRAIN`, without using the invalidated SGB-EXP-001 benchmark and without authorizing execution, verification mutation, or a product successor by assertion alone.

## Canonical baseline

```text
repository = TheHalfMoon/SpecGrain
canonical_main = f2e8378dcba0cfea2beedc6da61324b0c3fea95e
program_state = POST_023_OBSERVATION
active_product_specification = none
published_release = v0.3.0
```

The post-023 review permits a successor shaping cycle when fresh reproducible evidence includes a deterministic interoperability fixture showing that a bounded portable handoff cannot be expressed through the current native surface without unsafe or duplicative glue.

## Observation fixture

A test-only observation branch was created directly from the canonical baseline:

```text
branch = obs/024-workpacket-handoff-fixture
final_observation_head = 95e5358ed420cd2e6fbd0bc7c56690763cea1283
fixture = tests/test_post_023_workpacket_handoff_observation.py
fixture_blob = 58cb3e355468f6bcd7de63b676dba52361ff0dd7
```

Earlier observation heads on that branch are superseded and are not evidence for this conclusion.

The final fixture performs one isolated deterministic flow:

```text
init
-> draft
-> shape
-> refine
-> grain
-> next --json
```

The resulting `SG-000001` is stored in `GRAIN`, and `next --json` reports it in the native `eligible` set.

The fixture then attempts the natural native handoff command:

```text
specgrain packet SG-000001 <workspace> --json
```

The current CLI rejects `packet` at argument parsing with exit code `2` because no such command exists.

The same fixture then leaves the CLI and uses the already-public Python API:

```text
load_project
ContextSource
ContextBudgetPolicy
require_context_budget
build_work_packet
WorkPacket.to_json
```

That API path succeeds and produces a portable digest-bound WorkPacket for the exact same stored Grain.

## Machine-run evidence

GitHub Actions run:

```text
run_id = 33416110142
head = 95e5358ed420cd2e6fbd0bc7c56690763cea1283
workflow = CI
status = completed
conclusion = success
```

All permanent cells completed successfully:

```text
ubuntu-latest / Python 3.11 = success
ubuntu-latest / Python 3.12 = success
ubuntu-latest / Python 3.13 = success
macos-latest / Python 3.11 = success
windows-latest / Python 3.11 = success
```

The workflow also passed Ruff over source/tests/examples, the full regression suite, tracked-tree cleanliness, compileall, source CLI smoke, package build, built-wheel installation, and installed CLI smoke.

## Reproduced gap

The observed gap is narrower than executor orchestration:

1. native authoring reaches an eligible `GRAIN`;
2. the repository already contains the deterministic portable `WorkPacket` contract;
3. the public Python API can construct that packet;
4. the native CLI cannot export it;
5. therefore a CLI user must switch to custom Python glue and manually assemble existing public context-accounting objects at the exact `GRAIN -> external implementation` handoff.

This is a deterministic interoperability discontinuity, not a benchmark score or agent-quality claim.

## Smallest justified product boundary

The evidence justifies shaping only a read-only native WorkPacket export surface that reuses the existing contracts.

Candidate boundary:

- accept one existing dependency-eligible `GRAIN`;
- accept explicit context-source records rather than infer context;
- apply the Grain's existing token budget through the existing context-budget primitive;
- call the existing `build_work_packet` primitive;
- emit the resulting WorkPacket without mutating lifecycle or evidence state.

The evidence does **not** justify:

- `GRAIN -> READY` or any later lifecycle mutation;
- executor/provider invocation;
- `ExecutionResult` ingestion;
- verification execution or evidence mutation;
- automatic context discovery or LLM-assisted context selection;
- stronger multi-writer locking;
- release publication;
- benchmark superiority claims.

## Selection conclusion

The post-023 deterministic-interoperability criterion is satisfied by exact machine-run evidence.

```text
BOUNDED_PRODUCT_GAP = NATIVE_WORKPACKET_EXPORT_MISSING
SUCCESSOR_SHAPING_JUSTIFIED = true
IMPLEMENTATION_AUTHORIZED = false
```

A Specification 024 shaping candidate may therefore be created. Product implementation remains blocked until that documentation-only shaping package is merged canonically and the resulting `main` passes the permanent CI matrix.