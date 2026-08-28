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

Initial design is repository-local and file-based.

Proposed project state:

```text
.specgrain/
  project.yaml
  specs/
    SG-0001.yaml
    SG-0002.yaml
  evidence/
    SG-0002/
      <run-id>.json
  policies/
    default.yaml
```

Runtime caches and temporary run data are not canonical and should remain untracked.

The canonical format should be stable, machine-readable, diff-friendly, and editable without a server. YAML is preferred for authored state; canonical hashes should be computed from normalized data, not raw whitespace.

## 3. CLI

Initial command surface should remain small:

```text
specgrain init
specgrain scan
specgrain ask
specgrain refine
specgrain check
specgrain graph
specgrain next
specgrain packet
specgrain verify
specgrain prove
specgrain diff
```

`run` may be added when the portable packet/result boundary is stable. The first release should not embed many vendor-specific executors.

## 4. Python implementation

Initial implementation target:

- Python 3.11+;
- Typer for CLI;
- Rich for terminal presentation;
- Pydantic for model validation if dependency cost remains justified;
- PyYAML for authored state;
- pytest for tests;
- ruff and a static type checker for quality gates.

The core should avoid a heavy graph dependency unless profiling or complexity justifies one. DAG algorithms required for early releases are small and testable.

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
- Avoid shell interpolation in core subprocess boundaries.
- Evidence records should be append-oriented and digest-bound.
- Secrets and environment files must not be captured into work packets or evidence by default.
