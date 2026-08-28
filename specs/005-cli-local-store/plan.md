# Plan 005 — CLI and Local Store

## Strategy

Build the first local product surface with the Python standard library only. Keep persistence separate from kernel models: JSON files store the existing public `SpecNode.to_dict()` representation, while `load_project` reconstructs kernel values through `SpecNode.from_dict()`.

## Planned files

```text
src/specgrain/store.py
src/specgrain/cli.py
src/specgrain/__main__.py
src/specgrain/__init__.py
pyproject.toml
tests/test_store.py
tests/test_cli.py
specs/005-cli-local-store/*
docs/adr/0005-dependency-free-json-store.md
docs/architecture.md
```

Do not modify `model.py`, `lifecycle.py`, `refinement.py`, or `readiness.py` unless exact implementation evidence exposes a compatibility defect.

## Dependency decision

Use only:

- `argparse`;
- `json`;
- `pathlib`;
- `tempfile`/`shutil`/`os` for initialization;
- existing SpecGrain kernel modules.

Do not add Typer, Rich, Pydantic, PyYAML, or another runtime dependency in 005. ADR-0005 records why JSON v1 replaces the earlier provisional YAML preference for this milestone.

## Module boundaries

### `store.py`

Own:

- store/project/policy version constants;
- manifest/policy/result dataclasses and enums;
- strict JSON read/write helpers;
- path/symlink validation;
- `init_project`;
- `load_project`;
- `check_project`.

It must not parse CLI arguments or print terminal output.

### `cli.py`

Own:

- argparse parser;
- text/JSON rendering;
- exit-code mapping;
- calls into store API.

No store validation logic should be duplicated in CLI code.

### `__main__.py`

One thin call to `cli.main()`.

### `pyproject.toml`

Add only:

```toml
[project.scripts]
specgrain = "specgrain.cli:main"
```

No dependency changes.

## Strict JSON parser

Use `json.loads` with:

- an `object_pairs_hook` that rejects duplicate keys at every object level;
- `parse_constant` that rejects non-finite number tokens;
- UTF-8 text reads with decoding errors surfaced as store errors.

Do not silently coerce values.

## Contract parsing

Manifest and policy parsers:

1. require top-level Mapping/object;
2. reject non-string/unknown fields;
3. require exact supported version integers and reject bool;
4. validate safe names before path construction;
5. return frozen/slotted dataclasses.

Spec parser:

1. require filename stem to be canonical SpecGrain ID;
2. parse strict JSON object;
3. call `SpecNode.from_dict()`;
4. require `node.id == filename stem`;
5. wrap model errors with deterministic file path context.

## Symlink boundary

Before canonical reads:

- repository root must be an ordinary directory;
- `.specgrain`, `specs`, and `policies` must be ordinary non-symlink directories;
- `project.json`, active policy, and every loaded spec must be ordinary non-symlink files.

No recursive filesystem walk is needed in 005. Enumerate direct `.json` children of `specs/` only.

## Initialization

`init_project`:

1. resolve/validate existing repository root;
2. fail if `.specgrain` exists in any form;
3. validate explicit/default project ID;
4. create a sibling staging directory under the repository root;
5. write `project.json`, `policies/default.json`, and empty `specs/`;
6. atomically rename staging directory to `.specgrain`;
7. cleanup staging on failure.

If rename fails, `.specgrain` must not be partially populated by 005.

## Project check

For a loaded project:

1. call `validate_refinement(project.specs)`;
2. if structural issues exist, return invalid result and skip readiness evaluation;
3. otherwise compute roots;
4. select nodes with `state == REFINING` and no children, sorted by ID;
5. call `evaluate_grain_readiness(node, project.specs)` for each;
6. count ready/blocked candidates;
7. determine overall validity from policy:
   - `report`: structural/store validity only;
   - `enforce`: structural/store validity + zero readiness-blocked candidates.

Do not re-evaluate GRAIN/later states as historical transition proof.

## Structured check result

Prefer immutable dataclasses. Readiness-blocked entries can contain the existing immutable `GrainReadinessReport` rather than inventing a second readiness schema.

Provide a deterministic `to_dict()`/JSON-compatible projection for CLI JSON output. Do not serialize Python enum reprs.

## CLI rendering

### Text

Example valid report-mode project:

```text
SpecGrain check: PASS
Project: example-project
Policy: default (readiness=report)
Specs: 3
Roots: 1
REFINING leaves: 2
Grain-ready: 1
Readiness-blocked: 1
```

Then list blocked IDs and concise issue codes in canonical order.

### JSON

Use one object with stable keys/content and `json.dumps(..., sort_keys=True, ensure_ascii=False)`. One trailing newline.

Do not include timestamps, absolute paths, or environment-specific data in JSON output unless necessary for an error. This keeps repeated checks reproducible.

## Exit-code mapping

- parser usage => argparse `2`;
- `init` success => `0`;
- `init` store refusal/error => `1`;
- `check` policy-valid => `0`;
- `check` invalid/enforcement failure => `1`.

Unexpected internal exceptions must not be swallowed as a false PASS; CLI should emit a concise error and exit `1` in 005.

## Verification

### Store tests

Cover:

- successful initialization/layout/content;
- explicit/default project ID;
- existing store refusal;
- invalid root/project/policy names;
- staging cleanup on simulated write/rename failure where practical without implementation coupling;
- strict JSON duplicate/non-finite/top-level errors;
- manifest/policy unknown fields/version/bool failures;
- symlink rejection (skip only when platform cannot create symlinks);
- valid spec load/order;
- filename/content ID mismatch;
- malformed model/spec errors;
- valid/invalid refinement checks;
- report/enforce readiness modes;
- deterministic structured result;
- no writes during check.

### CLI tests

Call `main(argv)` directly and capture stdout/stderr. Cover:

- init success/refusal;
- check text pass/fail;
- report vs enforce exit codes;
- deterministic `--json`;
- argparse usage code 2;
- `python -m` thin entry point by structural/import smoke rather than subprocess where avoidable.

Run all 001–005 tests and compileall. Record Ruff as NOT RUN if unavailable.

## Scope review

Before PR, confirm no:

- dependency-DAG algorithms;
- repository scanning;
- subprocess execution;
- lifecycle mutation;
- evidence storage;
- YAML parser;
- agent/provider integration;
- generic write-spec/mutation API;
- third-party runtime dependency.

## Risk

The highest risks are filesystem ambiguity and accidentally turning `check` into mutation/authorization. Fail closed on store shape/symlinks, keep `check` read-only, and keep 004 readiness reports informational/policy-gating only rather than transition capabilities.
