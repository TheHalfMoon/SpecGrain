# Roadmap

The roadmap is intentionally progressive. Only the nearest specification should have implementation-level detail. Later entries are sequencing hypotheses and may be refined as evidence changes.

## M0 — Foundation

**Spec:** `000-foundation`

Define constitution, product thesis, domain model, architecture, methodology, competitive boundaries, donor policy, benchmark strategy, launch thesis, and the next-spec sequence.

Exit: internally consistent foundation merged to canonical `main`.

## M1 — Deterministic specification kernel

### 001 — SpecNode Schema

Define and implement only the canonical recursive `SpecNode` data model, stable IDs, normalized serialization, and revision digest.

Exit: a SpecNode can round-trip deterministically and identical semantic content yields identical canonical form/digest.

### 002 — Lifecycle State

Implement legal lifecycle states and deterministic transition validation independently of CLI or execution adapters.

Exit: illegal transitions are rejected with explainable errors.

### 003 — Refinement Tree

Implement parent/child structural rules, tree integrity, child ordering semantics where needed, and detection of malformed recursive structures.

Exit: a recursive spec forest can be loaded and structurally validated without AI.

### 004 — Grain Readiness

Implement the deterministic Definition of Grain contract and structured readiness failures.

Exit: a leaf cannot become `GRAIN` unless all required machine-checkable readiness conditions pass.

## M2 — Local product surface

### 005 — CLI and Local Store

Implement `init`, `check`, repository-local `.specgrain/` storage, project policy loading, and readable terminal output.

Exit: a user can initialize and validate a local SpecGrain project.

### 006 — Dependency Graph

Implement dependency references, cycle detection, ready-set computation, blocker propagation, and deterministic wave projection.

Exit: `next` can identify only genuinely eligible Grains from local state.

## M3 — Brownfield context

### 007 — Repository Scan

Implement a deterministic repository map from manifests, layout, test/config signals, and version-control facts.

Exit: SpecGrain can describe an existing repository without sending the whole repository to an LLM.

### 008 — Context Budget

Implement context-source records, selection reasons, size accounting, mandatory/optional classification, and budget validation.

Exit: required context that cannot fit policy can block Grain readiness with an explainable result.

## M4 — Portable execution boundary

### 009 — Work Packet

Implement immutable, digest-bound WorkPackets and a generic structured execution-result contract.

Exit: a human or external agent can receive all authorized Grain context without depending on SpecGrain-internal prompt text.

### 010 — Verification and Evidence

Implement exact-revision evidence records, acceptance/check results, changed-scope verification, result binding, and `prove` output.

Exit: executor assertion alone cannot produce `VERIFIED`.

**This closes the first complete MVP vertical slice.**

## M5 — Adaptive delivery control

### 011 — Method Profiles

Implement `quick`, `dmaic-lite`, `dmadv-lite`, `experiment`, and `controlled` profiles as incremental readiness/evidence requirements.

### 012 — Diff, Drift, and Metrics

Implement spec-aware change-surface diff, basic drift signals, first-pass verification, rework ratio, Grain cycle time, context efficiency, and scope accuracy.

## M6 — Ecosystem interoperability

### 013 — Spec Kit Import

Import relevant Spec Kit artifacts into SpecGrain state with explicit conversion reports and no silent data loss.

### 014 — Agent Adapters

Add thin integrations beginning with the generic packet/result protocol, then selected coding-agent adapters based on real adoption demand.

## M7 — Public proof

### 015 — SpecGrainBench

Build reproducible prompt-only, Spec Kit, and SpecGrain benchmark comparisons. Add other methods only where fair automation is possible.

### 016 — Public Launch

Ship installable releases, examples, terminal demo, benchmark report, migration guide, contribution paths, security documentation, and launch assets.

## Explicitly deferred

Until evidence justifies them:

- web dashboard;
- hosted SaaS;
- own LLM or fine-tuning;
- marketplace;
- enterprise account system;
- visual workflow designer;
- large agent-persona catalog.
