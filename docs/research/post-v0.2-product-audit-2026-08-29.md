# Post-v0.2 Product Audit — 2026-08-29

**Audit source revision:** `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`  
**Published release inspected:** `v0.2.0`, GitHub Release `378936896`

## Purpose

This audit re-evaluates the smallest defensible product frontier after Specification 018 product merge and live v0.2.0 publication. It is evidence for later shaping only. It does not authorize a successor specification or implementation.

## Live repository and adoption snapshot

At audit time:

- canonical product `main` is `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`;
- canonical product post-merge CI run `33245753969` succeeded across Ubuntu 3.11/3.12/3.13, macOS 3.11, and Windows 3.11;
- release workflow run `33245783948` successfully published `v0.2.0` at that exact product merge;
- GitHub Release `378936896` is public and non-prerelease with exactly the expected wheel and source distribution;
- `v0.1.0` remains unchanged at its historical release source;
- there are no open issues or pull requests;
- GitHub reports zero stars and zero forks;
- both new v0.2.0 release assets report zero downloads immediately after publication;
- the repository remains less than two days old.

These popularity and download counts are an absence of adoption evidence, not evidence of product failure.

## Current usable authoring journey

The public v0.2.0 user can now run:

```text
init -> draft -> check
```

`draft` creates exactly one root SpecNode in `DRAFT`. The deterministic core already knows how to validate recursive forests, reciprocal parent/child declarations, missing relationships, self-links, and cycles. However, the supported local authoring surface cannot yet create a child SpecNode or safely update the reciprocal parent relationship.

The lifecycle core separately defines structural states and transitions but intentionally owns no mutation authority. Grain readiness requires a `REFINING` leaf with explicit scope, acceptance, risk/recovery, context, evidence, and readiness metadata. A successor must not collapse those separate authorities merely to make the CLI appear more complete.

## Candidate frontier comparison

| Candidate | User value now | Scope/risk | Existing leverage | Decision |
| --- | --- | --- | --- | --- |
| Native child-DRAFT authoring | High: makes the public recursive specification model directly usable beyond one root | Medium: explicit parent rewrite plus new-child creation must be atomic/fail-closed | Existing SpecNode schema, ID allocator pattern, refinement validator, local store | **Recommend shaping next** |
| Broad `refine` command with lifecycle progression | High eventually | High: would combine child creation, parent lifecycle mutation, semantic decomposition, and protected transition authority | Structural validator exists, but mutation authority does not | Defer; split from child authoring |
| Native DRAFT editing / SHAPED transition | High later | Medium/high: generic replacement semantics and lifecycle authorization need a separate contract | Immutable SpecNode model and transition graph exist | Reassess after child-authoring boundary or if evidence changes |
| PyPI publication | Medium installation convenience | Medium/external: trusted publishing, package identity, credentials, registry governance | Reusable release metadata now exists | Defer while public adoption evidence is absent and GitHub install is functional |
| WorkPacket/executor CLI | Medium later-stage value | Medium/high | Packet and adapter APIs already exist | Defer until first-party native authoring can express useful recursive work |
| Empirical benchmark program | Potential proof value | High/resource-sensitive | Benchmark harness exists | Defer: no controlled public comparative dataset or execution evidence |
| Hosted dashboard/provider orchestration | Premature | High/lock-in risk | No adoption signal demanding it | Defer |

## Recommended next shaping candidate

The smallest next candidate is **native child-DRAFT authoring**.

The intended product outcome for later shaping should be narrower than a generic lifecycle-aware `refine` command:

- select an existing parent by canonical SpecNode ID;
- create one new child fixed to `DRAFT` from explicit title/outcome/rationale input;
- add the new child ID to the parent's reciprocal `children` declaration;
- leave parent and child lifecycle states unchanged;
- validate the complete proposed refinement forest before publication of the mutation;
- persist the parent update and child creation as one fail-closed logical operation so a crash/collision does not intentionally expose a half-refined canonical forest;
- refuse overwrite, missing parent, invalid existing forest, cycles, ID collisions, and unsafe/symlinked store state;
- provide deterministic API/CLI output and tests;
- grant no `SHAPED`, `REFINING`, Grain, readiness, or execution authority.

The command name and exact persistence algorithm remain shaping decisions. Extending `draft` with an explicit parent option may be smaller than introducing a broad `refine` verb, but this audit does not decide the interface.

## Why not lifecycle progression yet

Specification 002 deliberately provides structural transition validation without mutation authority. Specification 003 deliberately validates refinement without lifecycle mutation. Specification 004 requires `REFINING` for Grain readiness but also demands substantial semantic/readiness fields. Combining those authorities into the first recursive authoring write would silently expand the trust boundary.

Child-DRAFT authoring can expose the constitution's recursive primitive while preserving the existing rule that a DRAFT is incomplete and non-executable.

## Boundaries to preserve in later shaping

- no automatic parent state transition;
- no generic SpecNode editor or arbitrary field replacement unless separately justified;
- no readiness-field synthesis or `REFINING -> GRAIN` authorization;
- no dependency/execution/provider behavior;
- no network or hosted requirement;
- no new runtime dependency without demonstrated need;
- no PyPI publication bundled into recursive authoring;
- no benchmark or adoption claim stronger than live evidence;
- explicit crash/collision recovery semantics for any multi-file authoring mutation.

## External ecosystem context

The broader spec-driven-development ecosystem continues to add distribution and workflow breadth. That context increases the importance of a clear first-party journey, but it does not justify copying ecosystem breadth or claiming competitive superiority. SpecGrain should continue to differentiate through a small deterministic recursive/evidence boundary and shape only the next independently provable gap.
