# Architecture

## Architectural goal

Build a small deterministic control plane around recursive specifications. AI integrations should be replaceable helpers, not the source of truth.

## Core components

```text
                    +----------------------+
Intent / Import --->| Spec Compiler        |
                    | refine + validate    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Spec Store / Graph   |
                    | tree + dependency DAG|
                    +----+------------+----+
                         |            |
                         v            v
              +---------------+  +----------------+
              | Context Engine|  | Method / Risk  |
              +-------+-------+  +--------+-------+
                      \                 /
                       v               v
                    +----------------------+
                    | Readiness Engine     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Work Packet Builder  |
                    +----------+-----------+
                               |
                         adapter boundary
                               |
                               v
                    +----------------------+
                    | Human / Agent        |
                    | Executor             |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Verification Engine  |
                    +----------+-----------+
                               |
                  +------------+------------+
                  v                         v
          +---------------+          +---------------+
          | Evidence Ledger|          | Metrics       |
          +---------------+          +---------------+
```

## 1. Deterministic core

The following must be deterministic and extensively tested:

- schema parsing and validation;
- ID and revision rules;
- state transitions;
- Grain readiness gates;
- tree and dependency-graph integrity;
- ready-set calculation;
- context-budget accounting when source sizes are known;
- work-packet hashing;
- evidence binding;
- scope comparison;
- metric calculations.

AI may suggest values, but core validation decides whether they are acceptable.

## 2. Storage

Initial product state is repository-local and file-based.

Specification 005 defines store v1 as:

```text
.specgrain/
  project.json
  specs/
    SG-000001.json
    SG-000002.json
  policies/
    default.json
```

Evidence directories are added only when Specification 010 defines their canonical contract. Runtime caches and temporary run data are not canonical and should remain untracked.

JSON v1 is the canonical M2 store format because it is available in the Python standard library, maps directly onto `SpecNode` data, and permits strict duplicate-key/non-finite-number rejection without adding a runtime dependency. Canonical semantic hashes remain computed from normalized data, not raw whitespace.

YAML may later be supported as an import/export or authored-format adapter if evidence justifies it, but it must not silently replace or weaken the versioned store contract. See `docs/adr/0005-dependency-free-json-store.md`.

Specification 017 adds the first public native authoring write: create one root SpecNode fixed to `DRAFT` with deterministic positive ID allocation and create-if-absent persistence.

Specification 019 extends the unreleased native authoring surface with one reciprocal child write under a `DRAFT` parent. Because the operation changes two canonical SpecNode files, it uses the recoverable/fail-closed transaction contract from ADR-0018 rather than claiming multi-file operating-system atomicity.

The supported child writer creates an ignored runtime journal at:

```text
.specgrain/tmp/authoring-transaction.json
```

The journal records the exact parent preimage, intended parent postimage, and intended child. Reads refuse a pending journal. Explicit recovery recognizes only exact no-write, child-only, or completed states; ambiguous state is preserved without destructive repair. Parent replacement uses same-directory temporary-file + `os.replace` semantics for that single file only.

## 3. CLI

The CLI grows progressively as specifications own bounded product surfaces.

Shipped on current `main`:

```text
specgrain init
specgrain draft
specgrain recover
specgrain check
specgrain next
specgrain scan
specgrain prove
specgrain import-spec-kit
```

`draft` creates a root `DRAFT` when no parent is supplied. `draft --parent SG-XXXXXX` creates one child fixed to `DRAFT` only when the selected parent is also `DRAFT`; neither path promotes lifecycle state or synthesizes readiness metadata.

`recover` is an explicit bounded mutation for the native authoring journal. It does not attempt generic store repair and does not run automatically from read-oriented commands.

Still-deferred commands include:

```text
specgrain ask
specgrain refine
specgrain graph
specgrain packet
specgrain verify
specgrain diff
```

`run` may be added when evidence justifies a portable orchestration surface. Early releases should not embed many vendor-specific executors.

## 4. Python implementation

Initial implementation target:

- Python 3.11+;
- standard-library deterministic core wherever sufficient;
- `argparse` + `json` + `pathlib` for local CLI/store surfaces;
- pytest for tests;
- ruff and a static type checker as development quality gates when available.

Typer, Rich, Pydantic, PyYAML, and graph libraries are not architectural requirements. They may be adopted later only when a bounded problem justifies their dependency cost. The core should avoid a heavy graph dependency unless profiling or complexity demonstrates a need.

## 5. Repository intelligence

`scan` should not attempt to index an entire repository into a prompt. It should derive a compact repository map from deterministic signals such as:

- language/build manifests;
- directory structure;
- test layout;
- ownership/configuration files;
- active spec references;
- version-control changes.

Future semantic retrieval may be an adapter, but deterministic repository facts remain available without an embedding service.

## 6. Context engine

The context engine selects and records why each source is included. A context item should carry:

- source identifier/path;
- selection reason;
- size estimate;
- digest or repository revision;
- mandatory/optional classification.

Context policy can reject a candidate Grain that cannot fit within budget without omitting required context.

## 7. Scheduler

The scheduler computes eligible Grains from:

- Grain readiness;
- dependency state;
- repository baseline compatibility;
- blocker state;
- optional WIP policy.

Parallel waves are derived from the DAG but should remain advisory until conflict analysis is reliable.

## 8. Execution adapter boundary

Adapters receive an immutable WorkPacket and return a structured execution result. The core does not depend on transcript semantics.

Adapters may target:

- a human-readable packet;
- Claude Code;
- Codex;
- GitHub Copilot;
- Cursor;
- other local or hosted agent harnesses.

The contract is more important than the number of adapters.

## 9. Verification

Verification should be layered:

1. evidence presence;
2. acceptance evaluation;
3. required checks/tests;
4. changed-scope comparison;
5. dependency/baseline integrity;
6. provenance checks where applicable;
7. residual-risk handling.

A verifier may use AI for semantic review, but AI-only evidence cannot silently satisfy deterministic gates.

## 10. Security and trust

- Never execute arbitrary repository commands merely because a spec requests them.
- Execution adapters must make command authority explicit.
- Treat imported specs and external repository content as untrusted data.
- Canonical local-store readers must reject path escape and symlink ambiguity instead of following untrusted store links.
- Root authoring remains create-if-absent; child authoring may replace only the exact selected `DRAFT` parent preimage under the ADR-0018 journal contract.
- A pending authoring journal blocks ordinary store operations until explicit deterministic recovery succeeds.
- Recovery must not guess, overwrite unrelated content, or delete an ambiguous child.
- Avoid shell interpolation in core subprocess boundaries.
- Evidence records should be append-oriented and digest-bound once Specification 010 owns that contract.
- Secrets and environment files must not be captured into work packets or evidence by default.
- A readiness report is not reusable lifecycle mutation authority; future state writes must re-evaluate current preconditions at the mutation boundary.
