# SpecGrainBench Strategy

## Goal

Build an open benchmark for measuring whether software-delivery methods help humans and coding agents produce correct, scoped, efficient changes on real repositories.

The benchmark is also the primary mechanism for validating SpecGrain's product claims.

## Principles

- Same task, repository baseline, and acceptance oracle across compared methods.
- Same model/provider configuration when model-based systems are compared.
- Multiple repetitions for probabilistic systems.
- Raw run metadata and evaluation logic should be publishable when licenses permit.
- No benchmark claim without a reproducible harness.
- Prefer outcome metrics over document-volume metrics.

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
- specification change after partial implementation.

## Metrics

### Outcome quality

- acceptance pass rate;
- regression rate;
- hidden-test correctness where legally and technically appropriate;
- scope compliance;
- requirement coverage.

### Delivery efficiency

- wall-clock time where comparable;
- model input/output tokens where available;
- number of retries;
- number of human interventions;
- changed lines/files;
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
- scoring code version.

## Anti-gaming rules

- Benchmark fixtures must not be embedded into prompts as answers.
- Hidden evaluation data must not be shipped to the implementation agent when secrecy is necessary for validity.
- Method-specific manual rescue should be recorded as intervention, not silently normalized away.
- Failed runs remain in the dataset.

## Early benchmark hypothesis

SpecGrain should first attempt to validate narrow hypotheses rather than claim universal superiority:

1. Smaller verified Grains reduce unnecessary changed files on multi-part tasks.
2. Explicit Grain dependencies reduce order-related implementation failures.
3. Context-scoped packets reduce irrelevant context compared with whole-feature execution.
4. Independent verification catches self-declared completion failures.
5. Progressive refinement reduces stale detailed work in changing requirements.

A hypothesis that fails should change the product, not be hidden.
