# Specification 017 — Native DRAFT CLI

## Status

`CLOSED_CANONICAL`

## Outcome

Let a new local SpecGrain project create its first native root SpecNode through a deterministic CLI command, producing a validated `DRAFT` artifact in store v1 without requiring users to hand-author internal JSON or granting any readiness/execution authority.

## In scope

- one `specgrain draft` command for creating a root SpecNode;
- required user inputs for title and outcome, with optional rationale;
- deterministic repository-local SpecNode ID allocation;
- state fixed to `DRAFT` at creation;
- safe non-overwriting persistence in `.specgrain/specs/` using canonical store-v1 JSON;
- deterministic text and `--json` output identifying the created SpecNode and semantic revision;
- public Python store API for the same creation operation;
- tests covering creation, ID allocation, invalid input, missing store, non-overwrite behavior, and CLI output;
- README/architecture/changelog updates limited to the new supported surface.

## Out of scope

- child refinement or parent/child mutation;
- automatic conversion from DRAFT to SHAPED, REFINING, GRAIN, READY, or later lifecycle states;
- generating placeholder readiness metadata that could create false Grain readiness;
- editing or overwriting an existing SpecNode;
- importing Spec Kit artifacts into native SpecNodes;
- WorkPacket generation, executor invocation, agent/provider integration, verification execution, or evidence mutation;
- hosted services, networking, telemetry, dashboards, accounts, or model calls;
- PyPI publication or a new product release;
- benchmark execution or competitive claims.

## Acceptance conditions

1. `specgrain draft <path> --title <text> --outcome <text>` creates exactly one canonical root SpecNode under `.specgrain/specs/` when the local project is valid.
2. The created node is fixed to state `DRAFT`, has no parent, children, dependencies, acceptance conditions, change surface, or readiness declaration, and therefore receives no implied Grain/readiness/execution authority.
3. IDs are allocated deterministically as the lowest unused positive canonical identifier from `SG-000001` through `SG-999999`.
4. The creation boundary validates title, outcome, rationale, store structure, and the resulting SpecNode through existing deterministic contracts before persistence.
5. Existing spec files are never overwritten. A collision or write race fails closed without replacing prior canonical content.
6. Text output identifies the created ID, state, relative store path, and semantic revision. `--json` emits deterministic machine-readable data for the same facts.
7. Missing/invalid local stores and invalid user input return non-zero without leaking internal exception details or creating a spec artifact.
8. Existing CLI/API behavior and the zero-runtime-dependency package contract remain compatible.
9. README quickstart demonstrates `init -> draft -> check` using only shipped behavior, while documenting that recursive refinement remains outside 017.
10. Full regression, Ruff, compileall, CLI help parity, and the permanent Linux/macOS/Windows CI matrix succeed on the exact implementation PR head before merge.
11. Exact-head review confirms no lifecycle promotion, overwrite path, hidden external execution, unsupported claim, or scope expansion.

## Canonical product evidence

- Canonical shaping merge: `5c7783dde897c975b3519b37bfd45b547244b273`.
- Product PR #21 exact reviewed head: `1255a9187f85591edd041a3125359e70d2eea379`.
- Exact final-head CI run: `33235889444` — success across all five permanent matrix jobs.
- Product merge commit: `dedb9ee30a6b8856c9c06439c68f3a37225f0563`.
- Product merge first parent: `5c7783dde897c975b3519b37bfd45b547244b273`.
- Product merge second parent: exact reviewed head `1255a9187f85591edd041a3125359e70d2eea379`.
- Canonical post-merge CI run: `33236142514` — success across all five permanent matrix jobs.
- Exact job IDs and review-service boundaries are recorded in `closeout.md`.

## Risks and recovery

- **False readiness:** creation is hard-coded to `DRAFT` and does not populate readiness metadata; recovery is removal of the newly created DRAFT file if the user does not want it.
- **ID collision/race:** persistence uses create-if-absent semantics and fails closed rather than overwrite; the caller may retry after reloading current store truth.
- **Store corruption:** existing store/refinement state is validated before allocation or writing; unrelated invalid state is not silently repaired.
- **CLI/API drift:** API and CLI share the same creation primitive and are covered by regression tests.
- **Scope creep into refinement:** parent/child authoring remains deferred to a separately shaped specification.

## Dependencies

Specifications 000 through 016 were `CLOSED_CANONICAL` before 017 shaping. The shaped 017 authority chain became canonical at merge `5c7783dde897c975b3519b37bfd45b547244b273` before implementation began.

No constitution amendment or new ADR was required.

The `CLOSED_CANONICAL` status in this file becomes authoritative only when the exact documentation-only closeout head containing it is merged with expected-head protection and live GitHub post-closeout evidence confirms canonical `main`.
