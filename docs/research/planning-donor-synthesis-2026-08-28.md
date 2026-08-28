# Planning Donor Synthesis — 2026-08-28

## Purpose

Record concrete design lessons from selected open-source planning/agent projects before SpecGrain defines refinement, Grain readiness, WorkPackets, verification, and benchmarking.

This is a **design-reference review**, not a code adoption record. No donor source code is copied by this document.

## Sources reviewed

### Ponytail

- Repository: <https://github.com/DietrichGebert/ponytail>
- Reviewed revision: `2ed6c52c9d7e5e56942508591085fd45dea277d3`
- Key sources:
  - `AGENTS.md`
  - `benchmarks/results/2026-06-18-agentic.md`
- License reported by the project: MIT

### Karpathy-inspired coding guidelines

- Repository: <https://github.com/multica-ai/andrej-karpathy-skills>
- Reviewed revision: `2c606141936f1eeef17fa3043a72095b4765b9c2`
- Key source: `CLAUDE.md`
- License reported by the project: MIT

### GitHub Spec Kit

- Repository: <https://github.com/github/spec-kit>
- Reviewed revision: `5aa8bea7823dcd056f111f847bf2d576bad3f0a5`
- Key sources:
  - `templates/plan-template.md`
  - `templates/tasks-template.md`
- License: MIT

## Lessons adopted as SpecGrain design inputs

### 1. Understand before minimizing

Ponytail's minimality ladder explicitly runs only after the agent understands the task and traces the code path. SpecGrain should adopt the same ordering at the system level:

1. establish outcome and acceptance;
2. understand relevant repository context;
3. check whether the requested capability already exists or can be reused;
4. prefer standard/native/already-installed capability when it satisfies the outcome;
5. only then authorize the smallest implementation surface that works.

**SpecGrain mapping:**

- `004-grain-readiness`: bounded outcome, acceptance, unresolved-decision gate;
- `007-repository-scan`: deterministic evidence about existing repository capabilities/patterns;
- `008-context-budget`: only relevant context enters the execution boundary;
- `009-work-packet`: carry reuse/minimality decisions and authorized surface to the executor;
- `012-diff-drift-metrics`: measure unnecessary change and scope accuracy.

Minimality is not code golf. Security, trust-boundary validation, data-loss prevention, accessibility, explicit acceptance, and required recovery controls cannot be removed merely to reduce LOC.

### 2. Every changed line should trace to authorized intent

Karpathy-inspired guidance emphasizes surgical changes: do not improve adjacent code, refactor unrelated areas, or remove pre-existing dead code as a side effect.

SpecGrain should make this measurable rather than relying on agent discipline.

**SpecGrain mapping:**

- a Grain defines an allowed `change_surface`;
- a WorkPacket carries that surface explicitly;
- verification compares actual changed paths against authorized scope;
- `specgrain diff` should identify unscoped changes;
- unrelated improvements become separate specs instead of drive-by edits.

The Specification 002 review already demonstrated this rule by removing an unrelated documentation wording change before merge.

### 3. Success criteria are more valuable than imperative instructions

Karpathy-inspired guidance turns vague instructions into verifiable goals. SpecGrain should encode this in the product contract:

- acceptance criteria are required before execution-ready state;
- WorkPackets describe desired outcomes and checks, not a giant procedural prompt;
- executors may choose implementation details within authorized scope;
- verification evaluates evidence against acceptance independently of executor self-report.

This reinforces SpecGrain's existing `Evidence over assertion` principle.

### 4. Surface assumptions and uncertainty before execution

Silent assumptions are a recurring agent failure mode. SpecGrain should not require an agent to expose private reasoning, but it should require **decision-relevant uncertainty** to become explicit structured project information when it can change scope, safety, architecture, or acceptance.

This does not require a new mandatory hierarchy or a large reasoning transcript. A concise unresolved-decision/readiness failure is sufficient.

**SpecGrain mapping:**

- `004-grain-readiness`: unresolved decisions block Grain promotion;
- `009-work-packet`: include only assumptions/decisions material to execution;
- `011-method-profiles`: higher-risk profiles may require stronger decision/risk evidence.

### 5. Minimality needs safety floors

Ponytail's benchmark shows why "write fewer lines" is not enough: a shorter solution can remove a security guard. SpecGrain should therefore treat simplicity and safety as separate dimensions.

A change is not better merely because it has fewer files or lines. Minimality is acceptable only after required acceptance, security, validation, accessibility, recovery, and policy gates pass.

### 6. Benchmark real agent behavior, not answer verbosity

Ponytail's rebuilt benchmark measures real agent sessions editing a real repository and scores the resulting Git diff. Its earlier single-shot benchmark overstated the effect because conversational output polluted the metric.

**SpecGrainBench implication:** measure repository outcomes, not prose volume.

Preferred benchmark evidence includes:

- acceptance/hidden-test results;
- changed lines/files from Git diff;
- unscoped-change rate;
- regressions and safety checks;
- retries/interventions;
- tokens/cost/time when available;
- rework and first-pass verification.

### 7. Benchmark isolation is a first-class validity gate

Ponytail documented a contamination defect where a globally active plugin entered the baseline arm. SpecGrainBench must actively test for this class of failure.

Each benchmark arm should have:

- a fresh repository/worktree copy from the same pinned snapshot;
- a fresh agent process/context;
- explicit plugin/skill/tool configuration;
- no inherited method-specific hooks from another arm;
- environment/config capture sufficient to audit contamination;
- repeated probabilistic runs;
- failed runs retained in the dataset.

A benchmark harness should include a preflight/self-test that can detect obvious cross-arm contamination before expensive runs begin.

### 8. Publish negative results and corrected claims

Ponytail's benchmark write-up documents an earlier inflated baseline and narrows its public claim after criticism. SpecGrainBench should adopt this evidence culture:

- report tasks where SpecGrain ties or loses;
- report limitations and invalidated runs;
- preserve failed runs;
- correct public claims when benchmark design changes;
- design experiments that can falsify the product hypothesis.

### 9. Keep the useful Spec Kit gates, not its hierarchy assumptions

Spec Kit contributes several useful planning patterns:

- explicit technical context;
- constitution checks before design and re-checks after design;
- independent testability of delivery slices;
- explicit dependencies and parallel opportunities;
- complexity deviations that require justification.

SpecGrain should preserve these ideas as policy/context/readiness/graph concepts while avoiding a mandatory `feature -> plan -> flat tasks` terminal model.

The SpecGrain-native model remains:

```text
Intent
  -> SpecNode
      -> SpecNode
          -> Grain

Grain -> WorkPacket -> Execution -> Verification -> Evidence
```

## Rejected adoptions

The review does **not** justify:

- adding Ponytail or Karpathy guidelines as mandatory prompt text;
- copying their agent personalities;
- making LOC minimization a primary objective;
- adding a new dependency;
- replacing deterministic SpecGrain gates with prompt compliance;
- recreating Spec Kit's user-story/task taxonomy in the core;
- expanding the current implementation specification merely because a donor has adjacent features.

## Planning consequences

The roadmap remains progressively refined. The strongest donor-derived requirements should enter only when their owning specification becomes active:

- `003`: structural refinement only; no semantic/AI overreach;
- `004`: readiness, explicit success criteria, unresolved-decision and minimality/safety floors;
- `007/008`: repository understanding and context evidence before execution;
- `009`: surgical WorkPacket with authorized surface and relevant decisions;
- `010`: independent acceptance/scope evidence;
- `012`: unnecessary-change and scope-accuracy metrics;
- `015`: contamination-resistant, falsifiable benchmark harness.
