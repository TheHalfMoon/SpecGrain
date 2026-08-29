# SpecGrain

**Big ideas. Small specs. Proven software.**

SpecGrain is an open-source, agent-neutral delivery kernel for turning software work into small, bounded, independently verifiable changes. Its deterministic core owns specification structure, readiness, dependency ordering, context budgets, WorkPackets, evidence binding, drift/metrics, Spec Kit import, agent-adapter boundaries, and benchmark comparability checks.

[![CI](https://github.com/TheHalfMoon/SpecGrain/actions/workflows/ci.yml/badge.svg)](https://github.com/TheHalfMoon/SpecGrain/actions/workflows/ci.yml)

## One-minute start

SpecGrain requires Python 3.11 or newer. From a clone:

```bash
python -m pip install .
specgrain scan .
mkdir specgrain-demo
specgrain init specgrain-demo --project-id demo
specgrain draft specgrain-demo \
  --title "Add a bounded health check" \
  --outcome "The service exposes one deterministic health endpoint"
specgrain draft specgrain-demo \
  --parent SG-000001 \
  --title "Define the health response" \
  --outcome "The health response has one bounded deterministic contract"
specgrain check specgrain-demo
```

The commands above are local and deterministic. `scan` maps bounded brownfield repository facts without executing repository commands or sending the repository to a model. `init` creates repository-local `.specgrain/` state. `draft` creates a validated SpecNode fixed to `DRAFT`: without `--parent` it creates a root, and with `--parent` it creates one reciprocal child under an existing `DRAFT` parent. Neither path grants Grain/readiness/execution authority. `check` validates local state.

Child authoring uses a recoverable, fail-closed journal rather than claiming an operating-system-atomic two-file write. If a supported child-authoring transaction is interrupted, ordinary store reads refuse the pending journal until the user explicitly runs:

```bash
specgrain recover specgrain-demo
```

Recovery only clears, rolls back, or finalizes an exact recognized transaction state. Ambiguous parent/child state is preserved for manual investigation instead of being guessed or overwritten.

The published v0.2.0 release includes root `draft` authoring but predates the unreleased child-DRAFT and `recover` surfaces now present on `main`. v0.2.0 can be installed directly from its source archive:

```bash
python -m pip install "https://github.com/TheHalfMoon/SpecGrain/archive/refs/tags/v0.2.0.zip"
```

## What is a Grain?

A specification may recursively contain smaller specifications. A leaf becomes a **Grain** only after deterministic readiness rules establish that its outcome, scope, acceptance conditions, dependencies, risk/recovery plan, context footprint, change surface, and evidence requirements are bounded enough for independent execution and verification.

```text
Intent
  -> Spec
      -> Spec
          -> Grain -> WorkPacket -> Execute -> Verify -> Evidence
          -> Grain
```

When a change is too large, SpecGrain's default answer is further refinement—not a larger prompt.

## Supported CLI on current main

| Command | Purpose |
| --- | --- |
| `specgrain init [path]` | Initialize repository-local SpecGrain state. |
| `specgrain draft [path] --title ... --outcome ... [--parent SG-XXXXXX]` | Create a root DRAFT or one child DRAFT under an existing DRAFT parent. |
| `specgrain recover [path]` | Explicitly recover one exact pending native authoring transaction. |
| `specgrain check [path]` | Validate local state and Grain-readiness reports. |
| `specgrain next [path]` | Show dependency-eligible Grains and projected waves. |
| `specgrain scan [path]` | Build a bounded deterministic brownfield repository map. |
| `specgrain prove <spec-id> [path]` | Load and validate append-oriented evidence for a spec. |
| `specgrain import-spec-kit <feature-dir>` | Produce a read-only, source-bound Spec Kit migration report. |

Inspection commands, `draft`, and `recover` provide deterministic JSON output where `--json` is supported.

The published v0.2.0 release contains every command in the table except `recover`; its `draft` command creates roots only and has no `--parent` option. Current unreleased `main` adds child-DRAFT authoring without changing package version or claiming a new release. SpecGrain remains a deterministic control plane, not an agent runner or hosted service. External agents integrate through portable WorkPacket/result adapter contracts rather than becoming verification authority.

## Zero to VERIFIED

The repository includes a runnable API example that creates a Grain candidate, checks readiness, builds a context-bounded WorkPacket, simulates one bounded implementation change, performs independent acceptance/evidence checks, appends an immutable evidence record, and proves the chain:

```bash
python examples/zero_to_verified.py
```

See [`examples/zero_to_verified.py`](examples/zero_to_verified.py). The example is executed by the test suite; `VERIFIED` is derived from independent checks, not from the executor's success claim.

## Brownfield first

SpecGrain treats existing repositories as the normal case. [`examples/brownfield/README.md`](examples/brownfield/README.md) pins three public Python, Node.js, and Rust repositories and shows reproducible scan commands without publishing invented output.

## Migrating from GitHub Spec Kit

Use the explicit, read-only importer:

```bash
specgrain import-spec-kit path/to/specs/001-feature \
  --source-revision <git-sha> \
  --constitution path/to/.specify/memory/constitution.md
```

The importer preserves supported source information in a reviewable report, binds artifacts to their source revision/digests, and keeps legacy flat tasks as evidence rather than silently promoting them into SpecGrain's recursive ontology. See [`docs/migration-from-spec-kit.md`](docs/migration-from-spec-kit.md).

## Evidence and trust

Executor self-report is input, not authority. Independent verification binds the current SpecNode revision, WorkPacket digest, execution-result digest, observed changed paths, acceptance checks, evidence checks, and implementation revision. Append-oriented evidence records are hash chained.

Read [`docs/trust-model.md`](docs/trust-model.md), [`docs/architecture.md`](docs/architecture.md), and [`docs/methodology.md`](docs/methodology.md) for the trust and delivery model.

## Benchmarks: evidence before claims

SpecGrainBench provides deterministic experiment plans, isolation/contamination preflight, run ledgers, and no-automatic-winner reports for prompt-only, GitHub Spec Kit, and SpecGrain arms. v0.2.0 does **not** claim an empirical winner because a public comparative run dataset has not yet been published. The current public benchmark methodology report remains [`docs/benchmark-report-v0.1.0.md`](docs/benchmark-report-v0.1.0.md); see also [`docs/benchmark-strategy.md`](docs/benchmark-strategy.md).

## Architecture in one view

```text
Recursive SpecNode
  -> Lifecycle + refinement
  -> Grain readiness
  -> Local store + dependency DAG
  -> Brownfield repository map
  -> Context budget
  -> WorkPacket + agent-neutral adapter
  -> Independent verification + evidence
  -> Method profiles + drift/metrics
  -> Spec Kit import
  -> SpecGrainBench
```

The runtime package has zero third-party dependencies. LLMs, coding agents, IDEs, and providers remain optional adapters around the deterministic kernel.

## Project documents

- [`docs/product-thesis.md`](docs/product-thesis.md) — product/category thesis.
- [`docs/domain-model.md`](docs/domain-model.md) — recursive specification model.
- [`docs/architecture.md`](docs/architecture.md) — deterministic kernel and boundaries.
- [`docs/methodology.md`](docs/methodology.md) — Agile/Lean/PMP/Six-Sigma-inspired operating model.
- [`docs/donor-policy.md`](docs/donor-policy.md) — provenance and donor-code rules.
- [`docs/roadmap.md`](docs/roadmap.md) — milestone sequence.
- [`docs/execution-master-plan.md`](docs/execution-master-plan.md) — canonical continuation and completion state.

## Contributing and security

Contributions are welcome as small, independently reviewable changes. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). For vulnerabilities and trust boundaries, read [`SECURITY.md`](SECURITY.md).

SpecGrain is released under the [MIT License](LICENSE).
