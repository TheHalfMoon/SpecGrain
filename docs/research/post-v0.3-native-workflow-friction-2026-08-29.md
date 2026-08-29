# Post-v0.3 Native Workflow Friction Audit — 2026-08-29

**Audit source revision:** `3b98914200c68909f09db08642faf56de48305eb`  
**Latest published release:** `v0.3.0`, GitHub Release `378962445`

## Evidence trigger

A maintainer-supplied external adversarial review exercised the public v0.3.0 CLI and identified the missing native path from authored DRAFTs into the deterministic Grain/readiness system as the most severe current adoption blocker. The review specifically observed that the quickstart can create DRAFT files but cannot complete readiness fields or advance lifecycle state without writing Python against the library or editing internal JSON.

This audit reproduces that finding against live canonical source rather than accepting the external conclusion on authority.

## Reproduced repository facts

At exact canonical `main` `3b98914200c68909f09db08642faf56de48305eb`:

- `specgrain draft` can create root and child SpecNodes only in state `DRAFT`;
- the public CLI exposes `init`, `draft`, `recover`, `check`, `next`, `scan`, `prove`, and `import-spec-kit`;
- there is no native CLI surface that populates acceptance, scope, risk/recovery, context, change-surface, evidence, or readiness metadata on an existing DRAFT;
- there is no native lifecycle command that advances `DRAFT -> SHAPED -> REFINING` or promotes a ready `REFINING` leaf to `GRAIN`;
- `check_project()` evaluates Grain readiness only for leaves already in state `REFINING`;
- `next_project()` considers only nodes already in state `GRAIN`;
- the README truthfully states that current `draft` authoring does not grant Grain/readiness/execution authority;
- the API example can reach VERIFIED, but the supported CLI cannot reach the pre-execution Grain boundary.

Therefore the public v0.3.0 path is structurally bounded but product-incomplete:

```text
init -> draft -> check
          |
          +-> no native path to SHAPED / REFINING / GRAIN
```

## Smallest evidence-supported frontier

The external review argues for a full DRAFT-to-VERIFIED workflow. That direction is valuable but too broad for one Grain because it would combine:

- semantic editing authority;
- lifecycle transition authority;
- Grain-readiness authorization;
- WorkPacket generation;
- executor/result handling;
- verification execution;
- evidence mutation.

The smallest coherent next step is instead to close the **pre-execution authoring dead end**:

```text
DRAFT -> SHAPED -> REFINING -> GRAIN
```

through bounded native commands, with `REFINING -> GRAIN` permitted only when the existing deterministic readiness evaluator passes the exact candidate revision.

This unlocks an actual user-visible result from the kernel without introducing agent/provider execution authority.

## Decision

Shape Specification 022 — Native Grain Preparation.

022 should:

- provide native single-node DRAFT shaping for the existing readiness fields;
- authorize only the structurally legal pre-execution transitions `DRAFT -> SHAPED`, `SHAPED -> REFINING`, and readiness-gated `REFINING -> GRAIN`;
- preserve immutable SpecNode construction, exact-preimage replacement, deterministic validation, and zero runtime dependencies;
- keep WorkPacket CLI, executor orchestration, verification execution, evidence mutation, automatic AI authoring, and provider integration out of scope.

The next frontier after 022 must be re-evaluated from canonical post-closeout truth. A WorkPacket/execution surface is not pre-authorized by this audit.
