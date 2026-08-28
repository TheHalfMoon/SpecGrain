# Roadmap

The roadmap is intentionally progressive. Only the nearest specification should have implementation-level detail.

## M0 — Foundation

**Spec:** `000-foundation`

Define constitution, product thesis, domain model, architecture, methodology, competitive boundaries, donor policy, benchmark strategy, launch thesis, and the next-spec sequence.

Exit: internally consistent foundation merged to canonical `main`.

## M1 — Core Model

**Planned spec:** `001-core-model`

Implement deterministic models for SpecNode, lifecycle state, Grain readiness inputs, dependency references, normalized serialization, and content digests.

Exit: a recursive spec tree can be loaded, validated, normalized, and classified without AI.

## M2 — Grain Readiness

**Planned spec:** `002-grain-readiness`

Implement deterministic Grain gates, explainable failures, method-profile hooks, and refinement recommendations as structured output.

Exit: invalid candidate leaves cannot become Grains.

## M3 — CLI and Local Store

**Planned spec:** `003-cli-store`

Implement `init`, `check`, state storage, IDs/revisions, and human-readable terminal rendering.

Exit: a user can create and inspect a valid repository-local SpecGrain project.

## M4 — Dependency Graph and Scheduler

**Planned spec:** `004-graph-scheduler`

Implement DAG validation, cycle detection, ready-set computation, blocker propagation, and deterministic execution-wave planning.

Exit: `next` returns only genuinely eligible Grains.

## M5 — Brownfield Context

**Planned spec:** `005-repository-context`

Implement repository scan, deterministic repository map, context-source records, context-size accounting, and budget gates.

Exit: a Grain can carry a reproducible bounded context packet from an existing repository.

## M6 — Work Packets

**Planned spec:** `006-work-packets`

Implement immutable portable WorkPackets and structured execution-result ingestion.

Exit: a human or external agent can execute a Grain without depending on internal SpecGrain prompts.

## M7 — Verification and Evidence

**Planned spec:** `007-evidence-verification`

Implement evidence records, exact-revision binding, acceptance/check results, changed-scope verification, and `prove` output.

Exit: an implementation cannot become `VERIFIED` through executor assertion alone.

**This is the first complete MVP vertical slice.**

## M8 — Adaptive Method Profiles

**Planned spec:** `008-method-profiles`

Implement quick, DMAIC-lite, DMADV-lite, experiment, and controlled profile extensions to readiness/evidence.

## M9 — Drift, Diff, and Metrics

**Planned spec:** `009-control-metrics`

Implement spec/code drift signals, spec-aware diff, rework, first-pass verification, cycle-time, context-efficiency, and scope-accuracy metrics.

## M10 — Spec Kit Migration

**Planned spec:** `010-speckit-import`

Import relevant Spec Kit project artifacts into SpecGrain state with explicit conversion reports and no silent data loss.

## M11 — Agent Adapters

**Planned spec:** `011-agent-adapters`

Add thin integrations beginning with a generic stdout/file protocol, then selected popular coding agents based on demand.

## M12 — SpecGrainBench

**Planned spec:** `012-benchmark`

Build reproducible prompt-only, Spec Kit, and SpecGrain comparisons.

## M13 — Public Launch

Documentation, examples, recorded terminal demo, benchmark results, contribution guides, release packaging, and community launch.

## Explicitly deferred

Until evidence justifies them:

- web dashboard;
- hosted SaaS;
- own LLM or fine-tuning;
- marketplace;
- enterprise account system;
- visual workflow designer;
- large agent-persona catalog.
