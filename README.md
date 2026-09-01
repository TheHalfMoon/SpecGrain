<div align="center">

# SpecGrain

**Big ideas. Small specs. Proven software.**

A local-first, agent-neutral delivery control plane for turning software work into small, bounded, independently verifiable changes.

[![CI](https://github.com/TheHalfMoon/SpecGrain/actions/workflows/ci.yml/badge.svg)](https://github.com/TheHalfMoon/SpecGrain/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/TheHalfMoon/SpecGrain?display_name=tag)](https://github.com/TheHalfMoon/SpecGrain/releases/tag/v0.3.0)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Runtime dependencies](https://img.shields.io/badge/runtime%20dependencies-0-2ea44f)](pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Current published release:** `v0.3.0` · **Python:** `3.11+` · **License:** MIT · **Runtime dependencies:** zero

[Quickstart](#quickstart) · [Why SpecGrain](#why-specgrain) · [Architecture](#architecture) · [Developer map](#developer-map) · [Contributing](#contributing)

</div>

---

## Why SpecGrain?

AI coding agents can generate large changes quickly. The hard part is keeping those changes **bounded, reviewable, recoverable, and provable**.

SpecGrain treats delivery control as a deterministic engineering problem:

- **Small by construction** — recursively refine work until one leaf is independently understandable and verifiable.
- **Evidence over self-report** — executor success is input; verification is a separate decision bound to exact revisions and checks.
- **Local-first** — repository state stays local; the deterministic core does not require a hosted control plane or model call.
- **Agent-neutral** — WorkPackets and result contracts are portable across coding agents, IDEs, and providers.
- **Brownfield-first** — existing repositories, conventions, tests, ownership, and change boundaries are first-class inputs.
- **Zero runtime dependencies** — the core package uses the Python standard library at runtime.

If a change is too large, SpecGrain's default answer is **refine it further**, not “use a larger prompt.”

## Quickstart

### Install the published release

The current published release is **v0.3.0**:

```bash
python -m pip install "https://github.com/TheHalfMoon/SpecGrain/archive/refs/tags/v0.3.0.zip"
```

Create a local project and one bounded root specification:

```bash
mkdir specgrain-demo
specgrain init specgrain-demo --project-id demo
specgrain draft specgrain-demo \
  --title "Add a bounded health check" \
  --outcome "The service exposes one deterministic health endpoint"
specgrain check specgrain-demo
```

Add a child specification when the parent still needs refinement:

```bash
specgrain draft specgrain-demo \
  --parent SG-000001 \
  --title "Define the health response" \
  --outcome "The health response has one bounded deterministic contract"
```

All of these operations are local and deterministic. `draft` creates only `DRAFT` specifications; it does not silently grant Grain, readiness, execution, or verification authority.

### Published release vs current `main`

`v0.3.0` is a historical release. Current `main` is intentionally ahead of that release.

| Capability | `v0.3.0` | Current `main` |
| --- | :---: | :---: |
| Root and child DRAFT authoring | ✓ | ✓ |
| Explicit authoring recovery | ✓ | ✓ |
| Project check / next / scan / prove | ✓ | ✓ |
| Read-only Spec Kit import | ✓ | ✓ |
| Explicit `DRAFT -> SHAPED -> REFINING -> GRAIN` preparation | — | ✓ |
| Read-only WorkPacket export | — | ✓ |
| Supported pre-Grain writer serialization | — | ✓ |
| Shared coordination between supported pre-Grain and child writers | — | ✓ |

To try current source behavior from a checkout:

```bash
python -m pip install . --no-deps
```

No newer release is implied by current source behavior.

## The core idea: a Grain

A specification may recursively contain smaller specifications. A leaf becomes a **Grain** only after deterministic readiness rules establish that its outcome, scope, acceptance conditions, dependencies, risk/recovery plan, context footprint, change surface, and evidence requirements are bounded enough for independent execution and verification.

```text
Intent
  -> Spec
      -> Spec
          -> Grain -> WorkPacket -> Execute -> Verify -> Evidence
          -> Grain
```

A Grain is not “whatever fits in the model context window.” It is a bounded unit with explicit proof requirements.

## Current source workflow

Current `main` includes the native pre-Grain path:

```text
DRAFT -> SHAPED -> REFINING -> GRAIN
```

Every readiness-sensitive declaration is explicit:

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

`shape` does not invent missing risk, recovery, evidence, context, minimality, or safety claims. `refine` is state-only. `grain` re-evaluates readiness and refuses promotion unless the exact current candidate is ready.

### Export a WorkPacket

For an already dependency-eligible `GRAIN`, context accounting remains explicit. Create a bounded JSON file containing `ContextSource` records:

```json
[
  {
    "source_id": "health-contract",
    "provenance": "repo:docs/health-contract.md",
    "selection_reason": "Bind the explicit health response contract to execution.",
    "revision": "git:0123456789abcdef",
    "size_bytes": 640,
    "token_cost": 160,
    "requirement": "required",
    "priority": 0
  }
]
```

Then export the deterministic packet:

```bash
specgrain packet SG-000001 specgrain-demo \
  --context-sources context-sources.json \
  --json
```

`packet` does not fetch the content named by `provenance`, discover context, invoke a model, run an executor, write a packet into `.specgrain/`, or advance lifecycle state.

No `GRAIN -> READY`, WorkPacket execution, agent/provider orchestration, execution-result ingestion, verification execution, or evidence mutation is authorized by these native commands.

## Supported CLI

### Published v0.3.0 CLI

| Command | Purpose |
| --- | --- |
| `specgrain init [path]` | Initialize repository-local SpecGrain state. |
| `specgrain draft [path] --title ... --outcome ... [--parent SG-XXXXXX]` | Create a root DRAFT or one child DRAFT. |
| `specgrain recover [path]` | Recover one exact recognized pending native authoring transaction. |
| `specgrain check [path]` | Validate local state and readiness reports. |
| `specgrain next [path]` | Show dependency-eligible Grains and projected waves. |
| `specgrain scan [path]` | Build a bounded deterministic brownfield repository map. |
| `specgrain prove <spec-id> [path]` | Load and validate append-oriented evidence for a spec. |
| `specgrain import-spec-kit <feature-dir>` | Produce a read-only, source-bound Spec Kit migration report. |

### Current source additions after v0.3.0

| Command | Purpose |
| --- | --- |
| `specgrain shape <spec-id> [path] ...` | Explicitly populate one DRAFT candidate and advance it to SHAPED. |
| `specgrain refine <spec-id> [path]` | Advance exactly SHAPED to REFINING without semantic mutation. |
| `specgrain grain <spec-id> [path]` | Promote exactly REFINING to GRAIN only after current readiness succeeds. |
| `specgrain packet <spec-id> [path] --context-sources <json-file>` | Export an eligible GRAIN through the deterministic WorkPacket contract. |

The historical v0.3.0 tag and GitHub Release do not contain `shape`, `refine`, `grain`, or `packet`.

## Reliability model

### Supported mutation coordination

Current source serializes supported pre-Grain persistence and coordinates it with native child authoring through one project-scoped, non-blocking advisory mutation lock. Child authoring keeps its separate durable recovery journal.

The design is intentionally narrow:

- no distributed locking;
- no retry/backoff/lease protocol;
- no arbitrary external-writer coordination claim;
- no runtime dependency added;
- losing supported writers fail closed instead of waiting indefinitely.

### Explicit recovery

Child authoring uses a recoverable journal instead of pretending a two-file update is operating-system atomic. If a recognized child-authoring transaction is interrupted, ordinary store reads refuse the pending state until explicit recovery:

```bash
specgrain recover specgrain-demo
```

Recovery clears, rolls back, or finalizes only exact recognized states. Ambiguous state is preserved for investigation rather than guessed or overwritten.

## Evidence and trust

Executor self-report is never verification authority. Independent verification binds:

- current SpecNode revision;
- WorkPacket digest;
- execution-result digest;
- implementation revision;
- observed changed paths;
- acceptance checks;
- evidence checks.

Evidence records are append-oriented and hash chained. Concurrent evidence forks fail closed rather than being silently accepted.

Run the repository's end-to-end API example:

```bash
python examples/zero_to_verified.py
```

The example creates a Grain candidate, builds a context-bounded WorkPacket, simulates one bounded change, evaluates independent checks, appends evidence, and proves the chain. It demonstrates API capability; it does not imply additional native CLI lifecycle authority.

## Brownfield first

`specgrain scan` maps bounded repository facts without executing repository commands or sending the repository to a model.

[`examples/brownfield/README.md`](examples/brownfield/README.md) pins public Python, Node.js, and Rust repositories and shows reproducible scan commands without publishing invented output.

## Migrating from GitHub Spec Kit

SpecGrain is architecturally independent from GitHub Spec Kit, but supports a read-only migration report:

```bash
specgrain import-spec-kit path/to/specs/001-feature \
  --source-revision <git-sha> \
  --constitution path/to/.specify/memory/constitution.md
```

The importer preserves supported source information, binds artifacts to their source revision/digests, and keeps legacy flat tasks as evidence rather than silently promoting them into SpecGrain's recursive ontology.

See [`docs/migration-from-spec-kit.md`](docs/migration-from-spec-kit.md).

## Architecture

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

The deterministic kernel owns correctness-sensitive decisions. LLMs, coding agents, IDEs, and providers remain optional adapters around it.

## Developer map

| Area | Start here |
| --- | --- |
| Spec schema and semantic revision | [`src/specgrain/model.py`](src/specgrain/model.py) |
| Lifecycle state machine | [`src/specgrain/lifecycle.py`](src/specgrain/lifecycle.py) |
| Recursive refinement | [`src/specgrain/refinement.py`](src/specgrain/refinement.py) |
| Grain readiness | [`src/specgrain/readiness.py`](src/specgrain/readiness.py) |
| Local store, authoring, recovery, mutation coordination | [`src/specgrain/store.py`](src/specgrain/store.py) |
| DRAFT → GRAIN preparation | [`src/specgrain/pregrain.py`](src/specgrain/pregrain.py) |
| Dependency ordering | [`src/specgrain/dependency.py`](src/specgrain/dependency.py) |
| Context budgeting | [`src/specgrain/context.py`](src/specgrain/context.py) |
| WorkPacket and execution-result contracts | [`src/specgrain/packet.py`](src/specgrain/packet.py) |
| Independent verification and evidence | [`src/specgrain/verification.py`](src/specgrain/verification.py) |
| Brownfield repository scanning | [`src/specgrain/repository.py`](src/specgrain/repository.py) |
| Benchmark framework | [`src/specgrain/benchmark.py`](src/specgrain/benchmark.py) |

For deeper design context, read [`docs/architecture.md`](docs/architecture.md), [`docs/trust-model.md`](docs/trust-model.md), and [`docs/methodology.md`](docs/methodology.md).

## What SpecGrain is not

SpecGrain is intentionally **not**:

- a hosted project-management dashboard;
- an autonomous agent runner;
- a model/provider requirement;
- a replacement for Git;
- a claim that every filesystem writer is transactionally coordinated;
- a benchmark winner without a valid public comparative dataset.

Those boundaries keep the core deterministic, portable, and auditable.

## Benchmarks: evidence before claims

SpecGrainBench provides deterministic experiment plans, contamination/isolation preflight, run ledgers, and no-automatic-winner reports. No benchmark winner is claimed without valid reproducible evidence.

See [`docs/benchmark-report-v0.1.0.md`](docs/benchmark-report-v0.1.0.md) and [`docs/benchmark-strategy.md`](docs/benchmark-strategy.md).

## Project documentation

- [`docs/product-thesis.md`](docs/product-thesis.md) — product/category thesis.
- [`docs/domain-model.md`](docs/domain-model.md) — recursive specification model.
- [`docs/architecture.md`](docs/architecture.md) — deterministic kernel and boundaries.
- [`docs/trust-model.md`](docs/trust-model.md) — verification and trust model.
- [`docs/methodology.md`](docs/methodology.md) — delivery methodology.
- [`docs/donor-policy.md`](docs/donor-policy.md) — provenance and donor-code rules.
- [`docs/roadmap.md`](docs/roadmap.md) — evidence-shaped program sequence.
- [`docs/execution-master-plan.md`](docs/execution-master-plan.md) — canonical continuation rules.

## Contributing

Contributions are welcome when they are **small, reproducible, and independently reviewable**.

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check src tests examples
python -m compileall -q src tests examples
```

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before changing product behavior. Please also follow [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), and report security issues according to [`SECURITY.md`](SECURITY.md).

SpecGrain is released under the [MIT License](LICENSE).
