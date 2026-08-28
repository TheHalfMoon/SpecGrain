# Product Thesis

## Thesis

SpecGrain is an open-source delivery control plane for humans and AI coding agents. Its core belief is simple: software work becomes safer and more reliable when every executable change is small enough to understand, contextually isolate, verify independently, recover, and prove.

The product does not treat a specification as a one-time document that is later converted into a flat task list. A specification is recursive. If a spec is too broad to execute safely, it is refined into smaller specs. This continues until a leaf passes the Definition of Grain.

## Problem

Modern spec-driven and agentic development tools improve planning, but large changes still commonly suffer from:

- long, stale specification documents;
- up-front task explosion;
- context dilution and context rot;
- hidden dependencies;
- agents modifying adjacent code outside the intended scope;
- self-declared completion without durable proof;
- expensive rework after late discovery;
- weak linkage between requirements, code, tests, commits, and verification;
- process frameworks that add ceremony without improving outcomes.

Increasing model context windows does not eliminate these problems. It often hides the need to reduce batch size and clarify boundaries.

## Product promise

SpecGrain should make it natural to answer five questions for every change:

1. What outcome is this change responsible for?
2. Is it small and clear enough to execute safely?
3. What does it depend on and what may it change?
4. What evidence proves it works?
5. What did the delivery process teach us for the next change?

## Core primitive

A `SpecNode` is the single recursive planning primitive.

A `Grain` is not a separate planning object. It is a leaf `SpecNode` that has passed the Grain readiness contract and is therefore eligible for execution once its dependencies are satisfied.

```text
Intent
  -> SpecNode
      -> SpecNode
          -> Grain
          -> Grain
      -> SpecNode
          -> Grain

Grain -> Work Packet -> Execution -> Verification -> Evidence -> Learning
```

This avoids mandatory taxonomies such as epic/feature/story/task/subtask while still allowing organizations to add labels or views if they want them.

## Target users

### Individual developers

Developers using AI coding assistants on real repositories who want smaller changes, less drift, and trustworthy completion evidence.

### Agent builders

Teams building coding-agent systems that need a model-neutral specification, scheduling, and verification contract.

### Engineering teams

Teams that want traceable requirements-to-change evidence without adopting a heavyweight project-management suite.

### Regulated or high-trust teams

Organizations that need explicit scope, provenance, risk, and verification records for software changes.

## Product boundaries

SpecGrain is not intended to become:

- a Jira clone;
- a Scrum ceremony manager;
- a generic note-taking tool;
- a hosted-only platform;
- an LLM vendor;
- an IDE replacement;
- a personality-based multi-agent framework;
- a giant prompt library.

The core is local-first, deterministic where trust matters, and integration-neutral.

## Differentiation

The product wins through the combination of:

- recursive spec refinement;
- deterministic Grain readiness gates;
- dependency-aware execution planning;
- context budgets and scoped work packets;
- independent verification;
- evidence ledgers bound to exact revisions;
- process-quality metrics and waste detection;
- brownfield-first repository intelligence;
- migration and interoperability with existing spec-driven workflows.

No single feature is sufficient. The system must make these capabilities feel like one coherent delivery model.

## MVP proof

The first useful vertical slice must demonstrate this end to end:

```text
existing repository
  -> create intent
  -> recursively refine
  -> identify one READY Grain
  -> generate bounded work packet
  -> record implementation revision
  -> verify acceptance + scope + tests
  -> emit durable evidence record
```

The MVP does not require autonomous agent execution. Producing a portable work packet and accepting a result is enough to prove the core abstraction before building many adapters.

## Long-term position

SpecGrain should become the portable operating layer between intent and implementation for agentic software delivery. Tickets, GitHub issues, prompts, incidents, or product requests may enter from different systems, but SpecGrain should normalize them into small, measurable, provable change units.
