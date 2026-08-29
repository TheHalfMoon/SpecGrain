# Post-023 Fable Review and Benchmark Preflight — 2026-08-29

## Status

Observation evidence only. This document does not select, shape, or authorize Specification 024 and does not widen lifecycle, execution, verification, release, locking, or Spec Kit integration authority.

## Exact inputs

SpecGrain canonical input:

- repository: `TheHalfMoon/SpecGrain`;
- canonical `main`: `ca8f8b7a8d2146c38c35d6535c52f311bba0ae80`;
- canonical state: post-Specification-023 observation;
- active product specification: none.

GitHub Spec Kit comparison input:

- repository: `github/spec-kit`;
- reviewed `main`: `51e52be6c3b26fed3ff5424c671f4a559519a759`;
- current README workflow at that revision: constitution -> specify -> plan -> tasks -> implement -> converge;
- current project metadata at that revision declares `specify-cli` version `1.0.2.dev0` and runtime dependencies including Typer, Click, Rich, Platformdirs, Readchar, PyYAML, Packaging, Pathspec, and JSON5.

External review input:

- an independent Fable architecture review supplied on 2026-08-29;
- treated as external evidence and architectural opinion only;
- not treated as repository authority, implementation authorization, benchmark data, or a substitute for canonical source inspection.

## Reproduced findings

### 1. SpecGrain and Spec Kit currently operate at different practical layers

Current GitHub Spec Kit explicitly provides an agent-facing end-to-end workflow through implementation and convergence. It also exposes integrations for more than 30 coding agents and supports extensions, presets, and bundles.

Current SpecGrain native CLI exposes:

- `init`;
- `draft`;
- `shape`;
- `refine`;
- `grain`;
- `recover`;
- `check`;
- `next`;
- `scan`;
- `prove`;
- `import-spec-kit`.

The native CLI does not currently expose WorkPacket generation, executor invocation, execution-result ingestion, READY/RUNNING/VERIFYING lifecycle mutation, or verification execution.

This is a concrete current-surface difference, not evidence that SpecGrain must permanently remain preparation-only.

### 2. SpecGrain already contains portable execution and proof contracts below the native CLI surface

`src/specgrain/packet.py` defines deterministic, portable `WorkPacket` and `ExecutionResult` contracts. `build_work_packet(...)` binds a packet to exact spec and context facts while explicitly refusing to authorize lifecycle transitions or execution.

`examples/zero_to_verified.py` demonstrates a deterministic Grain-to-proof API path:

1. establish Grain readiness;
2. establish bounded context;
3. build a WorkPacket;
4. obtain an externally represented `ExecutionResult`;
5. independently verify the implementation against acceptance and evidence checks;
6. append a verification report;
7. load a proof bound to the exact implementation revision.

Therefore the external-review statement that SpecGrain has no execution/verification architecture is too broad. The narrower reproduced gap is that current canonical product authority does not expose or authorize a native execution-orchestration path from GRAIN through later lifecycle states.

### 3. SpecGrain is not canonically defined as a permanent preparation-only layer

`AGENTS.md` states that SpecGrain exists to make changes small enough to understand, execute, verify, recover, and prove and describes the project as an evidence-backed delivery system.

The constitution requires portable work packets and result contracts and defines Grain before execution, evidence-bound verification, deterministic state transitions, and agent/vendor neutrality.

The execution master plan likewise preserves WorkPacket, verification/evidence, and agent-adapter architecture while currently withholding later lifecycle mutation and orchestration authority.

Accordingly, `preparation-only forever` is not a canonical architectural conclusion. `Preparation is the currently authorized native mutation frontier` is accurate.

### 4. Spec Kit has materially broader execution and extension ergonomics today

At reviewed upstream `main`, GitHub Spec Kit documents:

- constitution/specify/plan/tasks/implement/converge workflow;
- more than 30 coding-agent integrations;
- extension, preset, and bundle systems;
- bundled bug and idea-assessment workflows;
- agent-specific project initialization and optional skills mode.

This supports the external review's conclusion that Spec Kit is currently stronger in direct execution integration, agent ecosystem breadth, and workflow onboarding.

### 5. Runtime-dependency contrast is reproduced

Current SpecGrain policy and package structure retain a zero-third-party-runtime-dependency core.

Current GitHub Spec Kit `pyproject.toml` declares multiple runtime dependencies. This is an architectural trade-off, not by itself a quality ranking.

## Findings not reproduced as product defects

### Onboarding severity

The native `shape` command is intentionally explicit and has a relatively large argument surface. That is observable. No controlled abandonment, task-completion, error-rate, or user-study dataset currently demonstrates that this is a high-severity adoption defect.

### Governance overhead severity

SpecGrain has substantial canonical process and evidence artifacts. Principle V explicitly says ceremony that does not improve value, evidence, safety, flow, or learning should be removed. However, no measured contributor-cost dataset currently proves which specific governance artifact is redundant enough to remove.

### Concurrent-writer severity

The bounded race around exact-preimage validation plus atomic replacement remains a documented residual. Calling it low, moderate, or critical for real teams would require observed concurrent usage or a controlled race reproduction. No such empirical dataset was produced by the external review.

### Need for SpecGrain-to-Spec-Kit export

The absence of a direct SpecGrain GRAIN -> Spec Kit execution export/handoff adapter is reproducible. User need, lossless mapping requirements, round-trip expectations, and whether Spec Kit is the correct execution target are not yet empirically established.

### Need for native execution orchestration

The native CLI discontinuity after GRAIN is reproducible. That alone does not establish that SpecGrain should invoke agents or become another end-to-end SDD toolkit. Existing portable packet/result and independent-verification contracts leave multiple possible future integration shapes.

## SpecGrainBench preflight

The repository benchmark strategy requires a fair comparison to use:

- the same task and immutable repository baseline across arms;
- the same acceptance oracle;
- the same model/provider configuration where model-based systems are compared;
- fresh workspaces and fresh agent contexts/processes for every `(task, method, repetition)` cell;
- multiple repetitions for probabilistic systems;
- isolated method-specific skills, hooks, plugins, rules, and global configuration;
- exact method/model configuration records;
- contamination preflight;
- retained failed and blocked runs;
- repository-outcome scoring rather than prose-volume proxies.

The current published benchmark report explicitly states that no controlled public multi-arm external-agent dataset exists yet and no method winner is declared.

### Candidate comparison

A useful future first controlled case remains a small brownfield change with a deterministic acceptance oracle and tightly bounded change surface, using the existing initial arms:

1. prompt-only baseline;
2. GitHub Spec Kit;
3. SpecGrain.

The experiment should measure at minimum:

- acceptance pass/fail;
- regression pass/fail;
- changed files and lines;
- unauthorized/unnecessary changed paths;
- retries;
- human interventions;
- model input/output tokens where available;
- first-pass verification;
- rework ratio;
- context utilization;
- recovery cost if an induced failure is included.

### Current execution preflight result

`BLOCKED_FOR_VALID_COMPARATIVE_CLAIM`

Reason: this observation session can inspect both repositories and record exact source evidence, but it does not provide a controlled mechanism for launching independent fresh prompt-only, Spec Kit, and SpecGrain agent cells with identical model/provider configuration, isolated workspaces, isolated agent contexts, repetitions, and contamination checks.

Running all arms through one shared conversational context would violate SpecGrainBench isolation rules and would not produce publishable evidence. A fabricated or contaminated comparison must not be recorded as a benchmark result.

This blocker is methodological, not a product failure.

## Fresh technical observation produced by this audit

The strongest concrete current observation is a **native handoff-surface discontinuity**:

- SpecGrain can deterministically create a GRAIN through the native CLI;
- the core can programmatically build a portable WorkPacket and represent an ExecutionResult;
- the core can independently verify externally supplied execution facts;
- but the native CLI currently has no command that turns an eligible GRAIN into a portable execution handoff or ingests an executor result for the later proof chain;
- canonical authority intentionally withholds READY/execution/verification mutation and executor/provider orchestration.

This discontinuity is reproducible from source. It is not yet enough to choose a solution.

Possible future solutions include, but are not limited to:

- a read-only/export-only WorkPacket handoff command;
- a generic adapter contract exposed through CLI without invoking an executor;
- an execution-result ingestion boundary;
- a verification runner boundary;
- a Spec Kit-specific export adapter;
- no new product surface if real users do not need the handoff.

No option is selected by this audit.

## Evidence required before a successor can be shaped

At least one of the following should be reproduced before selecting a successor:

1. a controlled SpecGrainBench cell set demonstrating a measurable handoff, scope, verification, context, recovery, or execution-traceability problem;
2. repeated real-user evidence that the GRAIN-to-external-execution boundary causes concrete workflow failure or manual evidence loss;
3. a deterministic interoperability fixture showing that a bounded, portable handoff cannot be expressed through the current public API/CLI without unsafe or duplicative glue;
4. a reproducible concurrent-writer failure whose practical blast radius exceeds the currently accepted residual;
5. repeated onboarding failures attributable to a specific CLI or artifact surface rather than general unfamiliarity.

## Decision

`OBSERVATION SHOULD CONTINUE`

No Specification 024 is selected or authorized by the Fable review or this preflight.

The Fable review is useful evidence for where to look next, but its strongest product recommendations are hypotheses until controlled or repeated evidence is produced. The current canonical architecture should remain unchanged while the project gathers a valid benchmark or real workflow evidence.
