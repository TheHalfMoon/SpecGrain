# Specification 019 — Native Child-DRAFT Authoring

## Status

`SHAPED`

## Outcome

Let a valid local SpecGrain project create one native child SpecNode under an existing `DRAFT` parent through the supported API/CLI, preserving reciprocal refinement structure through a deterministic recoverable multi-file authoring transaction without granting lifecycle, readiness, or execution authority.

## Why this is the next frontier

Specification 018 is `CLOSED_CANONICAL` after closeout merge `c5282caa29fbfeb8c118755766b6a7b8a49d2781`, post-closeout CI run `33246162550`, and no-mutation release verification run `33246212598`.

Public `v0.2.0` can initialize a project and create root `DRAFT` SpecNodes, while the deterministic core already validates recursive parent/child forests. The fresh post-v0.2 audit identifies the inability to author a child through the supported product surface as the smallest current gap.

This specification deliberately stops before broad `refine` orchestration. Creating a child changes the parent semantic revision because `children` is part of SpecNode content, so 019 permits that mutation only while the selected parent remains `DRAFT`.

## In scope

- extend native DRAFT authoring so a caller may select an existing parent by canonical SpecNode ID;
- parent eligibility fixed to lifecycle state `DRAFT`;
- one new child fixed to `DRAFT`, with explicit title/outcome and optional rationale;
- deterministic lowest-unused positive SpecNode ID allocation using the existing store-v1 range;
- reciprocal mutation: child `parent_id` identifies the selected parent and the parent `children` declaration includes the new child ID;
- validate the complete proposed forest before any canonical parent/child mutation is published;
- a versioned internal authoring-transaction journal under ignored runtime state, with deterministic explicit recovery semantics for interrupted two-file mutations;
- handled-failure rollback where the exact transaction preimage remains recoverable;
- fail-closed behavior when journal/files do not match a recognized transaction phase;
- read APIs refuse pending authoring transactions rather than silently repairing them;
- public explicit recovery API plus `specgrain recover` CLI for the bounded authoring journal;
- `specgrain draft --parent <SG-ID>` while preserving existing root-DRAFT behavior when `--parent` is absent;
- deterministic text/JSON outputs that identify child and parent revisions for child authoring and recovery outcome for recovery;
- tests for child creation, nested DRAFT creation, reciprocal structure, state restriction, invalid/missing parent, collisions, interrupted phases, recovery, journal ambiguity, and CLI behavior;
- README/architecture/changelog updates limited to the new supported surface.

## Out of scope

- automatic parent transition from `DRAFT` to `SHAPED`, `REFINING`, `GRAIN`, `READY`, or any later state;
- child creation under a non-`DRAFT` parent;
- generic editing/replacement of arbitrary SpecNode fields;
- semantic decomposition generation, AI-created child content, or model/provider calls;
- readiness metadata synthesis or `REFINING -> GRAIN` authorization;
- dependency scheduling, WorkPacket generation, executor/provider invocation, verification execution, or evidence mutation;
- changing the SpecNode schema or refinement-validation semantics;
- claiming operating-system atomicity for a mutation that spans two canonical files;
- cross-process locking guarantees against arbitrary non-cooperating manual file edits;
- hosted services, networking, telemetry, dashboards, or accounts;
- new runtime dependencies;
- PyPI publication, package-version bump, or a new GitHub release;
- empirical benchmark execution or competitive superiority claims.

## Authoring transaction contract

The canonical child operation changes two SpecNode files. Standard portable filesystem primitives do not provide one atomic commit across both files, so 019 MUST NOT describe the operation as OS-atomic.

Instead, the supported writer uses one exclusive versioned journal at:

```text
.specgrain/tmp/authoring-transaction.json
```

The journal records enough exact before/after data to classify recovery without guessing, including:

- transaction version and operation kind;
- parent ID and child ID;
- exact parent preimage;
- exact intended parent postimage;
- exact intended child content.

The write sequence is:

1. load and validate the current project/refinement forest and require no pending authoring transaction;
2. require the selected parent to exist and remain `DRAFT`;
3. allocate the child ID and construct child + parent postimage;
4. validate the complete proposed forest;
5. create the journal with create-if-absent semantics before canonical multi-file mutation;
6. create the child with create-if-absent semantics;
7. re-check the parent preimage and atomically replace the single parent file using same-directory temporary-file replacement;
8. remove the journal only after the resulting exact child/parent state is confirmed.

Handled failures attempt deterministic rollback. If rollback cannot prove the exact expected state, the journal remains and ordinary reads/writes fail closed until explicit recovery succeeds.

### Recovery classification

`recover_authoring_transaction()` / `specgrain recover` may mutate state only when the journal and files exactly identify one of these safe cases:

- **no canonical mutation:** parent equals preimage and child is absent -> remove journal;
- **child-only partial write:** parent equals preimage and child equals journal child -> remove the transaction-created child, then remove journal;
- **completed write with stale journal:** parent equals postimage and child equals journal child -> preserve both canonical files and remove journal.

Any other combination is ambiguous and MUST fail closed without replacing or deleting canonical SpecNode content.

Read-oriented surfaces MUST NOT silently recover a journal. They report recovery-required state so mutation remains explicit.

## Acceptance conditions

1. Existing `specgrain draft <path> --title ... --outcome ...` root behavior remains backward compatible.
2. `specgrain draft <path> --parent SG-XXXXXX --title ... --outcome ...` creates exactly one child fixed to `DRAFT` under an existing `DRAFT` parent.
3. The new child uses the lowest unused positive canonical ID and carries `parent_id=<parent>`; the parent postimage includes the child ID exactly once.
4. The complete proposed forest passes the existing deterministic refinement validator before the journal or canonical files are mutated.
5. A missing parent, malformed parent ID, invalid existing forest, non-`DRAFT` parent, exhausted ID space, unsafe store path, or known collision fails non-zero without an authorized semantic mutation.
6. Child authoring does not change parent lifecycle state and does not populate acceptance, dependency, change-surface, evidence, risk/readiness, or execution authority for the new child.
7. A versioned create-if-absent journal prevents two supported child-authoring transactions from intentionally overlapping; a pending journal blocks ordinary store reads/writes with an explicit recovery-required error.
8. Normal success leaves no journal and produces a structurally valid project with deterministic parent/child revisions and CLI output.
9. Interruption before child publication is recoverable by clearing only the matching journal; interruption after exact child creation but before parent replacement is recoverable by removing only that transaction-created child; interruption after exact parent replacement is recoverable by finalizing the already-valid state.
10. Recovery refuses any state whose parent or child bytes/semantic content do not exactly match a recognized journal phase; it never guesses, overwrites unrelated content, or deletes an ambiguous child.
11. Parent replacement uses same-directory temporary-file + `os.replace` semantics after an exact preimage check; no two-file OS-atomicity claim is made.
12. `specgrain recover` and the public recovery API are idempotent when no journal exists and emit deterministic text/JSON status.
13. Full regression, Ruff, compileall, CLI help parity, package build/install, and the permanent Ubuntu 3.11/3.12/3.13, macOS 3.11, and Windows 3.11 matrix succeed on the exact implementation PR head before merge.
14. Exact-head review confirms no non-DRAFT parent mutation, lifecycle promotion, silent read-time repair, overwrite path, new dependency, hidden external execution, unsupported atomicity claim, or unrelated product scope.
15. Product merge uses expected-head protection and canonical post-merge CI succeeds before product completion is claimed.
16. 019 becomes `CLOSED_CANONICAL` only through a bounded documentation-only closeout PR whose exact head is merged with expected-head protection and whose post-closeout canonical CI succeeds.

## Dependencies

- Specifications 000 through 018 are `CLOSED_CANONICAL`.
- Canonical 018 closeout merge: `c5282caa29fbfeb8c118755766b6a7b8a49d2781`.
- Canonical 018 post-closeout CI: `33246162550` — success across all five permanent jobs.
- Canonical 018 no-mutation release verification: `33246212598` — success; `v0.2.0` remained at historical product source `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`.
- `docs/research/post-v0.2-product-audit-2026-08-29.md` supplies frontier evidence only.
- Specification 001 supplies immutable SpecNode content/revision semantics.
- Specification 002 / ADR-0004 preserve the distinction between transition legality and mutation authority.
- Specification 003 supplies reciprocal refinement validation.
- Specification 005 / ADR-0005 supply store-v1 JSON and dependency-free local IO.
- Specification 017 supplies root-DRAFT creation and deterministic ID allocation.
- ADR-0018 defines the recoverable multi-file authoring transaction boundary.

## Risks and recovery

- **Half-refined forest after interruption:** durable journal classification plus explicit recovery; ordinary operations fail closed while a journal remains.
- **Mutation of a mature spec revision:** only `DRAFT` parents are eligible; non-DRAFT parents are rejected before journal creation.
- **Child collision/race:** child creation remains create-if-absent; handled collisions roll back/clear only when the parent preimage remains exact.
- **Parent concurrent/manual edit:** exact preimage is re-checked before replacement; detected drift fails closed. Arbitrary non-cooperating edits in the final race window are a documented residual risk, not a claimed locking guarantee.
- **Ambiguous recovery:** preserve journal and canonical files unchanged and report the mismatch rather than guessing.
- **Read-time side effects:** reads never perform recovery automatically.
- **Scope creep into refinement orchestration:** no state promotion, semantic generation, or readiness/execution authority is included.

## Constitution and architecture

No constitution amendment is required. 019 directly advances Principle I (recursive specification) while preserving Principle II (Grain before execution), Principle VII (deterministic control plane), Principle VIII (vendor neutrality), and Principle XI (reversibility/blast-radius control).

This shaped status is prospective on its documentation-only branch. Implementation authority exists only after the exact shaping head is merged canonically and canonical `main` is re-read.
