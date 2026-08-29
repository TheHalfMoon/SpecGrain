# SpecGrain

**Big ideas. Small specs. Proven software.**

[![CI](https://github.com/TheHalfMoon/SpecGrain/actions/workflows/ci.yml/badge.svg)](https://github.com/TheHalfMoon/SpecGrain/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/TheHalfMoon/SpecGrain?display_name=tag)](https://github.com/TheHalfMoon/SpecGrain/releases/tag/v0.3.0)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

SpecGrain is an open-source, local-first, agent-neutral delivery control plane for turning software work into small, bounded, independently verifiable changes. Its deterministic core owns specification structure, readiness, dependency ordering, context budgets, WorkPackets, evidence binding, drift/metrics, Spec Kit import, agent-adapter boundaries, and benchmark comparability checks.

**Current published release:** `v0.3.0` · **Python:** `3.11+` · **License:** MIT · **Runtime dependencies:** zero

## Published v0.3.0 quickstart

Install the current published release directly from GitHub:

```bash
python -m pip install "https://github.com/TheHalfMoon/SpecGrain/archive/refs/tags/v0.3.0.zip"
```

Then try the native local workflow shipped by that historical release:

```bash
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

The published v0.3.0 release includes root and child DRAFT authoring plus explicit recovery. It does **not** contain `shape`, `refine`, or `grain`.

## Current source workflow after Specification 022

Current source adds a bounded native path from an existing `DRAFT` through deterministic Grain preparation:

```text
DRAFT -> SHAPED -> REFINING -> GRAIN
```

Install a current source checkout with `python -m pip install . --no-deps`, then provide every readiness-sensitive declaration explicitly:

```bash
specgrain shape SG-000001 specgrain-demo \
  --scope-in "Implement the bounded health endpoint" \
  --scope-out "No provider or hosted integration" \
  --acceptance "Focused health endpoint tests pass" \
  --risk-level low \
  --recovery "Revert the bounded endpoint change." \
  --context-budget 2000 \
  --context-estimate 500 \
  --change-surface "src/health.py" \
  --evidence "focused-tests" \
  --minimality-choice native \
  --minimality-rationale "No existing equivalent primitive is present." \
  --safety-status none-identified
specgrain refine SG-000001 specgrain-demo
specgrain check specgrain-demo
specgrain grain SG-000001 specgrain-demo
specgrain next specgrain-demo
```

`shape` mutates only one existing `DRAFT` and does not invent risk, recovery, context, evidence, minimality, or safety claims. `refine` is a state-only `SHAPED -> REFINING` transition. `grain` re-evaluates the unchanged deterministic Grain-readiness rules and refuses mutation with stable blockers unless the exact current candidate is ready. The state-only transitions preserve the semantic revision digest.

Specification 022 stops at `GRAIN`. No `GRAIN -> READY`, WorkPacket execution, agent/provider orchestration, verification execution, or evidence mutation is authorized by these commands.

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

## Supported CLI

### Published v0.3.0 CLI

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

Every command in this table exists in the historical `v0.3.0` tag and GitHub Release.

### Current source additions after v0.3.0

| Command | Purpose |
| --- | --- |
| `specgrain shape <spec-id> [path] ...` | Explicitly populate one DRAFT candidate and advance it to SHAPED. |
| `specgrain refine <spec-id> [path]` | Advance exactly SHAPED to REFINING without semantic mutation. |
| `specgrain grain <spec-id> [path]` | Promote exactly REFINING to GRAIN only after current readiness succeeds. |

The historical v0.3.0 tag and GitHub Release do not contain `shape`, `refine`, or `grain`. These commands are current-source additions from Specification 022; no new release or version bump is claimed here.

Inspection commands and the bounded mutation commands provide deterministic output; JSON is available where `--json` is supported. SpecGrain remains a deterministic control plane, not an agent runner or hosted service. External agents integrate through portable WorkPacket/result adapter contracts rather than becoming verification authority.

## Zero to VERIFIED

The repository includes a runnable API example that creates a Grain candidate, checks readiness, builds a context-bounded WorkPacket, simulates one bounded implementation change, performs independent acceptance/evidence checks, appends an immutable evidence record, and proves the chain:

```bash
python examples/zero_to_verified.py
```

See [`examples/zero_to_verified.py`](examples/zero_to_verified.py). The example is executed by the test suite; `VERIFIED` is derived from independent checks, not from the executor's success claim. The example demonstrates existing API capability and is not a claim that Specification 022 authorizes a native CLI transition beyond `GRAIN`.

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

SpecGrainBench provides deterministic experiment plans, isolation/contamination preflight, run ledgers, and no-automatic-winner reports for prompt-only, GitHub Spec Kit, and SpecGrain arms. v0.3.0 does **not** claim an empirical winner because a public comparative run dataset has not yet been published. The current public benchmark methodology report remains [`docs/benchmark-report-v0.1.0.md`](docs/benchmark-report-v0.1.0.md); see also [`docs/benchmark-strategy.md`](docs/benchmark-strategy.md).

## Architecture in one view

```text
Recursive SpecNode
  -> Lifecycle + refinement
  -> Native pre-Grain preparation
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
