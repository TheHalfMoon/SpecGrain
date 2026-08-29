# Specification 022 — Native Grain Preparation

## Status

`SHAPED`

## Outcome

Let a user take an existing native SpecGrain candidate from `DRAFT` through the deterministic pre-execution lifecycle to `GRAIN` using supported API/CLI surfaces, without hand-editing internal JSON and without granting READY/execution/verification authority.

## Why this is the next frontier

Specifications 000 through 021 are `CLOSED_CANONICAL`. Canonical `main` is `3b98914200c68909f09db08642faf56de48305eb` and the published release remains `v0.3.0` at product source `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

The post-v0.3 observation rule requires fresh evidence before a successor. `docs/research/post-v0.3-native-workflow-friction-2026-08-29.md` reproduces a maintainer-supplied external adoption finding against canonical source:

- `draft` produces validated DRAFTs;
- no supported CLI populates the fields needed by Grain readiness;
- no supported CLI advances a candidate into `SHAPED`, `REFINING`, or `GRAIN`;
- `check` evaluates readiness only for existing `REFINING` leaves;
- `next` considers only existing `GRAIN` nodes.

This is concrete user/adoption friction and satisfies the post-v0.1 evidence rule for shaping 022.

The external review recommends a full DRAFT-to-VERIFIED loop. 022 deliberately chooses the smaller authority boundary: close only the pre-execution dead end first. WorkPacket/executor/verification/evidence mutation remains separately shapeable later.

## In scope

- public store/API operations for one-node pre-Grain mutation under ADR-0019;
- `DRAFT -> SHAPED` with explicit population of existing bounded-candidate fields;
- `SHAPED -> REFINING` state-only transition;
- `REFINING -> GRAIN` state-only transition only when existing deterministic Grain readiness passes for the exact current candidate revision and complete forest;
- a native `specgrain shape <spec-id> [path]` command;
- a native `specgrain refine <spec-id> [path]` command;
- a native `specgrain grain <spec-id> [path]` command;
- deterministic text and `--json` output for all three commands;
- explicit readiness blocker output for rejected `grain` promotion;
- exact-preimage single-file replacement and fail-closed drift detection;
- pending ADR-0018 child-authoring transaction refusal;
- proposed forest/schema/dependency validation before semantic shaping replacement;
- public API exports for the new bounded mutation functions/results;
- regression tests for API, CLI, wrong-state refusal, malformed input, drift, pending recovery, readiness blocking, exact successful promotion, and revision semantics;
- README/changelog/architecture updates limited to the new supported pre-execution workflow.

## Shape contract

`specgrain shape` operates only on an existing node in state `DRAFT` and preserves identity/refinement structure. The initial CLI must accept explicit values for the existing readiness-relevant fields without inventing hidden claims:

- repeatable `--scope-in` (at least one);
- repeatable `--scope-out` (optional);
- repeatable `--acceptance` (at least one);
- repeatable `--dependency` (optional canonical SpecNode IDs);
- `--risk-level` (`low`, `medium`, `high`, `critical`);
- `--recovery` (non-empty text);
- `--context-budget` (positive integer tokens);
- `--context-estimate` (non-negative integer tokens);
- repeatable `--change-surface`, or a non-empty `--change-surface-exception`;
- repeatable `--evidence` (at least one required evidence identifier);
- `--minimality-choice` using the existing readiness enum;
- `--minimality-rationale` (non-empty text);
- `--safety-status` using the existing readiness enum;
- repeatable `--safety-requirement` when `requirements-defined` is selected.

The shaped node sets `metadata.readiness.version` to the existing canonical readiness version and records explicit empty `unresolved_decisions`. The CLI may normalize ordering through existing SpecNode canonicalization but must not silently synthesize risk, recovery, context, evidence, minimality, or safety assertions.

The semantic fields `id`, `title`, `outcome`, `rationale`, `parent_id`, `children`, `labels`, `method`, and `schema_version` remain unchanged by the initial `shape` operation.

## Lifecycle contract

### `DRAFT -> SHAPED`

Authorized only through successful bounded shaping. The replacement must construct and validate the complete proposed project before exact-preimage single-file replacement.

### `SHAPED -> REFINING`

`specgrain refine` authorizes exactly this state edge on the selected current node. It changes no semantic field and therefore preserves the semantic revision digest.

### `REFINING -> GRAIN`

`specgrain grain`:

1. loads and validates the current project;
2. requires source state `REFINING`;
3. runs the existing `evaluate_grain_readiness()` against the exact node and complete forest;
4. refuses mutation and returns deterministic blocker codes if any issue exists;
5. otherwise performs only the legal `REFINING -> GRAIN` state change through exact-preimage replacement;
6. confirms the resulting project remains valid.

No direct edge skipping is authorized.

## Out of scope

- `GRAIN -> READY` or any later lifecycle transition;
- WorkPacket CLI generation;
- executor/provider invocation, model calls, orchestration, or agent-specific command installation;
- execution-result ingestion;
- running acceptance/evidence commands on behalf of the user;
- verification-report or evidence-record mutation;
- automatic AI shaping, interactive LLM interviews, inferred risk, inferred context estimates, or inferred safety claims;
- generic arbitrary SpecNode editing after `DRAFT`;
- changing title/outcome/rationale/refinement structure in the initial shaping command;
- changing Grain-readiness v1 semantics or weakening any existing gate;
- changing the SpecNode schema;
- multi-writer locking expansion or widening ADR-0018 recovery semantics;
- PyPI/publication/version bump or a new release;
- hosted/network/provider/account surfaces;
- runtime dependency growth;
- empirical benchmark runs or superiority claims.

## Acceptance conditions

1. Existing `init`, root/child `draft`, `recover`, `check`, `next`, `scan`, `prove`, and `import-spec-kit` behavior remains backward compatible.
2. `shape` succeeds only for an existing `DRAFT` and persists exactly the explicit readiness-related data defined above plus state `SHAPED`.
3. `shape` preserves ID, title, outcome, rationale, parent/children structure, labels, method, and schema version.
4. `shape` validates inputs through existing SpecNode/readiness vocabulary and rejects missing/invalid required declarations without mutation.
5. `shape` requires either a non-empty change surface or an explicit non-empty change-surface exception.
6. `shape` validates the complete proposed refinement/dependency state before replacement and rejects invalid dependency IDs/graphs without mutation.
7. `shape` refuses a pending ADR-0018 authoring journal and detects exact-preimage drift before replacement.
8. `refine` succeeds only for source state `SHAPED`, changes only state to `REFINING`, and preserves the semantic revision digest.
9. `grain` succeeds only for source state `REFINING` when the existing Grain-readiness evaluator returns zero issues for the exact candidate/forest.
10. A blocked `grain` attempt writes no canonical mutation and reports the stable readiness blocker codes in deterministic text/JSON output.
11. Successful `grain` changes only state to `GRAIN`, preserves the semantic revision digest, and causes existing `next` behavior to consider the node according to current dependency eligibility semantics.
12. No command skips lifecycle edges or grants `READY`, execution, verification, or evidence authority.
13. All three commands fail non-zero on malformed IDs, missing specs, wrong source states, unsafe/symlink store paths, pending recovery, invalid existing project state, or exact-preimage drift.
14. Public API exports and CLI help accurately describe the bounded authority; no documentation presents 022 as DRAFT-to-VERIFIED completion.
15. Runtime dependencies remain zero and no network/model/provider code is introduced.
16. Full regression, Ruff, compileall, tracked-tree cleanliness, CLI help parity, package build/install, and permanent Ubuntu 3.11/3.12/3.13, macOS 3.11, and Windows 3.11 CI succeed on the exact implementation PR head.
17. Exact-head review confirms no readiness weakening, hidden defaults, lifecycle edge skipping, post-GRAIN mutation, multi-file recovery widening, execution/evidence authority, dependency creep, or unrelated scope.
18. Product merge uses expected-head protection; canonical post-merge CI succeeds before implementation completion is claimed.
19. 022 becomes `CLOSED_CANONICAL` only after a documentation-only closeout PR with exact evidence is merged using expected-head protection and post-closeout canonical CI is verified.

## Dependencies

- Specifications 000 through 021 are `CLOSED_CANONICAL`.
- Canonical pre-022 main: `3b98914200c68909f09db08642faf56de48305eb`.
- `docs/research/post-v0.3-native-workflow-friction-2026-08-29.md` supplies fresh adoption-friction evidence.
- Specification 001 supplies immutable SpecNode content/revision semantics.
- Specification 002 / ADR-0004 supply lifecycle legality vs. authorization separation.
- Specification 003 supplies refinement validation.
- Specification 004 supplies Grain-readiness v1.
- Specification 005 / ADR-0005 supply the dependency-free local store.
- Specifications 017 and 019 supply native DRAFT authoring/recovery.
- ADR-0018 remains authoritative for child-authoring multi-file recovery only.
- ADR-0019 defines the new bounded pre-Grain mutation authority.

## Risks and recovery

- **Over-broad editing authority:** initial shaping mutates only a DRAFT and only the enumerated existing fields; mature states are rejected.
- **Fabricated readiness assertions:** every readiness-sensitive declaration is explicit input; no model/default invents risk, context, evidence, minimality, or safety facts.
- **Concurrent/manual edit:** exact preimage is checked immediately before same-directory replacement; detected drift fails closed.
- **Interaction with pending child transaction:** all new mutations refuse while ADR-0018 recovery is pending.
- **Readiness bypass:** only the existing evaluator can authorize `REFINING -> GRAIN`; blockers produce no state mutation.
- **Scope creep into execution:** 022 stops at `GRAIN`; READY/WorkPacket/executor/verification/evidence remain outside authority.

## Constitution and architecture

No constitution amendment is required. 022 advances Principle II (Grain before execution), Principle III (evidence over assertion), Principle V (minimal ceremony by removing hand-edited internal JSON), Principle VII (deterministic control plane), Principle VIII (agent/vendor neutrality), and Principle XI (reversibility/blast-radius control).

This `SHAPED` status is prospective on a documentation-only branch. Implementation authority exists only after the exact shaping head is merged canonically and canonical `main` is re-read.
