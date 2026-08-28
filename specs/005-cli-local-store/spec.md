# Specification 005 — CLI and Local Store

**Status:** SHAPED  
**Type:** implementation  
**Created:** 2026-08-28  
**Depends on:** `004-grain-readiness` (`CLOSED_CANONICAL`)

## Problem

Specifications 001–004 provide deterministic in-memory primitives but no repository-local product surface. A user cannot initialize SpecGrain state, load authored specs from disk, validate a local refinement forest, or run the readiness kernel from a stable CLI.

The first local product surface must remain small. It must not smuggle dependency scheduling, repository scanning, agent execution, evidence verification, or lifecycle mutation into a generic "check" command.

## Outcome

Implement a dependency-free repository-local JSON store plus `specgrain init` and `specgrain check`. A user can initialize `.specgrain/`, author SpecNode JSON files, load project policy, validate the store deterministically, and see readable or machine-readable check results.

## Canonical store v1

```text
.specgrain/
  project.json
  specs/
    SG-000001.json
    SG-000002.json
  policies/
    default.json
```

Evidence directories are not created by 005; their contract belongs to Specification 010.

### `project.json`

Exact fields:

```json
{
  "store_version": 1,
  "project_id": "example-project",
  "policy": "default"
}
```

Rules:

- `store_version` MUST be integer `1` and bool MUST be rejected;
- `project_id` MUST match `[A-Za-z0-9][A-Za-z0-9._-]{0,63}`;
- `policy` MUST use the same safe name grammar and resolves only to `.specgrain/policies/<policy>.json`;
- unknown fields MUST fail closed.

### Policy v1

Exact fields:

```json
{
  "policy_version": 1,
  "readiness_mode": "report"
}
```

`readiness_mode` is:

- `report`: readiness blockers on structurally valid `REFINING` leaves are reported but do not make the project structurally invalid;
- `enforce`: any readiness-blocked `REFINING` leaf makes `check` fail.

This is the only project-policy behavior owned by 005. Later policy surfaces require their owning specs.

### Spec files

- filename MUST be exactly `<SpecNode.id>.json`;
- only direct `*.json` files inside `.specgrain/specs/` are canonical spec files;
- file content MUST be one JSON object accepted by `SpecNode.from_dict()`;
- filename ID and content ID MUST match exactly;
- file iteration and diagnostics MUST be deterministic by filename/path;
- symlinked canonical store files/directories MUST be rejected rather than followed.

## Strict JSON rules

All canonical store JSON reads MUST:

- decode UTF-8;
- reject duplicate object keys;
- reject `NaN`, `Infinity`, and `-Infinity`;
- require an object at the expected top level;
- surface path-qualified deterministic errors.

Store writes created by `init` use UTF-8, sorted keys, two-space indentation, `ensure_ascii=False`, and one trailing newline.

## Public local-store API

### Constants

- `STORE_VERSION = 1`
- `POLICY_VERSION = 1`

### `ReadinessPolicyMode`

`StrEnum` with `report` and `enforce`.

### `ProjectManifest`

Immutable manifest containing `store_version`, `project_id`, and `policy`.

### `ProjectPolicy`

Immutable policy containing `policy_version` and `readiness_mode`.

### `LocalProject`

Immutable loaded project containing:

- repository root;
- `.specgrain` path;
- manifest;
- active policy;
- specs sorted by canonical ID.

### Errors

Expose stable store exceptions carrying deterministic messages and source paths. Malformed JSON/model data MUST not leak raw `KeyError` or parser implementation details to CLI users.

### `init_project(root, project_id=None)`

Initializes a new store only when:

- `root` exists and is an ordinary directory;
- `.specgrain` does not already exist as a file, directory, or symlink;
- project ID is valid.

Initialization MUST be fail-closed and avoid leaving a partially canonical `.specgrain` on a normal write failure. Use a sibling temporary initialization directory and atomic same-parent rename into `.specgrain`; cleanup the staging directory on failure.

The default `project_id` is the root directory basename and must satisfy the same validation rule. If it does not, the caller must supply `--project-id`.

### `load_project(root)`

Loads and validates manifest, active policy, spec filenames/content, and returns `LocalProject`. It does not run refinement/readiness checks.

### `check_project(root)`

Loads the project and then:

1. validates the full refinement forest with Specification 003;
2. if structurally valid, evaluates Specification 004 readiness for every `REFINING` leaf in canonical ID order;
3. summarizes ready and blocked candidates;
4. applies the active `readiness_mode` only to the overall check decision.

A `GRAIN`/later-state node is not retrospectively re-authorized by 005. Historical transition evidence belongs to later persistence/evidence specifications.

## Check result

Expose an immutable structured result with at least:

- `valid`;
- `project_id`;
- `policy`;
- `spec_count`;
- `root_count` when structural validation succeeds;
- `refining_leaf_count`;
- `grain_ready_count`;
- readiness-blocked candidate reports;
- structural/store issues.

Ordering MUST be deterministic.

### Validity semantics

- malformed store/project/spec/refinement data => `valid = false`;
- structurally valid project + `readiness_mode=report` => readiness blockers are reported but `valid = true`;
- structurally valid project + `readiness_mode=enforce` => any readiness-blocked `REFINING` leaf makes `valid = false`.

## CLI

### `specgrain init [PATH] [--project-id ID]`

- PATH defaults to `.`;
- creates the canonical store;
- prints the initialized path/project ID;
- refuses overwrite/re-initialization.

### `specgrain check [PATH] [--json]`

- PATH defaults to `.`;
- text output is compact and human-readable;
- `--json` emits one deterministic JSON object suitable for automation;
- command never mutates canonical state.

### Exit codes

- `0`: command succeeded and, for `check`, policy-valid;
- `1`: store/check validation failure or initialization refusal;
- `2`: CLI usage error (argparse default).

No other exit codes are introduced in 005.

## Entrypoints

- `python -m specgrain ...`
- installed console script `specgrain ...`

Both MUST call the same CLI implementation.

## Security/trust requirements

- do not execute repository commands or subprocesses;
- do not follow canonical-store symlinks;
- do not interpolate shell commands;
- treat all file content as untrusted data;
- do not create or read outside `.specgrain` except resolving/validating the supplied repository root;
- `check` is read-only;
- no readiness report is converted into lifecycle mutation authority.

## Explicit out of scope

- dependency DAG validation/ready-set/waves (`006`);
- repository scan or capability discovery (`007`);
- computed context-source accounting (`008`);
- WorkPackets/execution (`009`);
- evidence ledger/verification (`010`);
- method-profile policy (`011`);
- YAML import/export;
- lifecycle mutation commands;
- `ask`, `refine`, `graph`, `next`, `packet`, `verify`, `prove`, `diff`, or `run`;
- Rich/Typer presentation layers;
- generic spec-writing/mutation API.

## Acceptance criteria

1. `init` creates exactly the canonical v1 project/specs/policies surface without runtime dependencies.
2. initialization refuses existing `.specgrain` state and does not overwrite it.
3. project/policy/spec JSON rejects duplicate keys, non-finite numbers, malformed UTF-8/JSON, wrong top-level types, unknown contract fields, and unsupported versions.
4. project/policy names cannot escape the canonical store path.
5. symlinked canonical store components/files are rejected.
6. spec filenames must match contained canonical IDs.
7. valid multi-root SpecNode forests load and check deterministically.
8. malformed refinement forests fail `check` with structured deterministic diagnostics.
9. valid REFINING leaves receive 004 readiness reports in canonical order.
10. `readiness_mode=report` reports readiness blockers without making a structurally valid project fail.
11. `readiness_mode=enforce` fails when any REFINING leaf is readiness-blocked.
12. `check --json` is deterministic and machine-readable; text mode remains readable.
13. CLI exit codes are exactly 0/1/2 for the defined outcomes.
14. `check` never mutates files or lifecycle state.
15. `python -m specgrain` and console-script paths share one implementation.
16. Specifications 001–004 regression tests remain green.

## Success criterion

A user can install SpecGrain, run `specgrain init`, author repository-local specs, and run `specgrain check` to deterministically validate the first real local SpecGrain project surface without a server, model provider, or third-party runtime dependency.
