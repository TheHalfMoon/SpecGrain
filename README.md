# SpecGrain

**Make every software change small enough to understand, execute, verify, and prove.**

SpecGrain is an open-source, AI-native software delivery system built around recursively refined specifications. Instead of turning a large specification directly into a long task list, SpecGrain keeps decomposing work into smaller specifications until each leaf is independently valuable, context-safe, bounded, and verifiable.

> Big ideas. Small specs. Proven software.

## Status

SpecGrain is in its foundation and methodology design phase. The repository will develop in public from a written constitution, explicit domain model, measurable quality gates, and reproducible benchmarks.

## Core idea

```text
Intent
  -> Spec
      -> Spec
          -> Grain
          -> Grain
      -> Spec
          -> Grain

Grain -> Execute -> Verify -> Evidence -> Measure -> Improve
```

A **Grain** is the smallest independently valuable, context-safe, reversible, and verifiable unit of software delivery.

## Principles

- Recursive refinement instead of giant up-front specifications.
- Small-batch delivery instead of long agent runs.
- Evidence instead of self-declared completion.
- Explicit dependencies instead of flat task lists.
- Context budgets instead of unlimited prompt growth.
- Adaptive planning instead of ceremony by default.
- Measured flow and quality instead of vanity activity metrics.
- Human and agent interoperability instead of vendor lock-in.
- Brownfield repositories as a first-class use case.
- Compatibility with existing spec-driven workflows, including GitHub Spec Kit, without being architecturally dependent on them.

## Project direction

SpecGrain is an independent project. GitHub Spec Kit is an important upstream influence, compatibility target, and potential source of MIT-licensed implementation patterns, but SpecGrain uses a different core model: recursive specifications, execution graphs, readiness gates, context isolation, independent verification, and an evidence ledger.

Detailed specifications, architecture, roadmap, benchmark methodology, and execution tasks are being added next.
