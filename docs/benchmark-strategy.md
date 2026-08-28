# SpecGrainBench Strategy

## Goal

Build an open benchmark for measuring whether software-delivery methods help humans and coding agents produce correct, scoped, efficient changes on real repositories.

The benchmark is also the primary mechanism for validating SpecGrain's product claims.

## Principles

- Same task, repository baseline, and acceptance oracle across compared methods.
- Same model/provider configuration when model-based systems are compared.
- Multiple repetitions for probabilistic systems.
- Each arm receives a fresh repository workspace and fresh agent context/process.
- Method-specific plugins, hooks, skills, rules, and global configuration must be isolated and recorded.
- Raw run metadata and evaluation logic should be publishable when licenses permit.
- No benchmark claim without a reproducible harness.
- Prefer repository outcome metrics over answer/prose volume.
- Publish ties, losses, failed runs, limitations, and corrected claims rather than filtering them away.

## Initial methods

First milestone:

1. prompt-only baseline;
2. GitHub Spec Kit baseline;
3. SpecGrain.

Later, add OpenSpec, BMAD, OpenAgile.AI, or other methods only where a fair automated protocol can be defined.

## Task classes

- localized bug fix;
- small new capability;
- cross-cutting feature;
- refactor with behavioral invariants;
- brownfield change in an unfamiliar repository;
- dependency or migration change;
- specification change after partial implementation;
- safety-sensitive surgical change where minimizing code could remove a required guard.

## Metrics

### Outcome quality

- acceptance pass rate;
- regression rate;
- hidden-test correctness where legally and technically appropriate;
- scope compliance;
- requirement coverage;
- explicit safety/adversarial check pass rate for applicable cases.

### Delivery efficiency

- wall-clock time where comparable;
- model input/output tokens where available;
- number of retries;
- number of human interventions;
- changed lines/files measured from repository diff;
- rework ratio.

### Process quality

- first-pass verification rate;
- spec drift;
- dependency-order violations;
- unnecessary change rate;
- context utilization/efficiency;
- recovery cost after an induced failure.

## Experimental controls

Each benchmark case should define:

- immutable repository snapshot;
- task intent;
- acceptance oracle;
- allowed and forbidden surfaces where applicable;
- environment image or reproducible setup;
- time/resource caps;
- model configuration;
- seed/repetition policy;
- scoring code version;
- exact method/plugin/skill configuration;
- inherited/global configuration policy.

Each `(task, method, repetition)` cell should use a fresh workspace and fresh agent context. No conversation history, method-specific hook, plugin state, or generated artifact may leak from another arm unless the experiment explicitly studies persistence.

## Contamination preflight

Before expensive benchmark runs, the harness should perform a self-test that can detect obvious arm contamination, including:

- a baseline unexpectedly loading a method-specific plugin/skill/hook;
- shared writable state between arms;
- reused agent conversation/session identifiers;
- repository workspaces that are not reset to the pinned snapshot;
- scorer fixtures visible to the implementation agent when they should be hidden.

A contamination failure invalidates the affected comparison; it must not be averaged into published results.

## Anti-gaming rules

- Benchmark fixtures must not be embedded into prompts as answers.
- Hidden evaluation data must not be shipped to the implementation agent when secrecy is necessary for validity.
- Method-specific manual rescue should be recorded as intervention, not silently normalized away.
- Failed runs remain in the dataset.
- Do not score generated prose length as a proxy for implementation size; use repository artifacts/diffs.
- Safety-sensitive cases must not reward smaller changes that fail the required safety oracle.

## Early benchmark hypotheses

SpecGrain should first attempt to validate narrow hypotheses rather than claim universal superiority:

1. Smaller verified Grains reduce unnecessary changed files on multi-part tasks.
2. Explicit Grain dependencies reduce order-related implementation failures.
3. Context-scoped packets reduce irrelevant context compared with whole-feature execution.
4. Independent verification catches self-declared completion failures.
5. Progressive refinement reduces stale detailed work in changing requirements.
6. Explicit authorized change surfaces reduce drive-by edits without reducing acceptance pass rate.
7. Minimality/reuse discipline can reduce implementation size without reducing safety/validation pass rates.

A hypothesis that fails should change the product, not be hidden.

## Research influence

The benchmark-isolation and repository-diff principles are strengthened by the Ponytail agentic benchmark review recorded in `docs/research/planning-donor-synthesis-2026-08-28.md`, especially its documented baseline-contamination failure and subsequent correction.
