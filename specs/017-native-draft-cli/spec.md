# Specification 017 — Native DRAFT CLI

## Status

`SHAPED`

## Outcome

Let a new local SpecGrain project create its first native root SpecNode through a deterministic CLI command, producing a validated `DRAFT` artifact in store v1 without requiring users to hand-author internal JSON or granting any readiness/execution authority.

## Evidence basis

The post-v0.1 product audit at `docs/research/post-v0.1-product-audit-2026-08-29.md` identifies first-party native authoring as the smallest current adoption gap. `specgrain init` creates an empty store, while the shipped CLI has no command that creates a SpecNode. The Python model/store contracts already provide the deterministic validation boundary required for a small native implementation.

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
3. IDs are allocated deterministically as the lowest unused canonical `SG-######` identifier representable by store v1.
4. The creation boundary validates title, outcome, rationale, store structure, and the resulting SpecNode through existing deterministic contracts before persistence.
5. Existing spec files are never overwritten. A collision or write race fails closed without replacing prior canonical content.
6. Text output identifies the created ID, state, relative store path, and semantic revision. `--json` emits deterministic machine-readable data for the same facts.
7. Missing/invalid local stores and invalid user input return non-zero without leaking internal exception details or creating a spec artifact.
8. Existing CLI/API behavior and the zero-runtime-dependency package contract remain compatible.
9. README quickstart demonstrates `init -> draft -> check` using only shipped behavior, while documenting that recursive refinement remains outside 017.
10. Full regression, Ruff, compileall, CLI help parity, and the permanent Linux/macOS/Windows CI matrix succeed on the exact implementation PR head before merge.
11. Exact-head review confirms no lifecycle promotion, overwrite path, hidden external execution, unsupported claim, or scope expansion.

## Risks and recovery

- **False readiness:** creation is hard-coded to `DRAFT` and does not populate readiness metadata; recovery is removal of the newly created DRAFT file if the user does not want it.
- **ID collision/race:** persistence must use create-if-absent semantics and fail closed rather than overwrite; the caller may retry after reloading current store truth.
- **Store corruption:** validate the existing store before allocating or writing. Do not repair unrelated invalid state silently.
- **CLI/API drift:** use one shared store creation primitive and test both public API and CLI surfaces.
- **Scope creep into refinement:** parent/child authoring is explicitly deferred and requires a fresh post-017 decision.

## Dependencies

Specifications 000 through 016 are `CLOSED_CANONICAL`. Specification 017 is shaped from canonical `main` `7c343841424ca48207f9c42eae725a53213d19e5` and the live post-v0.1 audit.

No constitution amendment or new ADR is required: the change implements the existing deterministic local-store and progressive CLI architecture without changing a durable architectural decision.
