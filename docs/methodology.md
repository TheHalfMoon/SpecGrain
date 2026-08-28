# SpecGrain Methodology

## Purpose

SpecGrain combines useful ideas from Agile, Lean, PMI project-management practice, Six Sigma, DevOps, software verification, and evidence-backed coding-agent practice without forcing a single ceremony framework.

The methodology exists to improve value, flow, clarity, evidence, and learning. Any ceremony that does not improve one of those outcomes is optional.

## 1. Progressive refinement

Long-range work should remain coarse until better evidence exists. Near-term work becomes detailed only when it is likely to execute soon.

This adapts rolling-wave planning and progressive elaboration to agentic development:

```text
Later:   broad intent
Next:    shaped specs
Now:     verified-ready Grains
```

The system should resist generating hundreds of detailed future tasks that will become stale.

## 2. Small-batch Agile and Lean flow

Core flow principles:

- reduce batch size;
- limit concurrent work;
- make blockers visible;
- prefer independently deliverable slices;
- shorten feedback loops;
- remove non-value-added documentation and repeated analysis;
- optimize whole-system flow rather than agent utilization.

A Grain is the mechanism that turns these principles into a machine-checkable delivery boundary.

### 2.1 Understand before minimizing

Small does not mean careless. Before optimizing implementation size, the delivery process should understand the outcome and relevant repository flow, then prefer the first sufficient option:

1. do not build work that is not necessary for the outcome;
2. reuse an existing repository capability or pattern when it already satisfies the need;
3. prefer standard-library or native platform capability when sufficient;
4. prefer an already-approved/installed dependency over a redundant custom implementation when appropriate;
5. only then add the minimum new implementation that satisfies acceptance.

This ladder is a planning heuristic until deterministic repository evidence exists. It must never justify removing required security, trust-boundary validation, accessibility, data-loss protection, recovery, or explicit acceptance behavior.

### 2.2 Surgical change

Every changed line or file should trace to the active Grain's outcome, acceptance, or required supporting change. Adjacent cleanup, speculative abstractions, unrelated refactors, and pre-existing dead-code removal belong in separate specs unless the active change actually requires them.

`change_surface`, WorkPackets, verification, and later diff tooling should make this rule machine-checkable instead of depending only on prompt discipline.

### 2.3 Goal-driven execution

Execution should optimize for verified success criteria rather than blindly following procedural instructions. A Grain defines the outcome and acceptance evidence; an executor may choose implementation details within authorized boundaries; verification independently determines whether the result satisfies the contract.

Decision-relevant uncertainty must be surfaced before execution when it can materially change scope, safety, architecture, or acceptance. SpecGrain does not require private reasoning transcripts.

## 3. PMP-inspired governance

SpecGrain uses project-management concepts where they add control:

- charter-like product intent;
- decomposition of scope;
- explicit dependencies;
- risk ownership;
- stakeholder/consumer context when relevant;
- progressive planning;
- change control through spec revisions;
- lessons learned through process metrics and evidence.

It intentionally avoids making formal PMP artifacts mandatory for ordinary software work.

## 4. Six Sigma-inspired evidence loops

### DMADV-lite

Use for meaningful new capabilities where the target behavior does not yet exist.

- **Define:** outcome, customer/user value, boundaries.
- **Measure:** baseline and success signals.
- **Analyze:** constraints, dependencies, alternatives, failure modes.
- **Design:** refine into executable Grains.
- **Verify:** prove the implemented result against acceptance and evidence requirements.

### DMAIC-lite

Use for defects, regressions, reliability problems, or process improvements.

- **Define:** observed failure or performance gap.
- **Measure:** reproducible baseline.
- **Analyze:** evidence-backed cause.
- **Improve:** smallest corrective Grain set.
- **Control:** regression evidence and, when justified, post-change monitoring criteria.

These profiles should be lightweight metadata and gates, not document factories.

## 5. Quick flow

Use for small, already-understood changes with low risk. Quick flow still requires a bounded outcome, acceptance, scope, and evidence, but skips analysis fields that add no value.

## 6. Experiment flow

Use when uncertainty is the primary problem. An experiment spec should define:

- hypothesis;
- evidence to collect;
- time/resource boundary;
- decision rule;
- what is explicitly not productionized.

The output is evidence and a decision, not necessarily production code.

## 7. Controlled flow

Use for high-risk, security-sensitive, migration-heavy, compliance-relevant, or difficult-to-reverse work. It may require:

- stronger review separation;
- explicit rollback proof;
- migration rehearsal;
- security checks;
- additional provenance;
- staged verification or post-change control.

## 8. Method router

Initial deterministic routing inputs:

- work class: new, defect, refactor, experiment, migration, security, documentation;
- risk level;
- reversibility;
- production blast radius;
- uncertainty;
- external/regulatory constraints.

The router may recommend a profile. Repositories may override with policy, but the override must be explicit.

## 9. Metrics

Start with a small metric set:

1. First-Pass Verification Rate.
2. Rework Ratio.
3. Grain Cycle Time.
4. Context Efficiency.
5. Spec Drift Rate.
6. Escaped Defect Rate.
7. Change-Scope Accuracy.

Metrics should help diagnose process quality. They must not become productivity scores for individuals.

## 10. Waste model

SpecGrain should eventually identify AI-delivery waste patterns such as:

- overproduction: changed files or abstractions not needed by the Grain;
- overprocessing: repeated planning or unnecessary layers;
- waiting: avoidable dependency or review delay;
- rework: repeated implementation caused by weak shaping;
- context waste: loaded context unrelated to the Grain;
- defects: failed acceptance or escaped regressions;
- drift: implementation or documentation no longer matches canonical specs.

The first releases should measure only waste that can be computed reliably.

## Research note

The minimality, surgical-change, goal-driven, and benchmark implications above are derived in `docs/research/planning-donor-synthesis-2026-08-28.md`. They are design inputs, not copied donor code or mandatory vendor-specific prompt text.
